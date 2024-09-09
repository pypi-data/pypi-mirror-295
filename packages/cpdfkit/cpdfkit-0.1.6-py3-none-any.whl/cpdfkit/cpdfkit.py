import subprocess
import time
import os
import shutil
import tempfile
from urllib.parse import urlparse
from cpdfkit.exceptions import (
    InvalidFormatException,
    InvalidWindowSizeException,
    InvalidDelayException,
    InvalidMarginException,
    InvalidUrlException,
    ChromiumPathException,
    NoDocumentException,
    DangerousPathException,
    InvalidPathException
)

# Dictionary of common paper sizes with dimensions in millimeters.
PAPER_SIZES = {
    "A0": (841, 1189),
    "A1": (594, 841),
    "A2": (420, 594),
    "A3": (297, 420),
    "A4": (210, 297),
    "A5": (148, 210),
    "A6": (105, 148),
    "A7": (74, 105),
    "A8": (52, 74),
    "A9": (37, 52),
    "A10": (26, 37),
    "B0": (1000, 1414),
    "B1": (707, 1000),
    "B2": (500, 707),
    "B3": (353, 500),
    "B4": (250, 353),
    "B5": (176, 250),
    "B6": (125, 176),
    "B7": (88, 125),
    "B8": (62, 88),
    "B9": (44, 62),
    "B10": (31, 44),
    "C0": (917, 1297),
    "C1": (648, 917),
    "C2": (458, 648),
    "C3": (324, 458),
    "C4": (229, 324),
    "C5": (162, 229),
    "C6": (114, 162),
    "C7": (81, 114),
    "C8": (57, 81),
    "C9": (40, 57),
    "C10": (28, 40),
    "Legal": (216, 356),
    "Letter": (216, 279),
    "Executive": (184, 267),
    "Tabloid": (279, 432),
}


class CPDFKit:
    """Toolkit for rendering PDFs using Chrome in headless mode."""

    def __init__(self, chrome_path=None, window_size=(1920, 1080)):
        """Initializes the toolkit with the path to Chrome and the desired window size.

        Args:
            chrome_path (str, optional): Path to the Chrome executable.
            window_size (tuple, optional): The dimensions of the browser window. Defaults to (1920, 1080)
        """
        provided_path_exists = False

        if isinstance(chrome_path, str):
            provided_path_exists = os.path.exists(chrome_path)

        if not chrome_path:
            chrome_path = find_chrome()
            provided_path_exists = isinstance(chrome_path, str)

        if not chrome_path or not provided_path_exists:
            raise ChromiumPathException(
                f"Chrome or Chromium browser not found at {chrome_path}. Please install it or provide the path."
            )

        self.chrome_path = chrome_path
        self.window_size = self._sanitize_window_size(window_size)

    def _sanitize_paper_size(self, format: str):
        """Ensures that the paper size format is valid.

        Args:
            format (str): The paper size format to validate.

        Returns:
            str: The validated paper size format.

        Raises:
            ValueError: If the format is not recognized.
        """
        if format in PAPER_SIZES:
            return format
        raise InvalidFormatException(
            f"Invalid format chosen. Must be one of {list(PAPER_SIZES.keys())}."
        )

    def _sanitize_window_size(self, window_size):
        """Validates and sanitizes the provided window size.

        Args:
            window_size (tuple): The window size to validate.

        Returns:
            tuple: The validated window size.

        Raises:
            ValueError: If the window size is invalid.
        """
        if isinstance(window_size, tuple) and len(window_size) == 2:
            width, height = window_size
            if (
                isinstance(width, int)
                and isinstance(height, int)
                and width > 0
                and height > 0
            ):
                return window_size
        raise InvalidWindowSizeException(
            "Invalid window size. Must be a tuple of two positive integers."
        )

    def _sanitize_path(self, path):
        """Validates and sanitizes the provided filesystem path.

        Args:
            path (str): The path to validate.

        Returns:
            str: The sanitized path.

        Raises:
            ValueError: If the path is potentially dangerous or malformed.
        """
        if not isinstance(path, str) or path == "":
            raise InvalidPathException("Invalid path provided.")
        path = os.path.normpath(path)
        if any(x in path for x in ("..", "~", "//", "\\\\")):
            raise DangerousPathException("Invalid path contains potentially dangerous components.")
        return path

    def _sanitize_url(self, url):
        """Validates and sanitizes the provided URL.

        Args:
            url (str): The URL to validate.

        Returns:
            str: The sanitized URL.

        Raises:
            ValueError: If the URL is not properly formatted or is unsafe.
        """
        parsed_url = urlparse(url)
        if not parsed_url.scheme or parsed_url.scheme not in ("http", "https", "file"):
            raise InvalidUrlException("URL must start with http://, https://, or file://")
        return url

    def _sanitize_delay(self, delay):
        """Validates and sanitizes the provided delay for JavaScript execution.

        Args:
            delay (int): The delay in seconds.

        Returns:
            int: The validated non-negative delay.

        Raises:
            ValueError: If the delay is negative.
        """
        if isinstance(delay, int) and delay >= 0:
            return delay
        raise InvalidDelayException("JavaScript delay must be a non-negative integer.")

    def _sanitize_margins(self, margin):
        """Validates and sanitizes the provided margin values.

        Args:
            margin (float): The margin value to validate.

        Returns:
            float: The validated non-negative margin.

        Raises:
            ValueError: If the margin is negative.
        """
        if isinstance(margin, (int, float)) and margin >= 0:
            return margin
        raise InvalidMarginException("Margins must be non-negative numbers.")

    def render_pdf(
        self,
        url_or_path,
        output_path=None,
        format="A4",
        margin_top=0,
        margin_bottom=0,
        margin_left=0,
        margin_right=0,
        js_delay=0,
        landscape=False,
    ):
        """Renders a PDF from a URL or a file path.

        Args:
            url_or_path (str): The URL or file path to render.
            output_path (str, optional): The path where the PDF will be saved.
            format (str): The paper size format.
            margin_top (float): The top margin in inches.
            margin_bottom (float): The bottom margin in inches.
            margin_left (float): The left margin in inches.
            margin_right (float): The right margin in inches.
            js_delay (int): The delay in milliseconds before rendering the page.
            landscape (bool): Whether to render the page in landscape orientation.

        Returns:
            bytes|None: The PDF data if no output path is specified, otherwise None.

        Raises:
            subprocess.CalledProcessError: If the Chrome subprocess fails.
        """
        sanitized_input = (
            self._sanitize_url(url_or_path)
            if url_or_path.startswith(("http", "file"))
            else self._sanitize_path(url_or_path)
        )
        sanitized_delay = self._sanitize_delay(js_delay)
        sanitized_margins = {
            "top": self._sanitize_margins(margin_top),
            "bottom": self._sanitize_margins(margin_bottom),
            "left": self._sanitize_margins(margin_left),
            "right": self._sanitize_margins(margin_right),
        }
        sanitized_format = self._sanitize_paper_size(format)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
            temp_pdf_path = temp_pdf_file.name

        try:
            chrome_command = [
                self._sanitize_path(self.chrome_path),
                "--headless",
                "--disable-gpu",
                "--run-all-compositor-stages-before-draw",
                "--no-pdf-header-footer",
                "--print-to-pdf-no-header",
                "--no-sandbox",
                f"--window-size={self.window_size[0]},{self.window_size[1]}",
                f"--print-to-pdf={temp_pdf_path}",
            ]

            if sanitized_margins:
                chrome_command.extend(
                    [
                        f'--print-to-pdf-margin-top={sanitized_margins["top"]}',
                        f'--print-to-pdf-margin-bottom={sanitized_margins["bottom"]}',
                        f'--print-to-pdf-margin-left={sanitized_margins["left"]}',
                        f'--print-to-pdf-margin-right={sanitized_margins["right"]}',
                    ]
                )
            else:
                chrome_command.append("--no-margins")

            if format in PAPER_SIZES:
                w, h = PAPER_SIZES[sanitized_format]
                chrome_command.append(f"--print-to-pdf-paper-size={w},{h}")

            if landscape:
                chrome_command.append("--landscape")

            if sanitized_delay and sanitized_delay > 0:
                chrome_command.append(f"--virtual-time-budget={sanitized_delay}")


            chrome_command.append(sanitized_input)
            subprocess.run(chrome_command, check=True)

            with open(temp_pdf_path, "rb") as file:
                pdf_data = file.read()

            if output_path:
                with open(self._sanitize_path(output_path), "wb") as file:
                    file.write(pdf_data)
                return None
            else:
                return pdf_data

        finally:
            os.remove(temp_pdf_path)

    def html_to_pdf(
        self,
        html_string,
        output_path=None,
        format="A4",
        margin_top=0,
        margin_bottom=0,
        margin_left=0,
        margin_right=0,
        js_delay=0,
        landscape=False,
    ):
        """Converts HTML string to PDF.

        Args:
            html_string (str): The HTML content to render into a PDF.
            output_path (str, optional): The path where the PDF will be saved.
            format (str): The paper size format.
            margin_top (float): The top margin in inches.
            margin_bottom (float): The bottom margin in inches.
            margin_left (float): The left margin in inches.
            margin_right (float): The right margin in inches.
            js_delay (int): The delay in seconds before rendering the page.
            landscape (bool): Whether to render the page in landscape orientation.

        Returns:
            bytes|None: The PDF data if no output path is specified, otherwise None.

        Raises:
            IOError: If the HTML file creation or reading fails.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            temp_file.write(html_string.encode("utf-8"))
            temp_file_path = temp_file.name

        try:
            return self.render_pdf(
                url_or_path=f"file://{temp_file_path}",
                output_path=output_path,
                format=format,
                margin_top=margin_top,
                margin_bottom=margin_bottom,
                margin_left=margin_left,
                margin_right=margin_right,
                js_delay=js_delay,
                landscape=landscape,
            )
        finally:
            os.remove(temp_file_path)

    def close(self):
        """Cleans up any resources used by the toolkit."""
        pass


def find_chrome():
    """Searches for the Chrome or Chromium browser executable on the system.

    Returns:
        str|None: The path to the executable, or None if not found.
    """
    paths = [
        shutil.which("chrome"),
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
    ]
    for path in paths:
        if path:
            return path
    return None


def generate_pdf(
    url_or_path=None,
    html_string=None,
    output_path=None,
    format="A4",
    margin_top=0,
    margin_bottom=0,
    margin_left=0,
    margin_right=0,
    js_delay=0,
    landscape=False,
    chrome_path=None,
):
    """Generates a PDF from a URL or HTML string using detected Chrome.

    Args:
        url_or_path (str, optional): The URL or file path to render.
        html_string (str, optional): The HTML content to render.
        output_path (str, optional): The path where the PDF will be saved.
        format (str): The paper size format.
        margin_top (float): The top margin.
        margin_bottom (float): The bottom margin.
        margin_left (float): The left margin.
        margin_right (float): The right margin.
        js_delay (int): The delay before rendering.
        landscape (bool): Whether to render in landscape orientation.
        chrome_path(string, optional): Provide a path to your Chrome installation

    Returns:
        bytes|None: The generated PDF data, or None if saved to a file.

    Raises:
        EnvironmentError: If Chrome is not found on the system.
        ValueError: If neither `url_or_path` nor `html_string` is provided.
    """

    toolkit = CPDFKit(chrome_path=chrome_path)

    try:
        if html_string is not None:
            return toolkit.html_to_pdf(
                html_string=html_string,
                output_path=output_path,
                format=format,
                margin_top=margin_top,
                margin_bottom=margin_bottom,
                margin_left=margin_left,
                margin_right=margin_right,
                js_delay=js_delay,
                landscape=landscape,
                
            )
        elif url_or_path is not None:
            return toolkit.render_pdf(
                url_or_path=url_or_path,
                output_path=output_path,
                format=format,
                margin_top=margin_top,
                margin_bottom=margin_bottom,
                margin_left=margin_left,
                margin_right=margin_right,
                js_delay=js_delay,
                landscape=landscape,
            )
        else:
            raise NoDocumentException("Either url_or_path or html_string must be provided.")
    finally:
        toolkit.close()


# Example usage:
if __name__ == "__main__":
    try:
        # Generate a PDF from a URL and save it to a file.
        generate_pdf(
            url_or_path="https://codingcow.de",
            output_path="output.pdf",
            format="A4",
            margin_top=0,
            margin_bottom=0,
            margin_left=0,
            margin_right=0,
            js_delay=2,
            landscape=False,
        )

        # Generate a PDF from an HTML string.
        html_content = """
        <html>
        <head><title>Test PDF</title></head>
        <body><h1>Hello, PDF!</h1><p>This is a test.</p></body>
        </html>
        """
        pdf_bytes = generate_pdf(
            html_string=html_content,
            format="A4",
            margin_top=10,
            margin_bottom=10,
            margin_left=10,
            margin_right=10,
            js_delay=2,
            landscape=False,
        )
        if pdf_bytes:
            print(f"PDF generated, length: {len(pdf_bytes)} bytes")
    except ValueError as e:
        print(f"Input validation error: {str(e)}")
    except RuntimeError as e:
        print(f"Rendering error: {str(e)}")
    except EnvironmentError as e:
        print(f"Chrome detection error: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


