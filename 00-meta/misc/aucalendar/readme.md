# ÄÜCalendar und ÄÜConvert 2.0

Umrechnung zwischen irdischer UTC-Zeit und dem ÄÜC-Kalender der Äöüzz aus den Infinite Adventures.

## Version 1.0: ÄÜCalendar (2022, Tobias Frei)

* `aucalendar.html`, `aucalendar.css`, `aucalendar.js` – Browserfassung, beide Richtungen
* `aucalendar.py.txt` – Python 3.9, UTC → ÄÜC, erzeugt die Tabellen
* `aucalendar-wm.txt` – Wolfram Language, UTC → ÄÜC
* `utc-auc-4000years-*-conversion-table.txt` – vorberechnete Tabellen (jährlich, täglich, stündlich)

Bekannte Abweichungen: Die Rückrichtung ÄÜC → UTC der JavaScript-Fassung liegt durch doppeltes Abschneiden
eine Sekunde zu früh. In der täglichen Tabelle (1.460.970 Zeilen) weichen 7 Zeilen um einen Örzklök ab,
weil die Gleitkommarechnung knapp unter einer Klök-Grenze aufrundet (z. B. 1566-01-05: exakt 38:03:11, Tabelle 38:03:12).

## Version 2.0: ÄÜConvert (2025)

* `aueconvert-2.0.html` – eigenständige HTML-Seite ohne externe Ressourcen, hell/dunkel nach Systemeinstellung

Rechenkern ganzzahlig (BigInt), gregorianische Schaltjahre auch vor 1582, Jahr 0 und negative Jahre in beide
Richtungen. Die Rückrichtung liefert die einzige volle UTC-Sekunde im jeweiligen Örzklök-Intervall, sodass jede
Rundreise exakt zum Ausgangswert zurückkehrt. Geprüft gegen alle Beispieldaten der Bonuskapitel und gegen die
tägliche 4000-Jahre-Tabelle (übereinstimmend bis auf die 7 oben genannten Zeilen, dort ist 2.0 exakt).

ÄÜConvert 2.0 ist eine Überarbeitung des ÄÜCalendars, den Tobias Frei ursprünglich auf Basis seiner Romane
geschrieben hat. Diese überarbeitete Fassung wurde von Claude Fable 5.1 (Anthropic) erstellt.
Wie das Original ist auch diese Version gemeinfrei (CC0 / Public Domain). Die Zeitrechnung selbst stammt aus den
Bonuskapiteln der Infinite Adventures 2 und 3 (CC BY-SA 4.0, Tobias Frei).
