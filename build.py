#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore statico del sito AMSIC S.r.l. a Socio unico.
Uso:  python3 build.py   → scrive le pagine HTML, sitemap.xml e robots.txt nella cartella del progetto.
Tutti i contenuti (testi, servizi, recapiti, documenti) vivono qui: modifica e rilancia.
Le foto, il logo e i PDF si preparano con prepara_asset.py.
"""
import os, re, glob, json, datetime, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.amsic.it"          # dominio definitivo (canonical, sitemap, condivisione)
VERSIONE = "4"                         # ← aumentare a ogni modifica di CSS o JS (evita la cache dei browser)
ANNO = datetime.date.today().year
OGGI = datetime.date.today().isoformat()
AGGIORNAMENTO_PRIVACY = "20 ottobre 2026"

AZIENDA = {
    "nome": "AMSIC",
    "ragione_sociale": "AMSIC S.r.l. a Socio unico",
    "indirizzo": "Stradale Primosole 13",
    "cap": "95121",
    "citta": "Catania",
    "provincia": "CT",
    "piva": "05589250876",
    "rea": "",              # ← numero REA (es. "CT-123456"): vuoto = non mostrato
    "capitale": "",         # ← capitale sociale (es. "10.000,00 € i.v."): vuoto = non mostrato
    "tel": "351 964 7981",
    "tel_link": "+393519647981",
    "whatsapp": "",         # ← quando confermato: "393519647981" (attiva i pulsanti WhatsApp da telefono)
    "email": "direzioneamsic@gmail.com",
    "pec": "amsic@pec.impresacatania.it",
    "email_odv": "odvamsic@gmail.com",
    "albo_numero": "PA/015069",
    "albo_sezione": "Sezione regionale Sicilia (Palermo)",
    "albo_categoria": "Categoria 8 – intermediazione e commercio di rifiuti senza detenzione",
    "albo_classe": "Classe D – quantità annua trattata da 6.000 a meno di 15.000 tonnellate",
    "odv_presidente": "Prof. Avv. Giuseppe Berretta",
    "revisione_231": "rev. 00 del 12 ottobre 2024",
}
INDIRIZZO_COMPLETO = f'{AZIENDA["indirizzo"]}, {AZIENDA["cap"]} {AZIENDA["citta"]} ({AZIENDA["provincia"]})'
MAPPA_LINK = "https://www.google.com/maps/search/?api=1&query=" + "Stradale+Primosole+13,+95121+Catania+CT"
MAPPA_EMBED = "https://www.google.com/maps?q=Stradale+Primosole+13,+95121+Catania+CT&output=embed"
ENDPOINT_MODULO = "https://formsubmit.co/ajax/" + AZIENDA["email"]
ACTION_MODULO = "https://formsubmit.co/" + AZIENDA["email"]

# ---------------------------------------------------------------- contenuti
SERVIZI = [
    {
        "id": "intermediazione", "nome": "Intermediazione rifiuti", "foto": "intermediazione", "icona": "rete",
        "alt": "Stretta di mano sopra un contratto firmato",
        "breve": "Mettiamo in contatto chi produce i rifiuti con trasportatori e impianti autorizzati, alle migliori condizioni.",
        "testo": "Siamo iscritti all’Albo Nazionale Gestori Ambientali per l’intermediazione e il commercio di rifiuti senza detenzione (categoria 8, classe D). Per ogni rifiuto individuiamo soluzioni affidabili e conformi, tramite partner autorizzati e certificati, e cerchiamo per te le migliori condizioni tecnico-economiche offerte dal mercato. Ogni passaggio è verificato con sistemi di controllo interni e documentazione trasparente.",
        "punti": ["Rifiuti speciali pericolosi e non pericolosi", "Partner verificati con controlli interni", "Documentazione trasparente a ogni passaggio"],
    },
    {
        "id": "raccolta", "nome": "Raccolta rifiuti speciali", "foto": "raccolta", "icona": "fusto",
        "alt": "Fusti e contenitori per rifiuti speciali pronti per il ritiro",
        "breve": "Raccolta programmata o su richiesta, per aziende, enti pubblici e privati.",
        "testo": "Organizziamo la raccolta di rifiuti speciali pericolosi e non pericolosi nel pieno rispetto delle normative ambientali, con soluzioni personalizzate per aziende, enti pubblici e privati. Puoi attivare un servizio programmato oppure su richiesta: ogni intervento è affidato a operatori qualificati e autorizzati, per garantire efficienza e sicurezza.",
        "punti": ["Servizio programmato o su richiesta", "Operatori qualificati e autorizzati", "Soluzioni su misura per ogni produttore"],
    },
    {
        "id": "trasporto", "nome": "Trasporto rifiuti", "foto": "trasporto", "icona": "camion",
        "alt": "Camion scarrabile in un impianto di trattamento rifiuti",
        "breve": "Vettori autorizzati, carichi tracciati, ogni movimentazione monitorata.",
        "testo": "Affidiamo il trasporto dei rifiuti speciali, pericolosi e non pericolosi, a vettori autorizzati, dopo aver verificato l’idoneità del trasportatore e dei mezzi. Ogni trasferimento avviene in conformità alle normative nazionali e comunitarie e ogni movimentazione è monitorata, per assicurare trasparenza e affidabilità.",
        "punti": ["Verifica di trasportatore e mezzi", "Tracciabilità dei carichi", "Conformità alle norme nazionali ed europee"],
    },
    {
        "id": "recupero", "nome": "Smaltimento e recupero", "foto": "recupero", "icona": "ciclo",
        "alt": "Mani che raccolgono granuli di plastica riciclata",
        "breve": "Impianti autorizzati e, quando possibile, recupero dei materiali.",
        "testo": "Collaboriamo con impianti autorizzati per garantire uno smaltimento sicuro e controllato dei rifiuti. Promuoviamo il recupero dei materiali valorizzabili, contribuendo all’economia circolare e alla riduzione dell’impatto ambientale, e gestiamo le pratiche amministrative necessarie, sollevando il cliente da ogni onere burocratico.",
        "punti": ["Impianti autorizzati e verificati", "Priorità al recupero dei materiali", "Pratiche amministrative incluse"],
    },
    {
        "id": "consulenza", "nome": "Consulenza ambientale", "foto": "consulenza", "icona": "foglia",
        "alt": "Pale eoliche su una collina verde",
        "breve": "Supporto tecnico e normativo per gestire i rifiuti senza rischi di sanzioni.",
        "testo": "Offriamo un servizio di consulenza tecnica e normativa per supportare le imprese nella corretta gestione dei rifiuti. Assistiamo i clienti nella richiesta e nel rinnovo delle autorizzazioni ambientali e svolgiamo audit interni per verificare la conformità alle normative vigenti. L’obiettivo è semplificare i processi e prevenire i rischi sanzionatori.",
        "punti": ["Richiesta e rinnovo delle autorizzazioni ambientali", "Audit di conformità", "Prevenzione dei rischi sanzionatori"],
    },
    {
        "id": "documentale", "nome": "Gestione documentale", "foto": "documentale", "icona": "documento",
        "alt": "Pila di documenti e registri in un archivio",
        "breve": "Formulari, registri di carico e scarico e MUD sempre in ordine.",
        "testo": "Gestiamo l’intero flusso documentale legato alla movimentazione e allo smaltimento dei rifiuti, garantendo tracciabilità, archiviazione sicura e rispetto delle scadenze normative. Ci occupiamo della compilazione dei formulari di trasporto, dei registri di carico e scarico e del MUD, con precisione e conformità alle normative ambientali.",
        "punti": ["Formulari di trasporto", "Registri di carico e scarico", "MUD e scadenze annuali"],
    },
]

PASSI = [
    ("Analisi della richiesta", "Valutiamo con te il tipo di rifiuto, le quantità e la documentazione necessaria per gestirlo a norma."),
    ("Scelta dei partner", "Selezioniamo trasportatori e impianti autorizzati, verificando l’idoneità del trasportatore, dei mezzi e della destinazione."),
    ("Organizzazione del conferimento", "Coordiniamo raccolta, trasporto e avvio a recupero o smaltimento, con un servizio programmato o su richiesta."),
    ("Documenti in ordine", "Seguiamo formulari, registri di carico e scarico e scadenze come il MUD, per una tracciabilità completa."),
]

PRESIDI = [
    ("Modello 231", "scudo", "Sistema di gestione per la prevenzione dei rischi e la garanzia di conformità normativa, supervisionato da un Organismo di Vigilanza indipendente."),
    ("Due diligence sui partner", "lente", "Controllo rigoroso dei partner e delle attività, con verifica delle autorizzazioni di tutti i soggetti coinvolti."),
    ("Antimafia e whistleblowing", "megafono", "Politiche antimafia operative e un canale per segnalare le irregolarità, con piena tutela dei segnalanti."),
    ("Tracciabilità finanziaria", "euro", "Controllo e sicurezza su tutti i flussi finanziari aziendali, per la massima trasparenza in ogni transazione."),
]

VALORI = [  # dal Codice Etico (rev. 00 del 12/10/2024)
    ("Legalità", "Rispetto tassativo di leggi, regolamenti, Modello 231 e Codice Etico in ogni attività."),
    ("Integrità e correttezza", "Rapporti fondati su lealtà, onestà e collaborazione, contro ogni forma di corruzione."),
    ("Imparzialità", "Decisioni prese con criteri oggettivi, evitando qualsiasi conflitto di interessi."),
    ("Trasparenza", "Contabilità chiara e tracciabile, informazioni complete e verificabili."),
    ("Salute e sicurezza", "Tutela delle persone che lavorano con noi e per noi, in ogni fase operativa."),
    ("Tutela ambientale", "Ogni scelta orientata a ridurre l’impatto sull’ambiente e a favorire il recupero."),
]

DOCUMENTI = [
    ("amsic-modello-231-parte-generale.pdf", "Modello 231 – Parte Generale", "Il quadro del D.Lgs. 231/2001, l’organizzazione di AMSIC, l’Organismo di Vigilanza e il sistema di controllo."),
    ("amsic-modello-231-parte-speciale.pdf", "Modello 231 – Parte Speciale", "Le attività sensibili, i reati presupposto e i protocolli di controllo per ciascun processo."),
    ("amsic-codice-etico.pdf", "Codice Etico", "I principi di comportamento: legalità, integrità, trasparenza, tutela della salute, della sicurezza e dell’ambiente."),
    ("amsic-sistema-disciplinare.pdf", "Sistema disciplinare", "Le misure previste per chi viola il Modello, il Codice Etico o le regole sul whistleblowing."),
    ("amsic-whistleblowing.pdf", "Sistema di gestione Whistleblowing", "Come segnalare un illecito, chi gestisce le segnalazioni e come viene tutelato chi segnala."),
    ("amsic-flussi-informativi-odv.pdf", "Segnalazioni e flussi informativi verso l’OdV", "Le informazioni periodiche e immediate che arrivano all’Organismo di Vigilanza."),
    ("amsic-procure-e-deleghe.pdf", "Sistema delle procure e delle deleghe", "Requisiti, validità ed elenco delle procure e delle deleghe aziendali."),
]

# ---------------------------------------------------------------- icone svg (tratto)
_S = 'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"'
ICONE = {
    "tel": f'<svg {_S}><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "mail": f'<svg {_S}><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "pec": f'<svg {_S}><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/><path d="m15.5 17 1.5 1.5 3-3"/></svg>',
    "pin": f'<svg {_S}><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>',
    "freccia": f'<svg {_S}><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "giu": f'<svg {_S}><path d="M12 4v14M6 12l6 6 6-6"/><path d="M5 21h14"/></svg>',
    "check": f'<svg {_S}><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
    "menu": f'<svg {_S}><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "chiudi": f'<svg {_S}><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "scudo": f'<svg {_S}><path d="M12 3 5 6v5c0 4.6 3 8.4 7 10 4-1.6 7-5.4 7-10V6z"/><path d="m9 12 2 2 4-4"/></svg>',
    "lente": f'<svg {_S}><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/><path d="m8.5 11 1.8 1.8 3.4-3.4"/></svg>',
    "megafono": f'<svg {_S}><path d="M4 10v4a1 1 0 0 0 1 1h2l6 4V5L7 9H5a1 1 0 0 0-1 1z"/><path d="M17 9a4 4 0 0 1 0 6"/><path d="M8 15l1 5"/></svg>',
    "euro": f'<svg {_S}><path d="M17.5 6.5A7 7 0 1 0 17.5 17.5"/><path d="M4 10.5h9M4 13.5h9"/></svg>',
    "rete": f'<svg {_S}><circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="6" r="2.2"/><circle cx="19" cy="18" r="2.2"/><path d="M7 11l10-4M7 13l10 4"/></svg>',
    "fusto": f'<svg {_S}><ellipse cx="12" cy="5" rx="6" ry="2"/><path d="M6 5v14c0 1.1 2.7 2 6 2s6-.9 6-2V5"/><path d="M6 10c0 1.1 2.7 2 6 2s6-.9 6-2M6 15c0 1.1 2.7 2 6 2s6-.9 6-2"/></svg>',
    "camion": f'<svg {_S}><path d="M2 6h12v10H2zM14 9h4l3 3.5V16h-7"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>',
    "ciclo": f'<svg {_S}><path d="M20 12a8 8 0 0 1-13.7 5.6M4 12A8 8 0 0 1 17.7 6.4"/><path d="M18 2.5v4h-4M6 21.5v-4h4"/></svg>',
    "foglia": f'<svg {_S}><path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19c3-4 6-6.5 9-8"/></svg>',
    "documento": f'<svg {_S}><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>',
    "pdf": f'<svg {_S}><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M8.5 16.5v-4h1.3a1.2 1.2 0 0 1 0 2.4H8.5M12.5 16.5v-4h1a2 2 0 0 1 0 4zM16.5 12.5h-1.2v4M15.3 14.5h1"/></svg>',
    "wa": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2m.01 1.67c4.55 0 8.24 3.7 8.24 8.24 0 4.55-3.69 8.24-8.24 8.24-1.49 0-2.94-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24M8.53 7.33c-.16 0-.43.06-.66.31-.22.25-.87.86-.87 2.07 0 1.22.89 2.39 1 2.56.14.17 1.76 2.67 4.25 3.73.59.27 1.050.42 1.41.53.59.19 1.13.16 1.56.1.48-.07 1.46-.6 1.67-1.18.21-.58.21-1.070.15-1.18-.07-.1-.23-.16-.48-.27-.25-.14-1.47-.74-1.69-.82-.23-.08-.37-.12-.56.12-.16.25-.64.81-.78.97-.15.17-.29.19-.53.07-.26-.13-1.06-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.12-.24-.01-.39.11-.5.11-.11.27-.29.37-.44.13-.14.17-.25.25-.41.08-.17 0-.31-.05-.43-.06-.12-.56-1.36-.78-1.85-.19-.5-.4-.42-.55-.43-.14 0-.3-.01-.47-.01"/></svg>',
}
MARCHIO_PUNTI = "438.71 285.48 302.45 151.16 157.4 296.08 304.07 443.77 441.47 308.66 583.67 309.8 304.96 591.78 10.35 294.78 304.07 3.5 585.54 285.48"

def ico(n): return ICONE[n]
def e(s): return H.escape(s, quote=True)

def marchio_svg(cls="marchio-sfondo"):
    return f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 595 595.28" aria-hidden="true" focusable="false"><polygon fill="currentColor" points="{MARCHIO_PUNTI}"/></svg>'

# ---------------------------------------------------------------- utilità html
def pulisci_html(html):
    """index.html → ./ ; servizi.html#x → servizi#x (GitHub Pages serve x.html anche senza estensione)."""
    def sostituisci(m):
        attr, pagina, resto = m.group(1), m.group(2), m.group(3)
        return f'{attr}="{"./" if pagina == "index" else pagina}{resto}"'
    return re.sub(r'(href|action)="([a-z0-9-]+)\.html((?:\?[^"#]*)?(?:#[^"]*)?)"', sostituisci, html)

def _larghezze(nome):
    out = []
    for p in glob.glob(os.path.join(ROOT, "assets/img", f"{nome}-*.jpg")):
        m = re.search(rf"{re.escape(nome)}-(\d+)\.jpg$", p)
        if m: out.append(int(m.group(1)))
    return sorted(out)

def _dim(nome, w):
    try:
        from PIL import Image
        with Image.open(os.path.join(ROOT, "assets/img", f"{nome}-{w}.jpg")) as im:
            return im.size
    except Exception:
        return (w, None)

def pic(nome, alt, sizes="100vw", priority=False, cls=""):
    ws = _larghezze(nome)
    assert ws, f"mancano le immagini per {nome}: lanciare prepara_asset.py"
    webp = ", ".join(f"assets/img/{nome}-{w}.webp {w}w" for w in ws)
    jpg = ", ".join(f"assets/img/{nome}-{w}.jpg {w}w" for w in ws)
    big = ws[-1]
    W, Hh = _dim(nome, big)
    dims = f' width="{W}" height="{Hh}"' if Hh else ""
    attrs = ' fetchpriority="high"' if priority else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture{c}><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="assets/img/{nome}-{big}.jpg" srcset="{jpg}" sizes="{sizes}" alt="{e(alt)}"{dims}{attrs} decoding="async"></picture>')

def btn(testo, href, cls="btn-primario", icona=None, extra=""):
    i = f'<span class="btn-ico">{ico(icona)}</span>' if icona else ""
    return f'<a class="btn {cls}" href="{href}"{extra}>{e(testo)}{i}</a>'

def btn_tel(cls="btn-secondario", testo=None):
    t = testo or f'Chiama {AZIENDA["tel"]}'
    return f'<a class="btn {cls}" href="tel:{AZIENDA["tel_link"]}" data-evento="chiamata"><span class="btn-ico">{ico("tel")}</span>{e(t)}</a>'

def btn_wa(cls="btn-wa", testo="Scrivici su WhatsApp", messaggio="Buongiorno, vorrei informazioni sui vostri servizi."):
    if not AZIENDA["whatsapp"]:
        return ""
    from urllib.parse import quote
    return f'<a class="btn {cls}" href="https://wa.me/{AZIENDA["whatsapp"]}?text={quote(messaggio)}" target="_blank" rel="noopener" data-evento="whatsapp"><span class="btn-ico">{ico("wa")}</span>{e(testo)}</a>'

def occhiello(testo, cls=""):
    c = f" {cls}" if cls else ""
    return f'<p class="occhiello{c}">{e(testo)}</p>'

def peso(file):
    b = os.path.getsize(os.path.join(ROOT, "assets/documenti", file))
    return f"{b / 1048576:.1f}".replace(".", ",") + " MB" if b >= 1000 * 1024 else f"{round(b / 1024)} KB"

# ---------------------------------------------------------------- testata e piè di pagina
NAV = [("index.html", "Home"), ("chi-siamo.html", "Chi siamo"), ("servizi.html", "Servizi"),
       ("trasparenza.html", "Trasparenza e 231"), ("contatti.html", "Contatti")]

def testata(pagina):
    corrente = ' aria-current="page"'
    voci = "".join(f'<li><a href="{f}"{corrente if f == pagina else ""}>{e(t)}</a></li>' for f, t in NAV)
    return f'''<a class="salta" href="#contenuto">Vai al contenuto</a>
<header class="testata" data-testata>
  <div class="wrap testata-in">
    <a class="logo" href="index.html" aria-label="AMSIC, torna alla home"><img src="assets/logo/amsic-logo.svg" alt="AMSIC S.r.l. a Socio unico" width="190" height="56"></a>
    <nav class="nav" id="menu" aria-label="Menu principale">
      <ul>{voci}</ul>
      <div class="nav-extra">{btn_tel("btn-secondario btn-piccolo")}</div>
    </nav>
    <a class="btn btn-primario btn-piccolo testata-cta" href="contatti.html#modulo">Richiedi una consulenza</a>
    <button class="menu-btn" type="button" aria-controls="menu" aria-expanded="false" data-menu>
      <span class="menu-apri">{ico("menu")}</span><span class="menu-chiudi">{ico("chiudi")}</span><span class="sr">Menu</span>
    </button>
  </div>
</header>'''

def pie():
    legale = [f'Sede legale: {e(INDIRIZZO_COMPLETO)}', f'P.IVA e C.F. {AZIENDA["piva"]}']
    if AZIENDA["rea"]:
        legale.append(f'REA {e(AZIENDA["rea"])}')
    if AZIENDA["capitale"]:
        legale.append(f'Capitale sociale {e(AZIENDA["capitale"])}')
    legale.append(f'PEC <a href="mailto:{AZIENDA["pec"]}">{AZIENDA["pec"]}</a>')
    legale.append(f'Albo Nazionale Gestori Ambientali n. {AZIENDA["albo_numero"]}, cat. 8 classe D')
    menu = "".join(f'<li><a href="{f}">{e(t)}</a></li>' for f, t in NAV)
    return f'''<footer class="pie">
  {marchio_svg("pie-marchio")}
  <div class="wrap pie-griglia">
    <div class="pie-col pie-marca">
      <img src="assets/logo/amsic-logo-bianco.svg" alt="AMSIC S.r.l. a Socio unico" width="210" height="62" loading="lazy">
      <p>Intermediazione e gestione dei rifiuti speciali, pericolosi e non pericolosi, con un Modello 231 e un Organismo di Vigilanza indipendente.</p>
    </div>
    <div class="pie-col">
      <h2 class="pie-titolo">Pagine</h2>
      <ul class="pie-lista">{menu}</ul>
    </div>
    <div class="pie-col">
      <h2 class="pie-titolo">Contatti</h2>
      <ul class="pie-lista pie-contatti">
        <li><a href="tel:{AZIENDA["tel_link"]}">{ico("tel")}{AZIENDA["tel"]}</a></li>
        <li><a href="mailto:{AZIENDA["email"]}">{ico("mail")}{AZIENDA["email"]}</a></li>
        <li><a href="{MAPPA_LINK}" target="_blank" rel="noopener">{ico("pin")}{e(INDIRIZZO_COMPLETO)}</a></li>
      </ul>
    </div>
    <div class="pie-col">
      <h2 class="pie-titolo">Trasparenza</h2>
      <ul class="pie-lista">
        <li><a href="trasparenza.html#documenti">Documenti del Modello 231</a></li>
        <li><a href="trasparenza.html#segnalazioni">Segnalazioni all’OdV</a></li>
        <li><a href="trasparenza.html#autorizzazioni">Iscrizione all’Albo</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap pie-legale">
    <p>{" · ".join(legale)}</p>
    <p class="pie-fondo"><span>© {ANNO} {e(AZIENDA["ragione_sociale"])}</span><a href="privacy.html">Privacy</a><a href="cookie.html">Cookie</a><span class="pie-firma">Sito di Freeze Studio</span></p>
  </div>
</footer>'''

def barra_mobile(pagina):
    href = "#modulo" if pagina == "contatti.html" else "contatti.html#modulo"
    wa = btn_wa("btn-wa", "WhatsApp")
    return f'''<div class="barra-mobile" data-barra aria-hidden="true">
  <a class="btn btn-secondario" href="tel:{AZIENDA["tel_link"]}" tabindex="-1" data-evento="chiamata"><span class="btn-ico">{ico("tel")}</span>Chiama</a>
  {wa.replace('class="btn', 'tabindex="-1" class="btn') if wa else ""}
  <a class="btn btn-primario" href="{href}" tabindex="-1">Scrivici</a>
</div>'''

JSONLD_AZIENDA = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": BASE + "/#azienda",
    "name": AZIENDA["ragione_sociale"],
    "alternateName": "AMSIC",
    "description": "Intermediazione e gestione di rifiuti speciali, pericolosi e non pericolosi: raccolta, trasporto, smaltimento e recupero tramite partner autorizzati, consulenza ambientale e gestione documentale.",
    "url": BASE + "/",
    "logo": BASE + "/assets/logo/icon-512.png",
    "image": BASE + "/assets/img/condivisione.jpg",
    "telephone": AZIENDA["tel_link"],
    "email": AZIENDA["email"],
    "vatID": "IT" + AZIENDA["piva"],
    "taxID": AZIENDA["piva"],
    "address": {"@type": "PostalAddress", "streetAddress": AZIENDA["indirizzo"], "postalCode": AZIENDA["cap"],
                "addressLocality": AZIENDA["citta"], "addressRegion": AZIENDA["provincia"], "addressCountry": "IT"},
}

def documento(pagina, titolo, descrizione, corpo, jsonld=None, noindex=False, tipo="website"):
    url = BASE + "/" + ("" if pagina == "index.html" else pagina[:-5])
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    canon = "" if noindex else f'<link rel="canonical" href="{url}">'
    ld = ""
    for blocco in (jsonld or []):
        ld += f'<script type="application/ld+json">{json.dumps(blocco, ensure_ascii=False)}</script>'
    html = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titolo)}</title>
<meta name="description" content="{e(descrizione)}">
{robots}{canon}
<meta name="theme-color" content="#1F4D9B">
<meta property="og:type" content="{tipo}">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="AMSIC">
<meta property="og:title" content="{e(titolo)}">
<meta property="og:description" content="{e(descrizione)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/condivisione.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/logo/amsic-marchio.svg" type="image/svg+xml">
<link rel="icon" href="assets/logo/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/logo/apple-touch-icon.png">
<link rel="preload" href="assets/font/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/font/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/stile.css?v={VERSIONE}">
{ld}
</head>
<body>
{testata(pagina)}
<main id="contenuto">
{corpo}
</main>
{pie()}
{barra_mobile(pagina)}
<script src="assets/js/sito.js?v={VERSIONE}" defer></script>
</body>
</html>
'''
    return pulisci_html(html)

# ---------------------------------------------------------------- blocchi riutilizzabili
def banda_cta(titolo="Contattaci per una consulenza personalizzata.", testo="Raccontaci che rifiuto devi gestire, in che quantità e dove: ti indichiamo la soluzione più adatta e conforme alle normative."):
    return f'''<section class="banda-cta">
  <div class="wrap banda-cta-in rivela">
    {marchio_svg("banda-marchio")}
    <div>
      <h2>{e(titolo)}</h2>
      <p>{e(testo)}</p>
    </div>
    <div class="azioni">{btn("Richiedi una consulenza", "contatti.html#modulo", "btn-bianco", "freccia")}{btn_tel("btn-contorno-bianco")}</div>
  </div>
</section>'''

def scheda_servizio(s, livello="h3"):
    return f'''<article class="scheda-servizio rivela">
  <a class="scheda-link" href="servizi.html#{s["id"]}">
    <div class="scheda-foto">{pic(s["foto"], s["alt"], "(min-width: 1100px) 360px, (min-width: 700px) 45vw, 92vw")}</div>
    <div class="scheda-testo">
      <span class="icona-rombo">{ico(s["icona"])}</span>
      <{livello}>{e(s["nome"])}</{livello}>
      <p>{e(s["breve"])}</p>
      <span class="scheda-piu">Scopri il servizio {ico("freccia")}</span>
    </div>
  </a>
</article>'''

def griglia_presidi(scuro=False):
    voci = "".join(f'''<li class="presidio rivela"><span class="icona-rombo{" chiara" if scuro else ""}">{ico(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>''' for t, i, d in PRESIDI)
    return f'<ul class="presidi">{voci}</ul>'

# ---------------------------------------------------------------- pagine
def pagina_home():
    servizi = "".join(scheda_servizio(s) for s in SERVIZI)
    passi = "".join(f'''<li class="passo rivela"><span class="passo-num" aria-hidden="true"><span>{i}</span></span><h3>{e(t)}</h3><p>{e(d)}</p></li>''' for i, (t, d) in enumerate(PASSI, 1))
    corpo = f'''
<section class="eroe">
  <div class="wrap eroe-in">
    <div class="eroe-testo">
      {occhiello("Intermediazione rifiuti speciali · Catania")}
      <h1>Gestione sicura, <span class="a-capo">ambiente protetto.</span></h1>
      <p class="lead">Organizziamo per la tua azienda raccolta, trasporto e avvio a recupero o smaltimento dei rifiuti speciali, pericolosi e non pericolosi, con trasportatori e impianti autorizzati. Un solo interlocutore, ogni passaggio tracciato.</p>
      <div class="azioni" data-sentinella>{btn("Richiedi una consulenza", "contatti.html#modulo", "btn-primario", "freccia")}{btn_tel()}</div>
      <ul class="garanzie">
        <li>{ico("check")}Albo Gestori Ambientali n. {AZIENDA["albo_numero"]}</li>
        <li>{ico("check")}Modello 231 e Organismo di Vigilanza</li>
      </ul>
    </div>
    <div class="eroe-visual" aria-hidden="true">
      <div class="rombo-grande">{pic("rombo-recupero", "", "(min-width: 1000px) 520px, 80vw", priority=True)}</div>
      <span class="rombo-pieno"></span>
      <span class="rombo-vuoto"></span>
      <div class="filiera">
        <span>Raccolta</span><i></i><span>Trasporto</span><i></i><span>Recupero</span>
      </div>
    </div>
  </div>
</section>

<section class="fatti" aria-label="AMSIC in breve">
  <div class="wrap fatti-griglia">
    <div class="fatto rivela"><strong>20+</strong><span>anni di esperienza del team nella gestione dei rifiuti speciali</span></div>
    <div class="fatto rivela"><strong>Cat. 8</strong><span>Albo Nazionale Gestori Ambientali, classe D: da 6.000 a 15.000 t/anno</span></div>
    <div class="fatto rivela"><strong>P · NP</strong><span>rifiuti speciali pericolosi e non pericolosi</span></div>
    <div class="fatto rivela"><strong>231</strong><span>Modello organizzativo vigilato da un Organismo indipendente</span></div>
  </div>
</section>

<section class="sezione">
  <div class="wrap">
    <div class="intestazione rivela">
      {occhiello("Cosa facciamo")}
      <h2>Un solo interlocutore per tutta la filiera del rifiuto.</h2>
      <p>Come intermediari iscritti all’Albo, ci interponiamo tra chi produce o detiene i rifiuti e le imprese che li trasportano, li recuperano o li smaltiscono: cerchiamo le migliori condizioni tecnico-economiche e verifichiamo che ogni soggetto coinvolto sia autorizzato.</p>
    </div>
    <div class="griglia-servizi">{servizi}</div>
  </div>
</section>

<section class="sezione sezione-chiara">
  <div class="wrap">
    <div class="intestazione rivela">
      {occhiello("Come lavoriamo")}
      <h2>Quattro passaggi, nessuna sorpresa.</h2>
    </div>
    <ol class="passi">{passi}</ol>
  </div>
</section>

<section class="sezione sezione-scura">
  {marchio_svg("scura-marchio")}
  <div class="wrap scura-in">
    <div class="scura-testo rivela">
      {occhiello("Trasparenza e Modello 231", "chiaro")}
      <h2>La legalità è il nostro metodo di lavoro.</h2>
      <p>AMSIC ha adottato un Modello di organizzazione, gestione e controllo ai sensi del D.Lgs. 231/2001, con un Codice Etico e procedure di controllo interne che regolano il comportamento di tutte le persone coinvolte. Il rispetto del Modello è affidato a un Organismo di Vigilanza indipendente, presieduto dal {e(AZIENDA["odv_presidente"])}.</p>
      <div class="azioni">{btn("Scopri il Modello 231", "trasparenza.html", "btn-bianco", "freccia")}{btn("Scarica i documenti", "trasparenza.html#documenti", "btn-contorno-bianco", "giu")}</div>
    </div>
    {griglia_presidi(scuro=True)}
  </div>
</section>

<section class="sezione">
  <div class="wrap duo">
    <div class="duo-foto rivela">{pic("tablet", "Due professionisti consultano un tablet con il logo AMSIC", "(min-width: 1000px) 540px, 92vw")}</div>
    <div class="duo-testo rivela">
      {occhiello("Chi siamo")}
      <h2>Vent’anni di esperienza, un’organizzazione nuova.</h2>
      <p>AMSIC nasce da un team di professionisti con oltre vent’anni di esperienza nella gestione dei rifiuti speciali, pericolosi e non. La nostra missione è garantire un servizio sicuro, trasparente e conforme alle normative, con soluzioni su misura per imprese pubbliche e private.</p>
      {btn("Conosci AMSIC", "chi-siamo.html", "btn-secondario", "freccia")}
    </div>
  </div>
</section>

{banda_cta()}
'''
    return documento("index.html",
                     "AMSIC | Intermediazione e gestione rifiuti speciali a Catania",
                     "Raccolta, trasporto, smaltimento e recupero di rifiuti speciali pericolosi e non pericolosi tramite partner autorizzati. Iscritti all’Albo Gestori Ambientali (cat. 8), Modello 231. Catania.",
                     corpo, jsonld=[JSONLD_AZIENDA])

def pagina_chi_siamo():
    valori = "".join(f'<li class="valore rivela"><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in VALORI)
    corpo = f'''
<section class="testa-pagina">
  <div class="wrap testa-duo">
    <div class="rivela">
      {occhiello("Chi siamo")}
      <h1>Vent’anni di esperienza, un’organizzazione nuova.</h1>
      <p class="lead">AMSIC S.r.l. nasce da un team di professionisti con oltre vent’anni di esperienza nella gestione dei rifiuti speciali, pericolosi e non.</p>
    </div>
    <div class="testa-foto rivela">{pic("biglietto", "Biglietto da visita AMSIC tenuto in mano da un professionista", "(min-width: 1000px) 520px, 92vw", priority=True)}</div>
  </div>
</section>

<section class="sezione">
  <div class="wrap colonne-testo">
    <div class="rivela">
      <h2>La nostra storia</h2>
      <p>Sebbene l’azienda sia di recente costituzione, il know-how accumulato in anni di attività sul campo ci consente di affrontare ogni sfida con competenza, tempestività e attenzione alle normative.</p>
      <p>In seguito a una profonda riorganizzazione interna, AMSIC ha adottato un Modello Organizzativo 231 tra i più avanzati del settore, istituendo un Organismo di Vigilanza indipendente che supervisiona costantemente tutte le attività aziendali.</p>
    </div>
    <div class="rivela">
      <h2>La nostra missione</h2>
      <p>Garantire un servizio sicuro, trasparente e conforme alle normative, offrendo ai nostri clienti soluzioni su misura per la raccolta, il trasporto, lo smaltimento e l’intermediazione dei rifiuti.</p>
      <p>Ogni intervento è pensato per unire sicurezza operativa, rispetto dell’ambiente e piena conformità legislativa, per imprese pubbliche e private.</p>
    </div>
  </div>
</section>

<section class="sezione sezione-chiara">
  <div class="wrap">
    <div class="intestazione rivela">
      {occhiello("I nostri valori")}
      <h2>I principi del nostro Codice Etico.</h2>
      <p>Valgono per chi lavora in AMSIC e per chiunque lavori con noi: clienti, fornitori, trasportatori e impianti partner.</p>
    </div>
    <ul class="valori">{valori}</ul>
  </div>
</section>

<section class="sezione">
  <div class="wrap duo">
    <div class="duo-testo rivela">
      {occhiello("Come siamo organizzati")}
      <h2>Una struttura snella, responsabilità chiare.</h2>
      <ul class="organi">
        <li><h3>Amministratore Unico</h3><p>Guida l’azienda e ha la responsabilità delle decisioni su tutte le operazioni.</p></li>
        <li><h3>Area Amministrativa e contabile</h3><p>Gestisce dati dei clienti, intermediazioni concluse, ordini, fatturazione, archivio documentale e scadenze.</p></li>
        <li><h3>Area Commerciale</h3><p>Cura i rapporti con produttori e detentori dei rifiuti, impianti di trattamento e trasportatori, per proporre le migliori soluzioni di recupero o smaltimento.</p></li>
      </ul>
    </div>
    <div class="duo-foto rivela">{pic("tablet", "Due professionisti consultano un tablet con il logo AMSIC", "(min-width: 1000px) 540px, 92vw")}</div>
  </div>
</section>

{banda_cta()}
'''
    return documento("chi-siamo.html", "Chi siamo | AMSIC – rifiuti speciali, Catania",
                     "AMSIC S.r.l. nasce da un team con oltre vent’anni di esperienza nella gestione dei rifiuti speciali. Modello 231, Organismo di Vigilanza indipendente e un Codice Etico condiviso.",
                     corpo, jsonld=[JSONLD_AZIENDA])

def pagina_servizi():
    salti = "".join(f'<a href="#{s["id"]}">{e(s["nome"])}</a>' for s in SERVIZI)
    blocchi = ""
    for i, s in enumerate(SERVIZI):
        punti = "".join(f"<li>{ico('check')}{e(p)}</li>" for p in s["punti"])
        blocchi += f'''<article class="servizio{" inverso" if i % 2 else ""}" id="{s["id"]}">
  <div class="servizio-foto rivela">{pic(s["foto"], s["alt"], "(min-width: 1000px) 540px, 92vw")}</div>
  <div class="servizio-testo rivela">
    <span class="icona-rombo">{ico(s["icona"])}</span>
    <h2>{e(s["nome"])}</h2>
    <p>{e(s["testo"])}</p>
    <ul class="spunte">{punti}</ul>
    {btn("Chiedi informazioni", f"contatti.html?servizio={s['id']}#modulo", "btn-secondario", "freccia")}
  </div>
</article>'''
    corpo = f'''
<section class="testa-pagina testa-centrata">
  <div class="wrap rivela">
    {occhiello("Servizi")}
    <h1>Servizi per la gestione dei rifiuti speciali.</h1>
    <p class="lead">Dall’analisi della richiesta alla documentazione finale, organizziamo l’intera gestione dei rifiuti speciali, pericolosi e non pericolosi, per aziende, enti pubblici e privati.</p>
    <nav class="salti" aria-label="Vai al servizio">{salti}</nav>
  </div>
</section>

<section class="sezione sezione-servizi">
  <div class="wrap">{blocchi}</div>
</section>

<section class="sezione sezione-chiara">
  <div class="wrap riquadro-spiega rivela">
    <div>
      {occhiello("In parole semplici")}
      <h2>Cosa fa un intermediario di rifiuti senza detenzione?</h2>
    </div>
    <div>
      <p>L’intermediario organizza per conto di terzi il conferimento dei rifiuti destinati a recupero o smaltimento. Non li trasporta e non li tratta direttamente: si interpone tra chi produce o detiene i rifiuti e le imprese autorizzate a trasportarli, recuperarli o smaltirli, e ne verifica l’idoneità.</p>
      <p>Per svolgere questa attività serve l’iscrizione alla categoria 8 dell’Albo Nazionale Gestori Ambientali (art. 212 del D.Lgs. 152/2006). AMSIC è iscritta con il numero {AZIENDA["albo_numero"]}, classe D.</p>
      {btn("Vedi le autorizzazioni", "trasparenza.html#autorizzazioni", "btn-testo", "freccia")}
    </div>
  </div>
</section>

<section class="sezione">
  <div class="wrap compliance rivela">
    <span class="icona-rombo grande">{ico("scudo")}</span>
    <div>
      <h2>Compliance e trasparenza</h2>
      <p>Lavorare con AMSIC significa affidarsi a un’azienda con un Modello 231, un Organismo di Vigilanza indipendente, due diligence sui partner e tracciabilità dei flussi finanziari.</p>
    </div>
    {btn("Trasparenza e Modello 231", "trasparenza.html", "btn-primario", "freccia")}
  </div>
</section>

{banda_cta()}
'''
    jsonld_servizi = {
        "@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [{"@type": "ListItem", "position": i, "item": {"@type": "Service", "name": s["nome"], "description": s["breve"],
                             "url": f'{BASE}/servizi#{s["id"]}', "provider": {"@id": BASE + "/#azienda"}}} for i, s in enumerate(SERVIZI, 1)],
    }
    return documento("servizi.html", "Servizi | Intermediazione, raccolta, trasporto e smaltimento rifiuti – AMSIC",
                     "Intermediazione rifiuti, raccolta, trasporto, smaltimento e recupero, consulenza ambientale e gestione documentale (formulari, registri, MUD) per aziende ed enti. Catania.",
                     corpo, jsonld=[JSONLD_AZIENDA, jsonld_servizi])

def pagina_trasparenza():
    docs = "".join(f'''<li class="doc rivela">
  <span class="doc-ico">{ico("pdf")}</span>
  <div class="doc-testo"><h3>{e(t)}</h3><p>{e(d)}</p><span class="doc-meta">PDF · {peso(f)}</span></div>
  <a class="btn btn-secondario btn-piccolo" href="assets/documenti/{f}" target="_blank" rel="noopener" aria-label="Scarica: {e(t)} (PDF, {peso(f)})">Scarica {ico("giu")}</a>
</li>''' for f, t, d in DOCUMENTI)
    corpo = f'''
<section class="testa-pagina testa-centrata">
  <div class="wrap rivela">
    {occhiello("Trasparenza e Modello 231")}
    <h1>Trasparenza, controllo e responsabilità.</h1>
    <p class="lead">Per garantire l’integrità aziendale e prevenire i rischi operativi, AMSIC ha adottato un Modello Organizzativo ai sensi del D.Lgs. 231/2001: procedure di controllo interne e un Codice Etico che regolano il comportamento di tutte le persone coinvolte.</p>
    <nav class="salti" aria-label="In questa pagina"><a href="#autorizzazioni">Autorizzazioni</a><a href="#modello-231">Modello 231 e OdV</a><a href="#presidi">Presidi</a><a href="#segnalazioni">Segnalazioni</a><a href="#documenti">Documenti</a></nav>
  </div>
</section>

<section class="sezione" id="autorizzazioni">
  <div class="wrap duo duo-alto">
    <div class="rivela">
      {occhiello("Autorizzazioni")}
      <h2>Iscrizione all’Albo Nazionale Gestori Ambientali.</h2>
      <p>L’intermediazione di rifiuti senza detenzione richiede l’iscrizione alla categoria 8 dell’Albo, da rinnovare ogni cinque anni (art. 212 del D.Lgs. 152/2006).</p>
    </div>
    <dl class="scheda-albo rivela">
      <div><dt>Numero di iscrizione</dt><dd>{AZIENDA["albo_numero"]}</dd></div>
      <div><dt>Sezione</dt><dd>{e(AZIENDA["albo_sezione"])}</dd></div>
      <div><dt>Categoria</dt><dd>{e(AZIENDA["albo_categoria"])}</dd></div>
      <div><dt>Classe</dt><dd>{e(AZIENDA["albo_classe"])}</dd></div>
      <div><dt>Rifiuti gestiti</dt><dd>Pericolosi e non pericolosi</dd></div>
    </dl>
  </div>
</section>

<section class="sezione sezione-chiara" id="modello-231">
  <div class="wrap colonne-testo">
    <div class="rivela">
      {occhiello("Modello 231 e Organismo di Vigilanza")}
      <h2>Un modello organizzativo tra i più avanzati del settore.</h2>
    </div>
    <div class="rivela">
      <p>Il Modello prevede procedure di controllo interne e un Codice Etico che regolano il comportamento di tutte le risorse coinvolte. Il suo rispetto è supervisionato da un Organismo di Vigilanza indipendente, attualmente presieduto dal {e(AZIENDA["odv_presidente"])}, che vigila costantemente sull’effettiva applicazione delle misure di prevenzione.</p>
      <p>Il Modello 231 è per noi uno strumento concreto per promuovere etica, legalità e trasparenza in ogni ambito operativo. Revisione in vigore: {e(AZIENDA["revisione_231"])}.</p>
    </div>
  </div>
</section>

<section class="sezione" id="presidi">
  <div class="wrap">
    <div class="intestazione rivela">
      {occhiello("I presidi")}
      <h2>Come preveniamo i rischi, ogni giorno.</h2>
    </div>
    {griglia_presidi()}
  </div>
</section>

<section class="sezione sezione-scura" id="segnalazioni">
  {marchio_svg("scura-marchio")}
  <div class="wrap scura-in">
    <div class="scura-testo rivela">
      {occhiello("Whistleblowing", "chiaro")}
      <h2>Come segnalare un illecito.</h2>
      <p>Chi viene a conoscenza di una violazione del Modello 231 o di un illecito può segnalarlo all’Organismo di Vigilanza, a cui AMSIC ha affidato la gestione del canale interno di segnalazione previsto dal D.Lgs. 24/2023. La riservatezza di chi segnala è sempre tutelata.</p>
      {btn("Leggi la procedura completa", "assets/documenti/amsic-whistleblowing.pdf", "btn-contorno-bianco", "giu", ' target="_blank" rel="noopener"')}
    </div>
    <ul class="canali rivela">
      <li><span class="icona-rombo chiara">{ico("mail")}</span><div><h3>Per email</h3><p><a href="mailto:{AZIENDA["email_odv"]}">{AZIENDA["email_odv"]}</a></p></div></li>
      <li><span class="icona-rombo chiara">{ico("documento")}</span><div><h3>Per posta</h3><p>Organismo di Vigilanza 231 di AMSIC, presso la sede legale: {e(INDIRIZZO_COMPLETO)}</p></div></li>
      <li><span class="icona-rombo chiara">{ico("megafono")}</span><div><h3>Di persona</h3><p>Con un incontro diretto con il Responsabile della gestione delle segnalazioni.</p></div></li>
    </ul>
  </div>
</section>

<section class="sezione" id="documenti">
  <div class="wrap">
    <div class="intestazione rivela">
      {occhiello("Documenti")}
      <h2>Scarica il Modello 231 e i documenti collegati.</h2>
      <p>Tutti i documenti sono in vigore nella {e(AZIENDA["revisione_231"])}.</p>
    </div>
    <ul class="documenti">{docs}</ul>
  </div>
</section>

{banda_cta()}
'''
    return documento("trasparenza.html", "Trasparenza e Modello 231 | AMSIC",
                     "Iscrizione all’Albo Gestori Ambientali n. PA/015069 (cat. 8, classe D), Modello 231 con Organismo di Vigilanza indipendente, canali di segnalazione e documenti da scaricare.",
                     corpo, jsonld=[JSONLD_AZIENDA])

def opzioni_servizi():
    voci = "".join(f'<option value="{e(s["nome"])}" data-id="{s["id"]}">{e(s["nome"])}</option>' for s in SERVIZI)
    return f'<option value="">Seleziona…</option>{voci}<option value="Altro">Altro</option>'

def modulo():
    return f'''<form class="modulo" id="modulo" action="{ACTION_MODULO}" method="post" data-modulo data-endpoint="{ENDPOINT_MODULO}" data-email="{AZIENDA['email']}" data-tel="{AZIENDA['tel']}" novalidate>
  <input type="hidden" name="_subject" value="Richiesta dal sito AMSIC">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_next" value="{BASE}/grazie">
  <p class="campo-esca" aria-hidden="true"><label>Lascia vuoto <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></p>
  <div class="campi">
    <p class="campo"><label for="m-nome">Nome e cognome <span aria-hidden="true">*</span></label><input id="m-nome" name="Nome" type="text" autocomplete="name" required></p>
    <p class="campo"><label for="m-azienda">Azienda o ente</label><input id="m-azienda" name="Azienda" type="text" autocomplete="organization"></p>
    <p class="campo"><label for="m-email">Email <span aria-hidden="true">*</span></label><input id="m-email" name="email" type="email" autocomplete="email" required></p>
    <p class="campo"><label for="m-tel">Telefono</label><input id="m-tel" name="Telefono" type="tel" autocomplete="tel" inputmode="tel"></p>
    <p class="campo largo"><label for="m-servizio">Servizio di interesse</label><select id="m-servizio" name="Servizio">{opzioni_servizi()}</select></p>
    <p class="campo largo"><label for="m-msg">Di cosa hai bisogno? <span aria-hidden="true">*</span></label><textarea id="m-msg" name="Messaggio" rows="5" required placeholder="Tipo di rifiuto, quantità indicativa, luogo e frequenza del ritiro…"></textarea></p>
  </div>
  <p class="consenso"><input id="m-privacy" type="checkbox" name="Privacy" value="Accettata" required><label for="m-privacy">Ho letto l’<a href="privacy.html" target="_blank">informativa sulla privacy</a> e acconsento al trattamento dei dati per ricevere una risposta. <span aria-hidden="true">*</span></label></p>
  <div class="modulo-fondo">
    <button class="btn btn-primario" type="submit"><span data-etichetta>Invia la richiesta</span><span class="btn-ico">{ico("freccia")}</span></button>
    <p class="nota">I campi con * sono obbligatori.</p>
  </div>
  <div class="esito" role="status" aria-live="polite" data-esito hidden></div>
</form>'''

def pagina_contatti():
    corpo = f'''
<section class="testa-pagina">
  <div class="wrap rivela">
    {occhiello("Contatti")}
    <h1>Richiedi una consulenza.</h1>
    <p class="lead">Scrivici che tipo di rifiuto devi gestire, in che quantità e dove: ti ricontattiamo per proporti la soluzione più adatta e conforme.</p>
  </div>
</section>

<section class="sezione sezione-contatti">
  <div class="wrap contatti-griglia">
    <div class="contatti-modulo rivela">{modulo()}</div>
    <aside class="contatti-info rivela" aria-label="Recapiti">
      <ul class="recapiti">
        <li><span class="icona-rombo">{ico("tel")}</span><div><h2>Telefono</h2><p><a href="tel:{AZIENDA["tel_link"]}" data-evento="chiamata">{AZIENDA["tel"]}</a></p></div></li>
        <li><span class="icona-rombo">{ico("mail")}</span><div><h2>Email</h2><p><a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a></p></div></li>
        <li><span class="icona-rombo">{ico("pec")}</span><div><h2>PEC</h2><p><a href="mailto:{AZIENDA["pec"]}">{AZIENDA["pec"]}</a></p></div></li>
        <li><span class="icona-rombo">{ico("pin")}</span><div><h2>Sede legale</h2><p>{e(INDIRIZZO_COMPLETO)}<br><a href="{MAPPA_LINK}" target="_blank" rel="noopener">Apri in Google Maps</a></p></div></li>
      </ul>
      {btn_wa("btn-wa")}
      <div class="mappa" data-mappa="{MAPPA_EMBED}">
        <button class="mappa-btn" type="button" data-mappa-btn>{ico("pin")}<span>Mostra la mappa</span></button>
        <p class="mappa-nota">La mappa viene caricata da Google solo se la apri.</p>
      </div>
      <p class="nota-odv">Devi fare una segnalazione all’Organismo di Vigilanza? Usa i <a href="trasparenza.html#segnalazioni">canali dedicati</a>.</p>
    </aside>
  </div>
</section>
'''
    return documento("contatti.html", "Contatti | AMSIC – richiedi una consulenza",
                     f"Contatta AMSIC per la gestione dei tuoi rifiuti speciali: telefono {AZIENDA['tel']}, email {AZIENDA['email']}, sede a Catania. Rispondiamo con una proposta su misura.",
                     corpo, jsonld=[JSONLD_AZIENDA])

def pagina_testo(file, titolo, descrizione, h1, contenuto, noindex=False):
    corpo = f'''
<section class="testa-pagina">
  <div class="wrap">{occhiello("Informazioni legali")}<h1>{e(h1)}</h1></div>
</section>
<section class="sezione testo-legale">
  <div class="wrap stretto">{contenuto}</div>
</section>'''
    return documento(file, titolo, descrizione, corpo, noindex=noindex)

PRIVACY = f'''
<p class="aggiornato">Ultimo aggiornamento: {AGGIORNAMENTO_PRIVACY}</p>
<p>Questa informativa è resa ai sensi dell’art. 13 del Regolamento (UE) 2016/679 (“GDPR”) e descrive come {AZIENDA["ragione_sociale"]} tratta i dati personali di chi visita questo sito o ci contatta.</p>
<h2>1. Titolare del trattamento</h2>
<p>{AZIENDA["ragione_sociale"]}<br>Sede legale: {INDIRIZZO_COMPLETO}<br>P.IVA e C.F. {AZIENDA["piva"]}<br>Email: <a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a><br>PEC: <a href="mailto:{AZIENDA["pec"]}">{AZIENDA["pec"]}</a></p>
<h2>2. Quali dati trattiamo</h2>
<ul>
<li><strong>Dati di navigazione.</strong> Il servizio che ospita il sito registra, per motivi tecnici e di sicurezza, dati come l’indirizzo IP, il tipo di browser e l’orario della richiesta. Non usiamo strumenti di statistica né di profilazione.</li>
<li><strong>Dati che ci invii.</strong> Quando compili il modulo contatti, ci scrivi o ci telefoni trattiamo i dati che ci fornisci: nome e cognome, azienda o ente, email, telefono e il contenuto del messaggio.</li>
<li><strong>Segnalazioni all’Organismo di Vigilanza.</strong> Le segnalazioni inviate tramite i canali whistleblowing sono gestite secondo il <a href="assets/documenti/amsic-whistleblowing.pdf">Sistema di gestione Whistleblowing</a>, che descrive anche le relative tutele.</li>
</ul>
<h2>3. Perché li trattiamo e su quale base</h2>
<ul>
<li>Rispondere alle tue richieste e inviarti informazioni o preventivi: misure precontrattuali richieste dall’interessato (art. 6.1.b GDPR).</li>
<li>Gestire l’eventuale rapporto contrattuale e adempiere agli obblighi di legge, fiscali e ambientali: art. 6.1.b e 6.1.c GDPR.</li>
<li>Garantire la sicurezza e il funzionamento del sito: legittimo interesse del titolare (art. 6.1.f GDPR).</li>
</ul>
<h2>4. Per quanto tempo</h2>
<p>Conserviamo i dati delle richieste per il tempo necessario a gestirle. Se nasce un rapporto contrattuale, i dati sono conservati per la durata prevista dagli obblighi di legge (per esempio dieci anni per i documenti contabili e fiscali).</p>
<h2>5. Chi può riceverli</h2>
<p>I dati sono trattati dal personale autorizzato di AMSIC e possono essere comunicati a fornitori che operano per nostro conto come responsabili del trattamento, tra cui:</p>
<ul>
<li>GitHub, Inc. (ospitalità del sito);</li>
<li>FormSubmit (formsubmit.co), il servizio che inoltra alla nostra casella email i messaggi inviati con il modulo;</li>
<li>Google (servizio di posta elettronica e, solo se la apri, mappa di Google Maps).</li>
</ul>
<p>Alcuni di questi fornitori hanno sede negli Stati Uniti: il trasferimento avviene sulla base della decisione di adeguatezza della Commissione europea (EU-U.S. Data Privacy Framework) o delle clausole contrattuali standard. I dati non sono diffusi né usati per finalità di marketing.</p>
<h2>6. I tuoi diritti</h2>
<p>Puoi chiedere in qualsiasi momento l’accesso ai tuoi dati, la rettifica, la cancellazione, la limitazione del trattamento, la portabilità e opporti al trattamento (artt. 15–22 GDPR), scrivendo a <a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a> o alla PEC <a href="mailto:{AZIENDA["pec"]}">{AZIENDA["pec"]}</a>. Hai anche il diritto di proporre reclamo al Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it" target="_blank" rel="noopener">www.garanteprivacy.it</a>).</p>
<h2>7. Conferimento dei dati</h2>
<p>Il conferimento dei dati nel modulo è facoltativo, ma senza i dati contrassegnati come obbligatori non possiamo rispondere alla tua richiesta.</p>
<h2>8. Cookie</h2>
<p>Per l’uso dei cookie consulta l’<a href="cookie.html">informativa sui cookie</a>.</p>
'''

COOKIE = f'''
<p class="aggiornato">Ultimo aggiornamento: {AGGIORNAMENTO_PRIVACY}</p>
<h2>Cosa sono i cookie</h2>
<p>I cookie sono piccoli file di testo che i siti salvano sul dispositivo di chi li visita, per farli funzionare o per raccogliere informazioni sulla navigazione.</p>
<h2>Cookie usati da questo sito</h2>
<p>Questo sito <strong>non usa cookie di profilazione né cookie di statistica</strong> e non installa strumenti di tracciamento di terze parti. I caratteri tipografici sono ospitati sul sito stesso, senza collegamenti a servizi esterni. Per questo non è necessario un banner per il consenso.</p>
<h2>Mappa di Google Maps</h2>
<p>Nella pagina Contatti la mappa non viene caricata automaticamente: compare solo se premi “Mostra la mappa”. In quel momento Google può installare i propri cookie, secondo la sua <a href="https://policies.google.com/technologies/cookies?hl=it" target="_blank" rel="noopener">informativa sui cookie</a>. Se non apri la mappa, nessun dato viene inviato a Google.</p>
<h2>Come gestire i cookie</h2>
<p>Puoi cancellare o bloccare i cookie dalle impostazioni del tuo browser. Per qualsiasi domanda scrivi a <a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a>.</p>
'''

def pagina_grazie():
    corpo = f'''
<section class="testa-pagina testa-centrata pagina-breve">
  <div class="wrap">
    {occhiello("Richiesta inviata")}
    <h1>Grazie, abbiamo ricevuto la tua richiesta.</h1>
    <p class="lead">Ti ricontatteremo al più presto. Se è urgente puoi chiamarci al {AZIENDA["tel"]}.</p>
    <div class="azioni centrate">{btn("Torna alla home", "index.html", "btn-primario", "freccia")}{btn_tel()}</div>
  </div>
</section>'''
    return documento("grazie.html", "Richiesta inviata | AMSIC", "Grazie per averci contattato.", corpo, noindex=True)

def pagina_404():
    corpo = f'''
<section class="testa-pagina testa-centrata pagina-breve">
  <div class="wrap">
    {occhiello("Errore 404")}
    <h1>Questa pagina non esiste.</h1>
    <p class="lead">Forse l’indirizzo è cambiato. Puoi ripartire dalla home o scriverci.</p>
    <div class="azioni centrate">{btn("Vai alla home", "index.html", "btn-primario", "freccia")}{btn("Contatti", "contatti.html", "btn-secondario")}</div>
  </div>
</section>'''
    html = documento("404.html", "Pagina non trovata | AMSIC", "La pagina cercata non esiste.", corpo, noindex=True)
    # la 404 può essere servita a qualsiasi profondità: percorsi assoluti dalla radice del sito
    # con il dominio collegato (file CNAME) il sito sta nella radice; su github.io sta in /amsic/
    radice = "/" if os.path.exists(os.path.join(ROOT, "CNAME")) else "/amsic/"
    html = html.replace('href="assets/', f'href="{radice}assets/').replace('src="assets/', f'src="{radice}assets/')
    html = re.sub(r'href="(\./|[a-z0-9-]+(?:#[^"]*)?)"', lambda m: f'href="{radice}{"" if m.group(1) == "./" else m.group(1)}"', html)
    return html

PAGINE = {
    "index.html": pagina_home,
    "chi-siamo.html": pagina_chi_siamo,
    "servizi.html": pagina_servizi,
    "trasparenza.html": pagina_trasparenza,
    "contatti.html": pagina_contatti,
    "privacy.html": lambda: pagina_testo("privacy.html", "Informativa sulla privacy | AMSIC", "Come AMSIC S.r.l. tratta i dati personali di chi visita il sito o la contatta.", "Informativa sulla privacy", PRIVACY),
    "cookie.html": lambda: pagina_testo("cookie.html", "Informativa sui cookie | AMSIC", "Il sito AMSIC non usa cookie di profilazione né di statistica.", "Informativa sui cookie", COOKIE),
    "grazie.html": pagina_grazie,
    "404.html": pagina_404,
}
IN_SITEMAP = ["index.html", "chi-siamo.html", "servizi.html", "trasparenza.html", "contatti.html", "privacy.html", "cookie.html"]

def main():
    for nome, fn in PAGINE.items():
        with open(os.path.join(ROOT, nome), "w", encoding="utf-8") as f:
            f.write(fn())
    righe = "".join(
        f'<url><loc>{BASE}/{"" if p == "index.html" else p[:-5]}</loc><lastmod>{OGGI}</lastmod></url>' for p in IN_SITEMAP)
    righe += "".join(f'<url><loc>{BASE}/assets/documenti/{f}</loc><lastmod>{OGGI}</lastmod></url>' for f, _, _ in DOCUMENTI)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{righe}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    print("pagine generate:", ", ".join(PAGINE))

if __name__ == "__main__":
    main()
