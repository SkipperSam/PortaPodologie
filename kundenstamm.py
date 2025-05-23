import tkinter as tk
from tkinter import ttk
import sqlite3
import os

def kundenstamm_window():

    print("Arbeitsverzeichnis:", os.getcwd())
    print("Erwartete Datenbank:", os.path.abspath('database_pp.db'))

    def lade_kunden(suchbegriff=""):
        # Tabelle leeren
        for item in tree.get_children():
            tree.delete(item)
        # Datenbankabfrage
        conn = sqlite3.connect('database_pp.db')
        cursor = conn.cursor()
        if suchbegriff:
            suchbegriff = f"%{suchbegriff}%"
            cursor.execute(
                "SELECT Vorname, Nachname FROM Kundendaten WHERE Vorname LIKE ? OR Nachname LIKE ?",
                (suchbegriff, suchbegriff)
            )
        else:
            cursor.execute("SELECT Vorname, Nachname FROM Kundendaten")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def suchen():
        lade_kunden(such_entry.get())

    window = tk.Toplevel()
    window.title("Kundenstamm")
    window.configure(bg="white")
    window.geometry("520x440")

    # Style
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="white",
                    fieldbackground="white",
                    font=("Arial", 12),
                    rowheight=28)
    style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

    heading = ttk.Label(window, text="Kundenstamm", font=("Arial", 18), background="white")
    heading.pack(pady=8)

    # Suchfeld
    such_frame = tk.Frame(window, bg="white")
    such_frame.pack(pady=5)
    such_label = ttk.Label(such_frame, text="Suche:", background="white")
    such_label.pack(side="left")
    such_entry = ttk.Entry(such_frame, width=20)
    such_entry.pack(side="left", padx=5)
    such_button = ttk.Button(such_frame, text="Suchen", command=suchen)
    such_button.pack(side="left")

    # Treeview für Kundenliste
    tree = ttk.Treeview(window, columns=("Vorname", "Nachname"), show="headings")
    tree.heading("Vorname", text="Vorname")
    tree.heading("Nachname", text="Nachname")
    tree.pack(fill="both", expand=True, padx=20, pady=15)

    lade_kunden()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    kundenstamm_window()
    root.mainloop()