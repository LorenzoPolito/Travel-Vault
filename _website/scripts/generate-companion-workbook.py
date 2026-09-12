#!/usr/bin/env python3
"""
Genera il workbook Excel "companion" per il viaggio Giappone 2026 (23 ott - 6 nov).

Approccio "expression-first":
  - il foglio CONFIG e' l'unica fonte di verita' (date, tasso, persone, liste, budget)
  - tutte le celle derivate sono formule che usano Defined Names
  - le liste a tendina puntano ai Defined Names del CONFIG
  - per estendere il workbook basta aggiungere righe/valori, non riscrivere formule

Output: _website/public/downloads/Giappone-2026-Companion.xlsx

Dipendenze: openpyxl, Pillow
    python -m pip install openpyxl Pillow

Uso:
    python _website/scripts/generate-companion-workbook.py
"""

from __future__ import annotations

import math
import os
import random
import tempfile
from datetime import date

from PIL import Image, ImageDraw, ImageFilter

from openpyxl import Workbook
from openpyxl.chart import BarChart, DoughnutChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.marker import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.image import Image as XLImage
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

# --------------------------------------------------------------------------- #
# Palette / tema "sakura"
# --------------------------------------------------------------------------- #
C_SAKURA_DEEP = "A6285A"
C_SAKURA = "D94F79"
C_SAKURA_MID = "EC6A8B"
C_SAKURA_LIGHT = "F6A5C0"
C_SAKURA_PALE = "FCE4EC"
C_SAKURA_BLOSSOM = "FFF5F8"
C_INK = "4A2B3A"
C_INK_SOFT = "8A6572"
C_LEAF = "7BA05B"
C_GOLD = "C9A227"
C_WHITE = "FFFFFF"
C_BORDER = "F0C4D4"
C_GRAY = "F7F2F4"

SAKURA_PALETTE = ["D94F79", "EC6A8B", "F6A5C0", "F8BBD0", "C9A227",
                  "7BA05B", "B39DDB", "80CBC4", "FFAB91", "BCAAA4", "FCE4EC"]

CJU = Font(name="Yu Gothic", color=C_INK, size=11)
FONT_BODY = Font(name="Yu Gothic", size=11, color=C_INK)
FONT_BOLD = Font(name="Yu Gothic", size=11, color=C_INK, bold=True)
FONT_SMALL = Font(name="Yu Gothic", size=9, color=C_INK_SOFT)
FONT_TITLE = Font(name="Yu Mincho", size=22, color=C_SAKURA_DEEP, bold=True)
FONT_SUB = Font(name="Yu Gothic", size=11, color=C_INK_SOFT, italic=True)
FONT_SECTION = Font(name="Yu Mincho", size=13, color=C_WHITE, bold=True)
FONT_HEADER = Font(name="Yu Gothic", size=10, color=C_WHITE, bold=True)
FONT_KPI = Font(name="Yu Mincho", size=18, color=C_SAKURA_DEEP, bold=True)
FONT_FORMULA = Font(name="Yu Gothic", size=10, color=C_INK)

NUM_EUR = '#,##0.00" €"'
NUM_EUR0 = '#,##0" €"'
NUM_JPY = '#,##0" ¥"'
NUM_PCT = '0.0%'
NUM_DATE = "dd/mm/yyyy"
NUM_DATE_LONG = "ddd dd mmm"
NUM_ZERO_HIDDEN = '#,##0.00" €";-#,##0.00" €";""'

THIN = Side(style="thin", color=C_BORDER)
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
FILL_HEADER = PatternFill("solid", fgColor=C_SAKURA)
FILL_SECTION = PatternFill("solid", fgColor=C_SAKURA_DEEP)
FILL_PALE = PatternFill("solid", fgColor=C_SAKURA_PALE)
FILL_PALE2 = PatternFill("solid", fgColor=C_GRAY)
FILL_BLOSSOM = PatternFill("solid", fgColor=C_SAKURA_BLOSSOM)
FILL_TOTAL = PatternFill("solid", fgColor=C_SAKURA_LIGHT)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")


def eur(value: float) -> float:
    return round(float(value), 2)


def add_name(wb, name: str, ref: str) -> None:
    wb.defined_names.add(DefinedName(name, attr_text=ref))


def style_title(ws, last_col: str, text: str, subtitle: str | None = None) -> None:
    ws.merge_cells(f"A1:{last_col}1")
    c = ws["A1"]
    c.value = text
    c.font = FONT_TITLE
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    c.fill = PatternFill("solid", fgColor=C_SAKURA_BLOSSOM)
    ws.row_dimensions[1].height = 38
    if subtitle:
        ws.merge_cells(f"A2:{last_col}2")
        s = ws["A2"]
        s.value = subtitle
        s.font = FONT_SUB
        s.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        s.fill = PatternFill("solid", fgColor=C_SAKURA_BLOSSOM)
        ws.row_dimensions[2].height = 18


def style_section(ws, row: int, last_col: str, text: str) -> None:
    ws.merge_cells(f"A{row}:{last_col}{row}")
    c = ws.cell(row=row, column=1, value="  " + text)
    c.font = FONT_SECTION
    c.fill = FILL_SECTION
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 22


def style_header_row(ws, row: int, headers: list[str], start_col: int = 1) -> None:
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + i, value=h)
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_CENTER
        c.border = BORDER
    ws.row_dimensions[row].height = 30


def set_widths(ws, widths: dict[int, float]) -> None:
    for col, w in widths.items():
        ws.column_dimensions[get_column_letter(col)].width = w


def format_range(ws, cell_range, fmt=None, font=None, align=None, border=True, fill=None):
    for row in ws[cell_range]:
        for c in row:
            if fmt:
                c.number_format = fmt
            if font:
                c.font = font
            if align:
                c.alignment = align
            if border:
                c.border = BORDER
            if fill:
                c.fill = fill


# --------------------------------------------------------------------------- #
# Immagini sakura generate proceduralmente
# --------------------------------------------------------------------------- #
def _lerp(c1, c2, t):
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * t)) for i in range(3))


def _vgradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=_lerp(top, bottom, y / max(1, h - 1)))
    return img


def _petal_points(cx, cy, r, ang, width_factor=0.55, n=36):
    pts = []
    for i in range(n + 1):
        s = i / n
        d = r * s
        wd = r * width_factor * (math.sin(math.pi * s) ** 0.75)
        pts.append((cx + d * math.cos(ang) - wd * math.sin(ang),
                    cy + d * math.sin(ang) + wd * math.cos(ang)))
    for i in range(n, -1, -1):
        s = i / n
        d = r * s
        wd = r * width_factor * (math.sin(math.pi * s) ** 0.75)
        pts.append((cx + d * math.cos(ang) + wd * math.sin(ang),
                    cy + d * math.sin(ang) - wd * math.cos(ang)))
    return pts


def _draw_blossom(d, cx, cy, r, tone):
    base = _lerp((236, 106, 139), (255, 246, 250), 0.15 + 0.35 * tone)
    tip = _lerp((255, 214, 228), (255, 255, 255), 0.3 + 0.5 * tone)
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5 + random.uniform(-0.05, 0.05)
        col = _lerp(base, tip, random.uniform(0.15, 0.85))
        d.polygon(_petal_points(cx, cy, r, ang), fill=col)
    d.ellipse([cx - r * 0.16, cy - r * 0.16, cx + r * 0.16, cy + r * 0.16],
              fill=(240, 200, 120))


def _draw_falling_petal(d, cx, cy, r, color):
    ang = random.uniform(0, math.pi * 2)
    d.polygon(_petal_points(cx, cy, r, ang, width_factor=0.6, n=18), fill=color)


def _branch(d, pts, width, color):
    for i in range(len(pts) - 1):
        w = max(1, int(width * (1 - i / max(1, len(pts) - 1))))
        d.line([pts[i], pts[i + 1]], fill=color, width=w)
        if i % 2 == 0:
            d.ellipse([pts[i][0] - w / 2, pts[i][1] - w / 2,
                       pts[i][0] + w / 2, pts[i][1] + w / 2], fill=color)


def generate_images(outdir: str) -> dict:
    os.makedirs(outdir, exist_ok=True)
    random.seed(20261023)
    paths = {}

    scale = 2
    # ---------------- Banner (header dashboard) ----------------
    W, H = 1800, 200
    img = _vgradient(W * scale, H * scale, (255, 247, 250), (250, 214, 229)).convert("RGBA")

    # macchie acquerello
    blobs = Image.new("RGBA", (W * scale, H * scale), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blobs)
    for _ in range(70):
        x = random.uniform(0, W * scale)
        y = random.uniform(0, H * scale)
        rr = random.uniform(40, 180) * scale
        col = random.choice([(246, 165, 192, 55), (252, 228, 236, 70), (217, 79, 121, 30)])
        bd.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col)
    blobs = blobs.filter(ImageFilter.GaussianBlur(38 * scale))
    img = Image.alpha_composite(img, blobs)

    draw = ImageDraw.Draw(img)
    branch_pts = [(0.00 * W * scale, 0.55 * H * scale), (0.12 * W * scale, 0.62 * H * scale),
                  (0.26 * W * scale, 0.48 * H * scale), (0.40 * W * scale, 0.62 * H * scale)]
    _branch(draw, branch_pts, 12 * scale, (150, 106, 92))
    branch_pts2 = [(1.00 * W * scale, 0.45 * H * scale), (0.86 * W * scale, 0.58 * H * scale),
                   (0.72 * W * scale, 0.44 * H * scale), (0.60 * W * scale, 0.58 * H * scale)]
    _branch(draw, branch_pts2, 11 * scale, (150, 106, 92))

    for bx, by in branch_pts + branch_pts2:
        for _ in range(random.randint(1, 2)):
            ox = bx + random.uniform(-38, 38) * scale
            oy = by + random.uniform(-30, 30) * scale
            _draw_blossom(draw, ox, oy, random.uniform(20, 36) * scale, random.random())

    for _ in range(150):
        x = random.uniform(0, W * scale)
        y = random.uniform(0, H * scale)
        col = random.choice([(255, 214, 228, 235), (246, 165, 192, 235),
                             (255, 255, 255, 235), (236, 106, 139, 220)])
        _draw_falling_petal(draw, x, y, random.uniform(5, 13) * scale, col)

    img = img.resize((W, H), Image.LANCZOS)
    paths["banner"] = os.path.join(outdir, "banner.png")
    img.save(paths["banner"])


    # ---------------- Fiore / cluster ----------------
    W3, H3 = 360, 360
    blossom = Image.new("RGBA", (W3 * scale, H3 * scale), (0, 0, 0, 0))
    bl = ImageDraw.Draw(blossom)
    _branch(bl, [(20 * scale, 330 * scale), (120 * scale, 240 * scale),
                 (210 * scale, 160 * scale)], 9 * scale, (150, 106, 92))
    for (bx, by, rr) in [(120, 240, 46), (215, 150, 56), (160, 180, 34),
                         (250, 200, 30), (90, 280, 26)]:
        _draw_blossom(bl, bx * scale, by * scale, rr * scale, random.random())
    for _ in range(40):
        _draw_falling_petal(bl, random.uniform(0, W3) * scale,
                            random.uniform(0, H3) * scale,
                            random.uniform(5, 12) * scale,
                            random.choice([(255, 214, 228, 245), (246, 165, 192, 245),
                                           (236, 106, 139, 235)]))
    blossom = blossom.resize((W3, H3), Image.LANCZOS)
    paths["blossom"] = os.path.join(outdir, "blossom.png")
    blossom.save(paths["blossom"])

    return paths


# --------------------------------------------------------------------------- #
# Dati di partenza (fonte: itinerario + Info/Japan + Locations/Japan)
# --------------------------------------------------------------------------- #
ITINERARIO = [
    # giorno, data, base, titolo, difficolta, cibo, trasporti, ingressi, attivita, stato, note
    (1, date(2026, 10, 23), "Roma → KIX", "Partenza & Arrivo KIX (Izumisano)", 1, 15, 10, 0,
     "Volo MU788 (FCO→PVG) + FM3051 (PVG→KIX) · arrivo 21:00 · Nankai → Izumisano · KURA Hotel",
     "Prenotato", "Volo notturno, scalo Shanghai 2h45 · pasto speciale Rebecca"),
    (2, date(2026, 10, 25), "Osaka", "Trasferimento a Osaka · Shinsaibashi & Dotonbori", 2, 25, 14, 0,
     "Nankai Izumisano→Namba · Shinsaibashi shopping · Tempio Hozen-ji · Dotonbori illuminato",
     "Da pianificare", "Piano B pioggia: Namba Walk coperto"),
    (3, date(2026, 10, 26), "Osaka", "Osaka: Cultura & Quartieri", 3, 30, 8, 8,
     "Castello di Osaka · Shitenno-ji · Shinsekai · Tsutenkaku (opz.) · Nipponbashi Den Den Town ⭐Lorenzo",
     "Da pianificare", "Umeda rimosso: giornata tranquilla in zona Minami"),
    (4, date(2026, 10, 27), "Osaka", "Universal Studios Japan", 4, 25, 5, 88,
     "USJ: Super Nintendo World · Harry Potter · Minion/Jurassic · voucher pasto incluso",
     "Prenotato", "Biglietto 88 €/pax (05/09) · portare QR · Rebecca porta cibo da casa"),
    (5, date(2026, 10, 28), "Hiroshima + Miyajima", "Hiroshima + Miyajima", 4, 25, 0, 5,
     "Attivazione JR Pass · Shinkansen Sakura → Hiroshima · traghetto Miyajima · Itsukushima · Museo della Pace",
     "Da pianificare", "Sveglia 05:15 · attivare JR Kansai-Hiroshima (28/09!) · maree Miyajima"),
    (6, date(2026, 10, 29), "Nara → Kyoto", "Nara + Arrivo Kyoto", 3, 30, 7, 10,
     "Check-out Osaka · Takkyubin valigie → Tokyo · Kintetsu Nara · Todaiji · Fushimi Inari sera",
     "Da pianificare", "Bagagli spediti (consegna 1 nov) · solo bagaglio a mano"),
    (7, date(2026, 10, 30), "Kyoto", "Kyoto: Higashiyama & Gion", 4, 30, 8, 6,
     "Sannenzaka/Ninenzaka · Kodai-ji · Yasaka · Gion · Kiyomizu-dera al tramonto ~17:15",
     "Da pianificare", "Ultimo ingresso Kiyomizu ~17:30"),
    (8, date(2026, 10, 31), "Kyoto", "Kyoto: Templi del Nord + Uzumasa + Halloween", 3, 30, 8, 20,
     "Kinkaku-ji · Ryoan-ji · Uzumasa Kyoto Village (EVA, ultimo ingresso 17:15) · Halloween a Gion",
     "Parziale", "Uzumasa ¥2.800 · alternativa EN Tea Ceremony"),
    (9, date(2026, 11, 1), "Kyoto → Tokyo", "Kyoto→Tokyo via Shinkansen", 2, 25, 86, 13,
     "Shinkansen Hikari (¥13.650) · arrivo Tokyo · Skytree al tramonto · Solamachi",
     "Da pianificare", "Prenotare posto riservato dal 1 ott (SmartEX)"),
    (10, date(2026, 11, 2), "Tokyo", "Tokyo: Asakusa → Akihabara", 4, 30, 10, 0,
     "Senso-ji mattina · Nakamise · Akihabara pieno (arcade, Super Potato, Mandarake) · Ameyoko",
     "Da pianificare", "Giorni coperti: pioggia ok"),
    (11, date(2026, 11, 3), "Tokyo", "Sanrio Puroland + Ikebukuro", 3, 35, 12, 25,
     "Sanrio Puroland (Day Passport, indoor) · Sunshine City / Pokémon Center MEGA · Animate Ikebukuro",
     "Prenotato", "Sanrio ✅ 09/09 (~19,97 €) · 3 nov = Bunka no Hi"),
    (12, date(2026, 11, 4), "Tokyo", "Tokyo: Meiji → Nakano → Shinjuku → Shibuya", 3, 35, 10, 18,
     "Meiji · Harajuku · Nakano Broadway ⭐Lorenzo · Shinjuku · Shibuya Crossing · Shibuya Sky (opz.)",
     "Da pianificare", "Shibuya Sky ¥3.400 tramonto · prenotare 21/10"),
    (13, date(2026, 11, 5), "Tokyo", "Anniversario D&R · Lorenzo: nerd & Tokyo Tower", 2, 35, 12, 8,
     "D&R: programma a cura loro · Lorenzo: Akihabara deep dive · Tokyo Tower al tramonto",
     "Da pianificare", "Punto fisso: bagagli pronti entro 20:30"),
    (14, date(2026, 11, 6), "Tokyo → Roma", "Partenza da Tokyo (volo 08:40)", 1, 35, 5, 5,
     "Sveglia 04:30 · Keikyu Asakusa→HND · MU576 (HND→PVG) + MU787 (PVG→FCO) · arrivo 18:15",
     "Prenotato", "Pasto speciale Rebecca su entrambi i segmenti"),
    (15, date(2026, 11, 7), "Roma", "Rientro", 1, 15, 15, 0,
     "Giorno di recupero a casa — nessuna attivita' pianificata",
     "Da pianificare", "Arrivo FCO la sera del 6/11"),
]

ATTIVITA = [
    # giorno, data, citta, attivita, tipo, voto, costo_yen, stato, prenotazione, note
    (1, date(2026, 10, 24), "Izumisano (KIX)", "Nankai Airport Express KIX→Izumisano", "Trasporto", 3, 520, "Da fare", "", "~10 min"),
    (1, date(2026, 10, 24), "Izumisano (KIX)", "Check-in KURA Hotel Izumisano", "Alloggio", 4, 0, "Da fare", "Booking.com", "Self check-in · kitchenette"),
    (2, date(2026, 10, 25), "Osaka", "Nankai Main Line Izumisano→Namba", "Trasporto", 3, 610, "Da fare", "", "~34 min"),
    (2, date(2026, 10, 25), "Osaka", "Shinsaibashi-suji (shopping)", "Shopping", 4, 0, "Da fare", "", "Negozi ~10:30–20:30"),
    (2, date(2026, 10, 25), "Osaka", "Tempio Hozen-ji", "Tempio", 4, 0, "Da fare", "", "A 2 min da Dotonbori"),
    (2, date(2026, 10, 25), "Osaka", "Dotonbori (sera, illuminato)", "Quartiere", 5, 0, "Da fare", "", "Insegne al neon · street food"),
    (3, date(2026, 10, 26), "Osaka", "Castello di Osaka + giardini", "Castello", 4, 600, "Da fare", "in loco", "Apertura 9:00"),
    (3, date(2026, 10, 26), "Osaka", "Tempio Shitenno-ji", "Tempio", 4, 500, "Da fare", "in loco", "9:00–16:30"),
    (3, date(2026, 10, 26), "Osaka", "Shinsekai", "Quartiere", 4, 0, "Da fare", "", "Atmosfera retrò · kushikatsu"),
    (3, date(2026, 10, 26), "Osaka", "Torre Tsutenkaku", "Attività", 2, 900, "Opzionale", "in loco", ""),
    (3, date(2026, 10, 26), "Osaka", "Nipponbashi Den Den Town ⭐Lorenzo", "Shopping", 4, 0, "Da fare", "", "Osaka's Akihabara · ~2h45"),
    (4, date(2026, 10, 27), "Osaka", "USJ — Super Nintendo World", "Attività", 4, 0, "Da fare", "Klook", "Orario assegnato · incluso nel biglietto"),
    (4, date(2026, 10, 27), "Osaka", "USJ — Harry Potter", "Attività", 4, 0, "Da fare", "Klook", "Hogwarts Castle"),
    (4, date(2026, 10, 27), "Osaka", "USJ — Minion Park / Jurassic", "Attività", 3, 0, "Da fare", "Klook", "Voucher pasto incluso"),
    (5, date(2026, 10, 28), "Hiroshima / Miyajima", "Attivazione JR Kansai-Hiroshima Pass", "Trasporto", 5, 17000, "Da fare", "JR-WEST ONLINE", "Ritiro/attivazione 28 ott"),
    (5, date(2026, 10, 28), "Hiroshima / Miyajima", "Shinkansen Shin-Osaka→Hiroshima", "Trasporto", 3, 0, "Da fare", "", "Incluso nel pass · ~1h30"),
    (5, date(2026, 10, 28), "Hiroshima / Miyajima", "Traghetto JR → Miyajima", "Trasporto", 4, 0, "Da fare", "", "Incluso nel pass · tassa 100 ¥"),
    (5, date(2026, 10, 28), "Hiroshima / Miyajima", "Itsukushima Shrine (torii)", "Tempio", 5, 300, "Da fare", "in loco", "Verificare orari maree"),
    (5, date(2026, 10, 28), "Hiroshima / Miyajima", "Tempio Daisho-in", "Tempio", 3, 0, "Da fare", "", "8:00–17:00"),
    (5, date(2026, 10, 28), "Hiroshima / Miyajima", "Museo della Pace Hiroshima", "Museo", 4, 200, "Da fare", "Klook/Asoview", "Slot 30' · ~2h"),
    (5, date(2026, 10, 28), "Hiroshima / Miyajima", "Genbaku Dome / Peace Park", "Monumento", 5, 0, "Da fare", "", "UNESCO · gratuito"),
    (5, date(2026, 10, 28), "Hiroshima / Miyajima", "Hondori street", "Shopping", 3, 0, "Opzionale", "", "Momiji manju · uscire 17:30"),
    (6, date(2026, 10, 29), "Nara / Kyoto", "Takkyubin valigie Osaka→Tokyo", "Logistica", 4, 9480, "Da fare", "Yamato", "3 valigie · consegna 1 nov"),
    (6, date(2026, 10, 29), "Nara / Kyoto", "Kintetsu Namba→Nara", "Trasporto", 3, 570, "Da fare", "", "Non-JR · ~40 min"),
    (6, date(2026, 10, 29), "Nara / Kyoto", "Parco di Nara (cervi)", "Natura", 4, 0, "Da fare", "", "Shika senbei 150 ¥"),
    (6, date(2026, 10, 29), "Nara / Kyoto", "Tempio Todaiji (Gran Buddha)", "Tempio", 5, 800, "Da fare", "in loco", "Daibutsu 15 m"),
    (6, date(2026, 10, 29), "Nara / Kyoto", "Santuario Kasuga Taisha", "Tempio", 3, 0, "Da fare", "", "3.000 lanterne"),
    (6, date(2026, 10, 29), "Nara / Kyoto", "Fushimi Inari (sera)", "Tempio", 3, 0, "Da fare", "", "24h · JR 5 min dal pass"),
    (7, date(2026, 10, 30), "Kyoto", "Sannenzaka & Ninenzaka", "Quartiere", 4, 0, "Da fare", "", "Viuzze acciottolate"),
    (7, date(2026, 10, 30), "Kyoto", "Tempio Kodai-ji", "Tempio", 3, 600, "Da fare", "in loco", "9:00–17:00"),
    (7, date(2026, 10, 30), "Kyoto", "Nishiki Market", "Mercato", 4, 0, "Da fare", "", "Attenzione: alcuni negozi chiusi il mercoledì"),
    (7, date(2026, 10, 30), "Kyoto", "Santuario Yasaka", "Tempio", 4, 0, "Da fare", "", "24h · gratuito"),
    (7, date(2026, 10, 30), "Kyoto", "Quartiere Gion", "Quartiere", 2, 0, "Da fare", "", "Vietato vicoli privati (multa)"),
    (7, date(2026, 10, 30), "Kyoto", "Kiyomizu-dera al tramonto", "Tempio", 5, 500, "Da fare", "in loco", "Ultimo ingresso ~17:30"),
    (8, date(2026, 10, 31), "Kyoto", "Kinkaku-ji (Padiglione d'Oro)", "Tempio", 3, 500, "Da fare", "in loco", "9:00–17:00"),
    (8, date(2026, 10, 31), "Kyoto", "Ryoan-ji", "Tempio", 2, 600, "Opzionale", "in loco", "Giardino zen di rocce"),
    (8, date(2026, 10, 31), "Kyoto", "Uzumasa Kyoto Village + EVA", "Attività", 3, 2800, "Da fare", "ticket.eigamura.com", "EVA ultimo ingresso 17:15"),
    (8, date(2026, 10, 31), "Kyoto", "Halloween a Gion", "Evento", 3, 0, "Da fare", "", "Verificare eventi serali"),
    (9, date(2026, 11, 1), "Kyoto → Tokyo", "Shinkansen Hikari Kyoto→Tokyo", "Trasporto", 3, 13650, "Da fare", "SmartEX", "Posto riservato · ~2h40"),
    (9, date(2026, 11, 1), "Tokyo", "Tokyo Skytree al tramonto", "Attività", 3, 2300, "Da fare", "sito ufficiale", "Tramonto ~16:40"),
    (9, date(2026, 11, 1), "Tokyo", "Pokemon Center Skytree Town", "Shopping", 4, 0, "Da fare", "", "Solamachi"),
    (9, date(2026, 11, 1), "Tokyo", "Solamachi (cena + shopping)", "Shopping", 3, 0, "Da fare", "", "Food court"),
    (10, date(2026, 11, 2), "Tokyo", "Tempio Senso-ji", "Tempio", 5, 0, "Da fare", "", "6:30 · gratis · mattina presto"),
    (10, date(2026, 11, 2), "Tokyo", "Nakamise-dori", "Shopping", 3, 0, "Da fare", "", "Via shopping"),
    (10, date(2026, 11, 2), "Tokyo", "Akihabara", "Quartiere", 4, 0, "Da fare", "", "Elettronica, arcade, retrogame ⭐Lorenzo"),
    (10, date(2026, 11, 2), "Tokyo", "Ameyoko (Ueno)", "Mercato", 3, 0, "Da fare", "", "Street food"),
    (11, date(2026, 11, 3), "Tokyo", "Sanrio Puroland", "Attività", 4, 0, "Da fare", "e-Passport/Klook", "Indoor · riserva visita"),
    (11, date(2026, 11, 3), "Tokyo", "Sunshine City / Pokemon Center MEGA", "Shopping", 4, 0, "Da fare", "", "Il più grande"),
    (11, date(2026, 11, 3), "Tokyo", "Animate Ikebukuro", "Shopping", 4, 0, "Da fare", "", "Flagship anime · Otome Road"),
    (12, date(2026, 11, 4), "Tokyo", "Santuario Meiji", "Tempio", 3, 0, "Da fare", "", "10:00–16:30 · gratis"),
    (12, date(2026, 11, 4), "Tokyo", "Harajuku (Takeshita Street)", "Quartiere", 2, 0, "Da fare", "", "Moda kawaii"),
    (12, date(2026, 11, 4), "Tokyo", "Nakano Broadway ⭐Lorenzo", "Shopping", 5, 0, "Da fare", "", "Collezionismo vintage · Mandarake"),
    (12, date(2026, 11, 4), "Tokyo", "Shinjuku", "Quartiere", 4, 0, "Da fare", "", "Omoide Yokocho · osservatorio"),
    (12, date(2026, 11, 4), "Tokyo", "Shibuya Crossing", "Quartiere", 5, 0, "Da fare", "", "Attraversamento più famoso"),
    (12, date(2026, 11, 4), "Tokyo", "Shibuya Sky ⭐Rebecca", "Attività", 4, 3400, "Opzionale", "shibuya-sky.com", "Slot tramonto · prenotare 21/10"),
    (12, date(2026, 11, 4), "Tokyo", "Pokemon Center Shibuya", "Shopping", 5, 0, "Da fare", "", "Merch esclusivo · Nintendo Tokyo"),
    (13, date(2026, 11, 5), "Tokyo", "Akihabara deep dive", "Quartiere", 4, 0, "Da fare", "", "Improvvisazione ⭐Lorenzo"),
    (13, date(2026, 11, 5), "Tokyo", "Tokyo Tower al tramonto", "Attività", 4, 1500, "Opzionale", "cassa/online", "Tramonto ~16:40"),
    (14, date(2026, 11, 6), "Tokyo → Roma", "Keikyu Asakusa→HND", "Trasporto", 3, 600, "Da fare", "", "~50 min"),
    (14, date(2026, 11, 6), "Tokyo → Roma", "Volo MU576 + MU787 HND→FCO", "Trasporto", 5, 0, "Da fare", "China Eastern", "Partenza 08:40 · arrivo 18:15"),
]

PRENOTAZIONI = [
    # voce, categoria, evento, finestra, scadenza, canale, importo, valuta, per, stato, priorita, note
    ("Voli A/R China Eastern (open-jaw)", "Voli", "23 ott / 6 nov", "—", None,
     "China Eastern", 1096.33, "EUR", "A testa", "Pagato", "Alta",
     "FCO→KIX + HND→FCO · tot 3.289 € · ordine 09/08/26"),
    ("Alloggio KURA Hotel Izumisano", "Alloggio", "24–25 ott", "—", None,
     "Booking.com", 26.67, "EUR", "A testa", "Pagato", "Alta", "Self check-in · kitchenette"),
    ("Alloggio Hanazonocho Apartment 103 (Osaka)", "Alloggio", "25–29 ott", "—", None,
     "Booking.com / Airbnb", 74.33, "EUR", "A testa", "Pagato", "Alta", "Angolo cottura · metro 1 min"),
    ("Alloggio Miro Kyoto Nijo Hotel", "Alloggio", "29 ott–1 nov", "—", None,
     "Booking.com", 85.72, "EUR", "A testa", "Pagato", "Alta", "Cucina attrezzata · tel +81-50-5444-6620"),
    ("Alloggio Taito City Guesthouse (Tokyo)", "Alloggio", "1–6 nov", "—", None,
     "Booking.com", 173.17, "EUR", "A testa", "Pagato", "Alta", "Cucina condivisa 1° piano · confermare ricezione bagagli"),
    ("Universal Studios Japan (1-day + SNW + voucher)", "Ingressi/Attività", "27 ott", "—", None,
     "Klook / ufficiale", 88.25, "EUR", "A testa", "Prenotato", "Alta",
     "Acquistato 05/09 · portare QR · Express Pass non incluso"),
    ("Sanrio Puroland (Day Passport + riserva)", "Ingressi/Attività", "3 nov", "—", None,
     "e-Passport / Klook", 19.97, "EUR", "A testa", "Prenotato", "Alta",
     "Prenotato 09/09 · annotare n. conferma/orario · chiuso 4-5 nov"),
    ("Assicurazione sanitaria", "Assicurazione", "—", "—", None,
     "Heymondo (da confermare)", 53.43, "EUR", "A testa", "Prenotato", "Alta",
     "Annotare provider + n. polizza · copertura allergie Rebecca da verificare"),
    ("JR Kansai-Hiroshima Area Pass (5gg)", "Trasporti", "attivo 28 ott", "28 set 10:00 JST",
     date(2026, 9, 28), "JR-WEST ONLINE", 17000, "JPY", "A testa", "Da fare", "Alta",
     "Acquistare su JR-WEST ONLINE per prenotare i posti online · ritiro/attivazione 28 ott"),
    ("Posti riservati Shin-Osaka→Hiroshima", "Trasporti", "28 ott", "28 set 10:00 JST",
     date(2026, 9, 28), "JR-WEST Online", 0, "JPY", "A testa", "Da fare", "Alta",
     "Gratis con il pass · Sakura ~06:45"),
    ("Posti riservati Hiroshima→Shin-Osaka", "Trasporti", "28 ott", "28 set 10:00 JST",
     date(2026, 9, 28), "JR-WEST Online", 0, "JPY", "A testa", "Da fare", "Alta",
     "Gratis con il pass · ritorno ~18:15"),
    ("Kyoto→Tokyo Shinkansen Hikari (riservato)", "Trasporti", "1 nov", "1 ott 10:00 JST",
     date(2026, 10, 1), "SmartEX", 13650, "JPY", "A testa", "Da fare", "Alta",
     "Hayatoku 21 se entro 11 ott · ~2h40"),
    ("Tokyo Skytree", "Ingressi/Attività", "1 nov (dom)", "~2 ott 00:00 JST",
     date(2026, 10, 2), "sito ufficiale / Klook", 2300, "JPY", "A testa", "Da fare", "Media",
     "Weekend ~¥2.600 in loco · salita al tramonto ~16:40"),
    ("Uzumasa Kyoto Village (Evangelion / EVA)", "Ingressi/Attività", "31 ott", "vendita anticipata",
     None, "ticket.eigamura.com", 2800, "JPY", "A testa", "Da fare", "Media",
     "EVA ultimo ingresso 17:15 · entrare entro ~16:00"),
    ("Shibuya Sky ⭐ Rebecca", "Ingressi/Attività", "4 nov", "21 ott 00:00 JST",
     date(2026, 10, 21), "shibuya-sky.com / Webket", 3400, "JPY", "A testa", "Da fare", "Alta",
     "Slot tramonto (dalle 15:00) · prenotare subito all'apertura"),
    ("Museo della Pace Hiroshima (slot web)", "Ingressi/Attività", "28 ott", "90 gg (aperta)",
     None, "Klook / Asoview", 200, "JPY", "A testa", "Da fare", "Media",
     "Slot 30' · di giorno ok anche in cassa"),
    ("Tokyo Tower", "Ingressi/Attività", "5 nov", "nessuna",
     None, "cassa / online", 1500, "JPY", "A testa", "Da fare", "Bassa", "¥1.500 stesso prezzo"),
    ("Takkyubin valigie Osaka→Tokyo (3 valigie)", "Bagagli", "29 ott (consegna 1 nov)", "—",
     None, "Yamato Namba Station Center", 9480, "JPY", "Totale", "Da fare", "Alta",
     "¥3.160/valigia · confermare host Tokyo · non spedire valori/documenti"),
    ("eSIM Giappone", "eSIM", "pre-partenza", "~2 settimane prima",
     date(2026, 10, 14), "Klook / Airalo", 20.00, "EUR", "A testa", "Da fare", "Alta",
     "Attivare prima della partenza"),
    ("Pasto speciale Rebecca (China Eastern)", "Extra", "23 ott / 6 nov", "pre-partenza",
     None, "China Eastern", 0, "EUR", "A testa", "Da fare", "Alta",
     "No soia/pesce/crostacei/frutta secca · verificare entrambi i segmenti + scalo PVG"),
    ("Express Pass USJ (opzionale)", "Ingressi/Attività", "27 ott", "—",
     None, "Klook", 8000, "JPY", "A testa", "Opzionale", "Bassa", "Solo per saltare code 2h+"),
    ("EN Tea Ceremony (alternativa a Uzumasa)", "Ingressi/Attività", "31 ott", "—",
     None, "asoview / byFood / KKDay", 2500, "JPY", "A testa", "Opzionale", "Bassa",
     "Verificare operativita' (segnalazioni chiusura 2024)"),
    ("Cena anniversario Davide & Rebecca", "Cibo", "5 nov", "—",
     None, "a cura di Rebecca", 0, "EUR", "Totale", "Opzionale", "Bassa", "Ristorante Rebecca-safe"),
    ("Verifica maree Miyajima", "Extra", "27 ott", "giorno prima",
     date(2026, 10, 27), "—", 0, "EUR", "A testa", "Da fare", "Media",
     "Torii piu' scenico con alta marea · tassa visita 100 ¥"),
    ("Confermare host Tokyo ricezione bagagli", "Extra", "entro 29 ott", "—",
     date(2026, 10, 29), "—", 0, "EUR", "A testa", "Da fare", "Alta",
     "Private lodging puo' rifiutare la consegna differita"),
]

SPESE_PREFILL = [
    # data, categoria, descrizione, importo TOTALE, valuta, pagato_da, p1, p2, p3, note
    (date(2026, 8, 9), "Voli", "Volo A/R China Eastern (open-jaw)", 3288.99, "EUR",
     "", "X", "X", "X", "totale 3 pax · ordine 09/08/26"),
    (date(2026, 8, 9), "Alloggio", "KURA Hotel Izumisano (1 notte)", 80.01, "EUR",
     "", "X", "X", "X", "24–25 ott"),
    (date(2026, 8, 9), "Alloggio", "Hanazonocho Apartment 103 (4 notti)", 222.99, "EUR",
     "", "X", "X", "X", "25–29 ott"),
    (date(2026, 8, 9), "Alloggio", "Miro Kyoto Nijo Hotel (3 notti)", 257.16, "EUR",
     "", "X", "X", "X", "29 ott–1 nov"),
    (date(2026, 8, 9), "Alloggio", "Taito City Guesthouse (5 notti)", 519.51, "EUR",
     "", "X", "X", "X", "1–6 nov"),
    (date(2026, 9, 5), "Ingressi/Attività", "USJ 1-day + Super Nintendo World + voucher", 264.75, "EUR",
     "", "X", "X", "X", "27 ott"),
    (date(2026, 9, 9), "Ingressi/Attività", "Sanrio Puroland Day Passport", 59.91, "EUR",
     "", "X", "X", "X", "3 nov"),
    (date(2026, 9, 9), "Assicurazione", "Assicurazione sanitaria", 160.29, "EUR",
     "", "X", "X", "X", "Provider e polizza da annotare"),
]

SCADENZE = [
    (date(2026, 9, 28), "Acquisto JR Kansai-Hiroshima Pass + posti Shinkansen A/R", "Trasporti", "Alta",
     "28 set 10:00 JST · JR-WEST ONLINE · in Italia ~03:00"),
    (date(2026, 10, 1), "Prenotazione Kyoto→Tokyo Hikari (SmartEX)", "Trasporti", "Alta",
     "1 ott 10:00 JST · posto riservato ~¥13.650"),
    (date(2026, 10, 2), "Prenotazione Tokyo Skytree (1 nov)", "Attività", "Media", "~30 gg prima, 00:00 JST"),
    (date(2026, 10, 11), "Scadenza sconto Hayatoku 21 (Kyoto→Tokyo)", "Trasporti", "Media",
     "Entro l'11 ott per lo sconto"),
    (date(2026, 10, 14), "Comprare eSIM Giappone", "eSIM", "Alta", "~2 settimane prima (Klook/Airalo)"),
    (date(2026, 10, 21), "Prenotazione Shibuya Sky (4 nov, tramonto) ⭐Rebecca", "Attività", "Alta",
     "21 ott 00:00 JST · finestra 14 gg · ¥3.400"),
    (date(2026, 10, 23), "PARTENZA — Volo MU788 FCO→PVG 21:10", "Viaggio", "Alta", "Check-in FCO ~18:10"),
    (date(2026, 10, 27), "Verifica maree Miyajima", "Info", "Media", "Giorno prima di Hiroshima · tassa 100 ¥"),
    (date(2026, 10, 28), "Attivazione JR Pass + Hiroshima/Miyajima", "Viaggio", "Alta", "Sveglia 05:15 · ritirare pass"),
    (date(2026, 10, 29), "Takkyubin valigie Osaka→Tokyo (consegna 1 nov)", "Bagagli", "Alta",
     "Yamato Namba Station Center 9:00–20:00"),
    (date(2026, 11, 1), "Consegna bagagli a Tokyo + Kyoto→Tokyo", "Viaggio", "Alta", "Arrivo Tokyo · Skytree"),
    (date(2026, 11, 3), "Sanrio Puroland", "Attività", "Media", "Bunka no Hi · arrivare presto"),
    (date(2026, 11, 4), "Shibuya Sky (slot tramonto)", "Attività", "Media", "Prenotato il 21/10"),
    (date(2026, 11, 5), "Anniversario Davide & Rebecca", "Speciale", "Bassa", "Programma a cura loro"),
    (date(2026, 11, 6), "RITORNO — Volo MU576 HND→PVG 08:40", "Viaggio", "Alta", "Sveglia 04:30 · arrivo FCO 18:15"),
]

LOGISTICA_VOLI = [
    ("Andata", "FCO→KIX", "23 ott 21:10 → 24 ott 21:00", "MU788 + FM3051 (via Shanghai PVG)", "16h50"),
    ("Ritorno", "HND→FCO", "6 nov 08:40 → 18:15", "MU576 + MU787 (via Shanghai PVG)", "17h35"),
]
LOGISTICA_HOTEL = [
    ("Izumisano (KIX)", "KURA Hotel Izumisano", "24–25 ott", "1", "Uemachi 3-10-11, Izumisano",
     "16:00 / 10:00", "Kitchenette + microonde"),
    ("Osaka", "Hanazonocho Apartment 103", "25–29 ott", "4", "1-2-35 Bainan, Nishinari Ward",
     "16:00 / 10:00", "Angolo cottura"),
    ("Kyoto", "Miro Kyoto Nijo Hotel", "29 ott–1 nov", "3", "20-1 Nishinokyokangakuincho, Nakagyo",
     "16:00 / 10:00", "Cucina attrezzata"),
    ("Tokyo", "Taito City Guesthouse", "1–6 nov", "5", "4-27-6 Senzoku, Taito City",
     "15:00 / 10:00", "Cucina condivisa (1° piano)"),
]
LOGISTICA_EMERGENZE = [
    ("110", "Polizia", "Gratuito da qualsiasi telefono"),
    ("119", "Ambulanza / Vigili del Fuoco", "Gratuito da qualsiasi telefono"),
    ("118", "Guardia Costiera", "Emergenze in mare"),
    ("#7119", "Consulenza medica urgente 24h", "Operatori in inglese"),
    ("+81-3-3501-0110", "Ambasciata d'Italia a Tokyo", "2-11-3 Mita, Meguro-ku"),
    ("+81-6-6226-3100", "Consolato onorario Osaka", "—"),
]


def build_config(wb, img_paths):
    ws = wb.create_sheet("CONFIG")
    ws.sheet_properties.tabColor = C_SAKURA_DEEP
    set_widths(ws, {1: 30, 2: 26, 3: 4, 4: 20, 5: 4, 6: 20, 7: 4, 8: 18, 9: 4,
                    10: 16, 11: 4, 12: 14, 13: 4, 14: 18})
    style_title(ws, "K", "CONFIG — Fonte unica di verita'",
                "Modifica SOLO questo foglio: date, tasso, persone, liste e budget alimentano tutte le formule del workbook.")

    # Viaggio
    style_section(ws, 4, "K", "VIAGGIO")
    trip = [
        ("Nome viaggio", "Giappone 2026 — 23 Ott / 6 Nov"),
        ("Data partenza", date(2026, 10, 23)),
        ("Data ritorno", date(2026, 11, 6)),
        ("Ultimo giorno (rientro)", date(2026, 11, 7)),
        ("N° persone", "=COUNTA(B15:B19)"),
        ("Tasso di cambio (1 € = ? ¥)", 184),
        ("Budget target / persona (€)", 2875),
        ("Valuta base", "EUR"),
    ]
    for i, (label, value) in enumerate(trip):
        r = 5 + i
        lc = ws.cell(row=r, column=1, value=label)
        lc.font = FONT_BOLD
        lc.alignment = ALIGN_LEFT
        lc.fill = FILL_PALE2
        lc.border = BORDER
        vc = ws.cell(row=r, column=2, value=value)
        vc.font = FONT_BODY
        vc.alignment = ALIGN_LEFT
        vc.border = BORDER
        if isinstance(value, date):
            vc.number_format = NUM_DATE

    # Persone
    style_section(ws, 14, "K", "PERSONE")
    for i, name in enumerate(["Lorenzo", "Davide", "Rebecca", "", ""]):
        r = 15 + i
        lc = ws.cell(row=r, column=1, value=f"Persona {i + 1}")
        lc.font = FONT_BOLD
        lc.fill = FILL_PALE2
        lc.border = BORDER
        vc = ws.cell(row=r, column=2, value=name)
        vc.font = FONT_BODY
        vc.border = BORDER

    # Liste (in fondo, dove le colonne sono libere: i range dinamici restano puliti)
    style_section(ws, 60, "K", "LISTE (menu a tendina)")
    lists = {
        1: ("Categorie", ["Voli", "Alloggio", "Trasporti", "Ingressi/Attività", "Cibo",
                          "Spese personali", "Souvenir", "Assicurazione", "eSIM", "Bagagli", "Extra"]),
        4: ("Stati", ["Da fare", "In corso", "Prenotato", "Pagato", "Annullato", "Opzionale"]),
        6: ("Partecipa", ["X"]),
        8: ("Priorita'", ["Alta", "Media", "Bassa"]),
        10: ("Valute", ["EUR", "JPY"]),
        14: ("Stato attività", ["Da fare", "Fatto", "Saltato", "Opzionale"]),
    }
    for col, (title, values) in lists.items():
        hc = ws.cell(row=61, column=col, value=title)
        hc.font = FONT_HEADER
        hc.fill = FILL_HEADER
        hc.alignment = ALIGN_CENTER
        hc.border = BORDER
        for j, v in enumerate(values):
            c = ws.cell(row=62 + j, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
    # tipo importo
    hc = ws.cell(row=61, column=12, value="Tipo")
    hc.font = FONT_HEADER
    hc.fill = FILL_HEADER
    hc.alignment = ALIGN_CENTER
    hc.border = BORDER
    for j, v in enumerate(["A testa", "Totale"]):
        c = ws.cell(row=62 + j, column=12, value=v)
        c.font = FONT_BODY
        c.border = BORDER

    # Budget per categoria
    style_section(ws, 34, "K", "BUDGET PER CATEGORIA (€ / persona)")
    budgets = [
        ("Voli", 1096.33), ("Alloggio", 359.89), ("Trasporti", 302.57),
        ("Ingressi/Attività", 206), ("Cibo", 420), ("Spese personali", 400),
        ("Souvenir", 0), ("Assicurazione", 53.43), ("eSIM", 20), ("Bagagli", 17.17),
        ("Extra", 0),
    ]
    h1 = ws.cell(row=35, column=1, value="Categoria")
    h2 = ws.cell(row=35, column=2, value="Budget €/persona")
    for h in (h1, h2):
        h.font = FONT_HEADER
        h.fill = FILL_HEADER
        h.alignment = ALIGN_CENTER
        h.border = BORDER
    for i, (cat, val) in enumerate(budgets):
        r = 36 + i
        c1 = ws.cell(row=r, column=1, value=cat)
        c1.font = FONT_BODY
        c1.border = BORDER
        c2 = ws.cell(row=r, column=2, value=val)
        c2.font = FONT_BODY
        c2.number_format = NUM_EUR
        c2.border = BORDER
    tr = 36 + len(budgets)
    ws.cell(row=tr, column=1, value="TOTALE").font = FONT_BOLD
    tc = ws.cell(row=tr, column=2, value=f"=SUM(B36:B{tr - 1})")
    tc.font = FONT_BOLD
    tc.number_format = NUM_EUR
    tc.fill = FILL_TOTAL
    tc.border = BORDER
    ws.cell(row=tr, column=1).fill = FILL_TOTAL
    ws.cell(row=tr, column=1).border = BORDER

    # immagini decorative
    blossom = XLImage(img_paths["blossom"])
    blossom.width, blossom.height = 170, 170
    ws.add_image(blossom, "D35")

    # ---- Come si usa (sostituisce il foglio LEGENDA) ----
    style_section(ws, 50, "K", "COME SI USA")
    guida = [
        ("Regola d'oro", "Modifica solo CONFIG (date, tasso, persone, liste, budget) e il registro SPESE. "
                         "Tutto il resto e' formula: si ricalcola da solo."),
        ("Aggiungere una spesa", "SPESE: compila Data, Categoria, Descrizione, Importo TOTALE, Valuta, poi scegli 'Pagato da'. "
                                 "Importo €, quota/persona e saldi si calcolano."),
        ("Dividere una spesa", "Stile Tricount: spunta con 'X' le colonne delle persone che dividono la spesa (una, due o tutte). "
                               "La quota/persona è sempre importo totale ÷ numero di spuntati."),
        ("Prenotazioni", "PRENOTAZIONI e' solo per logistica e scadenze (canale, costo, stato, codice conferma). "
                         "Chi ha pagato e come si divide si registra in SPESE."),
        ("Attività", "ATTIVITÀ: aggiorna lo Stato (Da fare / Fatto / Saltato / Opzionale). "
                     "ITINERARIO mostra automaticamente quante attività per giorno sono state fatte."),
        ("Saldi", "SALDI conta solo le spese con 'Pagato da' compilato: saldo positivo = deve ricevere, negativo = deve pagare. "
                  "Le spese senza pagante sono mostrate a parte."),
        ("Estendere", "Aggiungi voci in fondo alle liste del CONFIG: i menu a tendina si allargano da soli (range dinamici). "
                      "I fogli SPESE/PRENOTAZIONI hanno righe con formule gia' pronte."),
        ("Rigenerare", "python _website/scripts/generate-companion-workbook.py — ricrea il file dai dati sorgente."),
        ("Download", "https://lorenzopolito.github.io/Travel-Vault/downloads/Giappone-2026-Companion.xlsx"),
    ]
    gr = 51
    for title, desc in guida:
        t = ws.cell(row=gr, column=1, value=title)
        t.font = FONT_BOLD
        t.fill = FILL_PALE
        t.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        t.border = BORDER
        d = ws.cell(row=gr, column=2, value=desc)
        d.font = FONT_BODY
        d.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        d.border = BORDER
        ws.merge_cells(start_row=gr, start_column=2, end_row=gr, end_column=11)
        ws.row_dimensions[gr].height = 34
        gr += 1

    return {
        "NomeViaggio": "CONFIG!$B$5",
        "DataPartenza": "CONFIG!$B$6",
        "DataRitorno": "CONFIG!$B$7",
        "UltimoGiorno": "CONFIG!$B$8",
        "N_Persone": "CONFIG!$B$9",
        "Tasso_JPY_EUR": "CONFIG!$B$10",
        "Budget_Target_Pax": "CONFIG!$B$11",
        "ListaCategorie": "OFFSET(CONFIG!$A$62,0,0,COUNTA(CONFIG!$A$62:$A$140),1)",
        "ListaStati": "OFFSET(CONFIG!$D$62,0,0,COUNTA(CONFIG!$D$62:$D$140),1)",
        "ListaPersone": "OFFSET(CONFIG!$B$15,0,0,COUNTA(CONFIG!$B$15:$B$19),1)",
        "ListaPartecipa": "OFFSET(CONFIG!$F$62,0,0,COUNTA(CONFIG!$F$62:$F$140),1)",
        "ListaPriorita": "OFFSET(CONFIG!$H$62,0,0,COUNTA(CONFIG!$H$62:$H$140),1)",
        "ListaValute": "OFFSET(CONFIG!$J$62,0,0,COUNTA(CONFIG!$J$62:$J$140),1)",
        "ListaTipo": "OFFSET(CONFIG!$L$62,0,0,COUNTA(CONFIG!$L$62:$L$140),1)",
        "ListaStatiAtt": "OFFSET(CONFIG!$N$62,0,0,COUNTA(CONFIG!$N$62:$N$140),1)",
        "BudgetVoli": "CONFIG!$B$36",
        "BudgetAlloggio": "CONFIG!$B$37",
        "BudgetTrasporti": "CONFIG!$B$38",
        "BudgetIngressi": "CONFIG!$B$39",
        "BudgetCibo": "CONFIG!$B$40",
        "BudgetPersonali": "CONFIG!$B$41",
        "BudgetSouvenir": "CONFIG!$B$42",
        "BudgetAssicurazione": "CONFIG!$B$43",
        "BudgetESIM": "CONFIG!$B$44",
        "BudgetBagagli": "CONFIG!$B$45",
        "BudgetExtra": "CONFIG!$B$46",
    }


def build_itinerario(wb, img_paths):
    ws = wb.create_sheet("ITINERARIO")
    ws.sheet_properties.tabColor = C_SAKURA
    set_widths(ws, {1: 7, 2: 12, 3: 15, 4: 18, 5: 34, 6: 9, 7: 9, 8: 9, 9: 11,
                    10: 9, 11: 52, 12: 13, 13: 40})
    style_title(ws, "M", "ITINERARIO — Giappone 2026",
                "15 giorni · 23 ott – 7 nov 2026 · Roma → KIX → Izumisano → Osaka → Hiroshima → Nara → Kyoto → Tokyo. Budget per persona.")
    headers = ["Giorno", "Data", "Giorno sett.", "Base/Città", "Titolo", "Difficoltà",
               "Cibo €", "Trasporti €", "Ingressi €", "Totale €", "Attività principali",
               "Fatte", "Note / Piano B"]
    style_header_row(ws, 4, headers)
    for i, (g, dt, base, title, diff, food, trans, entr, act, stato, note) in enumerate(ITINERARIO):
        r = 5 + i
        vals = [g, dt, None, base, title, diff, food, trans, entr, None, act, None, note]
        for col, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_CENTER if col in (1, 2, 3, 6, 7, 8, 9, 10, 12) else ALIGN_LEFT
        ws.cell(row=r, column=2).number_format = NUM_DATE
        ws.cell(row=r, column=3, value=(
            f'=CHOOSE(WEEKDAY(B{r},2),"Lun","Mar","Mer","Gio","Ven","Sab","Dom")'))
        ws.cell(row=r, column=10, value=f"=SUM(G{r}:I{r})").number_format = NUM_EUR
        ws.cell(row=r, column=12, value=(
            f'=IF(COUNTIF(Att_Giorno,A{r})=0,"—",'
            f'COUNTIFS(Att_Giorno,A{r},Att_Stato,"Fatto")&"/"&COUNTIF(Att_Giorno,A{r}))'))
        for col in (7, 8, 9):
            ws.cell(row=r, column=col).number_format = NUM_EUR
        ws.row_dimensions[r].height = 42

    tr = 5 + len(ITINERARIO)
    ws.cell(row=tr, column=1, value="TOT").font = FONT_BOLD
    ws.cell(row=tr, column=4, value="Totale / persona").font = FONT_BOLD
    for col, letter in ((7, "G"), (8, "H"), (9, "I"), (10, "J")):
        c = ws.cell(row=tr, column=col, value=f"=SUM({letter}5:{letter}{tr - 1})")
        c.font = FONT_BOLD
        c.number_format = NUM_EUR
        c.fill = FILL_TOTAL
        c.border = BORDER
    for col in range(1, 14):
        ws.cell(row=tr, column=col).fill = FILL_TOTAL
        ws.cell(row=tr, column=col).border = BORDER
    ws.freeze_panes = "A5"

    # conditional formatting difficolta'
    ws.conditional_formatting.add(
        f"F5:F{tr - 1}",
        ColorScaleRule(start_type="num", start_value=1, start_color="C8E6C9",
                       mid_type="num", mid_value=2.5, mid_color="FFE0B2",
                       end_type="num", end_value=4, end_color="F8BBD0"))



def build_attivita(wb, img_paths):
    ws = wb.create_sheet("ATTIVITÀ")
    ws.sheet_properties.tabColor = C_SAKURA_LIGHT
    set_widths(ws, {1: 7, 2: 12, 3: 26, 4: 42, 5: 14, 6: 7, 7: 11, 8: 11, 9: 12,
                    10: 20, 11: 34})
    style_title(ws, "K", "ATTIVITÀ — Tracker attività e luoghi",
                "Una riga per attività/luogo. Aggiorna 'Stato' dal menu a tendina: le attività completate aumentano la barra in DASHBOARD.")
    headers = ["Giorno", "Data", "Città", "Attività / Luogo", "Tipo", "Voto",
               "Costo ¥", "Costo €", "Stato", "Prenotazione", "Note / Rebecca"]
    style_header_row(ws, 4, headers)
    start = 5
    for i, (g, dt, city, att, tipo, voto, yen, stato, pren, note) in enumerate(ATTIVITA):
        r = start + i
        data = [g, dt, city, att, tipo, voto, (yen if yen else None), None, stato, pren, note]
        for col, v in enumerate(data, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_CENTER if col in (1, 2, 5, 6, 7, 8, 9) else ALIGN_LEFT
        ws.cell(row=r, column=2).number_format = NUM_DATE
        ws.cell(row=r, column=7).number_format = NUM_JPY
        ws.cell(row=r, column=8, value=f'=IF(OR(G{r}="",G{r}=0),"",G{r}/Tasso_JPY_EUR)')
        ws.cell(row=r, column=8).number_format = NUM_ZERO_HIDDEN
        ws.row_dimensions[r].height = 30

    tr = start + len(ATTIVITA)
    ws.cell(row=tr, column=3, value="TOTALE (attività a pagamento)").font = FONT_BOLD
    c = ws.cell(row=tr, column=8, value=f'=SUM(H{start}:H{tr - 1})')
    c.font = FONT_BOLD
    c.number_format = NUM_EUR
    for col in range(1, 12):
        ws.cell(row=tr, column=col).fill = FILL_TOTAL
        ws.cell(row=tr, column=col).border = BORDER

    dv = DataValidation(type="list", formula1="=ListaStatiAtt", allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"I{start}:I{tr - 1}")

    ws.conditional_formatting.add(f"F{start}:F{tr - 1}", ColorScaleRule(
        start_type="num", start_value=1, start_color="ECEFF1",
        mid_type="num", mid_value=3, mid_color="F8BBD0",
        end_type="num", end_value=5, end_color="D94F79"))
    ws.conditional_formatting.add(f"I{start}:I{tr - 1}", CellIsRule(
        operator="equal", formula=['"Da fare"'], fill=PatternFill("solid", fgColor="FFF9C4"),
        font=Font(color="7A5B00")))
    ws.conditional_formatting.add(f"I{start}:I{tr - 1}", CellIsRule(
        operator="equal", formula=['"Fatto"'], fill=PatternFill("solid", fgColor="C8E6C9"),
        font=Font(color="1B5E20", bold=True)))
    ws.conditional_formatting.add(f"I{start}:I{tr - 1}", CellIsRule(
        operator="equal", formula=['"Saltato"'], fill=PatternFill("solid", fgColor="FFCDD2"),
        font=Font(color="B71C1C")))
    ws.conditional_formatting.add(f"I{start}:I{tr - 1}", CellIsRule(
        operator="equal", formula=['"Opzionale"'], fill=PatternFill("solid", fgColor="ECEFF1"),
        font=Font(color="607D8B")))

    ws.freeze_panes = "A5"


def build_prenotazioni(wb, img_paths):
    ws = wb.create_sheet("PRENOTAZIONI")
    ws.sheet_properties.tabColor = C_SAKURA_MID
    set_widths(ws, {1: 42, 2: 15, 3: 18, 4: 20, 5: 12, 6: 9, 7: 24, 8: 10, 9: 7,
                    10: 11, 11: 11, 12: 12, 13: 11, 14: 12, 15: 18, 16: 10, 17: 44})
    style_title(ws, "Q", "PRENOTAZIONI — Tracker prenotazioni & scadenze",
                "Tutto cio' che va prenotato/acquistato. I giorni rimanenti si aggiornano da soli (TODAY).")
    headers = ["Voce", "Categoria", "Data/Giorno", "Finestra apertura", "Scadenza",
               "Giorni", "Canale", "Importo", "Valuta", "Tipo", "Importo unit. €",
               "Importo tot. €", "Importo/pax €", "Stato", "Codice conferma", "Priorità", "Note"]
    style_header_row(ws, 4, headers)
    start = 5
    n_rows = 50
    for i in range(n_rows):
        r = start + i
        if i < len(PRENOTAZIONI):
            (voce, cat, ev, fin, scad, canale, imp, val, per, stato, prio, note) = PRENOTAZIONI[i]
            data = [voce, cat, ev, fin, scad, None, canale, imp, val, per, None, None,
                    None, stato, "", prio, note]
        else:
            data = [None] * 17
        for col, v in enumerate(data, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_CENTER if col in (2, 5, 6, 9, 10, 11, 12, 13, 14, 16) else ALIGN_LEFT
        ws.cell(row=r, column=5).number_format = NUM_DATE
        ws.cell(row=r, column=6, value=f'=IF(E{r}="","",E{r}-TODAY())')
        ws.cell(row=r, column=6).number_format = "0"
        ws.cell(row=r, column=11, value=f'=IF(H{r}="","",IF(UPPER(I{r})="JPY",H{r}/Tasso_JPY_EUR,H{r}))')
        ws.cell(row=r, column=11).number_format = NUM_EUR
        ws.cell(row=r, column=12,
                value=f'=IF(H{r}="","",K{r}*IF(LEFT(UPPER(J{r}),1)="A",N_Persone,1))')
        ws.cell(row=r, column=12).number_format = NUM_EUR
        ws.cell(row=r, column=13,
                value=f'=IF(H{r}="","",IF(LEFT(UPPER(J{r}),1)="A",K{r},K{r}/N_Persone))')
        ws.cell(row=r, column=13).number_format = NUM_EUR
        ws.cell(row=r, column=8).number_format = '#,##0'
        ws.row_dimensions[r].height = 26

    # totali
    tr = start + n_rows
    ws.cell(row=tr, column=1, value="TOTALE").font = FONT_BOLD
    for col in (11, 12, 13):
        L = get_column_letter(col)
        c = ws.cell(row=tr, column=col, value=f"=SUM({L}{start}:{L}{tr - 1})")
        c.font = FONT_BOLD
        c.number_format = NUM_EUR
        c.fill = FILL_TOTAL
        c.border = BORDER
    for col in range(1, 18):
        ws.cell(row=tr, column=col).fill = FILL_TOTAL
        ws.cell(row=tr, column=col).border = BORDER

    # validazioni
    def dv(formula, cellrange, allow_blank=True):
        v = DataValidation(type="list", formula1=f"={formula}", allow_blank=allow_blank)
        ws.add_data_validation(v)
        v.add(cellrange)

    dv("ListaCategorie", f"B{start}:B{tr - 1}")
    dv("ListaValute", f"I{start}:I{tr - 1}")
    dv("ListaTipo", f"J{start}:J{tr - 1}")
    dv("ListaStati", f"N{start}:N{tr - 1}")
    dv("ListaPriorita", f"P{start}:P{tr - 1}")

    last = tr - 1
    # stato
    ws.conditional_formatting.add(f"N{start}:N{last}", CellIsRule(
        operator="equal", formula=['"Pagato"'], fill=PatternFill("solid", fgColor="C8E6C9"),
        font=Font(color="1B5E20", bold=True)))
    ws.conditional_formatting.add(f"N{start}:N{last}", CellIsRule(
        operator="equal", formula=['"Prenotato"'], fill=PatternFill("solid", fgColor="B3E5FC"),
        font=Font(color="01579B", bold=True)))
    ws.conditional_formatting.add(f"N{start}:N{last}", CellIsRule(
        operator="equal", formula=['"Da fare"'], fill=PatternFill("solid", fgColor="FFF9C4"),
        font=Font(color="7A5B00", bold=True)))
    ws.conditional_formatting.add(f"N{start}:N{last}", CellIsRule(
        operator="equal", formula=['"Annullato"'], fill=PatternFill("solid", fgColor="FFCDD2"),
        font=Font(color="B71C1C")))
    ws.conditional_formatting.add(f"N{start}:N{last}", CellIsRule(
        operator="equal", formula=['"Opzionale"'], fill=PatternFill("solid", fgColor="ECEFF1"),
        font=Font(color="607D8B")))
    # giorni rimanenti
    ws.conditional_formatting.add(f"F{start}:F{last}", CellIsRule(
        operator="lessThanOrEqual", formula=["0"], fill=PatternFill("solid", fgColor="EF9A9A"),
        font=Font(color="B71C1C", bold=True)))
    ws.conditional_formatting.add(f"F{start}:F{last}", CellIsRule(
        operator="between", formula=["1", "7"], fill=PatternFill("solid", fgColor="FFCC80"),
        font=Font(color="7A4B00", bold=True)))
    ws.conditional_formatting.add(f"F{start}:F{last}", CellIsRule(
        operator="between", formula=["8", "30"], fill=PatternFill("solid", fgColor="FFF9C4"),
        font=Font(color="7A5B00")))

    ws.freeze_panes = "A5"


def build_spese(wb, img_paths):
    ws = wb.create_sheet("SPESE")
    ws.sheet_properties.tabColor = C_LEAF
    set_widths(ws, {1: 12, 2: 7, 3: 16, 4: 40, 5: 11, 6: 7, 7: 12, 8: 13,
                    9: 6, 10: 6, 11: 6, 12: 9, 13: 12, 14: 34})
    style_title(ws, "N", "SPESE — Registro spese (stile Tricount)",
                "Inserisci l'importo TOTALE, chi ha pagato e spunta con 'X' chi la divide. "
                "Importo €, quota/persona e saldi si calcolano da soli.")
    headers = ["Data", "Giorno", "Categoria", "Descrizione", "Importo", "Valuta",
               "Importo €", "Pagato da", "P1", "P2", "P3", "N° partec.",
               "Quota/persona €", "Note"]
    style_header_row(ws, 4, headers)
    # intestazioni persone dinamiche dal CONFIG
    for col, src in ((9, "$B$15"), (10, "$B$16"), (11, "$B$17")):
        c = ws.cell(row=4, column=col, value=f"=CONFIG!{src}")
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_CENTER
        c.border = BORDER
    start = 5
    n_rows = 120
    for i in range(n_rows):
        r = start + i
        if i < len(SPESE_PREFILL):
            (dt, cat, desc, imp, val, pagato, p1, p2, p3, note) = SPESE_PREFILL[i]
            data = [dt, None, cat, desc, imp, val, None, pagato, p1, p2, p3, None, None, note]
        else:
            data = [None] * 14
        for col, v in enumerate(data, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_CENTER if col in (2, 6, 9, 10, 11, 12) else ALIGN_LEFT
        ws.cell(row=r, column=1).number_format = NUM_DATE
        ws.cell(row=r, column=2, value=f'=IF(A{r}="","",IF(A{r}<DataPartenza,"pre",MAX(1,A{r}-DataPartenza)))')
        ws.cell(row=r, column=2).number_format = '"G"0'
        ws.cell(row=r, column=7, value=f'=IF(E{r}="","",IF(UPPER(F{r})="JPY",E{r}/Tasso_JPY_EUR,E{r}))')
        ws.cell(row=r, column=7).number_format = NUM_EUR
        ws.cell(row=r, column=12, value=f'=COUNTIF(I{r}:K{r},"X")')
        ws.cell(row=r, column=12).number_format = "0"
        ws.cell(row=r, column=13, value=f'=IF(OR(G{r}="",L{r}=0),0,G{r}/L{r})')
        ws.cell(row=r, column=13).number_format = NUM_ZERO_HIDDEN
        ws.row_dimensions[r].height = 20

    tr = start + n_rows
    ws.cell(row=tr, column=4, value="TOTALE SPESO (gruppo)").font = FONT_BOLD
    c = ws.cell(row=tr, column=7, value=f"=SUM(G{start}:G{tr - 1})")
    c.font = FONT_BOLD
    c.number_format = NUM_EUR
    for col in range(1, 15):
        ws.cell(row=tr, column=col).fill = FILL_TOTAL
        ws.cell(row=tr, column=col).border = BORDER

    def dv(formula, cellrange):
        v = DataValidation(type="list", formula1=f"={formula}", allow_blank=True)
        ws.add_data_validation(v)
        v.add(cellrange)

    dv("ListaCategorie", f"C{start}:C{tr - 1}")
    dv("ListaValute", f"F{start}:F{tr - 1}")
    dv("ListaPersone", f"H{start}:H{tr - 1}")
    for col in (9, 10, 11):
        L = get_column_letter(col)
        v = DataValidation(type="list", formula1="=ListaPartecipa", allow_blank=True)
        ws.add_data_validation(v)
        v.add(f"{L}{start}:{L}{tr - 1}")
        ws.conditional_formatting.add(f"{L}{start}:{L}{tr - 1}", CellIsRule(
            operator="equal", formula=['"X"'], fill=PatternFill("solid", fgColor="F8BBD0"),
            font=Font(color=C_SAKURA_DEEP, bold=True)))

    ws.freeze_panes = "A5"


def build_budget(wb, img_paths):
    ws = wb.create_sheet("BUDGET")
    ws.sheet_properties.tabColor = C_GOLD
    set_widths(ws, {1: 22, 2: 16, 3: 16, 4: 16, 5: 16, 6: 14, 7: 12, 8: 36})
    style_title(ws, "H", "BUDGET — Stimato vs Reale",
                "Il budget stimato arriva dal CONFIG; lo speso reale è calcolato dal registro SPESE (SUMIF per categoria).")
    headers = ["Categoria", "Budget gruppo €", "Budget/pax €", "Speso gruppo €",
               "Speso/pax €", "Delta €", "Utilizzo", "Note"]
    style_header_row(ws, 4, headers)

    cats = [("Voli", "BudgetVoli"), ("Alloggio", "BudgetAlloggio"),
            ("Trasporti", "BudgetTrasporti"), ("Ingressi/Attività", "BudgetIngressi"),
            ("Cibo", "BudgetCibo"), ("Spese personali", "BudgetPersonali"),
            ("Souvenir", "BudgetSouvenir"), ("Assicurazione", "BudgetAssicurazione"),
            ("eSIM", "BudgetESIM"), ("Bagagli", "BudgetBagagli"), ("Extra", "BudgetExtra")]
    notes = {
        "Voli": "China Eastern open-jaw (reale)",
        "Alloggio": "4 strutture · 13 notti (reale)",
        "Trasporti": "JR pass + Kyoto→Tokyo + locali",
        "Ingressi/Attività": "USJ, Sanrio, torri, templi…",
        "Cibo": "Rebecca cucina: possibile risparmio",
        "Spese personali": "Souvenir ed extra",
        "Souvenir": "Voce libera",
        "Assicurazione": "Provider da annotare",
        "eSIM": "Klook / Airalo",
        "Bagagli": "Takkyubin Osaka→Tokyo",
        "Extra": "Imprevisti",
    }
    start = 5
    for i, (cat, ref) in enumerate(cats):
        r = start + i
        ws.cell(row=r, column=1, value=cat).font = FONT_BODY
        b = ws.cell(row=r, column=2, value=f"={ref}*N_Persone")
        b.number_format = NUM_EUR
        ws.cell(row=r, column=3, value=f"={ref}").number_format = NUM_EUR
        d = ws.cell(row=r, column=4, value=f'=SUMIF(Spese_Categoria,A{r},Spese_ImportoTot)')
        d.number_format = NUM_EUR
        ws.cell(row=r, column=5, value=f"=IF(D{r}=0,0,D{r}/N_Persone)").number_format = NUM_EUR
        ws.cell(row=r, column=6, value=f"=B{r}-D{r}").number_format = NUM_EUR
        ws.cell(row=r, column=7, value=f'=IF(B{r}=0,"",D{r}/B{r})').number_format = NUM_PCT
        ws.cell(row=r, column=8, value=notes[cat]).font = FONT_SMALL
        for col in range(1, 9):
            ws.cell(row=r, column=col).border = BORDER
            if col in (2, 3, 4, 5, 6):
                ws.cell(row=r, column=col).font = FONT_BODY
        ws.cell(row=r, column=1).font = FONT_BOLD
    tr = start + len(cats)
    ws.cell(row=tr, column=1, value="TOTALE").font = FONT_BOLD
    for col in (2, 3, 4, 5, 6):
        L = get_column_letter(col)
        c = ws.cell(row=tr, column=col, value=f"=SUM({L}{start}:{L}{tr - 1})")
        c.font = FONT_BOLD
        c.number_format = NUM_EUR if col != 6 else NUM_EUR
    ws.cell(row=tr, column=7, value=f'=IF(B{tr}=0,"",D{tr}/B{tr})').number_format = NUM_PCT
    for col in range(1, 9):
        ws.cell(row=tr, column=col).fill = FILL_TOTAL
        ws.cell(row=tr, column=col).border = BORDER
    ws.cell(row=tr, column=7).font = FONT_BOLD

    # data bar su utilizzo
    ws.conditional_formatting.add(
        f"G{start}:G{tr - 1}",
        DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1,
                    color=C_SAKURA, showValue=True, minLength=None, maxLength=None))
    ws.conditional_formatting.add(
        f"G{start}:G{tr - 1}",
        CellIsRule(operator="greaterThan", formula=["1"],
                   font=Font(color="B71C1C", bold=True)))

    # grafico budget vs speso
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "clustered"
    chart.title = "Budget vs Speso per categoria (gruppo)"
    chart.style = 10
    data = Reference(ws, min_col=2, max_col=2, min_row=4, max_row=tr - 1)
    data2 = Reference(ws, min_col=4, max_col=4, min_row=4, max_row=tr - 1)
    catsref = Reference(ws, min_col=1, min_row=start, max_row=tr - 1)
    chart.add_data(data, titles_from_data=True)
    chart.add_data(data2, titles_from_data=True)
    chart.set_categories(catsref)
    chart.series[0].graphicalProperties.solidFill = C_SAKURA
    chart.series[1].graphicalProperties.solidFill = C_SAKURA_LIGHT
    chart.height = 9
    chart.width = 20
    chart.y_axis.title = "€ (gruppo)"
    ws.add_chart(chart, "A22")



def build_scadenze(wb, img_paths):
    ws = wb.create_sheet("SCADENZE")
    ws.sheet_properties.tabColor = C_SAKURA_DEEP
    set_widths(ws, {1: 12, 2: 52, 3: 16, 4: 10, 5: 10, 6: 14, 7: 46})
    style_title(ws, "G", "SCADENZE — Timeline prenotazioni",
                "Ordinate per data. 'Giorni' e 'Stato' si calcolano da TODAY(): rosso = urgente/scaduta.")
    headers = ["Data", "Cosa", "Categoria", "Priorità", "Giorni", "Stato", "Note"]
    style_header_row(ws, 4, headers)
    start = 5
    for i, (dt, cosa, cat, prio, note) in enumerate(SCADENZE):
        r = start + i
        vals = [dt, cosa, cat, prio, None, None, note]
        for col, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_CENTER if col in (1, 3, 4, 5, 6) else ALIGN_LEFT
        ws.cell(row=r, column=1).number_format = NUM_DATE
        ws.cell(row=r, column=5, value=f'=IF(A{r}="","",A{r}-TODAY())').number_format = "0"
        ws.cell(row=r, column=6, value=(
            f'=IF(A{r}="","",IF(A{r}-TODAY()<0,"Scaduta",'
            f'IF(A{r}-TODAY()<=7,"Urgente",IF(A{r}-TODAY()<=30,"In arrivo","Programmata"))))'))
        ws.row_dimensions[r].height = 24
    last = start + len(SCADENZE) - 1
    ws.conditional_formatting.add(f"F{start}:F{last}", CellIsRule(
        operator="equal", formula=['"Scaduta"'], fill=PatternFill("solid", fgColor="EF9A9A"),
        font=Font(color="B71C1C", bold=True)))
    ws.conditional_formatting.add(f"F{start}:F{last}", CellIsRule(
        operator="equal", formula=['"Urgente"'], fill=PatternFill("solid", fgColor="FFAB91"),
        font=Font(color="7A2E00", bold=True)))
    ws.conditional_formatting.add(f"F{start}:F{last}", CellIsRule(
        operator="equal", formula=['"In arrivo"'], fill=PatternFill("solid", fgColor="FFE082"),
        font=Font(color="7A5B00")))
    ws.conditional_formatting.add(f"F{start}:F{last}", CellIsRule(
        operator="equal", formula=['"Programmata"'], fill=PatternFill("solid", fgColor="C8E6C9"),
        font=Font(color="1B5E20")))
    ws.freeze_panes = "A5"


def build_saldi(wb, img_paths, config_names):
    ws = wb.create_sheet("SALDI")
    ws.sheet_properties.tabColor = C_LEAF
    set_widths(ws, {1: 18, 2: 16, 3: 16, 4: 16, 5: 18, 6: 34})
    style_title(ws, "F", "SALDI — Chi ha anticipato e chi deve dare",
                "Anticipato = spese pagate dalla persona. Quota = spese in cui è spuntata con 'X'. Saldo = Anticipato - Quota.")
    headers = ["Persona", "Anticipato €", "Quota dovuta €", "Saldo €", "Stato", "Note"]
    style_header_row(ws, 4, headers)
    start = 5
    people_cols = ["Spese_P1", "Spese_P2", "Spese_P3"]
    for i, pcol in enumerate(people_cols):
        r = start + i
        n = ws.cell(row=r, column=1, value=f"=CONFIG!$B${15 + i}")
        n.font = FONT_BOLD
        n.border = BORDER
        ws.cell(row=r, column=2, value=f'=SUMIF(Spese_PagatoDa,A{r},Spese_ImportoTot)')
        ws.cell(row=r, column=2).number_format = NUM_EUR
        ws.cell(row=r, column=3, value=(
            f'=SUMIFS(Spese_QuotaPax,{pcol},"X",Spese_PagatoDa,"<>")'))
        ws.cell(row=r, column=3).number_format = NUM_EUR
        ws.cell(row=r, column=4, value=f"=B{r}-C{r}").number_format = NUM_EUR
        ws.cell(row=r, column=5, value=(
            f'=IF(AND(B{r}=0,C{r}=0),"",IF(D{r}>0.01,"Da ricevere",IF(D{r}<-0.01,"Da pagare","In pari")))'))
        for col in range(1, 7):
            ws.cell(row=r, column=col).border = BORDER
            if col not in (1, 6):
                ws.cell(row=r, column=col).font = FONT_BODY
        ws.row_dimensions[r].height = 22
    ws.cell(row=start, column=6, value="Chi ha speso di più riceve dagli altri").font = FONT_SMALL
    ws.cell(row=start + 1, column=6, value="Spunta le persone in SPESE (colonne 'X')").font = FONT_SMALL
    ws.cell(row=start + 2, column=6, value="Compila 'Pagato da' per calcolare i saldi").font = FONT_SMALL

    tr = start + len(people_cols)
    ws.cell(row=tr, column=1, value="TOTALE").font = FONT_BOLD
    for col in (2, 3, 4):
        L = get_column_letter(col)
        c = ws.cell(row=tr, column=col, value=f"=SUM({L}{start}:{L}{tr - 1})")
        c.font = FONT_BOLD
        c.number_format = NUM_EUR
    for col in range(1, 7):
        ws.cell(row=tr, column=col).fill = FILL_TOTAL
        ws.cell(row=tr, column=col).border = BORDER

    ur = tr + 1
    ws.cell(row=ur, column=1, value="Senza 'Pagato da'").font = FONT_BOLD
    ws.cell(row=ur, column=1).fill = FILL_PALE
    ws.cell(row=ur, column=1).border = BORDER
    u2 = ws.cell(row=ur, column=2, value='=SUMIF(Spese_PagatoDa,"",Spese_ImportoTot)')
    u2.number_format = NUM_EUR
    u2.font = FONT_BOLD
    u2.border = BORDER
    ws.merge_cells(start_row=ur, start_column=3, end_row=ur, end_column=6)
    ws.cell(row=ur, column=3, value='=IF(B' + str(ur) + '>0,"⚠ assegna chi ha pagato per calcolare i saldi","tutto assegnato")')
    ws.cell(row=ur, column=3).font = FONT_SMALL
    ws.cell(row=ur, column=3).alignment = ALIGN_LEFT
    ws.cell(row=ur, column=3).border = BORDER

    note = ws.cell(row=tr + 2, column=1, value=(
        "Stile Tricount: in SPESE scegli chi ha pagato e spunta con 'X' chi divide la spesa (una, due o tutte le persone). "
        "La quota/persona è sempre importo totale ÷ partecipanti. I saldi contano solo le spese con 'Pagato da' compilato: "
        "saldo positivo = deve RICEVERE, saldo negativo = deve PAGARE."))
    note.font = FONT_SMALL
    note.alignment = ALIGN_LEFT
    ws.merge_cells(start_row=tr + 2, start_column=1, end_row=tr + 3, end_column=6)
    ws.conditional_formatting.add(f"E{start}:E{tr - 1}", CellIsRule(
        operator="equal", formula=['"Da ricevere"'], fill=PatternFill("solid", fgColor="C8E6C9"),
        font=Font(color="1B5E20", bold=True)))
    ws.conditional_formatting.add(f"E{start}:E{tr - 1}", CellIsRule(
        operator="equal", formula=['"Da pagare"'], fill=PatternFill("solid", fgColor="FFCDD2"),
        font=Font(color="B71C1C", bold=True)))


def build_dashboard(wb, img_paths):
    ws = wb.create_sheet("DASHBOARD", 0)
    ws.sheet_properties.tabColor = C_SAKURA
    # griglia uniforme: KPI e tabelle condividono le stesse colonne
    set_widths(ws, {i: 15 for i in range(1, 16)})
    style_title(ws, "O", "Giappone 2026 — Companion",
                "Dashboard dinamica: si aggiorna da sola da CONFIG, SPESE, PRENOTAZIONI.")

    # banner (sotto titolo/sottotitolo, con spazio dedicato)
    ws.row_dimensions[3].height = 10
    for r in range(4, 10):
        ws.row_dimensions[r].height = 24
    banner = XLImage(img_paths["banner"])
    banner.width, banner.height = 1640, 182
    ws.add_image(banner, "A4")

    # KPI: label (10) + valori formattati (11) + barra info (12)
    row_lab, row_val = 10, 11
    labels = [("A", "C", "Giorni alla partenza"), ("E", "G", "Budget gruppo €"),
              ("I", "K", "Speso gruppo €"), ("M", "O", "Residuo €")]
    for c1, c2, txt in labels:
        ws.merge_cells(f"{c1}{row_lab}:{c2}{row_lab}")
        cell = ws[f"{c1}{row_lab}"]
        cell.value = txt
        cell.font = FONT_BOLD
        cell.alignment = ALIGN_CENTER
        cell.fill = FILL_PALE
        cell.border = Border(top=Side(style="thick", color=C_SAKURA),
                             left=Side(style="thick", color=C_SAKURA),
                             right=Side(style="thick", color=C_SAKURA))
    values = [
        ("A", "C",
         '=IF(TODAY()<DataPartenza,DataPartenza-TODAY(),IF(TODAY()<=DataRitorno,"in viaggio","concluso"))',
         '0" giorni"'),
        ("E", "G", "=Budget_Target_Pax*N_Persone", NUM_EUR0),
        ("I", "K", "=SUM(Spese_ImportoTot)", NUM_EUR0),
        ("M", "O", "=Budget_Target_Pax*N_Persone-SUM(Spese_ImportoTot)", NUM_EUR0),
    ]
    for c1, c2, formula, fmt in values:
        ws.merge_cells(f"{c1}{row_val}:{c2}{row_val}")
        cell = ws[f"{c1}{row_val}"]
        cell.value = formula
        cell.number_format = fmt
        cell.font = FONT_KPI
        cell.alignment = ALIGN_CENTER
        cell.fill = FILL_PALE
        cell.border = Border(bottom=Side(style="thick", color=C_SAKURA),
                             left=Side(style="thick", color=C_SAKURA),
                             right=Side(style="thick", color=C_SAKURA))
    ws.row_dimensions[row_lab].height = 20
    ws.row_dimensions[row_val].height = 30

    ws.merge_cells("A12:O12")
    act = ws["A12"]
    act.value = ('="Prenotazioni: " & (COUNTIF(Pren_Stato,"Pagato")+COUNTIF(Pren_Stato,"Prenotato")) '
                 '& "/" & COUNTA(Pren_Voce) & "   ·   Attività: " & COUNTIF(Att_Stato,"Fatto") '
                 '& "/" & COUNTA(Att_Attivita) & " completate   ·   Utilizzo budget: " '
                 '& TEXT(SUM(Spese_ImportoTot)/(Budget_Target_Pax*N_Persone),"0%")')
    act.font = FONT_BOLD
    act.alignment = ALIGN_CENTER
    act.fill = FILL_BLOSSOM
    ws.row_dimensions[12].height = 20

    # scadenze (A:G) + saldi (H:O)
    style_section(ws, 14, "G", "PROSSIME SCADENZE")
    ws.merge_cells("H14:O14")
    sh = ws["H14"]
    sh.value = "  SALDO PER PERSONA"
    sh.font = FONT_SECTION
    sh.fill = FILL_SECTION
    sh.alignment = Alignment(horizontal="left", vertical="center")

    def hcell(row, c1, c2, text):
        if c1 != c2:
            ws.merge_cells(f"{c1}{row}:{c2}{row}")
        c = ws[f"{c1}{row}"]
        c.value = text
        c.font = FONT_HEADER
        c.fill = FILL_HEADER
        c.alignment = ALIGN_CENTER
        c.border = BORDER

    hr = 15
    hcell(hr, "A", "A", "Data")
    hcell(hr, "B", "D", "Cosa")
    hcell(hr, "E", "E", "Giorni")
    hcell(hr, "F", "G", "Stato")
    hcell(hr, "H", "H", "Persona")
    hcell(hr, "I", "I", "Anticipato")
    hcell(hr, "J", "J", "Quota")
    hcell(hr, "K", "K", "Saldo")
    hcell(hr, "L", "L", "Stato")
    hcell(hr, "M", "O", "Nota")

    for i in range(8):
        r = hr + 1 + i
        src = 5 + i
        ws.cell(row=r, column=1, value=f'=IF(SCADENZE!A{src}="","",SCADENZE!A{src})').number_format = NUM_DATE
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws.cell(row=r, column=2, value=f'=IF(SCADENZE!B{src}="","",SCADENZE!B{src})')
        ws.cell(row=r, column=5, value=f'=IF(SCADENZE!E{src}="","",SCADENZE!E{src})').number_format = "0"
        ws.merge_cells(start_row=r, start_column=6, end_row=r, end_column=7)
        ws.cell(row=r, column=6, value=f'=IF(SCADENZE!F{src}="","",SCADENZE!F{src})')
        for col in range(1, 8):
            cel = ws.cell(row=r, column=col)
            cel.font = FONT_BODY
            cel.border = BORDER
            cel.alignment = ALIGN_LEFT if col == 2 else ALIGN_CENTER

    for i in range(3):
        r = hr + 1 + i
        src = 5 + i
        ws.cell(row=r, column=8, value=f"=SALDI!A{src}").font = FONT_BODY
        ws.cell(row=r, column=9, value=f"=SALDI!B{src}").number_format = NUM_EUR
        ws.cell(row=r, column=10, value=f"=SALDI!C{src}").number_format = NUM_EUR
        ws.cell(row=r, column=11, value=f"=SALDI!D{src}").number_format = NUM_EUR
        ws.cell(row=r, column=12, value=f"=SALDI!E{src}")
        ws.merge_cells(start_row=r, start_column=13, end_row=r, end_column=15)
        ws.cell(row=r, column=13, value=f'=IF(SALDI!B{src}=0,"—","compila \'Pagato da\' in SPESE")')
        for col in range(8, 16):
            cel = ws.cell(row=r, column=col)
            cel.font = FONT_BODY
            cel.border = BORDER
            cel.alignment = ALIGN_CENTER

    # GRAFICI
    style_section(ws, 25, "O", "GRAFICI")
    b_ws = wb["BUDGET"]
    bar = BarChart()
    bar.type = "col"
    bar.grouping = "clustered"
    bar.title = "Budget vs Speso per categoria (gruppo)"
    bar.style = 10
    data = Reference(b_ws, min_col=2, max_col=2, min_row=4, max_row=15)
    data2 = Reference(b_ws, min_col=4, max_col=4, min_row=4, max_row=15)
    cats = Reference(b_ws, min_col=1, min_row=5, max_row=15)
    bar.add_data(data, titles_from_data=True)
    bar.add_data(data2, titles_from_data=True)
    bar.set_categories(cats)
    bar.series[0].graphicalProperties.solidFill = C_SAKURA
    bar.series[1].graphicalProperties.solidFill = C_SAKURA_LIGHT
    bar.height = 8.5
    bar.width = 18
    ws.add_chart(bar, "A26")

    dough = DoughnutChart()
    dough.title = "Distribuzione spesa per categoria"
    d1 = Reference(b_ws, min_col=4, max_col=4, min_row=4, max_row=15)
    dough.add_data(d1, titles_from_data=True)
    dough.set_categories(cats)
    dough.dataLabels = DataLabelList()
    dough.dataLabels.showPercent = True
    dough.dataLabels.showCatName = False
    dough.dataLabels.showSerName = False
    dough.dataLabels.showVal = False
    dough.dataLabels.showLegendKey = False
    dough.dataLabels.showLeaderLines = True
    dough.series[0].data_points = [
        DataPoint(idx=i, spPr=GraphicalProperties(solidFill=SAKURA_PALETTE[i % len(SAKURA_PALETTE)]))
        for i in range(11)
    ]
    dough.height = 8.5
    dough.width = 13
    ws.add_chart(dough, "K26")

    it_ws = wb["ITINERARIO"]
    itbar = BarChart()
    itbar.type = "col"
    itbar.title = "Budget giornaliero (€/persona)"
    itbar.style = 10
    idata = Reference(it_ws, min_col=10, max_col=10, min_row=4, max_row=19)
    icats = Reference(it_ws, min_col=1, min_row=5, max_row=19)
    itbar.add_data(idata, titles_from_data=True)
    itbar.set_categories(icats)
    itbar.series[0].graphicalProperties.solidFill = C_SAKURA_MID
    itbar.height = 8.5
    itbar.width = 18
    ws.add_chart(itbar, "A45")

    leg = ws.cell(row=45, column=9, value=(
        "Legenda stati\n"
        "• Da fare / Da pianificare → giallo\n"
        "• Prenotato → azzurro\n"
        "• Pagato / Fatto → verde\n"
        "• Annullato / Scaduta → rosso\n"
        "• Opzionale → grigio"))
    leg.font = FONT_SMALL
    leg.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)


def build_logistica(wb, img_paths):
    ws = wb.create_sheet("LOGISTICA")
    ws.sheet_properties.tabColor = C_SAKURA_MID
    set_widths(ws, {1: 18, 2: 34, 3: 30, 4: 20, 5: 34, 6: 18})
    style_title(ws, "F", "LOGISTICA — Info rapide",
                "Voli, alloggi, trasporti, emergenze, allergie Rebecca. Riferimenti utili sul campo.")

    style_section(ws, 4, "F", "VOLI — China Eastern (prenotati 09/08/26)")
    style_header_row(ws, 5, ["Tratta", "Percorso", "Orari", "Voli", "Durata"])
    for i, row in enumerate(LOGISTICA_VOLI):
        r = 6 + i
        for col, v in enumerate(row, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_LEFT

    style_section(ws, 9, "F", "ALLOGGI — tutti prenotati (cucina per Rebecca)")
    style_header_row(ws, 10, ["Città", "Struttura", "Date", "Notti", "Indirizzo"])
    for i, row in enumerate(LOGISTICA_HOTEL):
        r = 11 + i
        vals = row[:5]
        for col, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_LEFT
        # check-in/cucina in colonne F/G? aggiungo sotto forma note
        ws.cell(row=r, column=6, value=f"{row[5]} · {row[6]}").font = FONT_SMALL
        ws.cell(row=r, column=6).border = BORDER

    style_section(ws, 17, "F", "TRASPORTI — Pass & biglietti")
    style_header_row(ws, 18, ["Voce", "Copertura", "Costo", "Quando", "Note"])
    trasporti = [
        ("JR Kansai-Hiroshima Area Pass (5gg)", "Shinkansen Shin-Osaka⇔Hiroshima A/R, traghetto JR Miyajima, linee JR West",
         "17.000 ¥ (~92 €)", "Attivo 28 ott – 1 nov", "Acquistare su JR-WEST ONLINE (posti online dal 28/09)"),
        ("Kyoto→Tokyo Shinkansen Hikari", "Posto riservato, ~2h40", "~13.650 ¥ (~74 €)", "1 nov",
         "SmartEX · Hayatoku 21 entro 11/10"),
        ("Suica / Icoca", "Metro, bus, treni locali, konbini", "Ricarica", "Tutto il viaggio",
         "Suica digitale su iPhone o Icoca a KIX"),
        ("Osaka→Nara (Kintetsu)", "Non coperto dal JR Pass", "~570 ¥", "29 ott", "IC card"),
        ("Nara→Kyoto (JR Nara Line)", "Incluso nel pass", "—", "29 ott", "—"),
    ]
    for i, row in enumerate(trasporti):
        r = 19 + i
        for col, v in enumerate(row, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_LEFT

    style_section(ws, 25, "F", "EMERGENZE & ASSISTENZA")
    style_header_row(ws, 26, ["Numero", "Servizio", "Note"])
    for i, row in enumerate(LOGISTICA_EMERGENZE):
        r = 27 + i
        for col, v in enumerate(row, start=1):
            c = ws.cell(row=r, column=col, value=v)
            c.font = FONT_BODY
            c.border = BORDER
            c.alignment = ALIGN_LEFT
    ws.cell(row=33, column=1, value="Assicurazione").font = FONT_BOLD
    ws.cell(row=33, column=2, value="Heymondo — n. polizza e provider da annotare · app con chat medica 24/7").font = FONT_BODY
    ws.merge_cells("B33:F33")

    style_section(ws, 35, "F", "⚠️ ALLERGIE REBECCA — CRITICO")
    allergie = [
        "SOIA (shoyu, miso, tofu, edamame, natto, dashi) — ONNIPRESENTE",
        "PESCE (dashi, bonito, sushi) · CROSTACEI · FRUTTA SECCA",
        "BANANA · FRAGOLA · KIWI · ARANCIA · NICHEL (lieve: pomodoro, spinaci, cipolla)",
        "Rebecca deve cucinare da sola: TUTTI gli alloggi hanno cucina.",
        "Sicuri: Saizeriya (pasta aglio e olio), Matsuya (gyudon senza salsa), Sukiya (riso+uovo), yakiniku (carne non marinata, sale/limone), Royal Host, Shogun Burger.",
        "Portare SEMPRE il cartellino allergie in giapponese (plastificato).",
    ]
    for i, txt in enumerate(allergie):
        r = 36 + i
        c = ws.cell(row=r, column=1, value=("• " if i < 5 else "") + txt)
        c.font = FONT_BODY if i < 4 else FONT_SMALL
        c.alignment = ALIGN_LEFT
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        ws.row_dimensions[r].height = 28
    r = 36 + len(allergie) + 1
    ws.cell(row=r, column=1, value="Riferimenti nel vault: Lista Prenotazioni · Spese Reali · Allergie Alimentari Rebecca · "
                                   "Info pratiche · Attività e Prenotazioni · Trasferimento Bagagli (Takkyubin).").font = FONT_SMALL
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)



def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    website_root = os.path.dirname(script_dir)
    out_dir = os.path.join(website_root, "public", "downloads")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Giappone-2026-Companion.xlsx")

    img_tmp = tempfile.mkdtemp(prefix="sakura_")
    img_paths = generate_images(img_tmp)

    wb = Workbook()
    wb.remove(wb.active)

    config_names = build_config(wb, img_paths)
    build_itinerario(wb, img_paths)
    build_attivita(wb, img_paths)
    build_prenotazioni(wb, img_paths)
    build_spese(wb, img_paths)
    build_budget(wb, img_paths)
    build_scadenze(wb, img_paths)
    build_saldi(wb, img_paths, config_names)
    build_dashboard(wb, img_paths)
    build_logistica(wb, img_paths)

    # Defined Names globali
    for name, ref in config_names.items():
        add_name(wb, name, ref)
    add_name(wb, "Spese_Categoria", "SPESE!$C$5:$C$124")
    add_name(wb, "Spese_ImportoTot", "SPESE!$G$5:$G$124")
    add_name(wb, "Spese_PagatoDa", "SPESE!$H$5:$H$124")
    add_name(wb, "Spese_P1", "SPESE!$I$5:$I$124")
    add_name(wb, "Spese_P2", "SPESE!$J$5:$J$124")
    add_name(wb, "Spese_P3", "SPESE!$K$5:$K$124")
    add_name(wb, "Spese_QuotaPax", "SPESE!$M$5:$M$124")
    add_name(wb, "Pren_Stato", "PRENOTAZIONI!$N$5:$N$54")
    add_name(wb, "Pren_Voce", "PRENOTAZIONI!$A$5:$A$54")
    add_name(wb, "Att_Giorno", "'ATTIVITÀ'!$A$5:$A$300")
    add_name(wb, "Att_Stato", "'ATTIVITÀ'!$I$5:$I$300")
    add_name(wb, "Att_Attivita", "'ATTIVITÀ'!$D$5:$D$300")

    # ordine fogli
    order = ["DASHBOARD", "ITINERARIO", "ATTIVITÀ", "PRENOTAZIONI", "SPESE", "BUDGET",
             "SCADENZE", "SALDI", "LOGISTICA", "CONFIG"]
    wb._sheets = [wb[n] for n in order]
    wb.active = 0

    wb.properties.title = "Giappone 2026 — Companion"
    wb.properties.creator = "Travel-Vault"
    wb.properties.description = "Tracker itinerario, prenotazioni, spese e scadenze — Giappone 23 ott / 6 nov 2026"
    wb.calculation.fullCalcOnLoad = True

    wb.save(out_path)
    print(f"OK -> {out_path}")
    return out_path


if __name__ == "__main__":
    main()
