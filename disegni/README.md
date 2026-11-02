# Disegni tecnici

Foglio `A-01` preliminare dell'apertura per finestra sul tetto.

## Dati di rilievo

- Misura netta lungo la pendenza: 120 cm
- Misura trasversale: 93 cm
- Bordo alto: +53 cm
- Bordo basso: +10 cm
- Dislivello: 43 cm
- Inclinazione derivata: 21,0°
- Proiezione orizzontale lungo la pendenza: circa 112,0 cm

Le quote verticali di 53 cm e 10 cm sono considerate riferite allo stesso piano orizzontale. Il foglio contiene solo la geometria confermata; spessori, profili, cerniere e fissaggi devono ancora essere rilevati.

## File generati

- `../finestra_tetto_A01.svg`: tavola vettoriale
- `../finestra_tetto_A01.pdf`: tavola pronta per la stampa

Per rigenerarli:

```bash
python3 disegni/genera_disegno.py
```

Il documento è preliminare e non è destinato alla costruzione.

## Varianti

Ogni variante viene salvata in una cartella numerata sotto `varianti/`.

```bash
python3 disegni/genera_orizzontale.py
python3 disegni/genera_concept.py
python3 disegni/genera_a_libro.py
python3 disegni/genera_concept_a_libro.py
python3 disegni/genera_variante_03.py
```

I risultati vengono scritti nelle rispettive cartelle `varianti/variante_NN/`.
