from playwright.sync_api import sync_playwright
import re
import time
import os
import requests
def run(playwright):
    browser = playwright.chromium.launch(headless = False)
    context = browser.new_context()

    page = context.new_page()


    page.goto("https://oficinajudicialvirtual.pjud.cl/home/index.php")
    page.get_by_role("button", name="Consulta causas").click()
    page.get_by_role("link", name="Búsqueda por Fecha").click()
    page.locator(".input-group-addon").first.click()
    page.get_by_role("link", name="1", exact=True).click()
    page.locator(".input-group-addon").nth(1).click()
   
    page.get_by_role("link", name="23", exact=True).click()
    page.select_option('#fecCompetencia', '3')
    page.locator("//body/div[8]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[1]/div[1]/div[2]/div[3]/div[1]/form[1]/div[2]/div[1]/div[2]/div[1]/button[1]").click()
    page.click("[data-original-index='2']")
#    page.locator("#formConsultaFec i").nth(1).click()
#    page.pause()
    page.get_by_role("button", name="Buscar").click()
    rows = page.query_selector_all("table#dtaTableDetalleFecha tr")

    page.locator("//body[1]/div[8]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[1]/div[1]/div[2]/div[3]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]").click()

    with page.expect_popup() as page1_info:
        new_page = context.expect_page()
        page.get_by_role("link", name="Descargar Certificado").click()
        new_page = context.wait_for_event("page")
        pdf_url = new_page.url
        print(pdf_url)
        response = requests.get(pdf_url)
        with open('output.pdf', 'wb') as f:
            f.write(response.content)

    #closing the enviroment
    new_page.close()
    page.close()
    context.close()
    browser.close()

def run2(playwright):
    browser = playwright.chromium.launch(headless = False)
    context = browser.new_context()

    page = context.new_page()


    page.goto("https://oficinajudicialvirtual.pjud.cl/home/index.php")
    page.get_by_role("button", name="Consulta causas").click()
    page.get_by_role("link", name="Búsqueda por RIT").click()
    page.select_option('#competencia', '3')
    page.select_option('#conCorte', '15')
#    page.select_option('#competencia', '3')
    page.select_option('#conTipoCausa','C')
    page.locator('#conRolCausa').fill('1')
    page.locator('#conEraCausa').fill('2023')
    
    page.get_by_role("button", name="Buscar").click()
    page.locator('//tbody/tr[1]/td[1]/a[1]/i[1]').click()

    time.sleep(4)
#    rows = page.query_selector_all("table#dtaTableDetalleFecha tr")

#    page.locator("//body[1]/div[8]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[1]/div[1]/div[2]/div[3]/div[4]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]").click()

    with page.expect_popup() as page1_info:
        new_page = context.expect_page()
        page.get_by_role("link", name="Descargar Certificado").click()
        new_page = context.wait_for_event("page")
        pdf_url = new_page.url
        print(pdf_url)
        response = requests.get(pdf_url)
        with open('output.pdf', 'wb') as f:
            f.write(response.content)

    #closing the enviroment
    new_page.close()
    page.close()
    context.close()
    browser.close()



def main():
    with sync_playwright() as p:
#        run(p)
        run2(p)


if __name__ == "__main__":
    main()
