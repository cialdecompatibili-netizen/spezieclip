import io, json, os
# GUIDA-SVILUPPO: popola lo shop spezieclip (categorie + prodotti IT+EN), toglie gli esempi del template. Idempotente. Poi: python automation/allinea_hash.py en
C = [
("spezie","Spezie","🌶️","Spices","spices"),
("erbe-aromatiche","Erbe aromatiche","🌿","Herbs","herbs"),
("pepi-peperoncini","Pepe e peperoncino","🌶️","Pepper and chilli","peppers-and-chillies"),
("miscele-insaporitori","Miscele e insaporitori","🧂","Blends and seasonings","blends-and-seasonings"),
]
# id, nome IT, nome EN, categoria, centesimi, icona, uso IT, uso EN
P = [
("aglio-granulare","Aglio granulare","Granulated garlic","spezie",249,"🧄","Per sughi, arrosti e verdure.","For sauces, roasts and vegetables."),
("cannella-bastoncini","Cannella in bastoncini","Cinnamon sticks","spezie",299,"🪵","Per dolci, vin brulé e infusi.","For desserts, mulled wine and infusions."),
("cannella-macinata","Cannella macinata","Ground cinnamon","spezie",249,"🪵","Per dolci, creme e colazioni.","For desserts, creams and breakfasts."),
("curcuma-macinata","Curcuma macinata","Ground turmeric","spezie",279,"🟡","Per risotti, zuppe e golden milk.","For risottos, soups and golden milk."),
("zenzero-macinato","Zenzero macinato","Ground ginger","spezie",279,"🫚","Per biscotti, infusi e piatti orientali.","For biscuits, infusions and Asian dishes."),
("noce-moscata","Noce moscata macinata","Ground nutmeg","spezie",299,"🌰","Per besciamella, ripieni e dolci.","For béchamel, fillings and desserts."),
("cumino-macinato","Cumino macinato","Ground cumin","spezie",249,"🌾","Per legumi, carni e piatti speziati.","For legumes, meats and spiced dishes."),
("coriandolo-macinato","Coriandolo macinato","Ground coriander","spezie",249,"🌾","Per curry, marinate e pane.","For curries, marinades and bread."),
("paprika-dolce","Paprika dolce","Sweet paprika","spezie",249,"🫑","Per carni, patate e uova.","For meats, potatoes and eggs."),
("paprika-affumicata","Paprika affumicata","Smoked paprika","spezie",299,"🫑","Per arrosti, barbecue e salse.","For roasts, barbecue and sauces."),
("semi-di-sesamo","Semi di sesamo","Sesame seeds","spezie",249,"⚪","Per pane, insalate e piatti asiatici. Contiene sesamo.","For bread, salads and Asian dishes. Contains sesame."),
("origano","Origano","Oregano","erbe-aromatiche",199,"🌿","Per pizza, pomodoro e pesce.","For pizza, tomato and fish."),
("basilico","Basilico","Basil","erbe-aromatiche",199,"🌿","Per sughi, insalate e piatti estivi.","For sauces, salads and summer dishes."),
("rosmarino","Rosmarino tagliato","Cut rosemary","erbe-aromatiche",199,"🌿","Per arrosti, patate e focacce.","For roasts, potatoes and focaccia."),
("timo","Timo","Thyme","erbe-aromatiche",199,"🌿","Per carni, funghi e salse.","For meats, mushrooms and sauces."),
("salvia","Salvia","Sage","erbe-aromatiche",199,"🌿","Per burro e salvia, arrosti e ripieni.","For sage butter, roasts and fillings."),
("prezzemolo","Prezzemolo","Parsley","erbe-aromatiche",199,"🌿","Per pesce, sughi e insalate.","For fish, sauces and salads."),
("menta-piperita","Menta piperita","Peppermint","erbe-aromatiche",199,"🌿","Per dolci, insalate e infusi.","For desserts, salads and infusions."),
("pepe-nero-grani","Pepe nero in grani","Black peppercorns","pepi-peperoncini",299,"⚫","Da macinare al momento su qualsiasi piatto.","To grind fresh over any dish."),
("pepe-nero-macinato","Pepe nero macinato","Ground black pepper","pepi-peperoncini",279,"⚫","Per carni, sughi e uova.","For meats, sauces and eggs."),
("pepe-bianco-grani","Pepe bianco in grani","White peppercorns","pepi-peperoncini",349,"⚪","Per salse chiare, pesce e purè.","For light sauces, fish and mashed potatoes."),
("peperoncino-cayenna","Peperoncino di Cayenna macinato","Ground cayenne pepper","pepi-peperoncini",279,"🌶️","Per chi ama il piccante: attenzione alle dosi.","For those who like heat: mind the quantity."),
("peperoncino-jalapeno","Peperoncino jalapeño in fiocchi","Jalapeño chilli flakes","pepi-peperoncini",299,"🌶️","Per pizza, tacos e salse.","For pizza, tacos and sauces."),
("miscela-pizza","Erbe e spezie per pizza","Herbs and spices for pizza","miscele-insaporitori",249,"🍕","Da spargere sulla pizza prima o dopo la cottura.","Sprinkle on pizza before or after baking."),
("garam-masala","Garam masala","Garam masala","miscele-insaporitori",349,"🍛","Per curry, legumi e riso.","For curries, legumes and rice."),
("curry-polvere","Curry in polvere","Curry powder","miscele-insaporitori",299,"🍛","Per pollo, riso e verdure.","For chicken, rice and vegetables."),
("condimento-aglio-olio","Condimento aglio, olio e peperoncino","Garlic, oil and chilli seasoning","miscele-insaporitori",249,"🍝","Per la pasta e per condire verdure.","For pasta and for seasoning vegetables."),
("condimento-bistecche","Condimento per bistecche","Steak seasoning","miscele-insaporitori",299,"🥩","Per carne alla griglia e in padella.","For grilled and pan-fried meat."),
]
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
for f in ['_negozio/categoria-esempio.md','_negozio/prodotto-esempio.md','en/negozio/prodotto-esempio.md','en/negozio/categoria/esempio.md']:
    if os.path.exists(f): os.remove(f)
d = json.load(io.open('_data/catalogo.json', encoding='utf-8'))
d['categorie'] = []; d['prodotti'] = []
for c in C:
    d['categorie'].append({"nome": c[1], "id": c[0], "icona": c[2], "tr": {"en": {"nome": c[3]}}})
    wr('_negozio/categoria-%s.md' % c[0], '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /negozio/categoria/%s/\ndescription: "%s"\nref: shop-cat-%s\n---\n' % (c[1], c[0], c[0], c[1], c[0]))
    wr('en/negozio/categoria/%s.md' % c[0], '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /en/shop/category/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-cat-%s\ntr: tradotto\n---\n' % (c[3], c[0], c[4], c[3], c[0]))
for p in P:
    i, ni, ne, cat, pr, ic, ui, ue = p
    li = "%s nel pratico sacchetto richiudibile con clip salva freschezza: dopo l'apertura richiudi la clip e aromi e profumi si mantengono più a lungo.\n\n## Come usarlo\n\n%s\n\n## Conservazione\n\nTieni il sacchetto chiuso con la clip, al riparo da luce, calore e umidità. Ingredienti e allergeni sono indicati sull'etichetta della confezione." % (ni, ui)
    le = "%s in a handy resealable pouch with a freshness clip: after opening, close the clip and aroma and flavor last longer.\n\n## How to use\n\n%s\n\n## Storage\n\nKeep the pouch closed with the clip, away from light, heat and moisture. Ingredients and allergens are shown on the pack label." % (ne, ue)
    d['prodotti'].append({"tipo":"fisico","id":i,"nome":ni,"categoria":cat,"prezzo_centesimi":pr,"descrizione":"%s Sacchetto richiudibile con clip." % ui,"descrizione_completa":li,"immagine":"","icona":ic,"visibile":True,
      "tr":{"en":{"nome":ne,"descrizione":"%s Resealable pouch with clip." % ue,"descrizione_completa":le}}})
    wr('_negozio/%s.md' % i, '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /negozio/%s/\ndescription: "%s"\nref: shop-prod-%s\n---\n' % (ni, i, i, ui, i))
    wr('en/negozio/%s.md' % i, '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /en/shop/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-prod-%s\ntr: tradotto\n---\n' % (ne, i, i, ue, i))
io.open('_data/catalogo.json', 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2))
print('ok', len(d['categorie']), 'cat', len(d['prodotti']), 'prod')
