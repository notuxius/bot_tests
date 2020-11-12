def test_food_scenario(bot_chat_window, inputs, responses):
    bot_chat_window.load()

    bot_chat_window.input_text(inputs["HELLO_TEXT"])
    assert (
        bot_chat_window.actual_response_text()
        == bot_chat_window.expected_response_text(responses["HELLO_TEXT"])
    )

    bot_chat_window.input_text(inputs["START_SCENARIO_TEXT"])
    assert (
        bot_chat_window.actual_response_text()
        == bot_chat_window.expected_response_text(
            responses["OK_LETS_CHOOSE_SUITABLE_FOOD_TEXT"],
            responses["WHAT_DO_YOU_WANT_TEXT"],
        )
    )

    bot_chat_window.click_button(inputs["DUMPLINGS_TEXT"])
    assert (
        bot_chat_window.actual_response_text()
        == bot_chat_window.expected_response_text(
            responses["WRONG_CHOICE_LETS_TRY_AGAIN_TEXT"],
            responses["WHAT_DO_YOU_WANT_TEXT"],
        )
    )

    bot_chat_window.click_button(inputs["PANCAKES_TEXT"])
    assert (
        bot_chat_window.actual_response_text()
        == bot_chat_window.expected_response_text(
            responses["QUESTION_REMINDER_TEXT"],
            inputs["START_SCENARIO_TEXT"],
            responses["BON_APPETIT_TEXT"],
        )
    )