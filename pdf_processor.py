"""
PDF processing for NyayAI - handles PDF text extraction and processing
"""
import io
from typing import Optional, Tuple

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

class PDFProcessor:
    def __init__(self):
        self.available = PYMUPDF_AVAILABLE
    
    def is_available(self) -> bool:
        """Check if PDF processing is available"""
        return self.available
    
    def extract_text_from_pdf(self, pdf_file, max_pages: int = None, preview_mode: bool = False) -> Tuple[str, bool]:
        """
        Extract text from PDF file
        Args:
            pdf_file: The PDF file to process
            max_pages: Maximum number of pages to process (None for all pages)
            preview_mode: If True, only extract first 1000 chars per page
        Returns: (extracted_text, success)
        """
        if not self.available:
            return "PDF processing library not available. Please install PyMuPDF.", False
        
        try:
            try:
                pdf_file.seek(0)
            except Exception:
                pass

            pdf_bytes = pdf_file.read()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            extracted_text = ""
            total_pages = len(pdf_document)
            pages_to_process = min(max_pages or total_pages, total_pages)
            
            # Only process specified number of pages
            for page_num in range(pages_to_process):
                page = pdf_document[page_num]
                text = page.get_text()
                if preview_mode:
                    text = text[:1000] + "..." if len(text) > 1000 else text
                extracted_text += f"\n--- Page {page_num + 1} of {total_pages} ---\n{text}\n"
                
                # For large documents in preview mode, stop after getting enough text
                if preview_mode and len(extracted_text) > 5000:
                    extracted_text += f"\n... Preview truncated. {total_pages - page_num - 1} more pages available ..."
                    break
            
            pdf_document.close()
            
            if not extracted_text.strip():
                return "No text could be extracted from this PDF. The document might contain only images or be password protected.", False
            
            try:
                pdf_file.seek(0)
            except Exception:
                pass

            return extracted_text, True
            
        except Exception as e:
            return f"Error processing PDF: {str(e)}", False
    
    def get_pdf_info(self, pdf_file) -> dict:
        """Get basic PDF information"""
        if not self.available:
            return {"error": "PDF processing not available"}
        
        try:
            try:
                pdf_file.seek(0)
            except Exception:
                pass

            pdf_bytes = pdf_file.read()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            info = {
                "pages": len(pdf_document),
                "title": pdf_document.metadata.get("title", "Unknown"),
                "author": pdf_document.metadata.get("author", "Unknown"),
                "subject": pdf_document.metadata.get("subject", "Unknown"),
                "creator": pdf_document.metadata.get("creator", "Unknown")
            }
            
            pdf_document.close()
            return info
            
        except Exception as e:
            return {"error": f"Could not read PDF info: {str(e)}"}
    
    def preview_pdf_pages(self, pdf_file, max_pages: int = 3) -> list:
        """Get preview text from first few pages"""
        if not self.available:
            return ["PDF processing not available"]
        
        try:
            try:
                pdf_file.seek(0)
            except Exception:
                pass

            pdf_bytes = pdf_file.read()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            previews = []
            pages_to_preview = min(max_pages, len(pdf_document))
            
            for page_num in range(pages_to_preview):
                page = pdf_document[page_num]
                text = page.get_text()
                # Get first 500 characters of each page
                preview_text = text[:500] + "..." if len(text) > 500 else text
                previews.append(f"**Page {page_num + 1}:**\n{preview_text}")
            
            pdf_document.close()
            try:
                pdf_file.seek(0)
            except Exception:
                pass
            return previews
            
        except Exception as e:
            return [f"Error previewing PDF: {str(e)}"]