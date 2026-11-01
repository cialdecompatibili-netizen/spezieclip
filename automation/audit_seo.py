#!/usr/bin/env python3
"""Audit SEO: title/description di tutte le pagine .md (IT+EN). Solo lettura.
USO: python automation/audit_seo.py"""
import re, sys, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {'node_modules', '_site', '.git', 'automation', 'redirect', 'vendor'}
rows = []
for p in ROOT.rglob('*.md'):
    rel = p.relative_to(ROOT)
    if any(x in SKIP for x in rel.parts) or rel.name.upper() in ('README.MD', 'CLAUDE.MD', 'ISTRUZIONI.MD'):
        continue
    t = p.read_text(encoding='utf-8', errors='ignore')
    m = re.match(r'---\s*\n(.*?)\n---', t, re.S)
    if not m: continue
    fm = m.group(1)
    if 'redirect_to' in fm: continue
    def g(k):
        mm = re.search(r'^%s:\s*(.*)$' % k, fm, re.M)
        return mm.group(1).strip().strip('"\'') if mm else ''
    rows.append((str(rel), g('title'), g('excerpt') or g('description'), g('permalink')))
dup = collections.Counter(r[1] for r in rows if r[1])
bad = 0
for f, ti, de, pl in sorted(rows):
    pr = []
    if not ti: pr.append('NO TITLE')
    elif len(ti) > 60: pr.append('title %d>60' % len(ti))
    if ti and dup[ti] > 1: pr.append('title duplicato')
    if not de: pr.append('NO DESC')
    elif len(de) > 160: pr.append('desc %d>160' % len(de))
    elif len(de) < 50: pr.append('desc %d<50' % len(de))
    if re.search(r'lorem|segnaposto|Sostituisci|esempio|placeholder', ti + de, re.I): pr.append('PLACEHOLDER')
    if pr:
        bad += 1
        print('%s | %s | %s' % (f, ' ; '.join(pr), ti[:50]))
print('\nPagine: %d, con problemi: %d' % (len(rows), bad))
