import streamlit as st
import requests
from io import BytesIO

# Fonctions pour obtenir le token et les documents
def get_token():
    # ... (Votre code existant ici)

def get_documents(siren, token):
    # ... (Votre code existant ici)

def download_document(doc_id, token):
    url = f"https://registre-national-entreprises.inpi.fr/api/actes/{doc_id}/download"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        return None

# Configuration Streamlit
# ... (Votre code existant ici)

# Titre de la page
# ... (Votre code existant ici)

# Entrée du SIREN
# ... (Votre code existant ici)

# Obtenir le token
# ... (Votre code existant ici)

if token and siren:
    documents = get_documents(siren, token)
    if documents:
        for doc in documents:
            # ... (Votre code existant pour afficher les détails du document)
            
            doc_id = doc.get('id')  # Assume 'id' is the key that contains the document ID
            if doc_id:
                pdf_data = download_document(doc_id, token)
                if pdf_data:
                    st.download_button(
                        label="Télécharger le document",
                        data=pdf_data,
                        file_name=f"{doc_id}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Impossible de télécharger le document.")
    else:
        st.warning("Aucun document trouvé pour ce SIREN.")
else:
    if not token:
        st.error("Impossible d'obtenir le token.")
