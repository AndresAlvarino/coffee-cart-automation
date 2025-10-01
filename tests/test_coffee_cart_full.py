import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

def take_screenshot(driver, case_name, step_name):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    folder_path = os.path.join("screenshots", case_name)
    os.makedirs(folder_path, exist_ok=True)
    driver.save_screenshot(os.path.join(folder_path, f"{timestamp}_{step_name}.png"))

class CoffeeCartFullTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    # 1
    def test_compra_espresso(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        take_screenshot(driver, "compra_espresso", "home_loaded")
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]").click()
        take_screenshot(driver, "compra_espresso", "espresso_selected")
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        take_screenshot(driver, "compra_espresso", "checkout_opened")
        driver.find_element(By.NAME, "name").send_keys("Andres")
        driver.find_element(By.NAME, "email").send_keys("asd123@gmail.com")
        take_screenshot(driver, "compra_espresso", "form_filled")
        driver.find_element(By.ID, "submit-payment").click()
        take_screenshot(driver, "compra_espresso", "order_submitted")

    # 2
    def test_compra_multiple_productos(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]").click()
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Cappuccino')]]").click()
        take_screenshot(driver, "compra_multiple_productos", "productos_agregados")
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        take_screenshot(driver, "compra_multiple_productos", "checkout_opened")

    # 3
    def test_navegacion_basica(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.LINK_TEXT, "cart (0)").click()
        take_screenshot(driver, "navegacion_basica", "cart_page")
        driver.find_element(By.LINK_TEXT, "github").click()
        take_screenshot(driver, "navegacion_basica", "github_page")

    # 4
    def test_formulario_vacio(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        driver.find_element(By.ID, "submit-payment").click()
        take_screenshot(driver, "formulario_vacio", "submit_empty")

    # 5 (fix aplicado)
    def test_eliminar_producto(self):
        driver = self.driver
        driver.get("http://localhost:5173")

        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]").click()
        take_screenshot(driver, "eliminar_producto", "product_added")

        # Ir al carrito
        cart_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "cart (1)"))
        )
        cart_link.click()
        take_screenshot(driver, "eliminar_producto", "cart_opened")

        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "delete"))
        )
        delete_button.click()
        take_screenshot(driver, "eliminar_producto", "product_removed")

    # 6
    def test_email_invalido(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        driver.find_element(By.NAME, "name").send_keys("Andres")
        driver.find_element(By.NAME, "email").send_keys("andres@@gmail")
        driver.find_element(By.ID, "submit-payment").click()
        take_screenshot(driver, "email_invalido", "invalid_email")

    # 7
    def test_persistencia_carrito(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]").click()
        driver.refresh()
        take_screenshot(driver, "persistencia_carrito", "page_refreshed")

    # 8
    def test_responsive_design(self):
        driver = self.driver
        driver.set_window_size(375, 812)
        driver.get("http://localhost:5173")
        take_screenshot(driver, "responsive_design", "mobile_view")

    # 9
    def test_compra_mocha(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Mocha')]]").click()
        take_screenshot(driver, "compra_mocha", "mocha_selected")

    # 10
    def test_compra_datos_diferentes(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Americano')]]").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        driver.find_element(By.NAME, "name").send_keys("Maria")
        driver.find_element(By.NAME, "email").send_keys("maria123@example.com")
        driver.find_element(By.ID, "submit-payment").click()
        take_screenshot(driver, "compra_datos_diferentes", "order_maria")

    # 11
    def test_cancelar_modal(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        driver.find_element(By.CLASS_NAME, "close").click()
        take_screenshot(driver, "cancelar_modal", "modal_closed")

    # 12
    def test_cerrar_modal_x(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        driver.find_element(By.CLASS_NAME, "close").click()
        take_screenshot(driver, "cerrar_modal_x", "modal_closed")

    # 13
    def test_hover_producto(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        product = driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]")
        ActionChains(driver).move_to_element(product).perform()
        take_screenshot(driver, "hover_producto", "hover_espresso")

    # 14
    def test_hover_total(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        total_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Total')]")
        ActionChains(driver).move_to_element(total_btn).perform()
        take_screenshot(driver, "hover_total", "hover_total_btn")

    # 15
    def test_hover_navegacion(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        nav_link = driver.find_element(By.LINK_TEXT, "cart (0)")
        ActionChains(driver).move_to_element(nav_link).perform()
        take_screenshot(driver, "hover_navegacion", "hover_cart")

    # 16
    def test_clic_derecho_producto(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        product = driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]")
        ActionChains(driver).context_click(product).perform()
        take_screenshot(driver, "clic_derecho_producto", "context_menu")

    # 17
    def test_doble_clic_producto(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        product = driver.find_element(By.XPATH, "//li[h4[contains(text(), 'Espresso')]]")
        ActionChains(driver).double_click(product).perform()
        take_screenshot(driver, "doble_clic_producto", "double_click")

    # 18
    def test_tab_formulario(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        name_field = driver.find_element(By.NAME, "name")
        name_field.send_keys("Juan")
        ActionChains(driver).send_keys("\t").perform()
        take_screenshot(driver, "tab_formulario", "tab_pressed")

    # 19
    def test_enter_submit(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        driver.find_element(By.NAME, "name").send_keys("Juan")
        driver.find_element(By.NAME, "email").send_keys("juan@test.com\n")
        take_screenshot(driver, "enter_submit", "submitted_with_enter")

    # 20 (fix aplicado)
    def test_focus_input_email(self):
        driver = self.driver
        driver.get("http://localhost:5173")
        driver.find_element(By.XPATH, "//button[contains(text(),'Total')]").click()
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        )
        ActionChains(driver).move_to_element(email_field).click().perform()
        take_screenshot(driver, "focus_input_email", "email_focused")


if __name__ == "__main__":
    unittest.main()
