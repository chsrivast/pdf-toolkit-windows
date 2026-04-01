import customtkinter as ctk
from tkinter import filedialog, messagebox
import pdf_operations
import os

# Set UI Theme
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")

class PDFToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF Toolkit")
        self.geometry("500x600")

        # Title Label
        self.label = ctk.CTkLabel(self, text="PDF Toolkit", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="green")
        self.status_label.pack(pady=5)

        # Buttons for operations
        self.create_buttons()

    def update_status(self, success, message):
        color = "green" if success else "red"
        self.status_label.configure(text=message, text_color=color)

    def select_file(self, filetypes=[("PDF Files", "*.pdf")]):
        return filedialog.askopenfilename(filetypes=filetypes)
        
    def save_file(self, defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]):
        return filedialog.asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes)

    def create_buttons(self):
        # 1. PDF to Word
        btn_pdf2word = ctk.CTkButton(self, text="Convert PDF to Word", command=self.do_pdf_to_word)
        btn_pdf2word.pack(pady=10)

        # 2. Word to PDF
        btn_word2pdf = ctk.CTkButton(self, text="Convert Word to PDF", command=self.do_word_to_pdf)
        btn_word2pdf.pack(pady=10)

        # 3. Split PDF
        btn_split = ctk.CTkButton(self, text="Split PDF", command=self.do_split_pdf)
        btn_split.pack(pady=10)

        # 4. Delete Pages
        btn_delete = ctk.CTkButton(self, text="Delete Pages", command=self.do_delete_pages)
        btn_delete.pack(pady=10)
        
        # 5. Add Watermark
        btn_watermark = ctk.CTkButton(self, text="Add Watermark", command=self.do_add_watermark)
        btn_watermark.pack(pady=10)

        # 6. Edit Content
        btn_edit = ctk.CTkButton(self, text="Edit Text (Replace)", command=self.do_edit_text)
        btn_edit.pack(pady=10)

    # --- Operation Handlers ---
    
    def do_pdf_to_word(self):
        input_file = self.select_file()
        if not input_file: return
        output_file = self.save_file(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")])
        if not output_file: return
        
        self.status_label.configure(text="Converting...", text_color="yellow")
        self.update() # Force UI update
        success, msg = pdf_operations.pdf_to_word(input_file, output_file)
        self.update_status(success, msg)

    def do_word_to_pdf(self):
        input_file = self.select_file(filetypes=[("Word Documents", "*.docx")])
        if not input_file: return
        output_file = self.save_file()
        if not output_file: return
        
        self.status_label.configure(text="Converting...", text_color="yellow")
        self.update()
        success, msg = pdf_operations.word_to_pdf(input_file, output_file)
        self.update_status(success, msg)

    def do_split_pdf(self):
        input_file = self.select_file()
        if not input_file: return
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir: return
        
        dialog = ctk.CTkInputDialog(text="Enter pages per split (e.g., 1):", title="Split PDF")
        pages = dialog.get_input()
        if pages and pages.isdigit():
            success, msg = pdf_operations.split_pdf(input_file, output_dir, int(pages))
            self.update_status(success, msg)

    def do_delete_pages(self):
        input_file = self.select_file()
        if not input_file: return
        output_file = self.save_file()
        if not output_file: return
        
        dialog = ctk.CTkInputDialog(text="Enter page numbers to delete (comma-separated, e.g., 1,3,5):", title="Delete Pages")
        pages = dialog.get_input()
        if pages:
            success, msg = pdf_operations.delete_pages(input_file, output_file, pages)
            self.update_status(success, msg)

    def do_add_watermark(self):
        input_file = self.select_file()
        if not input_file: return
        output_file = self.save_file()
        if not output_file: return
        
        dialog = ctk.CTkInputDialog(text="Enter watermark text:", title="Watermark")
        text = dialog.get_input()
        if text:
            success, msg = pdf_operations.add_watermark(input_file, output_file, text)
            self.update_status(success, msg)

    def do_edit_text(self):
        input_file = self.select_file()
        if not input_file: return
        output_file = self.save_file()
        if not output_file: return
        
        dialog_old = ctk.CTkInputDialog(text="Enter text to replace:", title="Edit Text")
        old_text = dialog_old.get_input()
        if not old_text: return
        
        dialog_new = ctk.CTkInputDialog(text="Enter new text:", title="Edit Text")
        new_text = dialog_new.get_input()
        
        if new_text is not None:
            success, msg = pdf_operations.simple_edit_text(input_file, output_file, old_text, new_text)
            self.update_status(success, msg)

if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()