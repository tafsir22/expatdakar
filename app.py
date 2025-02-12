import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
# --- Fonctions de scraping ---
def load_data(file_path):
    """Charge les données scrapées en DataFrame."""
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"Le fichier {file_path} n'existe pas.")
        return None

def telephone(pages):
    """Scrape les données des téléphones sur expat-dakar.com"""
    df = pd.DataFrame()
    for page in range(1, pages+1):  
        url = f'https://www.expat-dakar.com/telephones?page={page}'
        print(url)
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item') 

        data = []
        for container in containers:
            try:
                url_container = container.find('a', class_='listing-card__inner')['href']
                res_c = requests.get(url_container)
                soup_c = bs(res_c.text, 'html.parser')
            
                dd_elements = soup_c.find_all('dd', class_="listing-item__properties__description")
                
                etat = dd_elements[0].text.strip()
                marque = dd_elements[1].text.strip()
                details = soup_c.find('h1', class_ = "listing-item__header")
                price = soup_c.find('span', class_="listing-card__price__value").text.strip().replace('F Cfa', '')
                address = soup_c.find('span', class_="listing-item__address-location").text.strip()
                image_link = soup_c.find('img', class_="gallery__image__resource vh-img").get('src', '')
            
                dic = {
                    'details': details,
                    'Etat': etat,
                    'Marque': marque,
                    'Prix': price,
                    'Adresse': address,
                    'Image_link': image_link
                }
                data.append(dic)
            except Exception as e:
                pass
                # print(f"Erreur lors du traitement d'un conteneur : {e}")
        DF = pd.DataFrame(data)
        df = pd.concat([df,DF], axis=0).reset_index(drop=True)
    df.to_csv('telephone.csv', index=False)
    return df

def ordinateurs(pages):
    """Scrape les données des ordinateurs sur expat-dakar.com."""
    df = pd.DataFrame()
    for page in range(1, pages+1):  
        url = f'https://www.expat-dakar.com/ordinateurs?page={page}'
        print(url)
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item') 

        data = []
        for container in containers:
            try:
                url_container = container.find('a', class_='listing-card__inner')['href']
                res_c = requests.get(url_container)
                soup_c = bs(res_c.text, 'html.parser')
            
                dd_elements = soup_c.find_all('dd', class_="listing-item__properties__description")
                
                etat = dd_elements[0].text.strip()
                marque = dd_elements[1].text.strip()
                details = soup_c.find('h1', class_ = "listing-item__header")
                price = soup_c.find('span', class_="listing-card__price__value 1").text.strip().replace('F Cfa', '')
                address = soup_c.find('span', class_="listing-item__address-location").text.strip()
                image_link = soup_c.find('img', class_="gallery__image__resource vh-img").get('src', '')
            
                dic = {
                    'details': details,
                    'Etat': etat,
                    'Marque': marque,
                    'Prix': price,
                    'Adresse': address,
                    'Image_link': image_link
                }
                data.append(dic)
            except Exception as e:
                pass
                # print(f"Erreur lors du traitement d'un conteneur : {e}")
        DF = pd.DataFrame(data)
        df = pd.concat([df,DF], axis=0).reset_index(drop=True)
        
        df.to_csv('ordinateur.csv', index=False)
        return df

def tv_home(pages):
    """Scrape les données des tv et multimédias sur expat-dakar.com."""
    df = pd.DataFrame()
    for page in range(1, pages+1):  
        url = f'https://www.expat-dakar.com/tv-home-cinema?page={page}'
        print(url)
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='listings-cards__list-item') 

        data = []
        for container in containers:
            try:
                url_container = container.find('a', class_='listing-card__inner')['href']
                res_c = requests.get(url_container)
                soup_c = bs(res_c.text, 'html.parser')
            
                dd_elements = soup_c.find_all('dd', class_="listing-item__properties__description")
                
                etat = dd_elements[0].text.strip()
                marque = dd_elements[1].text.strip()
                details = soup_c.find('h1', class_ = "listing-item__header")
                price = soup_c.find('span', class_="listing-card__price__value 1").text.strip().replace('F Cfa', '')
                address = soup_c.find('span', class_="listing-item__address-location").text.strip()
                image_link = soup_c.find('img', class_="gallery__image__resource vh-img").get('src', '')
            
                dic = {
                    'details': details,
                    'Etat': etat,
                    'Marque': marque,
                    'Prix': price,
                    'Adresse': address,
                    'Image_link': image_link
                }
                data.append(dic)
            except Exception as e:
                pass
                # print(f"Erreur lors du traitement d'un conteneur : {e}")
        DF = pd.DataFrame(data)
        df = pd.concat([df,DF], axis=0).reset_index(drop=True)
        df.to_csv("tv_home.csv", index=False)
        return df

# --- Application Streamlit ---
st.set_page_config(page_title="Scraping Expat-Dakar", layout="centered")
page = st.sidebar.selectbox("Choisissez une page :", ["🏠 Accueil", "📊 Scraping", "⭐ Noter l'Application", "📋 Données Nettoyées"])

if page == "🏠 Accueil":
    st.title("Bienvenue sur l'application de scraping Expat-Dakar")
    st.write("Cette application vous permet de scraper des données sur les téléphones, ordinateurs et tv et multimédias du site Expat-Dakar.")
    st.write("Pour commencer, sélectionnez '📊 Scraping' dans le menu lateral.")

# Page de scraping
elif page == "📊 Scraping":
    st.title("Scraping Expat-Dakar")
    st.sidebar.header("Configuration du Scraping")
    type_scraping = st.sidebar.radio("Choisissez une catégorie :", ["Téléphones", "Ordinateurs", "Tv et multimédias"])
    pages = st.sidebar.number_input("Nombre de pages à scraper :", min_value=1, max_value=50, value=5)
    if st.sidebar.button("Lancer le scraping"):
        # Initialisation des éléments d'affichage sur la page principale
        progress_text = "Scraping en cours..."
        my_bar = st.progress(0, text=progress_text)  # Barre de progression sur la page principale
        page_status = st.empty()
        
        try:
            if type_scraping == "Téléphones":
                total_items = telephone(pages)
                data_file = "telephone.csv"
            elif type_scraping == "Ordinateurs":
                total_items = ordinateurs(pages)
                data_file = "ordinateur.csv"
            elif type_scraping == "Tv et multimédias":
                total_items = tv_home(pages)
                data_file = "tv_home.csv"

            # Message de succès après le scraping
            page_status.success(f"✅ Scraping terminé ! {len(total_items)} éléments ont été récupérés.")
            my_bar.empty() 

            
            data = load_data(data_file)
            if data is not None:
                st.markdown("### 🔍 Résultats du scraping")
                st.dataframe(data)
                st.download_button(
                    "Télécharger les données",
                    data.to_csv(index=False),
                    file_name=data_file,
                    mime="text/csv"
                )
            else:
                st.error("Aucune donnée trouvée.")

        except Exception as e:
            page_status.error(f"Erreur lors du scraping : {e}")

# Données nettoyer 
elif page == "📋 Données Nettoyées":
    st.title("Données Nettoyées")
    st.title("Visualisation des Données Nettoyées")

    # Définir le chemin vers le répertoire contenant les fichiers CSV préconfigurés
    directory = "cleans"  # Adaptez ce chemin à votre configuration

    # Récupération de la liste des fichiers CSV dans le répertoire
    try:
        files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    except Exception as e:
        st.error(f"Erreur lors de l'accès au répertoire : {e}")
        files = []

    if files:
        # Sélection d'un fichier via un selectbox
        selected_file = st.selectbox("Sélectionnez un fichier à afficher :", files)
        file_path = os.path.join(directory, selected_file)
        
        # Lecture et affichage du fichier CSV sélectionné
        try:
            data = pd.read_csv(file_path)
            st.success(f"Fichier '{selected_file}' chargé avec succès !")
            st.dataframe(data)
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")
    else:
        st.warning("Aucun fichier CSV n'a été trouvé dans le répertoire spécifié.")

# Page pour noter l'application
elif page == "⭐ Noter l'Application":
    st.title("Noter cette application")
    st.write("Nous apprécions vos retours pour améliorer notre service. Veuillez prendre quelques secondes pour évaluer l'application.")

    # Collecte des informations utilisateur
    name = st.text_input("Votre nom complet :")
    email = st.text_input("Votre adresse e-mail :")
    
    # Système de notation
    rating = st.slider("Quelle note donnez-vous à cette application ?", 1, 5, 3)
    feedback = st.text_area("Ajoutez un commentaire (facultatif) :", "")
    feedback_file = "feedback/user_feedback.csv"
    if st.button("Soumettre votre avis"):
        # Enregistrement des notes et commentaires dans un fichier CSV
        if not name or not email:
            st.error("Veuillez remplir votre nom et votre adresse e-mail.")
        else:
            # Enregistrement des notes et commentaires dans un fichier CSV
            feedback_data = pd.DataFrame({
                "Name": [name],
                "Email": [email],
                "Rating": [rating],
                "Feedback": [feedback]
            })

            if os.path.exists(feedback_file):
                feedback_data.to_csv(feedback_file, mode='a', header=False, index=False)
            else:
                feedback_data.to_csv(feedback_file, index=False)

            st.success("Merci pour votre retour ! 🙏")

    # Affichage des retours utilisateur
    if os.path.exists(feedback_file):
        st.subheader("Retours utilisateurs :")
        feedback_df = pd.read_csv(feedback_file)
        st.dataframe(feedback_df)
