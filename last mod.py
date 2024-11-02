import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

root = tk.Tk()
root.title("Login")
root.geometry("300x200")
root.configure(bg="#f2f2f2")

menu_window = None

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="bose15238",
        database="gym_manage"
    )

def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login WHERE username=%s AND pwd=%s", (username, password))
    result = cursor.fetchone()

    if result:
        root.destroy()
        show_main_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

    conn.close()

# Main menu after login
def show_main_menu():
    global menu_window
    if menu_window is not None:
        menu_window.destroy()

    menu_window = tk.Tk()
    menu_window.title("Gym Management System")
    menu_window.geometry("400x500")
    menu_window.configure(bg="#f2f2f2")

    tk.Label(menu_window, text="Gym Management System", font=("courier", 20, "bold"), bg="#f2f2f2", fg="#333").pack(pady=20)

    tk.Button(menu_window, text="NEW GYM", command=gym_page, width=20, bg="#4CAF50", fg="white", font=("Arial", 16)).pack(pady=20)
    tk.Button(menu_window, text="MAKE PAYMENT", command=payment_page, width=20, bg="#2196F3", fg="white", font=("Arial", 16)).pack(pady=20)
    tk.Button(menu_window, text="TRAINER", command=trainer_page, width=20, bg="#FF9800", fg="white", font=("Arial", 16)).pack(pady=20)
    tk.Button(menu_window, text="MEMBER", command=member_page, width=20, bg="#9C27B0", fg="white", font=("Arial", 16)).pack(pady=20)

def gym_page():
    gym_window = tk.Toplevel()
    gym_window.title("Gym Management")
    gym_window.geometry("780x640")
    gym_window.configure(bg="#e6e6e6")

    tk.Label(gym_window, text="Gym ID:", bg="#e6e6e6").grid(row=0, column=0, padx=10, pady=5)
    gym_id_entry = tk.Entry(gym_window, width=30)
    gym_id_entry.grid(row=0, column=1)

    tk.Label(gym_window, text="Gym Name:", bg="#e6e6e6").grid(row=1, column=0, padx=10, pady=5)
    gym_name_entry = tk.Entry(gym_window, width=30)
    gym_name_entry.grid(row=1, column=1)

    tk.Label(gym_window, text="Address:", bg="#e6e6e6").grid(row=2, column=0, padx=10, pady=5)
    address_entry = tk.Entry(gym_window, width=30)
    address_entry.grid(row=2, column=1)

    tk.Label(gym_window, text="Type:", bg="#e6e6e6").grid(row=3, column=0, padx=10, pady=5)
    type_entry = tk.Entry(gym_window, width=30)
    type_entry.grid(row=3, column=1)

    # Function to add a new gym
    def add_gym():
        gym_id = gym_id_entry.get()
        gym_name = gym_name_entry.get()
        address = address_entry.get()
        gym_type = type_entry.get()

        if not gym_id or not gym_name or not address or not gym_type:
            messagebox.showerror("Input Error", "Please fill in all fields")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO gym (gym_id, gym_name, address, type) VALUES (%s, %s, %s, %s)",
                           (gym_id, gym_name, address, gym_type))
            conn.commit()
            messagebox.showinfo("Success", "Gym added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add gym: {e}")
        finally:
            conn.close()

    # Function to search and display gym details
    def search_gym():
        search_id = search_entry.get()
        if not search_id:
            messagebox.showerror("Input Error", "Please enter a Gym ID to search")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM gym WHERE gym_id = %s", (search_id,))
            results = cursor.fetchall()

            # Clear previous search results
            for row in tree.get_children():
                tree.delete(row)

            if results:
                for result in results:
                    tree.insert("", tk.END, values=result)
                messagebox.showinfo("Search Result", "Gym details found.")
            else:
                messagebox.showinfo("Search Result", "No gym found with the provided ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving gym details: {e}")
        finally:
            conn.close()

    # Add buttons and labels to the Gym window
    tk.Button(gym_window, text="Add Gym", command=add_gym, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=4, column=1, pady=10)

    # Search section
    tk.Label(gym_window, text="Search Gym by ID:", bg="#e6e6e6").grid(row=5, column=0, padx=10, pady=10)
    search_entry = tk.Entry(gym_window, width=30)
    search_entry.grid(row=5, column=1)
    tk.Button(gym_window, text="Search", command=search_gym, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=5, column=2, padx=10)

    # Treeview for displaying results
    columns = ("Gym ID", "Gym Name", "Address", "Type")
    tree = ttk.Treeview(gym_window, columns=columns, show='headings')
    tree.grid(row=6, column=0, columnspan=3, pady=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

def member_page():
    member_window = tk.Toplevel()
    member_window.title("Member Management")
    member_window.geometry("780x640")
    member_window.configure(bg="#e6e6e6")

    tk.Label(member_window, text="Member ID:", bg="#e6e6e6").grid(row=0, column=0, padx=10, pady=5)
    member_id_entry = tk.Entry(member_window, width=30)
    member_id_entry.grid(row=0, column=1)

    tk.Label(member_window, text="Member Name:", bg="#e6e6e6").grid(row=1, column=0, padx=10, pady=5)
    member_name_entry = tk.Entry(member_window, width=30)
    member_name_entry.grid(row=1, column=1)

    tk.Label(member_window, text="Phone Number:", bg="#e6e6e6").grid(row=2, column=0, padx=10, pady=5)
    phone_entry = tk.Entry(member_window, width=30)
    phone_entry.grid(row=2, column=1)

    tk.Label(member_window, text="Membership Type:", bg="#e6e6e6").grid(row=3, column=0, padx=10, pady=5)
    membership_entry = tk.Entry(member_window, width=30)
    membership_entry.grid(row=3, column=1)

    def add_member():
        mem_id = member_id_entry.get()
        name = member_name_entry.get()
        phone = phone_entry.get()
        membership = membership_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO member (member_id, member_name, phone, membership_type) VALUES (%s, %s, %s, %s)",
                           (mem_id, name, phone, membership))
            conn.commit()
            messagebox.showinfo("Success", "Member added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add member: {e}")
        finally:
            conn.close()

    def search_member():
        search_id = search_entry.get()
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM member WHERE member_id = %s", (search_id,))
            results = cursor.fetchall()

            # Clear previous search results
            for row in tree.get_children():
                tree.delete(row)

            if results:
                for result in results:
                    tree.insert("", tk.END, values=result)
                messagebox.showinfo("Search Result", "Member details found.")
            else:
                messagebox.showinfo("Search Result", "No member found with the provided ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving member details: {e}")
        finally:
            conn.close()

    # Add buttons and labels to the Member window
    tk.Button(member_window, text="Add Member", command=add_member, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=4, column=1, pady=10)

    # Search section
    tk.Label(member_window, text="Search Member by ID:", bg="#e6e6e6").grid(row=5, column=0, padx=10, pady=10)
    search_entry = tk.Entry(member_window, width=30)
    search_entry.grid(row=5, column=1)
    tk.Button(member_window, text="Search", command=search_member, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=5, column=2, padx=10)

    # Treeview for displaying results
    columns = ("Member ID", "Member Name", "Phone Number", "Membership Type")
    tree = ttk.Treeview(member_window, columns=columns, show='headings')
    tree.grid(row=6, column=0, columnspan=3, pady=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

def payment_page():
    payment_window = tk.Toplevel()
    payment_window.title("Payment Management")
    payment_window.geometry("780x640")
    payment_window.configure(bg="#e6e6e6")

    tk.Label(payment_window, text="Payment ID:", bg="#e6e6e6").grid(row=0, column=0, padx=10, pady=5)
    payment_id_entry = tk.Entry(payment_window, width=30)
    payment_id_entry.grid(row=0, column=1)

    tk.Label(payment_window, text="Member ID:", bg="#e6e6e6").grid(row=1, column=0, padx=10, pady=5)
    member_id_entry = tk.Entry(payment_window, width=30)
    member_id_entry.grid(row=1, column=1)

    tk.Label(payment_window, text="Amount:", bg="#e6e6e6").grid(row=2, column=0, padx=10, pady=5)
    amount_entry = tk.Entry(payment_window, width=30)
    amount_entry.grid(row=2, column=1)

    tk.Label(payment_window, text="Date:", bg="#e6e6e6").grid(row=3, column=0, padx=10, pady=5)
    date_entry = tk.Entry(payment_window, width=30)
    date_entry.grid(row=3, column=1)

    def add_payment():
        payment_id = payment_id_entry.get()
        member_id = member_id_entry.get()
        amount = amount_entry.get()
        date = date_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO payment (payment_id, member_id, amount, date) VALUES (%s, %s, %s, %s)",
                           (payment_id, member_id, amount, date))
            conn.commit()
            messagebox.showinfo("Success", "Payment added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add payment: {e}")
        finally:
            conn.close()

    tk.Button(payment_window, text="Add Payment", command=add_payment, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=4, column=1, pady=10)

def trainer_page():
    trainer_window = tk.Toplevel()
    trainer_window.title("Trainer Management")
    trainer_window.geometry("780x640")
    trainer_window.configure(bg="#e6e6e6")

    tk.Label(trainer_window, text="Trainer ID:", bg="#e6e6e6").grid(row=0, column=0, padx=10, pady=5)
    trainer_id_entry = tk.Entry(trainer_window, width=30)
    trainer_id_entry.grid(row=0, column=1)

    tk.Label(trainer_window, text="Trainer Name:", bg="#e6e6e6").grid(row=1, column=0, padx=10, pady=5)
    trainer_name_entry = tk.Entry(trainer_window, width=30)
    trainer_name_entry.grid(row=1, column=1)

    tk.Label(trainer_window, text="Phone Number:", bg="#e6e6e6").grid(row=2, column=0, padx=10, pady=5)
    trainer_phone_entry = tk.Entry(trainer_window, width=30)
    trainer_phone_entry.grid(row=2, column=1)

    tk.Label(trainer_window, text="Specialization:", bg="#e6e6e6").grid(row=3, column=0, padx=10, pady=5)
    specialization_entry = tk.Entry(trainer_window, width=30)
    specialization_entry.grid(row=3, column=1)

    def add_trainer():
        trainer_id = trainer_id_entry.get()
        name = trainer_name_entry.get()
        phone = trainer_phone_entry.get()
        specialization = specialization_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO trainer (trainer_id, trainer_name, phone_number, specialization) VALUES (%s, %s, %s, %s)",
                           (trainer_id, name, phone, specialization))
            conn.commit()
            messagebox.showinfo("Success", "Trainer added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add trainer: {e}")
        finally:
            conn.close()

    def search_trainer():
        search_id = search_entry.get()
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM trainer WHERE trainer_id = %s", (search_id,))
            results = cursor.fetchall()

            # Clear previous search results
            for row in tree.get_children():
                tree.delete(row)

            if results:
                for result in results:
                    tree.insert("", tk.END, values=result)
                messagebox.showinfo("Search Result", "Trainer details found.")
            else:
                messagebox.showinfo("Search Result", "No trainer found with the provided ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving trainer details: {e}")
        finally:
            conn.close()

    # Add buttons and labels to the Trainer window
    tk.Button(trainer_window, text="Add Trainer", command=add_trainer, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=4, column=1, pady=10)

    # Search section
    tk.Label(trainer_window, text="Search Trainer by ID:", bg="#e6e6e6").grid(row=5, column=0, padx=10, pady=10)
    search_entry = tk.Entry(trainer_window, width=30)
    search_entry.grid(row=5, column=1)
    tk.Button(trainer_window, text="Search", command=search_trainer, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=5, column=2, padx=10)

    # Treeview for displaying results
    columns = ("Trainer ID", "Trainer Name", "Phone Number", "Specialization")
    tree = ttk.Treeview(trainer_window, columns=columns, show='headings')
    tree.grid(row=6, column=0, columnspan=3, pady=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

# UI Elements for login
tk.Label(root, text="Username:", bg="#f2f2f2").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password:", bg="#f2f2f2").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Login", command=login, bg="#4CAF50", fg="white").pack(pady=20)

root.mainloop()
