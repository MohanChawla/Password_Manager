# ToDo Create basic UI, a canvas & a logo image onto it
# ToDO Complete the UI design with all components in grid layout
# ToDo Function for generating random password
# ToDo Function for saving the password to a file
# ToDo Implement a search functionality as well to search for stored data

from tkinter import *
from tkinter import messagebox
import json
import string
import random
# import pyperclip


# ---------------------------------- PASSWORD GENERATOR ---------------------------- #

def generate_password():
    cap_letters = string.printable[36:62]
    low_letters = string.printable[10:36]
    numbers = string.printable[:10]
    symbols = string.printable[62:94]

    password_letters = [random.choice(cap_letters) for _ in range(random.randint(3, 5))]
    password_l_letters = [random.choice(low_letters) for _ in range(random.randint(3, 5))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers + password_l_letters
    random.shuffle(password_list)

    password = "".join(password_list)
    e_password.insert(0, password)
    # pyperclip.copy(password)


# ---------------------------------- SAVE PASSWORD --------------------------------- #
def save():
    website = e_website.get()
    email = e_email.get()
    password = e_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            e_website.delete(0, END)
            e_password.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = e_website.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------------- UI SETUP -------------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg='white')

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_image = PhotoImage(file="lock_image.png")
# putting the image at the center of the canvas so position = 100,100
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=0, column=1)

# Labels
l_website = Label(text="Website:", bg='white')
l_website.grid(row=1, column=0)
l_email = Label(text="Email/Username:", bg='white')
l_email.grid(row=2, column=0)
l_password = Label(text="Password:", bg='white')
l_password.grid(row=3, column=0)

# Entries
e_website = Entry(width=35, highlightbackground='white')
e_website.grid(row=1, column=1, sticky=EW)
e_website.focus()
e_email = Entry(width=35, highlightbackground='white')
e_email.grid(row=2, column=1, columnspan=2, sticky=EW)
e_email.insert(0, "cmchawla68@gmail.com")
e_password = Entry(width=21, highlightbackground='white')
e_password.grid(row=3, column=1, sticky=EW)

# Buttons
search_button = Button(text="Search", width=14, command=find_password, highlightbackground='white',
                       activebackground='blue')
search_button.grid(row=1, column=2)
b_generate_password = Button(text="Generate Password", command=generate_password, highlightbackground='white',
                             activebackground='blue')
b_generate_password.grid(row=3, column=2, sticky=EW)
b_add = Button(text="Add", width=51, highlightbackground='white', activebackground='blue', command=save)
b_add.grid(row=4, column=1, columnspan=2)

window.mainloop()
