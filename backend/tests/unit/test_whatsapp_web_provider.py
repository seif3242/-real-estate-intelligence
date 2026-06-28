from app.collector.providers.whatsapp_web import _is_group_row


def test_is_group_row_true_for_default_group_icon() -> None:
    assert _is_group_row(["default-group"]) is True


def test_is_group_row_true_for_refreshed_group_icon() -> None:
    assert _is_group_row(["default-group-refreshed"]) is True


def test_is_group_row_false_for_contact_icon() -> None:
    assert _is_group_row(["default-user"]) is False


def test_is_group_row_false_for_no_icons() -> None:
    assert _is_group_row([]) is False
