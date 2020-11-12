from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import (
    visibility_of_all_elements_located,
)
from selenium.webdriver.support.ui import WebDriverWait


class BotChatWindow:
    URL = "https://autofaq.ai/awsbotkate"

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
        self.browser.get(self.URL)

    def wait_for_elements(self, *elements_locators):
        # TODO refactor without sleep
        sleep(1)
        elements = WebDriverWait(self.browser, 5).until(
            visibility_of_all_elements_located(*elements_locators)
        )

        return elements

    def input_text(self, text_to_input):
        input_field = self.wait_for_elements(self.INPUT_FIELD)

        input_field[0].clear()
        input_field[0].send_keys(text_to_input)
        input_field[0].send_keys(Keys.RETURN)

    def click_button(self, button_text):
        self.wait_for_elements(
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

    def assemble_text(self, *text_to_assemble):
        assembled_text = ""

        for text in text_to_assemble:
            if not isinstance(text, str):
                text = text.text

            assembled_text += text + " "

        return assembled_text.rstrip()

    def actual_response_text(self):
        response_elements = self.wait_for_elements(self.RESPONSE_MESSAGE)

        return self.assemble_text(*response_elements)

    def expected_response_text(self, *expected_text):

        return self.assemble_text(*expected_text)
