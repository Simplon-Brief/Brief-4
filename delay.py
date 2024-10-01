from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configurer le WebDriver de Selenium (Assurez-vous que chromedriver est installé et dans votre PATH)
driver = webdriver.Chrome()

# L'URL à scrapper
url = "https://quotes.toscrape.com/js-delayed/page/10/"
driver.get(url)

# Attendre que les citations soient chargées dans l'élément avec l'ID 'quotesPlaceholder'
# Nous attendons jusqu'à 15 secondes (délai de sécurité en plus des 10 secondes du script)
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "quotesPlaceholder"))
)

# Attendre qu'il y ait au moins 5 citations (ceci est spécifique à cette page)
# En attente que 5 éléments avec la classe 'quote' soient chargés dans 'quotesPlaceholder'
WebDriverWait(driver, 20).until(
    lambda d: len(d.find_elements(By.CLASS_NAME, "quote")) >= 5
)

# Extraire le contenu de la page après le chargement
page_source = driver.page_source

# Utiliser BeautifulSoup pour analyser le contenu de la page
soup = BeautifulSoup(page_source, 'html.parser')

# Trouver toutes les citations dans le div avec l'ID 'quotesPlaceholder'
quote_divs = soup.find('div', id='quotesPlaceholder').find_all('div', class_='quote')

# Vérifier s'il y a au moins 5 citations
if len(quote_divs) >= 5:
    # Extraire la cinquième citation
    fifth_quote_div = quote_divs[4]  # Les index commencent à 0, donc la cinquième citation est à l'index 4

    # Extraire le texte de la citation
    quote_text = fifth_quote_div.find('span', class_='text').get_text(strip=True)

    # Extraire le nom de l'auteur
    author_name = fifth_quote_div.find('small', class_='author').get_text(strip=True)

    # Extraire les tags
    tags = [tag.get_text(strip=True) for tag in fifth_quote_div.find_all('a', class_='tag')]

    # Afficher les résultats
    print(f"Citation : {quote_text}")
    print(f"Auteur : {author_name}")
    print(f"Tags : {', '.join(tags)}")
else:
    print("Il y a moins de 5 citations sur cette page.")

# Fermer le WebDriver
driver.quit()
