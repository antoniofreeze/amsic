#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara gli asset del sito AMSIC partendo dagli originali.
Uso:  python3 prepara_asset.py
- foto: da _originali/ (non pubblicata) → assets/img/<nome>-<larghezza>.webp|jpg
- logo, favicon, immagine di condivisione (og) → assets/logo/, assets/img/
- PDF del Modello 231 → assets/documenti/ con nomi leggibili
Va rilanciato solo se cambiano foto, logo o documenti; per i testi basta build.py.
"""
import os, re, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(ROOT, "_originali")
IMG = os.path.join(ROOT, "assets/img")
LOGO = os.path.join(ROOT, "assets/logo")
DOC = os.path.join(ROOT, "assets/documenti")
CLIENTE = os.path.abspath(os.path.join(ROOT, "..", ".."))          # ARCHIVIO FREEZE/Clienti/AMSIC
PDF_SORGENTE = os.path.join(CLIENTE, "Documenti", "Fwd_ SITO")
for d in (IMG, LOGO, DOC):
    os.makedirs(d, exist_ok=True)

BLU = "#1F4D9B"
GRIGIO = "#5B5A58"

# ------------------------------------------------------------------ marchio (dal file Illustrator del cliente)
# poligono del simbolo, viewBox 0 0 595 595.28
MARCHIO = [(438.71, 285.48), (302.45, 151.16), (157.4, 296.08), (304.07, 443.77), (441.47, 308.66),
           (583.67, 309.8), (304.96, 591.78), (10.35, 294.78), (304.07, 3.5), (585.54, 285.48)]
PUNTI_MARCHIO = " ".join(f"{x} {y}" for x, y in MARCHIO)

# logo orizzontale: simbolo + scritta AMSIC in tracciati, sottotitolo come testo
def _logo_paths():
    """Copia esatta di tracciati e poligoni dal file Illustrator del cliente (senza le classi di stile)."""
    sorgente = os.path.join(CLIENTE, "Grafiche", "logo amsic_Tavola disegno 1-01.svg")
    testo = open(sorgente, encoding="utf-8").read()
    pezzi = re.findall(r'<(?:polygon|path) class="st[23]" ([^>]*)/>', testo)
    tag = re.findall(r'<(polygon|path) class="st[23]"', testo)
    assert len(pezzi) == 6, f"attesi 6 tracciati nel logo, trovati {len(pezzi)}"
    return "\n".join(f"<{t} {a.strip()}/>" for t, a in zip(tag, pezzi))

def svg_logo(colore_marchio, colore_testo):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 822.4 242.7" role="img" aria-label="AMSIC S.r.l. a Socio unico">
<g fill="{colore_marchio}">{_logo_paths()}</g>
<text x="293.73" y="219.82" fill="{colore_testo}" font-family="Arial, Helvetica, sans-serif" font-size="63.76">S.r.l. a Socio unico</text>
</svg>
'''

def scrivi(percorso, testo):
    with open(percorso, "w", encoding="utf-8") as f:
        f.write(testo)

def loghi():
    scrivi(os.path.join(LOGO, "amsic-logo.svg"), svg_logo(BLU, GRIGIO))
    scrivi(os.path.join(LOGO, "amsic-logo-bianco.svg"), svg_logo("#FFFFFF", "#C9D6EC"))
    scrivi(os.path.join(LOGO, "amsic-marchio.svg"),
           f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 595 595.28"><polygon fill="{BLU}" points="{PUNTI_MARCHIO}"/></svg>\n')
    # icone: simbolo blu su bianco (apple/android) e trasparente (favicon)
    def marchio_png(lato, sfondo, margine):
        S = 4  # supersampling per bordi puliti
        im = Image.new("RGBA", (lato * S, lato * S), sfondo)
        d = ImageDraw.Draw(im)
        area = lato * S * (1 - 2 * margine)
        k = area / 595.28
        off = lato * S * margine
        d.polygon([(off + x * k, off + y * k) for x, y in MARCHIO], fill=BLU)
        return im.resize((lato, lato), Image.LANCZOS)
    marchio_png(32, (0, 0, 0, 0), 0.02).save(os.path.join(LOGO, "favicon-32.png"))
    # Google mostra la favicon nei risultati solo se è quadrata e multipla di 48 px (48, 96, 144…)
    marchio_png(48, (255, 255, 255, 255), 0.06).convert("RGB").save(os.path.join(LOGO, "favicon-48.png"))
    marchio_png(96, (255, 255, 255, 255), 0.06).convert("RGB").save(os.path.join(LOGO, "favicon-96.png"))
    marchio_png(192, (255, 255, 255, 255), 0.12).convert("RGB").save(os.path.join(LOGO, "icon-192.png"))
    # favicon.ico nella radice del sito (16, 32 e 48 px), cercata da browser e motori di ricerca
    marchio_png(256, (255, 255, 255, 255), 0.06).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    marchio_png(180, (255, 255, 255, 255), 0.16).convert("RGB").save(os.path.join(LOGO, "apple-touch-icon.png"))
    marchio_png(512, (255, 255, 255, 255), 0.16).convert("RGB").save(os.path.join(LOGO, "icon-512.png"))

# ------------------------------------------------------------------ foto
def taglia(im, rapporto, fuoco=(0.5, 0.5)):
    """Ritaglia al rapporto L/A tenendo il punto di fuoco (0–1)."""
    w, h = im.size
    if w / h > rapporto:
        nw = int(h * rapporto)
        x = int((w - nw) * fuoco[0])
        return im.crop((x, 0, x + nw, h))
    nh = int(w / rapporto)
    y = int((h - nh) * fuoco[1])
    return im.crop((0, y, w, y + nh))

def esporta(im, nome, larghezze):
    for L in larghezze:
        if im.width < L:
            L = im.width
        r = im.resize((L, round(im.height * L / im.width)), Image.LANCZOS)
        r.save(os.path.join(IMG, f"{nome}-{L}.webp"), "WEBP", quality=80, method=6)
        r.save(os.path.join(IMG, f"{nome}-{L}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)

FOTO = [
    # nome sorgente, nome uscita, rapporto, fuoco, larghezze, ritaglio preliminare (frazioni l,t,r,b)
    ("raccolta.jpg", "raccolta", 3 / 2, (0.5, 0.75), (640, 1100), None),
    ("trasporto.jpg", "trasporto", 3 / 2, (0.5, 0.5), (640, 1100), (0, 0, 1, 0.86)),   # toglie la sfumatura bianca in basso
    ("recupero.webp", "recupero", 3 / 2, (0.5, 0.4), (640, 1100), None),
    ("intermediazione.jpg", "intermediazione", 3 / 2, (0.5, 0.35), (640, 800), None),
    ("consulenza.jpg", "consulenza", 3 / 2, (0.5, 0.6), (640, 1100), None),
    ("documentale.jpg", "documentale", 3 / 2, (0.4, 0.5), (640, 1100), None),
    ("compliance.jpg", "compliance", 3 / 2, (0.55, 0.5), (640, 1100), None),
    # quadrato per il rombo dell'apertura (home)
    ("recupero.webp", "rombo-recupero", 1, (0.5, 0.35), (420, 760), None),
    # chi siamo: i materiali con il marchio forniti dal cliente
    ("biglietto.png", "biglietto", 4 / 3, (0.5, 0.5), (700, 1100), None),
    ("tablet.png", "tablet", 4 / 3, (0.5, 0.5), (700, 1100), None),
]

def foto():
    for src, nome, rapporto, fuoco, larghezze, pre in FOTO:
        im = Image.open(os.path.join(ORIG, src)).convert("RGB")
        if pre:
            l, t, r, b = pre
            im = im.crop((int(im.width * l), int(im.height * t), int(im.width * r), int(im.height * b)))
        esporta(taglia(im, rapporto, fuoco), nome, larghezze)

# ------------------------------------------------------------------ immagine per la condivisione (1200×630)
def font(nomi, size):
    cartelle = [os.path.expanduser("~/Library/Fonts"), "/Library/Fonts", "/System/Library/Fonts/Supplemental"]
    for n in nomi:
        for c in cartelle:
            p = os.path.join(c, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def og():
    S = 2
    W, Hh = 1200 * S, 630 * S
    im = Image.new("RGB", (W, Hh), "#F3F6FB")
    d = ImageDraw.Draw(im)
    # grande simbolo tagliato sul lato destro
    k = 760 * S / 595.28
    ox, oy = 760 * S, -60 * S
    d.polygon([(ox + x * k, oy + y * k) for x, y in MARCHIO], fill="#DCE5F3")
    # simbolo + scritta
    k2 = 150 * S / 595.28
    ox2, oy2 = 90 * S, 110 * S
    d.polygon([(ox2 + x * k2, oy2 + y * k2) for x, y in MARCHIO], fill=BLU)
    f1 = font(["Archivo-Bold.ttf", "Arial Bold.ttf"], 128 * S)
    f2 = font(["Inter.ttf", "Arial.ttf"], 34 * S)
    f3 = font(["Archivo-Bold.ttf", "Arial Bold.ttf"], 50 * S)
    d.text((270 * S, 112 * S), "AMSIC", font=f1, fill=BLU)
    d.text((274 * S, 245 * S), "S.r.l. a Socio unico", font=f2, fill=GRIGIO)
    d.text((90 * S, 380 * S), "Gestione sicura,", font=f3, fill="#14213A")
    d.text((90 * S, 440 * S), "ambiente protetto.", font=f3, fill="#14213A")
    d.text((90 * S, 530 * S), "Intermediazione rifiuti speciali · Catania", font=f2, fill="#3E4A5E")
    im.resize((1200, 630), Image.LANCZOS).save(os.path.join(IMG, "condivisione.jpg"), "JPEG", quality=88)

# ------------------------------------------------------------------ PDF del Modello 231
DOCUMENTI = [
    ("AMSIC - Parte Generale_2024_10_12.pdf", "amsic-modello-231-parte-generale.pdf"),
    ("AMSIC - Parte Speciale_rev.00_2024_10_12.pdf", "amsic-modello-231-parte-speciale.pdf"),
    ("AMSIC - Codice Etico_rev.00_2024_10_12.pdf", "amsic-codice-etico.pdf"),
    ("AMSIC - Sistema disciplinare_rev.00_2024_10_12.pdf", "amsic-sistema-disciplinare.pdf"),
    ("AMSIC - Sistema di gestione Whistleblowing_rev.00-2024_10_12 .pdf", "amsic-whistleblowing.pdf"),
    ("AMSIC - sistema delle procure e delle deleghe_rev.00_2024_10 _12.pdf", "amsic-procure-e-deleghe.pdf"),
    ("AMSIC- Segnalazioni e Flussi Informativi verso l (2)", "amsic-flussi-informativi-odv.pdf"),
]

def documenti():
    for src, dst in DOCUMENTI:
        shutil.copyfile(os.path.join(PDF_SORGENTE, src), os.path.join(DOC, dst))

if __name__ == "__main__":
    loghi(); foto(); og(); documenti()
    print("asset pronti:", len(os.listdir(IMG)), "immagini,", len(os.listdir(DOC)), "documenti")
