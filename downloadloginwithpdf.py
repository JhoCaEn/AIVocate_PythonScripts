from playwright.sync_api import Playwright, sync_playwright, expect
import openai
import os
import PyPDF2
import random
import string
from google.cloud import storage
from io import BytesIO
import requests
import firebase_admin
# from firebase_admin import firestore
from google.cloud import firestore

def access_to_case(page):
    try:
        page.goto("https://oficinajudicialvirtual.pjud.cl/home/index.php")
        page.get_by_role("button", name="Todos los servicios").click()
        page.get_by_role("button", name="Todos los servicios").click()
        page.locator("#myDropdown").get_by_role("link", name="Clave Única").click()
        page.get_by_label("Ingresa tu RUN").click()
        page.get_by_label("Ingresa tu RUN").fill("13.597.575-3")
        page.get_by_label("Ingresa tu ClaveÚnica").fill("Bularz113!")
        page.get_by_label("Ingresa", exact=True).click()
    #    page.goto("https://oficinajudicialvirtual.pjud.cl/indexN.php")
        page.get_by_role("link", name="Mis Causas").click()
        page.get_by_role("row", name="1842-2015 SOCIEDAD DE SERVICIOS DE ALIMENTACION S A/JUNTA NACIONAL DE AUXILIO ESCOLAR Y BECAS 04/02/2015 Fallada Corte Suprema").get_by_role("link").click()
        return True
    except Exception:
        return False

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, timeout=10000)
    context = browser.new_context()
    page = context.new_page()
    accessed = access_to_case(page)
    while(accessed == False):
        accessed = access_to_case(page)
#    with page.expect_popup() as page1_info:
#        page.get_by_role("row", name="2015 04/02/2015 Otro Tramite CERTIFICADO DE INGRESO Unidad Ingreso Bloqueado").get_by_role("link").click()
#    page1 = page1_info.value

# implementacion de descarga de un pop up
    with page.expect_popup() as page1_info:
        new_page = context.expect_page()
        page.locator('#contenedorEbook').get_by_role("link").click()
#        page.get_by_role("link", name="Descargar Certificado").click()
        new_page = context.wait_for_event("page")
        pdf_url = new_page.url
        print(pdf_url)
        response = requests.get(pdf_url)
#        storage_client = storage.Client()
#        bucket = storage_client.bucket('projectonepdflawyers')
#        blob = bucket.blob("test_downloadpdf.pdf") 
#        blob.upload_from_file(response.content,rewind=True)
        with open('output.pdf', 'wb') as f:
            f.write(response.content)

#codigo para subitlo al bukcet
#        storage_client = storage.Client()
#        bucket = storage_client.bucket('projectonepdflawyers')
#        blob = bucket.blob(file_aux.filename) //esto puede tener un string con cualquier nombre
#        blob.upload_from_file(file_aux,rewind=True)


    #closing the enviroment
    new_page.close()
    page.close()
    # ---------------------
    context.close()
    browser.close()



def main():
    with sync_playwright() as p:
        run(p)

if __name__ == "__main__":
    main()
