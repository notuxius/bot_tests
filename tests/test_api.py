import pytest
import requests


# Methods that are used in API tests:
def _make_post_receive_response(url_port_endp, user_action, feedback):
    return requests.post(
        url_port_endp, json={"user_action": user_action, "feedback": feedback}
    )


# API Tests:
@pytest.mark.parametrize(
    "user_action, feedback",
    [
        ("0", 'Testing API valid "0" user action ~!@#$%^&*()_+{}|:<>?,./;\'[]\\|=-`'),
        ("1", 'Testing API valid "1" user action'),
        ("2", 'Testing API valid "2" user action'),
        ("3", 'Testing API valid "3" user action'),
        ("4", 'Testing API valid "4" user action'),
        ("5", 'Testing API valid "5" user action'),
        ("6", 'Testing API valid "6" user action'),
        ("7", ""),
        ("8", ""),
        ("9", ""),
        ("10", ""),
    ],
)
def test_valid_user_action(url_port_endp, user_action, feedback):
    resp = _make_post_receive_response(url_port_endp[0], user_action, feedback)
    assert resp.status_code == 200
