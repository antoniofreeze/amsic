# Sito AMSIC S.r.l. a Socio unico

Sito statico (HTML, CSS e JavaScript, nessun framework) pubblicato con GitHub Pages dal repository `antoniofreeze/amsic`.
Dominio definitivo: **www.amsic.it** (registrato su Aruba).

## Come si aggiorna

1. Testi, servizi, recapiti, documenti: si cambiano in **`build.py`** (in alto c'è `AZIENDA`, poi `SERVIZI`, `DOCUMENTI`…).
2. `python3 build.py` rigenera tutte le pagine, `sitemap.xml` e `robots.txt`.
3. Se cambi CSS o JS, aumenta `VERSIONE` in `build.py` (evita la cache dei browser).
4. `git add -A && git commit -m "…" && git push`: GitHub Pages pubblica in un paio di minuti.

Foto, logo, icone e PDF si preparano con **`prepara_asset.py`** partendo da `_originali/` (non pubblicata) e dalla cartella cliente `ARCHIVIO FREEZE/Clienti/AMSIC`.

## Anteprima in locale

`python3 anteprima.py 4241 .` e apri http://localhost:4241 (imita GitHub Pages: `/servizi` serve `servizi.html`).

## Da completare quando arrivano i dati

- `AZIENDA["rea"]` e `AZIENDA["capitale"]`: numero REA e capitale sociale (compaiono nel piè di pagina appena compilati).
- `AZIENDA["whatsapp"]`: se il 351 964 7981 è anche WhatsApp, scrivere `"393519647981"` → compaiono i pulsanti WhatsApp.
- Modulo contatti: usa FormSubmit verso `direzioneamsic@gmail.com`. Alla **prima richiesta** FormSubmit manda a quella casella una mail "Activate Form": va cliccata una volta, poi le richieste arrivano normalmente. Finché non è attivato, il sito propone l'invio via email e il telefono.

## Dominio amsic.it (Aruba)

Record DNS da impostare nel pannello Aruba:

| Tipo | Nome | Valore |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | antoniofreeze.github.io |

Poi: file `CNAME` con `www.amsic.it` nel repository, dominio personalizzato nelle impostazioni Pages, "Enforce HTTPS" quando il certificato è pronto.
Non toccare eventuali record MX/SPF della posta.
