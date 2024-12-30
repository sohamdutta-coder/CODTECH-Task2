import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ModernInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#FFFFFF")
        self.user_role = None
        self.init_login()

    def init_login(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="#FFFFFF", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Helvetica", 24, "bold"), bg="#FFFFFF", fg="#000000").pack(pady=20)

        tk.Label(frame, text="Username", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333").pack(anchor=tk.W)
        self.username_entry = tk.Entry(frame, width=30, font=("Helvetica", 12), bg="#F0F0F0", bd=1, relief="flat")
        self.username_entry.pack(pady=5)

        tk.Label(frame, text="Password", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333").pack(anchor=tk.W)
        self.password_entry = tk.Entry(frame, show="*", width=30, font=("Helvetica", 12), bg="#F0F0F0", bd=1, relief="flat")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(
            frame, text="Login", command=self.login, bg="#000000", fg="#FFFFFF",
            font=("Helvetica", 12, "bold"), padx=20, pady=5, relief="flat", cursor="hand2"
        )
        login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM users WHERE username = ? AND password = ?', (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            self.user_role = result[0]
            self.init_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def init_dashboard(self):
        self.clear_frame()
        tk.Label(
            self.root, text="Dashboard", font=("Helvetica", 24, "bold"),
            bg="#FFFFFF", fg="#000000"
        ).pack(pady=20)

        button_frame = tk.Frame(self.root, bg="#FFFFFF")
        button_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.create_flat_button(button_frame, "Manage Products", self.manage_products)
        self.create_flat_button(button_frame, "Sales Summary", self.sales_summary)
        self.create_flat_button(button_frame, "Check Low Stock", self.check_low_stock)
        self.create_flat_button(button_frame, "Logout", self.init_login)

    def create_flat_button(self, parent, text, command):
        button = tk.Button(
            parent, text=text, command=command, bg="#FFFFFF", fg="#000000",
            font=("Helvetica", 14), padx=10, pady=10, relief="flat", cursor="hand2",
            activebackground="#F0F0F0", activeforeground="#000000", width=20
        )
        button.pack(pady=10)

    def manage_products(self):
        self.clear_frame()
        tk.Label(self.root, text="Manage Products", font=("Helvetica", 24, "bold"), bg="#FFFFFF", fg="#000000").pack(pady=20)

        table_frame = tk.Frame(self.root, bg="#FFFFFF")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Category", "Price", "Stock")
        self.product_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.product_table.heading(col, text=col)
            self.product_table.column(col, width=120)

        self.product_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.product_table.yview)
        self.product_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        button_bar = tk.Frame(self.root, bg="#FFFFFF")
        button_bar.pack(fill=tk.X, padx=20, pady=10)

        self.create_flat_button(button_bar, "Add Product", self.add_product)
        self.create_flat_button(button_bar, "Back", self.init_dashboard)

        self.load_products()

    def add_product(self):
        def save_product():
            name = name_entry.get().strip()
            category = category_entry.get().strip()
            try:
                price = float(price_entry.get())
                stock = int(stock_entry.get())
                if not name or not category:
                    raise ValueError("Name and category cannot be empty.")
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
                return

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)',
                           (name, category, price, stock))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Product added successfully")
            product_window.destroy()
            self.load_products()

        product_window = tk.Toplevel(self.root)
        product_window.title("Add Product")
        product_window.geometry("400x300")
        product_window.configure(bg="#FFFFFF")

        tk.Label(product_window, text="Name", bg="#FFFFFF", fg="#000000", font=("Helvetica", 12)).pack(pady=5)
        name_entry = tk.Entry(product_window, width=30, font=("Helvetica", 12), bg="#F0F0F0", bd=1, relief="flat")
        name_entry.pack()

        tk.Label(product_window, text="Category", bg="#FFFFFF", fg="#000000", font=("Helvetica", 12)).pack(pady=5)
        category_entry = tk.Entry(product_window, width=30, font=("Helvetica", 12), bg="#F0F0F0", bd=1, relief="flat")
        category_entry.pack()

        tk.Label(product_window, text="Price", bg="#FFFFFF", fg="#000000", font=("Helvetica", 12)).pack(pady=5)
        price_entry = tk.Entry(product_window, width=30, font=("Helvetica", 12), bg="#F0F0F0", bd=1, relief="flat")
        price_entry.pack()

        tk.Label(product_window, text="Stock", bg="#FFFFFF", fg="#000000", font=("Helvetica", 12)).pack(pady=5)
        stock_entry = tk.Entry(product_window, width=30, font=("Helvetica", 12), bg="#F0F0F0", bd=1, relief="flat")
        stock_entry.pack()

        tk.Button(product_window, text="Save", command=save_product, bg="#000000", fg="#FFFFFF", font=("Helvetica", 12)).pack(pady=20)

    def load_products(self):
        for row in self.product_table.get_children():
            self.product_table.delete(row)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()

        for product in products:
            self.product_table.insert("", tk.END, values=product)

    def check_low_stock(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, stock FROM products WHERE stock < 10')
        low_stock_products = cursor.fetchall()
        conn.close()

        if low_stock_products:
            alert_text = "\n".join([f"{product[0]}: {product[1]} left" for product in low_stock_products])
            messagebox.showwarning("Low Stock Alert", f"The following products are running low:\n{alert_text}")
        else:
            messagebox.showinfo("Stock Check", "No low-stock products!")

    def sales_summary(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT products.name, SUM(sales.quantity) as total_sold
            FROM sales
            JOIN products ON sales.product_id = products.id
            GROUP BY products.name
            ORDER BY total_sold DESC
        ''')
        summary = cursor.fetchall()
        conn.close()

        report = "\n".join([f"{row[0]}: {row[1]} units sold" for row in summary])
        if not report:
            report = "No sales recorded."

        report_window = tk.Toplevel(self.root)
        report_window.title("Sales Summary")
        report_window.geometry("400x300")
        tk.Label(report_window, text="Sales Summary", font=("Helvetica", 16, "bold")).pack(pady=10)
        report_text = tk.Text(report_window, wrap="word", height=15, width=50)
        report_text.insert("1.0", report)
        report_text.pack()
        report_text.config(state="disabled")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernInventoryApp(root)
    root.mainloop()