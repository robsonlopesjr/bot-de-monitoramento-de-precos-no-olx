from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import os


def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1920,1080', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver


driver = iniciar_driver()
url = ''
driver.get(url)
sleep(3)

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)

    titulos = driver.find_elements(
        By.XPATH, '//div[@class="sc-12rk7z2-7 kDVQFY"]//h2')

    precos = driver.find_elements(
        By.XPATH, '//div[@class="sc-1kn4z61-1 dGMPPn"]//span')

    links = driver.find_elements(
        By.XPATH, '//a[@data-lurker-detail="list_id"]')

    for titulo, preco, link in zip(titulos, precos, links):
        with open('precos.csv', 'a', encoding='utf-8', newline='') as arquivo:
            link_processado = link.get_attribute('href')
            arquivo.write(
                f'{titulo.text};{preco.text};{link_processado}{os.linesep}')

    try:
        botao_proxima_pagina = driver.find_element(
            By.XPATH, '//span[text()="Próxima página"]')
        sleep(2)
        botao_proxima_pagina.click()
    except Exception:
        print('Chegou na última página')
        break


input('')
driver.close()
