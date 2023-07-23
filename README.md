# Hibabejelentő rendszer ami a helyi gépen található SQLite adatbázist használja. 
Ez a verzió (Python + Tkinter + SQLite) a helyi gépen létrehozott adatbázist használja,
és a hangsúly az MVC (Model-View-Controller) / Modell-Nézet-Vezérlő  programtervezési mintán található. 

Részei:
- hibabejelento.py 
    Az ügyfélszolgálat felveszi a hibajegyet. Ha tudjak, megoldja a problémát, és lezárja,
    ha nem tudják megoldani, akkor továbbdelegálja a műszakiak vagy a pénzügy felé.

- specialista.py
    A továbbdelegált problémát a műszakiak vagy a pénzügy lekéri (mindegyik a saját 
    illetékességébe tartozó típusút), megoldja, majd lezárja a hibajegyet. A lekérést a 
    legrégebbi hibajeggyel kezdi, csak olyat kér le, amin jelenleg más még nem dolgozik.

- test_ticket.py,  test_databasehandler.py
    TestCase az adatokhoz.
