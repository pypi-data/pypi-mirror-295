
# CPDFKit

While WKHTMLTOPDF and the pdf_kit have been fun for a while, it is time to grow up and use some real browser engine to render your HTML to PDF.

CPDFKit is a Python toolkit for rendering PDF documents using Chromium or Google Chrome in headless mode. It provides capabilities to generate PDFs from URLs, file paths, or directly from HTML content, with customizable options such as paper size, margins, and orientation.

It does not utilise the debugging port of chrome or selenium but subprocess to the call the binary directly. 

## Features

- **Render PDFs from URLs or file paths:** Easily generate PDFs from web pages or local HTML files.
- **Direct HTML to PDF conversion:** Convert HTML strings directly into PDF documents.
- **Customizable paper sizes:** Supports standard paper sizes like A4, A3, and more, including ability to specify custom dimensions.
- **Adjustable margins:** Set top, bottom, left, and right margins.
- **Landscape or Portrait orientation:** Generate PDFs in your preferred orientation.
- **JavaScript delay execution:** Add a delay before rendering to ensure JavaScript-heavy pages load completely.
- **Secure:** Runs Chrome with sandboxing disabled for operational compatibility but ensures path and URL sanitization to prevent common security issues.

## Installation

This toolkit requires a local installation of Google Chrome or Chromium. Ensure Chrome or Chromium is accessible in your system PATH or specify the path when using the toolkit.

### From GitHub

1. Clone the repository:
   ```bash
   git clone'https://github.com/codingcowde/cpdfkit.git
   ```
2. Navigate to the cloned directory:
   ```bash
   cd CPDFKit
   ```

### Via pip

```bash
pip install cpdfkit
```



## Usage

### Basic Example

Here is a simple example of how to generate a PDF from a URL and save it to a file:

```python
from cpdfkit import generate_pdf

# Generate PDF from a URL and save it to 'output.pdf'
generate_pdf(
    url_or_path="https://example.com",
    output_path="output.pdf",
    format="A4",
    margin_top=1,
    margin_bottom=1,
    margin_left=1,
    margin_right=1,
    js_delay=2,
    landscape=False
)
```

### HTML to PDF

You can also render PDFs directly from HTML strings:

```python
html_content = """
<html>
<head><title>Sample PDF</title></head>
<body><h1>Welcome to PDF Rendering</h1><p>This is a simple HTML to PDF conversion example.</p></body>
</html>
"""

pdf_data = generate_pdf(
    html_string=html_content,
    format="A4",
    margin_top=0.5,
    margin_bottom=0.5,
    margin_left=0.5,
    margin_right=0.5,
    js_delay=0,
    landscape=True
)

# Save the PDF data to a file
with open("output_from_html.pdf", "wb") as file:
    file.write(pdf_data)
```

### Configuration

You can customize the behavior by specifying various parameters:

- `format`: Paper size (e.g., "A4", "Letter").
- `margin_top`, `margin_bottom`, `margin_left`, `margin_right`: Margins in inches.
- `js_delay`: Time in seconds to wait before rendering the page, useful for waiting on JavaScript execution.
- `landscape`: Set to `True` for landscape orientation or `False` for portrait.

## Contributing

Contributions are welcome! Please read the contributing guide located in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
