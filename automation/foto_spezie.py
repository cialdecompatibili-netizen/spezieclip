import sys
# Wrapper di foto_sito.py per spezieclip: cambia solo il prompt (barattolo di vetro + sacchetto kraft con clip).
# Uso: python foto_spezie.py --repo C:\Users\mirco\Desktop\repository\spezieclip --api [--ids a,b] [--no-push]
sys.path.insert(0, r"C:\Users\mirco\Desktop\gemini_auto\core")
import foto_sito
ASP = {
"aglio-granulare": "coarse pale cream-white garlic granules",
"cannella-bastoncini": "rolled cinnamon sticks standing upright",
"cannella-macinata": "fine reddish-brown ground cinnamon",
"curcuma-macinata": "bright golden-yellow turmeric powder",
"zenzero-macinato": "pale beige-yellow ground ginger",
"noce-moscata": "fine light-brown ground nutmeg, one whole nutmeg in front of the jar",
"cumino-macinato": "warm greenish-brown ground cumin",
"coriandolo-macinato": "light tan-brown ground coriander",
"paprika-dolce": "vivid red sweet paprika powder",
"paprika-affumicata": "deep dark red-brown smoked paprika powder",
"semi-di-sesamo": "pale beige sesame seeds",
"origano": "dried grey-green oregano leaves",
"basilico": "dried green basil leaves",
"rosmarino": "dried needle-like rosemary pieces",
"timo": "tiny dried grey-green thyme leaves",
"salvia": "dried silvery-green sage leaves",
"prezzemolo": "bright green dried parsley flakes",
"menta-piperita": "dried green peppermint leaves",
"pepe-nero-grani": "whole black peppercorns",
"pepe-nero-macinato": "dark grey-black ground pepper",
"pepe-bianco-grani": "pale cream-white peppercorns",
"peperoncino-cayenna": "bright orange-red ground cayenne pepper",
"peperoncino-jalapeno": "dark green dried jalapeno chilli flakes",
"miscela-pizza": "dried green herb mix with small red flecks",
"garam-masala": "warm brown ground spice blend",
"curry-polvere": "golden yellow-orange curry powder",
"condimento-aglio-olio": "pale garlic granules mixed with red chilli flakes",
"condimento-bistecche": "coarse dark brown seasoning with peppercorn pieces and flecks",
}
def pp(p, colori, extra):
    nome = p["nome"]; asp = ASP.get(p["id"], "ground spice")
    s = (f'a small elegant clear glass spice jar with a cork-style lid, filled to the top with {asp}, simple cream paper label '
         f'with the readable text "{nome}"; beside the jar a small kraft paper resealable pouch with a clip, same spice, plain label')
    return s + (", " + extra if extra else "")
foto_sito.prompt_prodotto = pp
foto_sito.main()
