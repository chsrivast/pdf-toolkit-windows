import fitz  # PyMuPDF
from pdf2docx import Converter
from docx2pdf import convert as docx_convert
import os

def pdf_to_word(pdf_path, output_path):
    try:
        cv = Converter(pdf_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
        return True, "Successfully converted PDF to Word."
    except Exception as e:
        return False, f"Error: {str(e)}"

def word_to_pdf(docx_path, output_path):
    try:
        # Note: This requires Microsoft Word installed on the host machine to work perfectly.
        docx_convert(docx_path, output_path)
        return True, "Successfully converted Word to PDF."
    except Exception as e:
        return False, f"Error: {str(e)}"

def split_pdf(pdf_path, output_dir, pages_per_split=1):
    try:
        doc = fitz.open(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        for i in range(0, len(doc), pages_per_split):
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=i, to_page=min(i + pages_per_split - 1, len(doc) - 1))
            new_doc.save(os.path.join(output_dir, f"{base_name}_part_{i//pages_per_split + 1}.pdf"))
            new_doc.close()
        return True, "Successfully split PDF."
    except Exception as e:
        return False, f"Error: {str(e)}"

def delete_pages(pdf_path, output_path, pages_to_delete):
    try:
        doc = fitz.open(pdf_path)
        # Convert 1-based page numbers to 0-based and sort in reverse to avoid index shifting
        pages = sorted([int(p.strip()) - 1 for p in pages_to_delete.split(",")], reverse=True)
        
        for page_num in pages:
            if 0 <= page_num < len(doc):
                doc.delete_page(page_num)
                
        doc.save(output_path)
        return True, "Successfully deleted pages."
    except Exception as e:
        return False, f"Error: {str(e)}"

def add_watermark(pdf_path, output_path, watermark_text):
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            rect = page.rect
            # Insert text diagonally across the page with low opacity
            page.insert_text(
                point=(rect.width / 4, rect.height / 2),
                text=watermark_text,
                fontsize=50,
                color=(0.5, 0.5, 0.5), # Gray
                fill_opacity=0.3
            )
        doc.save(output_path)
        return True, "Watermark added successfully."
    except Exception as e:
        return False, f"Error: {str(e)}"

def simple_edit_text(pdf_path, output_path, old_text, new_text):
    """
    Finds text, redacts it, and inserts new text in its place.
    This is a basic implementation; complex formatting may not be preserved perfectly.
    """
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text_instances = page.search_for(old_text)
            for inst in text_instances:
                # Add redaction annotation over the old text
                page.add_redact_annot(inst, text=new_text, fill=(1, 1, 1)) # White background
            # Apply the redactions
            page.apply_redactions()
            
        doc.save(output_path)
        return True, "Text edited successfully."
    except Exception as e:
        return False, f"Error: {str(e)}"

def merge_pdfs(pdf_list, output_path):
    try:
        merged_doc = fitz.open()
        for pdf in pdf_list:
            with fitz.open(pdf) as doc:
                merged_doc.insert_pdf(doc)
        merged_doc.save(output_path)
        merged_doc.close()
        return True, "Successfully merged PDFs."
    except Exception as e:
        return False, f"Error: {str(e)}"

def compress_pdf(pdf_path, output_path):
    try:
        doc = fitz.open(pdf_path)
        # garbage=4 cleans up unused objects; deflate=True compresses data streams
        doc.save(output_path, garbage=4, deflate=True) 
        doc.close()
        return True, "Successfully compressed PDF."
    except Exception as e:
        return False, f"Error: {str(e)}"

def jpg_to_pdf(jpg_path, output_path):
    try:
        # PyMuPDF can open images and convert them to PDF bytes natively
        img_doc = fitz.open(jpg_path)
        pdf_bytes = img_doc.convert_to_pdf()
        pdf_doc = fitz.open("pdf", pdf_bytes)
        pdf_doc.save(output_path)
        img_doc.close()
        pdf_doc.close()
        return True, "Successfully converted JPG to PDF."
    except Exception as e:
        return False, f"Error: {str(e)}"

def pdf_to_jpg(pdf_path, output_dir):
    try:
        doc = fitz.open(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150) # 150 DPI is a good balance of quality and size
            output_file = os.path.join(output_dir, f"{base_name}_page_{i+1}.jpg")
            pix.save(output_file)
            
        doc.close()
        return True, f"Successfully extracted {len(doc)} JPGs."
    except Exception as e:
        return False, f"Error: {str(e)}"

def unlock_pdf(pdf_path, output_path, password):
    try:
        doc = fitz.open(pdf_path)
        if not doc.is_encrypted:
            doc.close()
            return False, "This PDF is not locked."
            
        if doc.authenticate(password):
            # Saving an authenticated document removes the encryption
            doc.save(output_path)
            doc.close()
            return True, "Successfully unlocked PDF."
        else:
            doc.close()
            return False, "Incorrect password."
    except Exception as e:
        return False, f"Error: {str(e)}"