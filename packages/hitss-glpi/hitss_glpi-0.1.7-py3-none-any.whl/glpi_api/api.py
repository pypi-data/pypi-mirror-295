import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class GLPIAPI:
    def __init__(self, base_url, username, password, selenium_url):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.selenium_url = selenium_url  # Hacer que el URL del Selenium Grid sea dinámico
        self.session = requests.Session()
        self.login()

    def login(self):
        login_url = f"{self.base_url}/front/login.php"

        # Configurar Selenium WebDriver para Selenium Grid con Firefox
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')

        driver = webdriver.Remote(
            command_executor=self.selenium_url,  # Usar el URL dinámico proporcionado en el constructor
            options=options,
        )

        try:
            # Navegar a la página de login
            driver.get(login_url)

            # Asegurarse de que la página se haya cargado completamente
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/form/div/div/div[2]/input"))
            )

            # Encontrar y llenar los campos de login utilizando los XPaths proporcionados
            user_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/form/div/div/div[2]/input")
            password_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/form/div/div/div[3]/input")
            login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/form/div/div/div[6]/button")

            user_input.send_keys(self.username)
            password_input.send_keys(self.password)

            # Desplazarse al botón de inicio de sesión y hacer clic
            driver.execute_script("arguments[0].scrollIntoView();", login_button)
            login_button.click()

            # Obtener cookies y CSRF token
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, '_glpi_csrf_token'))
            )

            cookies = driver.get_cookies()
            csrf_token = driver.find_element(By.NAME, '_glpi_csrf_token').get_attribute('value')
        finally:
            driver.quit()

        # Configurar sesión de requests con cookies y CSRF token
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        self.session.headers.update({'X-CSRF-Token': csrf_token})

    def create_ticket(self, title, content, urgency=3, category_id=None, requester_id=None, assigned_id=None, entity_id=None, status=5):
        create_ticket_url = f"{self.base_url}/front/ticket.form.php"
        response = self.session.get(create_ticket_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer el token del formulario
        form_token = soup.find('input', {'name': '_glpi_csrf_token'})['value']

        payload = {
            '_glpi_csrf_token': form_token,
            'name': title,
            'content': content,
            'urgency': urgency,
            'status': status,
            'add': 'Agregar'
        }

        # Agregar el ID de la categoría si se proporciona
        if category_id:
            payload['itilcategories_id'] = category_id  # Campo esperado por GLPI para la categoría

        if requester_id:
            payload['_users_id_requester'] = requester_id
        if assigned_id:
            payload['_users_id_assign'] = assigned_id
        if entity_id:
            payload['entities_id'] = entity_id

        response = self.session.post(create_ticket_url, data=payload, allow_redirects=False)

        if response.status_code == 302:
            redirect_url = response.headers['Location']
            response = self.session.get(f"{self.base_url}{redirect_url}")

        response_text = response.text

        if response.status_code == 200:
            ticket_id = self.extract_ticket_id_from_message(response_text)
            if ticket_id:
                self.close_ticket(ticket_id)
                return {"message": "Ticket created and closed successfully", "ticket_id": ticket_id}
            else:
                return {"message": "Ticket created successfully, but could not extract ticket ID"}
        else:
            return {"message": "Failed to create ticket", "details": response_text}

    def extract_ticket_id_from_message(self, response_text):
        # Buscar el ID del ticket en el mensaje de éxito
        soup = BeautifulSoup(response_text, 'html.parser')
        toast_container = soup.find('div', {'id': 'messages_after_redirect'})
        if toast_container:
            toast_body = toast_container.find('div', {'class': 'toast-body'})
            if toast_body:
                ticket_id_match = re.search(r'\((\d+)\)', toast_body.text)
                if ticket_id_match:
                    return ticket_id_match.group(1)
        return None

    def close_ticket(self, ticket_id):
        close_ticket_url = f"{self.base_url}/front/ticket.form.php?id={ticket_id}"
        response = self.session.get(close_ticket_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer el token del formulario
        form_token = soup.find('input', {'name': '_glpi_csrf_token'})['value']

        payload = {
            '_glpi_csrf_token': form_token,
            'id': ticket_id,
            'status': 6,  # 6 es el estado de cerrado en GLPI
            'save': 'Guardar'
        }

        response = self.session.post(close_ticket_url, data=payload, allow_redirects=False)
        return response.status_code == 200

    def close(self):
        self.session.close()
