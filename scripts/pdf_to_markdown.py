#!/usr/bin/env python3
"""
PDF to Markdown Converter with OCR

Converts a PDF (scanned or digital) to structured markdown with:
- Table of contents with links
- Chapter/section detection
- Page number references
- Multiple output formats (single file or directory structure)

Requirements:
    pip install pdf2image pytesseract pymupdf Pillow

System dependencies:
    - Tesseract OCR: sudo apt install tesseract-ocr
    - Poppler (for pdf2image): sudo apt install poppler-utils

Usage:
    python pdf_to_markdown.py input.pdf -o output/
    python pdf_to_markdown.py input.pdf --single-file -o book.md
    python pdf_to_markdown.py input.pdf --detect-chapters
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import fitz  # pymupdf
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nInstall with:")
    print("  pip install pdf2image pytesseract pymupdf Pillow")
    print("\nAlso install system dependencies:")
    print("  sudo apt install tesseract-ocr poppler-utils")
    sys.exit(1)


@dataclass
class Page:
    """Represents a single page of content."""
    number: int
    text: str
    chapter: Optional[str] = None
    section: Optional[str] = None


@dataclass
class Chapter:
    """Represents a chapter in the book."""
    title: str
    start_page: int
    pages: list[Page] = field(default_factory=list)


@dataclass
class Book:
    """Represents the entire book structure."""
    title: str
    chapters: list[Chapter] = field(default_factory=list)
    pages: list[Page] = field(default_factory=list)


class PDFToMarkdown:
    """Main converter class."""

    # Patterns for detecting chapters/sections
    # Note: Patterns are checked in order; first match wins
    CHAPTER_PATTERNS = [
        r'^Chapter\s+(\d+|[IVXLC]+)[:\.\s]*(.*)',
        r'^CHAPTER\s+(\d+|[IVXLC]+)[:\.\s]*(.*)',
        r'^Part\s+(\d+|[IVXLC]+)[:\.\s]*(.*)',
        r'^PART\s+(\d+|[IVXLC]+)[:\.\s]*(.*)',
        r'^§\s*(\d+)\s*(.*)',  # "§1 Topic"
        # Numbered chapters with ALL CAPS title (at least 3 words)
        r'^(\d+)\s+([A-Z]{2,}(?:\s+[A-Z]{2,}){2,})$',
    ]

    SECTION_PATTERNS = [
        r'^(\d+\.\d+)\s+(.*)',  # "1.1 Subsection"
        r'^Section\s+(\d+)[:\.\s]*(.*)',
        r'^§\s*(\d+\.\d+)\s*(.*)',
    ]

    # Words that indicate this is NOT a chapter (e.g., exercise starters)
    CHAPTER_BLACKLIST = [
        r'^(\d+)\.\s*(Let|Define|Prove|Show|Find|Compute|If|Suppose|Given)',
    ]

    def __init__(
        self,
        pdf_path: str,
        use_ocr: bool = True,
        ocr_lang: str = "eng",
        dpi: int = 300,
        detect_chapters: bool = True,
    ):
        self.pdf_path = Path(pdf_path)
        self.use_ocr = use_ocr
        self.ocr_lang = ocr_lang
        self.dpi = dpi
        self.detect_chapters = detect_chapters

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

    def extract_text_native(self, page_num: int) -> str:
        """Extract text from PDF using PyMuPDF (for digital PDFs)."""
        doc = fitz.open(self.pdf_path)
        page = doc[page_num]
        text = page.get_text()
        doc.close()
        return text.strip()

    def extract_text_ocr(self, page_num: int) -> str:
        """Extract text using OCR (for scanned PDFs)."""
        images = convert_from_path(
            self.pdf_path,
            first_page=page_num + 1,
            last_page=page_num + 1,
            dpi=self.dpi,
        )
        if not images:
            return ""

        text = pytesseract.image_to_string(images[0], lang=self.ocr_lang)
        return text.strip()

    def extract_text(self, page_num: int) -> str:
        """Extract text from a page, using OCR if needed."""
        # First try native extraction
        text = self.extract_text_native(page_num)

        # If no text or very little text, try OCR
        if self.use_ocr and len(text.strip()) < 50:
            ocr_text = self.extract_text_ocr(page_num)
            if len(ocr_text) > len(text):
                text = ocr_text

        return text

    def detect_chapter(self, text: str) -> Optional[str]:
        """Detect if text starts with a chapter heading."""
        lines = text.split('\n')[:10]  # Check first 10 lines

        for line in lines:
            line = line.strip()
            if not line:
                continue

            for pattern in self.CHAPTER_PATTERNS:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # Return the full chapter title
                    return line

        return None

    def detect_section(self, text: str) -> Optional[str]:
        """Detect section headings in text."""
        lines = text.split('\n')[:10]

        for line in lines:
            line = line.strip()
            if not line:
                continue

            for pattern in self.SECTION_PATTERNS:
                match = re.match(pattern, line)
                if match:
                    return line

        return None

    def get_page_count(self) -> int:
        """Get total number of pages in the PDF."""
        doc = fitz.open(self.pdf_path)
        count = len(doc)
        doc.close()
        return count

    def process(self, progress_callback=None) -> Book:
        """Process the entire PDF and return a Book structure."""
        book = Book(title=self.pdf_path.stem)
        total_pages = self.get_page_count()

        current_chapter = None

        for page_num in range(total_pages):
            if progress_callback:
                progress_callback(page_num + 1, total_pages)

            text = self.extract_text(page_num)

            page = Page(
                number=page_num + 1,
                text=text,
            )

            # Detect chapter/section
            if self.detect_chapters:
                chapter_title = self.detect_chapter(text)
                if chapter_title:
                    current_chapter = Chapter(
                        title=chapter_title,
                        start_page=page_num + 1,
                    )
                    book.chapters.append(current_chapter)
                    page.chapter = chapter_title

                section_title = self.detect_section(text)
                if section_title:
                    page.section = section_title

            # Add page to current chapter and global list
            if current_chapter:
                current_chapter.pages.append(page)
            book.pages.append(page)

        return book

    def to_markdown_single(self, book: Book) -> str:
        """Convert book to a single markdown file."""
        lines = []

        # Title
        lines.append(f"# {book.title}\n")

        # Table of Contents
        lines.append("## Table of Contents\n")

        if book.chapters:
            for i, chapter in enumerate(book.chapters, 1):
                anchor = self._make_anchor(chapter.title)
                lines.append(f"- [{chapter.title}](#{anchor}) (p. {chapter.start_page})")
        else:
            # Just list pages
            for page in book.pages:
                lines.append(f"- [Page {page.number}](#page-{page.number})")

        lines.append("\n---\n")

        # Content
        if book.chapters:
            for chapter in book.chapters:
                lines.append(f"\n## {chapter.title}\n")
                lines.append(f"*Starting page: {chapter.start_page}*\n")

                for page in chapter.pages:
                    lines.append(f"\n### Page {page.number} {{#page-{page.number}}}\n")
                    if page.section and page.section != chapter.title:
                        lines.append(f"**{page.section}**\n")
                    lines.append(self._clean_text(page.text))
                    lines.append("\n")
        else:
            for page in book.pages:
                lines.append(f"\n## Page {page.number} {{#page-{page.number}}}\n")
                lines.append(self._clean_text(page.text))
                lines.append("\n")

        return '\n'.join(lines)

    def to_markdown_directory(self, book: Book, output_dir: Path) -> None:
        """Convert book to a directory structure with multiple files."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create index file
        index_lines = [f"# {book.title}\n", "## Table of Contents\n"]

        if book.chapters:
            for i, chapter in enumerate(book.chapters, 1):
                chapter_dir = output_dir / f"chapter-{i:02d}"
                chapter_dir.mkdir(exist_ok=True)

                # Add to index
                safe_title = self._safe_filename(chapter.title)
                index_lines.append(
                    f"- [{chapter.title}](chapter-{i:02d}/README.md) (p. {chapter.start_page})"
                )

                # Create chapter README
                chapter_readme = [
                    f"# {chapter.title}\n",
                    f"*Pages {chapter.start_page}-{chapter.start_page + len(chapter.pages) - 1}*\n",
                    "## Pages\n",
                ]

                for page in chapter.pages:
                    chapter_readme.append(f"- [Page {page.number}](page-{page.number:03d}.md)")

                    # Create page file
                    page_content = [
                        f"# Page {page.number}\n",
                        f"[← Back to Chapter](./) | ",
                        f"[← Table of Contents](../)\n",
                    ]
                    if page.section:
                        page_content.append(f"\n**{page.section}**\n")
                    page_content.append(f"\n{self._clean_text(page.text)}\n")

                    page_file = chapter_dir / f"page-{page.number:03d}.md"
                    page_file.write_text('\n'.join(page_content))

                chapter_readme_file = chapter_dir / "README.md"
                chapter_readme_file.write_text('\n'.join(chapter_readme))
        else:
            # No chapters detected - flat structure
            pages_dir = output_dir / "pages"
            pages_dir.mkdir(exist_ok=True)

            for page in book.pages:
                index_lines.append(f"- [Page {page.number}](pages/page-{page.number:03d}.md)")

                page_content = [
                    f"# Page {page.number}\n",
                    f"[← Table of Contents](../)\n",
                    f"\n{self._clean_text(page.text)}\n",
                ]

                page_file = pages_dir / f"page-{page.number:03d}.md"
                page_file.write_text('\n'.join(page_content))

        # Write index
        index_file = output_dir / "README.md"
        index_file.write_text('\n'.join(index_lines))

    def _make_anchor(self, text: str) -> str:
        """Create a markdown anchor from text."""
        anchor = text.lower()
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)
        return anchor

    def _safe_filename(self, text: str) -> str:
        """Create a safe filename from text."""
        safe = re.sub(r'[^\w\s-]', '', text)
        safe = re.sub(r'\s+', '-', safe)
        return safe[:50].lower()

    def _clean_text(self, text: str) -> str:
        """Clean OCR text for markdown."""
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Fix common OCR errors (can be expanded)
        text = text.replace('|', 'I')  # Common OCR mistake
        return text.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to structured Markdown with OCR support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s textbook.pdf -o output/
      Convert to directory structure with chapters

  %(prog)s textbook.pdf --single-file -o book.md
      Convert to single markdown file

  %(prog)s scanned.pdf --ocr-only --lang eng+fra
      Force OCR with multiple languages

  %(prog)s book.pdf --no-chapters -o flat/
      Skip chapter detection
        """,
    )

    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("-o", "--output", required=True, help="Output file or directory")
    parser.add_argument(
        "--single-file",
        action="store_true",
        help="Output as single markdown file instead of directory",
    )
    parser.add_argument(
        "--ocr-only",
        action="store_true",
        help="Force OCR even for digital PDFs",
    )
    parser.add_argument(
        "--no-ocr",
        action="store_true",
        help="Disable OCR (native text extraction only)",
    )
    parser.add_argument(
        "--lang",
        default="eng",
        help="Tesseract language(s), e.g., 'eng' or 'eng+deu' (default: eng)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI for OCR image conversion (default: 300)",
    )
    parser.add_argument(
        "--no-chapters",
        action="store_true",
        help="Skip chapter/section detection",
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=1,
        help="Start from this page number (default: 1)",
    )
    parser.add_argument(
        "--end-page",
        type=int,
        help="End at this page number (default: last page)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show progress",
    )

    args = parser.parse_args()

    # Progress callback
    def progress(current, total):
        if args.verbose:
            print(f"\rProcessing page {current}/{total}...", end="", flush=True)

    # Create converter
    converter = PDFToMarkdown(
        pdf_path=args.pdf,
        use_ocr=not args.no_ocr,
        ocr_lang=args.lang,
        dpi=args.dpi,
        detect_chapters=not args.no_chapters,
    )

    print(f"Processing: {args.pdf}")
    print(f"Total pages: {converter.get_page_count()}")

    # Process the PDF
    book = converter.process(progress_callback=progress)

    if args.verbose:
        print()  # New line after progress

    # Output
    if args.single_file:
        markdown = converter.to_markdown_single(book)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown)
        print(f"Written to: {output_path}")
    else:
        output_dir = Path(args.output)
        converter.to_markdown_directory(book, output_dir)
        print(f"Written to: {output_dir}/")

    # Summary
    print(f"\nSummary:")
    print(f"  Pages processed: {len(book.pages)}")
    print(f"  Chapters detected: {len(book.chapters)}")

    if book.chapters:
        print("\nChapters:")
        for ch in book.chapters:
            print(f"  - {ch.title} (p. {ch.start_page}, {len(ch.pages)} pages)")


if __name__ == "__main__":
    main()
