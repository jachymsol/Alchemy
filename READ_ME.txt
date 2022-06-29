Alchemy je hra připravená pro tábory Země Nezemě 2020. 
Inspirace je ze hry na stejném principu ze soustředění Matematického korespondenčního semináře PraSe z roku 2018.
Programy vytvořil Jáchym Solecký. Máte-li dotazy či potíže, můžete mě kontaktovat e-mailem na solejabreck@gmail.com.


==== PRAVIDLA PRO ÚČASTNÍKY ====

Účastníci jsou rozděleni do několika týmů, každý tým má k dispozici jednu alchymistickou stanici.
Jejich cílem je vytvořit danou věc (případně vícero daných věcí) ze základních surovin: kamen, voda, vzduch, zeme.
Tyto suroviny jsou k dispozici ke sběru (jako žetony, tj. lístečky/korky/apod.) na stanovištích kolem základny (ve vzdálenosti cca 100 metrů - na Výštici voda u mola, země u vchodu do lesa, kamen 30 metrů po příjezdovce, vzduch u čtvrté třešně).
Každý účastník může na jednu cestu přinést pouze jeden žeton, který poté přidá do své alchymistické stanice a s nimi může experimentovat.
V průběhu hry se výtěžnost jednoho žetonu může zlepšovat (protože je jich větší spotřeba). 

Ve své alchymistické stanici pak účastníci mohou kombinovat získané suroviny, aby vytvořili nové (například voda + vzduch = mlha apod.) a dostali se tak až k cílové věci.


==== PROGRAMY ====

Každý počítač musí mít staženou složku alchemy (a extrahovanou). Musí mít také nainstalovaný Python.

alchemy_full_release.py - samostačné vydání, suroviny se přidávají přímo v něm
alchemy_server_release.py - serverové vydání, tj samostatná stanice na zadávání surovin pro týmy
alchemy_client_release.py - klientové vydání, bez možnosti přidávat suroviny, závisí na serveru
alchemy_vyhodnoceni.py - vyhodnocení výsledků, viz níže


Pro server/klient vydání je potřeba mít oba počítače připojené na stejné síti (např. přes Wi-Fi nebo Ethernet). 
Je také potřeba znát IP adresu server počítače na dané síti (lze najít v Nastavení -> Síť a Internet -> Zobrazit vlastnosti sítí -> IPv4 adresa), bude mít tvar např. 192.168.2.148 (číslo za lomítkem není potřeba)

Nejprve je potřeba spustit serverové vydání, pak až klientové vydání. Poté lze kliknout na tlačítko Přidat tým a nový tým by se měl připojit. 

Zkratkou <Control-F11> lze přepnout do fullscreen módu - funguje jako další pojistka, že účastníci nezneužijí notebooku. Veškeré ostatní ovládání by mělo být intuitivní.


==== RECEPTY ====

Recepty jsou uložené v dokumentu recipes.txt
Je možné tento soubor nahradit svou vlastní verzí (podle konečných surovin), recepty musí být na jednotlivých řádcích ve formátu věc1 + věc2 = výsledek (včetně mezer).


==== VYHODNOCENÍ ====

Každý tým po sobě nechá log toho, co udělal, pojmenovaný podle času vytvoření (např. "Log 2020-08-07 20-25-11.txt"). Tyto log soubory slouží k závěrečnému vyhodnocení.

AUTOMATICKÉ: Spusťte program alchemy_vyhodnoceni.py a ve chvíli, kdy se zeptá na název log souboru, vložte jej (včetně koncovky .txt) a stiskněte Enter. Až postupně vložíte log soubory všech týmů, nechte pole prázdné a stiskněte Enter. Výsledky se uloží do stejné složky do souboru s názvem "vysledky.txt".

MANUÁLNÍ: Každý tým po sobě nechá log toho, co udělal. Ve chvíli, kdy se stanice zavře, na konec logu se zapíše i inventář, který tým na konci hry měl. Je možné tedy log zkontrolovat manuálně.

Log soubory lze také použít pokud je hra zavřená předčasně, viz debugging.


==== DEBUGGING ====

Pokud účastníci log zavřou předčasně, je možné hru spustit v místě, kde přestali. Stačí při novém spuštění vložit název logu, který se při dané hře vytvořil (včetně koncovky .txt)

Pokud se přeruší spojení mezi serverem a klientem, poznají to obě stanice (server při snaze poslat další surovinu, klient při jakémkoliv dalším kliknutí). Pro obnovení spojení je potřeba začít novou hru (pomocí vytvořeného logu) a na serverovské stanici přidat nový tým.