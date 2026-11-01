import io, json, os, subprocess, sys, glob
# GUIDA-SVILUPPO: pipeline unica spezieclip. Uso dalla radice del repo:  python automation/sviluppa_spezie.py [--no-push]
# Fa in ordine: contenuti (home, chi siamo, articoli) -> permalink articoli -> hash EN -> controlli JSON/testo -> commit + push.
# Idempotente: si puo' rilanciare. Le foto prodotto NON sono qui (vedi IMMAGINI.md, automation/foto_spezie.py).
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(R)
env = dict(os.environ, PYTHONIOENCODING='utf-8')
def run(*a):
    r = subprocess.run(a, capture_output=True, text=True, encoding='utf-8', env=env)
    out = (r.stdout + r.stderr).strip()
    print('>', ' '.join(a[1:]), '->', 'OK' if r.returncode == 0 else 'ERRORE %d' % r.returncode)
    if out: print('   ' + out[-300:].replace('\n', '\n   '))
    if r.returncode: sys.exit(r.returncode)
    return out
py = sys.executable
run(py, 'automation/contenuti_spezie.py')
run(py, 'automation/permalink_articoli.py', '--apply')
run(py, 'automation/allinea_hash.py', 'en')
# controlli: JSON validi e niente testo corrotto (mojibake)
bad = []
for f in glob.glob('_data/**/*.json', recursive=True):
    try: t = io.open(f, encoding='utf-8').read(); json.loads(t)
    except Exception as e: bad.append('JSON rotto %s: %s' % (f, e)); continue
    if '\u00c3' in t or '\ufffd' in t: bad.append('testo corrotto in ' + f)
for f in glob.glob('_posts/*.md') + glob.glob('en/_posts/*.md') + glob.glob('_pages/*.md'):
    t = io.open(f, encoding='utf-8').read()
    if '\u00c3' in t or '\ufffd' in t: bad.append('testo corrotto in ' + f)
if bad: print('\n'.join(bad)); sys.exit(2)
print('controlli ok')
if '--no-push' in sys.argv: sys.exit(0)
run('git', 'add', '-A')
if subprocess.run(['git', 'diff', '--cached', '--quiet']).returncode == 0: print('niente da pubblicare'); sys.exit(0)
run('git', 'commit', '-q', '-m', 'Home, Chi siamo e articoli IT+EN, tolto Servizi')
print(subprocess.run(['git', 'push'], capture_output=True, text=True).stderr.strip().splitlines()[-1])
