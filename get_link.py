import time
import json
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAÇÕES ---
# 1. ARQUIVO_CREDENCIAL: O arquivo JSON com as credenciais da sua conta de serviço do Google (para acessar a API do Google Sheets).
ARQUIVO_CREDENCIAL = "SEU_ARQUIVO_CREDENCIAL.json"  # Substitua pelo caminho do seu arquivo de credenciais JSON

# 2. ID_PLANILHA: O ID único da planilha do Google Sheets onde você quer salvar os dados.
ID_PLANILHA = "SEU_ID_DE_PLANILHA"  # Substitua pelo ID da sua planilha do Google Sheets

# 3. NOME_ABA: O nome da aba onde os dados serão salvos.
NOME_ABA = "Nome_da_Aba"  # Substitua pelo nome da aba da sua planilha do Google Sheets

def log(msg):
    print(f"{msg}")

def setup_driver():
    # Configura o driver do Chrome (usando undetected_chromedriver)
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")  # Descomente para rodar em modo sem interface gráfica (headless)
    driver = uc.Chrome(options=options, version_main=142)  # Defina a versão do Chrome se necessário
    return driver

def login_with_cookies(driver):
    log(">>> Acessando Mercado Livre para login...")
    driver.get("https://www.mercadolivre.com.br")
    time.sleep(3)

    try:
        # Carrega os cookies de sessão salvos
        with open("cookies.json", "r") as file:
            cookies = json.load(file)
        
        # Adiciona os cookies ao navegador
        for cookie in cookies:
            if 'sameSite' in cookie: del cookie['sameSite']  # Remove cookies de sameSite se houver
            if 'storeId' in cookie: del cookie['storeId']    # Remove cookies de storeId se houver
            try:
                driver.add_cookie(cookie)  # Adiciona o cookie
            except: pass
                
        driver.refresh()  # Atualiza a página após adicionar os cookies
        time.sleep(3)
        return True
    except Exception as e:
        log(f"Erro ao carregar cookies: {e}")
        return False

def connect_to_sheets():
    """Conecta no Google Sheets e retorna a aba pronta para uso"""
    log(">>> Conectando ao Google Sheets...")
    try:
        # Defina o escopo de permissões para acessar o Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Credenciais para acesso ao Google Sheets (substitua pelo seu arquivo de credenciais)
        creds = ServiceAccountCredentials.from_json_keyfile_name(ARQUIVO_CREDENCIAL, scope)
        client = gspread.authorize(creds)
        
        # Conecta à planilha pelo ID
        sheet = client.open_by_key(ID_PLANILHA)
        try:
            worksheet = sheet.worksheet(NOME_ABA)  # Tenta acessar a aba específica
        except:
            worksheet = sheet.get_worksheet(0)  # Se falhar, usa a primeira aba
            
        log(">>> Conexão com a Planilha: SUCESSO!")
        return worksheet
    except Exception as e:
        log(f"ERRO CRÍTICO DE CONEXÃO: {e}")
        sys.exit(1)

def scrape_mais_vendidos(driver):
    target_url = "https://www.mercadolivre.com.br/mais-vendidos"
    log(f">>> Acessando: {target_url}")
    driver.get(target_url)
    time.sleep(3)
    
    # Scroll na página para carregar todos os produtos
    for _ in range(4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
    driver.execute_script("window.scrollTo(0, 0);")
    
    products_data = []
    seen_ids = set()
    
    # Encontra todos os links na página
    all_links = driver.find_elements(By.TAG_NAME, "a")
    log(f">>> Analisando {len(all_links)} links...")

    for link in all_links:
        try:
            url = link.get_attribute("href")
            if not url or "mercadolivre.com.br" not in url: continue
            if "click1" in url or "#" in url: continue

            # Verifica se o link é de um produto
            if "MLB" in url or "/p/" in url:
                clean_link = url.split("?")[0]  # Remove parâmetros do link
                if clean_link in seen_ids: continue
                seen_ids.add(clean_link)

                # Coleta o título e a imagem do produto
                raw_title = link.text
                image_url = "N/A"
                
                try:
                    img = link.find_element(By.TAG_NAME, "img")
                    if not raw_title: raw_title = img.get_attribute("alt")
                    src = img.get_attribute("src")
                    data_src = img.get_attribute("data-src")
                    image_url = data_src if data_src else src
                except: pass
                
                if not raw_title: 
                    try: raw_title = link.find_element(By.XPATH, "./..").text.split("\n")[0]
                    except: raw_title = "Produto ML"

                title = raw_title.replace("\n", " ").strip()
                
                # Se o título for válido, salva os dados
                if len(title) > 3 and "Ver mais" not in title:
                    products_data.append({
                        "titulo": title,
                        "link_original": clean_link,
                        "imagem": image_url
                    })
        except: continue
            
    log(f">>> Coletados {len(products_data)} produtos para processamento.")
    return products_data

def process_and_save_realtime(driver, products_list, worksheet):
    log(f">>> Iniciando processamento e salvamento de {len(products_list)} itens...")
    
    url_ferramenta = "https://www.mercadolivre.com.br/afiliados/linkbuilder"
    driver.get(url_ferramenta)
    time.sleep(4)
    
    for i, product in enumerate(products_list):
        log(f"--- Item {i+1}/{len(products_list)}: {product['titulo'][:20]}... ---")
        
        affiliate_link = None
        
        # Tenta converter o link para afiliado
        try:
            if i > 0 and i % 5 == 0: 
                driver.refresh()  # Atualiza a página a cada 5 itens
                time.sleep(3)

            wait = WebDriverWait(driver, 8)
            input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea, input[placeholder*='http']")))
            input_field.click()
            input_field.clear()
            input_field.send_keys(product['link_original'])
            time.sleep(0.3)
            input_field.send_keys(Keys.TAB)
            
            try:
                btn = driver.find_element(By.XPATH, "//button[contains(., 'Gerar') or contains(., 'Criar')]")
                driver.execute_script("arguments[0].click();", btn)
            except: 
                input_field.send_keys(Keys.ENTER)
            
            time.sleep(3)
            
            # Verifica o link gerado
            try:
                outputs = driver.find_elements(By.CSS_SELECTOR, "input[readonly], textarea[readonly]")
                for out in outputs:
                    val = out.get_attribute("value")
                    if val and ("/sec/" in val or "meli.la" in val):
                        affiliate_link = val
                        break
            except: pass
            
            if not affiliate_link:
                import re
                matches = re.findall(r'https?://(?:www\.)?mercadolivre\.com/sec/[a-zA-Z0-9]+', driver.page_source)
                if matches: affiliate_link = matches[-1]

        except Exception as e:
            log(f"Erro na conversão: {e}")
            driver.refresh()
            time.sleep(2)
        
        # --- SALVAMENTO NA PLANILHA ---
        if affiliate_link:
            log(f"   Link Gerado: {affiliate_link}")
            
            # Coleta a imagem
            url_img = product.get('imagem', '')
            if not url_img or url_img == "N/A":
                url_img = ""
                
            nova_linha = [
                product.get('titulo', ''),
                product.get('link_original', ''),
                affiliate_link,
                url_img  # Envia apenas a URL da imagem
            ]
            
            try:
                worksheet.append_row(nova_linha, value_input_option='USER_ENTERED')
                log("   >>> SALVO NA PLANILHA COM SUCESSO!")
            except Exception as e:
                log(f"   >>> ERRO AO SALVAR NA PLANILHA: {e}")
                
        else:
            log("   >>> Falha ao gerar link. Item ignorado.")
            driver.refresh()
            time.sleep(2)

def main():
    # Conecta à planilha e configura o driver
    worksheet = connect_to_sheets()
    driver = setup_driver()
    try:
        if login_with_cookies(driver):
            produtos = scrape_mais_vendidos(driver)
            if produtos:
                process_and_save_realtime(driver, produtos, worksheet)
            else:
                log("Nenhum produto encontrado.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
