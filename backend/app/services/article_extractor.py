"""Article extraction service for URLs, PDFs, and DOCX files."""
import logging
import io
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ExtractedArticle:
    """Structured article data from any source."""
    text: str
    title: str | None = None
    author: str | None = None
    publish_date: str | None = None
    source_url: str | None = None


def extract_from_url(url: str) -> ExtractedArticle:
    """Extract article content from a URL using trafilatura."""
    import trafilatura

    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise ValueError(f"Could not fetch content from URL: {url}")

        # Extract with metadata
        result = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
            output_format="txt",
        )

        if not result or len(result.strip()) < 50:
            raise ValueError("Extracted content too short or empty. The page may be paywalled or unsupported.")

        # Get metadata separately
        metadata = trafilatura.extract(
            downloaded,
            include_comments=False,
            output_format="xmltei",
        )
        
        # Try to extract metadata
        title = None
        author = None
        date = None
        
        try:
            meta = trafilatura.metadata.extract_metadata(downloaded)
            if meta:
                title = meta.title if hasattr(meta, 'title') else None
                author = meta.author if hasattr(meta, 'author') else None
                date = str(meta.date) if hasattr(meta, 'date') and meta.date else None
        except Exception:
            pass

        return ExtractedArticle(
            text=result,
            title=title,
            author=author,
            publish_date=date,
            source_url=url,
        )

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"URL extraction failed: {e}")
        raise ValueError(f"Failed to extract article from URL: {str(e)}")


def extract_from_pdf(file_bytes: bytes, filename: str = "document.pdf") -> ExtractedArticle:
    """Extract text from a PDF file using PyMuPDF."""
    import fitz  # PyMuPDF

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []

        for page in doc:
            text_parts.append(page.get_text("text"))

        doc.close()

        text = "\n".join(text_parts).strip()
        if len(text) < 50:
            raise ValueError("PDF contains too little extractable text.")

        # Clean up common PDF artifacts
        text = _clean_extracted_text(text)

        return ExtractedArticle(
            text=text,
            title=filename.replace(".pdf", ""),
        )

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def extract_from_docx(file_bytes: bytes, filename: str = "document.docx") -> ExtractedArticle:
    """Extract text from a DOCX file using python-docx."""
    from docx import Document

    try:
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        text = "\n\n".join(paragraphs)

        if len(text) < 50:
            raise ValueError("DOCX contains too little text.")

        return ExtractedArticle(
            text=text,
            title=filename.replace(".docx", ""),
        )

    except ValueError:
        raise
    except Exception as e:
        logger.error(f"DOCX extraction failed: {e}")
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")


def extract_from_txt(file_bytes: bytes, filename: str = "document.txt") -> ExtractedArticle:
    """Extract text from a plain text file."""
    try:
        text = file_bytes.decode("utf-8", errors="replace").strip()

        if len(text) < 50:
            raise ValueError("Text file contains too little content.")

        return ExtractedArticle(
            text=text,
            title=filename.replace(".txt", ""),
        )

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to read text file: {str(e)}")


def _clean_extracted_text(text: str) -> str:
    """Clean common artifacts from extracted text."""
    import re
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    # Remove page numbers
    text = re.sub(r'\n\d+\n', '\n', text)
    return text.strip()
