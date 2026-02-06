import time
import json
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAÇÕES ---
WEBHOOK_URL = "https://webhook.gcsconsulting.com.br/webhook/meta"
URL_INSIGHTS = "https://business.facebook.com/latest/whatsapp_manager/insights?business_id={BUSINESS_ID}&asset_id={ASSET_ID}"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    
    # Forçamos a versão 144 para bater com o seu navegador atual
    try:
        driver = uc.Chrome(options=options, version_main=144)
    except Exception as e:
        log(f"Erro ao iniciar com versão específica: {e}")
        # Caso ele atualize sozinho no futuro, deixamos o padrão como fallback
        driver = uc.Chrome(options=options)
        
    return driver

def login_meta(driver):
    log("Acessando Facebook para validar cookies...")
    driver.get("https://www.facebook.com")
    try:
        with open("cookies_facebook.json", "r") as file:
            cookies = json.load(file)
        for cookie in cookies:
            if 'sameSite' in cookie: del cookie['sameSite']
            try: driver.add_cookie(cookie)
            except: pass
        driver.refresh()
        time.sleep(4)
        return True
    except Exception as e:
        log(f"Erro ao carregar cookies: {e}")
        return False

def enviar_para_webhook(dados):
    """Envia os dados extraídos para o endpoint da GCS Consulting"""
    try:
        response = requests.post(WEBHOOK_URL, json=dados, timeout=10)
        if response.status_code == 200:
            log(">>> SUCESSO: Dados enviados ao Webhook.")
        else:
            log(f">>> ERRO: Webhook retornou status {response.status_code}")
    except Exception as e:
        log(f">>> ERRO CRÍTICO no envio: {e}")

def extrair_e_processar(driver):
    log(f"Navegando para Insights: {URL_INSIGHTS}")
    driver.get(URL_INSIGHTS)
    
    # Aguarda o painel carregar (ajuste o tempo se sua internet for lenta)
    wait = WebDriverWait(driver, 25)
    
    try:
        # Espera um elemento chave da página (o seletor de data, por exemplo)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Calendário')] | //div[contains(@class, 'x1i10hfl')]")))
        time.sleep(8) # Garantia para carregamento dos números internos

        # --- EXTRAÇÃO DOS DADOS ---
        # 1. Tenta capturar o período selecionado
        try:
            periodo = driver.find_element(By.XPATH, "//div[contains(@class, 'x1i10hfl')]//span[contains(text(), '202')]").text
        except:
            periodo = "Período não identificado"

        # 2. Busca valores financeiros (procurando por R$ ou símbolos monetários)
        # Adaptado para capturar o que estiver visível na tela no momento
        elementos_texto = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$') or contains(text(), '$')]")
        valores_financeiros = [el.text for el in elementos_texto if el.text.strip() != ""]

        # 3. Montagem do JSON
        payload = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url_origem": URL_INSIGHTS,
            "periodo": periodo,
            "dados_financeiros": valores_financeiros,
            "status_painel": "Dados Disponíveis" if valores_financeiros else "Sem dados na tela"
        }

        log(f"Dados extraídos: {payload}")
        enviar_para_webhook(payload)

    except Exception as e:
        log(f"Erro durante a extração: {e}")
        # Envia log de erro para o webhook também, para você monitorar
        enviar_para_webhook({"erro": str(e), "url": URL_INSIGHTS})

def main():
    driver = setup_driver()
    try:
        if login_meta(driver):
            extrair_e_processar(driver)
    finally:
        log("Encerrando driver...")
        driver.quit()

if __name__ == "__main__":
    main()
