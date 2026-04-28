import fitz  # PyMuPDF
import re
import os

def traiter_contrat(chemin_pdf):
    # 1. Extraction du texte
    doc = fitz.open(chemin_pdf)
    texte_brut = ""
    for page in doc:
        texte_brut += page.get_text()
    
    # 2. Nettoyage de base (Post-processing)
    # On remplace les multiples sauts de ligne par un seul
    texte_propre = re.sub(r'\n+', '\n', texte_brut)
    # On enlève les espaces en trop
    texte_propre = re.sub(r' +', ' ', texte_propre)
    
    return texte_propre

def anonymiser_texte(texte):
    # 1. Masquer les numéros de téléphone (Maroc)
    texte = re.sub(r'0[5-7]([\s.-]?\d){8}', '[TEL_MASQUÉ]', texte)
    # 2. Masquer le Fax 
    texte = re.sub(r'05([\s.-]?\d){8}', '[FAX_MASQUÉ]', texte)
    # 3. Masquer les CIN 
    texte = re.sub(r'[A-Z]{1,2}\s?\d{5,6}', '[CIN_MASQUÉ]', texte)
    # 4. Masquer les Emails 
    texte = re.sub(r'\S+@\S+', '[EMAIL_MASQUÉ]', texte)
    
    return texte

dossier_entree = "contrats_pdf"
dossier_sortie = "output"

if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

for fichier in os.listdir(dossier_entree):
    if fichier.endswith(".pdf"):
        print(f"Traitement de : {fichier}")
        
        # Extraire et nettoyer
        contenu = traiter_contrat(os.path.join(dossier_entree, fichier))
        # Anonymiser
        contenu_final = anonymiser_texte(contenu)
        
        # Sauvegarder en format .txt
        nom_txt = fichier.replace(".pdf", ".txt")
        with open(os.path.join(dossier_sortie, nom_txt), "w", encoding="utf-8") as f:
            f.write(contenu_final)

print("Tâche 2 terminée avec succès !")