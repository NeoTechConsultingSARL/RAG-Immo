import os
import json
import re
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="mistral", temperature=0)

dossier_txt = "output"
path_json_final = "donnees_finales_ner.json"
fichiers_a_traiter = [4, 19, 20, 22, 29, 34, 35, 36, 43, 47, 48, 60, 63]

try:
    with open(path_json_final, 'r', encoding='utf-8') as f:
        resultats_ner = json.load(f)
    print(f"Base chargée : {len(resultats_ner)} contrats.")
except FileNotFoundError:
    resultats_ner = []
    print("Nouveau fichier créé.")

def extraire_donnees_pfe(texte_contrat):
    prompt = f"""
    Analyse ce contrat et extrais les entités en JSON.
    IMPORTANT : La date de signature est souvent à la toute FIN du texte.
    
    REGLÈS : 
    - Réponds uniquement par le JSON.
    - Utilise des guillemets doubles "" pour TOUTES les valeurs, surtout les dates.
    - Format date : "JJ/MM/AAAA".
    - Si absent : "Inconnu".

    CHAMPS :
    1. nom_client, 2. cin_client, 3. designation_bien, 4. prix_vente, 5. montant_avance, 6. date_signature, 7. ville

    TEXTE :
    {texte_contrat}
    """
    return llm.invoke(prompt)

tous_fichiers = sorted([f for f in os.listdir(dossier_txt) if f.endswith(".txt")])

for i, fichier in enumerate(tous_fichiers, 1):
    if i in fichiers_a_traiter:
        print(f"[{i}/64] Analyse ciblée : {fichier}...")
        
        with open(os.path.join(dossier_txt, fichier), "r", encoding="utf-8") as f:
            contenu = f.read()
            
        try:
            reponse_ia = extraire_donnees_pfe(contenu)
            
            debut = reponse_ia.find('{')
            fin = reponse_ia.rfind('}') + 1
            json_propre = json.loads(reponse_ia[debut:fin])
            
            nouvelle_entree = {
                "source_file": fichier,
                "data": json_propre
            }
            
            resultats_ner.append(nouvelle_entree)
            print(f" Ajouté : {json_propre.get('date_signature')}")
            
        except Exception as e:
            print(f" Erreur sur {fichier} : {e}")

with open(path_json_final, "w", encoding="utf-8") as f_json:
    json.dump(resultats_ner, f_json, indent=4, ensure_ascii=False)

print(f"Terminé. Le fichier contient maintenant {len(resultats_ner)} contrats.")