import io, json, os, re, glob
# GUIDA-SVILUPPO: contenuti di spezieclip (home, chi siamo, articoli IT+EN), toglie Servizi e gli esempi del template.
# Uso dalla radice:  python automation/contenuti_spezie.py   poi  python automation/permalink_articoli.py --apply  e  python automation/allinea_hash.py en
def rd(p): return json.load(io.open(p, encoding='utf-8'))
def wj(p, d): io.open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2))
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
def card(title, items=None, text=None, n=None):
    s = '<div class="gc-pl%s">' % (' ent-pl' if items else '')
    if n: s += '<span class="n">%s</span>' % n
    s += '<b>%s</b>' % title
    if items: s += '<ul>' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
    if text: s += '<p>%s</p>' % text
    return s + '</div>'
# LINEE home: pannelli in vetro (classe .lin in assets/css/gaming.css) con spotlight che segue il mouse. Niente numeri: non e' una sequenza.
LIN_JS = '<script>(function(){if(!window.matchMedia||!matchMedia("(hover:hover)").matches)return;document.querySelectorAll(".lin-card").forEach(function(c){c.addEventListener("pointermove",function(e){var r=c.getBoundingClientRect();c.style.setProperty("--mx",e.clientX-r.left+"px");c.style.setProperty("--my",e.clientY-r.top+"px")})})})();</script>'
def lin_card(i, title, items):
    return '<article class="lin-card lin-c%d"><i class="lin-dot" aria-hidden="true"></i><h3>%s</h3><ul>%s</ul></article>' % (i + 1, title, ''.join('<li>%s</li>' % x for x in items))
def home(L):
    t = L
    hero = ('<div class="gc"><section class="ent-hero"><div class="gc-wrap gc-hero-in"><div><p class="gc-eyebrow">%s</p><h1 class="gc-h1">%s</h1><p class="gc-lead">%s</p>'
      '<div class="gc-act"><a class="gc-btn gc-btn-a" href="__BASEURL__%s">%s</a><a class="gc-btn gc-btn-o" href="#linee">%s</a></div></div><div class="ent-cycle">%s</div></div></section></div>'
      % (t['eb'], t['h1'], t['lead'], t['shop'], t['b1'], t['b2'], ''.join('<div><b>%s</b><span>%s</span></div>' % x for x in t['cyc'])))
    linee = ('<div class="gc"><section class="gc-sec lin" id="linee"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><div class="lin-grid">%s</div>'
      '<p class="lin-all"><a class="gc-link" href="__BASEURL__%s">%s</a></p></div></section></div>'
      % (t['l_eb'], t['l_h2'], ''.join(lin_card(i, a, b) for i, (a, b) in enumerate(t['linee'])), t['shop'], t['l_all'])) + LIN_JS
    perchi = ('<div class="gc"><section class="gc-sec" id="perchi"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><div class="gc-plat ent-4">%s</div></div></section></div>'
      % (t['p_eb'], t['p_h2'], ''.join(card(a, items=b) for a, b in t['perchi'])))
    metodo = ('<div class="gc"><section class="gc-sec gc-soft" id="metodo"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><div class="gc-plat ent-4">%s</div></div></section></div>'
      % (t['m_eb'], t['m_h2'], ''.join(card(a, text=b, n='0%d' % (i + 1)) for i, (a, b) in enumerate(t['metodo']))))
    avvisi = ('<div class="gc"><section class="gc-sec" id="avvisi"><div class="gc-wrap gc-2c"><div><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><a class="gc-btn gc-btn-k" href="__BASEURL__%s">%s</a></div>%s</div></section></div>'
      % (t['a_eb'], t['a_h2'], t['a_lead'], t['blog'], t['a_btn'], card(t['a_t'], text=t['a_p'], n=t['a_n'])))
    cont = ('<div class="gc"><section class="gc-sec gc-dark" id="contatti"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><a class="gc-btn" href="__BASEURL__%s">%s</a></div></section></div>'
      % (t['c_eb'], t['c_h2'], t['c_lead'], t['contatti'], t['c_btn']))
    return {'hero': hero, 'servizi': linee, 'perchi': perchi, 'metodo': metodo, 'avvisi': avvisi, 'contatti': cont}
IT = dict(eb='Spezie ed erbe in sacchetti richiudibili', h1='Il sapore giusto, <em>sempre a portata di mano.</em>',
  lead='Spezie, erbe aromatiche e miscele per la cucina di ogni giorno, in pratici sacchetti con clip: apri, usi la quantità che serve, richiudi. Cominci da 5 g a 0,99 €.',
  shop='/negozio/', b1='Vai al negozio', b2='Scopri le linee',
  cyc=[('Sacchetto richiudibile','La clip chiude bene dopo ogni uso'),('Da 5 g a 0,99 €','Assaggia una spezie nuova, poi scegli 10, 25 o 50 g'),('Tante varietà','Spezie, erbe, pepe, peperoncino e miscele'),('Etichetta chiara','Ingredienti e allergeni sempre indicati')],
  l_eb='Il catalogo', l_h2='Le nostre linee', l_all='Vedi tutto il negozio',
  linee=[('Spezie',['Cannella, curcuma, zenzero','Paprika dolce e affumicata','Cumino, coriandolo, noce moscata']),('Erbe aromatiche',['Origano, basilico, rosmarino','Timo, salvia, prezzemolo','Menta piperita']),('Pepe e peperoncino',['Pepe nero e bianco','Peperoncino di Cayenna','Jalapeño in fiocchi']),('Miscele e insaporitori',['Erbe e spezie per pizza','Garam masala e curry','Condimenti per carne e pasta'])],
  p_eb='Per chi è', p_h2='Chi si trova bene con noi',
  perchi=[('Cucina di casa',['Spezie di base sempre pronte','Scegli 5, 10, 25 o 50 g: compri quanto ti serve']),('Chi ama sperimentare',['Prova una spezie con soli 5 g','Spezie intere da macinare al momento']),('Chi cucina per tanti',['Erbe per pizza, carne e sughi','Scorta di pepe e paprika']),('Idee regalo',['Assortimento di sacchetti','Pratico da conservare in dispensa'])],
  m_eb='Come funziona', m_h2='Il sacchetto con la clip',
  metodo=[('Apri','Strappa o taglia il sacchetto nel punto indicato.'),('Usa','Prendi la quantità che ti serve con un cucchiaino asciutto.'),('Chiudi','Richiudi con la clip dopo ogni uso.'),('Conserva','Tienilo in dispensa, lontano da luce, calore e umidità.')],
  a_eb='Dal blog', a_h2='Idee e consigli', a_lead='Guide brevi su spezie, erbe e conservazione, scritte in modo semplice.', blog='/blog/', a_btn='Vai al blog',
  a_t='Come conservare spezie ed erbe aromatiche', a_p='Pochi accorgimenti per mantenere profumo e sapore più a lungo.', a_n='ULTIMO ARTICOLO',
  c_eb='Contatti', c_h2='Scriviamoci', c_lead='Domande su un prodotto o su un ordine? Scrivici, ti rispondiamo appena possibile.', contatti='/contatti/', c_btn='Scrivici')
EN = dict(eb='Spices and herbs in resealable pouches', h1='The right flavor, <em>always within reach.</em>',
  lead='Spices, herbs and blends for everyday cooking, in handy pouches with a clip: open, use what you need, close. Start from 5 g at €0.99.',
  shop='/en/shop/', b1='Go to the shop', b2='Discover our ranges',
  cyc=[('Resealable pouch','The clip closes well after every use'),('From 5 g at €0.99','Try a new spice, then pick 10, 25 or 50 g'),('Many varieties','Spices, herbs, pepper, chilli and blends'),('Clear label','Ingredients and allergens always shown')],
  l_eb='The catalog', l_h2='Our ranges', l_all='See the whole shop',
  linee=[('Spices',['Cinnamon, turmeric, ginger','Sweet and smoked paprika','Cumin, coriander, nutmeg']),('Herbs',['Oregano, basil, rosemary','Thyme, sage, parsley','Peppermint']),('Pepper and chilli',['Black and white pepper','Cayenne pepper','Jalapeño flakes']),('Blends and seasonings',['Herbs and spices for pizza','Garam masala and curry','Seasonings for meat and pasta'])],
  p_eb='Who it is for', p_h2='Who gets on well with us',
  perchi=[('Home cooking',['Basic spices always ready','Pick 5, 10, 25 or 50 g: buy what you need']),('Adventurous cooks',['Try a spice with just 5 g','Whole spices to grind fresh']),('Cooking for many',['Herbs for pizza, meat and sauces','Stock of pepper and paprika']),('Gift ideas',['Assortment of pouches','Handy to keep in the pantry'])],
  m_eb='How it works', m_h2='The pouch with a clip',
  metodo=[('Open','Tear or cut the pouch at the marked point.'),('Use','Take what you need with a dry spoon.'),('Close','Close with the clip after every use.'),('Store','Keep in the pantry, away from light, heat and moisture.')],
  a_eb='From the blog', a_h2='Ideas and tips', a_lead='Short guides on spices, herbs and storage, written simply.', blog='/en/blog/', a_btn='Go to the blog',
  a_t='How to store spices and dried herbs', a_p='A few tips to keep aroma and flavor for longer.', a_n='LATEST ARTICLE',
  c_eb='Contact', c_h2='Get in touch', c_lead='Questions about a product or an order? Write to us, we will reply as soon as possible.', contatti='/en/contact/', c_btn='Write to us')
for path, L in (('_data/blocks_home.json', IT), ('_data/i18n/en/blocks_home.json', EN)):
    d = rd(path); new = home(L)
    for b in d:
        if b['id'] == 'contesto': b['enabled'] = False
        if b['id'] in new: b['html'] = new[b['id']]
        if b['id'] == 'servizi': b['nome'] = 'Le linee' if L is IT else 'Ranges'
    wj(path, d)
def az(p, h2, lead, par, pr):
    d = rd(p)
    for b in d:
        if b['id'] == 'chi': b['html'] = '<div class="gc"><section class="gc-sec" id="chi"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><p>%s</p></div></section></div>' % (pr[0], h2, lead, par)
        if b['id'] == 'principi': b['html'] = '<div class="gc"><section class="gc-sec gc-soft" id="principi"><div class="gc-wrap"><h2 class="gc-h2">%s</h2><div class="gc-plat">%s</div></div></section></div>' % (pr[1], ''.join(card(a, text=t, n=str(i + 1)) for i, (a, t) in enumerate(pr[2])))
    wj(p, d)
az('_data/blocks_azienda.json', 'Spezie in formato pratico', 'Spezie Clip propone spezie, erbe aromatiche e miscele in sacchetti richiudibili con clip, pensati per la cucina di ogni giorno.', 'Ogni prodotto si sceglie in più pesi, da 5 g a 0,99 € fino a 50 g, così provi senza comprare di più del necessario. Sull\'etichetta trovi gli ingredienti e gli allergeni. Se hai un dubbio su un prodotto o su un ordine, scrivici.',
   ('Chi siamo', 'Come ci comportiamo', [('Chiarezza', 'Ingredienti e allergeni scritti sull\'etichetta, senza promesse che non possiamo verificare.'), ('Praticità', 'Sacchetti richiudibili e pesi da 5 a 50 g: prendi la dose giusta per la tua cucina.'), ('Assistenza', 'Ci scrivi, ti rispondiamo: prima e dopo l\'acquisto.')]))
az('_data/i18n/en/blocks_azienda.json', 'Spices in a handy format', 'Spezie Clip offers spices, herbs and blends in resealable pouches with a clip, made for everyday cooking.', 'Every product comes in several weights, from 5 g at €0.99 up to 50 g, so you can try without buying more than you need. The label lists ingredients and allergens. If you have a question about a product or an order, write to us.',
   ('About us', 'How we behave', [('Clarity', 'Ingredients and allergens written on the label, with no promises we cannot verify.'), ('Practicality', 'Resealable pouches and weights from 5 to 50 g: take the right amount for your kitchen.'), ('Support', 'You write, we reply: before and after your purchase.')]))
# menu: tolta la voce Servizi, tolte le pagine Servizi, esempi e redirect di prova
for p, pat in (('_data/navigation.yml', r'  - title: "Servizi"\r?\n    url: /servizi/\r?\n'), ('_data/i18n/en/navigation.yml', r'  - title: "Services"\r?\n    url: /en/services/\r?\n')):
    s = io.open(p, encoding='utf-8').read(); io.open(p, 'w', encoding='utf-8', newline='').write(re.sub(pat, '', s))
for f in ['_pages/servizi.md', 'en/servizi.md'] + glob.glob('redirect/*.html') + glob.glob('_posts/*.md') + glob.glob('en/_posts/*.md'):
    if os.path.exists(f): os.remove(f)
def post(path, ref, title, date, exc, cat, body, en=False):
    wr(path, '---\nlayout: single\nref: %s\ntitle: "%s"\ndate: %s\nexcerpt: "%s"\ncategories:\n  - %s\n%s---\n\n%s\n' % (ref, title, date, exc, cat, 'tr: tradotto\n' if en else '', body))
A1 = ("Le spezie e le erbe aromatiche perdono profumo soprattutto per tre motivi: luce, calore e umidità. Pochi accorgimenti fanno la differenza.\n\n## Chiudi bene dopo ogni uso\n\nCon il sacchetto con clip basta richiudere subito: l'aria e l'umidità della cucina restano fuori.\n\n## Lontano dai fornelli\n\nIl calore e il vapore sono i nemici peggiori. Meglio una dispensa o un cassetto, non il ripiano sopra la cucina.\n\n## Cucchiaino sempre asciutto\n\nNon dosare mai la spezia direttamente sopra una pentola che bolle: il vapore entra nel sacchetto. Usa un cucchiaino asciutto.\n\n## Intere o macinate\n\nLe spezie intere, come pepe in grani e noce moscata, mantengono il profumo più a lungo di quelle macinate: macinale al momento.\n\n## Quando cambiarle\n\nAnnota la data di apertura. Se aprendo il sacchetto senti poco profumo, è il momento di sostituire la spezia.")
A2 = ("Non servono cento barattoli: con dieci spezie ed erbe si cucina quasi tutto.\n\n- **Origano**: pizza, pomodoro, pesce.\n- **Basilico**: sughi e insalate.\n- **Rosmarino**: arrosti e patate.\n- **Pepe nero**: quasi ovunque, meglio macinato al momento.\n- **Paprika dolce**: carni, uova e patate.\n- **Cannella**: dolci, creme e colazioni.\n- **Curcuma**: risotti, zuppe e golden milk.\n- **Cumino**: legumi e piatti speziati.\n- **Noce moscata**: besciamella e ripieni.\n- **Peperoncino**: per chi ama il piccante, da dosare con cautela.\n\nCon questo assortimento hai già una base completa, e puoi cominciare con 5 g a 0,99 € per ognuna. Le miscele, come curry e garam masala, si aggiungono dopo, quando vuoi provare cucine nuove.")
A3 = ("È online Spezie Clip: un negozio di spezie, erbe aromatiche e miscele in sacchetti richiudibili con clip.\n\n## Cosa trovi\n\nQuattro linee: spezie, erbe aromatiche, pepe e peperoncino, miscele e insaporitori. Ogni prodotto si compra da 5 g a 0,99 €, oppure da 10, 25 o 50 g. Su ogni scheda trovi come usarlo e come conservarlo.\n\n## Cosa arriverà\n\nSul blog pubblichiamo guide su conservazione e uso delle spezie. Se hai una richiesta, scrivici dalla pagina Contatti.")
B1 = ("Spices and dried herbs lose aroma mainly because of light, heat and moisture. A few habits make the difference.\n\n## Close well after every use\n\nWith the pouch with a clip, just close it right away: air and kitchen humidity stay out.\n\n## Away from the stove\n\nHeat and steam are the worst enemies. A pantry or drawer is better than the shelf above the cooker.\n\n## Always a dry spoon\n\nNever measure spice directly over a boiling pot: steam gets into the pouch. Use a dry spoon.\n\n## Whole or ground\n\nWhole spices, such as peppercorns and nutmeg, keep their aroma longer than ground ones: grind them fresh.\n\n## When to replace them\n\nNote the opening date. If you smell little when opening the pouch, it is time to replace the spice.")
B2 = ("You do not need a hundred jars: ten spices and herbs cover almost any cooking.\n\n- **Oregano**: pizza, tomato, fish.\n- **Basil**: sauces and salads.\n- **Rosemary**: roasts and potatoes.\n- **Black pepper**: almost everywhere, best ground fresh.\n- **Sweet paprika**: meats, eggs and potatoes.\n- **Cinnamon**: desserts, creams and breakfasts.\n- **Turmeric**: risottos, soups and golden milk.\n- **Cumin**: legumes and spiced dishes.\n- **Nutmeg**: béchamel and fillings.\n- **Chilli**: for those who like heat, to be used with care.\n\nWith this selection you already have a complete base, and you can start with 5 g at €0.99 for each. Blends such as curry and garam masala come later, when you want to try new cuisines.")
B3 = ("Spezie Clip is online: a shop for spices, herbs and blends in resealable pouches with a clip.\n\n## What you will find\n\nFour ranges: spices, herbs, pepper and chilli, blends and seasonings. Every product is available from 5 g at €0.99, or in 10, 25 or 50 g. Each page explains how to use and store it.\n\n## What is coming\n\nOn the blog we publish guides on storing and using spices. If you have a request, write to us from the Contact page.")
post('_posts/2026-11-01-come-conservare-spezie-ed-erbe.md', 'conservare-spezie', 'Come conservare spezie ed erbe aromatiche', '2026-11-01', 'Pochi accorgimenti per mantenere profumo e sapore più a lungo.', 'Guide', A1)
post('_posts/2026-11-01-dieci-spezie-per-iniziare.md', 'dieci-spezie', 'Dieci spezie ed erbe per iniziare', '2026-11-01', 'Una base completa per cucinare quasi tutto, senza riempire la dispensa.', 'Guide', A2)
A4 = ("Prima di comprare un barattolo intero di una spezie che non conosci, c'è un modo più semplice: provarne un po'.\n\n## Perché cominciare con 5 g\n\nCinque grammi bastano per qualche ricetta e costano 0,99 €. Se la spezie ti piace, la volta dopo scegli 10, 25 o 50 g.\n\n## Come scegliere il peso\n\n- **5 g**: per provare una spezie nuova.\n- **10 g**: per un uso occasionale.\n- **25 g**: per le spezie che usi ogni settimana.\n- **50 g**: per quelle di base, come pepe, paprika e origano.\n\n## Dopo l'apertura\n\nRichiudi sempre il sacchetto con la clip: la spezie dura di più e profuma meglio.")
B4 = ("Before buying a big jar of a spice you do not know, there is a simpler way: try a little.\n\n## Why start with 5 g\n\nFive grams are enough for a few recipes and cost €0.99. If you like the spice, next time choose 10, 25 or 50 g.\n\n## How to choose the weight\n\n- **5 g**: to try a new spice.\n- **10 g**: for occasional use.\n- **25 g**: for spices you use every week.\n- **50 g**: for basics, such as pepper, paprika and oregano.\n\n## After opening\n\nAlways close the pouch with the clip: the spice lasts longer and smells better.")
post('_posts/2026-11-01-prova-una-spezia-con-5-grammi.md', 'prova-5-grammi', 'Prova una spezia con soli 5 grammi', '2026-11-01', 'Come scegliere il peso giusto: da 5 g a 0,99 € fino a 50 g.', 'Guide', A4)
post('en/_posts/2026-11-01-try-a-spice-with-5-grams.md', 'prova-5-grammi', 'Try a spice with just 5 grams', '2026-11-01', 'How to choose the right weight: from 5 g at €0.99 up to 50 g.', 'Guides', B4, True)
post('_posts/2026-11-01-nasce-spezie-clip.md', 'nasce-spezie-clip', 'Nasce Spezie Clip', '2026-11-01', 'Il nuovo negozio di spezie in sacchetti richiudibili con clip.', 'Novità', A3)
post('en/_posts/2026-11-01-how-to-store-spices-and-herbs.md', 'conservare-spezie', 'How to store spices and dried herbs', '2026-11-01', 'A few tips to keep aroma and flavor for longer.', 'Guides', B1, True)
post('en/_posts/2026-11-01-ten-spices-to-start-with.md', 'dieci-spezie', 'Ten spices and herbs to start with', '2026-11-01', 'A complete base to cook almost anything, without filling the pantry.', 'Guides', B2, True)
post('en/_posts/2026-11-01-spezie-clip-is-born.md', 'nasce-spezie-clip', 'Spezie Clip is born', '2026-11-01', 'The new spice shop with resealable pouches with a clip.', 'News', B3, True)
print('ok')
