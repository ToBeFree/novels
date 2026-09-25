#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt die ASCII-Karten der Fnbsrd-Welt.

    python3 world-map-generator.py 1  > world-map-fnbsrd-01.txt
    python3 world-map-generator.py 12 > world-map-fnbsrd-01-02.txt

Die Karten werden auf einer Zeichenfläche zusammengesetzt; Orte lassen sich
durch Ändern der Koordinaten in draw_band1() und draw_band2() verschieben.

Dieses Skript wurde auf Basis der von Tobias Frei geschriebenen Romane
durch die KI Claude Fable 5.1 erstellt und ist gemeinfrei (CC0 / Public Domain).
"""
import sys


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [[" "] * w for _ in range(h)]

    def put(self, x, y, s, clear=0):
        """Schreibt s an (x,y); clear=n löscht n Zeichen links/rechts davon."""
        if clear:
            for i in range(x - clear, x + len(s) + clear):
                if 0 <= i < self.w and 0 <= y < self.h:
                    self.g[y][i] = " "
        for i, ch in enumerate(s):
            if 0 <= x + i < self.w and 0 <= y < self.h:
                self.g[y][x + i] = ch

    def box(self, x0, y0, x1, y1):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if 0 <= x < self.w and 0 <= y < self.h:
                    self.g[y][x] = " "

    def fill(self, x0, y0, x1, y1, fn):
        """fn(x,y) -> Zeichen oder None."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < self.w and 0 <= y < self.h:
                    ch = fn(x, y)
                    if ch:
                        self.g[y][x] = ch

    def line(self, pts, ch=None, clear=0):
        """Verbindet Punkte; ch=None wählt / \\ - | automatisch."""
        cells = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0), 1)
            dx, dy = x1 - x0, y1 - y0
            if ch is not None:
                c = ch
            elif dy == 0:
                c = "-"
            elif dx == 0:
                c = "|"
            elif (dx > 0) == (dy > 0):
                c = "\\"
            else:
                c = "/"
            for i in range(n + 1):
                x = round(x0 + dx * i / n)
                y = round(y0 + dy * i / n)
                cells.append((x, y, c))
        if clear:
            for x, y, _ in cells:
                self.box(x - clear, y, x + clear, y)
        for x, y, c in cells:
            self.put(x, y, c)

    def render(self):
        return "\n".join("".join(r).rstrip() for r in self.g)


# ---------------------------------------------------------------- Muster
def ocean(x, y):
    return "~" if (x + 3 * y) % 6 in (0, 1) else " "


def coast(x, y):
    return "~" if (x * 5) % 7 in (0, 3) else " "


def forest_dense(x, y):
    return "#" if (x + 2 * y) % 4 == 0 else None


def forest_light(x, y):
    return "#" if (x + 3 * y) % 8 == 0 else None


def jungle(x, y):
    return "#" if (x + 2 * y) % 3 == 0 else None


def ellipse_mountain(cx, cy, rx, ry):
    """Berg als Ellipse; dichter zur Mitte (zum Gipfel) hin."""
    def fn(x, y):
        d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
        if d > 1:
            return None
        if d < 0.35:
            return "^" if (x + 2 * y) % 2 == 0 else None
        return "^" if (x + 2 * y) % 4 == 0 else None
    return fn


# ---------------------------------------------------------------- Band 1
B1W = 90  # Breite des Band-1-Teils
H = 54    # Höhe der Karte


def draw_ocean(c, w):
    c.fill(0, 0, w - 1, 4, ocean)
    c.fill(0, 5, w - 1, 5, coast)  # Küstenlinie
    t = "   O Z E A N   "
    c.put((w - len(t)) // 2, 2, t, clear=1)
    t = "  (östliche und westliche Begrenzung unbekannt)  "
    c.put(max(2, (w - len(t)) // 2 - 22), 1, t)
    t = "  jenseits des Ozeans: Smaragdminen  "
    c.put(w - len(t) - 1, 1, t)


def draw_band1(c, ox, oy, west_note=True):
    """Ellens Karte: Nabenberg, Last Hope, Proxima, Alpha, Cygnis, Pavonis, Leporis."""
    W = B1W

    # Wald im Nordosten (Laubwald zwischen Proxima und Alpha, Nadelwald östlich von Alpha)
    c.fill(ox + 20, oy + 7, ox + 45, oy + 21, forest_light)
    c.fill(ox + 32, oy + 6, ox + 45, oy + 14, forest_dense)
    c.fill(ox + 46, oy + 6, ox + W - 1, oy + 28, forest_dense)
    c.put(ox + 24, oy + 16, " Laubwald ", clear=1)
    c.put(ox + 21, oy + 17, " (wilde Tiere, Wölfe) ", clear=1)
    c.put(ox + 70, oy + 16, " dunkler Nadelwald ", clear=1)

    # Pavonis an der Küste (Blaudorf, nach Band 1 nur noch Krater)
    c.box(ox + 50, oy + 6, ox + 72, oy + 8)
    c.put(ox + 52, oy + 6, "[x] PAVONIS")
    c.put(ox + 52, oy + 7, "(Blaudorf, gefallen:")
    c.put(ox + 52, oy + 8, " Weltstein-Krater)")
    c.put(ox + 77, oy + 6, "--> Arae", clear=1)
    c.put(ox + 75, oy + 7, "(weit entfernt)", clear=1)

    # Fluss: von Cygnis nordwestwärts zum Meer, Mündung westlich von Pavonis
    c.line([(ox + 46, oy + 6), (ox + 49, oy + 10), (ox + 53, oy + 14), (ox + 57, oy + 18)], clear=1)
    c.put(ox + 39, oy + 10, " Fluss ", clear=1)

    # Cygnis (Waldsiedlung, Hütten zwischen Bäumen, Mutterbaum)
    c.line([(ox + 57, oy + 18), (ox + 54, oy + 21)], clear=1)  # Bach
    c.put(ox + 49, oy + 20, "Bach", clear=1)
    c.box(ox + 58, oy + 18, ox + 84, oy + 20)
    c.put(ox + 59, oy + 19, "* CYGNIS (Hütten im Wald,")
    c.put(ox + 61, oy + 20, "Mutterbaum)")

    # Alpha
    c.line([(ox + 50, oy + 22), (ox + 53, oy + 21)], ".")  # Trampelpfad bis zum Bach
    c.box(ox + 39, oy + 22, ox + 49, oy + 24)
    c.put(ox + 40, oy + 22, "[*] ALPHA")
    c.put(ox + 40, oy + 23, "(Osttor)")

    # Proxima
    c.box(ox + 22, oy + 22, ox + 33, oy + 23)
    c.put(ox + 23, oy + 22, "* PROXIMA")

    # Last Hope am Nordwestfuß des Nabenbergs
    c.box(ox + 0, oy + 22, ox + 19, oy + 24)
    c.put(ox + 1, oy + 22, "[*] LAST HOPE")
    c.put(ox + 1, oy + 23, "(Westtor--Osttor,")
    c.put(ox + 1, oy + 24, " Lindenbibliothek)")

    # Hauptweg: Last Hope = Proxima = Alpha = ... (nördlich am Berg vorbei)
    c.put(ox + 14, oy + 22, "=========")
    c.put(ox + 32, oy + 22, "========")
    c.put(ox + 50, oy + 23, "== = = = =", clear=1)
    c.put(ox + 61, oy + 23, "entfernte kleinere Dörfer -->", clear=1)

    # Nabenberg (Ellipse, dichter zum Gipfel hin)
    cx, cy = ox + 28, oy + 38
    c.fill(cx - 19, cy - 11, cx + 19, cy + 11, ellipse_mountain(cx, cy, 19, 11))
    c.put(cx - 2, cy - 2, " /\\ ", clear=1)
    c.put(cx - 3, cy - 1, " NABE ", clear=1)
    c.put(cx - 9, cy + 3, " N A B E N B E R G ", clear=1)
    c.put(cx - 12, cy - 6, " BLAUTAL ", clear=1)
    c.put(cx - 14, cy - 5, " (Xenophob) ", clear=1)
    c.put(cx + 6, cy - 1, " ROTTAL ", clear=1)
    c.put(cx + 5, cy, " (lyssenko) ", clear=1)
    c.put(cx - 12, cy + 6, " GRÜNTAL ", clear=1)
    c.put(cx - 13, cy + 7, " (Thürstön) ", clear=1)
    c.line([(ox + 15, oy + 25), (ox + 18, oy + 28)])  # Abstieg Last Hope -> Berg
    c.put(ox + 17, oy + 25, "Abstieg")

    # Eine Handvoll namenloser, Alpha-großer Dörfer rund um den Berg
    c.put(ox + 4, oy + 36, "*", clear=1)
    c.put(ox + 3, oy + 46, "*", clear=1)
    c.put(ox + 56, oy + 36, "*", clear=1)
    c.put(ox + 40, oy + 50, "*", clear=1)

    # Leporis, Arneb, Nihal im tiefen Südosten
    c.put(ox + 70, oy + 44, "[*] LEPORIS")      # Stern in Spalte ox+71
    c.put(ox + 70, oy + 45, "(am ehesten")
    c.put(ox + 70, oy + 46, " eine Stadt)")
    c.put(ox + 71, oy + 47, "|")                 # direkt unter dem Stern
    c.put(ox + 60, oy + 48, "* Arneb -- + -- * Nihal")  # Knoten "+" in Spalte ox+71

    # Rand-Notizen
    c.put(ox + 24, oy + 52, "fern im Süden: ein Land mit Straßen aus Gold (MAGNUS' Erzählung)")
    if west_note:
        c.put(ox + 1, oy + 49, "<-- weit im Westen:")
        c.put(ox + 1, oy + 50, "    Urwald um Luyten")
        c.put(ox + 1, oy + 51, "    (jenseits der Karte)")


# ---------------------------------------------------------------- Band 2
B2W = 60  # Breite des Band-2-Teils (westlich von Last Hope)


def draw_band2(c, ox, oy):
    """MAGNUS' Karte: Ebene, Luhman, Wolf, Lalande, Majoris, Ross, Ran, Aquarii,
    Urwald, Elfenberge, Luyten.  Last Hope beginnt bei ox + B2W."""
    lh = ox + B2W  # Spalte, an der Last Hopes Kasten beginnt

    # Urwald der Elfenberge (Westen)
    c.fill(ox + 0, oy + 7, ox + 19, oy + 51, jungle)
    # Elfenberge im Urwald
    ex, ey = ox + 9, oy + 20
    c.fill(ex - 8, ey - 8, ex + 8, ey + 8, ellipse_mountain(ex, ey, 8, 8))
    c.put(ex - 2, ey - 6, " /\\ ", clear=1)
    c.put(ex - 4, ey - 5, " Schnee ", clear=1)
    c.put(ex - 6, ey - 4, " Einsiedler ", clear=1)
    c.put(ex - 6, ey - 3, " (Atrokius) ", clear=1)
    c.put(ex - 7, ey, " ELFENBERGE ", clear=1)
    c.put(ex - 4, ey + 2, " w w w ", clear=1)
    c.put(ex - 4, ey + 3, " Wölfe ", clear=1)
    c.put(ex - 3, ey + 5, " ~~ ", clear=1)
    c.put(ex - 5, ey + 6, " Waldsee ", clear=1)
    c.put(ox + 3, oy + 9, " x Elfendorf ", clear=1)
    c.put(ox + 3, oy + 10, " (überfallen) ", clear=1)
    c.put(ox + 3, oy + 32, " U R W A L D ", clear=1)
    c.put(ox + 4, oy + 36, " x LUYTEN ", clear=1)
    c.put(ox + 3, oy + 37, " (zerstört) ", clear=1)
    c.put(ox + 3, oy + 46, " Elfenwald ", clear=1)

    # Wolfsspur (Spur der Verwüstung, ostwärts)
    c.put(ox + 13, oy + 39, "w", clear=1)
    c.put(ox + 16, oy + 35, "w", clear=1)
    c.put(ox + 18, oy + 30, "w", clear=1)

    # Ebene westlich von Last Hope (weitgehend vegetationslos, im Winter verschneit)
    c.put(ox + 34, oy + 31, "  E B E N E  ", clear=1)
    c.put(ox + 21, oy + 32, "  (kaum Vegetation, im Winter verschneit)  ", clear=1)

    # Weg Last Hope -> Aquarii (Band 2), Dörfer abwechselnd über/unter dem Weg
    y = oy + 22
    c.put(ox + 31, y, "=" * (lh - (ox + 31)), clear=0)
    c.put(lh, y, "=")  # Anschluss an "[*] LAST HOPE"

    # Aquarii am Waldrand
    c.box(ox + 19, y, ox + 30, y + 2)
    c.put(ox + 20, y, "[*] AQUARII")
    c.put(ox + 20, y + 1, "(Eukalyptus-")
    c.put(ox + 20, y + 2, " halle)")

    def stop(x, name, above, extra=None):
        """Knoten + auf dem Weg bei x; der Stern des Namens steht genau darüber/darunter."""
        off = name.index("*")  # Position des Sterns im Namen
        c.put(x, y, "+")
        if above:
            c.put(x, y - 1, "|")
            c.put(x - off, y - 2, name, clear=1)
            if extra:
                c.put(x - off, y - 3, extra, clear=1)
        else:
            c.put(x, y + 1, "|")
            c.put(x - off, y + 2, name, clear=1)
            if extra:
                c.put(x - off, y + 3, extra, clear=1)

    stop(ox + 34, "* Ran", above=True)
    stop(ox + 40, "[*] MAJORIS", above=False, extra="(Tempel der Liebe)")
    stop(ox + 47, "* Lalande", above=True)
    stop(ox + 52, "* Wolf", above=False)
    stop(ox + 57, "** Luhman", above=True, extra="(Doppeldorf)")

    # Ross: Gründorf abseits, wird in großem Bogen umgangen
    c.put(ox + 30, oy + 28, "[*] ROSS (Gründorf,", clear=1)
    c.put(ox + 30, oy + 29, " wird umgangen)", clear=1)


LEGEND = """\
LEGENDE
  ~ ~ ~   Ozean, Küste, See                 [*]  Dorf oder Stadt mit Mauern
  ^ ^ ^   Gebirge (dichter = höher)          *   Dorf, Siedlung (offen)
  # # #   Wald (Laub-, Nadel-, Urwald)       x   Ruine, Krater
  = = =   Hauptweg der Handlung              .   Trampelpfad
  / \\     Fluss, Bach, Abstieg               w   Wölfe (Band 2)
  | +     Anschluss eines Ortes an den Weg
  /\\      Berggipfel                         N   Norden ist oben

  Unbeschriftete Sterne: die »Handvoll Alpha-großer Dörfer« rund um den Berg (im Roman namenlos).
  Blautal, Grüntal, Rottal: die drei Talstädte, tausende Häuser hoch in den Nabenberg gekerbt.
  Maßstab: keiner. Die Welt ist unendlich groß und flach; Entfernungen sind Fußmärsche von Tagen.
"""

NOTES_1 = """\
HINWEISE ZUR KARTE
  * Grundlage ist Ellens Landkarte (Kapitel »You Walk Away«): Last Hope, Proxima und Alpha liegen auf
    einer Linie, die nördlich am Nabenberg vorbeiführt; im Norden der Ozean, im tiefen Südosten Leporis
    mit Arneb und Nihal; Cygnis nordöstlich von Alpha; Pavonis nahe der nördlichen Kartengrenze am Meer.
  * Die Lage der drei Täler rund um die Nabe wird im Roman nicht beschrieben. Hier zeigt Blautal nach
    Nordwesten (Fnbsrds Abstieg nach Last Hope), Grüntal nach Südwesten, Rottal nach Osten.
  * Arae ist nur »weit entfernt«; die Richtung ist frei gewählt.
  * Pavonis ist im Zustand nach Band 1 eingezeichnet (Weltstein-Krater). Zu Beginn: ein Blaudorf mit
    Betonmauern am Meer, Westtor, sternförmigen Wegen und sieben Springbrunnen.
"""

NOTES_12 = NOTES_1 + """\
  * Westteil nach MAGNUS' Landkarte (Kapitel »Frozen Winter Moonlight«): Luhman, Wolf, Lalande, Majoris,
    Ross (umgangen), Ran, Aquarii; westlich von Aquarii der große Urwald und die Elfenberge.
  * Luyten liegt »weit im Westen, jenseits der Kartengrenze des vorherigen Abenteuers« im Urwald der
    Elfenberge; die genaue Lage ist frei gewählt. Auf welcher Seite des Weges Ross liegt, ebenfalls.
  * Elfendorf, Waldsee und Wolfsspur stammen aus dem angefangenen Text bzw. den Notizen zu Band 2.
"""


def frame(canvas, title, subtitle):
    body = canvas.render().split("\n")
    w = canvas.w
    out = []
    out.append("+" + "-" * (w + 2) + "+")
    out.append("| " + title.ljust(w) + " |")
    out.append("| " + subtitle.ljust(w) + " |")
    out.append("+" + "-" * (w + 2) + "+")
    for r in body:
        out.append("| " + r.ljust(w) + " |")
    out.append("+" + "-" * (w + 2) + "+")
    return "\n".join(out)


def compass(c, x, y):
    c.put(x, y, "  N  ")
    c.put(x, y + 1, "  |  ")
    c.put(x, y + 2, "W-+-O")
    c.put(x, y + 3, "  |  ")
    c.put(x, y + 4, "  S  ")


def build_band1():
    c = Canvas(B1W, H)
    draw_ocean(c, B1W)
    draw_band1(c, 0, 0, west_note=True)
    compass(c, 3, 9)
    return "\n".join([
        frame(c, "DIE WELT  --  Fnbsrd: Der Hilferuf des Drachen (Band 1)",
              "nach Ellens Landkarte  --  Norden ist oben"),
        "", LEGEND, NOTES_1])


def build_band12():
    c = Canvas(B2W + B1W, H)
    draw_ocean(c, B2W + B1W)
    draw_band1(c, B2W, 0, west_note=False)
    draw_band2(c, 0, 0)
    compass(c, B2W + 3, 9)
    return "\n".join([
        frame(c, "DIE WELT  --  Fnbsrd, Band 1 (Der Hilferuf des Drachen) und Band 2 (Die Rache der Wölfe, in Arbeit)",
              "nach Ellens Landkarte (Band 1) und MAGNUS' Landkarte (Band 2)  --  Norden ist oben"),
        "", LEGEND, NOTES_12])


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "1"
    print(build_band12() if which == "12" else build_band1())
