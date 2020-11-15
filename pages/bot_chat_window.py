from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    visibility_of_all_elements_located,
)
from selenium.webdriver.support.ui import WebDriverWait


class BotChatWindow:
    INPUT_AREA = (By.CSS_SELECTOR, "textarea#chat21-main-message-context")
    INPUT_BUTTON = (
        By.XPATH,
        (
            '//div[contains(@class,"msg_block-last")]'
            '//button[contains(@class, "button") and (.="")]'
        ),
    )
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
        elements = WebDriverWait(self.browser, 5).until(
            visibility_of_all_elements_located(*elements_locators)
        )

        return elements

    def enter_text(self, text_to_enter):
        input_area = self.wait_for_elements(self.INPUT_AREA)

        input_area[0].clear()
        input_area[0].send_keys(text_to_enter)
        input_area[0].send_keys(Keys.RETURN)

    def prepare_button(self, button_text):
        prepared_button = (
            self.INPUT_BUTTON[0],
            self.INPUT_BUTTON[1].replace('(.="")', f'(.="{button_text}")'),
        )

        return prepared_button

    def click_button(self, button_text):
        self.wait_for_elements(self.prepare_button(button_text))[0].click()

    def make_action(self, action_type, element_text):
        if action_type == "enter text":
            self.enter_text(element_text)

        elif action_type == "click button":
            self.click_button(element_text)

    def extract_and_assemble_text(self, inputs, responses, *elements):
        assembled_text = ""
        element_text = ""

        for element in elements:
            if isinstance(element, WebElement):
                element_text = element.text

            elif isinstance(element, list):
                for element_list in element:
                    try:
                        element_text += responses[element_list]

                    except KeyError:
                        element_text += inputs[element_list]

                    element_text += " "

            else:
                element_text = responses[element]

            assembled_text += element_text + " "

        return assembled_text.rstrip()

    def get_actual_response_text(self, inputs, responses):
        previous_elements = ""

        for _ in range(10):
            actual_response_elements = self.wait_for_elements(self.RESPONSE_MESSAGE)
            actual_response_text = self.extract_and_assemble_text(
                inputs, responses, *actual_response_elements
            )

            if not previous_elements:
                previous_elements = actual_response_elements
                continue

            if (
                not actual_response_text
                or actual_response_text == responses["INITIAL_RESPONSE_TEXT"]
                or actual_response_elements == previous_elements
            ):
                previous_elements = actual_response_elements
                sleep(0.25)
                continue

            return actual_response_text

    def get_expected_response_text(self, inputs, responses, *response_text):
        return self.extract_and_assemble_text(inputs, responses, *response_text)
