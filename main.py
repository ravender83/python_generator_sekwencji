from tkinter import *
from tkinter.font import Font
import tkinter.filedialog
import tkinter.messagebox
import os.path
import sekwencja
import rav.poka as poka

a_sciezki = ["funkcja.txt", "network.txt", "msg.txt", "tagi.txt"]


def czy_pliki_istnieja(lista_plikow):
    brakujace = []
    for plik in lista_plikow:
        if not os.path.isfile(plik):
            brakujace.append(os.path.basename(plik))
    return brakujace


def open_file():
    file = tkinter.filedialog.askopenfile(mode='rb', title='Wybierz plik')
    if file is not None:
        nazwa_pliku = os.path.basename(file.name)
        nazwa_pliku = nazwa_pliku.split('.')
        if str(nazwa_pliku[1]).isnumeric():
            edit_nazwa_funkcji.delete(0, END)
            edit_nazwa_funkcji.insert(0, nazwa_pliku[0])
            edit_numer_komunikatu.delete(0, END)
            edit_numer_komunikatu.insert(0, nazwa_pliku[1])

        data = file.read().decode('windows-1250')
        file.close()
        edytor_txt.delete(1.0, END)
        edytor_txt.insert(1.0, data)


def save_file(t):
    savelocation = tkinter.filedialog.asksaveasfilename(title='Podaj lokalizację',
                                                        filetypes=[('Plik sekwencji', '*.'+edit_numer_komunikatu.get())],
                                                        defaultextension='.txt', initialfile=edit_nazwa_funkcji.get())
    if savelocation != '':
        with open(savelocation, "w") as file:
            try:
                file.write(t)
                tkinter.messagebox.showinfo('Zapisywanie', 'Zapisano plik: {}'.format(savelocation))
            except:
                tkinter.messagebox.showerror('Zapisywanie', 'Wystąpił błąd zapisu!')
                pass


def clean_edytor():
    txt = edytor_txt.get(1.0, END)
    txt = sekwencja.Sekwencja.s_lst_prepare(txt)
    edytor_txt.delete(1.0, END)
    edytor_txt.insert(1.0, '\n'.join(txt))


def numer_komunikatu_callback(p):
    if str.isdigit(p) or p == '':
        return True
    else:
        return False


def toggle_nazwa_funkcji(*_):
    if edit_nazwa_funkcji.var.get() and edit_numer_komunikatu.var.get() and edit_nazwa_kroku.var.get():
        btn_convert['state'] = 'normal'
    else:
        btn_convert['state'] = 'disabled'


def toggle_numer_komunikatu(*_):
    if edit_nazwa_funkcji.var.get() and edit_numer_komunikatu.var.get() and edit_nazwa_kroku.var.get():
        btn_convert['state'] = 'normal'
    else:
        btn_convert['state'] = 'disabled'


def toggle_nazwa_kroku(*_):
    if edit_nazwa_funkcji.var.get() and edit_numer_komunikatu.var.get() and edit_nazwa_kroku.var.get():
        btn_convert['state'] = 'normal'
    else:
        btn_convert['state'] = 'disabled'


def generuj_sekwencje():
    l = [f'tmp/{plc.get()}/{a_sciezki[0]}', f'tmp/{plc.get()}/{a_sciezki[1]}',
         f'tmp/{plc.get()}/{a_sciezki[2]}', f'tmp/{plc.get()}/{a_sciezki[3]}']
    brak_szablonu = czy_pliki_istnieja(l)
    if len(brak_szablonu) > 0:
        edytor_txt.delete(1.0, END)
        edytor_txt.insert(END, 'Brakujące pliki szablonów:\n')
        edytor_txt.insert(END, brak_szablonu)
    else:
        clean_edytor()
        txt = edytor_txt.get(1.0, END)
        # global sekw
        sq = sekwencja.Sekwencja(edit_nazwa_funkcji.get(), int(edit_numer_komunikatu.get()),
                                 edit_nazwa_kroku.get(), txt)

        with open(f'tmp/{plc.get()}/{a_sciezki[0]}', "r", encoding="windows-1250") as f:
            sq.szablon['funkcja'] = f.read()
        with open(f'tmp/{plc.get()}/{a_sciezki[1]}', "r", encoding="windows-1250") as f:
            sq.szablon['network'] = f.read()
        with open(f'tmp/{plc.get()}/{a_sciezki[2]}', "r", encoding="windows-1250") as f:
            sq.szablon['msg'] = f.read()
        with open(f'tmp/{plc.get()}/{a_sciezki[3]}', "r", encoding="windows-1250") as f:
            sq.szablon['tagi'] = f.read()

        sciezka = os.path.abspath(os.path.dirname(sys.argv[0]))
        nazwa_pliku = sciezka + "/out/" + edit_nazwa_funkcji.get() + ".awl"
        nazwa_pliku_tag = sciezka + "/out/" + edit_nazwa_funkcji.get() + "_tagi.txt"
        nazwa_pliku_hmi = sciezka + "/out/" + edit_nazwa_funkcji.get() + "_hmi.txt"

        sq.zapisz_szablon(nazwa_pliku)
        sq.zapisz_tagi(nazwa_pliku_tag)
        sq.zapisz_komunikaty_hmi(nazwa_pliku_hmi)


#  ------------------------------------------


root = Tk()
root.title('STLgen v4.0')
root.minsize(800, 600)

sideFrame = Frame(root, width=100, padx=1)
sideFrame.pack(side=RIGHT, fill=Y)

leftFrame = Frame(root)
leftFrame.pack(side=LEFT, expand=TRUE, fill=BOTH)

#  ------------------------------------------

# Font
font_14_courier_new = Font(family='Courier New', size=14)
font_12_courier_new = Font(family='Courier New', size=12)

#  Open button
btn_open_ico = PhotoImage(file='ico/document-open.png')
btn_open = Button(sideFrame, text='Otwórz', height=34, image=btn_open_ico, compound=LEFT, padx=10, pady=2,
                  command=open_file).pack(fill=X)

#  Save button
btn_save_ico = PhotoImage(file='ico/media-floppy.png')
btn_save = Button(sideFrame, text='Zapisz', height=34, image=btn_save_ico, compound=LEFT, padx=10, pady=2,
                  command=lambda: save_file(edytor_txt.get(1.0, END))).pack(fill=X)

# Pole 'Nazwa funkcji'
Label(sideFrame, text='Nazwa funkcji').pack(fill=X, pady=[5, 0])
edit_nazwa_funkcji = Entry(sideFrame, font=font_12_courier_new, width=16, justify='center')
edit_nazwa_funkcji.var = tkinter.StringVar()
edit_nazwa_funkcji['textvariable'] = edit_nazwa_funkcji.var
edit_nazwa_funkcji.var.trace_add('write', toggle_nazwa_funkcji)
edit_nazwa_funkcji.pack()

# Pole 'Numer komunikatu'
Label(sideFrame, text='Numer komunikatu').pack(fill=X, pady=[5, 0])
edit_numer_komunikatu_vcmd = (sideFrame.register(numer_komunikatu_callback))
edit_numer_komunikatu = Entry(sideFrame, font=font_12_courier_new, width=16, justify='center',
                              validate='all', validatecommand=(edit_numer_komunikatu_vcmd, '%P'))
edit_numer_komunikatu.var = tkinter.StringVar()
edit_numer_komunikatu['textvariable'] = edit_numer_komunikatu.var
edit_numer_komunikatu.var.trace_add('write', toggle_numer_komunikatu)
edit_numer_komunikatu.pack()

# Pole 'Nazwa kroki'
Label(sideFrame, text='Nazwa kroku').pack(fill=X, pady=[5, 0])
edit_nazwa_kroku = Entry(sideFrame, font=font_12_courier_new, width=16, justify='center')
edit_nazwa_kroku.var = tkinter.StringVar()
edit_nazwa_kroku['textvariable'] = edit_nazwa_kroku.var
edit_nazwa_kroku.var.trace_add('write', toggle_nazwa_kroku)
edit_nazwa_kroku.pack()

# Pole 'Rodzaj sterownika'
sterownik = ['et200sp', 'et200s', 's7-1200']
plc = StringVar()
plc.set(sterownik[0])
Label(sideFrame, text='Rodzaj sterownika').pack(fill=X, pady=[5, 0])
edit_plc = OptionMenu(sideFrame, plc, *sterownik)
edit_plc.config(font=font_12_courier_new, width=16, justify='center')
edit_plc.pack()

#  Formatuj button
btn_format_ico = PhotoImage(file='ico/format-justify-left.png')
btn_format = Button(sideFrame, text='Formatuj', height=34, image=btn_format_ico, compound=LEFT, padx=10, pady=2,
                    command=clean_edytor)
btn_format.pack(fill=X, pady=[20, 0])

#  Convert button
btn_convert_ico = PhotoImage(file='ico/preferences-desktop-wallpaper.png')
btn_convert = Button(sideFrame, text='Konwertuj', height=34, image=btn_convert_ico, compound=LEFT, padx=10, pady=2,
                     command=generuj_sekwencje)
btn_convert.config(state=DISABLED)
btn_convert.pack(fill=X)

# #  Steps button
# btn_steps_ico = PhotoImage(file='ico/view-sort-descending.png')
# btn_steps = Button(sideFrame, text='Pokaż kroki', height=34, image=btn_steps_ico, compound=LEFT, padx=10, pady=2)
# btn_steps.config(state=DISABLED)
# btn_steps.pack(fill=X, pady=[20, 0])
#
# #  Msg button
# btn_msg_ico = PhotoImage(file='ico/accessories-dictionary.png')
# btn_msg = Button(sideFrame, text='Pokaż komunikaty', height=34, image=btn_msg_ico, compound=LEFT, padx=10, pady=2)
# btn_msg.config(state=DISABLED)
# btn_msg.pack(fill=X)
#
# #  Tags button
# btn_tags_ico = PhotoImage(file='ico/preferences-desktop-theme.png')
# btn_tags = Button(sideFrame, text='Pokaż tagi', height=34, image=btn_tags_ico, compound=LEFT, padx=10, pady=2)
# btn_tags.config(state=DISABLED)
# btn_tags.pack(fill=X)

#  Text
edytor_txt = Text(leftFrame, padx=5, pady=2, spacing1=1, font=font_14_courier_new, width=20)
edytor_txt.pack(fill=BOTH, expand=True, padx=1, pady=1)

root.mainloop()
