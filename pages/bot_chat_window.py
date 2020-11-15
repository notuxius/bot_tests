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
        input_area[0].send_keys(text_to_enter)
        input_area[0].send_keys(Keys.RETURN)

    # take generic input button template and replace it's text locator with provided
    def prepare_button(self, button_text):
        prepared_button = (
            self.INPUT_BUTTON[0],
            self.INPUT_BUTTON[1].replace('(.="")', f'(.="{button_text}")'),
        )

        return prepared_button

    def click_button(self, button_text):
        self.wait_for_elements(self.prepare_button(button_text))[0].click()

    # launch methods depending on action type provided
    def make_action(self, action_type, element_text):
        if action_type == "enter text":
            self.enter_text(element_text)

        elif action_type == "click button":
            self.click_button(element_text)

    # text is taken from web element or from responses dict
    # from multi items by list or single item by its key
    def extract_and_assemble_text(self, responses, *items):
        assembled_text = ""
        element_text = ""

        for item in items:
            if isinstance(item, WebElement):
                element_text = item.text

            elif isinstance(item, list):
                for item_list in item:
                    element_text += responses[item_list] + " "

            else:
                element_text = responses[item]

            assembled_text += element_text + " "

        return assembled_text.rstrip()

    def get_actual_response_text(self, inputs, responses):
        previous_elements = ""

        # try few times to locate needed elemens
        for _ in range(10):
            actual_response_elements = self.wait_for_elements(self.RESPONSE_MESSAGE)
            actual_response_text = self.extract_and_assemble_text(
                inputs, responses, *actual_response_elements
            )

            # TODO refactor locating/identifying previous/current elements
            if not previous_elements:
                previous_elements = actual_response_elements
                continue

            if (
                actual_response_elements == previous_elements
                # sometimes actual response text is returned as None
                or not actual_response_text
                or actual_response_text == responses["INITIAL_RESPONSE_TEXT"]
            ):
                previous_elements = actual_response_elements
                sleep(0.25)
                continue

            return actual_response_text

    def get_expected_response_text(self, responses, *response_text):
        return self.extract_and_assemble_text(responses, *response_text)
