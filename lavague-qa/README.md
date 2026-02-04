# Test runner for LaVague

LaVague QA is a specialized tool to generate pytest files from Gherkin test descriptions. 

## Usage

```
Usage: lavague-qa [OPTIONS]

Options:
  -u, --url TEXT      URL of the site to test
  -f, --feature TEXT  Path to the .feature file containing Gherkin
  -l, --full-llm      Enable full LLM pytest generation
  -c, --context TEXT  Path of python file containing an initialized context
                      and token_counter. Defaults to OpenAI GPT4o
  -h, --headless      Enable headless mode for the browser
  -db, --log-to-db    Enables logging to a SQLite database
  --help              Show this message and exit.
```


Some examples are provided in `./features/`:

```bash
lavague-qa --url https://amazon.fr/ --feature features/demo_amazon.feature
```
Run `lavague-qa` to run a default example: Wikipedia login test

## Custom context (authenticated flows)
Create a `context.py` to provide an authenticated Selenium driver. A sample is provided:

1) Copy the example:
   `cp context.example.py context.py`
2) Fill in the selectors and make sure `BASE_URL`, `TEST_USERNAME`, and `TEST_PASSWORD` are set.

## Redaction
By default, `lavague-qa` redacts sensitive values (e.g., passwords, tokens) from logs before sending them to the LLM.
You can disable this for higher-fidelity generation if needed:

`lavague-qa --no-redact ...`

## TODO
- Improve `get_selenium_driver` source extraction when contexts are loaded via `exec` (currently hardened against empty source).

## Learn more

To learn more, please visit our LaVague QA documentation and join our [Discord](https://discord.gg/invite/SDxn9KpqX9) to reach our core team and get support!
