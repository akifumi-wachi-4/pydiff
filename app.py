#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import difflib
import re

app = FastAPI(title="diff-python", version="1.0")

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Default sample texts for demo
DEFAULT_TEXT_A = """"""

DEFAULT_TEXT_B = """"""


def split_text_for_diff(text: str) -> list:
    """Split text into comparison units (words/characters) like the original Perl version"""
    if not text:
        return []

    # Replace newlines with special marker like original
    text = text.replace("\n", "<$>")

    # Split into words (English) or characters (Japanese/others)
    tokens = []
    i = 0
    while i < len(text):
        # HTML entities
        if text[i] == "&":
            match = re.match(r"&#?\w+;", text[i:])
            if match:
                tokens.append(match.group())
                i += len(match.group())
                continue

        # Special newline marker
        if text[i : i + 3] == "<$>":
            tokens.append("<$>")
            i += 3
            continue

        # English words (lowercase letters)
        match = re.match(r"[a-z]+", text[i:], re.IGNORECASE)
        if match:
            tokens.append(match.group())
            i += len(match.group())
            continue

        # Single character
        tokens.append(text[i])
        i += 1

    return tokens


def escape_html(text: str) -> str:
    """Escape HTML characters like the original escape_char function"""
    if not text:
        return ""

    # More comprehensive HTML escaping to prevent XSS
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("'", "&#39;")
    text = text.replace('"', "&quot;")
    text = text.replace("/", "&#x2F;")  # Forward slash
    text = text.replace("`", "&#x60;")  # Backtick
    text = text.replace("=", "&#x3D;")  # Equals sign
    return text


def escape_spaces(text: str) -> str:
    """Convert spaces to &nbsp; like the original escape_space function"""
    return re.sub(r"\s", "&nbsp;", text)


def count_characters(text: str) -> dict:
    """Count characters like the original count_char function"""
    if not text:
        return {"chars_only": 0, "with_spaces": 0, "with_newlines": 0, "words": 0}

    # Count words
    words = re.findall(r"\S+", text)
    word_count = len(words)

    # Remove CR and count
    text_no_cr = text.replace("\r", "")
    char_count_with_newlines = len(text_no_cr)

    # Remove newlines and count
    text_no_newlines = text_no_cr.replace("\n", "")
    char_count_with_spaces = len(text_no_newlines)

    # Remove all whitespace and count
    text_no_spaces = re.sub(r"\s", "", text_no_newlines)
    char_count_only = len(text_no_spaces)

    # Ensure all values are integers (security)
    return {
        "chars_only": int(char_count_only),
        "with_spaces": int(char_count_with_spaces),
        "with_newlines": int(char_count_with_newlines),
        "words": int(word_count),
    }


def compare_texts(text_a: str, text_b: str) -> str:
    """Compare two texts and return HTML with highlighted differences"""
    if not text_a and not text_b:
        return ""

    # Escape HTML in input texts
    escaped_a = escape_html(text_a)
    escaped_b = escape_html(text_b)

    # Split texts into tokens
    tokens_a = split_text_for_diff(escaped_a)
    tokens_b = split_text_for_diff(escaped_b)

    # Use difflib to find differences
    diff = difflib.unified_diff(tokens_a, tokens_b, n=0, lineterm="")
    diff_lines = list(diff)

    # Process diff output to highlight changes
    result_a = tokens_a.copy()
    result_b = tokens_b.copy()

    # Parse diff output
    i = 0
    while i < len(diff_lines):
        line = diff_lines[i]
        if line.startswith("@@"):
            # Parse hunk header: @@ -start_a,count_a +start_b,count_b @@
            match = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
            if match:
                start_a = int(match.group(1)) - 1  # Convert to 0-based
                count_a = int(match.group(2)) if match.group(2) else 1
                start_b = int(match.group(3)) - 1  # Convert to 0-based
                count_b = int(match.group(4)) if match.group(4) else 1

                # Highlight deleted tokens (from text A)
                if count_a > 0:
                    if start_a < len(result_a):
                        result_a[start_a] = "<em>" + result_a[start_a]
                    end_a = min(start_a + count_a - 1, len(result_a) - 1)
                    if end_a >= 0:
                        result_a[end_a] += "</em>"

                # Highlight added tokens (in text B)
                if count_b > 0:
                    if start_b < len(result_b):
                        result_b[start_b] = "<em>" + result_b[start_b]
                    end_b = min(start_b + count_b - 1, len(result_b) - 1)
                    if end_b >= 0:
                        result_b[end_b] += "</em>"
        i += 1

    # Join tokens back and split by newline markers
    final_a = "".join(result_a)
    final_b = "".join(result_b)

    # Handle em tags that cross newline boundaries
    while re.search(r"(<em>[^<>]*)<\$>(([^<>]|<\$>)*</em>)", final_a):
        final_a = re.sub(
            r"(<em>[^<>]*)<\$>(([^<>]|<\$>)*</em>)", r"\1</em><$><em>\2", final_a
        )

    while re.search(r"(<em>[^<>]*)<\$>(([^<>]|<\$>)*</em>)", final_b):
        final_b = re.sub(
            r"(<em>[^<>]*)<\$>(([^<>]|<\$>)*</em>)", r"\1</em><$><em>\2", final_b
        )

    # Split by newline markers
    lines_a = final_a.split("<$>")
    lines_b = final_b.split("<$>")

    # Make arrays equal length
    max_lines = max(len(lines_a), len(lines_b))
    while len(lines_a) < max_lines:
        lines_a.append("")
    while len(lines_b) < max_lines:
        lines_b.append("")

    # Generate table rows
    rows = []
    for i in range(max_lines):
        # Handle spaces before closing em tags
        line_a = re.sub(r"(\s+</em>)", lambda m: escape_spaces(m.group(1)), lines_a[i])
        line_b = re.sub(r"(\s+</em>)", lambda m: escape_spaces(m.group(1)), lines_b[i])

        rows.append({"text_a": line_a, "text_b": line_b})

    return rows


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Show the main comparison page"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "text_a": DEFAULT_TEXT_A,
            "text_b": DEFAULT_TEXT_B,
            "show_result": False,
            "comparison_result": None,
            "stats_a": None,
            "stats_b": None,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def compare(
    request: Request, sequenceA: str = Form(""), sequenceB: str = Form("")
):
    """Process text comparison"""
    
    # Input size limit for DoS prevention (100KB per field)
    MAX_INPUT_SIZE = 100 * 1024
    if len(sequenceA) > MAX_INPUT_SIZE or len(sequenceB) > MAX_INPUT_SIZE:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "text_a": "",
                "text_b": "",
                "show_result": False,
                "comparison_result": None,
                "stats_a": None,
                "stats_b": None,
                "error": "入力テキストが大きすぎます。各フィールド100KB（約10万文字）以内にしてください。"
            },
        )
    
    # Validate input contains only safe characters (optional strict validation)
    # This could be uncommented for extra security but may be too restrictive
    # import string
    # allowed_chars = set(string.printable + ''.join(chr(i) for i in range(0x3040, 0x30FF)))  # Japanese characters
    # if sequenceA and not all(c in allowed_chars for c in sequenceA):
    #     return templates.TemplateResponse("index.html", {..., "error": "無効な文字が含まれています"})
    
    # Rate limiting could be added here for production use

    # If both texts are empty, show default page
    if not sequenceA and not sequenceB:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "text_a": DEFAULT_TEXT_A,
                "text_b": DEFAULT_TEXT_B,
                "show_result": False,
                "comparison_result": None,
                "stats_a": None,
                "stats_b": None,
            },
        )

    try:
        # Compare texts
        comparison_result = compare_texts(sequenceA, sequenceB)

        # Calculate character statistics
        stats_a = count_characters(sequenceA)
        stats_b = count_characters(sequenceB)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "text_a": sequenceA,
                "text_b": sequenceB,
                "show_result": True,
                "comparison_result": comparison_result,
                "stats_a": stats_a,
                "stats_b": stats_b,
            },
        )
    except Exception:
        # Handle any unexpected errors gracefully
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "text_a": sequenceA,
                "text_b": sequenceB,
                "show_result": False,
                "comparison_result": None,
                "stats_a": None,
                "stats_b": None,
                "error": ""
            },
        )
