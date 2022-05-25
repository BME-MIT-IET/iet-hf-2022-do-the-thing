# Stressz tesztek a rendező algoritmusokhoz

A rendező algoritmusok egyszerű osztályok, jobbára egyetlen függvénnyel, és függetlenek voltak egymástól, így csak a teljesítményükre voltunk kíváncsiak.
Ehhez különböző kevertségű listákat adtunk nekik, és próbálkoztunk többféle hosszúsággal is.

A tapasztalatok:
- az osztályok rosszúl szervezettek, egységesek kellenének legyenek, pl. egy interfészen keresztül.
- teljesítményük nem a legjobb, 20.000-nél hosszabb lista rendezésére nem alkalmasak.
- igyekeztünk a teljesítményüket a listák mérete mellett a listák kevertségével árnyalni, ez bizonyos esetekben sikeresnek tűnt (pl. a quicksortnál), a többieknél kevésbé.
- a teszteknél, a teljesítményt időben mértük: nem a legjobb megoldás, mivel nincs garanciánk arra, hogy a szálunk folyton prioritást élvez.
- az eredményeket jobb lenne látványosabban megjeleníteni.
