import pytest


@pytest.mark.parametrize(
    "action_type, input_text, response_check_condition, response_text",
    [
        (
            "enter text",
            "HELLO_INPUT_TEXT",
            "response is equal",
            "HELLO_RESPONSE_TEXT",
        ),
        (
            "enter text",
            "START_SCENARIO_INPUT_TEXT",
            "response is equal",
            [
                "OK_LETS_CHOOSE_SUITABLE_FOOD_RESPONSE_TEXT",
                "WHAT_DO_YOU_WANT_RESPONSE_TEXT",
            ],
        ),
        (
            "click button",
            "DUMPLINGS_INPUT_BUTTON_TEXT",
            "response is equal",
            [
                "WRONG_CHOICE_LETS_TRY_AGAIN_RESPONSE_TEXT",
                "WHAT_DO_YOU_WANT_RESPONSE_TEXT",
            ],
        ),
        (
            "click button",
            "PANCAKES_INPUT_BUTTON_TEXT",
            "response is equal",
            [
                "QUESTION_REMINDER_RESPONSE_TEXT",
                "START_SCENARIO_INPUT_TEXT",
                "BON_APPETIT_RESPONSE_TEXT",
            ],
        ),
    ],
)
@pytest.mark.web
def test_food_scenarios_responses(
    bot_chat_window,
    inputs,
    responses,
    action_type,
    input_text,
    response_check_condition,
    response_text,
):
    bot_chat_window.make_action(action_type, inputs[input_text])

    assert bot_chat_window.expected_response_is_correct(
        bot_chat_window.actual_response_text(inputs, responses),
        response_check_condition,
        bot_chat_window.expected_response_text(inputs, responses, response_text),
    )
