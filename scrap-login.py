from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialisation du navigateur
driver = webdriver.Chrome()

# Accéder à l'URL
driver.get("http://quotes.toscrape.com/login")

# Attente pour les champs de login et mot de passe
wait = WebDriverWait(driver, 8)

# Remplir le champ login
login_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
login_field.send_keys("UserName")

# Remplir le champ mot de passe et soumettre le formulaire
password_field = driver.find_element(By.ID, "password")
password_field.send_keys("Password")
password_field.submit()  # Utilisation de submit() pour soumettre le formulaire

# Attendre quelques secondes pour que la page se charge
time.sleep(5)

