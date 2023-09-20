import streamlit as st
import requests
from io import BytesIO
import pandas as pd

# Fonctions pour obtenir le token et les documents
def get_token():
    # ... (pas de changement ici)
    pass

def get_documents(siren, token):
    # ... (pas de changement ici)
    pass

def download_document(doc_id, token):
    # ... (pas de changement ici)
    pass

# Configuration Streamlit
st.set_page_config(
    # ... (pas de changement ici)
)

# Titre de la page
st.header("Consultation des Actes d'Entreprises via SIREN")
st.caption("App développée par Kevin MAMERI")

# Entrée du SIREN
siren = st.text_input("Veuillez entrer le SIREN de l'entreprise:")

# Obtenir le token
token = get_token()

if token and siren:
    documents = get_documents(siren, token)
    data_list = []  # Pour stocker les données de chaque document
    if documents:
        for doc in documents:
            date_depot = doc.get('dateDepot')
            nom_document = doc.get('nomDocument')
            
            for type_rdd in doc.get('typeRdd', []):
                type_acte = type_rdd.get('typeActe')
                decision = type_rdd.get('decision')
            
            doc_id = doc.get('id')  # Assume 'id' is the key that contains the document ID
            download_button = None
            if doc_id:
                pdf_data = download_document(doc_id, token)
                if pdf_data:
                    # Créer un bouton de téléchargement en tant que chaîne HTML
                    download_button = f'<a href="data:application/pdf;base64,{pdf_data.read().encode("base64").decode("utf-8")}" download="{doc_id}.pdf">Télécharger le document</a>'
                else:
                    st.error("Impossible de télécharger le document.")

            # Ajoutez les données du document actuel à data_list
            data_list.append({
                "Date de dépôt": date_depot,
                "Type d'acte": type_acte,
                "Décision": decision,
                "Télécharger le document": download_button
            })
        
        # Convertissez data_list en un DataFrame
        df = pd.DataFrame(data_list)

        # Affichez le DataFrame avec Streamlit
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
    else:
        st.warning("Aucun document trouvé pour ce SIREN.")
else:
    if not token:
        st.error("Impossible d'obtenir le token.")
