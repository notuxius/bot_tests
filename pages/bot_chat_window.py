from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located as element_is_visible,
)
from selenium.webdriver.support.expected_conditions import (
    visibility_of_all_elements_located as elements_are_visible,
)


class BotChatWindow:
    URL = "https://autofaq.ai/awsbotkate"

    INPUT_FIELD = (By.CSS_SELECTOR, "textarea#chat21-main-message-context")
    RESPONSE_MESSAGE = (
        By.XPATH,
        '//div[contains(@class,"msg_block-last")]//div[contains(@class, "msg_receive")]',
    )

    def __init__(self, browser):
        self.browser = browser
        self.browser.get(self.URL)

    def wait_for_element(self, *elem_locator):
        element = WebDriverWait(self.browser, 5).until(
            element_is_visible(*elem_locator)
        )

        return element

    def wait_for_elements(self, *elem_locator):
        # TODO refactor to without sleep
        sleep(1)
        elements = WebDriverWait(self.browser, 5).until(
            elements_are_visible(*elem_locator)
        )

        return elements

    def input_text(self, input):
        input_field = self.wait_for_element(self.INPUT_FIELD)

        input_field.clear()
        input_field.send_keys(input)
        input_field.send_keys(Keys.RETURN)

    def click_button(self, button_text):
        self.wait_for_element(
            (
                By.XPATH,
                f'//div[contains(@class,"msg_block-last")]//button[contains(@class, "button") and (.="{button_text}")]',
            )
        ).click()

    def actual_response_text(self):
        all_response_message_text = ""
        response_message_text = ""

        response_elements = self.wait_for_elements(self.RESPONSE_MESSAGE)

        # TODO refactor
        for response_element in response_elements:
            if len(response_elements) > 1:
                response_message_text = response_element.text + " "
            else:
                response_message_text = response_element.text

            all_response_message_text += response_message_text

        return all_response_message_text.rstrip()

    def expected_response_text(self, *text_to_assemble):
        assembled_text = ""
        for text in text_to_assemble:
            print(text)
            assembled_text += text + " "

        return assembled_text.rstrip()
