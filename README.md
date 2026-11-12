
# DocChat
docchat is a chatbot that uses Groq API to answer questions about files.  

DocChat is a simple chatbot created in Python.

It uses the Groq API to generate responses and remembers
previous messages during a conversation.

## Installation

Install the dependencies and the chatbot:

    python -m pip install .

## Usage

To start the chatbot, type:

    chat

Type messages to have a conversation.

Press Ctrl+C or Ctrl+D to exit on macOS/Linux.

## Testing

To run the offline doctests:

    python -m pytest chat.py --doctest-modules

The tests use fake API replies and do not need a live
model connection.


### eBay Scraper


```
cd test_projects/ebay-scraper
chat
chat> /ls .
READ.md  README.md  ebay-dl.py  garden tools.csv  garden tools.json  laptop.csv  laptop.json  practice-pages  practice-pages.zip  shoes.csv  shoes.json  submission.toml
chat> Use the cat tool to read ebay-dl.py. Explain how it collects and saves eBay data.
**How `ebay-dl.py` works**

| Step | What it does | Key code snippets |
|------|--------------|-------------------|
| **1. Parse command‑line arguments** | The script accepts three options: `--search` (required), `--pages-dir` (optional), and `--csv` (flag). | ```python<br>parser.add_argument("--search", required=True)<br>parser.add_argument("--pages-dir")<br>parser.add_argument("--csv", action="store_true")<br>``` |
| **2. Loop over pages** | It iterates over the first 10 pages of an eBay search. For each page it calls `load_page()` to fetch the HTML. | ```python<br>for page_number in range(1, 11):<br>    html = load_page(args.search, page_number, args.pages_dir)<br>``` |
| **3. Load a page** | `load_page()` either reads a local file (if `--pages-dir` is supplied) or makes an HTTP GET request to eBay’s search URL. It also checks for a CAPTCHA/robot check and raises an error if detected. | ```python<br>response = requests.get("https://www.ebay.com/sch/i.html", params={…})<br>if "captcha" in html.lower(): raise RuntimeError(...)<br>``` |
| **4. Parse the HTML** | `extract_items()` uses BeautifulSoup to find all listing “cards” (`li.s-item` or `div.s-item`). For each card it pulls out: <br>• **name** – title of the listing<br>• **price** – converted to cents via `money_to_cents()`<br>• **status** – e.g., “New”, “Used”<br>• **shipping** – parsed to cents (free → 0) via `parse_shipping()`<br>• **free_returns** – boolean via `parse_returns()`<br>• **items_sold** – number of sold items via `parse_sold()` | ```python<br>cards = soup.select("li.s-item, div.s-item")<br>for card in cards:<br>    name = get_text(card, [".s-item__title", …])<br>    price = money_to_cents(get_text(card, [".s-item__price", …]))<br>    …<br>``` |
| **5. Collect all items** | The script aggregates the dictionaries returned by `extract_items()` into a single list `all_items`. | ```python<br>all_items.extend(items)<br>``` |
| **6. Save the data** | After all pages are processed, the script writes the list to a file. If `--csv` is set, it writes a CSV with the columns defined in `FIELDS`; otherwise it writes a pretty‑printed JSON file. | ```python<br>if args.csv:<br>    with open(f"{args.search}.csv", "w", newline="", encoding="utf-8") as f:<br>        writer = csv.DictWriter(f, fieldnames=FIELDS)<br>        writer.writeheader()<br>        writer.writerows(all_items)<br>else:<br>    with open(f"{args.search}.json", "w", encoding="utf-8") as f:<br>        json.dump(all_items, f, indent=2)<br>``` |
| **7. Rate‑limiting** | When scraping live eBay pages (i.e., no `--pages-dir`), the script sleeps 1 second between requests to reduce the chance of being blocked. | ```python<br>if not args.pages_dir and page_number < 10:<br>    time.sleep(1)<br>``` |

**Summary**

1. **Fetch**: For each of the first 10 pages, download the HTML (or read from a local file).  
2. **Parse**: Use BeautifulSoup to locate each listing card and extract the relevant fields, converting prices and shipping to numeric cents, and parsing booleans and sold counts.  
3. **Collect**: Append every listing dictionary to a master list.  
4. **Persist**: Write the master list to either a CSV or JSON file named after the search term.  

The script is intentionally simple, relying on CSS selectors that match eBay’s current page structure, and includes basic error handling for missing data or CAPTCHA blocks.

```

**what i learned: this project collects ebay listings information from webpages and saves it as csv files. 

### Webpage

cd test_projects/lab-1
chat
chat> /ls .
Neb photo.webp  README.md  history.html  history.jpg  hitting.jpg  index.html  passing.jpg  serving.jpg  setting.jpg  skills.html  style.css  submission.toml
chat> Use your cat tool to read index.html and explain what this webpage does.
Its purpose is to introduce the fundamentals of volleyball and provide quick navigation to the other lab pages.

**Key elements**

| Section | What it does |
|---------|--------------|
| **Header / Navbar** | Links to the three main pages of the lab: Home (this page), Skills, and History. |
| **Hero image** | A large image (`Neb photo.webp`) of a Nebraska volleyball game that visually sets the theme. |
| **Title & Intro** | `<h1 id="top">Lab 1: Volleyball Basics</h1>` followed by two `<p class="second_title">` blocks that give a brief overview of what will be covered. |
| **Skill list** | A bulleted list of the six core volleyball skills: Serving, Passing, Setting, Hitting, Defending, Blocking. |
| **Video link** | A hyperlink to a YouTube video that demonstrates a rally containing all those skills. |
| **Info box** | A styled `<div class="info_box">` that highlights a short note about volleyball’s fast‑paced, teamwork‑heavy nature. |
| **Footer box** | A closing message thanking the reader. |
| **External links** | Two paragraphs with links to the course website, the professor’s site, and the classmates’ lab homepages. |

**Styling & tracking**

* The page pulls in `style.css` for layout and visual styling.  
* Google Analytics is loaded asynchronously via the `gtag` script, so page views are tracked.

Overall, the page serves as an introductory hub for the lab, giving students a quick overview of volleyball basics, a visual example, and easy navigation to deeper content.
chat> 

i learned: this command extracts what the website components are, with the different pages and parts of the website, and then gives an overall idea of the website. 



### Markdown compiler

(.venv) arianaclarkson@Arianas-MacBook-Air-4 docchat % ls test_projects/markdown-compiler
README.md               markdown_compiler       requirements.txt
example                 pyproject.toml          submission.toml
(.venv) arianaclarkson@Arianas-MacBook-Air-4 docchat % cd test_projects/markdown-compiler
chat
chat> /ls .
README.md  example  markdown_compiler  pyproject.toml  requirements.txt  submission.toml
chat> Use your tools to inspect the markdown_compiler folder. Explain how this project converts Markdown into HTML.
**How the `markdown_compiler` package turns Markdown into HTML**

The package is split into two logical layers:

| Layer | Responsibility |
|-------|----------------|
| **Line‑level helpers** (`markdown_compiler/util/line_functions.py`) | Convert a *single* line of Markdown into the corresponding HTML fragments. |
| **Document‑level orchestrator** (`markdown_compiler/__init__.py`) | Walk through the whole file, keep track of context (paragraph, list, code block), and stitch the line‑level fragments together into a complete HTML document. |

Below is a step‑by‑step walk‑through of the conversion process.

---

## 1.  Line‑level helpers

All helpers live in `line_functions.py`.  
Each helper takes a string and returns a new string with the Markdown syntax replaced by the appropriate HTML tag.

| Markdown syntax | Helper function | Result |
|-----------------|-----------------|--------|
| `# Header` (1–6 `#`) | `compile_headers` | `<h1>…</h1>` … `<h6>…</h6>` |
| `**bold**` | `compile_bold_stars` | `<b>bold</b>` |
| `__bold__` | `compile_bold_underscore` | `<b>bold</b>` |
| `*italic*` | `compile_italic_star` | `<i>italic</i>` |
| `_italic_` | `compile_italic_underscore` | `<i>italic</i>` |
| `~~strikethrough~~` | `compile_strikethrough` | `<ins>strikethrough</ins>` |
| `` `inline code` `` | `compile_code_inline` | `<code>inline code</code>` (escapes `<` and `>` inside) |
| `[label](url)` | `compile_links` | `<a href="url">label</a>` |
| `![alt](url)` | `compile_images` | `<img src="url" alt="alt" />` |

All of these helpers are thin wrappers around a generic `replace_markers` routine that scans the line for a marker pair and replaces the content between them with the supplied tag.

---

## 2.  Document‑level orchestration (`compile_lines`)

`compile_lines` is the heart of the conversion.  
It receives the entire Markdown document as a single string and returns a string that contains the HTML body (everything between `<body>` and `</body>`).

### 2.1  State machine

The function keeps three boolean flags:

| Flag | Meaning |
|------|---------|
| `in_paragraph` | We are inside a `<p>` block. |
| `in_code` | We are inside a fenced code block (` ``` `). |
| `in_list` | We are inside an ordered list (`<ol>`). |

The flags are updated as the function walks through each line.

### 2.2  Processing loop

```python
for line in lines:
    stripped = line.strip()

    # 1. Fenced code blocks
    if stripped.startswith('```'):
        toggle <pre> / </pre> and flip in_code
        continue

    # 2. Inside a code block – keep indentation verbatim
    if in_code:
        new_lines.append(line)
        continue

    # 3. Ordered list items
    dot = line.find('. ')
    is_list_item = dot > 0 and line[:dot].isdigit()
    if is_list_item:
        close paragraph if needed
        open <ol> if not already open
        transform the list item text with all inline helpers
        wrap in <li> and continue

    # 4. Blank line
    if line == '':
        close paragraph or list if needed
        continue

    # 5. Paragraph start
    if line[0] != '#' and not in_paragraph:
        in_paragraph = True
        line = '<p>\n' + line

    # 6. Inline transformations
    line = compile_headers(line)
    line = compile_strikethrough(line)
    line = compile_bold_stars(line)
    line = compile_bold_underscore(line)
    line = compile_italic_star(line)
    line = compile_italic_underscore(line)
    line = compile_code_inline(line)
    line = compile_images(line)
    line = compile_links(line)

    new_lines.append(line)
```

After the loop, any open list is closed.

### 2.3  Result

`new_lines` is joined with `'\n'` and returned.  
The output contains:

* `<p>` blocks for normal paragraphs.
* `<ol>` / `<li>` for ordered lists.
* `<pre>` for fenced code blocks (indentation preserved).
* Inline tags (`<b>`, `<i>`, `<ins>`, `<code>`, `<a>`, `<img>`) inside the text.

---

## 3.  Wrapping the body into a full HTML document

`markdown_to_html` takes the Markdown string and a flag `add_css`.  
It builds a minimal HTML skeleton:

```html
<html>
<head>
    <style>ins { text-decoration: line-through; }</style>
    <!-- optional CSS links -->
</head>
<body>
    [compiled body from compile_lines]
</body>
</html>
```

If `add_css` is true, two external stylesheets are linked.

---

## 4.  File‑level conversion (`convert_file`)

* Validates that the input file ends with `.md`.
* Reads the file into a string.
* Calls `markdown_to_html` to get the full HTML.
* Writes the result to a file with the same name but an `.html` extension.

---

## 5.  Summary

1. **Read** the Markdown file.  
2. **Split** it into lines and walk through them, keeping track of whether we’re inside a paragraph, list, or code block.  
3. **Apply** the line‑level helpers to each line to replace Markdown markers with HTML tags.  
4. **Wrap** the processed lines in `<p>`, `<ol>`, `<pre>`, etc., as needed.  
5. **Insert** the resulting body into a minimal HTML skeleton (optionally adding CSS).  
6. **Write** the output to an `.html` file.

The design keeps the line‑level transformations simple and reusable, while the document‑level logic handles the structural aspects of Markdown (paragraphs, lists, code fences). This separation makes the code easy to understand, test, and extend.
chat> 

i learned: this command shows all of the important imputs of the  previous lab, then gives a summary with the important steps and the design.