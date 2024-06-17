"""
Created on Tue Nov  7 11:15:29 2023

@RPC
"""

import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os

db_path = 'C:/Users/Student/Desktop/Abschlussprojekt-Inventur.db'

# Prüfen ob bereits eine Datenbank existiert
if not os.path.exists(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Erstellen der Datenbank falls nicht existent
    sql = '''CREATE TABLE IF NOT EXISTS 'inventur1' (
        'Artikelbezeichnung' TEXT NOT NULL,
        'Artikelnummer' INTEGER NOT NULL,
        Lagerort TEXT NOT NULL,
        ArtikelIst INTEGER,
        ArtikelSoll INTEGER,
        Nachbestellung TEXT NOT NULL,
        PRIMARY KEY(Artikelbezeichnung)
    )'''
    cursor.execute(sql)

    connection.commit()
else:
    # Ansonsten Verbindung zur Datenbank herstellen 
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

def bestätigt():
    bestätigung = bestätigung_var.get()
    if bestätigung == 'Bestätigt!':
        bezeichnung = bezeichnung_eingabe.get()
        artikelnummer = artikelnummer_eingabe.get()
        if bezeichnung and artikelnummer:
            lagerort = lagerort_combobox.get()
            artikelIst = artikelIst_spinbox.get()
            artikelSoll = artikelSoll_spinbox.get()
            nachlieferung = nachlieferung_combobox.get()
            
            # Daten in die Datenbank einfügen
            sql = 'INSERT INTO inventur1 (Artikelbezeichnung, Artikelnummer, Lagerort, ArtikelIst, ArtikelSoll, Nachbestellung) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(sql, (bezeichnung, artikelnummer, lagerort, artikelIst, artikelSoll, nachlieferung))
            connection.commit()
            
            # Leeren der Eingabefelder nach Bestätigung
            bezeichnung_eingabe.delete(0, 'end')
            artikelnummer_eingabe.delete(0, 'end')
            lagerort_combobox.set('')
            artikelIst_spinbox.delete(0, 'end')
            artikelSoll_spinbox.delete(0, 'end')
            nachlieferung_combobox.set('')
            bestätigung_var.set('Nicht bestätigt')
            
            # Meldung bei unvollständiger Eingabe
        else:
            tkinter.messagebox.showwarning(title='Achtung!', message='Artikel-Bezeichnung und Nummer müssen eingegeben werden!')
    else:
        tkinter.messagebox.showwarning(title='Achtung!', message='Eingaben müssen bestätigt werden!')

    print('Bezeichnung:', bezeichnung, 'Artikelnummer:', artikelnummer)
    print('Lagerort:', lagerort, 'Artikel-Ist:', artikelIst, 'Artikel-Soll:', artikelSoll, 'Nachlieferung?:', nachlieferung)

# Erstellung des User Interface
fenster = tkinter.Tk()
fenster.title('Inventur1')

rahmen = tkinter.Frame(fenster)
rahmen.pack()

artikelbeschreibung_rahmen = tkinter.LabelFrame(rahmen, text='Artikelbeschreibung')
artikelbeschreibung_rahmen.grid(row=0, column=0, padx=20, pady=10)

bezeichnung_label = tkinter.Label(artikelbeschreibung_rahmen, text='Artikelbezeichnung')
bezeichnung_label.grid(row=0, column=0)

artikelnummer_label = tkinter.Label(artikelbeschreibung_rahmen, text='Artikelnummer')
artikelnummer_label.grid(row=0, column=1)

lagerort_label = tkinter.Label(artikelbeschreibung_rahmen, text='Lagerort')
lagerort_label.grid(row=0, column=2)

bezeichnung_eingabe = tkinter.Entry(artikelbeschreibung_rahmen)
bezeichnung_eingabe.grid(row=1, column=0)

artikelnummer_eingabe = tkinter.Entry(artikelbeschreibung_rahmen)
artikelnummer_eingabe.grid(row=1, column=1)

lagerort_combobox = ttk.Combobox(artikelbeschreibung_rahmen, values=['A-1', 'A-2', 'A-3', 'A-4', 'A-5', 'B-1', 'B-2', 'B-3', 'B-4', 'B-5', 'C-1', 'C-2', 'C-3', 'C-4', 'C-5'])
lagerort_combobox.grid(row=1, column=2)

for widget in artikelbeschreibung_rahmen.winfo_children():  # Überträgt Format
    widget.grid_configure(padx=10, pady=5)

artikelmenge_rahmen = tkinter.LabelFrame(rahmen, text='Artikelmenge')
artikelmenge_rahmen.grid(row=1, column=0, sticky='news', padx=20, pady=10)

artikelIst_label = tkinter.Label(artikelmenge_rahmen, text='Artikel-Ist')
artikelIst_label.grid(row=2, column=0)

artikelSoll_label = tkinter.Label(artikelmenge_rahmen, text='Artikel-Soll')
artikelSoll_label.grid(row=2, column=1)

nachlieferung_label = tkinter.Label(artikelmenge_rahmen, text='Nachbestellung?')
nachlieferung_label.grid(row=2, column=2)

artikelIst_spinbox = tkinter.Spinbox(artikelmenge_rahmen, from_=0, to='infinity')
artikelIst_spinbox.grid(row=3, column=0)

artikelSoll_spinbox = tkinter.Spinbox(artikelmenge_rahmen, from_=0, to='infinity')
artikelSoll_spinbox.grid(row=3, column=1)

nachlieferung_combobox = ttk.Combobox(artikelmenge_rahmen, values=['Ja!', 'Nein!'])
nachlieferung_combobox.grid(row=3, column=2)

for widget in artikelmenge_rahmen.winfo_children():
    widget.grid_configure(padx=10, pady=5)

bestätigung_rahmen = tkinter.LabelFrame(rahmen, text='Bestätigung der Eingabe')
bestätigung_rahmen.grid(row=2, column=0, sticky='news', padx=20, pady=10)

bestätigung_var = tkinter.StringVar(value='Nicht bestätigt')

bestätigung_check = tkinter.Checkbutton(bestätigung_rahmen, text='Hiermit bestätige ich Vollständig- und Richtigkeit, der Angaben!',
                                        variable=bestätigung_var, onvalue='Bestätigt!', offvalue='Nicht bestätigt')
bestätigung_check.grid(row=0, column=0)

button = tkinter.Button(rahmen, text='Eingabe bestätigt', command=bestätigt)
button.grid(row=3, column=0, sticky='news', padx=20, pady=20)

fenster.mainloop()
