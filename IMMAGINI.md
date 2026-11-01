# IMMAGINI.md - Foto prodotti spezieclip (Gemini API, senza Chrome)

Stile: barattolo di vetro con tappo in sughero + sacchetto kraft con clip accanto, sfondo bianco #FFFFFF, 1:1, webp.
Etichetta: SOLO il nome prodotto (niente marchi, niente altre scritte).

## Comando (1 riga, dalla cartella claudetemp o ovunque)
Prodotti senza foto:
    python C:\Users\mirco\Desktop\repository\spezieclip\automation\foto_spezie.py --repo C:\Users\mirco\Desktop\repository\spezieclip --api

Rifare uno o piu' prodotti (anche se hanno gia' la foto):
    python ...\automation\foto_spezie.py --repo C:\Users\mirco\Desktop\repository\spezieclip --api --ids origano,timo

Opzioni: `--no-push` (solo commit) | `--dry` (mostra i prompt) | `--extra "testo"` (aggiunge al prompt) | `--rielabora` (rifa sfondo/ritaglio dagli originali, senza Gemini, senza crediti).
In PowerShell prima: `$env:PYTHONIOENCODING='utf-8'`.

## Cosa fa da solo
Genera con Gemini (cookie Google in `Desktop\gemini_api_test\cookies.json`), sistema sfondo bianco, crea webp 1000/500/200,
copia in `assets/images/prodotti/<id>.webp`, aggiorna `_data/catalogo.json` (campo `immagine`), commit e push. ~10-15 s a foto.

## Nuovo prodotto = 3 passi (per non sbagliare)
1. Aggiungi il prodotto in `_data/catalogo.json` con `"immagine": ""` (+ le 2 pagine `_negozio/<id>.md` e `en/negozio/<id>.md`, come `automation/popola_spezie.py`).
2. Aggiungi l'aspetto della spezia in `automation/foto_spezie.py`, dizionario `ASP` (chiave = id, valore = descrizione in inglese: colore e forma, es. "bright orange-red ground cayenne pepper"). Senza voce usa "ground spice" (generico).
3. Lancia il comando sopra (senza `--ids` fa tutti quelli senza foto).

## Regole
- NON toccare a mano `immagine` nel catalogo se usi lo script: lo aggiorna lui.
- Il prompt sta in `foto_spezie.py` (funzione `pp`). Per cambiare stile modifica solo li'.
- Profilo base (sfondo, formato, "solo nome in etichetta"): `Desktop\gemini_auto\profili\prodotto.md`.
- Se Gemini storpia il nome sull'etichetta: `--ids <id> --extra "The label must contain ONLY the text '<Nome>'. No other words."`
- Se Gemini aggiunge marchi o scritte sul sacchetto: stesso trucco con `--extra "The pouch label is completely blank."`
- Se il batch si blocca o non risponde: controlla `Get-ChildItem Desktop\gemini_auto\immagini\prodotto\originali | sort LastWriteTime -desc`; i file gia' generati ci sono, poi `--rielabora --ids ...` li pubblica senza usare crediti.

## Crediti e problemi
- Crediti Gemini: si vedono nel log all'avvio ("credits remaining"); `python Desktop\gemini_auto\img.py --crediti`.
- Crediti finiti: NON aspettare il reset. Pubblica quelle gia' fatte (lo script lo fa da solo per i riusciti), le altre le rilanci dopo con `--ids`.
- Il comando stampa "NON generati via API": rilancia solo quelli con `--ids`; se persiste, senza `--api` usa il watcher con Chrome (piano B).
- Cookie scaduti (codice uscita 3): `Desktop\gemini_auto\COOKIE_SCADUTI.md` + `login.bat`.
- Limite: Gemini non supera ~1408x768; la scheda usa la foto da 1000 px con lightbox.
