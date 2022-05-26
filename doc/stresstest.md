# Stressz tesztek a rendező algoritmusokhoz

A rendező algoritmusok egyszerű osztályok, jobbára egyetlen függvénnyel, és függetlenek voltak egymástól, így csak a teljesítményükre voltunk kíváncsiak.
Ehhez különböző kevertségű listákat adtunk nekik, és próbálkoztunk többféle hosszúsággal is.

## Tanulságok
- az osztályok rosszul szervezettek, egységesek kellene legyenek, pl. egy interfészen keresztül.
- teljesítményük nem a legjobb, 20.000-nél hosszabb lista rendezésére nem alkalmasak.
- igyekeztünk a teljesítményüket a listák mérete mellett a listák kevertségével árnyalni, ez bizonyos esetekben sikeresnek tűnt (pl. a quicksortnál), a többieknél kevésbé.
- a teszteknél, a teljesítményt időben mértük: nem a legjobb megoldás, mivel nincs garanciánk arra, hogy a szálunk folyton prioritást élvez, de jobb megoldás a vizsgált kód manipulálása nélkül gyakorlatilag nincs.
- az eredményeket jobb lenne látványosabban megjeleníteni, pl grafikonban.

## Utólagos változtatás
A teljesítményellenőrzés egyes tesztesetei annyira sokáig futottak, hogy ki kellett zárni őket a maven build folyamatból, mivel hátráltatták a pull request-ek ellenőrzését. Ezek akár lokálisan visszakapcsolhatók a `pom.xml` megfelelő `exclude` tagjeinek törlésével.
