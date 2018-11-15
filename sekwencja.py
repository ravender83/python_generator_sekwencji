class Sekwencja:
    def __init__(self, nazwa_funkcji, numer_komunikatu, nazwa_kroku, kroki):
        self.nazwa_funkcji = nazwa_funkcji  # np. A-kroki
        self.numer_komunikatu = numer_komunikatu  # np. 500
        self.nazwa_kroku = nazwa_kroku  # np. A-krok
        self.kroki = self.s_lst_prepare(kroki)
        self.lista_komentarzy = self.s_lst_gen_komentarze(self.kroki)

        if self.kroki:
            self.lista_krokow = self.s_lst_gen_kroki(len(self.kroki), self.nazwa_kroku)
        else:
            self.lista_krokow = []

        if self.kroki:
            self.lista_nr_komunikatow = self.s_lst_gen_nr_komunikatow(len(self.kroki), numer_komunikatu)
        else:
            self.lista_nr_komunikatow = []

        self.szablon = {
                        'network': '',
                        'msg': '',
                        'funkcja': '',
                        'tagi': ''
                       }

    @staticmethod
    def cc(string):
        return chr(34) + str(string) + chr(34) + ";"

    @staticmethod
    def s_lst_prepare(fdata):
        tekst = fdata.splitlines()

        kroki = []
        for i in tekst:
            tt = i.strip()
            if tt != '':
                kroki.append(tt)

        if len(kroki) > 0:
            if kroki[-1].lower() != 'koniec':
                kroki.append('Koniec')
            return kroki
        else:
            return []

    @staticmethod
    def s_lst_gen_komentarze(kroki):
        if kroki:
            l_komentarzy = []
            l_komentarzy.extend(kroki)
            l_komentarzy.append('Brak kroków')
            l_komentarzy.append('Reset kroków')
            return l_komentarzy
        else:
            return []

    @staticmethod
    def s_lst_gen_kroki(ilosc_krokow, nazwa_kroku):
        if ilosc_krokow != 0:
            if nazwa_kroku != '':
                l_krokow = []
                for i in range(ilosc_krokow):
                    if i < ilosc_krokow - 1:
                        l_krokow.append(nazwa_kroku + "_" + '{:02d}'.format(i))
                    elif i == ilosc_krokow - 1:
                        l_krokow.append(nazwa_kroku + "_" + '{:02d}'.format(50))
                return l_krokow
            else:
                return []
        else:
            return []

    @staticmethod
    def s_lst_gen_nr_komunikatow(ilosc_krokow, poczatek):
        if ilosc_krokow >= 2:
            if poczatek > 0:
                l_nr_komunikatow = []
                for i in range(poczatek, (poczatek + ilosc_krokow) - 1):
                    l_nr_komunikatow.append(str(i))
                return l_nr_komunikatow
            else:
                return []
        else:
            return []

    @property
    def p_str_krok_brak(self):
        return self.nazwa_kroku + '_brak'

    @property
    def p_str_krok_reset(self):
        return self.nazwa_kroku + '_reset'

    def str_brak_krokow(self):
        l_brak = []
        if self.lista_krokow:
            for i in self.lista_krokow:
                l_brak.append(f'      AN {self.cc(i)}\n')
            l_brak.append(f'      =  {self.cc(self.p_str_krok_brak)}')
            return ''.join(l_brak)
        else:
            return ''

    def str_network_init(self, szablon):
        if szablon != '':
            szablon_init = szablon
            szablon_init = szablon_init.replace("{tytul}", "Inicjalizacja")
            szablon_init = szablon_init.replace("{nastepny_krok}", self.cc(self.lista_krokow[0]))
            szablon_init = szablon_init.replace("{reset_krokow}", self.cc(self.p_str_krok_reset))
            warunek_wejsca = f'      AN {self.cc(self.p_str_krok_reset)}\n      A {self.cc(self.p_str_krok_brak)}'
            warunek_wyjscia = f'      O {self.cc(self.lista_krokow[1])}'
            szablon_init = szablon_init.replace("{warunek_wejscia}", warunek_wejsca)
            szablon_init = szablon_init.replace("{warunek_wyjscia}", warunek_wyjscia)
            szablon_init = szablon_init + '\n'
            return szablon_init
        else:
            return ''

    def str_networki(self, nowy_szablon):
        # Network inicjalizacyjny
        l_networki = [self.str_network_init(nowy_szablon)]

        # Reszta networków
        for i in range(len(self.lista_krokow)-1):
            szablon = nowy_szablon
            szablon = szablon.replace("{tytul}", self.lista_komentarzy[i])
            szablon = szablon.replace("{nastepny_krok}", self.cc(self.lista_krokow[i + 1]))
            szablon = szablon.replace("{reset_krokow}", self.cc(self.p_str_krok_reset))

            # Warunek wejścia
            if i == 0:
                warunek_wejsca = f'      A {self.cc(self.lista_krokow[i])}'
            else:
                warunek_wejsca = f'      AN {self.cc(self.lista_krokow[i - 1])}\n' + \
                                 f'      A {self.cc(self.lista_krokow[i])}'

            # Warunek wyjścia
            if i == len(self.lista_krokow)-2:
                warunek_wyjscia = f'      AN {self.cc(self.lista_krokow[i])}\n' + \
                                  f'      A {self.cc(self.lista_krokow[i + 1])}'
            else:
                warunek_wyjscia = f'      O {self.cc(self.lista_krokow[i + 2])}'

            szablon = szablon.replace("{warunek_wejscia}", warunek_wejsca)
            szablon = szablon.replace("{warunek_wyjscia}", warunek_wyjscia)
            szablon = szablon + '\n'
            l_networki.append(szablon)
        return ''.join(l_networki)

    def str_komunikaty(self, nowy_szablon):
        l_komunikaty = []

        l_zip = list(zip(self.lista_nr_komunikatow, self.lista_krokow, self.lista_komentarzy))

        for i in l_zip:
            szablon = nowy_szablon
            szablon = szablon.replace("{msg_numer}", i[0])  # i[0] numer komunikatu, np. 500
            szablon = szablon.replace("{warunek_wejscia}", "      O " + self.cc(i[1]))  # i[1] nazwa kroku, A-krok_00
            szablon = szablon.replace("{tytul}", i[2])  # i[2] komentarz, np. Sprawdzenie PW
            szablon = szablon + '\n'
            l_komunikaty.append(szablon)
        return ''.join(l_komunikaty)

    def str_tagi(self, nowy_szablon):
        l_kroki = []
        l_kroki.extend(self.lista_krokow)
        l_kroki.append(self.p_str_krok_brak)
        l_kroki.append(self.p_str_krok_reset)
        l_tt = list(zip(l_kroki, self.lista_komentarzy))

        l_tagi = []
        for i in l_tt:
            szablon = nowy_szablon
            szablon = szablon.replace("{krok}", i[0])  # i[0] nazwa kroku, np. A-krok_00
            szablon = szablon.replace("{komentarz}", i[1])  # i[2] komentarz, np. Sprawdzenie PW
            l_tagi.append(szablon + '\n')
        return ''.join(l_tagi)

    def str_komunikaty_hmi(self):
        l_zip = list(zip(self.lista_nr_komunikatow, self.lista_krokow, self.lista_komentarzy))

        l_komunikaty = []
        for i in l_zip:
            l_komunikaty.append(f'{i[0]}\t{i[2]}\n')
        return ''.join(l_komunikaty)

    def zapisz_szablon(self, sciezka):
        # Wczytanie głównego szablonu funkcji
        plik_funkcji = self.szablon['funkcja']
        plik_funkcji = plik_funkcji.replace("{nazwa_funkcji}", self.nazwa_funkcji)
        plik_funkcji = plik_funkcji.replace("{reset_krokow}", self.cc(self.p_str_krok_reset))
        plik_funkcji = plik_funkcji.replace("{brak_krokow}", self.str_brak_krokow())
        plik_funkcji = plik_funkcji.replace("{kroki}", self.str_networki(self.szablon['network']))
        plik_funkcji = plik_funkcji.replace("{komunikaty}", self.str_komunikaty(self.szablon['msg']))
        try:
            f = open(sciezka, "w", encoding="windows-1250")
            f.write(plik_funkcji)
            f.close()
            print("Wygenerowano plik: " + sciezka)
            return 1
        except ValueError:
            print("Błąd zapisu pliku")

    def zapisz_tagi(self, sciezka):
        try:
            f = open(sciezka, "w", encoding="windows-1250")
            f.write(self.str_tagi(self.szablon['tagi']))
            f.close()
            print("Wygenerowano plik: " + sciezka)
        except ValueError:
            print("Błąd zapisu pliku")

    def zapisz_komunikaty_hmi(self, sciezka):
        try:
            f = open(sciezka, "w", encoding="windows-1250")
            f.write(self.str_komunikaty_hmi())
            f.close()
            print("Wygenerowano plik: " + sciezka)
        except ValueError:
            print("Błąd zapisu pliku")
