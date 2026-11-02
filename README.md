# finestra_tetto

Progetto di rilievo e sviluppo di una finestra fisica per tetto.

## Stato del progetto

La variante attuale è la **03 - ricalcolo geometrico a libro**: due ante vetrate incernierate ai lati opposti, due pistoni a gas, porta frontale invariata e fasce vetrate perimetrali.

## Registro varianti

| Cartella | Tavola | Configurazione | Stato |
| --- | --- | --- | --- |
| `varianti/variante_01/` | A-02 | Coperchio unico scorrevole sopra il piano | Superata, conservata |
| `varianti/variante_02/` | A-03 | Prima impostazione a libro | Superata, conservata |
| `varianti/variante_03/` | A-04 | Ricalcolo geometrico e quote corrette | Attuale, preliminare |

## Rilievo di base

- `foto_orig/`: sei fotografie originali; indice e note in `foto_orig/README.md`.
- `anteprime/`: copie JPEG delle foto 3-6 per la visualizzazione su GitHub.
- Le fotografie sono prive di metadati EXIF, GPS e dati del dispositivo.
- `specifiche_tecniche.md`: misure e calcoli dello stato iniziale inclinato.
- `finestra_tetto_A01.pdf`: tavola dello stato iniziale.
- `finestra_tetto_A01.svg`: sorgente vettoriale dello stato iniziale.
- `disegni/`: generatori delle tavole e dei concept.

## Dati principali

- Luce dell'apertura: 120 × 93 cm.
- Stato iniziale lungo la pendenza: 120 cm.
- Stato iniziale trasversale: 93 cm.
- Bordi iniziali: +53 cm e +10 cm.
- Inclinazione iniziale derivata: 21,0°.
- Variante attuale: piano orizzontale.

## Organizzazione delle varianti

Ogni nuova variante deve essere pubblicata in una nuova cartella `varianti/variante_NN/`, senza sovrascrivere le precedenti. La cartella deve contenere tavola PDF, tavola SVG, immagine/concept e relazione tecnica. Dopo ogni modifica va aggiornato questo registro, seguito da commit e push su GitHub.

Il materiale è preliminare e deve essere verificato sul posto prima di qualsiasi utilizzo costruttivo.
