import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def get_elem(key_name):
    if key_name not in elems_by.keys():
        raise ValueError(f"{key_name} not in elems_by dict")
    elem = elems_by[key_name]

    if "index" in elem.keys():
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((elem["by"], elem["term"]))
        )
        elems = driver.find_elements(elem["by"], elem["term"])
        elem = elems[elem["index"]]
    else:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((elem["by"], elem["term"]))
        )
        elem = driver.find_element(elem["by"], elem["term"])

    return elem


def input_flow(url_to_input: str, _DEBUGGING=False):
    # Find the search bar
    search_bar = get_elem("search_bar")

    # Clear any pre-populated text in the search bar
    if not _DEBUGGING:
        search_bar.clear()

    # Enter text into the search bar
    if not _DEBUGGING:
        search_bar.send_keys(url_to_input)

    # GET SPOTIFY CODE button click
    get_elem("get_spotify_code").click()

    # Acknowledgement modal
    ack_modal = get_elem("ack")

    bottom_of_modal = get_elem("ack_bottom")

    ActionChains(driver).move_to_element(ack_modal).scroll_to_element(
        bottom_of_modal
    ).perform()

    get_elem("cookie_policy_close").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (elems_by["continue"]["by"], elems_by["continue"]["term"])
        )
    )

    # then find continue button
    cont_button = driver.find_element(
        elems_by["continue"]["by"], elems_by["continue"]["term"]
    )

    while not cont_button.is_enabled():
        ActionChains(driver).move_to_element(ack_modal).click().send_keys(
            Keys.PAGE_DOWN
        ).perform()

    cont_button.click()


def pick_dropdown_option_by_text(option_text, web_element):
    web_element.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (elems_by["dropdown_option"]["by"], elems_by["dropdown_option"]["term"])
        )
    )
    options = web_element.find_element(By.XPATH, "..").find_elements(
        elems_by["dropdown_option"]["by"], elems_by["dropdown_option"]["term"]
    )

    options = [e for e in options if e.text == option_text]
    if len(options) != 1:
        raise ValueError(f"ambiguous dropdown option text {option_text} for page")
    option = options.pop()
    option.click()


def config_and_download_flow(bg_color="#FFFFFF", code_color="black", format="SVG"):
    bg_color_field = get_elem("bg_color_field")
    bg_color_field.clear()
    bg_color_field.send_keys(bg_color)

    # the code color dropdown
    cc = get_elem("code_color_field")
    # pick the correct option
    pick_dropdown_option_by_text(code_color, cc)
    # the code format dropdown
    cf = get_elem("code_format_field")
    # pick the correct option
    pick_dropdown_option_by_text(format, cf)

    get_elem("download").click()


if __name__ == '__main__':

    song_url = "https://open.spotify.com/track/5EFczt9dqrCu60udoD41Yy?si=678eeedbb7b04e2b"

    download_dir = os.path.join(os.path.dirname(__file__), "downloaded_song_codes")

    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)


    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Go to a webpage
    driver.get("https://www.spotifycodes.com/")

    input_flow(song_url)
    config_and_download_flow()


    # Print the current URL
    print(song_url)

    # Close the browser
    driver.close()
