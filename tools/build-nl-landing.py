#!/usr/bin/env python3
"""Build the Dutch local service landing pages from the nl/services.html chrome
(head boilerplate, styles, nav, footer, scripts). Run from repo root; re-runnable."""
import re, json, html

ORIGIN = "https://unpeeldesign.com"
TPL = open("nl/services.html", encoding="utf-8").read()
STYLE = re.search(r"  <style>.*?</style>\n", TPL, re.S).group(0)
BODY_TOP = re.search(r"<body>.*?<main>\n", TPL, re.S).group(0)
BODY_END = re.search(r"</main>.*", TPL, re.S).group(0)
ANALYTICS = '  <script src="https://analytics.ahrefs.com/analytics.js" data-key="lHdxi6uilQ7AK1otl88LCA" async></script>\n'
FONTS = ('  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,700&display=swap" rel="stylesheet">\n'
         '  <link rel="icon" href="/uploads/LOGO%20ICON-02%202.jpg">\n'
         '  <link rel="stylesheet" href="/styles-v2.css">\n')

CASES = {
  "tuinen-arnaud": ("Tuinen Arnaud", "YXTMW11ZQrDM06YdtTzwwHI8xfA", "Branding · Webdesign"),
  "melabody":      ("Melabody", "wV5rrjFoD0UmrLmC4ldwBKDcgk", "Branding · Packaging"),
  "smashed":       ("Smashed", "GMhUNoPReTRI8UXw45EpLL2g", "Branding · Horeca"),
  "shared-ground": ("Shared Ground", "Mbin4nL2GlXWiaW6jQGfWaVZ4I", "Branding · Motion · Web"),
  "tuillerien":    ("Tuillerien", "ExAYxAsVkAaiyHVXURuYujmDbh4", "Branding · Hotel"),
}

def cards(slugs):
    out = []
    for i, s in enumerate(slugs):
        name, vid, tags = CASES[s]
        delay = f' style="transition-delay:.{i}s"' if i else ""
        out.append(f'''        <a class="svc-card fade-scale" href="/nl/works/{s}"{delay}>
          <video preload="none" src="/uploads/video/{vid}.mp4" autoplay muted loop playsinline loading="lazy" aria-label="{name}, {tags}"></video>
          <div class="svc-ghost"><p class="svc-ghost-name">{name}</p></div>
          <div class="svc-overlay"></div>
          <div class="svc-card-info"><p class="svc-card-title">{name}</p><p class="svc-card-tags">{tags}</p></div>
        </a>''')
    return "\n".join(out)

def items(lst):
    out = []
    for i, (n, d) in enumerate(lst):
        delay = f" d{i}" if i else ""
        out.append(f'''        <li class="svc-item fade-up{delay}">
          <span class="svc-item-n">{i+1:02d}</span>
          <div><span class="svc-item-name">{n}</span><span class="svc-item-desc">{d}</span></div>
        </li>''')
    return "\n".join(out)

def section(idx, sid, title, tagline, desc, lst, slugs):
    return f'''<!-- ═══ {sid.upper()} ═══ -->
<section id="{sid}" class="svc-section">
  <div class="svc-top fade-up">
    <span class="svc-num">{idx:02d}</span>
    <h2 class="svc-name">{title}</h2>
    <p class="svc-tagline">{tagline}</p>
  </div>
  <div class="svc-body">
    <div class="svc-left">
      <p class="svc-desc fade-up">{desc}</p>
      <ul class="svc-items">
{items(lst)}
      </ul>
    </div>
    <div class="svc-right">
      <div class="svc-cards">
{cards(slugs)}
      </div>
    </div>
  </div>
</section>
'''

STATS = re.search(r'<!-- ═══ SECTION 3 — STATS ═══ -->.*?</section>\n', TPL, re.S).group(0)

def page(p):
    e = html.escape
    sections = "".join(section(i + 1, *s) for i, s in enumerate(p["sections"]))
    ld_service = {
      "@context": "https://schema.org",
      "@type": "Service",
      "@id": f'{ORIGIN}{p["path"]}#service',
      "name": p["service_name"],
      "serviceType": p["service_type"],
      "description": p["description"],
      "url": f'{ORIGIN}{p["path"]}',
      "mainEntityOfPage": f'{ORIGIN}{p["path"]}',
      "inLanguage": "nl",
      "image": f'{ORIGIN}/uploads/works/{p["image"]}',
      "provider": {"@id": f"{ORIGIN}/#business"},
      "areaServed": [{"@type": "City", "name": "Gent"}, {"@type": "AdministrativeArea", "name": "Oost-Vlaanderen"}, {"@type": "Country", "name": "België"}],
      "availableLanguage": ["nl", "en"],
      "offers": {"@type": "Offer", "priceCurrency": "EUR", "price": p["price_from"], "description": p["offer_desc"],
                 "url": f"{ORIGIN}/nl/packages", "availability": "https://schema.org/InStock"},
    }
    ld_crumbs = {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{ORIGIN}/nl/"},
        {"@type": "ListItem", "position": 2, "name": "Diensten", "item": f"{ORIGIN}/nl/services"},
        {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": f'{ORIGIN}{p["path"]}'},
      ]}
    head = f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="theme-color" content="#ffffff">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(p["title"])}</title>
  <meta name="description" content="{e(p["description"])}">
  <meta property="og:title" content="{e(p["title"])}">
  <meta property="og:description" content="{e(p["description"])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{ORIGIN}{p["path"]}">
  <meta property="og:image" content="{ORIGIN}/uploads/works/{p["image"]}">
  <meta property="og:locale" content="nl_BE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(p["title"])}">
  <meta name="twitter:description" content="{e(p["description"])}">
  <meta name="twitter:image" content="{ORIGIN}/uploads/works/{p["image"]}">
  <link rel="canonical" href="{ORIGIN}{p["path"]}">
  <script type="application/ld+json">
{json.dumps(ld_service, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(ld_crumbs, ensure_ascii=False, indent=2)}
  </script>
{FONTS}{STYLE}{ANALYTICS}</head>
'''
    body_top = BODY_TOP.replace('<a href="/services">EN</a>', '<a href="/services">EN</a>')  # no EN twin: EN goes to the services overview
    main = f'''
<!-- ═══ HEADER ═══ -->
<section class="svcp-header">
  <p class="section-label fade-up">{p["label"]}</p>
  <h1 class="svcp-h1 fade-up d1">{p["h1"]}</h1>
  <p class="svcp-sub fade-up d2">{p["intro"]}</p>
</section>

{sections}
{STATS}
<!-- ═══ DARK CTA ═══ -->
<section class="svcp-cta">
  <h2 class="svcp-cta-h fade-up">{p["cta_h"]}</h2>
  <p class="svcp-cta-sub fade-up d1">{p["cta_sub"]}</p>
  <a href="/nl/contact" class="btn-white fade-up d2">Start een project →</a>
</section>

'''
    return head + body_top + main + BODY_END

PAGES = [
 {
  "path": "/nl/huisstijl-ontwerper-gent", "file": "nl/huisstijl-ontwerper-gent.html",
  "title": "Huisstijl ontwerper in Gent · Arnaud Boone | Unpeel",
  "description": "Huisstijl laten maken in Gent? Freelance ontwerper Arnaud Boone bouwt merkidentiteiten voor startups, horeca en zelfstandigen. Vanaf €1.000, in 1 tot 8 weken.",
  "image": "ZSHTbXMqr4PaBGUaZW6xuggvw.jpg", "crumb": "Huisstijl ontwerper Gent",
  "service_name": "Huisstijl ontwerpen in Gent", "service_type": "Huisstijl en merkidentiteit ontwerp",
  "price_from": "1000", "offer_desc": "Huisstijl pakketten Startup (vanaf €1.000), Studio (€1.000 – €3.000) en Full Brand (vanaf €3.000).",
  "label": "Huisstijl · Gent",
  "h1": "Huisstijl ontwerper<br>in Gent.",
  "intro": "Ik ben Arnaud Boone, freelance huisstijl ontwerper uit Gent. Ik ontwerp merkidentiteiten voor startups, horecazaken, zelfstandigen en kleine bedrijven in Gent en de rest van Oost-Vlaanderen: logo, kleuren, typografie, richtlijnen en alles wat je nodig hebt om er elke dag consistent uit te zien. Geen bureau, geen tussenlagen. Je werkt rechtstreeks met de ontwerper, van eerste gesprek tot oplevering.",
  "sections": [
   ("inbegrepen", "Wat zit er in een huisstijl?", "Meer dan een logo. Een systeem.",
    "Een huisstijl is het geheel van visuele keuzes dat jouw zaak herkenbaar maakt: op je gevel, je website, je visitekaartje en je Instagram. Een logo alleen volstaat niet, want een logo zonder regels valt uit elkaar zodra iemand anders ermee aan de slag gaat. Daarom lever ik altijd een systeem op, niet alleen een bestand. Zo ziet dat er concreet uit:",
    [("Logo en woordmerk", "Een primair logo, een horizontale variant en een icoon dat ook klein nog werkt, als favicon of profielfoto."),
     ("Kleurenpalet en typografie", "Kleuren met hun exacte codes voor print en scherm, en een lettertype-combinatie die je overal gratis of betaalbaar kunt gebruiken."),
     ("Huisstijlgids", "Een document van 15 tot 40 pagina's dat uitlegt hoe je alles gebruikt, zodat je drukker, webbouwer of collega niets hoeft te gokken."),
     ("Bronbestanden", "Alle bestanden in PNG, SVG, PDF en AI. Jij bent na oplevering volledig eigenaar van je merk.")],
    ["tuinen-arnaud", "melabody"]),
   ("werkwijze", "Zo werkt een huisstijltraject", "Eerst strategie, dan design.",
    "Elk huisstijlproject start met een gesprek over wie je bent, voor wie je werkt en waar je naartoe wil. Pas daarna teken ik. Die volgorde zorgt ervoor dat het eindresultaat vanzelfsprekend aanvoelt in plaats van willekeurig. Voor Tuinen Arnaud, een tuinaannemer uit Sint-Martens-Latem, leidde dat tot een strak woordmerk met een subtiele lijn en een boompictogram: modern, betrouwbaar en met oog voor detail, precies wat de zaak wilde uitstralen. Het traject in vier stappen:",
    [("Kennismaking en briefing", "Een videocall of een koffie in Gent. We bespreken je verhaal, je doelen, je publiek en je budget. Je krijgt binnen 24 uur een offerte."),
     ("Strategie en moodboard", "Positionering, tone of voice en een visuele richting die we samen vastleggen vóór ik begin te ontwerpen."),
     ("Ontwerp en feedback", "Logo, kleuren en typografie, met 2 tot 4 feedbackrondes afhankelijk van je pakket. Geen verrassingen, wel duidelijke keuzes."),
     ("Oplevering", "Huisstijlgids, alle bestanden en een korte uitleg zodat je er meteen mee aan de slag kunt.")],
    ["shared-ground", "tuillerien"]),
   ("prijs", "Wat kost een huisstijl in Gent?", "Transparante pakketten, geen verborgen kosten.",
    "Ik werk met drie vaste pakketten, zodat je vooraf weet wat je krijgt en wat het kost. Startup is een gericht logopakket voor wie met een klein budget professioneel wil starten: vanaf €1.000, klaar in 1 tot 2 weken. Studio is een volledige huisstijl met strategie, moodboard en huisstijlgids: tussen €1.000 en €3.000, in 3 tot 4 weken. Full Brand voegt daar een homepage-ontwerp, een motion asset en een verpakkingsontwerp aan toe: vanaf €3.000, in 6 tot 8 weken. Elk project start met een voorschot van 50%, de rest betaal je bij oplevering.",
    [("Startup", "Logo, kleurenpalet, typografie en een mini merkkaart. Vanaf €1.000, 1 tot 2 weken, 2 feedbackrondes."),
     ("Studio", "Strategie, moodboard, logosysteem, huisstijlgids en social media templates. €1.000 tot €3.000, 3 tot 4 weken, 3 feedbackrondes."),
     ("Full Brand", "Alles van Studio plus webdesign, motion en verpakking. Vanaf €3.000, 6 tot 8 weken, 4 feedbackrondes."),
     ("Op maat", "Zit je ergens tussenin? Vertel me wat je nodig hebt en je krijgt een offerte op maat.")],
    ["smashed"]),
  ],
  "cta_h": "Een huisstijl laten maken in Gent?",
  "cta_sub": "Vertel me over je zaak en je plannen. Je krijgt binnen 24 uur een eerlijk antwoord, een duidelijke scope en een prijs.",
 },
 {
  "path": "/nl/logo-ontwerp-gent", "file": "nl/logo-ontwerp-gent.html",
  "title": "Logo ontwerp in Gent · Arnaud Boone | Unpeel Design",
  "description": "Logo laten ontwerpen in Gent? Freelance ontwerper Arnaud Boone maakt onderscheidende logo's voor startups en horeca. Vanaf €1.000, klaar in 1 tot 2 weken.",
  "image": "qWr0EuA6QxGaaYY4IRKM0szW7AI.webp", "crumb": "Logo ontwerp Gent",
  "service_name": "Logo ontwerp in Gent", "service_type": "Logo ontwerp",
  "price_from": "1000", "offer_desc": "Logopakket Startup: logo, kleurenpalet, typografie en merkkaart vanaf €1.000, klaar in 1 tot 2 weken.",
  "label": "Logo · Gent",
  "h1": "Logo ontwerp<br>in Gent.",
  "intro": "Een goed logo is klein, eenvoudig en meteen herkenbaar. Het werkt op een gevel in de Veldstraat, op een koffiebeker, op een vrachtwagen en als icoontje van 32 pixels. Ik ben Arnaud Boone, freelance logo ontwerper uit Gent, en ik ontwerp logo's die vertrekken vanuit wat je zaak écht is, niet vanuit een trend die volgend jaar alweer gedateerd oogt.",
  "sections": [
   ("aanpak", "Een logo dat ergens over gaat", "Geen generator, geen template.",
    "Een logo-generator geeft je in twee minuten iets dat op duizend andere logo's lijkt. Een ontwerper geeft je een teken dat alleen van jou is. Voor Smashed, een smashed-burgerconcept in Gent, bracht ik het merk terug tot zijn kern, smaak, inclusiviteit en een duurzame mindset, en vertaalde dat naar een zacht, vriendelijk logo met een eigen mascotte. Voor Shared Ground, een wandelcommunity in Gent, zit het hele idee van ontmoeting in de overlappende, vloeiende vormen van het logo. Dat is wat een logo moet doen: in één blik vertellen waar je voor staat.",
    [("Woordmerk of beeldmerk", "We kiezen samen wat bij je past: een typografisch woordmerk, een symbool, of een combinatie van beide."),
     ("Schaalbaar en veelzijdig", "Elk logo wordt getest op klein formaat, in zwart-wit, op donkere achtergrond en in print, vóór je het te zien krijgt."),
     ("Uniek en registreerbaar", "Ik controleer op gelijkenissen met bestaande merken in je sector, zodat je geen logo krijgt dat al bestaat."),
     ("Klaar voor alles", "Je ontvangt het logo in alle varianten en formaten: PNG, SVG, PDF, in kleur, wit en zwart.")],
    ["smashed", "shared-ground"]),
   ("proces", "Van briefing tot oplevering in 1 tot 2 weken", "Snel, maar niet gehaast.",
    "Een logo-traject bij Unpeel is kort en helder. Je hoeft geen eindeloze vragenlijsten in te vullen en je krijgt geen tien willekeurige voorstellen om uit te kiezen. Je krijgt één of twee doordachte richtingen, met uitleg waarom ze werken, en we verfijnen samen tot het klopt.",
    [("Dag 1 tot 2: briefing", "Een gesprek over je zaak, je klanten en je concurrenten. Ik maak een kort moodboard om de richting vast te leggen."),
     ("Dag 3 tot 7: ontwerp", "Schetsen, selectie en uitwerking van de sterkste richting in woordmerk, icoon en varianten."),
     ("Dag 8 tot 10: feedback", "Twee feedbackrondes waarin we proporties, kleur en details bijsturen."),
     ("Dag 10 tot 14: oplevering", "Alle bestanden plus een merkkaart van één pagina met je logo, kleuren en lettertypes.")],
    ["tuinen-arnaud"]),
   ("prijs", "Wat kost een logo laten ontwerpen in Gent?", "Vanaf €1.000, alles inbegrepen.",
    "Het Startup-pakket is gemaakt voor wie een sterk logo nodig heeft zonder groot budget: logo met horizontale variant, een kleurenpalet van 2 tot 3 kleuren, een typografie-selectie en een mini merkkaart. Vanaf €1.000, klaar in 1 tot 2 weken, met 2 feedbackrondes. Wil je er meteen een volledige huisstijl van maken, met strategie, huisstijlgids en social media templates? Dan kies je voor Studio, tussen €1.000 en €3.000. Je kunt altijd met een logo starten en later upgraden; het logo blijft de basis.",
    [("Startup: vanaf €1.000", "Logo, kleuren, typografie, merkkaart. 1 tot 2 weken."),
     ("Studio: €1.000 – €3.000", "Alles van Startup plus strategie, huisstijlgids en templates. 3 tot 4 weken."),
     ("Betaling", "50% voorschot bij de start, 50% bij oplevering. Betaaltermijn 14 dagen."),
     ("Eigendom", "Na oplevering ben jij volledig eigenaar van het logo, inclusief de bronbestanden.")],
    ["melabody", "tuillerien"]),
  ],
  "cta_h": "Een logo laten ontwerpen?",
  "cta_sub": "Stuur me een korte beschrijving van je zaak. Binnen 24 uur weet je of we een match zijn en wat het kost.",
 },
 {
  "path": "/nl/branding-horeca-gent", "file": "nl/branding-horeca-gent.html",
  "title": "Branding voor horeca in Gent · Arnaud Boone | Unpeel",
  "description": "Huisstijl en branding voor restaurants, cafés, bars en hotels in Gent. Brand designer Arnaud Boone ontwerpt identiteiten die gasten onthouden. Vanaf €1.000.",
  "image": "qWr0EuA6QxGaaYY4IRKM0szW7AI.webp", "crumb": "Branding horeca Gent",
  "service_name": "Branding voor horeca in Gent", "service_type": "Huisstijl en branding voor restaurants, cafés en hotels",
  "price_from": "1000", "offer_desc": "Horeca branding pakketten vanaf €1.000 (logo) tot een volledige identiteit met menukaart, signage en website.",
  "label": "Horeca · Gent",
  "h1": "Branding voor horeca<br>in Gent.",
  "intro": "Gent telt honderden restaurants, cafés, bars en hotels. Je gasten kiezen in een paar seconden, op Instagram, op Google Maps of al wandelend voorbij je gevel. Een sterke identiteit maakt dat verschil. Ik ben Arnaud Boone, freelance brand designer uit Gent, en ik ontwerp huisstijlen voor horecazaken die even goed werken op een menukaart als op een story.",
  "sections": [
   ("horeca", "Waarom horeca anders is", "Je merk hangt letterlijk aan de muur.",
    "Een horeca-identiteit leeft op meer plekken dan eender welk ander merk: de gevel, het raam, de menukaart, de koffiebekers, de uniformen, de verpakking voor afhaal, de Instagram-feed en de Google-vermelding. Alles moet dezelfde taal spreken, anders voelt de zaak rommelig aan, hoe goed het eten ook is. Voor Smashed, een smashed-burgerconcept in Gent voor studenten en jonge professionals, ontwierp ik een speelse identiteit met een zacht logo en een eigen mascotte die gastvrij, energiek en vol persoonlijkheid aanvoelt. Voor Tuillerien, een vijfsterren boetiekhotel in Brugge, net het tegenovergestelde: verheven, precies en nooit luid.",
    [("Logo en huisstijl", "Een logo dat werkt op een lichtbak én op een stempel, met kleuren en lettertypes die bij je keuken en je publiek passen."),
     ("Menukaart en print", "Menu's, bierkaarten, tafelkaartjes, flyers en stickers, ontworpen als één geheel en drukklaar aangeleverd."),
     ("Signage en gevel", "Advies en ontwerp voor je uithangbord, raambelettering en bewegwijzering in de zaak."),
     ("Verpakking voor afhaal", "Bekers, zakken en dozen die je merk mee naar buiten nemen, de goedkoopste reclame die er is.")],
    ["smashed", "tuillerien"]),
   ("digitaal", "Van gevel tot Instagram", "Eén identiteit, overal herkenbaar.",
    "De meeste gasten zien je zaak eerst online. Daarom hoort bij een horeca-huisstijl ook een digitale laag: social media templates zodat je stories en posts er consistent uitzien, een Google Business-profiel met de juiste beelden, en als je dat wilt een eenvoudige website met menu, openingsuren en reservatieknop. Ik ontwerp dat allemaal vanuit dezelfde huisstijl, zodat een gast die je op Instagram ontdekt, je gevel meteen herkent.",
    [("Social media kit", "Drie tot zes templates voor posts, stories en highlight covers in Canva of Figma, zodat je team ze zelf kan invullen."),
     ("Website of landingspagina", "Een snelle, mobiele pagina met menu, openingsuren, locatie en reservatie. Ontworpen in Figma en klaar voor je webbouwer, of door mij gebouwd."),
     ("Motion", "Een geanimeerd logo of korte brand intro voor reels, je website of het scherm boven de toog."),
     ("AI-video", "Product- en sfeervideo's van je gerechten en je zaak, gemaakt met AI onder creatieve regie, voor advertenties en social media.")],
    ["shared-ground", "tuinen-arnaud"]),
   ("prijs", "Wat kost branding voor een horecazaak?", "Vanaf €1.000, afgestemd op je opening.",
    "Open je binnenkort een zaak, dan is timing alles. Daarom werk ik met vaste pakketten en vaste doorlooptijden. Startup geeft je een logo, kleuren en typografie vanaf €1.000, klaar in 1 tot 2 weken: genoeg om je gevel en je Instagram te starten. Studio is een volledige huisstijl met strategie, huisstijlgids en social media templates, tussen €1.000 en €3.000, in 3 tot 4 weken. Full Brand voegt daar een homepage-ontwerp, een motion asset en een verpakkingsontwerp aan toe, vanaf €3.000, in 6 tot 8 weken. Menukaarten, signage en extra drukwerk begroot ik apart op basis van wat je zaak nodig heeft.",
    [("Opening over 1 maand", "Startup: logo, kleuren en typografie zodat je gevel, kaart en social media op tijd klaar zijn."),
     ("Opening over 2 tot 3 maanden", "Studio: volledige huisstijl plus templates, met tijd voor menukaart en signage."),
     ("Rebranding van een bestaande zaak", "Full Brand of op maat: we bouwen verder op wat al werkt en vernieuwen wat niet meer past."),
     ("Betaling", "50% voorschot bij de start, 50% bij oplevering. Jij bent na oplevering volledig eigenaar.")],
    ["melabody"]),
  ],
  "cta_h": "Een nieuwe zaak of een frisse start?",
  "cta_sub": "Vertel me wat je opent, voor wie en wanneer. Je krijgt binnen 24 uur een eerlijk advies, een scope en een prijs.",
 },
]

for p in PAGES:
    out = page(p)
    open(p["file"], "w", encoding="utf-8").write(out)
    words = len(re.sub(r"<[^>]+>", " ", re.search(r"<main>.*?</main>", out, re.S).group(0)).split())
    print(f'wrote {p["file"]}  main words={words}')
