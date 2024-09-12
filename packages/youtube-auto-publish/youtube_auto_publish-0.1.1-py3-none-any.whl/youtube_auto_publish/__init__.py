from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from asyncio import sleep
from traceback import print_exc
from logging import getLogger

logger = getLogger(__name__)

__version__ = "0.1.1"


class AutoYoutube:
    def __init__(
        self,
        username: str,
        password: str,
        chromedriver_executable_path: str = "",
    ) -> None:
        self.__username = username
        self.__password = password
        self.__chromedriver_path = chromedriver_executable_path
        self.__browser: Chrome
        self.__options = ChromeOptions()
        self.__wait: WebDriverWait

    async def login(self) -> None:
        try:
            logger.info("Connecting to Youtube")
            self.__browser.get("https://youtube.com")

            sign_in_button = self.__wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
            )
            sign_in_button.click()

            logger.info("Sending Username")
            email_input = self.__wait.until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.send_keys(self.__username)

            next_button = self.__wait.until(
                EC.element_to_be_clickable((By.ID, "identifierNext"))
            )
            next_button.click()

            logger.info("Sending Password")
            password_input = self.__wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@type='password']")
                )
            )
            password_input.send_keys(self.__password)

            next_button_password = self.__wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#passwordNext button")
                )
            )

            await sleep(3)
            next_button_password.click()
        except Exception as e:
            print_exc()

            raise e

    def __post_thumbnail(self, thumbnail_path: str) -> None:
        thumbnail_button = self.__browser.find_element(By.ID, "select-button")

        thumbnail_button.send_keys(thumbnail_path)

    def __post_tags(self, tags: list[str]) -> None:
        show_more_button = self.__browser.find_element(By.ID, "toggle-button")

        show_more_button.click()

        tags_input_box = self.__browser.find_element(
            By.ID, "tags-container"
        ).find_element(By.ID, "text-input")

        tags_input_box.send_keys(",".join(tags))

    def __mark_no_safe_for_kids(self) -> None:
        not_for_kids_button = self.__browser.find_element(
            By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK"
        ).find_element(By.ID, "radioLabel")

        not_for_kids_button.click()

    def __mark_age_restricted(self) -> None:
        show_age_restriction_button = self.__browser.find_element(
            By.XPATH, "//button[@aria-controls='age-restriction']"
        )

        show_age_restriction_button.click()

        age_restriction_button = self.__browser.find_element(
            By.NAME, "VIDEO_AGE_RESTRICTION_SELF"
        ).find_element(By.ID, "radioLabel")

        age_restriction_button.click()

    def __go_to_publish_page(self) -> None:
        next_button_1 = self.__browser.find_element(By.ID, "next-button").find_element(
            By.CSS_SELECTOR, "button"
        )

        next_button_1.click()

        next_button_2 = self.__browser.find_element(By.ID, "next-button").find_element(
            By.CSS_SELECTOR, "button"
        )

        next_button_2.click()

        next_button_3 = self.__browser.find_element(By.ID, "next-button").find_element(
            By.CSS_SELECTOR, "button"
        )

        next_button_3.click()

    def __select_publish_video(self) -> None:
        public_button = self.__browser.find_element(
            By.XPATH, "//div[@id='radioLabel' and text()='Public']"
        )

        public_button.click()

    async def post_video(
        self,
        channel_name: str,
        video_path: str,
        tags: list[str] = [],
        video_description: str = "",
        thumbnail_path: str = "",
        age_restriction: bool = False,
    ) -> bool:
        try:
            logger.info("Selecting channel")
            channel_button = self.__wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//*[@id='channel-title' and text()='{channel_name}']")
                )
            )
            channel_button.click()

            await sleep(3)

            logger.info("Uploading video")
            create_button = self.__wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Create']"))
            )
            create_button.click()

            upload_video_button = self.__wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='label' and text()='Upload video']")
                )
            )
            upload_video_button.click()

            upload_arrow_button = self.__wait.until(
                EC.presence_of_element_located((By.ID, "content"))
            ).find_element(By.CSS_SELECTOR, "input")

            upload_arrow_button.send_keys(video_path)

            await sleep(3)

            logger.info("")
            description_box = self.__wait.until(
                EC.presence_of_element_located((By.ID, "description-wrapper"))
            ).find_element(By.ID, "textbox")

            description_box.send_keys(video_description)

            if thumbnail_path:
                self.__post_thumbnail(thumbnail_path)

            self.__mark_no_safe_for_kids()

            if age_restriction:
                self.__mark_age_restricted()

            if tags:
                self.__post_tags(tags)

            self.__go_to_publish_page()

            self.__select_publish_video()

            publish_button = self.__wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='done-button' and @aria-disabled='false']"),
                )
            )

            publish_button.click()

            await sleep(10)

            return True
        except Exception:
            print_exc()

            return False

    def __enter__(self):
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option("useAutomationExtension", False)
        self.__options.add_argument("--headless=new")
        self.__options.add_argument("--no-sandbox")
        self.__options.add_argument("--disable-dev-shm-usage")
        self.__options.add_argument("--disable-blink-features=AutomationControlled")
        self.__options.add_argument("--lang=en-US")
        self.__options.add_argument(
            "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.119 Safari/537.36"
        )
        self.__options.binary_location = "/usr/bin/google-chrome"

        self.__browser = Chrome(
            self.__options,
            service=ChromeService(executable_path=self.__chromedriver_path)
            if self.__chromedriver_path
            else None,
        )
        self.__browser.maximize_window()
        self.__wait = WebDriverWait(self.__browser, 10)
        return self

    def __exit__(self, *args):
        self.__browser.quit()
