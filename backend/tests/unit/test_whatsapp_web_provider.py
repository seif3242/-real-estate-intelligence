from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
from playwright.async_api import async_playwright

from app.collector.providers.base import CollectedContentType, ExtractedMessage
from app.collector.providers.exceptions import GroupListingUnavailableError, GroupNotFoundError
from app.collector.providers.whatsapp_web import (
    _GROUP_LOOKUP_SCRIPT,
    _READ_MESSAGES_SCRIPT,
    WhatsAppWebProvider,
)

# Minimal synthetic stand-in for WhatsApp Web's real webpack bundle: a
# `webpackChunk*` array whose `push` mimics webpack's real chunk-registration
# behavior closely enough to exercise `_GROUP_LOOKUP_SCRIPT` and
# `_READ_MESSAGES_SCRIPT` end-to-end, without depending on a live WhatsApp Web
# session. "Group One" carries a `msgs` collection (with a `loadEarlierMsgs`
# that yields two older messages exactly once, then is exhausted) so the
# message-reading pagination loop has something real to exercise.
_MOCK_CHAT_STORE_HTML = """
<!DOCTYPE html>
<html>
<head>
<script>
window.webpackChunktest_app = {
  modules: {},
  push: function (args) {
    const [, moreModules, entry] = args;
    Object.assign(this.modules, moreModules);
    const cache = {};
    const self = this;
    const req = function (id) {
      if (cache[id]) return cache[id].exports;
      const module = { exports: {} };
      cache[id] = module;
      self.modules[id](module, module.exports, req);
      return module.exports;
    };
    req.m = this.modules;
    entry(req);
  }
};

window.webpackChunktest_app.push([
  ["main"],
  {
    "modA": function (module, exports) {
      exports.default = { irrelevant: true };
    },
    "modB": function (module, exports) {
      let recentMsgs = [
        { type: "chat", t: 1700000000, body: "Hello everyone",
          author: "201111111111@c.us", senderObj: { pushname: "John" } },
        { type: "chat", t: 1700000100, body: "مرحبا بالجميع",
          author: "201222222222@c.us", senderObj: { name: "سارة" } },
        { type: "document", mimetype: "application/pdf", filename: "brochure.pdf",
          t: 1700000200, author: "201333333333@c.us",
          senderObj: { formattedName: "Property Bot" } },
        { type: "image", t: 1700000300, author: "201444444444@c.us" },
      ];
      let earlierLoaded = false;
      const msgsCollection = {
        getModelsArray: function () { return recentMsgs; },
      };
      const groupOne = {
        id: { server: "g.us", user: "1111" },
        name: "Group One",
        formattedTitle: "Group One",
        msgs: msgsCollection,
        setActive: function () {},
        loadEarlierMsgs: async function () {
          if (earlierLoaded) {
            return;
          }
          earlierLoaded = true;
          recentMsgs = [
            { type: "chat", t: 1699999800, body: "Older message 1",
              author: "201555555555@c.us", senderObj: null },
            { type: "chat", t: 1699999900, body: "Older message 2",
              author: "201666666666@c.us", senderObj: null },
          ].concat(recentMsgs);
        },
      };
      const chats = [
        groupOne,
        { id: { server: "g.us", user: "2222" }, name: "Group With Photo",
          formattedTitle: "Group With Photo", hasCustomPhoto: true },
        { id: { server: "c.us", user: "3333" }, name: "John Doe", formattedTitle: "John Doe" },
      ];
      exports.default = { Chat: { getModelsArray: function () { return chats; } } };
    },
  },
  function (require) {},
]);
</script>
</head>
<body></body>
</html>
"""

_NO_CHAT_STORE_HTML = "<!DOCTYPE html><html><head></head><body></body></html>"


@pytest.mark.asyncio
async def test_group_lookup_script_returns_only_groups_including_custom_photo() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(_MOCK_CHAT_STORE_HTML)

        result = await page.evaluate(_GROUP_LOOKUP_SCRIPT)

        await browser.close()

    assert result == ["Group One", "Group With Photo"]


@pytest.mark.asyncio
async def test_group_lookup_script_returns_none_when_chat_store_not_found() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(_NO_CHAT_STORE_HTML)

        result = await page.evaluate(_GROUP_LOOKUP_SCRIPT)

        await browser.close()

    assert result is None


@pytest.mark.asyncio
async def test_read_messages_script_paginates_and_classifies_message_types() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(_MOCK_CHAT_STORE_HTML)

        result = await page.evaluate(_READ_MESSAGES_SCRIPT, {"groupName": "Group One", "limit": 10})

        await browser.close()

    assert "error" not in result
    messages = result["messages"]
    # loadEarlierMsgs() pulled in the two older messages exactly once.
    assert len(messages) == 6

    older_one, older_two, hello, arabic, pdf, image = messages

    assert older_one["sender_name"] == "201555555555"  # no senderObj: falls back to author
    assert older_two["sender_name"] == "201666666666"

    assert hello["sender_name"] == "John"
    assert hello["message_type"] == "text"
    assert hello["message_text"] == "Hello everyone"
    assert hello["pdf_file_name"] is None

    assert arabic["sender_name"] == "سارة"
    assert arabic["message_type"] == "text"
    assert arabic["message_text"] == "مرحبا بالجميع"

    assert pdf["sender_name"] == "Property Bot"
    assert pdf["message_type"] == "pdf"
    assert pdf["message_text"] is None
    assert pdf["pdf_file_name"] == "brochure.pdf"

    assert image["message_type"] == "unsupported"
    assert image["message_text"] is None
    assert image["pdf_file_name"] is None


@pytest.mark.asyncio
async def test_read_messages_script_respects_limit() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(_MOCK_CHAT_STORE_HTML)

        result = await page.evaluate(_READ_MESSAGES_SCRIPT, {"groupName": "Group One", "limit": 2})

        await browser.close()

    messages = result["messages"]
    assert len(messages) == 2
    assert messages[-1]["message_type"] == "unsupported"  # newest message kept


@pytest.mark.asyncio
async def test_read_messages_script_returns_group_not_found() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(_MOCK_CHAT_STORE_HTML)

        result = await page.evaluate(
            _READ_MESSAGES_SCRIPT, {"groupName": "Does Not Exist", "limit": 10}
        )

        await browser.close()

    assert result == {"error": "group_not_found"}


@pytest.mark.asyncio
async def test_read_messages_script_returns_store_unavailable() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(_NO_CHAT_STORE_HTML)

        result = await page.evaluate(_READ_MESSAGES_SCRIPT, {"groupName": "Group One", "limit": 10})

        await browser.close()

    assert result == {"error": "store_unavailable"}


@pytest.mark.asyncio
async def test_list_groups_raises_when_chat_store_unavailable() -> None:
    provider = WhatsAppWebProvider(session_path="/tmp/unused-session")
    provider._page = AsyncMock()
    provider._page.evaluate = AsyncMock(return_value=None)

    with (
        patch.object(WhatsAppWebProvider, "is_connected", AsyncMock(return_value=True)),
        pytest.raises(GroupListingUnavailableError),
    ):
        await provider.list_groups()


@pytest.mark.asyncio
async def test_list_groups_returns_names_from_chat_store() -> None:
    provider = WhatsAppWebProvider(session_path="/tmp/unused-session")
    provider._page = AsyncMock()
    provider._page.evaluate = AsyncMock(return_value=["Group One", "Group With Photo", ""])

    with patch.object(WhatsAppWebProvider, "is_connected", AsyncMock(return_value=True)):
        groups = await provider.list_groups()

    assert groups == ["Group One", "Group With Photo"]


@pytest.mark.asyncio
async def test_read_recent_messages_raises_when_store_unavailable() -> None:
    provider = WhatsAppWebProvider(session_path="/tmp/unused-session")
    provider._page = AsyncMock()
    provider._page.evaluate = AsyncMock(return_value={"error": "store_unavailable"})

    with (
        patch.object(WhatsAppWebProvider, "is_connected", AsyncMock(return_value=True)),
        pytest.raises(GroupListingUnavailableError),
    ):
        await provider.read_recent_messages("Group One")


@pytest.mark.asyncio
async def test_read_recent_messages_raises_when_group_not_found() -> None:
    provider = WhatsAppWebProvider(session_path="/tmp/unused-session")
    provider._page = AsyncMock()
    provider._page.evaluate = AsyncMock(return_value={"error": "group_not_found"})

    with (
        patch.object(WhatsAppWebProvider, "is_connected", AsyncMock(return_value=True)),
        pytest.raises(GroupNotFoundError),
    ):
        await provider.read_recent_messages("Does Not Exist")


@pytest.mark.asyncio
async def test_read_recent_messages_maps_script_output_to_extracted_messages() -> None:
    provider = WhatsAppWebProvider(session_path="/tmp/unused-session")
    provider._page = AsyncMock()
    provider._page.evaluate = AsyncMock(
        return_value={
            "messages": [
                {
                    "sender_name": "John",
                    "timestamp": 1700000000000,
                    "message_type": "text",
                    "message_text": "Hello everyone",
                    "pdf_file_name": None,
                },
                {
                    "sender_name": "Property Bot",
                    "timestamp": None,
                    "message_type": "pdf",
                    "message_text": None,
                    "pdf_file_name": "brochure.pdf",
                },
            ]
        }
    )

    with patch.object(WhatsAppWebProvider, "is_connected", AsyncMock(return_value=True)):
        messages = await provider.read_recent_messages("Group One", limit=10)

    assert messages == [
        ExtractedMessage(
            sender_name="John",
            timestamp=datetime.fromtimestamp(1700000000, tz=UTC),
            message_type=CollectedContentType.TEXT,
            message_text="Hello everyone",
            pdf_file_name=None,
        ),
        ExtractedMessage(
            sender_name="Property Bot",
            timestamp=None,
            message_type=CollectedContentType.PDF,
            message_text=None,
            pdf_file_name="brochure.pdf",
        ),
    ]
    provider._page.evaluate.assert_awaited_once_with(
        _READ_MESSAGES_SCRIPT, {"groupName": "Group One", "limit": 10}
    )
