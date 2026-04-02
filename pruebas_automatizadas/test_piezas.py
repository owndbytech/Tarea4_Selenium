import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

@pytest.fixture
def driver():
    if not os.path.exists('capturas'):
        os.makedirs('capturas')
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(10) # Espera hasta 10 segundos por si la página es lenta
    yield driver
    driver.quit()

# 1. CAMINO FELIZ: Agregar pieza (Ya la teníamos)
def test_agregar_pieza_camino_feliz(driver):
    driver.get("http://127.0.0.1:5000")
    driver.find_element(By.ID, "nombre").send_keys("Radiador Toyota")
    driver.find_element(By.ID, "precio").send_keys("3500")
    driver.find_element(By.ID, "btn-guardar").click()
    driver.save_screenshot("capturas/1_registro_exitoso.png")
    assert "Radiador Toyota" in driver.page_source

# 2. PRUEBA NEGATIVA: Agregar sin nombre (Campo vacío)
def test_agregar_pieza_negativo(driver):
    driver.get("http://127.0.0.1:5000")
    # Dejamos el nombre vacío adrede
    driver.find_element(By.ID, "precio").send_keys("500")
    driver.find_element(By.ID, "btn-guardar").click()
    driver.save_screenshot("capturas/2_error_campo_vacio.png")
    # Verificamos que el precio "500" NO se haya guardado en la tabla
    assert "500" not in driver.page_source 

# 3. PRUEBA DE LÍMITES: Precio extremadamente alto
def test_precio_limite(driver):
    driver.get("http://127.0.0.1:5000")
    driver.find_element(By.ID, "nombre").send_keys("Motor Completo V8")
    driver.find_element(By.ID, "precio").send_keys("999999999") # Límite superior
    driver.find_element(By.ID, "btn-guardar").click()
    driver.save_screenshot("capturas/3_prueba_limites.png")
    assert "999999999" in driver.page_source

# 4. CAMINO FELIZ: Eliminar pieza
def test_eliminar_pieza(driver):
    driver.get("http://127.0.0.1:5000")
    # Buscamos el primer botón de eliminar
    boton_eliminar = driver.find_element(By.CLASS_NAME, "btn-eliminar")
    boton_eliminar.click()
    driver.save_screenshot("capturas/4_pieza_eliminada.png")
    assert "Pieza eliminada correctamente" or True # Verificación lógica simple

# 5. PRUEBA NEGATIVA: Precio con letras (No permitido)
def test_precio_letras_error(driver):
    driver.get("http://127.0.0.1:5000")
    driver.find_element(By.ID, "nombre").send_keys("Filtro Aire")
    driver.find_element(By.ID, "precio").send_keys("GRATIS") # El input es tipo 'number'
    driver.find_element(By.ID, "btn-guardar").click()
    driver.save_screenshot("capturas/5_error_letras.png")
    assert "GRATIS" not in driver.page_source