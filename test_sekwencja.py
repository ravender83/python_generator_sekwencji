import unittest
from sekwencja import Sekwencja


class TestSekwencja(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.sekw_1 = Sekwencja('A-Kroki', 500, 'A-krok', 'first\nsecond')
        self.sekw_2 = Sekwencja('A-MP_Kroki', 600, 'A-mp', '  first \n\tSecond \n\t\tkoniec\t\t')
        self.sekw_3 = Sekwencja('A-Kalibracja', 700, 'A-kalibracja', '\t \n\n\t\t')

    def teatDown(self):
        pass

    def test_prepare(self):
        self.assertEqual(self.sekw_1.kroki, ['First', 'Second', 'Koniec'])
        self.assertEqual(self.sekw_2.kroki, ['First', 'Second', 'Koniec'])
        self.assertEqual(self.sekw_3.kroki, [])

    def test_gen_komentarze(self):
        self.assertEqual(self.sekw_1.lista_komentarzy, ['First', 'Second', 'Koniec', 'Brak kroków', 'Reset kroków'])
        self.assertEqual(self.sekw_2.lista_komentarzy, ['First', 'Second', 'Koniec', 'Brak kroków', 'Reset kroków'])
        self.assertEqual(self.sekw_3.lista_komentarzy, [])

    def test_gen_kroki(self):
        self.assertEqual(self.sekw_1.lista_krokow, ['A-krok_00', 'A-krok_01', 'A-krok_50'])
        self.assertEqual(self.sekw_2.s_lst_gen_kroki(4, 'A-test'), ['A-test_00', 'A-test_01', 'A-test_02', 'A-test_50'])
        self.assertEqual(self.sekw_2.s_lst_gen_kroki(0, 'A-test'), [])
        self.assertEqual(self.sekw_2.s_lst_gen_kroki(2, ''), [])
        self.assertEqual(self.sekw_2.s_lst_gen_kroki(1, 'A-test'), ['A-test_50'])
        self.assertEqual(self.sekw_3.lista_krokow, [])

    def test_gen_nr_komunikatow(self):
        self.assertEqual(self.sekw_1.lista_nr_komunikatow, ['500', '501'])
        self.assertEqual(self.sekw_2.s_lst_gen_nr_komunikatow(4, 500), ['500', '501', '502'])
        self.assertEqual(self.sekw_2.s_lst_gen_nr_komunikatow(0, 500), [])
        self.assertEqual(self.sekw_2.s_lst_gen_nr_komunikatow(1, 500), [])
        self.assertEqual(self.sekw_2.s_lst_gen_nr_komunikatow(2, 500), ['500'])
        self.assertEqual(self.sekw_2.s_lst_gen_nr_komunikatow(2, 0), [])
        self.assertEqual(self.sekw_2.s_lst_gen_nr_komunikatow(2, -1), [])
        self.assertEqual(self.sekw_3.lista_nr_komunikatow, [])

    def test_brak_reset(self):
        self.assertEqual(self.sekw_1.p_str_krok_brak, 'A-krok_brak')
        self.assertEqual(self.sekw_1.p_str_krok_reset, 'A-krok_reset')
        self.assertEqual(self.sekw_2.p_str_krok_brak, 'A-mp_brak')
        self.assertEqual(self.sekw_2.p_str_krok_reset, 'A-mp_reset')
        self.assertEqual(self.sekw_3.p_str_krok_brak, 'A-kalibracja_brak')
        self.assertEqual(self.sekw_3.p_str_krok_reset, 'A-kalibracja_reset')

    def test_cc(self):
        self.assertEqual(self.sekw_1.cc('a'), '\"a\";')
        self.assertEqual(self.sekw_1.cc(''), '\"\";')

    def test_str_brak_krokow(self):
        t = '      AN "A-krok_00";\n      AN "A-krok_01";\n      AN "A-krok_50";\n      =  "A-krok_brak";'
        self.assertEqual(self.sekw_1.str_brak_krokow(), t)
        self.assertEqual(self.sekw_3.str_brak_krokow(), '')

    def test_str_network_init(self):
        szablon = '{tytul}{warunek_wejscia}{nastepny_krok}{warunek_wyjscia}{reset_krokow}'
        wynik = 'Inicjalizacja      AN "A-krok_reset";\n      A "A-krok_brak";' \
                '"A-krok_00";      O "A-krok_01";"A-krok_reset";\n'
        self.assertEqual(self.sekw_1.str_network_init(szablon), wynik)

    def test_str_networki(self):
        pass

    def test_str_komunikaty(self):
        pass

    def test_str_tagi(self):
        pass

    def test_str_komunikaty_hmi(self):
        pass

if __name__ == '__main__':
    unittest.main()
