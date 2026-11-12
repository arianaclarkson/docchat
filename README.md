# DocChat

DocChat is a Python command-line chatbot that uses the Groq API to answer questions about files in the current directory. It remembers conversation history and can list files, read text files, search with regular expressions, and calculate arithmetic expressions through manual commands or model-selected tools.

## Installation

From the docchat repository root, install the package and dependencies:

```bash
python -m pip install -e . -r requirements.txt
```

Set `GROQ_API_KEY` in a local `.env` file to use the model. Never commit `.env` to Git.

## Usage

Launch an interactive session:

```bash
chat
```

Use `/ls .`, `/cat README.md`, `/grep import chat.py`, or `/calculate 2 + 3` to call tools directly without an API request. Use `chat Hello` for a one-shot message or `chat --debug` to display tool calls. Press Ctrl+C or Ctrl+D to exit the interactive session.

## Testing

Run offline doctests, coverage, and lint checks from the repository root:

```bash
python -m pytest --doctest-modules tools chat.py
python -m coverage run --source=tools -m pytest --doctest-modules tools
python -m coverage report -m
python -m flake8 chat.py tools --ignore=E501
```

These doctests use local files or fake model responses rather than a live API call.

## Integration Tests

The three earlier class projects are Git submodules under `test_projects`. Each transcript starts in the docchat repository root, changes into the project directory, and launches the installed `chat` command. File listings and answer excerpts below are from actual sessions.

### Webpage

```text
cd test_projects/lab-1
chat
chat> /ls .
Neb photo.webp  README.md  history.html  history.jpg  hitting.jpg  index.html  passing.jpg  serving.jpg  setting.jpg  skills.html  style.css  submission.toml
chat> Use your cat tool to read index.html and explain what this webpage does.
Its purpose is to introduce the fundamentals of volleyball and provide quick navigation to the other lab pages.
```

What I learned: DocChat can inspect my volleyball site's HTML and explain how navigation, images, informational sections, and CSS styling fit together.

### Markdown Compiler

```text
cd test_projects/markdown-compiler
chat
chat> /ls .
README.md  example  markdown_compiler  pyproject.toml  requirements.txt  submission.toml
chat> Use your tools to inspect the markdown_compiler folder. Explain how this project converts Markdown into HTML.
The package is split into two logical layers:
Line-level helpers convert a single line of Markdown into HTML fragments.
A document-level orchestrator walks through the whole file, tracks paragraphs, lists, and code blocks, and builds the HTML document.
```

What I learned: The Markdown compiler separates inline formatting conversions from the document-level logic that organizes paragraphs, lists, and fenced code blocks.

### eBay Scraper

```text
cd test_projects/ebay-scraper
chat
chat> /ls .
READ.md  README.md  ebay-dl.py  garden tools.csv  garden tools.json  laptop.csv  laptop.json  practice-pages  practice-pages.zip  shoes.csv  shoes.json  submission.toml
chat> Use the cat tool to read ebay-dl.py. Explain how it collects and saves eBay data.
The script accepts command-line arguments, reads saved HTML or fetches eBay search-result pages, and uses BeautifulSoup to extract listing information.
It combines the results and writes them to CSV or JSON files.
```

What I learned: The eBay scraper separates page loading, listing extraction, and exporting product data such as prices, shipping costs, and conditions to CSV or JSON files.
