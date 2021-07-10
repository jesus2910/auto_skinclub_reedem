from os import system
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException

url = ["https://skin.club/login", "https://skin.club/es/cases/free-case", "https://skin.club/es/cases/premium-case"]


def login_steam(driver):

    form = driver.find_element_by_id("loginForm")
    username = form.find_element_by_name("username")
    password = form.find_element_by_name("password")
    username.send_keys(input("Usuario: "))
    password.send_keys(input("Password: "))
    system("cls")
    driver.find_element_by_class_name("btn_green_white_innerfade").click()


def code_steam_security(driver):
    code_type = None
    while code_type != "S" and code_type != "C":

        code_type = input("Que tipo de codigo tienes ? [Smartphone[S] | Mail[M]]").upper()

        if code_type == "S":
            code_user = input("Introduce el codigo: ").upper()
            form_steam = driver.find_element_by_class_name("newmodal_content")
            code = form_steam.find_element_by_class_name("twofactorauthcode_entry_input")
            code.send_keys(code_user + Keys.ENTER)
            break

        elif code_type == "C":
            code_user = input("Introduce el codigo: ").upper()
            form_steam = driver.find_element_by_class_name("newmodal_content")
            code = form_steam.find_element_by_id("authcode")
            code.send_keys(code_user + Keys.ENTER)
            break


def redeem_loop(driver):

    is_button_loaded = False
    button = None
    while not is_button_loaded:
        try:
            button = driver.find_element_by_class_name("take-part__link")
            is_button_loaded = True
        except NoSuchElementException:
            print("Pues no esta el boton")
            sleep(30)

    button_enabled = driver.find_element_by_class_name("take-part__link").is_enabled()
    while True:
        while not button_enabled:
            print("AUN NO ESTA DISPONIBLE")
            sleep(1800)
            driver.refresh()
            button_enabled = driver.find_element_by_class_name("take-part__link").is_enabled()

        driver.find_element_by_class_name("take-part__link").click()
        print("HAS PARTICIPADO EN EL SORTEO.")
        sleep(60)
        driver.refresh()
        button_enabled = driver.find_element_by_class_name("take-part__link").is_enabled()


def main():

    # Inicia el navegador, lo maximiza y lo manda a la primera url
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url[0])

    # Rellena el formulario de login de Steam con ayuda del usuario.
    login_steam(driver)

    # Rellena el 2nd Factor de Steam con ayuda del usuario.
    code_steam_security(driver)

    # Acepta las cookies para que sea visible el boton de participar posteriormente y no de error
    sleep(10)
    driver.find_element_by_class_name("accept-cookies").click()

    # Abre una nueva pestaña con la url de la caja gratis.
    sleep(10)
    driver.execute_script("window.open('" + url[1] + "', 'new_window')")

    # Pone en el punto de observacion la nueva pestaña.
    sleep(10)
    driver.switch_to.window(driver.window_handles[1])

    # Comprueba que el boton de Participar este cargado y identifica si esta desactivado
    redeem_loop(driver)



if __name__ == "__main__":
    main()
