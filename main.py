import customtkinter as ctk
from tkinter import filedialog, messagebox
import pdf_operations
import os
import sys

# Prevent missing console crash for docx2pdf
if sys.stdout is None: sys.stdout = open(os.devnull, 'w')
if sys.stderr is None: sys.stderr = open(os.devnull, 'w')

# --- UI THEME SETTINGS ---
ctk.set_appearance_mode("Light")  # Changed to Light mode
ctk.set_default_color_theme("blue") # Blue accents look very clean on white

class PDFToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF Toolkit V2.1")
        self.geometry("600x550") # Made slightly wider for the grid layout
        
        # Configure grid layout for the main window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER SECTION ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.label = ctk.CTkLabel(
            self.header_frame, 
            text="PDF Toolkit", 
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            text_color="#1F2937" # Soft dark gray instead of harsh black
        )
        self.label.pack()

        self.sub_label = ctk.CTkLabel(
            self.header_frame, 
            text="Select a tool below to get started", 
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="#6B7280"
        )
        self.sub_label.pack()

        # --- TABS SECTION ---
        self.tabview = ctk.CTkTabview(self, width=550, height=300, fg_color="#F3F4F6") # Very soft gray background
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.tab_convert = self.tabview.add("🔄 Convert")
        self.tab_modify = self.tabview.add("✏️ Modify")
        self.tab_security = self.tabview.add("🔒 Security & Size")

        self.populate_tabs()

        # --- STATUS BAR (Card Style) ---
        self.status_frame = ctk.CTkFrame(self, fg_color="#E5E7EB", corner_radius=10)
        self.status_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Ready", 
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color="#059669" # Emerald green
        )
        self.status_label.pack(pady=10)

    def update_status(self, success, message):
        color = "#059669" if success else "#DC2626" # Emerald green or Crimson red
        self.status_label.configure(text=message, text_color=color)

    def create_grid_button(self, parent, text, row, col, command):
        """Helper function to create uniform dashboard buttons"""
        btn = ctk.CTkButton(
            parent, 
            text=text, 
            command=command,
            font=ctk.CTkFont(size=14),
            height=45, # Taller, more clickable buttons
            corner_radius=8,
            fg_color="#FFFFFF", # White buttons
            text_color="#1F2937", # Dark text
            border_width=1,
            border_color="#D1D5DB",
            hover_color="#E0E7FF" # Soft blue hover effect
        )
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        return btn

    def populate_tabs(self):
        # Configure columns inside tabs to be equal width
        for tab in [self.tab_convert, self.tab_modify, self.tab_security]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_columnconfigure(1, weight=1)

        # --- CONVERT TAB (2-Column Grid) ---
        self.create_grid_button(self.tab_convert, "📄 PDF to Word", 0, 0, self.do_pdf_to_word)
        self.create_grid_button(self.tab_convert, "📝 Word to PDF", 0, 1, self.do_word_to_pdf)
        self.create_grid_button(self.tab_convert, "🖼️ JPG to PDF", 1, 0, self.do_jpg_to_pdf)
        self.create_grid_button(self.tab_convert, "📸 PDF to JPG", 1, 1, self.do_pdf_to_jpg)

        # --- MODIFY TAB (2-Column Grid) ---
        self.create_grid_button(self.tab_modify, "➕ Merge PDFs", 0, 0, self.do_merge_pdfs)
        self.create_grid_button(self.tab_modify, "✂️ Split PDF", 0, 1, self.do_split_pdf)
        self.create_grid_button(self.tab_modify, "🗑️ Delete Pages", 1, 0, self.do_delete_pages)
        self.create_grid_button(self.tab_modify, "🔤 Edit Text", 1, 1, self.do_edit_text)

        # --- SECURITY & SIZE TAB (2-Column Grid) ---
        self.create_grid_button(self.tab_security, "🗜️ Compress PDF", 0, 0, self.do_compress_pdf)
        self.create_grid_button(self.tab_security, "🔓 Unlock PDF", 0, 1, self.do_unlock_pdf)
        self.create_grid_button(self.tab_security, "©️ Add Watermark", 1, 0, self.do_add_watermark)

    # ================= OPERATION HANDLERS =================
    # (These remain exactly the same as before, they just call the logic and update the UI)
    
    def do_merge_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if not files: return
        file_list = list(files)
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file: return
        self.status_label.configure(text="Merging files...", text_color="#D97706") # Amber loading color
        self.update()
        success, msg = pdf_operations.merge_pdfs(file_list, output_file)
        self.update_status(success, msg)

    def do_compress_pdf(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file: return
        self.status_label.configure(text="Compressing...", text_color="#D97706")
        self.update()
        success, msg = pdf_operations.compress_pdf(input_file, output_file)
        self.update_status(success, msg)

    def do_jpg_to_pdf(self):
        input_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file: return
        self.status_label.configure(text="Converting...", text_color="#D97706")
        self.update()
        success, msg = pdf_operations.jpg_to_pdf(input_file, output_file)
        self.update_status(success, msg)

    def do_pdf_to_jpg(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir: return
        self.status_label.configure(text="Extracting images...", text_color="#D97706")
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
        self.status_label.configure(text="Unlocking...", text_color="#D97706")
        self.update()
        success, msg = pdf_operations.unlock_pdf(input_file, output_file, password)
        self.update_status(success, msg)

    def do_pdf_to_word(self):
        input_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word", "*.docx")])
        if not output_file: return
        self.status_label.configure(text="Converting...", text_color="#D97706")
        self.update()
        success, msg = pdf_operations.pdf_to_word(input_file, output_file)
        self.update_status(success, msg)

    def do_word_to_pdf(self):
        input_file = filedialog.askopenfilename(filetypes=[("Word", "*.docx")])
        if not input_file: return
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not output_file: return
        self.status_label.configure(text="Converting...", text_color="#D97706")
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
            self.status_label.configure(text="Splitting...", text_color="#D97706")
            self.update()
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
            self.status_label.configure(text="Deleting...", text_color="#D97706")
            self.update()
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
            self.status_label.configure(text="Watermarking...", text_color="#D97706")
            self.update()
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
            self.status_label.configure(text="Editing...", text_color="#D97706")
            self.update()
            success, msg = pdf_operations.simple_edit_text(input_file, output_file, old_text, new_text)
            self.update_status(success, msg)

if __name__ == "__main__":
    app = PDFToolApp()
    app.mainloop()