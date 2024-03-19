#IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS 

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook


print("Irei começar a busca pelas vagas")
search = input("Digite a vaga que deseja, acrescente uma virugula após a vaga deseja e coloque a cidade onde deseja buscar: \n")

# FUNÇÃO DE BUSCAR O ARQUIVO

def read_credentials(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

        cred = {}
        for line in lines:
            key, value = line.strip().split(":")
            cred[key] = value
        return cred

file_path_cred = "cred.txt"

cred = read_credentials(file_path_cred)


#FUNÇÃO QUE IRÁ LOCALIZAR ONDE DEVERÁ SER CLICADO E INSERIDO OS DADOS

browser = webdriver.Chrome()
browser.get("https://www.linkedin.com/")
sleep(5)
email = browser.find_element(By.XPATH, "//*[@id='session_key']")
password = browser.find_element(By.XPATH, "//*[@id='session_password']")
btn_enter = browser.find_element(By.XPATH, "//*[@id='main-content']/section[1]/div/div/form/div[2]/button")

sleep(2)


email.send_keys(cred['user'])
password.send_keys(cred['senha'])

sleep(4)
btn_enter.click()
sleep(4)
browser.get("https://www.linkedin.com/jobs")
input_jobs_search = browser.find_element(By.XPATH, "//header//input")
sleep(4)
input_jobs_search.send_keys(search)
sleep(4)
input_jobs_search.send_keys(Keys.ENTER)
sleep(5)

#Fim da função de inserção de dados

ul_element = browser.find_element(By.CSS_SELECTOR, "main div.jobs-search-results-list")
sleep(4)

#Início da função de rolar o scroll

def scroll_list(pixels):
    browser.execute_script(f"arguments[0].scrollTop+={pixels};", ul_element)
    sleep(2)

links = []

for _ in range(25):
    scroll_list(200)
    links = browser.find_elements(By.XPATH,"//main//div//div//ul//li//a[@data-control-id]")
    print(len(links))
    if len(links) >=25:
        print(f"Chegamos ao número esperado de {len(links)}")
        break

#Fim da função de rolar o scroll
    

#Início do código para armazenamento das informações coletadas 

spreadsheet = Workbook()

sheet = spreadsheet.active

sheet['A1'] = "NOME DA VAGA"
sheet['B1'] = "LINK DA VAGA"

next_line = sheet.max_row + 1

for link in links:
    text = link.text
    url_link = link.get_attribute("href")

    sheet[f'A{next_line}'] = text
    sheet[f'B{next_line}'] = url_link

    next_line += 1

spreadsheet.save("Vagas_links" + search + ".xlsx")
print("Planilha craida")
print("Encerrando Busca")
sleep(5)
browser.quit

#Fim da coleta de informações e armazenadas em um arquivo excel.