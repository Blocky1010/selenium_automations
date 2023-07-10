#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import os
import time

def effacer_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def count_days(start_date, end_date, jour_semaine):
    current_date = start_date
    dayz = []

    while current_date <= end_date:
        if current_date.weekday() == jour_semaine:  # 0 = Lundi, 1 = Mardi, 2 = Mercredi, 3 = Jeudi
            dayz.append(current_date)
        current_date += timedelta(days=1)

    return len(dayz), dayz

def inputs():
    effacer_terminal()
    start_date_in = input("Veuillez entrer la date de début (jour/mois/année) : ")
    effacer_terminal()
    end_date_in = input("Veuillez entrer la date de fin (jour/mois/année) : ")
    effacer_terminal()
    nom_lieu = "Altrimenti Maison de l'alimentation anti-gaspi"
    choix1 = int(input("Tapez '1' ( Altrimenti Maison de... ) ou '2' ( Personnalisé )\n\n->\t"))
    if choix1 == 1:
        pass 
    if choix1 == 2:
        nom_lieu = input("Nom lieu :\n\n->\t")
    effacer_terminal()
    adresse = "56 Boulevard Sérurier"
    choix2 = int(input("Tapez '1' ( 56 Boulevard Séru... ) ou '2' ( Personnalisé )\n\n->\t"))
    if choix2 == 1:
        pass
    if choix2 == 2:
        adresse = input("Adresse :\n\n->\t")
    effacer_terminal()
    debut = input("Entrez l'heure de début sous cette forme : 'HHmm',\nPar exemple si on veut noter 17h30 alors cela donnera -> 1730.\n\n->\t")
    effacer_terminal()
    fin = input("Entrez l'heure de fin sous cette forme : 'HHmm',\nPar exemple si on veut noter 19h00 alors cela donnera -> 1900.\n\n->\t")
    effacer_terminal()
    description = input("Ici, collez la description de l'atelier.\n\n->\t")
    effacer_terminal()
    prix = input("Entrez le prix sous forme simplement de chiffre:\n\n->\t")
    effacer_terminal()

    # Conversion des chaînes de caractères en objets datetime
    start_date = datetime.strptime(start_date_in, "%d/%m/%Y")
    end_date = datetime.strptime(end_date_in, "%d/%m/%Y")

    jour_semaine = int(input("Veuillez entrer le chiffre correspondant au jour de la semaine (0 pour lundi, 1 pour mardi, etc.) :\n\n->\t"))
    effacer_terminal()

    num_days, day_dates = count_days(start_date, end_date, jour_semaine)

    liste_jours = []
    for date1 in day_dates:
        formatted_date = date1.strftime("%d/%m/%Y")
        liste_jours.append(formatted_date)

    titre = input("\nEntrez le nom de l'évènement\nPar exemple : A table avec les anciens\n\n->\t")

    return titre,nom_lieu,adresse,debut,fin,description,prix,liste_jours,num_days

def login(var_driver):
    time.sleep(1)
    cookie = var_driver.find_element(By.XPATH,'//*[@id="axeptio_main_button"]')
    cookie.click()
    time.sleep(1)
    no = var_driver.find_element(By.XPATH,'//*[@id="axeptio_btn_dismiss"]')
    no.click()

    liste = var_driver.find_element(By.XPATH, '//*[@id="LayoutDefault"]/div[3]/header/button[2]')
    liste.click()

    compte = var_driver.find_element(By.XPATH, '//*[@id="LayoutDefault"]/div[3]/header/nav/ul/li[1]/button')
    compte.click()

    email = var_driver.find_element(By.XPATH, '//*[@id="LayoutDefault"]/div[3]/header/div/div/div/div[1]/form/div[1]/div/div[2]/div')
    email2 = email.find_element(By.TAG_NAME, "input")
    email2.send_keys("svergati@altrimenti-asso.org")

    mdp = var_driver.find_element(By.XPATH, '//*[@id="LayoutDefault"]/div[3]/header/div/div/div/div[1]/form/div[2]/div/div[2]/div/div')
    mdp2 = mdp.find_element(By.TAG_NAME, "input")
    mdp2.send_keys("Altrimenti21!")

    connect = var_driver.find_element(By.XPATH, '//*[@id="LayoutDefault"]/div[3]/header/div/div/div/div[2]/button')
    connect.click()


def actions(var_driver, name, nom_lieu, adresse, debut, fin, description, prix, liste_jours, num_days, i):

    var_driver.set_window_size(1100,800)
    #Rédaction nom
    time.sleep(1)
    atelier = var_driver.find_element(By.ID, "HaFormFieldInput-1")
    atelier.send_keys(name)
    #Choix de la catégorie
    selector1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/div[2]/select')
    type = Select(selector1)
    type.select_by_value("2")
    #Rédaction de l'adresse
    lieu = var_driver.find_element(By.ID, "HaFormFieldInput-4")
    lieu.send_keys(nom_lieu)

    input_element4 = var_driver.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[1]/div/div/div[1]/div[2]/button')
    input_element4.click()

    input_element3 = var_driver.find_element(By.ID, "HaFormFieldInput-12")
    input_element3.send_keys(adresse)

    input_element3 = var_driver.find_element(By.ID, "HaFormFieldInput-13")
    input_element3.send_keys("75019")

    input_element3 = var_driver.find_element(By.ID, "HaFormFieldInput-14")
    input_element3.send_keys("Paris")
    time.sleep(1)
    select_element = var_driver.find_element(By.XPATH, '//*[@id="HaFormFieldInput-15"]')
    pays = Select(select_element)
    pays.select_by_visible_text("France")

    time.sleep(1)
    duree = var_driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[1]/div/div/div[2]/fieldset/div[2]/label')
    duree.click()

    time.sleep(1)

    jour = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[1]/div/div/div[2]/div/fieldset[1]/div/div/div[2]/div/span/div[1]/input')
    jour.send_keys(str(liste_jours[i]))
    #Ecrire heure de début
    beg = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[1]/div/div/div[2]/div/fieldset[2]/span/div/div[2]/div/input')
    beg.send_keys(debut)
    #Ecrire heure de fin
    end = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[1]/div/div/div[2]/div/fieldset[2]/span/span/div/div[2]/div/input')
    end.send_keys(fin)
    #Clic vers l'autre page 
    next1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/button[2]')
    next1.click()
    time.sleep(3)
    # A partir d'ici, seconde page 
    add1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/button')
    add1.click()

    add2 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/div[2]/ul/li[1]/button')
    add2.click()

    tarif1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[3]/div/div/div[1]/div/div[1]/div[1]/div[2]/div/input')
    tarif1.send_keys("Payant")

    tarif2 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[3]/div/div/div[1]/div/div[2]/fieldset/div[2]/div[2]/div/input')
    tarif2.send_keys(prix)

    tarif3 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[3]/div/div/div[2]/button[2]')
    tarif3.click()

    time.sleep(2)

    tarif5 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[2]/button')
    tarif5.click()

    time.sleep(2)

    info1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/button')
    info1.click()

    time.sleep(1)

    info2 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[4]/div/div/div[1]/span/div[1]/div/div[2]/div/input')
    info2.send_keys("Téléphone")

    select_element1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[4]/div/div/div[1]/span/div[2]/div/div/div[2]/select')
    info3 = Select(select_element1)
    info3.select_by_visible_text("Téléphone")

    info4 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[1]/div[4]/div/div/div[2]/button[2]')
    info4.click()

    time.sleep(1)

    info5 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[2]/button')
    info5.click()

    time.sleep(2)

    desc = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div/div[2]/div/textarea')
    desc.send_keys(description)
    #Activer couleur personnalisée
    couleur1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[3]/div/label')
    couleur1.click()
    #Choix couleur
    couleur2 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[3]/div[2]/div[5]/label')
    couleur2.click()
    #Activer bannière
    banner1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[4]/div/label')
    banner1.click() 
    time.sleep(1)
    #Importer banniere
    banner2 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[4]/div[2]/div/div/input')
    banner2.send_keys('C:/Users/xx/Downloads/banniere.png')

    vignette1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[5]/div/label')
    vignette1.click()
    time.sleep(1)
    vignette2 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[5]/div[2]/div/div/input')
    vignette2.send_keys('C:/Users/xx/Downloads/vignette.png')

    message1 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[6]/div/label')
    message1.click()

    emoji = "\u267B"
    message2 = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[1]/div/div[6]/div[2]/div[2]/div/textarea')
    message2.send_keys(f"Merci pour votre réservation !\nÀ bientôt chez Altrimenti {emoji}")

    valider = var_driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/main/div/div[2]/div[2]/div[2]/button')
    valider.click()
    time.sleep(1)


def main():
    temps_debut = time.time() 
    titre, nom_lieu, adresse, debut, fin, description, prix, liste_jours, num_days = inputs()
    #####################################  Instance Driver  ###############################################
    occurence=0
    driver = webdriver.Chrome()
    driver.set_window_position(0, 0)
    driver.set_window_size(700, 700)
    driver.get("https://www.helloasso.com/associations/association-altrimenti")
    ##################################### Login et Création ###############################################
    login(driver)
    for i in range(int(num_days)):

        date_jour = int(liste_jours[i][:2])
        date_mois = liste_jours[i][3:5]
        mois = {"01": "Janvier","02": "Février","03": "Mars","04": "Avril","05": "Mai","06": "Juin","07": "Juillet","08": "Août","09": "Septembre","10": "Octobre","11": "Novembre","12": "Décembre"}
        date_mois = mois.get(date_mois)
        name = f"{date_jour} {date_mois} / {titre}"
        driver.get("https://admin.helloasso.com/association-altrimenti/evenements/creation")
        time.sleep(2)
        actions(driver, name, nom_lieu, adresse, debut, fin, description, prix, liste_jours, num_days, i)
        occurence += 1
        time.sleep(2)
    driver.quit()
    temps_fin = time.time()
    duree = temps_fin - temps_debut
    print(f"{duree}secondes")
main()
