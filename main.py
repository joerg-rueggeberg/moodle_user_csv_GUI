import os
from tkinter import *
from tkinter import messagebox

FILEPATH = os.environ.get("FILEPATH")

data = {
    "headline": "username,firstname,lastname,email,password",
    "user": [],
    "email_start": "",
    "password": ""
}
data_mail = []
umlaute = ["Ä", "Ö", "Ü", "ä", "ö", "ü"]
umlaute_neu = ["Ae", "Oe", "Ue", "ae", "oe", "ue"]


def data_prep():
    global data
    global data_mail

    if entry_mail.get() and entry_password.get() != "":
        data_mail_temp = entry_mail.get()
        data_pass_temp = entry_password.get()

        confirm_config = messagebox.askokcancel(title="Daten bestätigen", message=f"Diese Daten wurden erzeugt: \n\n"
                                                                                  f"E-Mail: {data_mail_temp}\n"
                                                                                  f"Passwort: {data_pass_temp}\n\n"
                                                                                  f"Sind diese Daten korrekt?")
        if confirm_config:
            data["password"] = entry_password.get()
            data_mail.append(data_mail_temp.split("@")[0][:-3])
            data_mail.append(int(data_mail_temp.split("@")[0][-3:]))
            data_mail.append(data_mail_temp.split("@")[1])

            entry_mail.config(state=DISABLED)
            entry_password.config(state=DISABLED)
            button_config.config(state=DISABLED)

            entry_vorname.config(state=NORMAL)
            entry_nachname.config(state=NORMAL)
            button_save.config(state=NORMAL)

            entry_vorname.focus()
    else:
        messagebox.showwarning(title="Fehler - fehlende Daten", message="Bitte E-Mail und Passwort vollständig "
                                                                        "ausfüllen!")


def user_add():
    global data
    global data_mail

    if entry_vorname.get() and entry_nachname.get() == "":
        messagebox.showwarning(title="Fehler - fehlende Daten", message="Bitte Vorname und Nachname vollständig "
                                                                        "ausfüllen!")
    else:
        firstname = entry_vorname.get().title()
        lastname = entry_nachname.get().title()

        firstname_temp = [umlaute_neu[umlaute.index(c)] if c in umlaute else c for c in firstname]
        firstname_temp = "".join(firstname_temp)
        lastname_temp = [umlaute_neu[umlaute.index(c)] if c in umlaute else c for c in lastname]
        lastname_temp = "".join(lastname_temp)

        username_temp = f"{firstname_temp[0]}{lastname_temp}".lower()

        data_mail_temp = data_mail
        data_mail_temp[1] += 1

        if len(str(data_mail_temp[1])) == 1:
            mail_num = f"00{data_mail_temp[1]}"
        elif len(str(data_mail_temp[1])) == 2:
            mail_num = f"0{data_mail_temp[1]}"
        else:
            mail_num = data_mail_temp[1]

        mail_temp = f"{data_mail[0]}{mail_num}@{data_mail[2]}"

        user_temp = [f"{username_temp},{firstname},{lastname},{mail_temp},{data['password']}"]
        confirm_user = messagebox.askokcancel(title="Benutzer hinzufügen", message=f"Diese Daten wurden erzeugt: \n\n"
                                                                                   f"Username: {username_temp}\n"
                                                                                   f"Vorname: {firstname}\n"
                                                                                   f"Nachname: {lastname}\n"
                                                                                   f"E-Mail: {mail_temp}\n"
                                                                                   f"Passwort: {data['password']}\n\n"
                                                                                   f"Sind diese Daten korrekt?")
        if confirm_user:
            data["user"].append(user_temp)
            print(data["user"])
            user_next = messagebox.askokcancel(title="Weitere Benutzer hinzufügen?", message=f"Sollen weitere "
                                                                                             f"Benutzer hinzugefügt "
                                                                                             f"werden? \n\n")
            if not user_next:
                entry_vorname.config(state=DISABLED)
                entry_nachname.config(state=DISABLED)
                button_save.config(state=DISABLED)

                button_export.config(state=NORMAL, bg="green", fg="white")
            else:
                entry_vorname.delete(0, "end")
                entry_vorname.focus()
                entry_nachname.delete(0, "end")
        else:
            data_mail_temp[1] -= 1


def export():
    with open(FILEPATH, "w") as file:
        file.write(f"{data['headline']}\n")

    for u in data["user"]:
        with open(FILEPATH, "a+") as file:
            file.write(f"{u[0]}\n")

    messagebox.showinfo(title="Info", message="CSV Datei erfolgreich erstellt.")
    exit()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Moodle CSV Generator - JR")
window.config(padx=30, pady=30, background="white")

# canvas = Canvas(width=100, height=100, bg="white", highlightthickness=0)
# logo_img = PhotoImage(file="img/logo.png")
# canvas.create_image(100, 100, image=logo_img)
# canvas.grid(column=0, row=0)

# LABELS
gui_mail = Label(text="Letzte E-Mail: ", background="white", pady=5)
gui_password = Label(text="Passwort: ", background="white", pady=5)
gui_vorname = Label(text="Vorname: ", background="white", pady=5)
gui_nachname = Label(text="Nachname: ", background="white", pady=5)
gui_empty_01 = Label(text="", background="white", pady=5)
gui_empty_02 = Label(text="", background="white", pady=5)

gui_mail.grid(column=0, row=1, sticky="w")
gui_password.grid(column=0, row=2, sticky="w")
gui_empty_01.grid(column=0, row=4)
gui_vorname.grid(column=0, row=5, sticky="w")
gui_nachname.grid(column=0, row=6, sticky="w")
gui_empty_02.grid(column=0, row=8)

# INPUTS
entry_mail = Entry()
entry_mail.focus()
entry_password = Entry()
entry_vorname = Entry(state=DISABLED)
entry_nachname = Entry(state=DISABLED)

entry_mail.grid(column=1, row=1, sticky="ew")
entry_password.grid(column=1, row=2, sticky="ew")
entry_vorname.grid(column=1, row=5, sticky="ew")
entry_nachname.grid(column=1, row=6, sticky="ew")

# BUTTONS
button_config = Button(text="Daten übernehmen", command=data_prep)
button_save = Button(text="Nutzer speichern", command=user_add, state=DISABLED)
button_import = Button(text="Nutzer importieren", state=DISABLED)
button_export = Button(text="CSV exportieren", command=export, state=DISABLED)

button_config.grid(column=1, row=3, sticky="ew")
button_save.grid(column=1, row=7, sticky="ew")
button_import.grid(column=0, row=9, sticky="ew")
button_export.grid(column=1, row=9, sticky="ew")

window.mainloop()
