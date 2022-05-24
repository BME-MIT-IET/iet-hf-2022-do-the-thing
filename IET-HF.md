# Cosmos

## A projekt célja

A Cosmos projekt sok nyelven implementált különféle algoritmusok tárháza, aminek a fő vonzereje, hogy egyetlen repoban, pull után offline tesz elérhetővé olyan algoritmusokat, aminek egyébként online néznénk utána. Emellett a lefedett nyelvek elég széles köre miatt mindenki megtalálja a számára legérthetőbb implementációt.

Az utóbbi dolgot árnyalja, hogy valójában sok témakörhöz csak egy nyelven tartozik megvalósítás, illetve tesztek sincsenek mindenre konzisztensen megírva.

A kód mellett a repoban megtalálhatók útmutatók, stílusszabályok, referenciák a különféle nyelvekhez, illetve a buildeléshez is.

## Az általunk vizsgált részek

Mi a kereső, kiválasztó és rendező algoritmusok közül választunk néhányat tesztelésre, ugyanis ezeknek kézenfekvő a teljesímény-metrikája (futási idő a bemeneti tömb méretétől függően), másrészt ismerünk aszimptotikus becsléseket a futásidejükre, így a gyakorlati viselkedésüket vizsgálni tudjuk.

Az általunk választott nyelv a Java, mivel ehhez tanultunk build és teszt keretrendszer beüzemelését. 

A vizsgált kód elkülönítése érdekében a repo gyökérmappájában létrehoztuk a `code_under_test` mappát, amin belül kialakítjuk a Javára jellemző projektstruktúrát, más nyelven írt forrásfájlok és egyéb zavaró körülmények nélkül.
