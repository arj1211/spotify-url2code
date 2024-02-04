import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SpotifyCodeDownloader:
    SLEEP_SECONDS = 2
    elems_by = {
        "search_bar": {"by": By.NAME, "term": "uri"},
        "get_spotify_code": {"by": By.TAG_NAME, "term": "button"},
        "ack": {"by": By.CLASS_NAME, "term": "modal-content"},
        "ack_bottom": {"by": By.CLASS_NAME, "term": "modal-faq-container", "index": -1},
        "continue": {"by": By.CLASS_NAME, "term": "accept-button"},
        "cookie_policy_close": {
            "by": By.CLASS_NAME,
            "term": "onetrust-close-btn-handler",
            "index": 0,
        },
        "bg_color_field": {"by": By.NAME, "term": "back-color"},
        "code_color_field": {"by": By.CLASS_NAME, "term": "new-code-color"},
        "code_format_field": {"by": By.CLASS_NAME, "term": "new-code-format"},
        "dropdown_option": {"by": By.CLASS_NAME, "term": "option"},
        "download": {"by": By.CLASS_NAME, "term": "download"},
    }

    def __init__(self):
        self.cookie_policy_closed = False
        self.driver = None

    def get_elem(self, key_name):
        if key_name not in self.elems_by.keys():
            raise ValueError(f"{key_name} not in elems_by dict")
        elem = self.elems_by[key_name]

        if "index" in elem.keys():
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located((elem["by"], elem["term"]))
            )
            WebDriverWait(self.driver, 60).until(
                EC.visibility_of_any_elements_located((elem["by"], elem["term"]))
            )

            elems = self.driver.find_elements(elem["by"], elem["term"])
            elem = elems[elem["index"]]
        else:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((elem["by"], elem["term"]))
            )
            elem = self.driver.find_element(elem["by"], elem["term"])
            WebDriverWait(self.driver, 60).until(EC.visibility_of(elem))

        return elem

    def input_flow(self, url_to_input: str, _DEBUGGING=False):
        # Find the search bar
        search_bar = self.get_elem("search_bar")

        # Clear any pre-populated text in the search bar
        if not _DEBUGGING:
            search_bar.clear()

        # Enter text into the search bar
        if not _DEBUGGING:
            search_bar.send_keys(url_to_input)

        # GET SPOTIFY CODE button click
        self.get_elem("get_spotify_code").click()

        # Acknowledgement modal
        ack_modal = self.get_elem("ack")

        if not self.cookie_policy_closed:
            self.get_elem("cookie_policy_close").click()
            self.cookie_policy_closed = True

        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(
                (self.elems_by["continue"]["by"], self.elems_by["continue"]["term"])
            )
        )

        # then find continue button
        cont_button = self.driver.find_element(
            self.elems_by["continue"]["by"], self.elems_by["continue"]["term"]
        )

        while not cont_button.is_enabled():
            ActionChains(self.driver).move_to_element(ack_modal).click().send_keys(
                Keys.PAGE_DOWN
            ).perform()

        cont_button.click()

    def pick_dropdown_option_by_text(self, option_text, web_element):
        web_element.click()
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located(
                (self.elems_by["dropdown_option"]["by"], self.elems_by["dropdown_option"]["term"])
            )
        )
        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_any_elements_located(
                (self.elems_by["dropdown_option"]["by"], self.elems_by["dropdown_option"]["term"])
            )
        )
        options = web_element.find_element(By.XPATH, "..").find_elements(
            self.elems_by["dropdown_option"]["by"], self.elems_by["dropdown_option"]["term"]
        )

        options = [e for e in options if e.text == option_text]
        time.sleep(self.SLEEP_SECONDS)
        if len(options) != 1:
            raise ValueError(f"ambiguous dropdown option text {option_text} for page")
        option = options.pop()
        option.click()
        time.sleep(self.SLEEP_SECONDS)

    def config_and_download_flow(self, bg_color="#FFFFFF", code_color="black", format="SVG"):
        bg_color_field = self.get_elem("bg_color_field")
        bg_color_field.clear()
        bg_color_field.send_keys(bg_color)

        # the code color dropdown
        cc = self.get_elem("code_color_field")
        # pick the correct option
        self.pick_dropdown_option_by_text(code_color, cc)
        # the code format dropdown
        cf = self.get_elem("code_format_field")
        # pick the correct option
        self.pick_dropdown_option_by_text(format, cf)

        self.get_elem("download").click()
        time.sleep(self.SLEEP_SECONDS)

    def download_codes(self, song_urls):
        for song_url in song_urls:
            # Go to a webpage
            self.driver.get("https://www.spotifycodes.com/")

            self.input_flow(song_url)
            self.config_and_download_flow()

            # Print the current URL
            print(song_url)

            time.sleep(self.SLEEP_SECONDS)

    def run(self, song_urls):
        download_dir = os.path.join(os.path.dirname(__file__), "downloaded_song_codes")

        if not os.path.isdir(download_dir):
            os.mkdir(download_dir)

        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome(options=chrome_options)

        self.download_codes(song_urls)

        # Close the browser
        self.driver.close()

if __name__ == "__main__":
    song_urls = [
        "https://open.spotify.com/track/5EFczt9dqrCu60udoD41Yy?si=678eeedbb7b04e2b",
        "spotify:track:4mL59LVbKgOpEACxraGYdr",
        "spotify:track:4204hwPYuToiuSunPFUoML",
        "spotify:track:0PJIbOdMs3bd5AT8liULMQ",
    ]

    downloader = SpotifyCodeDownloader()
    downloader.run(song_urls)
