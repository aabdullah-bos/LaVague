import click
import os
import linecache
from typing import Callable, Optional, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from lavague.core.context import Context
from lavague.core.token_counter import TokenCounter
from lavague.qa.generator import TestGenerator

default_feature = None
default_url = None

cwd = os.getcwd()
for path in (
    "/lavague-qa/features/demo_wikipedia.feature",
    "/features/demo_wikipedia.feature",
):
    if os.path.exists(cwd + path):
        default_feature = cwd + path
        default_url = "https://en.wikipedia.org/"
        break


@click.command()
@click.option(
    "--url",
    "-u",
    type=str,
    default=default_url,
    required=True,
    help="URL of the site to test",
)
@click.option(
    "--feature",
    "-f",
    default=default_feature,
    type=str,
    required=True,
    help="Path to the .feature file containing Gherkin",
)
@click.option(
    "--full-llm",
    "-l",
    is_flag=True,
    required=False,
    help="Enable full LLM pytest generation",
)
@click.option(
    "--context",
    "-c",
    type=str,
    default=None,
    required=False,
    help="Path of python file containing an initialized context and token_counter. Defaults to OpenAI GPT4o",
)
@click.option(
    "--redact/--no-redact",
    default=True,
    help="Redact sensitive values from logs before sending to the LLM",
)
@click.option(
    "--headless",
    "-h",
    is_flag=True,
    required=False,
    help="Enable headless mode for the browser",
)
@click.option(
    "--log-to-db",
    "-db",
    is_flag=True,
    required=False,
    help="Enables logging to a SQLite database",
)
def cli(
    url: str,
    feature: str,
    full_llm: bool,
    context: str,
    redact: bool,
    headless: bool,
    log_to_db: bool,
) -> None:
    context, token_counter, get_selenium_driver, selenium_driver = _load_context(
        context
    )
    pytest_generator = TestGenerator(
        context,
        url,
        feature,
        full_llm,
        token_counter,
        headless,
        log_to_db,
        get_selenium_driver=get_selenium_driver,
        selenium_driver=selenium_driver,
        redact_logs=redact,
    )
    pytest_generator.generate()


def _load_context(
    context_path: Optional[str],
) -> Tuple[Context, TokenCounter, Optional[Callable[[], WebDriver]], Optional[WebDriver]]:
    if context_path:
        with open(context_path, "r") as file:
            file_content = file.read()
        local_namespace = {}
        linecache.cache[context_path] = (
            len(file_content),
            None,
            file_content.splitlines(True),
            context_path,
        )
        compiled = compile(file_content, context_path, "exec")
        exec(compiled, local_namespace, local_namespace)

        if "context" not in local_namespace or "token_counter" not in local_namespace:
            raise Exception(
                "Expected variables (`context` and `token_counter`) not found in the provided context file"
            )
        get_selenium_driver = local_namespace.get("get_selenium_driver")
        if get_selenium_driver is None:
            get_selenium_driver = local_namespace.get("create_selenium_driver")
        if get_selenium_driver is not None and not callable(get_selenium_driver):
            raise Exception(
                "Expected `get_selenium_driver` (or `create_selenium_driver`) to be callable"
            )
        selenium_driver = local_namespace.get("selenium_driver")

        return (
            local_namespace["context"],
            local_namespace["token_counter"],
            get_selenium_driver,
            selenium_driver,
        )

    from contexts.default_context import context, token_counter

    return context, token_counter, None, None
