import json
import re

def clean_price(price_str):
    if price_str == "Inconnu": return 0.0
    # Enlever "DH", les espaces et remplacer la virgule par un point
    clean_str = re.sub(r'[^\d,.]', '', str(price_str)).replace(',', '.')
    try:
        return float(clean_str)
    except:
        return 0.0

# Charger le JSON 
with open("donnees_finales_ner.json", "r", encoding="utf-8") as f:
    base_donnees = json.load(f)

for entree in base_donnees:
    data = entree["data"]
    
    # 1. Nettoyage des prix (Conversion en nombres)
    data["prix_vente"] = clean_price(data.get("prix_vente"))
    data["montant_avance"] = clean_price(data.get("montant_avance"))
    
    # 2. Uniformisation du CIN
    if "CIN" in str(data.get("cin_client")) or data.get("cin_client") == "Inconnu (CIN masqué dans le texte)":
        data["cin_client"] = "Masqué"
        
    # 3. Nettoyage de la Ville
    if "Nador" in str(data.get("ville")):
        data["ville"] = "Nador"

# Sauvegarde du fichier propre
with open("donnees_finales_ner_propre.json", "w", encoding="utf-8") as f:
    json.dump(base_donnees, f, indent=4, ensure_ascii=False)

print(" Nettoyage terminé ! Le fichier 'donnees_finales_ner_propre.json' est prêt pour Neo4j.")