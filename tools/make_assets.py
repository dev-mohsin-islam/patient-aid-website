"""
Generate brand placeholder artwork for the Patient Aid marketing site.

The site uses genuine app screenshots in assets/img/screens/ (see
tools/process_uploads.py). This script only regenerates the logo, favicon,
touch icon, and social preview.

The legacy demo-screen functions are kept for reference but are no longer
called.

Usage:
    python tools/make_assets.py

Requires: Pillow (only for the PNG social preview + touch icon).
"""

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SCREENS = ROOT / "assets" / "img" / "screens"
IMG = ROOT / "assets" / "img"

PRIMARY = "#1686D9"
PRIMARY_DARK = "#0E6BB5"
SECONDARY = "#00A8B5"
SECONDARY_DARK = "#008A95"
INK = "#18324B"
MUTED = "#6B7C8F"
LINE = "#E2ECF5"
SOFT = "#EFF7FD"
SOFT_TEAL = "#E6F7F8"
WHITE = "#FFFFFF"
BG = "#F7FAFD"

FONT = "'Inter','Segoe UI',system-ui,-apple-system,Arial,sans-serif"

W, H = 390, 820


# --------------------------------------------------------------------------- #
# primitives
# --------------------------------------------------------------------------- #
def rect(x, y, w, h, rx=0, fill=WHITE, stroke=None, sw=1, opacity=None):
    attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"', f'rx="{rx}"',
             f'fill="{fill}"']
    if stroke:
        attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"']
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return f'<rect {" ".join(attrs)}/>'


def circle(cx, cy, r, fill, opacity=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{op}/>'


def text(x, y, value, size=13, weight=500, fill=INK, anchor="start", opacity=None,
         spacing=None):
    attrs = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'font-weight="{weight}"',
             f'fill="{fill}"']
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    return f'<text {" ".join(attrs)}>{escape(value)}</text>'


def bar(x, y, w, h=8, fill=LINE, rx=None):
    return rect(x, y, w, h, rx if rx is not None else h / 2, fill)


def path(d, fill="none", stroke=INK, sw=1.6, cap="round", join="round", opacity=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="{cap}" stroke-linejoin="{join}"{op}/>')


def chip(x, y, w, h, label, fill=SOFT, color=PRIMARY_DARK, size=10.5, rx=None):
    return (rect(x, y, w, h, rx if rx is not None else h / 2, fill) +
            text(x + w / 2, y + h / 2 + 3.6, label, size, 600, color, "middle"))


def status_bar(dark=False):
    c = "#FFFFFF" if dark else INK
    parts = [
        text(22, 22, "9:41", 11, 600, c),
        rect(322, 13, 3.5, 9, 1.5, c),
        rect(327.5, 11, 3.5, 11, 1.5, c),
        rect(333, 9, 3.5, 13, 1.5, c),
        rect(338.5, 7, 3.5, 15, 1.5, c),
        # wifi arc
        path("M347 16c2.3-2.4 5.2-3.7 8.3-3.7s6 1.3 8.3 3.7", "none", c, 1.5),
        path("M349.6 18.8c1.6-1.7 3.5-2.6 5.7-2.6s4.1.9 5.7 2.6", "none", c, 1.5),
        circle(355.3, 21.4, 1.3, c),
        rect(367, 9.5, 17, 9, 2.6, "none", c, 1.2),
        rect(368.4, 10.9, 12.4, 6.2, 1.4, c),
        rect(385, 12.2, 1.8, 4.6, 0.9, c, opacity=0.6),
    ]
    return "".join(parts)


def bottom_nav(active=0):
    labels = ["Home", "Medicines", "My Medicine", "More"]
    icons = [
        "M4 11.5 12 5l8 6.5V20a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z",
        "M9 3h6v4h4v4h-4v6H9v-6H5V7h4z",
        "M7 4h10a2 2 0 0 1 2 2v14l-7-4-7 4V6a2 2 0 0 1 2-2z",
        "M5 7h14M5 12h14M5 17h9",
    ]
    parts = [rect(0, 754, W, 66, 0, WHITE), rect(0, 754, W, 1, 0, LINE)]
    for i, label in enumerate(labels):
        cx = 48 + i * 98
        color = PRIMARY if i == active else "#9AAEBF"
        parts.append(f'<g transform="translate({cx - 11},757)">')
        parts.append(path(icons[i], "none", color, 1.7))
        parts.append("</g>")
        parts.append(text(cx, 800, label, 8.6, 600 if i == active else 500,
                          PRIMARY if i == active else "#9AAEBF", "middle"))
    return "".join(parts)


def header(title, dark=False, back=True, action=None):
    y = 40
    parts = [rect(0, 0, W, y + 52, 0, PRIMARY if dark else WHITE)]
    if not dark:
        parts.append(rect(0, y + 51, W, 1, 0, LINE))
    c = "#FFFFFF" if dark else INK
    if back:
        parts.append(path(f"M{c and 4 or 4} 0", "none", c, 0))
        parts.append(path("M20 62h-8m0 0 4-4m-4 4 4 4", "none", c, 2))
    parts.append(text(W / 2, 68, title, 15, 650, c, "middle"))
    if action == "bookmark":
        parts.append(path("M368 54h9v16l-4.5-3-4.5 3z", "none", c, 1.7))
    elif action == "plus":
        parts.append(path("M366 60h14M373 53v14", "none", c, 2))
    return "".join(parts)


def search_bar(y=104, placeholder="Search medicines, diseases…", teal=False):
    return "".join([
        rect(20, y, 350, 42, 21, SOFT_TEAL if teal else "#F1F6FA"),
        circle(41, y + 21, 7.5, "none"),
        path(f"M46 {y + 26}l4.5 4.5", "none", MUTED, 1.7),
        text(58, y + 25.5, placeholder, 12, 500, "#8698AA"),
    ])


def list_row(y, title, subtitle, icon_fill=SOFT, icon_color=PRIMARY, tag=None):
    parts = [
        rect(20, y, 350, 62, 14, WHITE, LINE),
        rect(32, y + 13, 36, 36, 11, icon_fill),
        circle(50, y + 31, 7, icon_color, 0.85),
        text(80, y + 27, title, 13, 600, INK),
        text(80, y + 45, subtitle, 10.5, 500, MUTED),
        path(f"M352 {y + 25}l4 6-4 6", "none", "#A9BCCA", 1.8),
    ]
    if tag:
        parts.append(chip(298, y + 21, 46, 20, tag, SOFT_TEAL, SECONDARY_DARK, 9.5))
    return "".join(parts)


def svg(inner, bg=BG):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" font-family="{FONT}">'
        f'<rect width="{W}" height="{H}" fill="{bg}"/>{inner}</svg>\n'
    )


# --------------------------------------------------------------------------- #
# screens
# --------------------------------------------------------------------------- #
def screen_home():
    p = [
        f'<defs><linearGradient id="hero" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#1686D9"/><stop offset="1" stop-color="#00A8B5"/>'
        f'</linearGradient></defs>',
        rect(0, 0, W, 300, 0, "url(#hero)"),
        circle(330, 40, 90, "#FFFFFF", 0.08),
        circle(30, 250, 70, "#FFFFFF", 0.07),
        status_bar(dark=True),
        text(22, 76, "Patient Aid", 21, 700, WHITE),
        text(22, 98, "Your healthcare companion", 11.5, 500, "#D8F0F6"),
        rect(20, 116, 350, 44, 22, WHITE, opacity=0.96),
        circle(42, 138, 8, "none"),
        path("M47 143l5 5", "none", MUTED, 1.8),
        text(60, 142, "Search medicines, diseases…", 11.5, 500, "#8698AA"),
        # quick action card
        rect(20, 180, 350, 150, 18, WHITE),
        text(36, 206, "Quick access", 12, 650, INK),
    ]

    tiles = [
        ("Medicine", "M9 3h6v4h4v4h-4v6H9v-6H5V7h4z", SOFT, PRIMARY),
        ("Diseases", "M12 21s-7-4.4-7-9a4 4 0 0 1 7-2.6A4 4 0 0 1 19 12c0 4.6-7 9-7 9z", SOFT_TEAL, SECONDARY),
        ("Doctors", "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0", "#EEF2FF", "#4B5BD7"),
    ]
    for i, (label, d, bgc, color) in enumerate(tiles):
        x = 34 + i * 108
        p += [rect(x, 218, 94, 46, 12, bgc),
              f'<g transform="translate({x + 10},231)">', path(d, "none", color, 1.7), "</g>",
              text(x + 34, 246, label, 11, 600, INK)]
    rows = [
        ("Hospitals", "M4 21V8l8-4 8 4v13M9 21v-5h6v5"),
        ("Reminders", "M12 8v5l3 2M12 3a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"),
        ("Calculators", "M6 3h12v18H6zM9 7h6M9 11h2M13 11h2M9 15h2M13 15h2"),
    ]
    for i, (label, d) in enumerate(rows):
        x = 34 + i * 108
        p += [rect(x, 272, 94, 46, 12, "#F4F7FB"),
              f'<g transform="translate({x + 10},285)">', path(d, "none", "#5B7288", 1.7), "</g>",
              text(x + 34, 300, label, 10.5, 600, INK)]
    # popular medicines
    p += [text(20, 362, "Popular medicines", 13.5, 700, INK),
          text(370, 362, "See all", 10.5, 600, PRIMARY, "end")]
    meds = [("Napa", "Paracetamol 500 mg", "Tablet"),
            ("Seclo", "Omeprazole 20 mg", "Capsule"),
            ("Monas 10", "Montelukast 10 mg", "Tablet")]
    for i, (name, generic, form) in enumerate(meds):
        p.append(list_row(376 + i * 72, name, generic, tag=form))
    # health tips
    p += [text(20, 614, "Health tips", 13.5, 700, INK),
          rect(20, 628, 168, 108, 14, WHITE, LINE),
          rect(20, 628, 168, 52, 14, "#DCEFF9"),
          rect(20, 668, 168, 12, 0, "#DCEFF9"),
          text(34, 706, "Staying hydrated", 11, 600, INK),
          text(34, 722, "5 tips for summer", 9.5, 500, MUTED),
          rect(202, 628, 168, 108, 14, WHITE, LINE),
          rect(202, 628, 168, 52, 14, "#D9F2F3"),
          rect(202, 668, 168, 12, 0, "#D9F2F3"),
          text(216, 706, "First aid basics", 11, 600, INK),
          text(216, 722, "Everyday safety", 9.5, 500, MUTED),
          bottom_nav(0)]
    return svg("".join(p))


def screen_medicines():
    p = [status_bar(), header("Medicines"),
         search_bar(104, "Search by brand or generic"),
         chip(20, 160, 48, 28, "All", PRIMARY, WHITE),
         chip(74, 160, 82, 28, "Analgesic"),
         chip(162, 160, 78, 28, "Antibiotic"),
         chip(246, 160, 62, 28, "Antacid"),
         chip(314, 160, 56, 28, "Cardiac")]
    for i, (name, generic, tag) in enumerate([
        ("Napa Extend", "Paracetamol 665 mg", "Tablet"),
        ("Seclo 20", "Omeprazole 20 mg", "Capsule"),
        ("Monas 10", "Montelukast 10 mg", "Tablet"),
        ("Fexo 120", "Fexofenadine 120 mg", "Tablet"),
        ("Maxpro 20", "Esomeprazole 20 mg", "Capsule"),
        ("Ceevit", "Vitamin C 250 mg", "Tablet"),
        ("Sergel 20", "Esomeprazole 20 mg", "Capsule"),
        ("Losartan 50", "Losartan Potassium 50 mg", "Tablet"),
    ]):
        p.append(list_row(202 + i * 68, name, generic, tag=tag))
    p.append(bottom_nav(1))
    return svg("".join(p))


def screen_drug():
    p = [status_bar(), header("Medicine details", action="bookmark"),
         rect(20, 104, 350, 96, 16, WHITE, LINE),
         text(36, 132, "Napa Extend", 18, 700, INK),
         text(36, 152, "Paracetamol 665 mg", 11.5, 500, MUTED),
         chip(36, 164, 58, 22, "Tablet", SOFT, PRIMARY_DARK, 9.5),
         chip(100, 164, 84, 22, "Analgesic", SOFT_TEAL, SECONDARY_DARK, 9.5),
         # tabs
         rect(20, 216, 350, 38, 12, "#F1F6FA"),
         rect(24, 220, 112, 30, 9, WHITE),
         text(80, 240, "Overview", 10.5, 650, PRIMARY_DARK, "middle"),
         text(196, 240, "Dosage", 10.5, 550, MUTED, "middle"),
         text(302, 240, "Side effects", 10.5, 550, MUTED, "middle"),
         text(20, 286, "Indications", 12.5, 700, INK),
         bar(20, 298, 350), bar(20, 314, 338), bar(20, 330, 300),
         text(20, 372, "Dosage & administration", 12.5, 700, INK),
         bar(20, 384, 348), bar(20, 400, 356), bar(20, 416, 240),
         text(20, 458, "Contraindications", 12.5, 700, INK),
         bar(20, 470, 340), bar(20, 486, 318),
         text(20, 528, "Precautions", 12.5, 700, INK),
         bar(20, 540, 350), bar(20, 556, 286),
         rect(20, 588, 350, 70, 14, "#FFF8E8", "#F3E4BD"),
         path("M34 608h0", "none", "#C4761A", 0),
         circle(42, 614, 8, "#E8B457"),
         text(42, 618, "!", 10, 800, WHITE, "middle"),
         text(58, 612, "Read the label before use", 11, 650, "#7A5B12"),
         text(58, 628, "Always follow your doctor's advice.", 9.5, 500, "#8B6E2A"),
         text(58, 644, "Keep out of reach of children.", 9.5, 500, "#8B6E2A"),
         text(20, 690, "Pack size & price", 12.5, 700, INK),
         rect(20, 702, 350, 44, 12, WHITE, LINE),
         text(36, 729, "Box of 10 × 10 tablets", 10.5, 550, INK),
         text(354, 729, "BDT 120.00", 10.5, 650, PRIMARY_DARK, "end"),
         bottom_nav(1)]
    return svg("".join(p))


def screen_diseases():
    p = [status_bar(), header("Diseases"), search_bar(104, "Search diseases")]
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for i, letter in enumerate(letters):
        x = 20 + i * 35
        active = i == 2
        p.append(circle(x + 13, 178, 13, PRIMARY if active else "#F1F6FA"))
        p.append(text(x + 13, 182, letter, 10.5, 650, WHITE if active else MUTED, "middle"))
    diseases = [
        ("Common Cold", "Viral infection of the nose and throat", "#DCEFF9", PRIMARY),
        ("Diabetes", "Chronic condition affecting blood sugar", "#D9F2F3", SECONDARY),
        ("Hypertension", "Persistently high blood pressure", "#EEF2FF", "#4B5BD7"),
        ("Dengue Fever", "Mosquito-borne viral infection", "#FDEBD3", "#C4761A"),
        ("Asthma", "Long-term inflammation of the airways", "#E8F6EC", "#2E8B57"),
    ]
    for i, (title, subtitle, bgc, color) in enumerate(diseases):
        y = 206 + i * 76
        p += [rect(20, y, 350, 66, 14, WHITE, LINE),
              rect(32, y + 15, 36, 36, 11, bgc),
              circle(50, y + 33, 8, color, 0.85),
              text(80, y + 29, title, 13, 600, INK),
              text(80, y + 47, subtitle, 9.8, 500, MUTED),
              path(f"M352 {y + 27}l4 6-4 6", "none", "#A9BCCA", 1.8)]
    p += [rect(20, 596, 350, 54, 27, PRIMARY),
          text(195, 629, "Browse all diseases", 12, 650, WHITE, "middle"),
          bottom_nav(3)]
    return svg("".join(p))


def screen_directory():
    p = [status_bar(), header("Doctor & Hospital"), search_bar(104, "Search doctors, chambers"),
         rect(20, 160, 350, 38, 12, "#F1F6FA"),
         rect(24, 164, 112, 30, 9, WHITE),
         text(80, 184, "Doctors", 10.5, 650, PRIMARY_DARK, "middle"),
         text(196, 184, "Hospitals", 10.5, 550, MUTED, "middle"),
         text(306, 184, "Ambulance", 10.5, 550, MUTED, "middle")]
    doctors = [
        ("Dr. A. Rahman", "Medicine specialist", "Labaid, Dhanmondi", "#DCEFF9", PRIMARY),
        ("Dr. S. Akter", "Gynaecologist", "Square Hospital", "#FDE9EF", "#C2506E"),
        ("Dr. M. Hasan", "Cardiologist", "National Heart Foundation", "#D9F2F3", SECONDARY),
    ]
    for i, (name, specialty, chamber, bgc, color) in enumerate(doctors):
        y = 216 + i * 92
        p += [rect(20, y, 350, 82, 14, WHITE, LINE),
              circle(52, y + 41, 20, bgc),
              circle(52, y + 34, 7, color),
              path(f"M40 {y + 52}a12 9 0 0 1 24 0", "none", color, 3),
              text(84, y + 30, name, 13, 650, INK),
              text(84, y + 47, specialty, 10.5, 550, MUTED),
              path(f"M84 {y + 64}h9", "none", PRIMARY, 1.6),
              text(98, y + 67, chamber, 9.6, 500, "#7E93A6"),
              chip(300, y + 16, 54, 22, "Profile", SOFT, PRIMARY_DARK, 9)]
    p += [rect(20, 494, 350, 76, 14, "url(#none)", "#E7F1F8"),
          rect(20, 494, 350, 76, 14, "#EFF7FD"),
          rect(34, 508, 44, 44, 13, "#FFE8CC"),
          text(56, 537, "+", 22, 700, "#C4761A", "middle"),
          text(90, 522, "Ambulance service", 12.5, 650, INK),
          text(90, 540, "Find nearby ambulance contacts", 9.8, 500, MUTED),
          text(90, 556, "Available in the healthcare directory", 9.8, 500, MUTED),
          text(20, 606, "Hospitals near you", 13.5, 700, INK)]
    for i, (name, area) in enumerate([("Square Hospital", "Panthapath"), ("Labaid Hospital", "Dhanmondi")]):
        y = 620 + i * 66
        p += [rect(20, y, 350, 56, 12, WHITE, LINE),
              rect(32, y + 12, 32, 32, 9, "#E8F6EC"),
              text(48, y + 33, "+", 15, 700, "#2E8B57", "middle"),
              text(76, y + 26, name, 12, 600, INK),
              text(76, y + 42, area, 9.8, 500, MUTED),
              path(f"M352 {y + 24}l4 6-4 6", "none", "#A9BCCA", 1.8)]
    p.append(bottom_nav(3))
    return svg("".join(p))


def screen_reminder():
    p = [status_bar(), header("Medicine Reminder", action="plus"),
         rect(20, 104, 350, 66, 14, "#F1F6FA"),
         circle(52, 137, 17, WHITE),
         text(52, 142, "12", 13, 700, PRIMARY, "middle"),
         text(80, 132, "Today", 12.5, 650, INK),
         text(80, 149, "3 reminders scheduled", 10, 500, MUTED),
         chip(296, 126, 58, 22, "Tomorrow", SOFT_TEAL, SECONDARY_DARK, 9)]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, d in enumerate(days):
        x = 30 + i * 48
        active = i == 3
        p += [circle(x, 200, 16, PRIMARY if active else "#F1F6FA"),
              text(x, 204, str(10 + i), 10.5, 650, WHITE if active else MUTED, "middle"),
              text(x, 228, d, 8.6, 550, MUTED, "middle")]
    reminders = [
        ("8:00 AM", "Napa Extend", "1 tablet · After breakfast", "#DCEFF9", PRIMARY),
        ("2:00 PM", "Seclo 20", "1 capsule · Before lunch", "#D9F2F3", SECONDARY),
        ("9:30 PM", "Monas 10", "1 tablet · Before sleep", "#EEF2FF", "#4B5BD7"),
    ]
    for i, (time_, name, dose, bgc, color) in enumerate(reminders):
        y = 250 + i * 96
        p += [rect(20, y, 350, 84, 16, WHITE, LINE),
              rect(20, y, 4, 84, 2, color),
              rect(36, y + 14, 58, 56, 12, bgc),
              text(65, y + 38, time_.split(" ")[0], 11.5, 700, color, "middle"),
              text(65, y + 53, time_.split(" ")[1], 8.6, 600, color, "middle"),
              text(108, y + 32, name, 13, 650, INK),
              text(108, y + 50, dose, 9.8, 500, MUTED),
              rect(300, y + 30, 44, 24, 12, "#D8F0E4"),
              circle(332, y + 42, 9, "#2E8B57"),
              text(108, y + 68, "Daily", 9, 550, "#7E93A6")]
    p += [rect(20, 550, 350, 56, 28, PRIMARY),
          text(195, 585, "+  Add reminder", 13, 650, WHITE, "middle"),
          text(20, 640, "Upcoming", 13.5, 700, INK),
          rect(20, 654, 350, 62, 14, WHITE, LINE),
          text(36, 680, "Vitamin D3", 12, 600, INK),
          text(36, 697, "Tomorrow · 10:00 AM", 9.8, 500, MUTED),
          chip(300, 674, 54, 22, "Once", SOFT, PRIMARY_DARK, 9),
          bottom_nav(0)]
    return svg("".join(p))


def screen_tips():
    p = [status_bar(), header("Health Tips")]
    p += [rect(20, 104, 350, 160, 18, "#DCEFF9"),
          circle(300, 140, 70, "#FFFFFF", 0.4),
          circle(120, 240, 50, "#FFFFFF", 0.35),
          text(36, 128, "FEATURED", 8.6, 700, PRIMARY_DARK, spacing="1.4"),
          text(36, 162, "Healthy habits for", 17, 700, INK),
          text(36, 184, "a stronger heart", 17, 700, INK),
          text(36, 208, "Simple daily practices for better health", 9.8, 500, "#4A6A85"),
          rect(36, 222, 96, 26, 13, WHITE),
          text(84, 239, "Read more", 9.6, 650, PRIMARY_DARK, "middle")]
    for i, (title, sub, bgc, color) in enumerate([
        ("First aid basics", "Everyday safety guidance", "#D9F2F3", SECONDARY),
        ("Nutrition & diet", "Eating well, every day", "#FDEBD3", "#C4761A"),
    ]):
        y = 284 + i * 84
        p += [rect(20, y, 350, 72, 14, WHITE, LINE),
              rect(32, y + 12, 48, 48, 12, bgc),
              circle(56, y + 36, 10, color, 0.85),
              text(94, y + 32, title, 12.5, 650, INK),
              text(94, y + 50, sub, 9.8, 500, MUTED),
              path(f"M352 {y + 30}l4 6-4 6", "none", "#A9BCCA", 1.8)]
    p += [text(20, 486, "All articles", 13.5, 700, INK)]
    for i, t in enumerate(["Managing fever at home", "Safe use of antibiotics",
                           "Staying active after 40", "Sleep and your health"]):
        y = 500 + i * 60
        p += [rect(20, y, 350, 50, 12, WHITE, LINE),
              text(34, y + 29, t, 11.5, 600, INK),
              path(f"M352 {y + 19}l4 6-4 6", "none", "#A9BCCA", 1.8)]
    p.append(bottom_nav(3))
    return svg("".join(p))


def screen_calculators():
    p = [status_bar(), header("Medical Calculators")]
    tiles = [("BMI", "#DCEFF9", PRIMARY), ("IBW", "#D9F2F3", SECONDARY), ("EDD", "#EEF2FF", "#4B5BD7")]
    for i, (label, bgc, color) in enumerate(tiles):
        x = 20 + i * 118
        p += [rect(x, 104, 108, 82, 16, bgc),
              circle(x + 54, 134, 14, WHITE),
              text(x + 54, 139, label, 9.6, 700, color, "middle"),
              text(x + 54, 166, label, 11, 650, INK, "middle")]
    p += [rect(20, 202, 350, 150, 18, WHITE, LINE),
          text(36, 228, "Body Mass Index (BMI)", 11.5, 650, MUTED),
          text(36, 274, "23.4", 34, 750, PRIMARY_DARK),
          chip(120, 252, 62, 24, "Normal", "#D8F0E4", "#2E8B57", 10),
          text(36, 296, "kg/m²  ·  Height 170 cm  ·  Weight 68 kg", 9.4, 500, MUTED),
          rect(36, 314, 318, 8, 4, "#EDF3F8"),
          rect(36, 314, 164, 8, 4, "#2E8B57"),
          text(36, 338, "18.5", 8, 500, "#9AAEBF"),
          text(195, 338, "25", 8, 500, "#9AAEBF"),
          text(354, 338, "30", 8, 500, "#9AAEBF", "end")]
    p += [rect(20, 368, 350, 90, 16, WHITE, LINE),
          text(36, 394, "Ideal Body Weight", 11.5, 650, INK),
          text(36, 414, "IBW  ·  Devine formula", 9.4, 500, MUTED),
          text(354, 414, "64.2 kg", 12, 700, SECONDARY_DARK, "end"),
          rect(36, 428, 318, 1, 0, LINE),
          text(36, 448, "Estimated Delivery Date", 11.5, 650, INK)]
    p += [rect(20, 474, 350, 100, 16, WHITE, LINE),
          text(36, 500, "EDD result", 11.5, 650, INK),
          text(36, 528, "12 Aug 2026", 18, 700, "#4B5BD7"),
          text(36, 550, "Based on last menstrual period", 9.4, 500, MUTED),
          chip(300, 500, 54, 22, "Info", SOFT, PRIMARY_DARK, 9)]
    p += [text(20, 616, "Weight charts", 13.5, 700, INK),
          rect(20, 630, 168, 100, 14, WHITE, LINE),
          text(36, 656, "Male", 11, 650, INK),
          rect(36, 672, 136, 1, 0, LINE),
          rect(36, 684, 40, 30, 4, "#DCEFF9"),
          rect(84, 676, 40, 38, 4, "#B9DCF4"),
          rect(132, 692, 40, 22, 4, "#DCEFF9"),
          rect(202, 630, 168, 100, 14, WHITE, LINE),
          text(218, 656, "Female", 11, 650, INK),
          rect(218, 672, 136, 1, 0, LINE),
          rect(218, 680, 40, 34, 4, "#D9F2F3"),
          rect(266, 688, 40, 26, 4, "#AEE3E7"),
          rect(314, 694, 40, 20, 4, "#D9F2F3"),
          bottom_nav(3)]
    return svg("".join(p))


def screen_mymedicine():
    p = [status_bar(), header("My Medicine", action="plus"),
         rect(20, 104, 350, 56, 14, "#F1F6FA"),
         circle(46, 132, 15, "#FFFFFF"),
         text(46, 136, "S", 11, 700, PRIMARY, "middle"),
         text(70, 130, "Self", 12, 650, INK),
         text(70, 146, "4 medicines", 9.4, 500, MUTED),
         chip(300, 121, 54, 22, "Switch", SOFT, PRIMARY_DARK, 9)]
    meds = [("Napa Extend", "665 mg · 1 tablet, 8:00 AM", "#DCEFF9", PRIMARY),
            ("Seclo 20", "20 mg · 1 capsule, 2:00 PM", "#D9F2F3", SECONDARY),
            ("Monas 10", "10 mg · 1 tablet, 9:30 PM", "#EEF2FF", "#4B5BD7"),
            ("Ceevit", "250 mg · 1 tablet, 10:00 AM", "#FDEBD3", "#C4761A")]
    for i, (name, dose, bgc, color) in enumerate(meds):
        y = 176 + i * 74
        p += [rect(20, y, 350, 64, 14, WHITE, LINE),
              rect(34, y + 14, 34, 34, 10, bgc),
              circle(51, y + 31, 7, color, 0.85),
              text(80, y + 28, name, 12.5, 650, INK),
              text(80, y + 45, dose, 9.6, 500, MUTED),
              circle(344, y + 32, 10, "#E8F6EC"),
              path(f"M339 {y + 32}l4 4 7-8", "none", "#2E8B57", 2)]
    p += [rect(20, 486, 350, 54, 27, WHITE, PRIMARY, 1.4),
          path("M138 513h0", "none", PRIMARY, 0),
          text(195, 519, "Share medicine list", 12, 650, PRIMARY_DARK, "middle"),
          text(20, 574, "Family profiles", 13.5, 700, INK),
          text(370, 574, "Premium", 9.6, 650, SECONDARY_DARK, "end")]
    profiles = [("Father", "3 medicines", "#DCEFF9", PRIMARY),
                ("Mother", "5 medicines", "#FDE9EF", "#C2506E")]
    for i, (name, count, bgc, color) in enumerate(profiles):
        x = 20 + i * 182
        p += [rect(x, 588, 168, 92, 14, WHITE, LINE),
              circle(x + 28, 616, 15, bgc),
              circle(x + 28, 610, 5.4, color),
              path(f"M{x + 19} 625a9 7 0 0 1 18 0", "none", color, 2.4),
              text(x + 52, 614, name, 11.5, 650, INK),
              text(x + 52, 630, count, 9.2, 500, MUTED),
              path(f"M{x + 16} 662h136", "none", LINE, 1),
              text(x + 16, 670, "View list", 9.4, 600, PRIMARY_DARK)]
    p.append(bottom_nav(2))
    return svg("".join(p))


def screen_family():
    p = [status_bar(), header("Family Profiles", action="plus"),
         text(20, 128, "Manage medicines for everyone", 11.5, 500, MUTED)]
    people = [("Self", "#DCEFF9", PRIMARY), ("Father", "#D9F2F3", SECONDARY),
              ("Mother", "#FDE9EF", "#C2506E"), ("Add", "#F1F6FA", "#8FA3B4")]
    for i, (name, bgc, color) in enumerate(people):
        x = 32 + i * 88
        p += [circle(x + 24, 176, 26, bgc),
              text(x + 24, 181, name[0], 15, 700, color, "middle"),
              text(x + 24, 218, name, 10, 600, INK, "middle")]
    p += [rect(20, 240, 350, 110, 16, WHITE, LINE),
          circle(52, 274, 18, "#D9F2F3"),
          text(52, 279, "F", 12, 700, SECONDARY, "middle"),
          text(80, 268, "Father", 13, 650, INK),
          text(80, 286, "3 medicines · 2 reminders", 9.6, 500, MUTED),
          rect(36, 306, 318, 1, 0, LINE),
          text(36, 326, "Last updated 2 days ago", 9.2, 500, "#9AAEBF"),
          chip(292, 314, 62, 22, "View", SOFT, PRIMARY_DARK, 9),
          rect(20, 362, 350, 110, 16, WHITE, LINE),
          circle(52, 396, 18, "#FDE9EF"),
          text(52, 401, "M", 12, 700, "#C2506E", "middle"),
          text(80, 390, "Mother", 13, 650, INK),
          text(80, 408, "5 medicines · 3 reminders", 9.6, 500, MUTED),
          rect(36, 428, 318, 1, 0, LINE),
          text(36, 448, "Last updated today", 9.2, 500, "#9AAEBF"),
          chip(292, 436, 62, 22, "View", SOFT, PRIMARY_DARK, 9)]
    p += [rect(20, 492, 350, 150, 18, "#EFF7FD"),
          text(36, 522, "Premium family profiles", 12.5, 700, INK),
          text(36, 544, "Keep a separate medicine list", 10, 500, "#456A85"),
          text(36, 560, "for each family member.", 10, 500, "#456A85"),
          rect(36, 580, 318, 40, 20, PRIMARY),
          text(195, 605, "Explore Premium", 11, 650, WHITE, "middle")]
    p += [text(20, 684, "Shared lists", 12.5, 700, INK),
          rect(20, 698, 350, 46, 12, WHITE, LINE),
          text(36, 726, "Monthly medicine list", 11, 600, INK),
          text(354, 726, "Shared", 9, 600, SECONDARY_DARK, "end"),
          bottom_nav(2)]
    return svg("".join(p))


SCREEN_MAP = [
    ("01-home.svg", screen_home),
    ("02-medicine-search.svg", screen_medicines),
    ("03-drug-details.svg", screen_drug),
    ("04-disease-info.svg", screen_diseases),
    ("05-doctor-hospital.svg", screen_directory),
    ("06-medicine-reminder.svg", screen_reminder),
    ("07-health-tips.svg", screen_tips),
    ("08-medical-calculators.svg", screen_calculators),
    ("09-my-medicine.svg", screen_mymedicine),
    ("10-family-profiles.svg", screen_family),
]


def write_screens():
    SCREENS.mkdir(parents=True, exist_ok=True)
    for filename, builder in SCREEN_MAP:
        (SCREENS / filename).write_text(builder(), encoding="utf-8")
        print("wrote", filename)


def write_logo():
    """Wordmark: the official app icon plus typeset product name."""
    import base64

    icon_data = base64.b64encode((IMG / "patient-aid-icon.png").read_bytes()).decode("ascii")
    svg_logo = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 64" width="240" height="64" '
        'role="img" aria-label="Patient Aid">'
        f'<image x="0" y="8" width="48" height="48" href="data:image/png;base64,{icon_data}"/>'
        f'<text x="62" y="34" font-family="{FONT}" font-size="22" font-weight="750" fill="{INK}">Patient Aid</text>'
        f'<text x="62" y="52" font-family="{FONT}" font-size="9.5" font-weight="650" '
        f'letter-spacing="2.1" fill="{MUTED}">BY ITMEDICUS</text>'
        '</svg>\n'
    )
    (IMG / "patient-aid-logo.svg").write_text(svg_logo, encoding="utf-8")
    print("wrote patient-aid-logo.svg")


def write_favicon():
    """SVG favicon that embeds the official raster icon, for crisp tab display."""
    import base64

    icon_data = base64.b64encode((IMG / "patient-aid-icon.png").read_bytes()).decode("ascii")
    favicon = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96">'
        f'<image width="96" height="96" href="data:image/png;base64,{icon_data}"/>'
        '</svg>\n'
    )
    (ROOT / "favicon.svg").write_text(favicon, encoding="utf-8")
    print("wrote favicon.svg")


def write_png_assets():
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError:
        print("Pillow not available — skipping PNG assets")
        return

    def font(size, bold=True):
        candidates = [
            r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                continue
        return ImageFont.load_default()

    # ---- Open Graph image (1200x630) ----
    W_, H_ = 1200, 630
    img = Image.new("RGB", (W_, H_), "#0F2A40")
    d = ImageDraw.Draw(img)
    # soft gradient wash
    for y in range(H_):
        t = y / H_
        r = int(0x0F + (0x0B) * t)
        g = int(0x2A + (0x4A) * t)
        b = int(0x40 + (0x5C) * t)
        d.line([(0, y), (W_, y)], fill=(r, g, b))
    # glow
    glow = Image.new("RGB", (W_, H_), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([760, -260, 1500, 420], fill=(0, 90, 105))
    img = Image.blend(img, glow, 0.35)
    d = ImageDraw.Draw(img)

    # official app icon in the top-left corner
    icon = Image.open(IMG / "patient-aid-icon.png").convert("RGBA").resize((64, 64), Image.LANCZOS)
    img.paste(icon, (80, 92), icon)

    d.text((168, 96), "Patient Aid", font=font(40), fill="#FFFFFF")
    d.text((170, 146), "BY ITMEDICUS SOLUTIONS", font=font(15), fill="#7FB3CE")

    d.text((80, 226), "Your Complete", font=font(64), fill="#FFFFFF")
    d.text((80, 300), "Healthcare Companion", font=font(64), fill="#FFFFFF")
    d.text((80, 392), "Offline healthcare information in Bangla & English", font=font(27, False), fill="#A8C8DC")
    d.text((80, 432), "for the people of Bangladesh.", font=font(27, False), fill="#A8C8DC")

    # store chip
    d.rounded_rectangle([80, 500, 392, 562], radius=31, fill="#0B1B29", outline="#2B4A63", width=2)
    d.polygon([(112, 516), (112, 546), (136, 531)], fill="#4FD1C5")
    d.text((150, 518), "GET IT ON", font=font(12), fill="#9FB6C8")
    d.text((150, 534), "Google Play", font=font(22), fill="#FFFFFF")

    # phone silhouette
    d.rounded_rectangle([872, 70, 1112, 590], radius=46, fill="#0A1A28", outline="#2B4358", width=3)

    # genuine home screen inside the phone
    x0, y0, x1, y1 = 888, 86, 1096, 574
    shot = Image.open(SCREENS / "home.webp").convert("RGB")
    fitted = ImageOps.fit(shot, (x1 - x0, y1 - y0), method=Image.LANCZOS)
    screen_mask = Image.new("L", fitted.size, 0)
    ImageDraw.Draw(screen_mask).rounded_rectangle(
        [0, 0, fitted.size[0] - 1, fitted.size[1] - 1], radius=34, fill=255
    )
    img.paste(fitted, (x0, y0), screen_mask)

    img.save(IMG / "og-image.png", optimize=True)
    print("wrote og-image.png")

    # ---- Touch icon (180x180) and favicon, built from the official icon ----
    app_icon = Image.open(IMG / "patient-aid-icon.png").convert("RGBA")
    full_icon = Image.new("RGBA", (512, 512), (0, 96, 138, 255))
    full_icon.alpha_composite(app_icon.resize((512, 512), Image.LANCZOS))

    full_icon.convert("RGB").resize((180, 180), Image.LANCZOS).save(
        IMG / "apple-touch-icon.png", optimize=True
    )
    print("wrote apple-touch-icon.png")

    full_icon.convert("RGB").resize((32, 32), Image.LANCZOS).save(
        ROOT / "favicon-32.png", optimize=True
    )
    print("wrote favicon-32.png")


if __name__ == "__main__":
    write_logo()
    write_favicon()
    write_png_assets()
