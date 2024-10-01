import requests
from bs4 import BeautifulSoup

# URL de la première page
url = "http://quotes.toscrape.com/page/1/"
page_count = 0  # Initialiser le compteur de pages

while True:
    # Faire la requête HTTP pour charger la page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Incrémenter le compteur de pages
    page_count += 1
    print(f"Page {page_count} scraped.")
    
    # Vérifier si le lien "Next" est présent
    next_button = soup.find('li', class_='next')
    if next_button:
        # Extraire le lien vers la page suivante
        next_page_url = next_button.find('a')['href']
        url = "http://quotes.toscrape.com" + next_page_url
    else:
        # S'il n'y a plus de bouton "Next", terminer la boucle
        break

# Afficher le nombre total de pages
print(f"Total pages: {page_count}")
