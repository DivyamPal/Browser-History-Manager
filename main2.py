import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Page:
    def __init__(self, url):
        self.url = url
        self.next = None
        self.prev = None

class HistoryManager:
    def __init__(self):
        self.current = None
        self.head = None
        self.tail = None

    def visit_page(self, url):
        new_page = Page(url)
        if not self.head:
            self.head = self.tail = new_page
        else:
            if self.current and self.current.next:
                self.current.next = None
            self.current.next = new_page
            new_page.prev = self.current
            self.tail = new_page
        self.current = new_page

    def go_back(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        else:
            messagebox.showinfo("Info", "No previous page in history.")

    def go_forward(self):
        if self.current and self.current.next:
            self.current = self.current.next
        else:
            messagebox.showinfo("Info", "No forward page in history.")

    def view_history(self):
        history = []
        node = self.head
        while node:
            if node == self.current:
                history.append(f"> {node.url} < (Current Page)")
            else:
                history.append(node.url)
            node = node.next
        return history

    def clear_history(self):
        self.head = self.tail = self.current = None

class BrowserHistoryApp:
    def __init__(self, root):
        self.root = root
        self.history_manager = HistoryManager()
        self.root.title("Browser History Manager")
        self.root.geometry("500x400")
        self.root.configure(bg="#f3f4f6")

        # Header Frame
        header_frame = tk.Frame(root, bg="#3b82f6")
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Browser History Manager", bg="#3b82f6", fg="white", font=("Helvetica", 16, "bold"))
        header_label.pack(pady=10)

        # URL Entry Frame
        entry_frame = tk.Frame(root, bg="#f3f4f6")
        entry_frame.pack(pady=10)

        self.url_label = tk.Label(entry_frame, text="Enter URL:", bg="#f3f4f6", font=("Helvetica", 12))
        self.url_label.grid(row=0, column=0, padx=5, pady=5)

        self.url_entry = tk.Entry(entry_frame, width=40, font=("Helvetica", 12))
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        self.visit_button = ttk.Button(entry_frame, text="Visit Page", command=self.visit_page)
        self.visit_button.grid(row=0, column=2, padx=5, pady=5)

        # Control Buttons Frame
        button_frame = tk.Frame(root, bg="#f3f4f6")
        button_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", padding=6, font=("Helvetica", 10, "bold"))

        self.back_button = ttk.Button(button_frame, text="Back", command=self.go_back, style="TButton")
        self.back_button.grid(row=0, column=0, padx=5)

        self.forward_button = ttk.Button(button_frame, text="Forward", command=self.go_forward, style="TButton")
        self.forward_button.grid(row=0, column=1, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear History", command=self.clear_history, style="TButton")
        self.clear_button.grid(row=0, column=2, padx=5)

        # History Display Frame
        self.history_label = tk.Label(root, text="History:", bg="#f3f4f6", font=("Helvetica", 12, "bold"))
        self.history_label.pack(pady=5)

        self.history_text = tk.Text(root, width=50, height=12, font=("Helvetica", 10), state=tk.DISABLED, bg="#e5e7eb")
        self.history_text.pack(pady=5)

    def visit_page(self):
        url = self.url_entry.get().strip()
        if url:
            self.history_manager.visit_page(url)
            self.url_entry.delete(0, tk.END)
            self.update_history()
        else:
            messagebox.showerror("Error", "Please enter a valid URL.")

    def go_back(self):
        self.history_manager.go_back()
        self.update_history()

    def go_forward(self):
        self.history_manager.go_forward()
        self.update_history()

    def clear_history(self):
        self.history_manager.clear_history()
        self.update_history()

    def update_history(self):
        history = self.history_manager.view_history()
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for url in history:
            self.history_text.insert(tk.END, url + "\n")
        self.history_text.config(state=tk.DISABLED)

# Run the application
root = tk.Tk()
app = BrowserHistoryApp(root)
root.mainloop()
