/* AMSIC — menu, comparse, barra da telefono, modulo contatti, mappa su richiesta */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var riduciMovimento = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- testata: ombra allo scorrimento e menu da telefono */
  var testata = document.querySelector("[data-testata]");
  var bottoneMenu = document.querySelector("[data-menu]");
  function chiudiMenu() {
    if (!testata) return;
    testata.classList.remove("aperto");
    if (bottoneMenu) bottoneMenu.setAttribute("aria-expanded", "false");
  }
  if (testata) {
    var ombra = function () { testata.classList.toggle("scorsa", window.scrollY > 8); };
    window.addEventListener("scroll", ombra, { passive: true });
    ombra();
  }
  if (bottoneMenu && testata) {
    bottoneMenu.addEventListener("click", function () {
      var aperto = testata.classList.toggle("aperto");
      bottoneMenu.setAttribute("aria-expanded", aperto ? "true" : "false");
    });
    testata.querySelectorAll(".nav a").forEach(function (a) { a.addEventListener("click", chiudiMenu); });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") chiudiMenu(); });
    window.addEventListener("resize", function () { if (window.innerWidth >= 1000) chiudiMenu(); });
  }

  /* ---------- comparsa degli elementi */
  var daRivelare = document.querySelectorAll(".rivela");
  if ("IntersectionObserver" in window && !riduciMovimento) {
    var osservatore = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) {
        if (v.isIntersecting) { v.target.classList.add("visto"); osservatore.unobserve(v.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    daRivelare.forEach(function (el) {
      // ciò che è già sullo schermo all'apertura compare subito, senza animazione
      if (el.getBoundingClientRect().top < window.innerHeight * 0.92) el.classList.add("visto", "subito");
      else osservatore.observe(el);
    });
  } else {
    daRivelare.forEach(function (el) { el.classList.add("visto"); });
  }

  /* ---------- barra fissa da telefono: compare quando i pulsanti principali escono dallo schermo */
  var barra = document.querySelector("[data-barra]");
  if (barra) {
    var imposta = function (visibile) {
      barra.classList.toggle("visibile", visibile);
      barra.setAttribute("aria-hidden", visibile ? "false" : "true");
      barra.querySelectorAll("a").forEach(function (a) {
        if (visibile) a.removeAttribute("tabindex"); else a.setAttribute("tabindex", "-1");
      });
    };
    var sentinella = document.querySelector("[data-sentinella]");
    if (sentinella && "IntersectionObserver" in window) {
      new IntersectionObserver(function (voci) {
        var v = voci[0];
        imposta(!v.isIntersecting && v.boundingClientRect.top < 0);
      }).observe(sentinella);
    } else {
      var aScorrimento = function () { imposta(window.scrollY > 420); };
      window.addEventListener("scroll", aScorrimento, { passive: true });
      aScorrimento();
    }
  }

  /* ---------- mappa caricata solo su richiesta (niente cookie di Google prima del clic) */
  document.querySelectorAll("[data-mappa]").forEach(function (box) {
    var b = box.querySelector("[data-mappa-btn]");
    if (!b) return;
    b.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = box.getAttribute("data-mappa");
      f.title = "Mappa della sede AMSIC";
      f.loading = "lazy";
      f.referrerPolicy = "no-referrer-when-downgrade";
      box.innerHTML = "";
      box.appendChild(f);
    });
  });

  /* ---------- modulo contatti (FormSubmit, con ripiego email) */
  var modulo = document.querySelector("[data-modulo]");
  if (!modulo) return;
  var esito = modulo.querySelector("[data-esito]");
  var bottone = modulo.querySelector('button[type="submit"]');
  var etichetta = modulo.querySelector("[data-etichetta]");
  var testoBottone = etichetta ? etichetta.textContent : "";

  // servizio preselezionato da servizi?servizio=<id>
  try {
    var id = new URLSearchParams(window.location.search).get("servizio");
    if (id) {
      var opzione = modulo.querySelector('option[data-id="' + id.replace(/[^a-z0-9-]/g, "") + '"]');
      if (opzione) opzione.selected = true;
    }
  } catch (err) { /* browser molto vecchi: nessuna preselezione */ }

  function mostra(tipo, html) {
    esito.className = "esito " + tipo;
    esito.innerHTML = html;
    esito.hidden = false;
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function valida() {
    var primo = null;
    modulo.querySelectorAll("[required]").forEach(function (c) {
      var ok = c.type === "checkbox" ? c.checked : c.value.trim() !== "";
      if (ok && c.type === "email") ok = emailOk.test(c.value.trim());
      var contenitore = c.closest(".campo, .consenso");
      if (contenitore) contenitore.classList.toggle("invalido", !ok);
      c.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok && !primo) primo = c;
    });
    return primo;
  }
  modulo.addEventListener("input", function (ev) {
    var c = ev.target.closest(".invalido");
    if (c) { c.classList.remove("invalido"); ev.target.setAttribute("aria-invalid", "false"); }
  });
  modulo.addEventListener("change", function (ev) {
    if (ev.target.type === "checkbox") {
      var c = ev.target.closest(".invalido");
      if (c && ev.target.checked) c.classList.remove("invalido");
    }
  });

  function ripiego(dati) {
    var email = modulo.getAttribute("data-email");
    var tel = modulo.getAttribute("data-tel");
    var righe = ["Nome: " + (dati.Nome || ""), "Azienda: " + (dati.Azienda || ""), "Email: " + (dati.email || ""),
      "Telefono: " + (dati.Telefono || ""), "Servizio: " + (dati.Servizio || ""), "", dati.Messaggio || ""];
    var link = "mailto:" + email + "?subject=" + encodeURIComponent("Richiesta dal sito AMSIC") + "&body=" + encodeURIComponent(righe.join("\n"));
    mostra("errore",
      "<p>Non siamo riusciti a inviare il modulo in questo momento.</p>" +
      '<p><a href="' + esc(link) + '">Invia la richiesta via email</a> (si apre il tuo programma di posta con il testo già pronto) oppure chiamaci al <a href="tel:' + esc(tel.replace(/\s/g, "")) + '">' + esc(tel) + "</a>.</p>");
  }

  modulo.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var primo = valida();
    if (primo) {
      mostra("errore", "<p>Controlla i campi evidenziati: mancano alcune informazioni obbligatorie.</p>");
      primo.focus();
      return;
    }
    var fd = new FormData(modulo);
    if ((fd.get("_honey") || "") !== "") return;
    var dati = {};
    fd.forEach(function (v, k) { if (k !== "_next" && k !== "_honey") dati[k] = v; });
    dati._subject = "Richiesta dal sito AMSIC – " + (dati.Azienda || dati.Nome);
    dati._replyto = dati.email;

    bottone.disabled = true;
    if (etichetta) etichetta.textContent = "Invio in corso…";
    esito.hidden = true;

    fetch(modulo.getAttribute("data-endpoint"), {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(dati)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; });
    }).then(function (res) {
      if (res.ok && String(res.j.success) === "true") {
        modulo.reset();
        mostra("ok", "<p><strong>Grazie, richiesta inviata.</strong> Ti ricontatteremo al più presto.</p>");
      } else {
        ripiego(dati);
      }
    }).catch(function () {
      ripiego(dati);
    }).then(function () {
      bottone.disabled = false;
      if (etichetta) etichetta.textContent = testoBottone;
      esito.scrollIntoView({ block: "nearest", behavior: riduciMovimento ? "auto" : "smooth" });
    });
  });
})();
