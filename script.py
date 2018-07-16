from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import random
import requests

mensajes = ["Feliz Cumpleaños", "Lindo dia", "Que la pases muy bien", "Etc"]

def revisar_sexo(nombre):
    res = json.loads(requests.get("https://api.genderize.io/", {'name': nombre.split(' ', 1)[0]}).text)
    prob = res['probability']
    if prob < 0.90:
        return 'neutro'
    return res['gender']

try:
    print("Comenzando")
    driver = webdriver.Edge()
    driver.get("http://www.facebook.com")
    assert "Facebook" in driver.title
    driver.get('https://www.facebook.com/events/birthdays')
    list_of_bdays = driver.find_elements_by_xpath("//div[@class='_4-u2 _tzh _fbBirthdays__todayCard _4-u8']//div[@class='_4-u3']//ul[@class='_tzl']//li")
    if list_of_bdays is not None:
        sent_messages = []
        for bday in list_of_bdays:
            fields = bday.text.split('\n')
            name = fields[1]
            sexo = revisar_sexo(name)
            mensaje = random.choice(mensajes)
            try:
                text_area = bday.find_element_by_xpath('.//textarea')
                if text_area is not None:
                    text_area.send_keys("Feliz Cumpleaños")
                    text_area.send_keys(Keys.ENTER)
                    sent_messages.append(name)
            except:
                continue
        print("Termino " + str(len(sent_messages)) + " mensajes enviados")
        for name in sent_messages:
            print(name)
    else:
        print("No hay cumpleaños hoy")
finally:
    driver.close()