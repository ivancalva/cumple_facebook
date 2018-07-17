from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import random
import requests
import sys
import time

mensajes_neutros = ["Feliz Cumpleaños {}, espero te lo pases muy bien", "Que estes pasando un feliz cumpleaños {}!"]
mensajes_hombre = ["Feliz Cumpleaños {}"]
mensajes_mujeres = ["Feliz cumpleaños {}, espero te la pases muy bien!", "Felicidades {}, que estes pasando un lindo dia!", "Feliz cumpleaños {}, te mando un abrazo."]

def revisar_sexo(nombre):
    try:
        res = json.loads(requests.get("https://api.genderize.io/", {'name': nombre}).text)
        prob = res['probability']
        if prob < 0.90:
            return 'neutro'
        return res['gender']
    except:
        return 'neutro'


def felicitar_amigos():
    driver = webdriver.Edge("C:/Users/luis.calva/Documents/Code/Python/Selenium/MicrosoftWebDriver.exe")
    try:
        print("Comenzando")
        driver.get("http://www.facebook.com")
        assert "Facebook" in driver.title
        driver.get('https://www.facebook.com/events/birthdays')
        list_of_bdays = driver.find_elements_by_xpath("//div[@class='_4-u2 _tzh _fbBirthdays__todayCard _4-u8']//div[@class='_4-u3']//ul[@class='_tzl']//li")
        if list_of_bdays is not None:
            sent_messages = []
            for bday in list_of_bdays:
                fields = bday.text.split('\n')
                name = fields[1].split(' ', 1)[0]
                sexo = revisar_sexo(name)
                if(sexo == 'female'):
                    mensaje = random.choice(mensajes_mujeres).format(name)
                elif(sexo == 'male'):
                    mensaje = random.choice(mensajes_hombre).format(name)
                else:
                    mensaje = random.choice(mensajes_neutros).format(name)
                try:
                    text_area = bday.find_element_by_xpath('.//textarea')
                    if text_area is not None:
                        text_area.send_keys(mensaje)
                        text_area.send_keys(Keys.ENTER)
                        time.sleep(1)
                        sent_messages.append(fields[1])
                except:
                    print(sys.exc_info()[0])
                    continue
            print("Termino " + str(len(sent_messages)) + " mensajes enviados")
            for name in sent_messages:
                print(name)
        else:
            print("No hay cumpleaños hoy")
    finally:
        driver.close()

    
felicitar_amigos()