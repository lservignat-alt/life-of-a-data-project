"""
Anonymisation d'un fichier CRM enrichi — usage pédagogique
Approche : suppression des coordonnées, généralisation minimale
"""

import pandas as pd

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
INPUT_FILE = "Fichier_Principal.csv"
OUTPUT_FILE = "Fichier_Principal_pedago_anonym.csv"
K = 5

# ─────────────────────────────────────────
# 1. CHARGEMENT
# ─────────────────────────────────────────
print("Chargement du fichier...")
df = pd.read_csv(INPUT_FILE)
print(f"Lignes chargées : {len(df):,}")

# ─────────────────────────────────────────
# 2. SUPPRESSION des champs identifiants
# ─────────────────────────────────────────
df = df.drop(columns=[
    "COORD_X",        # adresse précise
    "COORD_Y",        # adresse précise
    "IRIS2000_CD",    # maille trop fine
    "INSEE_NB",       # redondant avec ville
    "POSTAL_CD",      # redondant avec ville + département
], errors="ignore")

# ─────────────────────────────────────────
# 3. GÉNÉRALISATION année de naissance
#    → tranche décennale ex: "1960-1969"
# ─────────────────────────────────────────
df["PERSON_BIRTH_DT_year"] = df["PERSON_BIRTH_DT_year"].apply(
    lambda y: f"{(int(y)//10)*10}-{(int(y)//10)*10+9}" if pd.notna(y) else None
)

# ─────────────────────────────────────────
# 4. GÉNÉRALISATION des petites communes
#    < K occurrences → remplacée par "AUTRE"
# ─────────────────────────────────────────
city_counts = df["CITY_LN"].value_counts()
small_cities = city_counts[city_counts < K].index
nb_small = df["CITY_LN"].isin(small_cities).sum()
print(f"Communes trop petites : {len(small_cities):,} communes ({nb_small:,} lignes → 'AUTRE')")
df.loc[df["CITY_LN"].isin(small_cities), "CITY_LN"] = "AUTRE"

# ─────────────────────────────────────────
# 5. VÉRIFICATION DU K-ANONYMAT
# ─────────────────────────────────────────
QUASI_IDS = [
    "PERSON_BIRTH_DT_year",
    "PERSON_SALUTATION_CD",
    "DEPRTMNT_ID",
    "GEOLIFE_AGG",
]

# Normalisation civilité
df["PERSON_SALUTATION_CD"] = df["PERSON_SALUTATION_CD"].str.strip().str.upper().str.replace(".", "", regex=False)
# M, M., M -> "M"
# MME, Mme, MME. -> "MME"

# Nettoyage espaces ville
df["CITY_LN"] = df["CITY_LN"].str.strip()


print(f"\n── Vérification k={K} ──")
group_sizes = df.groupby(QUASI_IDS).size().reset_index(name="group_size")
violations  = group_sizes[group_sizes["group_size"] < K]
nb_lignes   = df.merge(violations, on=QUASI_IDS).shape[0]

print(f"Groupes totaux       : {len(group_sizes):,}")
print(f"Groupes en violation : {len(violations):,}")
print(f"Lignes concernées    : {nb_lignes:,}  ({100*nb_lignes/len(df):.1f}%)")

# ─────────────────────────────────────────
# 6. SUPPRESSION des lignes en violation
# ─────────────────────────────────────────
# Étape 6 corrigée
# Étape 6 corrigée
if len(violations) > 0:
    before = len(df)
    
    # Créer une clé composite pour identifier les groupes en violation
    violation_keys = set(
        violations[QUASI_IDS].apply(tuple, axis=1)
    )
    df_keys = df[QUASI_IDS].apply(tuple, axis=1)
    
    df = df[~df_keys.isin(violation_keys)]
    
    print(f"Lignes supprimées    : {before - len(df):,}  ({100*(before-len(df))/before:.1f}%)")
else:
    print("✓ Aucune violation")

print(f"Lignes finales       : {len(df):,}  ({100*len(df)/(len(df)+before-len(df) if len(violations) > 0 else len(df)):.1f}% conservées)")

# ─────────────────────────────────────────
# 7. EXPORT
# ─────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n✓ Fichier exporté : {OUTPUT_FILE}")
print(f"\nColonnes finales : {list(df.columns)}")