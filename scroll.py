from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_quotes(url):
    # Configurer le WebDriver de Selenium
    driver = webdriver.Chrome()  # Assurez-vous que chromedriver est installé et dans votre PATH
    driver.get(url)

    # Attendre que le contenu initial se charge
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "quote"))
    )

    # Initialiser le nombre total de citations
    total_quotes = 0

    # Extraire et afficher les données initiales
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, "html.parser")
    initial_quotes = initial_soup.find_all("div", class_="quote")
    total_quotes += len(initial_quotes)
    extract_and_print_quotes(initial_quotes)

    # Simuler des événements de défilement pour charger plus de contenu
    for scroll_count in range(4):  # Supposons qu'il y a 5 événements de défilement au total
        # Faire défiler vers le bas avec JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Attendre que le contenu chargé dynamiquement apparaisse
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quote"))
        )

        # Extraire et afficher les nouvelles citations chargées
        scroll_html = driver.page_source
        scroll_soup = BeautifulSoup(scroll_html, "html.parser")
        scroll_quotes = scroll_soup.find_all("div", class_="quote")
        total_quotes += len(scroll_quotes)
        extract_and_print_quotes(scroll_quotes)

    # Afficher le nombre total de citations
    print(f"Nombre total de citations : {total_quotes}")

    # Fermer le WebDriver
    driver.quit()

def extract_and_print_quotes(quotes):
    # Extraire et afficher les citations
    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

        print(f"Citation : {text}")
        print(f"Auteur : {author}")
        print(f"Tags : {', '.join(tags)}")
        print("----------")

if __name__ == "__main__":
    # L'URL cible à scraper
    target_url = "http://quotes.toscrape.com/scroll"
    scrape_quotes(target_url)
