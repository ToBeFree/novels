# ÄÜConvert 2.0

Umrechnung zwischen irdischer UTC-Zeit und dem ÄÜC-Kalender der Äöüzz aus den Infinite Adventures,
in beide Richtungen, sekundengenau.

* `aueconvert.html` – eigenständige HTML-Seite (keine externen Ressourcen, hell/dunkel nach Systemeinstellung)

Rechenkern: ganzzahlig (BigInt), gregorianische Schaltjahre auch vor 1582, Jahr 0 und negative Jahre.
Die Rückrichtung ÄÜC → UTC liefert die einzige volle UTC-Sekunde im jeweiligen Örzklök-Intervall,
sodass jede Rundreise exakt zum Ausgangswert zurückkehrt. Geprüft gegen alle Beispieldaten der Bonuskapitel.

ÄÜConvert 2.0 ist eine Überarbeitung des ÄÜCalendars, den Tobias Frei ursprünglich auf Basis seiner Romane
geschrieben hat (tfrei.de/software). Diese überarbeitete Fassung wurde von Claude Fable 5.1 (Anthropic) erstellt.
Wie das Original ist auch diese Version gemeinfrei (CC0 / Public Domain). Die Zeitrechnung selbst stammt aus den
Bonuskapiteln der Infinite Adventures 2 und 3 (CC BY-SA 4.0, Tobias Frei).
