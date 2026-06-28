from unittest.mock import AsyncMock, patch

import pytest
from playwright.async_api import async_playwright

from app.collector.providers.exceptions import GroupListingUnavailableError
from app.collector.providers.whatsapp_web import _GROUP_LOOKUP_SCRIPT, WhatsAppWebProvider

# Minimal synthetic stand-in for WhatsApp Web's real webpack bundle: a
# `webpackChunk*` array whose `push` mimics webpack's real chunk-registration
# behavior closely enough to exercise `_GROUP_LOOKUP_SCRIPT` end-to-end,
# without depending on a live WhatsApp Web session.
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
      const chats = [
        { id: { server: "g.us", user: "1111" }, name: "Group One", formattedTitle: "Group One" },
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
