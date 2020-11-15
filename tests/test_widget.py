import pytest


@pytest.mark.parametrize(
    "action_type, inputs_text, expected_response_text",
    [
        (
            "enter text",
            "HELLO_INPUT_TEXT",
            "HELLO_RESPONSE_TEXT",
        ),
        (
            "enter text",
            "START_SCENARIO_INPUT_TEXT",
            [
                "OK_LETS_CHOOSE_SUITABLE_FOOD_RESPONSE_TEXT",
                "WHAT_DO_YOU_WANT_RESPONSE_TEXT",
            ],
        ),
        (
            "click button",
            "DUMPLINGS_INPUT_BUTTON_TEXT",
            [
                "WRONG_CHOICE_LETS_TRY_AGAIN_RESPONSE_TEXT",
                "WHAT_DO_YOU_WANT_RESPONSE_TEXT",
            ],
        ),
        (
            "click button",
            "PANCAKES_INPUT_BUTTON_TEXT",
            [
                "QUESTION_REMINDER_RESPONSE_TEXT",
                "START_SCENARIO_INPUT_TEXT",
                "BON_APPETIT_RESPONSE_TEXT",
            ],
        ),
    ],
)
@pytest.mark.widget
def test_food_scenarios_responses(
    bot_chat_widget,
    inputs,
    responses,
    action_type,
    inputs_text,
    expected_response_text,
):
    bot_chat_widget.make_action(action_type, inputs[inputs_text])

    assert bot_chat_widget.get_actual_response_text(
        responses
    ) == bot_chat_widget.get_expected_response_text(responses, expected_response_text)
