import requests
from bs4 import BeautifulSoup

# URL de base du site Books to Scrape
BASE_URL = "https://books.toscrape.com/"

# Fonction pour scraper les livres d'une catégorie donnée et calculer le nombre total de livres et le prix moyen
def scrape_books_from_category(category_url):
    total_books = 0
    total_price = 0
    page_number = 1
    has_next_page = True
    
    while has_next_page:
        # Générer l'URL de la page actuelle (remplacer index.html par page-X.html si nécessaire)
        if page_number == 1:
            url = f"{BASE_URL}{category_url}"
        else:
            url = f"{BASE_URL}{category_url}".replace("index.html", f"page-{page_number}.html")
        
        # Faire la requête HTTP pour récupérer la page
        page = requests.get(url)
        
        # Vérifier si la page existe (code 200)
        if page.status_code != 200:
            break
        
        # Analyse le contenu HTML de la page
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Trouver tous les livres sur la page
        books = soup.find_all('article', class_="product_pod")
        
        # Compter et calculer le prix des livres sur cette page
        for book in books:
            price = book.find('p', class_='price_color').get_text(strip=True)
            price_value = float(price[1:])  # On retire le symbole "£" et convertit en float
            total_books += 1
            total_price += price_value
        
        # Vérifier s'il y a une page suivante
        next_button = soup.find('li', class_='next')
        has_next_page = next_button is not None
        page_number += 1
    
    # Calcul du prix moyen
    if total_books > 0:
        average_price = total_price / total_books
    else:
        average_price = 0
    
    return total_books, average_price

# Envoi d'une requête GET à l'URL principale pour obtenir la page d'accueil
page = requests.get(BASE_URL)

# Vérification de la réponse HTTP
if page.status_code == 200:
    print(f"Connexion réussie avec le code: {page.status_code}")
    
    # Analyse du contenu de la page d'accueil avec BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # Recherche des catégories de livres
    category_list = soup.find('ul', class_="nav nav-list")

    if category_list:
        # Trouver tous les liens des catégories (balises <a>) et exclure la catégorie "Books"
        categories = category_list.find_all('a')
        filtered_categories = [category for category in categories if category.get_text(strip=True).lower() != "books"]

        # Affichage du nombre total de catégories restantes
        print(f"Nombre total de catégories (hors 'Books') : {len(filtered_categories)}")

        # Parcourir chaque catégorie pour récupérer le nom et l'URL
        for category in filtered_categories:
            category_name = category.get_text(strip=True)
            category_url = category['href']
            
            if category_name and category_url != "#":
                print(f"\nScraping category: {category_name}")
                
                # Appel de la fonction pour scraper les livres de la catégorie et obtenir le nombre de livres et le prix moyen
                num_books, avg_price = scrape_books_from_category(category_url)
                
                # Affichage du résultat pour la catégorie
                print(f"Nombre total de livres dans la catégorie '{category_name}': {num_books}")
                print(f"Prix moyen des livres dans la catégorie '{category_name}': £{avg_price:.2f}")
    else:
        print("Impossible de trouver la liste des catégories.")
else:
    print(f"Échec de la connexion. Code de statut: {page.status_code}")
