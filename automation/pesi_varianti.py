# -*- coding: utf-8 -*-
"""
GUIDA-SVILUPPO: VARIANTI A PESO (grammi) + testi brevi piu' ricchi. Idempotente: si puo' rilanciare.
Uso dalla radice:  python automation/pesi_varianti.py   poi  python automation/allinea_hash.py en

COME FUNZIONA (leggi prima di toccare):
- _data/catalogo.json > "varianti": fasce valide per TUTTI i prodotti fisici [{g, prezzo_centesimi}] (prezzi in centesimi).
  Un prodotto puo' avere le sue fasce in p["varianti"] (se presente e non vuota vince su quelle globali).
- Nel carrello la riga e' l'id "<prodotto>~<grammi>" (es. origano~10). Il nome "Origano (10 g)" e il prezzo
  arrivano dal catalogo del header (_includes/masthead.html, attributo data-catalogo): per questo carrello, anteprima,
  ordine e riepilogo funzionano senza altre modifiche. L'id base (senza ~) resta valido per vecchi carrelli.
- prezzo_centesimi del prodotto = prezzo della prima fascia (serve a elenco e vecchi carrelli); lo riallinea questo script e l'admin.
- Admin: voce Shop > "Pesi e prezzi" (admin/index.html) modifica fasce globali e per prodotto.
"""
import io, json, re, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(R, *a)
def leggi(p):
    with io.open(p, encoding='utf-8', newline='') as f: return f.read()
def scrivi(p, t):
    with io.open(p, 'w', encoding='utf-8', newline='') as f: f.write(t)
def sostituisci(p, vecchio, nuovo, gia):
    """sostituisce UNA volta; se 'gia' e' presente il file e' gia' patchato"""
    t = leggi(p)
    if gia in t: return
    assert t.count(vecchio) == 1, (p, vecchio[:60], t.count(vecchio))
    scrivi(p, t.replace(vecchio, nuovo))

# ---------- 1) catalogo: fasce globali + testi brevi ----------
FASCE = [{"g": 5, "prezzo_centesimi": 99}, {"g": 10, "prezzo_centesimi": 179},
         {"g": 25, "prezzo_centesimi": 399}, {"g": 50, "prezzo_centesimi": 699}]

def frasi(t):
    t = re.sub(r'\s+', ' ', t.strip())
    return re.split(r'(?<=[.!?]) ', t)

def breve(completa, coda):
    par = [x.strip() for x in completa.split('\n\n') if x.strip()]
    intro = frasi(par[0])[0] if par else ''
    uso = ''
    for i, x in enumerate(par):
        if x.startswith('## ') and i + 1 < len(par) and not par[i + 1].startswith('## '):
            uso = frasi(par[i + 1])[0]; break
    return ' '.join(s for s in (intro, uso, coda) if s)

cp = P('_data', 'catalogo.json')
d = json.loads(leggi(cp))
if not d.get('varianti'): d['varianti'] = FASCE
for p in d['prodotti']:
    if p.get('descrizione_completa'):
        p['descrizione'] = breve(p['descrizione_completa'], 'Sacchetto richiudibile con clip.')
    en = (p.get('tr') or {}).get('en')
    if en and en.get('descrizione_completa'):
        en['descrizione'] = breve(en['descrizione_completa'], 'Resealable pouch with clip.')
    if p.get('tipo') != 'digitale':
        eff = sorted(p.get('varianti') or d['varianti'], key=lambda v: v['g'])
        p['prezzo_centesimi'] = eff[0]['prezzo_centesimi']
d['_nota_varianti'] = ('varianti = fasce a peso valide per tutti i prodotti fisici ([{g, prezzo_centesimi}]); '
                       'un prodotto con p.varianti usa le sue. Id nel carrello: <id>~<grammi>. Modifica da admin > Shop > Pesi e prezzi.')
scrivi(cp, json.dumps(d, ensure_ascii=False, indent=2) + '\n')

# ---------- 2) header: voci catalogo per ogni variante ----------
M = P('_includes', 'masthead.html')
sostituisci(M, '{%- unless b.visibile == false -%}{"id":',
 '{%- unless b.visibile == false -%}{%- capture nz_im -%}{% if b.immagine and b.immagine != \'\' %}{% if b.immagine contains \'://\' %}{{ b.immagine }}{% else %}{{ \'/\' | append: b.immagine | relative_url }}{% endif %}{% endif %}{%- endcapture -%}{"id":',
 'capture nz_im')
sostituisci(M, '"e":{{ b.icona | default: \'\' | jsonify }}},{%- endunless -%}',
 '"e":{{ b.icona | default: \'\' | jsonify }}},'
 '{%- if b.tipo != \'digitale\' -%}{%- assign nz_vv = b.varianti -%}{%- if nz_vv == nil or nz_vv.size == 0 -%}{%- assign nz_vv = site.data.catalogo.varianti -%}{%- endif -%}'
 '{%- for v in nz_vv -%}{"id":{{ b.id | append: \'~\' | append: v.g | jsonify }},"p":{{ v.prezzo_centesimi | jsonify }},"n":{{ b.tr[lg].nome | default: b.nome | append: \' (\' | append: v.g | append: \' g)\' | jsonify }},"t":"fisico","u":{{ nz_pu | jsonify }},"i":{{ nz_im | strip | jsonify }},"e":{{ b.icona | default: \'\' | jsonify }}},{%- endfor -%}{%- endif -%}'
 '{%- endunless -%}',
 'assign nz_vv = b.varianti')

# ---------- 3) scheda prodotto: selettore peso ----------
L = P('_layouts', 'negozio-prodotto.html')
sostituisci(L, "{%- assign nz_dig = false -%}",
 "{%- assign nz_vv = nz_p.varianti -%}{%- if nz_vv == nil or nz_vv.size == 0 -%}{%- assign nz_vv = site.data.catalogo.varianti -%}{%- endif -%}{%- assign nz_v0 = nz_vv | first -%}\n{%- assign nz_dig = false -%}",
 'assign nz_v0')
sostituisci(L, 'data-prezzo="{{ nz_p.prezzo_centesimi | default: 0 }}"',
 'data-prezzo="{% if nz_v0 and nz_p.tipo != \'digitale\' %}{{ nz_v0.prezzo_centesimi }}{% else %}{{ nz_p.prezzo_centesimi | default: 0 }}{% endif %}"{% if nz_v0 and nz_p.tipo != \'digitale\' %} data-g="{{ nz_v0.g }}"{% endif %}',
 'data-g="{{ nz_v0.g }}"')
sostituisci(L, '<p class="nz-prezzo nz-pp-prezzo fw-bold"></p>',
 '<p class="nz-prezzo nz-pp-prezzo fw-bold"></p>\n{%- if nz_v0 and nz_p.tipo != \'digitale\' -%}<div class="nz-var" role="radiogroup" aria-label="Peso">{% for v in nz_vv %}<button type="button" class="nz-vb{% if forloop.first %} on{% endif %}" role="radio" data-g="{{ v.g }}" data-p="{{ v.prezzo_centesimi }}">{{ v.g }} g</button>{% endfor %}</div>{%- endif -%}',
 'class="nz-var"')

# ---------- 4) riga elenco: parte dalla prima fascia ----------
G = P('_includes', 'negozio-riga.html')
sostituisci(G, "{%- assign nz_lh = '/' -%}{%- if page.lang",
 "{%- assign nz_vv = include.b.varianti -%}{%- if nz_vv == nil or nz_vv.size == 0 -%}{%- assign nz_vv = site.data.catalogo.varianti -%}{%- endif -%}{%- assign nz_v0 = nz_vv | first -%}\n{%- assign nz_lh = '/' -%}{%- if page.lang",
 'assign nz_v0')
sostituisci(G, 'data-prezzo="{{ include.b.prezzo_centesimi | default: 0 }}"',
 'data-prezzo="{% if nz_v0 and include.b.tipo != \'digitale\' %}{{ nz_v0.prezzo_centesimi }}{% else %}{{ include.b.prezzo_centesimi | default: 0 }}{% endif %}"{% if nz_v0 and include.b.tipo != \'digitale\' %} data-g="{{ nz_v0.g }}"{% endif %}',
 'data-g="{{ nz_v0.g }}"')
sostituisci(G, '<div class="nz-prezzo fw-bold"></div>',
 '<div class="nz-prezzo fw-bold"></div>{% if nz_v0 and include.b.tipo != \'digitale\' %}<p class="nz-peso">{% for v in nz_vv %}{{ v.g }}{% unless forloop.last %} &middot; {% endunless %}{% endfor %} g</p>{% endif %}',
 'class="nz-peso"')

# ---------- 5) carrello.js: riga = id~grammi ----------
J = P('assets', 'js', 'carrello.js')
sostituisci(J, 'aggId = card.dataset.id;',
 'aggId = card.dataset.id + (card.dataset.g ? "~" + card.dataset.g : ""); // variante a peso: id~grammi (vedi automation/pesi_varianti.py)',
 'card.dataset.g ? "~"')
sostituisci(J, '  /* ORDINE (/ordine/)',
 '''  /* VARIANTI PESO: i bottoni .nz-vb scelgono grammi e prezzo della scheda; "Aggiungi" usa data-g (id~grammi, voce presente nel catalogo del header) */
  radice.addEventListener("click", function (ev) {
    var v = ev.target.closest(".nz-vb");
    if (!v) return;
    var card = v.closest(".nz-box");
    card.dataset.g = v.dataset.g;
    card.dataset.prezzo = v.dataset.p;
    card.querySelectorAll(".nz-vb").forEach(function (x) {
      x.classList.toggle("on", x === v);
      x.setAttribute("aria-checked", x === v ? "true" : "false");
    });
    card.querySelector(".nz-prezzo").textContent = euro.format(Number(v.dataset.p) / 100);
  });

  /* ORDINE (/ordine/)''', 'VARIANTI PESO')

# ---------- 6) css ----------
C = P('assets', 'css', 'negozio.css')
if '.nz-vb' not in leggi(C):
    scrivi(C, leggi(C) + '''
/* VARIANTI PESO (selettore grammi nella scheda prodotto) */
.nz-var{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 14px}
.nz-vb{padding:8px 16px;border:1.5px solid #ddd;border-radius:var(--t-radius,10px);background:#fff;color:#333;font-weight:600;cursor:pointer}
.nz-vb:hover{border-color:var(--t-accent,#b5651d)}
.nz-vb.on{background:var(--t-accent,#b5651d);border-color:var(--t-accent,#b5651d);color:#fff}
.nz-peso{margin:2px 0 6px;font-size:.85em;color:#777}
''')

# ---------- 7) admin: pagina Shop > Pesi e prezzi ----------
A = P('admin', 'index.html')
sostituisci(A, '<div class="page" id="page-lingue">', '''<!-- PESI E PREZZI: fasce a grammi (_data/catalogo.json > varianti). Funzioni pesi*() nello script in fondo. -->
<div class="page" id="page-pesi">
<div class="page-title">&#9878; Pesi e prezzi</div>
<div class="card">
<div class="card-title">Fasce del negozio (valgono per tutti i prodotti fisici)</div>
<p style="font-size:13px;color:#666;margin-bottom:12px">Ogni fascia = grammi + prezzo. La prima (la pi&ugrave; piccola) &egrave; il prezzo &ldquo;da&rdquo; mostrato nell&rsquo;elenco.</p>
<div id="pesi-globali"><em style="color:#bbb;font-size:13px">Caricamento...</em></div>
<div class="btn-group"><button class="btn btn-secondary" onclick="pesiAdd('')">+ Fascia</button></div>
</div>
<div class="card">
<div class="card-title">Prodotto con fasce proprie (facoltativo)</div>
<div class="field"><label>Prodotto</label><select id="pesi-prod" onchange="pesiProd()"></select></div>
<div id="pesi-prodotto"></div>
</div>
<div class="btn-group"><button class="btn btn-primary" onclick="pesiSalva()">&#128190; Salva e pubblica</button></div>
<div class="msg" id="msg-pesi"></div>
</div>

<div class="page" id="page-lingue">''', 'id="page-pesi"')
sostituisci(A, '''<button class="nav-item" onclick="showPage('cat-prodotti',this)">''',
 '''<button class="nav-item" onclick="showPage('pesi',this)"><span class="icon">&#9878;</span>Pesi e prezzi</button>
<button class="nav-item" onclick="showPage('cat-prodotti',this)">''', "showPage('pesi',this)")
sostituisci(A, "  if(id==='cat-prodotti')caricaCatShop();",
 "  if(id==='cat-prodotti')caricaCatShop();\n  if(id==='pesi')caricaPesi();", "caricaPesi();")
sostituisci(A, 'async function ghGet(path){', '''// ============ PESI E PREZZI (varianti a grammi) ============
// Dati: _data/catalogo.json > varianti (globali) e prodotti[].varianti (solo se il prodotto ha fasce proprie).
// Prezzi in centesimi nel file, in euro (virgola) nei campi. Salva = riallinea anche prezzo_centesimi di ogni prodotto fisico alla prima fascia.
let _pesi=null,_pesiSha=null;
function pesiC2E(c){return (c/100).toFixed(2).replace('.',',');}
function pesiE2C(s){return Math.round(parseFloat(String(s).replace(',','.'))*100)||0;}
function pesiArr(id){
  if(!id)return _pesi.varianti;
  const p=_pesi.prodotti.find(x=>x.id===id);return p?p.varianti:null;
}
function pesiRows(id){
  const a=pesiArr(id)||[];
  return a.map((v,i)=>`<div style="display:flex;gap:8px;align-items:center;margin-bottom:8px">
    <input type="number" min="1" value="${v.g}" style="width:90px" onchange="pesiSet('${id}',${i},'g',this.value)"> g
    <input type="text" value="${pesiC2E(v.prezzo_centesimi)}" style="width:90px" onchange="pesiSet('${id}',${i},'p',this.value)"> &euro;
    <button class="btn btn-danger btn-sm" onclick="pesiDel('${id}',${i})">&#128465;</button></div>`).join('')||'<em style="color:#bbb;font-size:13px">Nessuna fascia.</em>';
}
function pesiDraw(){
  document.getElementById('pesi-globali').innerHTML=pesiRows('');
  const sel=document.getElementById('pesi-prod'),cur=sel.value;
  sel.innerHTML='<option value="">&mdash; scegli &mdash;</option>'+_pesi.prodotti.filter(p=>p.tipo!=='digitale').map(p=>`<option value="${p.id}">${p.nome}${p.varianti&&p.varianti.length?' *':''}</option>`).join('');
  sel.value=cur;pesiProd();
}
function pesiProd(){
  const id=document.getElementById('pesi-prod').value,box=document.getElementById('pesi-prodotto');
  if(!id){box.innerHTML='';return;}
  const p=_pesi.prodotti.find(x=>x.id===id);
  if(p.varianti&&p.varianti.length){
    box.innerHTML=pesiRows(id)+`<div class="btn-group"><button class="btn btn-secondary" onclick="pesiAdd('${id}')">+ Fascia</button><button class="btn btn-danger" onclick="pesiReset('${id}')">Torna alle fasce del negozio</button></div>`;
  }else{
    box.innerHTML=`<p style="font-size:13px;color:#666">Usa le fasce del negozio.</p><button class="btn btn-secondary" onclick="pesiOwn('${id}')">Dai fasce proprie (copia quelle del negozio)</button>`;
  }
}
function pesiSet(id,i,k,v){const a=pesiArr(id);if(k==='g')a[i].g=parseInt(v,10)||a[i].g;else a[i].prezzo_centesimi=pesiE2C(v);}
function pesiDel(id,i){pesiArr(id).splice(i,1);pesiDraw();}
function pesiAdd(id){const a=pesiArr(id);const last=a[a.length-1]||{g:0,prezzo_centesimi:0};a.push({g:last.g+5,prezzo_centesimi:last.prezzo_centesimi});pesiDraw();}
function pesiOwn(id){const p=_pesi.prodotti.find(x=>x.id===id);p.varianti=JSON.parse(JSON.stringify(_pesi.varianti));pesiDraw();}
function pesiReset(id){const p=_pesi.prodotti.find(x=>x.id===id);delete p.varianti;pesiDraw();}
async function caricaPesi(){
  const el=document.getElementById('pesi-globali');
  if(!tok()){el.innerHTML='<em style="color:#bbb;font-size:13px">Token mancante: vai in Token.</em>';return;}
  let res;try{res=await ghGet('_data/catalogo.json');}catch(e){el.innerHTML='<em>Errore di rete.</em>';return;}
  if(!res.ok){el.innerHTML='<em>catalogo.json non trovato (serve ecommerce: true).</em>';return;}
  const d=await res.json();_pesiSha=d.sha;_pesi=JSON.parse(dec(d.content));
  if(!_pesi.varianti)_pesi.varianti=[];
  pesiDraw();
}
async function pesiSalva(){
  if(!_pesi)return;
  const ord=a=>a.sort((x,y)=>x.g-y.g);
  ord(_pesi.varianti);
  _pesi.prodotti.forEach(p=>{
    if(p.varianti&&!p.varianti.length)delete p.varianti;
    if(p.varianti)ord(p.varianti);
    if(p.tipo!=='digitale'){const eff=p.varianti||_pesi.varianti;if(eff.length)p.prezzo_centesimi=eff[0].prezzo_centesimi;}
  });
  const res=await ghPut('_data/catalogo.json','Aggiorna pesi e prezzi',JSON.stringify(_pesi,null,2)+'\\n',_pesiSha||undefined);
  const j=await res.json();
  if(res.ok){_pesiSha=j.content.sha;showMsg('msg-pesi','Salvato: il sito si aggiorna in 1-2 minuti.','ok');pesiDraw();}
  else showMsg('msg-pesi','Errore salvataggio: '+(j.message||res.status),'err');
}

async function ghGet(path){''', 'PESI E PREZZI (varianti')

print('OK pesi_varianti')
