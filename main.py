import customtkinter as ctk
from tkinter import filedialog, messagebox
import pdf_operations
import os
import sys

# Prevent missing console crash for docx2pdf
if sys.stdout is None: sys.stdout = open(os.devnull, 'w')
if sys.stderr is None: sys.stderr = open(os.devnull, 'w')

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")

class PDFToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF Toolkit V2")
        self.geometry("550x500")

        self.label = ctk.CTkLabel(self, text="PDF Toolkit V2", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=15)

        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="green")
        self.status_label.pack(pady=5)

        # Create Tabs for organization
        self.tabview = ctk.CTkTabview(self, width=500, height=300)
        self.tabview.pack(padx=20, pady=10)

        self.tab_convert = self.tabview.add("Convert")
        self.tab_modify = self.tabview.add("Modify")
        self.tab_security = self.tabview.add("Security & Size")

        self.populate_tabs()

    def update_status(self, success, message):
        color = "green" if success else "red"
        self.status_label.configure(text=message, text_color=color)

    def populate_tabs(self):
        # --- CONVERT TAB ---
        ctk.CTkButton(self.tab_convert, text="PDF to Word", command=self.do_pdf_to_word).pack(pady=10)
        ctk.CTkButton(self.tab_convert, text="Word to PDF", command=self.do_word_to_pdf).pack(pady=10)
        ctk.CTkButton(self.tab_convert, text="JPG to PDF", command=self.do_jpg_to_pdf).pack(pady=10)
        ctk.CTkButton(self.tab_convert, text="PDF to JPG", command=self.do_pdf_to_jpg).pack(pady=10)

        # --- MODIFY TAB ---
        ctk.CTkButton(self.tab_modify, text="Merge PDFs", command=self.do_merge_pdfs).pack(pady=10)
        ctk.CTkButton(self.tab_modify, text="Split PDF", command=self.do_split_pdf).pack(pady=10)
        ctk.CTkButton(self.tab_modify, text="Delete Pages", command=self.do_delete_pages).pack(pady=10)
        ctk.CTkButton(self.tab_modify, text="Edit Text (Replace)", command=self.do_edit_text).pack(pady=10)

        # --- SECURITY & SIZE TAB ---
        ctk.CTkButton(self.tab_security, text="Compress PDF", command=self.do_compress_pdf).pack(pady=10)
        ctk.CTkButton(self.tab_security, text="Unlock PDF", command=self.do_unlock_pdf).pack(pady=10)
        ctk.CTkButton(self.tab_security, text="Add Watermark", command=self.do_add_watermark).pack(pady=10)

    # ================= OPERATION HANDLERS =================

    # --- NEW FEATURES ---
    
    def do_merge_pdfs(self):
        # Open multiple files
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if not files: return
        
        # Convert tuple to list so we can reorder it
        file_list = list(files)
        
        # Ask for output location right away
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file: return

        # Simple reordering mechanism via command line prompts for reliability in Tkinter
        # In a massive app, this would be a separate window with a listbox.
        self.status_label.configure(text="Merging files...", text_color="yellow")
        self.update()
        
        success, msg = pdf_operations.merge_pdfs(file_list, output_file)
        self.update_status(success, msg)

    def do_compress_pdf(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file: return
        
        self.status_label.configure(text="Compressing...", text_color="yellow")
        self.update()
        success, msg = pdf_operations.compress_pdf(input_file, output_file)
        self.update_status(success, msg)

    def do_jpg_to_pdf(self):
        input_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file: return
        
        success, msg = pdf_operations.jpg_to_pdf(input_file, output_file)
        self.update_status(success, msg)

    def do_pdf_to_jpg(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir: return
        
        self.status_label.configure(text="Extracting images...", text_color="yellow")
        self.update()
        success, msg = pdf_operations.pdf_to_jpg(input_file, output_dir)
        self.update_status(success, msg)

    def do_unlock_pdf(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        
        dialog = ctk.CTkInputDialog(text="Enter the PDF Password:", title="Unlock PDF")
        password = dialog.get_input()
        if not password: return

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file: return
        
        success, msg = pdf_operations.unlock_pdf(input_file, output_file, password)
        self.update_status(success, msg)

    # --- EXISTING FEATURES (Ported over) ---
    def do_pdf_to_word(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word", "*.docx")])
        if not output_file: return
        self.status_label.configure(text="Converting...", text_color="yellow")
        self.update()
        success, msg = pdf_operations.pdf_to_word(input_file, output_file)
        self.update_status(success, msg)

    def do_word_to_pdf(self):
        input_file = filedialog.askopenfilename(filetypes=[("Word", "*.docx")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not output_file: return
        self.status_label.configure(text="Converting...", text_color="yellow")
        self.update()
        success, msg = pdf_operations.word_to_pdf(input_file, output_file)
        self.update_status(success, msg)

    def do_split_pdf(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir: return
        dialog = ctk.CTkInputDialog(text="Enter pages per split (e.g., 1):", title="Split")
        pages = dialog.get_input()
        if pages and pages.isdigit():
            success, msg = pdf_operations.split_pdf(input_file, output_dir, int(pages))
            self.update_status(success, msg)

    def do_delete_pages(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not output_file: return
        dialog = ctk.CTkInputDialog(text="Pages to delete (e.g., 1,3,5):", title="Delete")
        pages = dialog.get_input()
        if pages:
            success, msg = pdf_operations.delete_pages(input_file, output_file, pages)
            self.update_status(success, msg)

    def do_add_watermark(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not output_file: return
        dialog = ctk.CTkInputDialog(text="Enter watermark text:", title="Watermark")
        text = dialog.get_input()
        if text:
            success, msg = pdf_operations.add_watermark(input_file, output_file, text)
            self.update_status(success, msg)

    def do_edit_text(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not output_file: return
        dialog_old = ctk.CTkInputDialog(text="Text to replace:", title="Edit")
        old_text = dialog_old.get_input()
        if not old_text: return
        dialog_new = ctk.CTkInputDialog(text="New text:", title="Edit")
        new_text = dialog_new.get_input()
        if new_text is not None:
            success, msg = pdf_operations.simple_edit_text(input_file, output_file, old_text, new_text)
            self.update_status(success, msg)

if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()