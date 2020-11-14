import pytest


@pytest.mark.parametrize(
    "action_type, input_text, response_text",
    [
        (
            "enter_text",
            "HELLO_INPUT_TEXT",
            "HELLO_RESPONSE_TEXT",
        )
    ],
)
@pytest.mark.web
@pytest.mark.smoke
def test_hello_response(
    bot_chat_window, action_type, inputs, responses, input_text, response_text
):
    bot_chat_window.make_action(action_type, inputs[input_text])
    assert bot_chat_window.actual_response_text(
        inputs, responses
    ) == bot_chat_window.expected_response_text(inputs, responses, response_text)


@pytest.mark.parametrize(
    "action_type, input_text, response_text",
    [
        (
            "enter_text",
            "START_SCENARIO_TEXT",
            ["OK_LETS_CHOOSE_SUITABLE_FOOD_TEXT", "WHAT_DO_YOU_WANT_TEXT"],
        ),
        (
            "click_button",
            "DUMPLINGS_TEXT",
            ["WRONG_CHOICE_LETS_TRY_AGAIN_TEXT", "WHAT_DO_YOU_WANT_TEXT"],
        ),
        (
            "click_button",
            "PANCAKES_TEXT",
            ["QUESTION_REMINDER_TEXT", "START_SCENARIO_TEXT", "BON_APPETIT_TEXT"],
        ),
    ],
)
@pytest.mark.web
@pytest.mark.e2e
def test_food_scenarios_responses(
    bot_chat_window, action_type, inputs, responses, input_text, response_text
):
    bot_chat_window.make_action(action_type, inputs[input_text])
    assert bot_chat_window.actual_response_text(
        inputs, responses
    ) == bot_chat_window.expected_response_text(inputs, responses, response_text)
