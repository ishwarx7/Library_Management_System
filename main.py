import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date

# --- Database Initialization (No Changes) ---
def init_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    # Book Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                quantity INTEGER NOT NULL
                )
    """)
    # student table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL UNIQUE
                )
    """)
    # issue table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issued_books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                foreign key(book_id) REFERENCES books(id),
                foreign key(student_id) REFERENCES students(id)
                )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# --- Main Application Class (Single-Page Architecture) ---
class LibraryApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Library Management System")
        self.geometry("900x650") # Start with a larger default size
        self.minsize(700, 500)   # Set a minimum size
        
        # --- Apply modern theme and custom styles ---
        self.setup_styles()
        
        # --- Main container to hold all "pages" ---
        # This container fills the whole window and lets pages expand into it
        container = ttk.Frame(self, padding=0)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {} # Dictionary to store all page frames
        
        # Create and store each page frame
        for F in (MainMenuFrame, AddBookFrame, ViewBooksFrame, IssueBookFrame, ReturnBookFrame, ViewIssuedBooksFrame):
            frame = F(container, self)
            self.frames[F] = frame
            # All frames sit in the same spot; tkraise() brings one to the front
            frame.grid(row=0, column=0, sticky="nsew") 
            
        self.show_frame(MainMenuFrame) # Show the main menu first
        
    def show_frame(self, frame_class):
        """Brings the requested frame to the front"""
        frame = self.frames[frame_class]
        # Call refresh method if it exists, to update data when page is shown
        if hasattr(frame, 'refresh'):
            frame.refresh()
        frame.tkraise()
        
    def setup_styles(self):
        """Configure styles for a modern look"""
        style = ttk.Style()
        style.theme_use('clam') # Use a more modern-looking theme

        # --- Color Palette ---
        BG_PRIMARY = "#2c3e50"   # Dark Slate Blue (for main menu)
        BG_CONTENT = "#ecf0f1"   # Light Gray (for content pages)
        TEXT_LIGHT = "#FFFFFF"   # White
        TEXT_DARK = "#34495e"    # Dark Gray
        TEXT_HEADER = "#3498db"  # Bright Blue (for headers)
        BTN_PRIMARY = "#3498db"  # Blue
        BTN_SUCCESS = "#2ecc71"  # Green
        BTN_DANGER = "#e74c3c"   # Red
        BTN_BACK = "#bdc3c7"     # Silver
        BTN_BACK_FG = "#2c3e50"  # Dark text for back button

        # --- Configure Styles ---
        style.configure('.', 
                        background=BG_CONTENT, 
                        foreground=TEXT_DARK, 
                        font=('Inter', 11))
        
        style.configure('TFrame', background=BG_CONTENT)
        style.configure('Content.TFrame', background=BG_CONTENT, relief='flat')
        style.configure('Dark.TFrame', background=BG_PRIMARY) # For Main Menu

        style.configure('TLabel', background=BG_CONTENT, padding=5)
        style.configure('Dark.TLabel', background=BG_PRIMARY, foreground=TEXT_LIGHT, padding=5)
        
        style.configure('Header.TLabel', 
                        font=('Inter', 26, 'bold'), 
                        foreground=TEXT_HEADER, 
                        background=BG_CONTENT, 
                        padding=(10, 20, 10, 10))
                        
        style.configure('DarkHeader.TLabel', 
                        font=('Inter', 32, 'bold'), 
                        foreground=TEXT_LIGHT, 
                        background=BG_PRIMARY, 
                        padding=(10, 30))

        style.configure('TButton', 
                        font=('Inter', 12, 'bold'), 
                        padding=(15, 12), 
                        width=25,
                        background=BTN_PRIMARY, 
                        foreground=TEXT_LIGHT)
        style.map('TButton', 
                  background=[('active', '#2980b9')]) # Darker blue on hover/click

        style.configure('Success.TButton', 
                        background=BTN_SUCCESS, 
                        foreground=TEXT_LIGHT)
        style.map('Success.TButton', 
                  background=[('active', '#27ae60')])

        style.configure('Danger.TButton', 
                        background=BTN_DANGER, 
                        foreground=TEXT_LIGHT)
        style.map('Danger.TButton', 
                  background=[('active', '#c0392b')])
        
        style.configure('Back.TButton', 
                        background=BTN_BACK, 
                        foreground=BTN_BACK_FG, 
                        width=15)
        style.map('Back.TButton', 
                  background=[('active', '#aab1b5')])
        
        style.configure('TEntry', 
                        fieldbackground='white', 
                        font=('Inter', 12), 
                        padding=8)
        
        style.configure('Treeview.Heading', 
                        font=('Inter', 13, 'bold'), 
                        padding=10)
        style.configure('Treeview', 
                        font=('Inter', 11), 
                        rowheight=30, 
                        fieldbackground='white')
        style.map('Treeview', 
                  background=[('selected', BTN_PRIMARY)]) # Selected row color


# --- Page 1: Main Menu (Responsive & Centered) ---
class MainMenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Dark.TFrame') # Use dark background
        self.controller = controller
        
        # --- Responsive Grid Layout ---
        # Configure rows/columns to center the content
        self.grid_rowconfigure(0, weight=2) # Empty space above
        self.grid_rowconfigure(1, weight=1) # Title
        self.grid_rowconfigure(2, weight=2) # Button Frame
        self.grid_rowconfigure(3, weight=1) # Exit Button
        self.grid_rowconfigure(4, weight=2) # Empty space below
        
        self.grid_columnconfigure(0, weight=1) # Empty space left
        self.grid_columnconfigure(1, weight=0) # Content
        self.grid_columnconfigure(2, weight=1) # Empty space right
        
        ttk.Label(self, text="Library Management System", 
                  style='DarkHeader.TLabel').grid(row=1, column=1, pady=20)
        
        btn_frame = ttk.Frame(self, style='Dark.TFrame')
        btn_frame.grid(row=2, column=1)
        
        buttons = [
            ("View & Manage Books", ViewBooksFrame),
            ("Add New Book", AddBookFrame),
            ("Issue a Book", IssueBookFrame),
            ("Return a Book", ReturnBookFrame),
            ("View Full Issue History", ViewIssuedBooksFrame)
        ]
        
        for i, (text, frame_class) in enumerate(buttons):
            ttk.Button(btn_frame, text=text, 
                       command=lambda fc=frame_class: controller.show_frame(fc)
                       ).pack(fill='x', pady=12)
            
        ttk.Button(self, text="Exit Application", 
                   style='Danger.TButton', 
                   width=25,
                   command=controller.destroy).grid(row=3, column=1, pady=40)


# --- Base Page for Content (Forms, Tables) ---
# We create a base class to standardize the "Back" button and header
class ContentFrame(ttk.Frame):
    def __init__(self, parent, controller, title):
        super().__init__(parent, style='Content.TFrame')
        self.controller = controller
        
        # --- Responsive Grid Layout ---
        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=1) # Main Content (will expand)
        self.grid_rowconfigure(2, weight=0) # Back Button
        
        self.grid_columnconfigure(0, weight=1) # Main Content (will expand)
        
        # --- Header ---
        header_frame = ttk.Frame(self, style='Content.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        
        ttk.Label(header_frame, text=title, 
                  style='Header.TLabel').pack(side='left')
        
        ttk.Button(header_frame, text="Back to Menu", 
                   style='Back.TButton',
                   command=lambda: controller.show_frame(MainMenuFrame)
                   ).pack(side='right', anchor='n', pady=10)

        # --- Main Content Area ---
        # Child classes will create and place self.main_content_frame
        self.main_content_frame = ttk.Frame(self, style='Content.TFrame')
        self.main_content_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

# --- Page 2: Add New Book (Responsive Form) ---
class AddBookFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Add New Book")
        
        # --- Responsive Grid for the content area ---
        # This will center the form
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(1, weight=1) # Form
        self.main_content_frame.grid_columnconfigure(2, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=1) # Center vertically
        self.main_content_frame.grid_rowconfigure(1, weight=2)
        
        form_frame = ttk.Frame(self.main_content_frame)
        form_frame.grid(row=0, column=1, sticky='nsew')
        
        # Configure form grid to be responsive
        form_frame.grid_columnconfigure(1, weight=1) # Entry column expands
        
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky='w', padx=10, pady=8)
        self.title_entry = ttk.Entry(form_frame, width=45)
        self.title_entry.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        
        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky='w', padx=10, pady=8)
        self.author_entry = ttk.Entry(form_frame)
        self.author_entry.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        
        ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, sticky='w', padx=10, pady=8)
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=8, sticky='ew')
        
        ttk.Button(form_frame, text="Save Book", style='Success.TButton', 
                   command=self.save_book).grid(row=3, column=1, sticky='e', padx=10, pady=20)

    def save_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        qty = self.quantity_entry.get().strip()

        if not title or not author or not qty:
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        
        try:
            qty = int(qty)
            if qty < 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be a positive number.")
            return

        try:
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)", (title, author, qty))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book added successfully!")
            self.refresh() # Clear fields
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def refresh(self):
        """Clear all entry fields"""
        self.title_entry.delete(0, 'end')
        self.author_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.title_entry.focus()


# --- Page 3: View All Books (Responsive Table) ---
class ViewBooksFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "View & Manage Books")
        
        # --- Responsive Grid for the content area ---
        self.main_content_frame.grid_rowconfigure(0, weight=0) # Search
        self.main_content_frame.grid_rowconfigure(1, weight=1) # Treeview
        self.main_content_frame.grid_rowconfigure(2, weight=0) # Actions
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        
        # --- Search Bar ---
        search_frame = ttk.Frame(self.main_content_frame)
        search_frame.grid(row=0, column=0, sticky='ew', pady=10)
        search_frame.grid_columnconfigure(1, weight=1) # Make entry expand
        
        ttk.Label(search_frame, text="Search by Title:").grid(row=0, column=0, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, sticky='ew', padx=5)
        ttk.Button(search_frame, text="Search", width=10,
                   command=self.search_action).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Refresh", style='Back.TButton', width=10,
                   command=self.refresh).grid(row=0, column=3, padx=5)

        # --- Treeview Table ---
        tree_frame = ttk.Frame(self.main_content_frame)
        tree_frame.grid(row=1, column=0, sticky='nsew')
        # Make Treeview responsive
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        columns = ("ID", "Title", "Author", "Quantity")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=60, stretch=tk.NO, anchor='center')
        self.tree.heading("Title", text="Title")
        self.tree.column("Title", width=300)
        self.tree.heading("Author", text="Author")
        self.tree.column("Author", width=200)
        self.tree.heading("Quantity", text="Quantity")
        self.tree.column("Quantity", width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.grid(row=0, column=0, sticky='nsew')

        # --- Action Buttons ---
        action_frame = ttk.Frame(self.main_content_frame)
        action_frame.grid(row=2, column=0, sticky='ew', pady=10)
        
        ttk.Button(action_frame, text="Update Selected", width=18, 
                   command=self.open_update_window).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Delete Selected", style='Danger.TButton', width=18, 
                   command=self.delete_selected).pack(side='left', padx=5)

        self.refresh() # Load data on init

    def load_books(self, filter_text=""):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()
            if filter_text:
                cur.execute("SELECT * FROM books WHERE title LIKE ? ORDER BY title", (f"%{filter_text}%",))
            else:
                cur.execute("SELECT * FROM books ORDER BY title")
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def search_action(self):
        query = self.search_entry.get().strip()
        self.load_books(query)

    def refresh(self):
        self.search_entry.delete(0, 'end')
        self.load_books()
        
    def delete_selected(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a book to delete.")
            return
        book_data = self.tree.item(selected_item, 'values')
        book_id, book_title = book_data[0], book_data[1]
        
        confirm = messagebox.askyesno("Confirm Delete", 
            f"Are you sure you want to delete '{book_title}' (ID: {book_id})?")
        
        if confirm:
            try:
                conn = sqlite3.connect("library.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM issued_books WHERE book_id = ? AND return_date IS NULL", (book_id,))
                if cur.fetchone():
                    messagebox.showerror("Error", "Cannot delete book. It is currently issued.")
                else:
                    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
                    conn.commit()
                    messagebox.showinfo("Deleted", "Book deleted successfully.")
                    self.refresh()
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                conn.close()

    def open_update_window(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a book to update.")
            return
        book_data = self.tree.item(selected_item, 'values')
        book_id, title, author, qty = book_data

        self.upd_win = tk.Toplevel(self.controller)
        self.upd_win.title("Update Book")
        self.upd_win.geometry("450x350")
        self.upd_win.config(bg=BG_CONTENT)
        self.upd_win.transient(self.controller)
        self.upd_win.grab_set()
        
        form_frame = ttk.Frame(self.upd_win, padding=20)
        form_frame.pack(expand=True, fill='both')
        form_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky='w', padx=10, pady=8)
        self.title_entry_upd = ttk.Entry(form_frame, width=40)
        self.title_entry_upd.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        self.title_entry_upd.insert(0, title)
        
        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky='w', padx=10, pady=8)
        self.author_entry_upd = ttk.Entry(form_frame)
        self.author_entry_upd.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        self.author_entry_upd.insert(0, author)
        
        ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, sticky='w', padx=10, pady=8)
        self.qty_entry_upd = ttk.Entry(form_frame)
        self.qty_entry_upd.grid(row=2, column=1, padx=10, pady=8, sticky='ew')
        self.qty_entry_upd.insert(0, qty)
        
        save_btn = ttk.Button(form_frame, text="Save Changes", style='Success.TButton', width=15,
            command=lambda: self.save_update(book_id))
        save_btn.grid(row=3, column=1, sticky='e', pady=20, padx=10)

    def save_update(self, book_id):
        title = self.title_entry_upd.get().strip()
        author = self.author_entry_upd.get().strip()
        qty = self.qty_entry_upd.get().strip()

        if not title or not author or not qty:
            messagebox.showwarning("Input Error", "All fields are required!", parent=self.upd_win)
            return
        try:
            qty = int(qty)
            if qty < 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be a positive number.", parent=self.upd_win)
            return
        try:
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()
            cur.execute("UPDATE books SET title = ?, author = ?, quantity = ? WHERE id = ?",
                        (title, author, qty, book_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book updated successfully.")
            self.upd_win.destroy()
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=self.upd_win)

# --- Page 4: Issue a Book (Responsive Form) ---
class IssueBookFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Issue a Book")
        
        # --- Responsive Grid for the content area ---
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(1, weight=1) # Form
        self.main_content_frame.grid_columnconfigure(2, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=1) # Center vertically
        self.main_content_frame.grid_rowconfigure(1, weight=2)
        
        form_frame = ttk.Frame(self.main_content_frame)
        form_frame.grid(row=0, column=1, sticky='nsew')
        
        # Configure form grid to be responsive
        form_frame.grid_columnconfigure(1, weight=1) # Entry column expands
        
        ttk.Label(form_frame, text="Book ID:").grid(row=0, column=0, sticky='w', padx=10, pady=8)
        self.book_id_entry = ttk.Entry(form_frame, width=45)
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        
        ttk.Label(form_frame, text="Student Roll No:").grid(row=1, column=0, sticky='w', padx=10, pady=8)
        self.roll_entry = ttk.Entry(form_frame)
        self.roll_entry.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        
        ttk.Label(form_frame, text="Student Name:").grid(row=2, column=0, sticky='w', padx=10, pady=8)
        self.sname_entry = ttk.Entry(form_frame)
        self.sname_entry.grid(row=2, column=1, padx=10, pady=8, sticky='ew')
        ttk.Label(form_frame, text="(Required if new student)").grid(row=3, column=1, sticky='w', padx=10)

        ttk.Button(form_frame, text="Issue Book", style='Success.TButton', 
                   command=self.issue_book).grid(row=4, column=1, sticky='e', padx=10, pady=20)

    def issue_book(self):
        book_id = self.book_id_entry.get().strip()
        sroll = self.roll_entry.get().strip()
        sname = self.sname_entry.get().strip()

        if not book_id or not sroll:
            messagebox.showwarning("Input Error", "Book ID and Student Roll No are required!")
            return

        try:
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()

            # 1. Check book availability
            cur.execute("SELECT quantity FROM books WHERE id = ?", (book_id,))
            book = cur.fetchone()
            if not book:
                messagebox.showwarning("Error", "Book ID not found.")
                conn.close(); return
            if book[0] <= 0:
                messagebox.showwarning("Unavailable", "No copies of this book are left to issue.")
                conn.close(); return

            # 2. Find or create student
            cur.execute("SELECT id, name FROM students WHERE roll_no = ?", (sroll,))
            student = cur.fetchone()
            if not student:
                if not sname:
                    messagebox.showwarning("Input Error", "Student Name is required for new students.")
                    conn.close(); return
                cur.execute("INSERT INTO students (name, roll_no) VALUES (?, ?)", (sname, sroll))
                conn.commit()
                student_id, student_name = cur.lastrowid, sname
            else:
                student_id, student_name = student[0], student[1]

            # 3. Check if student already has this book
            cur.execute("SELECT * FROM issued_books WHERE book_id = ? AND student_id = ? AND return_date IS NULL", 
                        (book_id, student_id))
            if cur.fetchone():
                messagebox.showwarning("Already Issued", f"{student_name} already has a copy of this book.")
                conn.close(); return

            # 4. Record issue
            cur.execute("INSERT INTO issued_books (book_id, student_id, issue_date) VALUES (?, ?, ?)",
                        (book_id, student_id, str(date.today())))
            
            # 5. Decrement book quantity
            cur.execute("UPDATE books SET quantity = quantity - 1 WHERE id = ?", (book_id,))
            
            conn.commit()
            messagebox.showinfo("Issued", f"Book ID {book_id} issued to {student_name} (Roll: {sroll})!")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn: conn.close()

    def refresh(self):
        self.book_id_entry.delete(0, 'end')
        self.roll_entry.delete(0, 'end')
        self.sname_entry.delete(0, 'end')
        self.book_id_entry.focus()


# --- Page 5: Return a Book (Responsive Table) ---
class ReturnBookFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Return a Book")
        
        # --- Responsive Grid for the content area ---
        self.main_content_frame.grid_rowconfigure(0, weight=0) # Note
        self.main_content_frame.grid_rowconfigure(1, weight=1) # Treeview
        self.main_content_frame.grid_rowconfigure(2, weight=0) # Actions
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(self.main_content_frame, 
                  text="Select a book from the list below (only currently issued books are shown).").grid(
                      row=0, column=0, sticky='w', pady=(0, 10))

        # --- Treeview Table ---
        tree_frame = ttk.Frame(self.main_content_frame)
        tree_frame.grid(row=1, column=0, sticky='nsew')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        columns = ("Issue ID", "Book Title", "Student Name", "Roll No", "Issue Date", "Book ID")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("Issue ID", text="Issue ID")
        self.tree.column("Issue ID", width=70, stretch=tk.NO, anchor='center')
        self.tree.heading("Book Title", text="Book Title")
        self.tree.column("Book Title", width=250)
        self.tree.heading("Student Name", text="Student Name")
        self.tree.column("Student Name", width=150)
        self.tree.heading("Roll No", text="Roll No")
        self.tree.column("Roll No", width=100)
        self.tree.heading("Issue Date", text="Issue Date")
        self.tree.column("Issue Date", width=110, anchor='center')
        self.tree.column("Book ID", width=0, stretch=tk.NO) # Hide Book ID
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.grid(row=0, column=0, sticky='nsew')

        # --- Action Buttons ---
        action_frame = ttk.Frame(self.main_content_frame)
        action_frame.grid(row=2, column=0, sticky='ew', pady=10)
        
        ttk.Button(action_frame, text="Return Selected Book", style='Success.TButton', 
                   width=22, command=self.return_book).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Refresh List", style='Back.TButton', width=15, 
                   command=self.refresh).pack(side='left', padx=5)

    def load_issued_books(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()
            query = """
                SELECT i.id, b.title, s.name, s.roll_no, i.issue_date, i.book_id
                FROM issued_books i
                JOIN books b ON i.book_id = b.id
                JOIN students s ON i.student_id = s.id
                WHERE i.return_date IS NULL
                ORDER BY i.issue_date
            """
            cur.execute(query)
            for row in cur.fetchall():
                self.tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def refresh(self):
        self.load_issued_books()

    def return_book(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an issued book to return.")
            return
            
        data = self.tree.item(selected_item, 'values')
        issue_id, book_title, student_name, book_id = data[0], data[1], data[2], data[5]
        
        confirm = messagebox.askyesno("Confirm Return", 
            f"Return '{book_title}' from {student_name}?")
        
        if confirm:
            try:
                conn = sqlite3.connect("library.db")
                cur = conn.cursor()
                cur.execute("UPDATE issued_books SET return_date = ? WHERE id = ?", 
                            (str(date.today()), issue_id))
                cur.execute("UPDATE books SET quantity = quantity + 1 WHERE id = ?", (book_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book returned successfully.")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                conn.close()


# --- Page 6: View Full Issue History (Responsive Table) ---
class ViewIssuedBooksFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Full Issue History")
        
        # --- Responsive Grid for the content area ---
        self.main_content_frame.grid_rowconfigure(0, weight=1) # Treeview
        self.main_content_frame.grid_rowconfigure(1, weight=0) # Actions
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # --- Treeview Table ---
        tree_frame = ttk.Frame(self.main_content_frame)
        tree_frame.grid(row=0, column=0, sticky='nsew', pady=(10,0))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        columns = ("ID", "Book Title", "Student", "Roll No", "Issued", "Returned")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, stretch=tk.NO, anchor='center')
        self.tree.heading("Book Title", text="Book Title")
        self.tree.column("Book Title", width=250)
        self.tree.heading("Student", text="Student")
        self.tree.column("Student", width=150)
        self.tree.heading("Roll No", text="Roll No")
        self.tree.column("Roll No", width=100)
        self.tree.heading("Issued", text="Issue Date")
        self.tree.column("Issued", width=110, anchor='center')
        self.tree.heading("Returned", text="Return Date")
        self.tree.column("Returned", width=110, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.grid(row=0, column=0, sticky='nsew')

        # --- Action Buttons ---
        action_frame = ttk.Frame(self.main_content_frame)
        action_frame.grid(row=1, column=0, sticky='ew', pady=10)
        
        ttk.Button(action_frame, text="Refresh List", style='Back.TButton', width=15, 
                   command=self.refresh).pack(side='left', padx=5)

    def load_all_issued(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            conn = sqlite3.connect("library.db")
            cur = conn.cursor()
            query = """
                SELECT i.id, b.title, s.name, s.roll_no, i.issue_date, i.return_date
                FROM issued_books i
                JOIN books b ON i.book_id = b.id
                JOIN students s ON i.student_id = s.id
                ORDER BY i.issue_date DESC
            """
            cur.execute(query)
            for row in cur.fetchall():
                display_row = list(row)
                if display_row[5] is None:
                    display_row[5] = "--- Not Returned ---"
                self.tree.insert("", "end", values=display_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def refresh(self):
        self.load_all_issued()


# --- Run the Application ---
if __name__ == "__main__":
    init_db()       # Setup the database first
    app = LibraryApp()
    app.mainloop()