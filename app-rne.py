import streamlit as st
import requests
import base64

# Fonctions pour obtenir le token et les documents
def get_token(stage=1):
    url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
    payload = {
        "username": "kmameri@scores-decisions.com",
        "password": "POC-Kevin-2023!"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        st.write(f"Erreur : {response.status_code}")
        st.write(f"Réponse : {response.text}")
        return None

# Obtenir le token (étape 1)
token = get_token(stage=1)

def get_document_list(siren, token):
    url = f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}/attachments"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()


def get_document(doc_id, doc_type, token=token):
    url = f"https://registre-national-entreprises.inpi.fr/api/{doc_type}/{doc_id}/download"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None



def trigger_download(data, filename) -> str:
    b64 = base64.b64encode(data).decode()
    dl_link = f"""
                <html>
                <head>
                <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
                <script>
                $('<a href="data:application/octet-stream;base64,{b64}" download="{filename}">')[0].click()
                </script>
                </head>
                </html>"""
    return dl_link


def callback_button(doc_id, doc_type) -> None:
    import streamlit.components.v1 as components
    trigger = trigger_download(get_document(doc_id, doc_type), f"{doc_id}.pdf")
    components.html(html=trigger, height=0, width=0)
    return


# Configuration Streamlit
st.set_page_config(
    page_title="Consultation des Actes d'Entreprises",
    layout='wide',
    page_icon="📑",
    menu_items={
         'About': 'Call Kevin MAMERI',
     }
)

# Titre de la page
st.header("Consultation des Actes d'Entreprises via SIREN")
st.caption("App développée par Kevin MAMERI")

# Entrée du SIREN
siren = st.text_input("Veuillez entrer le SIREN de l'entreprise:")


if token and siren:
    with st.spinner(f"Getting data ... 💫"):
        document_list = get_document_list(siren, token)

    tab_actes, tab_bilans, tab3 = st.tabs(["Actes", "Bilans", "IDK"])

    actes_list = document_list["actes"]
    bilans_list = document_list["bilans"]
    with tab_actes:
        if actes_list:
            colms = st.columns((1, 2, 2, 1))
            fields = ["Date de dépôt", "Type d'acte", "Décision", "Téléchargement"]
            for col, field_name in zip(colms, fields):
                col.write(field_name)
            for doc in actes_list:
                col1, col2, col3, col4 = st.columns((1, 2, 2, 1))
                col1.write(doc["dateDepot"])
                if "typeRdd" in doc:
                    col2.write("  \n".join(e.get("typeActe", "") for e in doc["typeRdd"]))
                    col3.write("  \n".join(e.get("decision", "") for e in doc["typeRdd"]))
                button_phold = col4.empty()
                do_action = button_phold.button("PDF", on_click=callback_button, args=(doc["id"], "actes",), key=f"button_actes_{doc['id']}")

        else:
            st.warning("Aucun document trouvé pour ce SIREN.")
    with tab_bilans:
        if bilans_list:
            colms = st.columns((1, 1, 1))
            fields = ["Date de dépôt", "Date de clôture", "Téléchargement"]
            for col, field_name in zip(colms, fields):
                col.write(field_name)
            for doc in bilans_list:
                col1, col2, col3 = st.columns((1, 1, 1))
                col1.write(doc["dateDepot"])
                col2.write(doc["dateCloture"])
                button_phold = col3.empty()
                do_action = button_phold.button("PDF", on_click=callback_button, args=(doc["id"], "bilans",), key=f"button_bilans_{doc['id']}")
        else:
            st.warning("Aucun bilan trouvé pour ce SIREN.")
else:
    if not token:
        st.error("Impossible d'obtenir le token.")