import tkinter as tk
from tkinter import messagebox

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Successful champ!", "Welcome, D. Nabeel !")
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Create the main window
root = tk.Tk()
root.title("Login")
root.geometry("350x250")
root.configure(bg="#2c3e50")  # Dark background

# Styling options
label_font = ("Segoe UI", 12)
entry_font = ("Segoe UI", 11)
btn_font = ("Segoe UI", 11, "bold")

# Header
header = tk.Label(root, text="Welcome Back!", font=("Segoe UI", 16, "bold"), fg="white", bg="#2c3e50")
header.pack(pady=(20, 10))

# Username
label_username = tk.Label(root, text="Username", font=label_font, fg="white", bg="#2c3e50")
label_username.pack()
entry_username = tk.Entry(root, font=entry_font, width=25)
entry_username.pack(pady=5)

# Password
label_password = tk.Label(root, text="Password", font=label_font, fg="white", bg="#2c3e50")
label_password.pack()
entry_password = tk.Entry(root, font=entry_font, show="*", width=25)
entry_password.pack(pady=5)

# Login Button
login_button = tk.Button(root, text="Login", command=login, font=btn_font, bg="#1abc9c", fg="white", width=15)
login_button.pack(pady=15)

root.mainloop()
