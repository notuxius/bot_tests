from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import (
    visibility_of_all_elements_located,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


class BotChatWindow:
    INPUT_FIELD = (By.CSS_SELECTOR, "textarea#chat21-main-message-context")
    RESPONSE_MESSAGE = (
        By.XPATH,
        (
            '//div[contains(@class,"msg_block-last")]'
            '//div[contains(@class, "msg_receive")]'
        ),
    )

    def __init__(self, browser):
        self.browser = browser

    def wait_for_elements(self, *elements_locators):
        # TODO refactor without sleep
        sleep(1)
        elements = WebDriverWait(self.browser, 2).until(
            visibility_of_all_elements_located(*elements_locators)
        )

        return elements

    def enter_text(self, text_to_enter):
        input_field = self.wait_for_elements(self.INPUT_FIELD)

        input_field[0].clear()
        input_field[0].send_keys(text_to_enter)
        input_field[0].send_keys(Keys.RETURN)

    def click_button(self, button_text):
        self.wait_for_elements(
            # TODO refactor into RESPONSE_BUTTON
            (
                By.XPATH,
                (
                    (
                        '//div[contains(@class,"msg_block-last")]'
                        '//button[contains(@class, "button")'
                        f' and (.="{button_text}")]'
                    )
                ),
            )
        )[0].click()

    def make_action(self, action_type, element_text):

        if action_type == "click button":
            self.click_button(element_text)

        elif action_type == "enter text":
            self.enter_text(element_text)

    def extract_and_assemble_text(self, inputs, responses, *elements):
        assembled_text = ""
        element_text = ""

        for element in elements:
            if isinstance(element, WebElement):
                element_text = element.text

            elif isinstance(element, list):
                for element_list_text in element:
                    try:
                        element_text += responses[element_list_text]

                    except KeyError:
                        element_text += inputs[element_list_text]

                    element_text += " "

            else:
                element_text = responses[element]

            assembled_text += element_text + " "

        return assembled_text.rstrip()

    def actual_response_text(self, inputs, responses):
        actual_response_elements = self.wait_for_elements(self.RESPONSE_MESSAGE)

        return self.extract_and_assemble_text(
            inputs, responses, *actual_response_elements
        )

    def expected_response_text(self, inputs, responses, *expected_response_elements):
        return self.extract_and_assemble_text(
            inputs, responses, *expected_response_elements
        )

    def expected_response_is_correct(
        self, actual_response_text, response_check_condition, expected_response_text
    ):
        if response_check_condition == "response is equal":
            return actual_response_text == expected_response_text

        elif response_check_condition == "response is not equal":
            return not actual_response_text == expected_response_text

        return False
