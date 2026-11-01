# -*- coding: utf-8 -*-
"""
GUIDA-SVILUPPO: SEO erbe aromatiche. Nome e URL con "essiccato" (es. /negozio/basilico-essiccato/, Title "Basilico essiccato").
Idempotente. Uso dalla radice:  python automation/seo_erbe.py   poi  python automation/allinea_hash.py en  e push.
PUNTI CRITICI:
- L'id prodotto NON cambia (basilico): e' usato da carrello, immagini, foto_prompt. Cambiano solo nome (catalogo.json), titolo e permalink
  delle pagine _negozio/<id>.md e en/negozio/<id>.md. Gli URL nel sito escono dal campo ref (shop-prod-<id>), quindi si aggiornano da soli.
- Il vecchio URL resta valido con una pagina in redirect/ (layout redirect), cosi' non diventa un 404.
- Se rilanci popola_spezie.py i nomi tornano quelli vecchi: rilancia anche questo script.
- La meta description della scheda = testo breve del catalogo (il campo description del front matter).
"""
import io, json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(R, *a)
def leggi(p):
    with io.open(p, encoding='utf-8', newline='') as f: return f.read()
def scrivi(p, t):
    with io.open(p, 'w', encoding='utf-8', newline='') as f: f.write(t)

# id: (nome IT, slug IT, nome EN, slug EN)
ERBE = {
 'origano':        ('Origano essiccato', 'origano-essiccato', 'Dried oregano', 'dried-oregano'),
 'basilico':       ('Basilico essiccato', 'basilico-essiccato', 'Dried basil', 'dried-basil'),
 'rosmarino':      ('Rosmarino essiccato', 'rosmarino-essiccato', 'Dried rosemary', 'dried-rosemary'),
 'timo':           ('Timo essiccato', 'timo-essiccato', 'Dried thyme', 'dried-thyme'),
 'salvia':         ('Salvia essiccata', 'salvia-essiccata', 'Dried sage', 'dried-sage'),
 'prezzemolo':     ('Prezzemolo essiccato', 'prezzemolo-essiccato', 'Dried parsley', 'dried-parsley'),
 'menta-piperita': ('Menta piperita essiccata', 'menta-piperita-essiccata', 'Dried peppermint', 'dried-peppermint'),
}
cp = P('_data', 'catalogo.json')
d = json.loads(leggi(cp))
byid = {p['id']: p for p in d['prodotti']}

def q(s): return s.replace('\\', '\\\\').replace('"', '\\"')
def front(testo, campo, valore):
    return re.sub(r'(?m)^%s: .*$' % campo, lambda m: '%s: %s' % (campo, valore), testo, count=1)

for i, (ni, si, ne, se) in ERBE.items():
    p = byid[i]
    p['nome'] = ni
    p.setdefault('tr', {}).setdefault('en', {})['nome'] = ne
    # pagina IT
    f = P('_negozio', i + '.md'); t = leggi(f)
    vecchio = re.search(r'(?m)^permalink: (\S+)$', t).group(1)
    nuovo = '/negozio/%s/' % si
    t = front(t, 'title', '"%s"' % q(ni)); t = front(t, 'permalink', nuovo); t = front(t, 'description', '"%s"' % q(p['descrizione']))
    scrivi(f, t)
    if vecchio != nuovo:
        scrivi(P('redirect', 'negozio-%s.html' % i), '---\nlayout: redirect\npermalink: "%s"\nredirect_to: "%s"\nsitemap: false\nnoindex: true\n---\n' % (vecchio, nuovo))
    # pagina EN
    f = P('en', 'negozio', i + '.md'); t = leggi(f)
    vecchio = re.search(r'(?m)^permalink: (\S+)$', t).group(1)
    nuovo = '/en/shop/%s/' % se
    t = front(t, 'title', '"%s"' % q(ne)); t = front(t, 'permalink', nuovo); t = front(t, 'description', '"%s"' % q(p['tr']['en']['descrizione']))
    scrivi(f, t)
    if vecchio != nuovo:
        scrivi(P('redirect', 'en-negozio-%s.html' % i), '---\nlayout: redirect\npermalink: "%s"\nredirect_to: "%s"\nsitemap: false\nnoindex: true\n---\n' % (vecchio, nuovo))
scrivi(cp, json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('ok erbe:', ', '.join(ERBE))
