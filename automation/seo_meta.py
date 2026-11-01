#!/usr/bin/env python3
"""Meta description (SEO) di prodotti, categorie e pagine, IT+EN. Idempotente.
Prodotti: "<Titolo>: <frase breve>. Sacchetto richiudibile con clip, da 5 g." (max 158 caratteri).
Se rilanci popola_spezie.py / seo_erbe.py le description tornano quelle vecchie: rilancia questo script.
USO: python automation/seo_meta.py            (dry-run)
     python automation/seo_meta.py --apply"""
import re, sys, glob, io, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
APPLY = '--apply' in sys.argv
SUF = {'it': ' Sacchetto richiudibile con clip, da 5 g.', 'en': ' Resealable clip bag, from 5 g.'}
MAXL = 158

PAGES = {
 '_pages/azienda.md': 'Chi siamo: spezie, erbe aromatiche e miscele in sacchetti richiudibili con clip, da 5 a 50 g. Scopri come lavoriamo.',
 '_pages/blog.md': 'Guide e consigli su spezie ed erbe aromatiche: come usarle, conservarle e scegliere i pesi giusti per la tua cucina.',
 '_pages/contatti.md': 'Contattaci per ordini, informazioni sui prodotti e collaborazioni. Rispondiamo il prima possibile.',
 '_pages/cat-guide.md': 'Guide pratiche su spezie ed erbe aromatiche: usi in cucina, abbinamenti e consigli di conservazione.',
 '_pages/cat-novita.md': 'Novità dal negozio: nuove spezie, nuove miscele e aggiornamenti del sito.',
 '_pages/carrello.md': 'Il tuo carrello: controlla spezie ed erbe aromatiche scelte, pesi e totale prima di ordinare.',
 '_pages/ordine.md': 'Completa il tuo ordine di spezie ed erbe aromatiche in sacchetti richiudibili con clip.',
 '_pages/grazie.md': 'Grazie per il tuo ordine di spezie ed erbe aromatiche. Ti scriviamo con i dettagli.',
 'en/azienda.md': 'About us: spices, herbs and blends in resealable clip bags, from 5 to 50 g. See how we work.',
 'en/blog.md': 'Guides and tips on spices and herbs: how to use and store them, and how to pick the right weight for your kitchen.',
 'en/contatti.md': 'Get in touch for orders, product questions and partnerships. We reply as soon as we can.',
 'en/category-guides.md': 'Practical guides on spices and herbs: kitchen uses, pairings and storage tips.',
 'en/category-news.md': 'Shop news: new spices, new blends and site updates.',
 'en/carrello.md': 'Your cart: check the spices and herbs you picked, weights and total before ordering.',
 'en/grazie.md': 'Thank you for your order of spices and herbs. We will email you the details.',
 '_negozio/categoria-spezie.md': 'Spezie in sacchetti richiudibili con clip, da 5 a 50 g: cannella, curcuma, cumino, paprika, noce moscata e altre.',
 '_negozio/categoria-erbe-aromatiche.md': 'Erbe aromatiche essiccate in sacchetti con clip, da 5 a 50 g: origano, basilico, rosmarino, timo, salvia e altre.',
 '_negozio/categoria-pepi-peperoncini.md': 'Pepi e peperoncini in sacchetti richiudibili con clip, da 5 a 50 g: pepe nero, pepe bianco, cayenna e jalapeño.',
 '_negozio/categoria-miscele-insaporitori.md': 'Miscele e insaporitori pronti in sacchetti con clip, da 5 a 50 g: curry, garam masala, condimenti per carne e pizza.',
 'en/negozio/categoria/spezie.md': 'Spices in resealable clip bags, from 5 to 50 g: cinnamon, turmeric, cumin, paprika, nutmeg and more.',
 'en/negozio/categoria/erbe-aromatiche.md': 'Dried herbs in clip bags, from 5 to 50 g: oregano, basil, rosemary, thyme, sage and more.',
 'en/negozio/categoria/pepi-peperoncini.md': 'Peppers and chillies in resealable clip bags, from 5 to 50 g: black pepper, white pepper, cayenne and jalapeño.',
 'en/negozio/categoria/miscele-insaporitori.md': 'Ready blends and seasonings in clip bags, from 5 to 50 g: curry, garam masala, steak and pizza seasonings.',
}

def rd(p): return io.open(p, encoding='utf-8', newline='').read()
def wr(p, t): io.open(p, 'w', encoding='utf-8', newline='').write(t)

def set_desc(t, d):
    d = d.replace('"', "'")
    line = 'description: "%s"' % d
    if re.search(r'^description:.*$', t, re.M):
        return re.sub(r'^description:.*$', lambda m: line, t, count=1, flags=re.M)
    return re.sub(r'^(title:.*)$', lambda m: m.group(1) + '\n' + line, t, count=1, flags=re.M)

def prodotto(t, lang):
    ti = re.search(r'^title:\s*"?(.*?)"?\s*$', t, re.M).group(1)
    old = re.search(r'^description:\s*"(.*)"\s*$', t, re.M)
    old = old.group(1) if old else ''
    if SUF[lang].strip() in old: return None
    s = old.split('. ')[0].strip().rstrip('.') if len(old) > 70 else old.strip().rstrip('.')
    s = s.replace(': ', ', ')
    if s: s = s[0].lower() + s[1:]
    extra = ''
    d = '%s: %s.%s%s' % (ti, s, extra, SUF[lang]) if s else '%s.%s' % (ti, SUF[lang])
    if len(d) > MAXL:
        d = '%s: %s.' % (ti, s)
        if len(d) > MAXL: d = d[:MAXL].rsplit(' ', 1)[0].rstrip(',;:.') + '.'
    return d

n = 0
files = [(f, 'it') for f in glob.glob(str(ROOT / '_negozio' / '*.md')) if 'categoria-' not in f] + \
        [(f, 'en') for f in glob.glob(str(ROOT / 'en' / 'negozio' / '*.md'))]
for f, lang in files:
    t = rd(f)
    if 'layout: negozio-prodotto' not in t: continue
    d = prodotto(t, lang)
    if d:
        n += 1
        print('%s\n   %d: %s' % (pathlib.Path(f).relative_to(ROOT), len(d), d))
        if APPLY: wr(f, set_desc(t, d))
for rel, d in PAGES.items():
    f = ROOT / rel
    if not f.exists(): print('MANCA', rel); continue
    t = rd(str(f))
    new = set_desc(t, d)
    if new != t:
        n += 1
        print('%s\n   %d: %s' % (rel, len(d), d))
        if APPLY: wr(str(f), new)
print('\nModificati: %d%s' % (n, '' if APPLY else ' (dry-run, usa --apply)'))
