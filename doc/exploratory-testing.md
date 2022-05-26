# Exploratory testing

## Tervezés

Rendezett tömbön kereső algoritmusokat céloztuk meg ezzel a teszteléssel, mivel a rendző algoritmusok már tesztelve voltak egy másik feladatban. 

Amelett döntöttünk, hogy itt is az algoritmusok futási idejét fogjuk tesztelni, mivel más adatok kinyeréséhez (pl. lépésszám) bele kellene nyúljunk az algoritmusok kódjába.
Viszont a másfajta tesztelés támogatásának érdekében azt találtuk ki, hogy egy interaktív tesztprogramot írunk, amiben a standard inputról beolvasott bemeneti értékekre futtatjuk a megadott kereső algoritmusokat.


## Megvalósítás

A program lekérdezi, hogy melyik algoritmus lesz tesztelve, ezután bekér egy tömb méretet, majd annyi darab számot. 
Nem várjuk el hogy a lista rendezett legyen, a program rendezi, miután megkapta. 
Ezután bekérjük a számot amit meg fog keresni a program. 
A tesztprogram lefuttatja a megfelelő algoritmust és kiírja, hogy pontosan mennyi idő alatt végzett (mikroszekundumban) és hogy sikerült-e megtalálnia vagy sem a keresett elemet.

## Eredmények

A programot ki is próbáltuk, néhány banális tesztesetet adtunk be, viszont így is sikerült hibát találni, mégpedig a Fibonacci keresés algoritmusában. Ha keresett elem nagyobb, mint a tömb összes eleme, nem -1-gyel tér vissza a vizsgált függvény, mint elvárt lenne, hanem túlindexelési hiba miatt leáll.
Ez egy issue-ban rögzítve is lett.

## Tanulság

A feladat megoldása során sikerült felfedezni, mennyire változatos lehet egy exploratory testing folyamat. Emellett felismertünk egy hibát az eredeti repositoryban, ami egyáltalán nem volt szembetűnő.


