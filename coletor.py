from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from tkinter import Tk, Label, Entry, Button, messagebox
from threading import Thread
from openpyxl import Workbook
from selenium.webdriver.chrome.service import Service

def start_job_search():
    search_query = job_entry.get()
    location_query = location_entry.get()

    if not search_query or not location_query:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showerror("Erro", "Por favor, preencha seu e-mail e senha.")
        return

    loading_screen()
    Thread(target=job_search, args=(search_query, location_query, email, password)).start()

def loading_screen():
    loading_window = Tk()
    loading_window.title("Carregando...")
    loading_label = Label(loading_window, text="Buscando vagas, por favor aguarde...")
    loading_label.pack(pady=20)
    loading_window.after(15001, loading_window.destroy)  # Fechar a tela de loading após 5 segundos
    loading_window.mainloop()

def job_search(search_query, location_query, email, password):
    print("Abrindo o navegador...")
    service = Service('C:/Users/wende/AppData/Local/Programs/Python/Python312/chrome-win64/chrome.exe')

    # Configure as opções do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # Executar o navegador em modo oculto

    # Inicialize o driver do Chrome
    print("Inicializando o navegador...")
    browser = webdriver.Chrome(service=service, options=options)
    print("Navegador inicializado.")

    print("Acessando o LinkedIn...")
    browser.get("https://www.linkedin.com/")
    sleep(5)
    email_field = browser.find_element(By.XPATH, "//*[@id='session_key']")
    password_field = browser.find_element(By.XPATH, "//*[@id='session_password']")
    login_button = browser.find_element(By.XPATH, "//*[@id='main-content']/section[1]/div/div/form/div[2]/button")
    sleep(2)
    print("Realizando login...")
    email_field.send_keys(email)
    password_field.send_keys(password)
    sleep(2)
    login_button.click()
    sleep(4)

    print("Acessando a página de vagas...")
    browser.get("https://www.linkedin.com/jobs")
    input_jobs_search = browser.find_element(By.XPATH, "//header//input")
    sleep(2)
    print("Realizando busca de vagas...")
    input_jobs_search.send_keys(f"{search_query}, {location_query}")
    sleep(2)
    input_jobs_search.send_keys(Keys.ENTER)
    sleep(5)

    ul_element = browser.find_element(By.CSS_SELECTOR, "main div.jobs-search-results-list")
    sleep(2)

    def scroll_list(pixels):
        browser.execute_script(f"arguments[0].scrollTop+={pixels};", ul_element)
        sleep(2)

    links = []

    for _ in range(25):
        scroll_list(200)
        links = browser.find_elements(By.XPATH, "//main//div//div//ul//li//a[@data-control-id]")
        print(len(links))
        if len(links) >= 25:
            print(f"Chegamos ao número esperado de {len(links)}")
            break

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

    spreadsheet.save(f"Vagas_links_{search_query}_{location_query}.xlsx")
    print("Planilha criada")
    browser.quit()

# Configuração da interface gráfica
root = Tk()
root.title("Busca de Vagas")

email_label = Label(root, text="E-mail:")
email_label.grid(row=0, column=0, padx=10, pady=5)
email_entry = Entry(root)
email_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = Label(root, text="Senha:")
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

job_label = Label(root, text="Vaga:")
job_label.grid(row=2, column=0, padx=10, pady=5)
job_entry = Entry(root)
job_entry.grid(row=2, column=1, padx=10, pady=5)

location_label = Label(root, text="Localização:")
location_label.grid(row=3, column=0, padx=10, pady=5)
location_entry = Entry(root)
location_entry.grid(row=3, column=1, padx=10, pady=5)

search_button = Button(root, text="Buscar", command=start_job_search)
search_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

root.mainloop()
