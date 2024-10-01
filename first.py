from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configurer le WebDriver de Selenium (Assurez-vous que chromedriver est installé et dans votre PATH)
driver = webdriver.Chrome()

# L'URL à scrapper
url = "https://quotes.toscrape.com/js/page/10/"
driver.get(url)

# Attendre que la première citation soit chargée (en utilisant la classe 'quote')
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "quote"))
)

# Extraire le contenu de la page après le chargement
page_source = driver.page_source

# Utiliser BeautifulSoup pour analyser le contenu de la page
soup = BeautifulSoup(page_source, 'html.parser')

# Trouver la première citation
first_quote_div = soup.find('div', class_='quote')

if first_quote_div:
    # Extraire le texte de la citation
    quote_text = first_quote_div.find('span', class_='text').get_text(strip=True)

    # Extraire le nom de l'auteur
    author_name = first_quote_div.find('small', class_='author').get_text(strip=True)

    # Extraire les tags
    tags = [tag.get_text(strip=True) for tag in first_quote_div.find_all('a', class_='tag')]

    # Afficher les résultats
    print(f"Citation : {quote_text}")
    print(f"Auteur : {author_name}")
    print(f"Tags : {', '.join(tags)}")

else:
    print("Aucune citation trouvée.")


