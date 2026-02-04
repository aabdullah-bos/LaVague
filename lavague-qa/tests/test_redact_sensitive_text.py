import math

from lavague.qa.utils import redact_sensitive_text


def test_redact_sensitive_text_handles_nan():
    assert redact_sensitive_text(math.nan) == ""


def test_redact_sensitive_text_handles_none():
    assert redact_sensitive_text(None) == ""


def test_redact_sensitive_text_preserves_non_secret_text():
    assert redact_sensitive_text("hello world") == "hello world"


def test_redact_sensitive_text_redacts_send_keys_with_marker_context():
    text = "password\n    element.send_keys('hunter2')"
    assert redact_sensitive_text(text) == "password\n    element.send_keys('[REDACTED]')"
