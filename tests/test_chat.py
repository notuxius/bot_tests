# TODO use parametrize
def test_food_scenario(bot_chat_window, input_templates_text, response_templates_text):
    bot_chat_window.load()

    bot_chat_window.input_text(input_templates_text["HELLO_TEXT"])
    assert bot_chat_window.response_text() == response_templates_text["HELLO_TEXT"]

    bot_chat_window.input_text(input_templates_text["START_SCENARIO_TEXT"])
    assert (
        bot_chat_window.response_text()
        == response_templates_text["OK_LETS_CHOOSE_SUITABLE_FOOD_TEXT"]
        + " "
        + response_templates_text["WHAT_DO_YOU_WANT_TEXT"]
    )

    bot_chat_window.click_button(input_templates_text["DUMPLINGS_TEXT"])
    assert (
        bot_chat_window.response_text()
        == response_templates_text["WRONG_CHOICE_LETS_TRY_AGAIN_TEXT"]
        + " "
        + response_templates_text["WHAT_DO_YOU_WANT_TEXT"]
    )

    bot_chat_window.click_button(input_templates_text["PANCAKES_TEXT"])
    assert (
        bot_chat_window.response_text()
        == response_templates_text["QUESTION_REMINDER_TEXT"]
        + " "
        + input_templates_text["START_SCENARIO_TEXT"]
        + " "
        + response_templates_text["BON_APPETIT_TEXT"]
    )