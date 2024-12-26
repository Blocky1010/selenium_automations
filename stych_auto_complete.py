from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests
import os
import json

chrome_options = Options()


user_home = os.path.expanduser('~')
chrome_options.add_argument(f'--user-data-dir={user_home}/Library/Application Support/Google/Chrome')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=chrome_options)
print("Chrome démarré")

liste_competences = [["1","1"],["2","43"],["3","78"], ["4","106"]]

def repeater(path, action, keys=None):
    element = driver.find_element(By.XPATH, path)
    if action == 0:
        element.click()
    elif action == 1 and keys is not None:
        element.send_keys(keys)

def get_question_type(driver):
    try:
        qst_grid = driver.find_element(By.CSS_SELECTOR, '.qst_grid')
        reponses = qst_grid.find_elements(By.CSS_SELECTOR, '.questionnaire_test_reponse')
        type_questions = len(reponses)
        return type_questions
        
    except Exception as e:
        return 0
def element_exists_and_click(driver, selector, timeout=2):

    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        if element.is_displayed():
            element.click()
            return True
        else:
            return False
    except:
        return False

try:
    #Connexion
    # driver.get('https://www.stych.fr/elearning/formation/conduite/formation')
    # repeater('/html/body/div[2]/div[1]/div/form/div[2]/input', 1, "YOUREMAIL")
    # repeater('/html/body/div[2]/div[1]/div/form/div[3]/div[1]/input', 1, "YOURPASSW")
    # repeater('/html/body/div[2]/div[1]/div/form/div[3]/div[3]/div[2]/div/label', 0)
    # repeater('/html/body/div[2]/div[1]/div/form/div[3]/input', 0)

    cookie_counter = 0
    cookie_counter_1 = 0

    driver.get("https://www.stych.fr/connexion")
    time.sleep(30)

    #compétences ( Totale = 4 )
    for z in range(4):
        driver.get("https://www.stych.fr/elearning/formation/conduite/")

        cookies = driver.get_cookies()
        phpsessid_cookie = next((cookie for cookie in cookies if cookie['name'] == 'PHPSESSID'), None)
        if phpsessid_cookie:
            print(f"Cookie: {phpsessid_cookie['name']}, Value: {phpsessid_cookie['value']}")

        # aller sur x compétence ( Totale = 4 )
        driver.get(f"https://www.stych.fr/elearning/formation/conduite/topics/{liste_competences[z][1]}")
        
        time.sleep(2)

        elements = driver.find_elements(By.CSS_SELECTOR, '.list-item.row')
        count = len(elements)
        print(f"Nombre sous compétences: {count}")

        links = driver.find_elements(By.XPATH, "//div[@class='card-body list']//a[@class='item-title']")
        result = []
        for link in links:
            url = link.get_attribute('href')
            text = link.text
            result.append(url)
        # print(result)

        #sous-compétences
        for i in range(count):

            driver.get(result[i])

            videos = driver.find_elements(By.CSS_SELECTOR, 'a.venobox-vimeo.vbox-item')
            fiches = driver.find_elements(By.CSS_SELECTOR, 'div.list-item.d-flex')
            evaluation = driver.find_elements(By.CSS_SELECTOR, 'div.card-image.w-40')
            print(f"{len(videos)} video(s), {len(fiches)} fiche(s) et {len(evaluation)} évaluation(s) dans cette section")

            if len(videos) != 0:
                for a in range(len(videos)):
                    driver.get(result[i])
                    time.sleep(2)

                    cookies = driver.get_cookies()
                    phpsessid_cookie = next((cookie for cookie in cookies if cookie['name'] == 'PHPSESSID'), None)
                    if phpsessid_cookie:
                        print(f"Cookie: {phpsessid_cookie['name']}, Value: {phpsessid_cookie['value']}")
                    
                    #clic dans la vidéo

                    repeater(f'/html/body/div[1]/div/div/main/div/div[2]/div/div/div[1]/div[2]/div/div/div/div[2]/div[{a+1}]/div[2]/a',0)
                    time.sleep(2)

                    play = driver.find_element(By.CSS_SELECTOR, '.plyr__control.plyr__control--overlaid')
                    play.click()

                    time.sleep(2)

                    progress_bar = driver.find_element(By.CSS_SELECTOR, 'input[data-plyr="seek"]')

                    #skip la video
                    for b in range(9):
                        driver.execute_script(f"arguments[0].value = {b*10+1}", progress_bar)
                        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }))", progress_bar)
                        time.sleep(0.2)

                    driver.execute_script(f"arguments[0].value = 99", progress_bar)
                    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }))", progress_bar)

                    time.sleep(5)

                    if element_exists_and_click(driver, ".btn.btn-secondary.btn-do-video-qcm.px-lg-5.mb-5"):
                        # print("Bouton trouvé et cliqué, on continue")

                        #demarrer le test
                        repeater('/html/body/div[3]/div/div/div/div/div[1]/div[2]/div[2]', 0)
                        time.sleep(7)
                        repeater('/html/body/div[3]/div/div/div/div/section/div/div/div[3]/div/div[2]/a', 0)
                        time.sleep(2)
                        
                        id_qst = driver.execute_script("return id_qst;")
                        # print(f"ID Question: {id_qst}")

                        final_list = []

                        #récup les réponses aux questions
                        for d in range(5):

                            coo = {
                                "PHPSESSID": f"{phpsessid_cookie['value']}",
                            }
                            headrs = {
                                'accept': 'application/json, text/javascript, */*; q=0.01',
                                'accept-language': 'en-GB,en;q=0.9',
                                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'origin': 'https://www.stych.fr',
                                'priority': 'u=1, i',
                                'referer': 'https://www.stych.fr/elearning/formation-test-code/test-video/2/125/5',
                                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                                'sec-ch-ua-mobile': '?0',
                                'sec-ch-ua-platform': '"macOS"',
                                'sec-fetch-dest': 'empty',
                                'sec-fetch-mode': 'cors',
                                'sec-fetch-site': 'same-origin',
                                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                                'x-requested-with': 'XMLHttpRequest',
                            }
                            da = {
                                'id_qst': f'{id_qst}',
                                'count': f'{d}',
                            }
                            response = requests.post(
                                'https://www.stych.fr/elearning/formation-test-code/test-video/2/0/5',
                                cookies=coo,
                                headers=headrs,
                                data=da,
                            )

                            if response.status_code == 200:
                                data = response.json()        
                                qst_array = data.get("qstArray", {})
                                if not qst_array:
                                    print("Warning: qstArray is empty")
                                    continue
                                combined_responses = []
                                
                                for question_id, question_data in qst_array.items():
                                    bonnes = [rep_data["bonne"] for rep_data in question_data["reponse"].values()]
                                    combined_responses.extend(bonnes)

                                if combined_responses:
                                    final_list.append(combined_responses)

                            else:
                                print(f"Request failed with status code: {response.status_code}")
                                print("Response content:", response.text)

                        # print("\nListe finale avec réponses combinées:")
                        # print(final_list)

                        xpaths = {
                            "4_choices": [
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[3]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[4]'
                            ],
                            "4_choices_2x2": [
                                '//*[@id="QST"]/div/div/div[2]/center[1]/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center[1]/div/div/div[2]',
                                '//*[@id="QST"]/div/div/div[2]/center[2]/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center[2]/div/div/div[2]'
                            ],
                            "3_choices": [
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[3]'
                            ],
                            "2_choices": [
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]'
                            ]
                        }
                        for c in range(5):
                            reponses = final_list[c]
                            num_choices = len(reponses)
                            # print(f"\nQuestion {c + 1} avec {num_choices} choix:")

                            # Sélectionner la liste de XPaths appropriée
                            if num_choices == 4:
                                # Vérifier si c'est un layout 2x2 en essayant de trouver un élément spécifique
                                try:
                                    driver.find_element(By.XPATH, '//*[@id="QST"]/div/div/div[2]/center[2]')
                                    current_xpaths = xpaths["4_choices_2x2"]
                                except:
                                    current_xpaths = xpaths["4_choices"]
                            elif num_choices == 3:
                                current_xpaths = xpaths["3_choices"]
                            else:
                                current_xpaths = xpaths["2_choices"]

                            # Trouver tous les index des bonnes réponses (où '1' apparaît)
                            correct_indices = [i for i, reponse in enumerate(reponses) if reponse == '1']
                            
                            if correct_indices:
                                # print(f"Les bonnes réponses sont en position(s): {[i + 1 for i in correct_indices]}")
                                
                                # Cliquer sur chaque bonne réponse
                                for correct_index in correct_indices:
                                    try:
                                        element = driver.find_element(By.XPATH, current_xpaths[correct_index])
                                        element.click()
                                        # print(f"Cliqué sur: {current_xpaths[correct_index]}")
                                        time.sleep(0.5)  # Petit délai entre les clics multiples
                                    except Exception as e:
                                        print(f"Erreur lors du clic sur la position {correct_index + 1}: {e}")
                                
                                # Cliquer sur le bouton suivant après avoir sélectionné toutes les réponses
                                for _ in range(2):
                                    repeater("/html/body/div[3]/div/div/div/div/div[2]/div/div[2]/div[2]",0)
                                    time.sleep(1)
                                time.sleep(1)

                            time.sleep(1)  # Attendre entre chaque question



                        time.sleep(2) 
                    else:
                        time.sleep(2)
                        close_button = driver.find_element(By.CLASS_NAME, 'vbox-close')
                        close_button.click()
            else:
                print("Pas de video, passage aux fiches...")

            if len(fiches) != 0:
                time.sleep(2)

                for g in range(len(fiches)):
                    driver.get(result[i])
                    time.sleep(2)
                    cookies = driver.get_cookies()
                    phpsessid_cookie = next((cookie for cookie in cookies if cookie['name'] == 'PHPSESSID'), None)
                    if phpsessid_cookie:
                        print(f"Cookie: {phpsessid_cookie['name']}, Value: {phpsessid_cookie['value']}")


                    first_fiche = driver.find_element(By.CSS_SELECTOR, f".list-item:nth-child({g+1}) .item-title > a[href*='fiche-cours']")
                    fiche_url = first_fiche.get_attribute('href')
                    first_fiche.click()

                    time.sleep(3)

                    duree_totale = 420
                    duree_actuelle = 0
                    
                    while duree_actuelle < duree_totale:
                        try:
                            # Simuler le scroll
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            
                            # Préparer la requête POST pour enregistrer la durée
                            headers = {
                                'accept': '*/*',
                                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
                                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'origin': 'https://www.stych.fr',
                                'referer': fiche_url,
                                'x-requested-with': 'XMLHttpRequest'
                            }
                            
                            data = {
                                'action': 'recordDureeConsultation',
                                'dureeConsultation': str(duree_actuelle + 5),
                            }
                            
                            # Envoyer la requête
                            response = requests.post(
                                fiche_url,
                                headers=headers,
                                cookies={'PHPSESSID': phpsessid_cookie['value']},
                                data=data
                            )
                            
                            duree_actuelle += 5
                            time.sleep(0.1)  # Attendre 5 secondes avant la prochaine requête
                            
                        except Exception as e:
                            print(f"Erreur lors de l'enregistrement de la durée : {e}")
                            break

                    # Une fois la durée atteinte, enregistrer que l'utilisateur a atteint la fin
                    try:
                        data_end = {
                            'action': 'recordScrollEnd',
                        }
                        
                        response_end = requests.post(
                            fiche_url,
                            headers=headers,
                            cookies={'PHPSESSID': phpsessid_cookie['value']},
                            data=data_end
                        )
                    except Exception as e:
                        print(f"Erreur lors de l'enregistrement de la fin du scroll : {e}")

                    # Mettre à jour visuellement la barre de progression
                    driver.execute_script("$('.progress-bar').css({width: '100%'});")
                    
                    # time.sleep(2)

                    if element_exists_and_click(driver, ".btn.btn-secondary"):
                        time.sleep(2)
                        #démarrer le test
                        repeater('/html/body/div[3]/div/div/div/div/div[1]/div[2]/div[2]', 0)
                        time.sleep(7)
                        repeater('/html/body/div[3]/div/div/div/div/section/div/div/div[3]/div/div[2]/a', 0)
                        time.sleep(3)
                        
                        id_qst = driver.execute_script("return id_qst;")
                        # print(f"ID Question: {id_qst}")

                        final_list = []

                        #récup les réponses aux questions
                        for d in range(5):

                            coo = {
                                "PHPSESSID": f"{phpsessid_cookie['value']}",
                            }
                            headrs = {
                                'accept': 'application/json, text/javascript, */*; q=0.01',
                                'accept-language': 'en-GB,en;q=0.9',
                                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'origin': 'https://www.stych.fr',
                                'priority': 'u=1, i',
                                'referer': 'https://www.stych.fr/elearning/formation-test-code/test-video/2/125/5',
                                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                                'sec-ch-ua-mobile': '?0',
                                'sec-ch-ua-platform': '"macOS"',
                                'sec-fetch-dest': 'empty',
                                'sec-fetch-mode': 'cors',
                                'sec-fetch-site': 'same-origin',
                                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                                'x-requested-with': 'XMLHttpRequest',
                            }
                            da = {
                                'id_qst': f'{id_qst}',
                                'count': f'{d}',
                            }
                            response = requests.post(
                                'https://www.stych.fr/elearning/formation-test-code/test-video/2/0/5',
                                cookies=coo,
                                headers=headrs,
                                data=da,
                            )

                            if response.status_code == 200:
                                data = response.json()        
                                qst_array = data.get("qstArray", {})
                                if not qst_array:
                                    print("Warning: qstArray is empty")
                                    continue
                                combined_responses = []
                                
                                for question_id, question_data in qst_array.items():
                                    bonnes = [rep_data["bonne"] for rep_data in question_data["reponse"].values()]
                                    combined_responses.extend(bonnes)

                                if combined_responses:
                                    final_list.append(combined_responses)

                            else:
                                print(f"Request failed with status code: {response.status_code}")
                                print("Response content:", response.text)

                        # print("\nListe finale avec réponses combinées:")
                        # print(final_list)

                        xpaths = {
                            "4_choices": [
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[3]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[4]'
                            ],
                            "4_choices_2x2": [
                                '//*[@id="QST"]/div/div/div[2]/center[1]/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center[1]/div/div/div[2]',
                                '//*[@id="QST"]/div/div/div[2]/center[2]/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center[2]/div/div/div[2]'
                            ],
                            "3_choices": [
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[3]'
                            ],
                            "2_choices": [
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                                '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]'
                            ]
                        }
                        for c in range(5):
                            reponses = final_list[c]
                            num_choices = len(reponses)
                            # print(f"\nQuestion {c + 1} avec {num_choices} choix:")

                            # Sélectionner la liste de XPaths appropriée
                            if num_choices == 4:
                                # Vérifier si c'est un layout 2x2 en essayant de trouver un élément spécifique
                                try:
                                    driver.find_element(By.XPATH, '//*[@id="QST"]/div/div/div[2]/center[2]')
                                    current_xpaths = xpaths["4_choices_2x2"]
                                except:
                                    current_xpaths = xpaths["4_choices"]
                            elif num_choices == 3:
                                current_xpaths = xpaths["3_choices"]
                            else:
                                current_xpaths = xpaths["2_choices"]

                            # Trouver tous les index des bonnes réponses (où '1' apparaît)
                            correct_indices = [i for i, reponse in enumerate(reponses) if reponse == '1']
                            
                            if correct_indices:
                                # print(f"Les bonnes réponses sont en position(s): {[i + 1 for i in correct_indices]}")
                                
                                # Cliquer sur chaque bonne réponse
                                for correct_index in correct_indices:
                                    try:
                                        element = driver.find_element(By.XPATH, current_xpaths[correct_index])
                                        element.click()
                                        # print(f"Cliqué sur: {current_xpaths[correct_index]}")
                                        time.sleep(0.5)  # Petit délai entre les clics multiples
                                    except Exception as e:
                                        print(f"Erreur lors du clic sur la position {correct_index + 1}: {e}")
                                
                                # Cliquer sur le bouton suivant après avoir sélectionné toutes les réponses
                                for _ in range(2):
                                    repeater("/html/body/div[3]/div/div/div/div/div[2]/div/div[2]/div[2]",0)
                                    time.sleep(1)
                                time.sleep(1)

                            time.sleep(1)  # Attendre entre chaque question
            else:
                print('Pas de fiches, passage à l\'évaluation...')

            if len(evaluation) != 0:
                driver.get(result[i])
                time.sleep(2)
                cookies = driver.get_cookies()
                phpsessid_cookie = next((cookie for cookie in cookies if cookie['name'] == 'PHPSESSID'), None)
                if phpsessid_cookie:
                    print(f"Cookie: {phpsessid_cookie['name']}, Value: {phpsessid_cookie['value']}")

                # print(len(evaluation), "évaluation")
                if element_exists_and_click(driver, ".btn.btn-secondary"):
                    time.sleep(2)
                    #démarrer le test
                    repeater('/html/body/div[3]/div/div/div/div/div[1]/div[2]/div[2]', 0)
                    time.sleep(7)
                    repeater('/html/body/div[3]/div/div/div/div/section/div/div/div[3]/div/div[2]/a', 0)
                    time.sleep(3)
                    
                    id_qst = driver.execute_script("return id_qst;")
                    # print(f"ID Question: {id_qst}")

                    final_list = []

                    #récup les réponses aux questions
                    for d in range(10):

                        coo = {
                            "PHPSESSID": f"{phpsessid_cookie['value']}",
                        }
                        headrs = {
                            'accept': 'application/json, text/javascript, */*; q=0.01',
                            'accept-language': 'en-GB,en;q=0.9',
                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'origin': 'https://www.stych.fr',
                            'priority': 'u=1, i',
                            'referer': 'https://www.stych.fr/elearning/formation-test-code/test-video/2/10/10',
                            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"macOS"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                            'x-requested-with': 'XMLHttpRequest',
                        }
                        da = {
                            'id_qst': f'{id_qst}',
                            'count': f'{d}',
                        }
                        response = requests.post(
                            'https://www.stych.fr/elearning/formation-test-code/test-video/2/10/10',
                            cookies=coo,
                            headers=headrs,
                            data=da,
                        )

                        if response.status_code == 200:
                            data = response.json()        
                            qst_array = data.get("qstArray", {})
                            if not qst_array:
                                print("Warning: qstArray is empty")
                                continue
                            combined_responses = []
                            
                            for question_id, question_data in qst_array.items():
                                bonnes = [rep_data["bonne"] for rep_data in question_data["reponse"].values()]
                                combined_responses.extend(bonnes)

                            if combined_responses:
                                final_list.append(combined_responses)

                        else:
                            print(f"Request failed with status code: {response.status_code}")
                            print("Response content:", response.text)

                    # print("\nListe finale avec réponses combinées:")
                    # print(final_list)

                    xpaths = {
                        "4_choices": [
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]',
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[3]',
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[4]'
                        ],
                        "4_choices_2x2": [
                            '//*[@id="QST"]/div/div/div[2]/center[1]/div/div/div[1]',
                            '//*[@id="QST"]/div/div/div[2]/center[1]/div/div/div[2]',
                            '//*[@id="QST"]/div/div/div[2]/center[2]/div/div/div[1]',
                            '//*[@id="QST"]/div/div/div[2]/center[2]/div/div/div[2]'
                        ],
                        "3_choices": [
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]',
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[3]'
                        ],
                        "2_choices": [
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[1]',
                            '//*[@id="QST"]/div/div/div[2]/center/div/div/div[2]'
                        ]
                    }

                    for c in range(10):
                        reponses = final_list[c]
                        num_choices = len(reponses)
                        # print(f"\nQuestion {c + 1} avec {num_choices} choix:")

                        # Sélectionner la liste de XPaths appropriée
                        if num_choices == 4:
                            # Vérifier si c'est un layout 2x2 en essayant de trouver un élément spécifique
                            try:
                                driver.find_element(By.XPATH, '//*[@id="QST"]/div/div/div[2]/center[2]')
                                current_xpaths = xpaths["4_choices_2x2"]
                            except:
                                current_xpaths = xpaths["4_choices"]
                        elif num_choices == 3:
                            current_xpaths = xpaths["3_choices"]
                        else:
                            current_xpaths = xpaths["2_choices"]

                        # Trouver tous les index des bonnes réponses (où '1' apparaît)
                        correct_indices = [i for i, reponse in enumerate(reponses) if reponse == '1']
                        
                        if correct_indices:
                            # print(f"Les bonnes réponses sont en position(s): {[i + 1 for i in correct_indices]}")
                            
                            # Cliquer sur chaque bonne réponse
                            for correct_index in correct_indices:
                                try:
                                    element = driver.find_element(By.XPATH, current_xpaths[correct_index])
                                    element.click()
                                    # print(f"Cliqué sur: {current_xpaths[correct_index]}")
                                    time.sleep(0.5)  # Petit délai entre les clics multiples
                                except Exception as e:
                                    print(f"Erreur lors du clic sur la position {correct_index + 1}: {e}")
                            
                            # Cliquer sur le bouton suivant après avoir sélectionné toutes les réponses
                            for _ in range(2):
                                repeater("/html/body/div[3]/div/div/div/div/div[2]/div/div[2]/div[2]",0)
                                time.sleep(1)
                            time.sleep(1)

                        time.sleep(1)  # Attendre entre chaque question
            else:
                print("Pas d'évaluation.")

finally:
    driver.quit()
