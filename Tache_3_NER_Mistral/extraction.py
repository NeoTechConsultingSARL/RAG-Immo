import os
import json
from langchain_ollama import OllamaLLM

# Configuration du modèle local 
llm = OllamaLLM(model="mistral", temperature=0) # temperature=0 pour plus de précision

dossier_txt = "output"
resultats_ner = []

def extraire_donnees_pfe(texte_contrat):
    # Prompt optimisé pour la structure de  Graphe Neo4j
    prompt = f"""
    En tant qu'expert en système d'information immobilier, analyse ce contrat et extrais les entités suivantes au format JSON.
    REGLÈS : 
    - Ne réponds QUE par le JSON. 
    - Si une info est absente, mets "Inconnu".

    CHAMPS REQUIS :
    1. nom_client : (Nom complet du client/acquéreur)
    2. cin_client : (Numéro de CIN si disponible)
    3. designation_bien : (Numéro d'appartement ou de local)
    4. prix_vente : (Montant total en chiffres)
    5. montant_avance : (Somme versée à la signature)
    6. date_signature : (Format JJ/MM/AAAA)
    7. ville : (Lieu de situation du bien)

    TEXTE DU CONTRAT :
    {texte_contrat[:2500]} 
    """
    return llm.invoke(prompt)

print(" Lancement de l'extraction finale ..")

fichiers = [f for f in os.listdir(dossier_txt) if f.endswith(".txt")]

for i, fichier in enumerate(fichiers):
    print(f"[{i+1}/{len(fichiers)}] Analyse de : {fichier}...")
    
    with open(os.path.join(dossier_txt, fichier), "r", encoding="utf-8") as f:
        contenu = f.read()
        
    try:
        reponse_ia = extraire_donnees_pfe(contenu)
        
        #  nettoyage da la réponse si l'IA ajoute du texte autour du JSON
        debut = reponse_ia.find('{')
        fin = reponse_ia.rfind('}') + 1
        json_propre = json.loads(reponse_ia[debut:fin])
        
        resultats_ner.append({
            "source_file": fichier,
            "data": json_propre
        })
    except Exception as e:
        print(f" Erreur sur {fichier} : {e}")

# Sauvegarde du fichier qui servira de base à Neo4j
with open("donnees_finales_ner.json", "w", encoding="utf-8") as f_json:
    json.dump(resultats_ner, f_json, indent=4, ensure_ascii=False)

print(f"Le fichier 'donnees_finales_ner.json' contient les données de  64 contrats.")