import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from lavague.core.context import Context
from lavague.core.token_counter import TokenCounter

load_dotenv()

TEST_USERNAME = os.getenv("TEST_USERNAME")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
BASE_URL = os.getenv("BASE_URL")

if not TEST_USERNAME or not TEST_PASSWORD or not BASE_URL:
    raise RuntimeError(
        "Missing TEST_USERNAME, TEST_PASSWORD, or BASE_URL environment variables."
    )

llm_name = "gpt-4o"
mm_llm_name = "gpt-4o"
embedding_name = "text-embedding-3-large"

token_counter = TokenCounter()
llm = OpenAI(model=llm_name)
mm_llm = OpenAIMultiModal(model=mm_llm_name)
embedding = OpenAIEmbedding(model=embedding_name)
context = Context(llm, mm_llm, embedding)


def get_selenium_driver(headless: bool = False):
    options = webdriver.ChromeOptions()
    # Intentionally keep headless disabled for authenticated flows.
    # If you later want headless, add the flag and remove this guard.
    if False and headless:
        options.add_argument("--headless=new")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    base_url = os.environ.get("BASE_URL")
    username = os.environ.get("TEST_USERNAME")
    password = os.environ.get("TEST_PASSWORD")
    if not base_url:
        raise RuntimeError("BASE_URL is required in the environment")
    if not username or not password:
        raise RuntimeError(
            "TEST_USERNAME and TEST_PASSWORD are required in the environment"
        )

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)

    # TODO: replace selectors with your login form fields/buttons.
    email = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#email")))
    password_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#password"))
    )
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit")))

    email.clear()
    email.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)
    login_btn.click()

    # TODO: replace with a selector that confirms a successful login.
    wait.until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                ".app-dashboard-container",
            )
        )
    )

    return driver
