#!/usr/bin/env python3
"""Expand the nine case studies (EN + NL) with brief / approach / deliverables /
result sections and enrich their CreativeWork JSON-LD. Idempotent: skips a page
that already contains the expanded block. Run from repo root."""
import re, json, html

ORIGIN = "https://unpeeldesign.com"
H = {"en": ("The brief", "The approach", "What was delivered", "The result"),
     "nl": ("De briefing", "De aanpak", "Wat werd opgeleverd", "Het resultaat")}

C = {
"aaronblommaert": {
 "genre": ["Branding", "Motion Design", "Web Design"],
 "keywords": "artist branding, visual identity, motion design, web design, Ghent",
 "en": dict(
  brief="Aaron Blommaert is an artist based in Ghent who performs, questions and flips perspectives rather than simply presenting finished work. He needed an identity that could follow him across stage, screen and social media without flattening that energy into a neat logo. The ask was a brand identity, motion design and a website that feel like him on a good day: real, raw and endlessly curious.",
  approach="The starting point was a simple observation: this brand is not about creating a persona, it is about revealing one. Instead of a fixed mark and a rigid grid, the identity is built as a visual world with rules loose enough to stay alive. Colour is allowed to collide with emotion, compositions sit slightly off-balance, and imperfection is treated as character rather than error. Motion is part of the system from the first sketch, because an identity for a performer has to move. The imagery for this project was generated with AI under creative direction, which kept the look consistent across formats while leaving room for the unexpected.",
  deliverables=["Brand identity: logo, colour world and typography built for an off-balance, energetic layout language", "Motion design: animated identity elements for video, stories and live use", "Web design: a website that carries the same restless energy on screen", "Imagery direction: AI-generated visuals art-directed to the brand"],
  result="The outcome is an identity that stays in motion and never feels too polished, exactly the point for an artist who refuses to sit still. It gives Aaron one coherent visual language for everything he puts out, from a reel to a show poster, and it is live on his own website, linked above. Unfiltered by nature, upside down by choice."),
 "nl": dict(
  brief="Aaron Blommaert is een kunstenaar uit Gent die optreedt, bevraagt en perspectieven omdraait in plaats van afgewerkt werk netjes te presenteren. Hij had een identiteit nodig die hem kon volgen op het podium, op het scherm en op social media, zonder die energie plat te slaan tot een proper logo. De vraag: een merkidentiteit, motion design en een website die aanvoelen als hijzelf op een goede dag: echt, rauw en eindeloos nieuwsgierig.",
  approach="Het vertrekpunt was een eenvoudige vaststelling: dit merk gaat niet over een persona bouwen, maar over er één onthullen. In plaats van een vast teken en een strak raster is de identiteit opgezet als een visuele wereld met regels die losjes genoeg zijn om levend te blijven. Kleur mag botsen met emotie, composities staan lichtjes uit balans en imperfectie wordt karakter in plaats van fout. Motion zit van de eerste schets in het systeem, want een identiteit voor een performer moet bewegen. De beelden voor dit project werden met AI gegenereerd onder creatieve regie, wat de look consistent hield over alle formaten en tegelijk ruimte liet voor het onverwachte.",
  deliverables=["Merkidentiteit: logo, kleurenwereld en typografie, gebouwd voor een energieke, lichtjes ontregelde lay-outtaal", "Motion design: geanimeerde identiteitselementen voor video, stories en live gebruik", "Webdesign: een website die dezelfde rusteloze energie op het scherm brengt", "Beeldregie: AI-gegenereerde visuals, art-directed naar het merk"],
  result="Het resultaat is een identiteit die in beweging blijft en nooit te gepolijst aanvoelt, precies het punt voor een kunstenaar die weigert stil te zitten. Aaron heeft nu één samenhangende visuele taal voor alles wat hij naar buiten brengt, van een reel tot een affiche, en ze staat live op zijn eigen website, hierboven gelinkt. Ongefilterd van nature, ondersteboven uit keuze."),
},
"hella-fast": {
 "genre": ["Type Design", "Branding", "Motion Design"],
 "keywords": "modular typeface, type design, brand identity system, motion design, F1",
 "en": dict(
  brief="HELLA FAST started as a type design project, not a client commission: a modular typeface built for pure speed, inspired by the sharp turns and sweeping lines of Formula 1 race tracks. The question was whether a single typeface could carry an entire brand identity on its own, from a monotype print to posters, motion and merchandise, without borrowing a logo or an illustration style.",
  approach="Every decision in the system is driven by the letterforms themselves. The curves and cuts of the typeface set the angles of the grid, the high-contrast layouts and the rhythm of the motion work. Rather than designing a logo and then choosing a font, the font is the logo, the pattern and the voice at once. The visual language borrows the energy of racing, bold grids, racing-fuel colour and hard contrast, while staying precise enough to read at speed. The project was presented through high-quality photographic mockups to show the system at real-world scale.",
  deliverables=["A modular display typeface with a full character set built on a speed-driven construction logic", "A brand identity system derived from the type: grid, colour, contrast and layout rules", "Motion design: animated type studies that turn the letterforms into a visual engine", "Application mockups: posters, print and merchandise showing the system in use"],
  result="The result proves the premise: HELLA FAST works as a visual engine, not just a font. One typeface generates a complete, recognisable identity that holds together across static and moving formats. It remains one of the clearest demonstrations of how I approach branding: find the one idea at the core and let everything else grow from it. That same logic applies whether the core is a typeface, a laurel symbol or a founder's story."),
 "nl": dict(
  brief="HELLA FAST begon als een type design-project, geen klantopdracht: een modulair lettertype gebouwd voor pure snelheid, geïnspireerd op de scherpe bochten en lange lijnen van Formule 1-circuits. De vraag was of één lettertype een volledige merkidentiteit kan dragen, van een monotype-print tot affiches, motion en merchandise, zonder een logo of illustratiestijl te lenen.",
  approach="Elke beslissing in het systeem vertrekt vanuit de letters zelf. De curves en snedes van het lettertype bepalen de hoeken van het raster, de hoge contrasten in de lay-outs en het ritme van het motion-werk. In plaats van eerst een logo te ontwerpen en dan een font te kiezen, is het font tegelijk logo, patroon en stem. De visuele taal leent de energie van de racerij, stevige rasters, racing-fuel-kleuren en hard contrast, en blijft precies genoeg om leesbaar te zijn op snelheid. Het project werd gepresenteerd met fotografische mockups van hoge kwaliteit om het systeem op ware grootte te tonen.",
  deliverables=["Een modulair display-lettertype met volledige tekenset, gebouwd op een constructielogica rond snelheid", "Een merkidentiteitssysteem afgeleid van het lettertype: raster, kleur, contrast en lay-outregels", "Motion design: geanimeerde typestudies die de letters omzetten in een visuele motor", "Toepassingsmockups: affiches, print en merchandise die het systeem in gebruik tonen"],
  result="Het resultaat bewijst het uitgangspunt: HELLA FAST werkt als een visuele motor, niet enkel als een font. Eén lettertype genereert een volledige, herkenbare identiteit die standhoudt in stilstaande en bewegende formaten. Het blijft een van de duidelijkste voorbeelden van hoe ik branding aanpak: zoek het ene idee in de kern en laat al de rest daaruit groeien. Diezelfde logica geldt of de kern nu een lettertype, een lauriersymbool of het verhaal van een founder is."),
},
"melabody": {
 "genre": ["Branding", "Packaging Design"],
 "keywords": "body care branding, packaging design, inclusive design, melanin-rich skin, gradient identity",
 "en": dict(
  brief="Melabody is a conceptual body-care brand, a self-initiated project rather than a client commission, created to explore one question: what does body care look like when it is designed for melanin-rich skin from the start, instead of as an afterthought? The brief I set myself was a complete brand identity and a packaging system that feel nourishing, warm and inclusive without leaning on the clichés of the category.",
  approach="The identity is built around three ideas: nourishment, warmth and inclusivity. Rather than flat colour blocks, the system uses a three-tone gradient palette of orange, blue and green, standing for warmth, hydration and balance. Gradients were a deliberate choice: skin holds depth, moisture and variation, and a gradient shows that layering in a way a solid colour cannot. Typography is kept minimal so the skin imagery stays central, and the packaging follows one unified structure across the range so the shelf reads as a family, not a collection of individual bottles.",
  deliverables=["Brand identity: wordmark, gradient colour system and minimal typography", "Packaging system: a unified structure and label logic for the full product range", "Art direction for skin photography that keeps people, not products, at the centre", "Presentation visuals showing the range as it would appear in retail"],
  result="Melabody positions body care as something rooted in intention rather than trends. As a concept project it has no sales figures to report, but it does what it was built to do: show how a brand can be inclusive by design rather than by messaging. Designed for melanin. Made to nourish. The same thinking, strategy first and a palette that means something, is what I bring to packaging work for real brands."),
 "nl": dict(
  brief="Melabody is een conceptueel bodycare-merk, een eigen initiatief en geen klantopdracht, gemaakt om één vraag te onderzoeken: hoe ziet bodycare eruit als ze van bij het begin voor melaninerijke huid ontworpen is, in plaats van als bijzaak? De briefing die ik mezelf gaf: een volledige merkidentiteit en een verpakkingssysteem die voedend, warm en inclusief aanvoelen zonder te leunen op de clichés van de categorie.",
  approach="De identiteit is gebouwd rond drie ideeën: voeding, warmte en inclusiviteit. In plaats van vlakke kleurblokken gebruikt het systeem een gradiëntpalet in drie tonen, oranje, blauw en groen, voor warmte, hydratatie en balans. Die gradiënten zijn een bewuste keuze: huid heeft diepte, vocht en variatie, en een gradiënt toont die gelaagdheid op een manier die een effen kleur niet kan. De typografie blijft minimaal zodat de huidbeelden centraal staan, en de verpakking volgt één structuur over het hele gamma, zodat het rek leest als een familie en niet als losse flessen.",
  deliverables=["Merkidentiteit: woordmerk, gradiëntkleurensysteem en minimale typografie", "Verpakkingssysteem: één structuur en etiketlogica voor het volledige gamma", "Beeldregie voor huidfotografie die mensen, niet producten, centraal zet", "Presentatiebeelden die het gamma tonen zoals het in de winkel zou staan"],
  result="Melabody positioneert bodycare als iets dat vertrekt vanuit intentie in plaats van trends. Als conceptproject heeft het geen verkoopcijfers om te rapporteren, maar het doet waarvoor het gebouwd is: tonen hoe een merk inclusief kan zijn door ontwerp, niet door boodschappen. Ontworpen voor melanine. Gemaakt om te voeden. Dezelfde denkwijze, strategie eerst en een palet dat iets betekent, neem ik mee in verpakkingswerk voor echte merken."),
},
"shared-ground": {
 "genre": ["Branding", "Motion Design", "Web Design"],
 "keywords": "community branding, walking community, logo design, motion design, web design, Ghent",
 "en": dict(
  brief="Shared Ground is a walking community in Ghent built around a simple idea: connection starts at street level. In a city where most contact happens through screens, the project invites people to slow down, step outside and meet each other on shared walks. The founders needed a full identity, motion design and a website that could introduce the idea to strangers and make joining a walk feel easy and open.",
  approach="The strategy came first: what is this community really about? The answer was movement and intersection, different routes and different people coming together to find common ground. That idea became the logo literally. Soft, flowing curves are drawn from walking paths and the natural rhythm of a stride, and the overlapping shapes stand for people meeting and sharing space. The colour palette is taken from the city itself: earthy olive and charcoal echo streets and urban textures, a muted blue brings calm, and a vibrant yellow accent adds the energy of a group setting off. Motion extends the logo's curves into movement, and the website keeps the same open, human tone.",
  deliverables=["Brand identity: logo, colour palette drawn from the city and a typography system", "Brand guidelines so the community can keep its own communication consistent", "Motion design: animated logo and identity elements for social media and video", "Web design: a website that explains the idea and makes joining a walk straightforward"],
  result="Shared Ground now has a visual system that feels contemporary, distinctive and human, which is exactly the tone a community about meeting people needs. It gives the founders a coherent identity for everything from a route map to an Instagram post, and a website that does the first job of any community: making a newcomer feel welcome before they have taken a step."),
 "nl": dict(
  brief="Shared Ground is een wandelcommunity in Gent rond een eenvoudig idee: verbinding begint op straatniveau. In een stad waar het meeste contact via schermen loopt, nodigt het project mensen uit om te vertragen, naar buiten te stappen en elkaar te ontmoeten op gedeelde wandelingen. De oprichters hadden een volledige identiteit, motion design en een website nodig om het idee aan onbekenden voor te stellen en meewandelen eenvoudig en open te laten aanvoelen.",
  approach="De strategie kwam eerst: waar gaat deze community echt over? Het antwoord was beweging en kruising, andere routes en andere mensen die samenkomen om gedeelde grond te vinden. Dat idee werd letterlijk het logo. Zachte, vloeiende curves komen uit wandelpaden en het natuurlijke ritme van een stap, en de overlappende vormen staan voor mensen die elkaar ontmoeten en ruimte delen. Het kleurenpalet komt uit de stad zelf: aardse olijf- en houtskooltinten verwijzen naar straten en stadse texturen, een gedempt blauw brengt rust en een levendig geel accent voegt de energie toe van een groep die vertrekt. Motion trekt de curves van het logo door in beweging, en de website houdt dezelfde open, menselijke toon aan.",
  deliverables=["Merkidentiteit: logo, kleurenpalet uit de stad en een typografisch systeem", "Merkrichtlijnen zodat de community haar eigen communicatie consistent houdt", "Motion design: geanimeerd logo en identiteitselementen voor social media en video", "Webdesign: een website die het idee uitlegt en meewandelen eenvoudig maakt"],
  result="Shared Ground heeft nu een visueel systeem dat eigentijds, eigenzinnig en menselijk aanvoelt, precies de toon die een community over ontmoeting nodig heeft. De oprichters hebben een samenhangende identiteit voor alles van een routekaart tot een Instagram-post, en een website die de eerste taak van elke community vervult: een nieuwkomer zich welkom laten voelen nog voor hij een stap heeft gezet."),
},
"smashed": {
 "genre": ["Branding", "Hospitality Branding"],
 "keywords": "restaurant branding, smash burger, street food identity, mascot design, logo design, Ghent",
 "en": dict(
  brief="Smashed is a young smashed-burger concept in Ghent made for today's city crowd: bold flavour, good vibes and plenty of vegan options. The team needed a brand identity that would work on a storefront, a menu board, packaging and Instagram at the same time, and that would speak to students and young professionals looking for a quick but quality bite without feeling like every other burger place.",
  approach="I unpeeled the brand to its core and found three things worth building on: flavour, inclusivity and a modern, sustainable mindset. Those became the brief for the visuals. The logo is soft and friendly rather than loud and greasy, which already sets Smashed apart on a street full of shouting fast-food signs. A custom mascot carries the brand's character into places where a logo alone would feel flat: packaging, social posts and in-store details. The identity was tested across print, digital and in-store applications through high-quality photographic mockups before anything went to production.",
  deliverables=["Brand identity: logo, colour palette and typography built for signage, menus and screens", "A custom mascot that brings the brand's personality to packaging and social media", "Application design: packaging, menu and in-store visuals shown in context", "Brand guidelines so the identity stays consistent as the concept grows"],
  result="The result is a fresh visual world that feels welcoming, energetic and full of personality. Smashed has an identity that is playful without losing credibility, and that works across print, digital and in-store, which is what a hospitality brand needs most: one recognisable face everywhere a guest meets it. For a concept aimed at students and young professionals in Ghent, that consistency is what turns a first visit into a habit."),
 "nl": dict(
  brief="Smashed is een jong smashed-burgerconcept in Gent voor het stadspubliek van vandaag: stevige smaak, goeie vibes en volop veggie-opties. Het team had een merkidentiteit nodig die tegelijk werkt op een gevel, een menubord, verpakking en Instagram, en die studenten en jonge professionals aanspreekt die snel maar kwalitatief willen eten, zonder op elke andere burgerzaak te lijken.",
  approach="Ik bracht het merk terug tot zijn kern en vond drie dingen om op te bouwen: smaak, inclusiviteit en een moderne, duurzame mindset. Die werden de briefing voor de visuals. Het logo is zacht en vriendelijk in plaats van luid en vettig, wat Smashed meteen onderscheidt in een straat vol schreeuwende fastfoodborden. Een eigen mascotte draagt het karakter van het merk naar plekken waar een logo alleen vlak zou aanvoelen: verpakking, social posts en details in de zaak. De identiteit werd getest op print, digitaal en in-store via fotografische mockups van hoge kwaliteit, nog voor er iets in productie ging.",
  deliverables=["Merkidentiteit: logo, kleurenpalet en typografie gebouwd voor signage, menu's en schermen", "Een eigen mascotte die de persoonlijkheid van het merk naar verpakking en social media brengt", "Toepassingsontwerp: verpakking, menu en in-store visuals in context getoond", "Merkrichtlijnen zodat de identiteit consistent blijft terwijl het concept groeit"],
  result="Het resultaat is een frisse visuele wereld die gastvrij, energiek en vol persoonlijkheid aanvoelt. Smashed heeft een identiteit die speels is zonder geloofwaardigheid te verliezen en die werkt op print, digitaal en in de zaak, wat een horecamerk het meest nodig heeft: één herkenbaar gezicht overal waar een gast het tegenkomt. Voor een concept gericht op studenten en jonge professionals in Gent is die consistentie wat een eerste bezoek omzet in een gewoonte."),
},
"stellar-secrets": {
 "genre": ["Editorial Design", "Book Design", "Packaging Design"],
 "keywords": "book design, editorial design, space, print design, packaging, Ghent",
 "en": dict(
  brief="Stellar Secrets is a book design project about space, built to make the universe feel within reach. The challenge was editorial and physical at once: how do you give a reader a sense of cosmic scale on paper, and how do you explain the impossible clearly without pretending the cosmos is fully knowable? The project covers the identity, the editorial design and the packaging of the book.",
  approach="The core idea is growth. The book unfolds across three chapters, each physically larger than the last, mirroring the universe's own expansion from the familiar to the infinite. The reader literally holds more as the subject gets bigger. Every spread pairs imagery with clear explanation so the content stays understandable, while the design keeps reminding you that part of the subject will always stay out of reach. The identity and packaging follow the same logic, so the object feels like one continuous journey from cover to final page. All photography of the finished book was shot in a photo studio.",
  deliverables=["Editorial design: structure, typography and layout across three expanding chapters", "Visual identity for the title, carried through cover, spine and interior", "Packaging design that frames the three-part format as one object", "Studio photography of the finished book for presentation"],
  result="The finished book is both a study and an experience: a way to see the universe and to understand how little of it we can truly grasp. For me it is a reference piece for how physical format can carry an idea, not just contain it, something I bring into packaging and print work for clients."),
 "nl": dict(
  brief="Stellar Secrets is een boekontwerpproject over de ruimte, gemaakt om het universum binnen handbereik te laten voelen. De uitdaging was tegelijk redactioneel en fysiek: hoe geef je een lezer op papier een gevoel van kosmische schaal, en hoe leg je het onmogelijke helder uit zonder te doen alsof de kosmos volledig kenbaar is? Het project omvat de identiteit, het redactionele ontwerp en de verpakking van het boek.",
  approach="Het kernidee is groei. Het boek ontvouwt zich in drie hoofdstukken, elk fysiek groter dan het vorige, als spiegel van de uitdijing van het universum van het vertrouwde naar het oneindige. De lezer houdt letterlijk meer vast naarmate het onderwerp groter wordt. Elke spread combineert beeld met heldere uitleg zodat de inhoud begrijpelijk blijft, terwijl het ontwerp je eraan blijft herinneren dat een deel van het onderwerp altijd buiten bereik zal blijven. De identiteit en de verpakking volgen dezelfde logica, zodat het object aanvoelt als één doorlopende reis van cover tot laatste pagina. Alle foto's van het afgewerkte boek werden in een fotostudio gemaakt.",
  deliverables=["Redactioneel ontwerp: structuur, typografie en lay-out over drie groeiende hoofdstukken", "Visuele identiteit voor de titel, doorgetrokken op cover, rug en binnenwerk", "Verpakkingsontwerp dat het driedelige formaat als één object kadert", "Studiofotografie van het afgewerkte boek voor presentatie"],
  result="Het afgewerkte boek is tegelijk een studie en een ervaring: een manier om het universum te zien en te begrijpen hoe weinig we er echt van kunnen vatten. Voor mij is het een referentiestuk voor hoe een fysiek formaat een idee kan dragen in plaats van het enkel te bevatten, iets wat ik meeneem in verpakkings- en printwerk voor klanten."),
},
"tuillerien": {
 "genre": ["Branding", "Hospitality Branding", "Motion Design"],
 "keywords": "hotel branding, boutique hotel identity, luxury branding, motion design, Bruges",
 "en": dict(
  brief="Tuillerien is a five-star boutique hotel in the heart of Bruges, where heritage and modern luxury come together. The hotel was opening its next chapter and needed an identity to match: one that honoured the iconic laurel symbol guests already knew, while bringing the typography, motion and overall tone up to the standard of the experience inside. The scope was brand identity and motion design.",
  approach="The guiding principle was never loud, always precise. Luxury in a boutique hotel is not about adding more, it is about getting every small thing right, so the identity was built the same way. The laurel symbol stays at the centre of the brand as a continuity with the hotel's history, refined rather than replaced. Typography was chosen to feel elevated and considered, with generous spacing that lets the mark breathe. Motion design extends that calm: slow, deliberate movement that suits a place built for taking your time. The system was proven across stationery, signage and screen through high-quality photographic mockups.",
  deliverables=["Brand identity: refined laurel symbol, wordmark, typography and colour system", "Brand guidelines covering print, signage and digital use", "Motion design: animated logo and identity elements for screens and video", "Application mockups: stationery, in-room and signage pieces shown in context"],
  result="The identity communicates one thing in every element, from the typography to the motion: this is a place that takes care of the details. Tuillerien now has a brand system that feels timeless rather than trend-driven, built to stay relevant for the hotel's next chapter and the ones after it. It is also a useful reference for any hospitality client in Bruges, Ghent or Knokke wondering what a restrained rebrand can look like when the existing symbol is worth keeping."),
 "nl": dict(
  brief="Tuillerien is een vijfsterren boetiekhotel in het hart van Brugge, waar erfgoed en moderne luxe samenkomen. Het hotel begon aan zijn volgende hoofdstuk en had een identiteit nodig op dat niveau: één die het iconische lauriersymbool eerde dat gasten al kenden, en tegelijk de typografie, de motion en de algemene toon optilde tot de standaard van de ervaring binnen. De scope: merkidentiteit en motion design.",
  approach="Het leidende principe was nooit luid, altijd precies. Luxe in een boetiekhotel gaat niet over meer toevoegen, maar over elk klein ding juist krijgen, dus werd de identiteit op dezelfde manier gebouwd. Het lauriersymbool blijft de kern van het merk als continuïteit met de geschiedenis van het hotel, verfijnd in plaats van vervangen. De typografie werd gekozen om verheven en doordacht aan te voelen, met ruime spatiëring die het teken laat ademen. Motion design trekt die rust door: trage, bewuste beweging die past bij een plek gemaakt om de tijd te nemen. Het systeem werd bewezen op briefpapier, signage en scherm via fotografische mockups van hoge kwaliteit.",
  deliverables=["Merkidentiteit: verfijnd lauriersymbool, woordmerk, typografie en kleurensysteem", "Merkrichtlijnen voor print, signage en digitaal gebruik", "Motion design: geanimeerd logo en identiteitselementen voor schermen en video", "Toepassingsmockups: briefpapier, kamerdetails en signage in context getoond"],
  result="De identiteit zegt in elk element hetzelfde, van de typografie tot de motion: dit is een plek met oog voor detail. Tuillerien heeft nu een merksysteem dat tijdloos aanvoelt in plaats van trendgedreven, gebouwd om relevant te blijven voor het volgende hoofdstuk van het hotel en de hoofdstukken daarna. Het is ook een nuttige referentie voor elke horecaklant in Brugge, Gent of Knokke die zich afvraagt hoe een ingetogen rebranding eruit kan zien wanneer het bestaande symbool de moeite waard is om te behouden."),
},
"tuinen-arnaud": {
 "genre": ["Branding", "Web Design"],
 "keywords": "garden company branding, logo design, web design, visual identity, Sint-Martens-Latem",
 "en": dict(
  brief="Tuinen Arnaud is a professional garden company in Sint-Martens-Latem working on garden design, maintenance and terracing. The existing look no longer reflected the craftsmanship and quality of the work, so the brief was a new visual identity and a website that would make the business look as modern, clean and trustworthy as it is in practice, and that would hold up on a van, a business card and a phone screen alike.",
  approach="A garden company sells trust and precision, so the identity takes a deliberately minimalist route. A clear wordmark does most of the work. A subtle line beneath it symbolises structure and stability, and a simple tree icon references nature and garden architecture without turning into a cartoon. The deep green tone and generous white space create a calm, professional appearance that feels at home next to real plants and stone. The website follows the same logic: clear services, real project imagery and a direct way to get in touch, with nothing in between.",
  deliverables=["Brand identity: wordmark, line and tree icon, colour palette and typography", "Brand guidelines for vehicles, workwear, print and digital", "Web design: a clean, mobile-first website presenting the services and the work", "Application design shown across van, cards and site signage"],
  result="The result is a timeless brand that looks modern, radiates trust and matches the core values of Tuinen Arnaud: modern, clean, trustworthy and detail-oriented. The website is live, linked above, and the identity is now the first thing a potential client sees, before a single plant goes in the ground."),
 "nl": dict(
  brief="Tuinen Arnaud is een professionele tuinaannemer uit Sint-Martens-Latem, actief in tuinontwerp, onderhoud en terrasaanleg. De bestaande uitstraling weerspiegelde het vakmanschap en de kwaliteit van het werk niet meer, dus de briefing was een nieuwe visuele identiteit en een website die de zaak zo modern, strak en betrouwbaar laten ogen als ze in de praktijk is, en die even goed standhouden op een bestelwagen, een visitekaartje en een telefoonscherm.",
  approach="Een tuinaannemer verkoopt vertrouwen en precisie, dus kiest de identiteit bewust voor een minimalistische aanpak. Een helder woordmerk doet het meeste werk. Een subtiele lijn eronder symboliseert structuur en stabiliteit, en een eenvoudig boompictogram verwijst naar natuur en tuinarchitectuur zonder een cartoon te worden. De diepe groene tint en het ruime gebruik van witruimte zorgen voor een rustige, professionele uitstraling die thuishoort naast echte planten en steen. De website volgt dezelfde logica: duidelijke diensten, echte projectbeelden en een directe manier om contact op te nemen, zonder iets ertussen.",
  deliverables=["Merkidentiteit: woordmerk, lijn en boompictogram, kleurenpalet en typografie", "Merkrichtlijnen voor voertuigen, werkkledij, print en digitaal", "Webdesign: een strakke, mobile-first website die de diensten en het werk presenteert", "Toepassingsontwerp op bestelwagen, kaartjes en werfsignalisatie"],
  result="Het resultaat is een tijdloos merk dat modern oogt, vertrouwen uitstraalt en aansluit bij de kernwaarden van Tuinen Arnaud: modern, strak, betrouwbaar en oog voor detail. De website staat live, hierboven gelinkt, en de identiteit is nu het eerste wat een potentiële klant ziet, nog voor er één plant in de grond gaat."),
},
"walter-swennen": {
 "genre": ["Editorial Design", "Book Design"],
 "keywords": "art book design, editorial design, limited edition, Walter Swennen, print design, Ghent",
 "en": dict(
  brief="This limited-edition book is an editorial design project around the work of Belgian painter Walter Swennen, made for the social media generation, where scrolling, reacting and reinterpreting are part of daily life. Swennen never titles his works because he wants viewers to create their own meaning. The brief was to design a book that respects that refusal: no titles, no answers, just you and the work. The project covers the book's identity, editorial design and packaging.",
  approach="The concept mirrors the feeling of moving through social media: quick impressions, shifting opinions, filters, and moments that make you question what you are really seeing. Instead of explaining the paintings, the book keeps inviting you to think twice, through sequencing, cropping, repetition and shifts in scale that change how a work reads from one page to the next. The typography stays out of the way so the paintings do the talking. All images are works by Walter Swennen himself, which set the only real rule of the project: the design may frame the work, never compete with it.",
  deliverables=["Editorial concept and sequencing that turn reading into reinterpreting", "Book design: format, typography, layout system and cover", "Packaging for the limited edition", "Print-ready production files for the edition"],
  result="Instead of telling you what Swennen's work means, the book lets you experience it freely, shaping your own story with every page. It is the project I point to when a client asks what I mean by letting the content lead: the design is everywhere in the book and visible almost nowhere."),
 "nl": dict(
  brief="Dit boek in beperkte oplage is een redactioneel ontwerpproject rond het werk van de Belgische schilder Walter Swennen, gemaakt voor de social media-generatie, waar scrollen, reageren en herinterpreteren deel uitmaken van het dagelijks leven. Swennen geeft zijn werken nooit een titel omdat hij wil dat kijkers hun eigen betekenis maken. De briefing: een boek ontwerpen dat die weigering respecteert: geen titels, geen antwoorden, alleen jij en het werk. Het project omvat de identiteit, het redactionele ontwerp en de verpakking van het boek.",
  approach="Het concept spiegelt het gevoel van door social media bewegen: snelle indrukken, verschuivende meningen, filters en momenten waarop je je afvraagt wat je echt ziet. In plaats van de schilderijen uit te leggen, blijft het boek je uitnodigen om twee keer te kijken, via volgorde, kadrering, herhaling en schaalwissels die veranderen hoe een werk leest van de ene pagina naar de volgende. De typografie blijft op de achtergrond zodat de schilderijen spreken. Alle beelden zijn werken van Walter Swennen zelf, wat de enige echte regel van het project bepaalde: het ontwerp mag het werk kaderen, nooit ermee concurreren.",
  deliverables=["Redactioneel concept en volgorde die lezen omzetten in herinterpreteren", "Boekontwerp: formaat, typografie, lay-outsysteem en cover", "Verpakking voor de beperkte oplage", "Drukklare productiebestanden voor de editie"],
  result="In plaats van te vertellen wat het werk van Swennen betekent, laat het boek je het vrij ervaren en met elke pagina je eigen verhaal vormen. Het is het project waarnaar ik verwijs als een klant vraagt wat ik bedoel met de inhoud laten leiden: het ontwerp zit overal in het boek en is bijna nergens zichtbaar."),
},
}

def block(lang, d):
    h = H[lang]
    lis = "\n".join(f"        <li>{html.escape(x, quote=False)}</li>" for x in d["deliverables"])
    return (f'\n      <h3>{h[0]}</h3>\n      <p>{d["brief"]}</p>'
            f'\n      <h3>{h[1]}</h3>\n      <p>{d["approach"]}</p>'
            f'\n      <h3>{h[2]}</h3>\n      <ul class="cs-deliverables">\n{lis}\n      </ul>'
            f'\n      <h3>{h[3]}</h3>\n      <p>{d["result"]}</p>\n    ')

def update(path, slug, lang):
    s = open(path, encoding="utf-8").read()
    d = C[slug][lang]
    if 'class="cs-deliverables"' not in s:
        m = re.search(r'(<div class="cs-desc-text fade-up d1"><p>.*?</p>)(</div>)', s, re.S)
        assert m, path
        s = s[:m.end(1)] + block(lang, d) + s[m.end(1):]
    # JSON-LD enrichment
    def enrich(mm):
        obj = json.loads(mm.group(1))
        if obj.get("@type") != "CreativeWork": return mm.group(0)
        obj["description"] = d["brief"]
        obj["genre"] = C[slug]["genre"]
        obj["keywords"] = C[slug]["keywords"]
        obj["abstract"] = d["result"]
        if isinstance(obj.get("about"), list) and obj["about"] and isinstance(obj["about"][0], str):
            obj["about"] = [{"@type": "Thing", "name": g} for g in C[slug]["genre"]]
        return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>'
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', enrich, s, flags=re.S)
    open(path, "w", encoding="utf-8").write(s)

for slug in C:
    update(f"works/{slug}.html", slug, "en")
    update(f"nl/works/{slug}.html", slug, "nl")

# Melabody has no location: say so instead of a dash
for p, val in (("works/melabody.html", "Concept project"), ("nl/works/melabody.html", "Conceptproject")):
    s = open(p, encoding="utf-8").read().replace('<span class="cs-meta-val">-</span>', f'<span class="cs-meta-val">{val}</span>', 1)
    open(p, "w", encoding="utf-8").write(s)

# Tuillerien: meta says Knokke, body says Bruges. Flag it rather than guess.
for p in ("works/tuillerien.html", "nl/works/tuillerien.html"):
    s = open(p, encoding="utf-8").read()
    if "TODO: confirm location" not in s:
        s = s.replace('<div class="cs-meta fade-up d3">', '<!-- TODO: confirm location with Arnaud. Meta says Knokke, body copy says Bruges. -->\n  <div class="cs-meta fade-up d3">', 1)
        open(p, "w", encoding="utf-8").write(s)

# CSS for the new headings and list (once)
css = open("works.css", encoding="utf-8").read()
if ".cs-desc-text h3" not in css:
    css = css.replace(".cs-desc-text { font-size: 15px; line-height: 1.82; color: var(--gray); }",
        ".cs-desc-text { font-size: 15px; line-height: 1.82; color: var(--gray); }\n"
        ".cs-desc-text p + h3, .cs-desc-text ul + h3 { margin-top: 36px; }\n"
        ".cs-desc-text h3 { font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: var(--ink); margin-bottom: 12px; }\n"
        ".cs-deliverables { list-style: none; padding: 0; margin: 0; }\n"
        ".cs-deliverables li { position: relative; padding-left: 18px; margin-bottom: 8px; }\n"
        ".cs-deliverables li::before { content: '\\2014'; position: absolute; left: 0; color: #bbb; }", 1)
    open("works.css", "w", encoding="utf-8").write(css)

import glob
for p in sorted(glob.glob("works/*.html") + glob.glob("nl/works/*.html")):
    h = open(p, encoding="utf-8").read()
    m = re.search(r'<main>.*?<section class="cs-next"', h, re.S).group(0)
    t = re.sub(r"<[^>]+>", " ", m)
    print(f"{len(t.split()):4d} words  {p}")
