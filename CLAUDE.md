# Life of a Data Project — Contexte pour Claude

## Le projet

Projet académique réalisé en groupe (Groupe 5) dans le cadre du cursus à Albert School.

**Objectif business** : Aider un opérateur télécom à optimiser son réseau de boutiques dans la zone commerciale **5_SUD_EST**. La recommandation finale classe chaque boutique dans une des 4 catégories : **FERMER / MAINTENIR / DÉVELOPPER / OUVRIR**.

**GitHub** : https://github.com/lservignat-alt/life-of-a-data-project

---

## Données sources

| Fichier | Contenu | Taille brute |
|---|---|---|
| `Fichier_Principal_pedago_anonym.csv` | Acquisitions clients (anonymisé) | 3,2M lignes, 13 colonnes |
| `COORD_BQT.csv` | Coordonnées GPS des boutiques (Lambert II) | 1 042 lignes |
| `LIB_BQT.csv` | Noms/labels des boutiques | 3 435 lignes |
| `Dico_Donnees.xlsx` | Dictionnaire des variables | — |
| `GeoData.json` / `GeoData_bis.json` | Données géographiques France | 2 MB / 13 MB |

**Clé de jointure entre les 3 tables** : `ORDER_SHOP_CD` (code boutique)

**Variables principales du fichier principal** :
- `ZONE` — zone commerciale (filtré sur `5_SUD_EST` = 326 478 lignes conservées)
- `ORDER_SHOP_CD` — code boutique
- `PERIOD_YYYY` + `PERIOD_MM` — période d'acquisition (2021-10 à 2022-12)
- `LINE_TYPE` — type de produit (mobile / box / fixe)
- `PERSON_BIRTH_DT_year` — décennie de naissance du client
- `CITY_LN` — ville du client
- `Geolife` — segment socio-démographique

---

## Pipeline — Les 8 étapes (toutes complétées)

| Notebook | Étape | Ce qui a été fait |
|---|---|---|
| `Etape_0_1_Preparation_Comprehension.ipynb` | Chargement & compréhension | Inspection des 4 fichiers, vérification de la clé de jointure, distribution des zones |
| `Etape_2_Nettoyage.ipynb` | Nettoyage | Filtre zone SUD-EST, 81 107 doublons supprimés, nettoyage ORDER_SHOP_CD, création colonne PERIOD datetime, suppression aberrants naissance, normalisation villes |
| `Etape_3_Jointure.ipynb` | Jointure des tables | Conversion Lambert II → WGS84, jointure principale × COORD_BQT × LIB_BQT → `base_travail_SUD_EST.csv` |
| `Etape_4_Exploration.ipynb` | Exploration | Analyse univariée, bivariée, temporelle (N vs N-1), géographique par département |
| `Etape_5_Nouvelles_Variables.ipynb` | Feature engineering | `age_client`, `tranche_age`, `distance_km` (Haversine client ↔ boutique), `rayon_chalandise`, `croissance_yoy`, `part_mobile`/`part_fixe`, `score_rentabilite` |
| `Etape_6_Analyse_Metier.ipynb` | Analyse métier | Tableau de bord par boutique, CC vs CV, segmentation, heatmap produits, saisonnalité → `tableau_bord_boutiques.csv` |
| `Etape_7_Modele_Business.ipynb` | Modèle business | Modélisation CA/marge, ROI ouverture/relocalisation, grille FERMER/MAINTENIR/DÉVELOPPER/OUVRIR → `recommandations_boutiques_SUD_EST.csv` |
| `Etape_8_Livrable.ipynb` | Livrable final | Synthèse complète, toutes sections, visualisations finales |

> Il existe aussi `Etape_4_Exploration.ipynb` à la racine et `analyses.ipynb` à la racine — ce sont des **versions de travail intermédiaires**, pas les versions finales. Les versions finales sont dans `01_Notebooks/`.

---

## Hypothèses business clés

**Structure de coûts (données fournies) :**
- Centre-Commercial (CC) : 85 000 EUR/an
- Centre-Ville (CV) : 65 000 EUR/an
- Ouverture / Relocalisation : 450 000 EUR (coût unique)

**ARPU estimé (source ARCEP) :**
- Mobile : 200 EUR/an/client
- Box/Fixe : 350 EUR/an/client

**Points de vigilance respectés :**
- Pas de CA réel dans les données → hypothèses ARPU explicites
- Pas de clé client → analyse sur acquisitions uniquement (pas de churn, pas de LTV)
- Déploiement fibre NRO (ARCEP) mentionné comme levier pour recommandations OUVRIR

---

## Structure des dossiers

```
01_Notebooks/         → Les 8 notebooks finaux (source de vérité)
02_Données/
  Brutes/             → Données sources originales
  Intermédiaires/     → Après nettoyage et jointure
  Finales/            → Outputs finaux (recommandations, tableaux de bord)
03_Graphiques/
  V1/                 → Graphiques version 1 (étapes 5-8)
  V2/                 → Graphiques version 2 (étape 4, plus récents)
04_Livrables/         → Livrable Word + PDF pour le client
05_Documentation/     → journal_nettoyage.txt, guides PDF
06_Scripts/           → requirements.txt, script_anonymisation.py
_Archives/            → Anciennes versions (ne pas modifier)
Dossier données/      → Dossier de données original (legacy, redondant avec 02_Données/)
```

---

## Stack technique

```
Python 3 + Jupyter
pandas, numpy
matplotlib, plotly
geopandas, pyproj, shapely, fiona, rtree
Environnement virtuel : .venv (non versionné)
```

---

## État d'avancement

**Toutes les étapes sont complétées.** Le livrable final existe (`04_Livrables/Opérateur Telecom.docx` + `.pdf`).

Les fichiers de données produits à la fin du pipeline :
- `02_Données/Finales/base_enrichie_SUD_EST.csv` — dataset complet enrichi
- `02_Données/Finales/tableau_bord_boutiques.csv` — métriques par boutique
- `02_Données/Finales/recommandations_boutiques_SUD_EST.csv` — recommandations FERMER/MAINTENIR/etc.
- `02_Données/Finales/livrable_recommandations_finales.csv` — version finale livrable
