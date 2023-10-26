from playwright.sync_api import Playwright, sync_playwright, expect
from flask import Flask, request, jsonify
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
        page.locator("#myDropdown").get_by_role("link", name="Clave Única").click()
        page.get_by_label("Ingresa tu RUN").click()
        page.get_by_label("Ingresa tu RUN").fill("13.597.575-3")
        page.get_by_label("Ingresa tu ClaveÚnica").click()
        page.get_by_label("Ingresa tu ClaveÚnica").fill("Bularz113!")
        page.get_by_label("Ingresa", exact=True).click()
        return True
    except Exception:
        return False
def first_step(page1):
    try:
        page1.get_by_text("13.597.575-3").click()
        page1.get_by_text("Ingresar Demanda/Recurso").click()
        page1.locator(
            '''select[data-bind="options: competencias, optionsText: 'nombre', optionsCaption: 'Seleccione Competencia', value : competencia"]''').select_option('Garantia') 
        page1.locator("#s2id_select-asientoCorte").click()#Corte
        page1.get_by_text('C.A. de Santiago.').click()
        page1.locator("#s2id_select-tribunales").click()#Tribunal
        page1.get_by_text('5º Juzgado de Garantía de Santiago').click()
        return True
    except Exception:
        return False
def second_step(page1):
    try:
        page1.get_by_text('Seleccione Procedimiento').click()
        page1.get_by_text('Ordinario').click()

        page1.get_by_text('Seleccione Forma Inicio').click()
        page1.get_by_text('Querella').click()

        page1.locator("xpath=////div[@class='d-none d-sm-block col-sm-3 col-lg-2']//div[@class='form-group']//input[@type='text']").fill("538")
        page1.get_by_text("Agregar").click()
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
#    page.goto("https://oficinajudicialvirtual.pjud.cl/indexN.php")
#   ajustar  a pagina con token que genral
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Ing. Demandas y Escritos").click()
    page1 = page1_info.value

    #recuadro uno ingreso demanda y recursos
    accessed = first_step(page1)
    while(accessed == False):
        print("first step")
        accessed = first_step(page1)

    #recuadro dos ingreso demanda
    accessed = second_step(page1)
    while(accessed == False):
        print("second step")
        accessed = second_step(page1)

    # ---------------------
    # litigantes QTE
    page1.locator('#s2id_autogen151').click()
    page1.locator('#select2-result-label-164').click()

    page1.get_by_tittle("Este campo es obligatorio").fill("150512077")
    page1.keyboard.press("Enter")

    page1.get_by_text("Agregar Litigante").click()

    # querellado QDo contra quier resulter responsables
    page1.get_by_text(" Contra quienes resulten responsables").click()
    page1.locator('#select2-chosen-152').click()
    page1.locator('#select2-result-label-177').click()
    page1.get_by_text("Agregar Litigante").click()

    # agregar abogadado ABO
    page1.locator('#s2id_autogen151').click()
    page1.locator('#select2-result-label-179').click()

    page1.get_by_tittle("Este campo es obligatorio").fill("135975753")
    page1.keyboard.press("Enter")
    page1.get_by_text("Agregar Litigante").click()

    page1.get_by_text(" Ingresar").click()
    # ----------------
    # Subir documento se debe usar with para el popou

    with page1.expect_popup() as page1_info:
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, 'elfile.pdf')
        page.get_by_text('Adjuntar').set_input_files([file_path])
        page.wait_for_timeout(4000)

        page.get_by_text("Cerrar y Continuar").click
    # ---------------
    context.close()
    browser.close()


# try:
with sync_playwright() as playwright:
    run(playwright)

# except Exception:
#    db = firestore.Client()
#    doc_ref = db.collection('deverrorlog').document('testone')
#    doc_ref.update({"isfail":True})
#    doc_ref.update({"numbererroes":firestore.Increment(1)})
