# Build+CI

## Build keretrendszer beüzemelése

Úgy döntöttünk, hogy a mi projektünkhöz egy Maven keretrendszert fogunk rendelni. 
Első lépésként kiválasztottuk a .java fájlokat amiket tesztelni szeretnénk és egy maven-nek megfelelő struktúrába rendeztük. Ezután generáltunk hozzá egy alapértelmezett pom.xml fájlt és abban dolgoztunk utána.
Itt függőségnek felvettük a JUnit-ot. 

## Continuous Integration

Generáltunk egy maven.yml fájlt ebben átírtuk a java verzióját és az pom.xml elérési útvonalát. 
Megadtuk, hogy gyorsítótárazza a maven termékeit és olvashatóbbá tettük a log-ot a --no-transfer-progress parancsal.

Ezek megcsinálása után githubon leteszteltük, hogy működik-e minden.

## Eredmény

A projektünk egy teljesen működő maven projekt lett.

## Tanulság

A github merge-ölési algoritmusa meglepően okos volt, mert különböző ágon változtattuk ugynazazt a fájl-t és semmi hiba nélkül működött a merge mert nem volt ütközés a változtatásokban.