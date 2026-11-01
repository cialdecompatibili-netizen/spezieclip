# IMMAGINI.md - Foto prodotti con Gemini API (senza Chrome), valida per OGNI sito

Un solo motore per tutti i siti: `Desktop\gemini_auto\core\foto_sito.py`. Niente script copiati nei repo.
Cosa cambia da sito a sito sta in `<repo>\_data\` (nessun nome o percorso fisso nel motore).

## Comando (1 riga, `<repo>` = cartella del sito)
    python $HOME\Desktop\gemini_auto\core\foto_sito.py --repo <repo> --api
Prodotti senza foto = quelli fisici con `"immagine": ""` in `_data/catalogo.json`. Opzioni:
`--ids a,b` rifa quelli | `--extra "testo"` aggiunge al prompt | `--dry` mostra i prompt | `--no-push` solo commit | `--rielabora` rifa sfondo/ritaglio dagli originali (0 crediti).
PowerShell: prima `$env:PYTHONIOENCODING='utf-8'`.

## Come si definisce lo stile di un sito (2 modi)
1. Bottiglie/bevande (default, nessun file): colore in `<repo>\_data\colori_foto.json` `{"id": "arancione ..."}`.
2. Qualsiasi altro prodotto: crea `<repo>\_data\foto_prompt.json`:
       {"template": "<prompt in inglese con {nome} e {aspetto}>", "default": "<aspetto generico>", "aspetti": {"<id>": "<aspetto di quel prodotto>"}}
   `{nome}` = nome del prodotto in catalogo (va in etichetta), `{aspetto}` = voce di `aspetti` per l'id (o `default`), `{id}` = id.
   Esempio vivo: `_data/foto_prompt.json` di spezieclip (barattolo di vetro + sacchetto kraft con clip).
   Regole sul prompt: etichetta SOLO col nome prodotto, niente marchi inventati; sfondo bianco e formato li impone il profilo `gemini_auto\profili\prodotto.md`.

## Nuovo prodotto = 3 passi
1. Aggiungilo in `_data/catalogo.json` con `"immagine": ""` (+ le pagine `_negozio/<id>.md` e `<lingua>/negozio/<id>.md`).
2. Se il sito usa `foto_prompt.json`: aggiungi la voce in `aspetti` (colore e forma in inglese).
3. Lancia il comando (senza `--ids` fa tutti quelli senza foto): genera, sfondo bianco, webp 1000/500/200, copia in `assets/images/prodotti/<id>.webp`, aggiorna il catalogo, commit e push (~10-15 s a foto).

## Problemi
- Crediti finiti: NON aspettare il reset. Pubblica quelle fatte, rilancia le altre dopo con `--ids`. Crediti: `python Desktop\gemini_auto\img.py --crediti`.
- Nome storpiato in etichetta: `--ids <id> --extra "The label must contain ONLY the text '<Nome>'. No other words."`
- Marchi o scritte sul sacchetto: `--extra "The pouch label is completely blank."`
- Batch bloccato: i file generati stanno in `Desktop\gemini_auto\immagini\prodotto\originali`; poi `--rielabora --ids ...` li pubblica senza crediti.
- "NON generati via API": rilancia con `--ids`; se persiste, senza `--api` usa il watcher con Chrome. Cookie scaduti (uscita 3): `gemini_auto\COOKIE_SCADUTI.md` + `login.bat`.
- Limite Gemini ~1408x768: la scheda mostra 1000 px con lightbox.

## Pipeline contenuti (non foto)
`python automation/sviluppa.py [-m "msg"] [--no-push] [--solo-controlli]` dal repo: esegue `automation/contenuti_*.py` del sito, permalink articoli, hash di ogni lingua trovata, controlli (JSON, testo corrotto, post con data futura), commit e push. Lingue e script si rilevano da soli.
