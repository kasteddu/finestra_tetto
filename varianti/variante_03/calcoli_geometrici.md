# Calcoli geometrici - variante 03

**Tavola:** A-04

**Stato:** preliminare, non per costruzione

## 1. Rilievo di partenza

| Parametro | Valore |
| --- | ---: |
| Lunghezza lungo il piano inclinato | 120,0 cm |
| Larghezza trasversale | 93,0 cm |
| Quota dei bordi | 53,0 cm e 10,0 cm |

## 2. Correzione della proiezione

Il dislivello iniziale è:

```text
h = 53,0 - 10,0 = 43,0 cm
```

L'angolo rispetto all'orizzontale è:

```text
alpha = arcsin(43,0 / 120,0) = 21,0°
```

La proiezione orizzontale della misura inclinata è:

```text
L_plan = sqrt(120,0² - 43,0²) = 112,0 cm
```

Per ottenere una luce orizzontale netta di 120,0 cm lungo la direzione di apertura, il nuovo fronte deve arretrare di:

```text
Delta = 120,0 - 112,0 = 8,0 cm
```

Il nuovo telaio deve quindi estendersi di circa 8,0 cm verso il lato basso, dove rimane la porta frontale.

## 3. Suddivisione delle ante

La luce di 120,0 cm viene divisa in due ante:

```text
l_anta = 120,0 / 2 = 60,0 cm
```

Dimensioni nominali di ciascuna anta:

```text
60,0 x 93,0 cm
```

La dimensione reale del telaio dell'anta dovrà comprendere battuta centrale, sovrapposizione perimetrale e giochi.

## 4. Movimento a libro

Con un'anta di 60,0 cm incernierata sul lato esterno e un'apertura di progetto di 75°:

```text
sollevamento del bordo libero = 60,0 x sin(75°) = 58,0 cm
proiezione verso il centro      = 60,0 x cos(75°) = 15,53 cm
```

La distanza libera tra i bordi centrali, vista in pianta, è:

```text
luce centrale = 120,0 - 2 x 15,53 = 88,94 cm
```

L'angolo di 75° è un'ipotesi di progetto e non una misura rilevata.

## 5. Fasce vetrate perimetrali

Se il nuovo piano orizzontale viene mantenuto alla quota del bordo alto, cioè +53,0 cm:

```text
altezza massima del raccordo vetrato = 53,0 - 10,0 = 43,0 cm
```

La fascia frontale sopra la porta può quindi raggiungere 43,0 cm. Le fasce laterali hanno altezza variabile tra il lato frontale e quello posteriore e richiedono una misurazione del cordolo reale.

## 6. Dati non ancora calcolabili

Non è possibile scegliere definitivamente i pistoni senza:

- spessore e composizione del vetro;
- profilo e sezione del telaio di ogni anta;
- peso di cerniere, maniglie e guarnizioni;
- posizione esatta degli ancoraggi;
- angolo di apertura definitivo;
- verifica della forza del vento sulla posizione aperta.

I pistoni proposti sono due, uno per anta. La forza e la corsa devono essere calcolate a partire dal momento rispetto alla cerniera.

## 7. Verifica preliminare del peso

Area nominale di una singola anta:

```text
A = 0,60 x 0,93 = 0,558 m²
```

Stima indicativa del solo vetro laminato, considerando circa 2,5 kg/m² per millimetro di spessore:

| Vetro | Peso del vetro | Peso anta con telaio e accessori stimati |
| --- | ---: | ---: |
| 6+6 mm | circa 16,7 kg | circa 23-27 kg |
| 8+8 mm | circa 22,3 kg | circa 28-32 kg |

Il momento statico rispetto alla cerniera, con baricentro ipotizzato a 30 cm e anta orizzontale, è:

```text
M = m x 9,81 x 0,30
```

Ciò corrisponde a circa 67-95 N·m per anta secondo la configurazione. La forza necessaria al pistone dipende da:

```text
F = M / (distanza di ancoraggio x componente utile del braccio)
```

La selezione definitiva deve includere un coefficiente di sicurezza e la verifica della posizione di ancoraggio su telaio e cerniera.
