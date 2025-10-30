"""
Script para extraer información de productos de recambioscoche.es usando Selenium
para superar la protección anti-bot que requiere JavaScript.
"""

import time
import random
import re
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin, urlparse, parse_qs

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠ Selenium no está instalado. Instala con: pip install selenium")


class RecambiosCocheSelenium:
    def __init__(self, headless: bool = True):
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium no está disponible. Instala con: pip install selenium")
        
        self.base_url = "https://www.recambioscoche.es"
        self.driver = None
        self.headless = headless
        self._setup_driver()
    
    def _setup_driver(self):
        """Configura el driver de Chrome con opciones anti-detección"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Opciones para evitar detección
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        
        # User agent realista
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Driver de Chrome configurado correctamente")
        except Exception as e:
            print(f"❌ Error configurando el driver: {e}")
            raise
    
    def get_page_content(self, url: str, wait_time: int = 15) -> bool:
        """
        Navega a una página y espera a que se cargue completamente
        """
        try:
            print(f"Navegando a: {url}")
            self.driver.get(url)
            
            # Delay inicial para permitir carga básica
            time.sleep(random.uniform(3, 5))
            
            # Esperar a que la página se cargue completamente
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Verificar si hay protección anti-bot
            if "Enable JavaScript and cookies to continue" in self.driver.page_source:
                print("⚠ Detectada protección anti-bot, esperando...")
                time.sleep(8)
                
                # Intentar hacer clic en algún elemento para activar JavaScript
                try:
                    body = self.driver.find_element(By.TAG_NAME, "body")
                    body.click()
                    time.sleep(5)
                except:
                    pass
            
            # Scroll hacia abajo para activar lazy loading
            print("📜 Haciendo scroll para cargar contenido dinámico...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Esperar específicamente a que se carguen los productos
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".listing-wrapper[data-listing-products] .product-card"))
                )
                
                # Esperar un poco más para que se carguen todos los elementos
                time.sleep(3)
                
                # Verificar cuántos productos se han cargado
                products = self.driver.find_elements(By.CSS_SELECTOR, ".listing-wrapper[data-listing-products] .product-card")
                print(f"✓ {len(products)} productos detectados en la página")
                return True
                
            except TimeoutException:
                print("⚠ No se encontraron productos con la estructura esperada")
                # Intentar buscar productos con selectores alternativos
                alternative_selectors = [
                    ".product-card",
                    "[data-article-id]",
                    ".listing-wrapper .product-card"
                ]
                
                for selector in alternative_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"✓ Encontrados {len(elements)} productos con selector alternativo: {selector}")
                        return True
                
                print("❌ No se encontraron productos con ningún selector")
                return False
                
        except TimeoutException:
            print(f"❌ Timeout al cargar la página: {url}")
            return False
        except Exception as e:
            print(f"❌ Error al cargar la página: {e}")
            return False
    
    def extract_products_from_page(self) -> List[Dict[str, str]]:
        """
        Extrae información de productos de la página actual
        """
        products = []
        
        try:
            # Intentar múltiples selectores para encontrar productos
            product_selectors = [
                ".listing-wrapper[data-listing-products] .product-card",
                ".product-card",
                "[data-article-id]",
                ".listing-wrapper .product-card"
            ]
            
            product_elements = []
            
            for selector in product_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"📦 Encontrados {len(elements)} productos con selector: {selector}")
                        product_elements = elements
                        break
                except Exception as e:
                    print(f"⚠ Error con selector {selector}: {e}")
                    continue
            
            if not product_elements:
                print("❌ No se encontraron productos con ningún selector")
                return products
            
            print(f"📦 Procesando {len(product_elements)} productos")
            
            # Procesar cada producto
            for i, element in enumerate(product_elements):
                try:
                    print(f"🔍 Procesando producto {i+1}/{len(product_elements)}")
                    
                    # Verificar que el elemento sea válido
                    if not element.is_displayed():
                        print(f"⚠ Producto {i+1} no está visible, intentando hacer scroll...")
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        time.sleep(1)
                    
                    product_info = self.extract_product_info_from_element(element)
                    if product_info:
                        product_info['position'] = i + 1
                        products.append(product_info)
                        print(f"✓ Producto {i+1}: {product_info.get('title', 'Sin título')[:50]}...")
                    
                    # Pequeña pausa entre productos para evitar problemas
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"❌ Error procesando producto {i+1}: {e}")
                    # Añadir producto con error pero continuar
                    products.append({
                        "title": f"Error en producto {i+1}",
                        "article_number": "N/A",
                        "generic_article_id": "N/A", 
                        "brand": "N/A",
                        "price": "N/A",
                        "position": i + 1,
                        "link": "N/A",
                        "image": "N/A"
                    })
                    continue
            
            print(f"✅ Total de productos extraídos: {len(products)}")
            
        except Exception as e:
            print(f"❌ Error general al extraer productos: {e}")
        
        return products
    
    def extract_product_info_from_element(self, element) -> Optional[Dict[str, str]]:
        """
        Extrae información de un elemento de producto individual usando la estructura específica de recambioscoche.es
        """
        try:
            # Scroll al elemento para asegurar que esté visible
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            
            product_info = {}
            
            # Buscar el wrapper del producto
            try:
                wrapper = element.find_element(By.CSS_SELECTOR, ".product-card__wrapper")
            except NoSuchElementException:
                wrapper = element  # Si no encuentra el wrapper, usar el elemento principal
            
            # Buscar el head del producto
            try:
                head = wrapper.find_element(By.CSS_SELECTOR, ".product-card__head")
            except NoSuchElementException:
                head = wrapper  # Si no encuentra el head, usar el wrapper
            
            # Extraer título desde product-card__title - intentar múltiples selectores
            title = "Sin título"
            title_selectors = [
                ".product-card__title",
                ".product-card__wrapper .product-card__head .product-card__title",
                ".product-card__head .product-card__title",
                "h3", "h2", ".title"
            ]
            
            for selector in title_selectors:
                try:
                    title_element = head.find_element(By.CSS_SELECTOR, selector)
                    if title_element and title_element.text.strip():
                        title = title_element.text.strip()
                        product_info['title'] = title
                        
                        # Buscar el enlace dentro del título
                        try:
                            title_link = title_element.find_element(By.TAG_NAME, "a")
                            href = title_link.get_attribute("href")
                            product_info['link'] = urljoin(self.base_url, href) if href else "N/A"
                        except NoSuchElementException:
                            product_info['link'] = "N/A"
                        break
                except NoSuchElementException:
                    continue
            
            if title == "Sin título":
                product_info['title'] = "Sin título"
                product_info['link'] = "N/A"
            
            # Extraer número de artículo desde data-article-id del product-card
            try:
                article_id = element.get_attribute("data-article-id")
                product_info['article_number'] = article_id if article_id else "N/A"
            except:
                product_info['article_number'] = "N/A"
            
            # Extraer información adicional desde data-generic-article-id
            try:
                generic_article_id = element.get_attribute("data-generic-article-id")
                product_info['generic_article_id'] = generic_article_id if generic_article_id else "N/A"
            except:
                product_info['generic_article_id'] = "N/A"
            
            # Buscar marca en el texto del título o en atributos - mejorado
            brand = "N/A"
            brand_selectors = [
                ".product-card__brand",
                ".brand",
                ".manufacturer",
                "[data-brand]"
            ]
            
            # Primero intentar desde atributos
            brand = element.get_attribute("data-brand")
            
            if not brand:
                for selector in brand_selectors:
                    try:
                        brand_element = element.find_element(By.CSS_SELECTOR, selector)
                        if brand_element and brand_element.text.strip():
                            brand = brand_element.text.strip()
                            break
                    except:
                        continue
            
            # Si no encontramos marca, intentar extraer del título
            if brand == "N/A" or not brand:
                title_text = product_info.get('title', '')
                if title_text and title_text != "Sin título":
                    # Buscar patrones comunes de marca al inicio del título
                    brand_patterns = [
                        r'^([A-Z][A-Za-z]+)\s+',  # Palabra que empieza con mayúscula al inicio
                        r'^([A-Z]{2,})\s+',       # Siglas en mayúsculas al inicio
                    ]
                    
                    for pattern in brand_patterns:
                        match = re.search(pattern, title_text)
                        if match:
                            potential_brand = match.group(1)
                            # Verificar que no sea una palabra común
                            if potential_brand.lower() not in ['cilindro', 'filtro', 'bomba', 'sensor', 'válvula']:
                                brand = potential_brand
                                break
                    
                    # Si no encontramos con patrones, usar la primera palabra si es larga
                    if brand == "N/A":
                        title_parts = title_text.split()
                        if len(title_parts) > 0 and len(title_parts[0]) > 2:
                            brand = title_parts[0]
            
            product_info['brand'] = brand
            
            # Extraer precio - mejorado con múltiples selectores
            price = "N/A"
            price_selectors = [
                ".product-card__price",
                ".price", ".cost", ".amount", 
                "[data-price]", ".price-current", ".price-value",
                ".product-price"
            ]
            
            for selector in price_selectors:
                try:
                    price_element = element.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_element.text.strip()
                    if price_text and ('€' in price_text or price_text.replace('.', '').replace(',', '').isdigit()):
                        price = price_text
                        break
                except NoSuchElementException:
                    continue
            
            product_info['price'] = price
            
            # Extraer imagen - mejorado
            image = "N/A"
            try:
                img_elements = element.find_elements(By.TAG_NAME, "img")
                for img in img_elements:
                    src = img.get_attribute("src") or img.get_attribute("data-src") or img.get_attribute("data-lazy-src")
                    if src and ("cdn." in src or "http" in src):
                        image = urljoin(self.base_url, src)
                        break
            except:
                pass
            
            product_info['image'] = image
            
            return product_info
            
        except Exception as e:
            print(f"Error al extraer información del producto: {e}")
            return None
    
    def find_text_by_selectors(self, element, selectors: List[str]) -> Optional[str]:
        """
        Busca texto usando una lista de selectores CSS
        """
        for selector in selectors:
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                text = found_element.text.strip()
                if text:
                    return text
            except NoSuchElementException:
                continue
        return None
    
    def get_next_page_url(self) -> Optional[str]:
        """
        Busca el enlace a la siguiente página
        """
        try:
            next_selectors = [
                "a[rel='next']",
                ".next-page",
                ".pagination .next",
                "a:contains('Siguiente')",
                "a:contains('>')"
            ]
            
            for selector in next_selectors:
                try:
                    next_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    href = next_element.get_attribute("href")
                    if href:
                        return href
                except NoSuchElementException:
                    continue
            
            # Buscar en la URL actual si hay parámetro de página
            current_url = self.driver.current_url
            parsed_url = urlparse(current_url)
            query_params = parse_qs(parsed_url.query)
            
            if 'pg' in query_params:
                current_page = int(query_params['pg'][0])
                next_page = current_page + 1
                new_query = current_url.replace(f'pg={current_page}', f'pg={next_page}')
                return new_query
            
        except Exception as e:
            print(f"Error al buscar siguiente página: {e}")
        
        return None
    
    def extract_all_products(self, start_url: str, max_pages: int = 5) -> List[Dict[str, str]]:
        """
        Extrae productos de múltiples páginas
        """
        all_products = []
        current_url = start_url
        page_count = 0
        
        while current_url and page_count < max_pages:
            page_count += 1
            print(f"\n--- Página {page_count}/{max_pages} ---")
            
            if not self.get_page_content(current_url):
                print(f"❌ No se pudo cargar la página {page_count}")
                break
            
            # Delay aleatorio entre páginas
            time.sleep(random.uniform(2, 4))
            
            products = self.extract_products_from_page()
            
            # Añadir número de página a cada producto
            for product in products:
                product['page'] = page_count
            
            all_products.extend(products)
            print(f"✓ Página {page_count}: {len(products)} productos extraídos")
            
            # Buscar siguiente página
            current_url = self.get_next_page_url()
            if current_url:
                print(f"➡ Siguiente página encontrada: {current_url}")
            else:
                print("ℹ No hay más páginas")
                break
        
        return all_products
    
    def search_product_by_number(self, oe_number: str, max_pages: int = 10) -> List[Dict[str, str]]:
        """
        Busca un producto específico por su número OE en múltiples páginas
        """
        print(f"🔍 Buscando producto con número OE: {oe_number}")
        
        # Construir URL de búsqueda
        search_url = f"{self.base_url}/oenumber/{oe_number}.html"
        
        all_products = []
        current_url = search_url
        page_count = 0
        
        while current_url and page_count < max_pages:
            page_count += 1
            print(f"\n--- Página {page_count}/{max_pages} ---")
            
            if not self.get_page_content(current_url):
                print(f"❌ No se pudo cargar la página {page_count}")
                break
            
            # Delay aleatorio entre páginas
            time.sleep(random.uniform(2, 4))
            
            products = self.extract_products_from_page()
            
            # Añadir número de página a cada producto
            for product in products:
                product['page'] = page_count
                product['search_oe'] = oe_number
            
            all_products.extend(products)
            print(f"✓ Página {page_count}: {len(products)} productos extraídos")
            
            # Buscar siguiente página
            current_url = self.get_next_page_url()
            if current_url:
                print(f"➡ Siguiente página encontrada: {current_url}")
            else:
                print("ℹ No hay más páginas")
                break
        
        return all_products
    
    def search_product_by_number_with_page(self, oe_number: str, page_number: int = 1) -> List[Dict[str, str]]:
        """
        Busca un producto específico por su número OE en una página específica
        """
        print(f"🔍 Buscando producto {oe_number} en página {page_number}")
        
        # Construir URL con número de página
        search_url = f"{self.base_url}/oenumber/{oe_number}.html?pg={page_number}"
        
        if not self.get_page_content(search_url):
            print(f"❌ No se pudo cargar la página {page_number}")
            return []
        
        products = self.extract_products_from_page()
        
        # Añadir información adicional a cada producto
        for product in products:
            product['page'] = page_number
            product['search_oe'] = oe_number
        
        print(f"✓ Página {page_number}: {len(products)} productos extraídos")
        return products
    
    def get_product_info_summary(self, products: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Genera un resumen de la información de productos extraídos
        """
        if not products:
            return {
                "total_products": 0,
                "brands": [],
                "price_range": {"min": None, "max": None},
                "pages": []
            }
        
        # Extraer marcas únicas
        brands = set()
        prices = []
        pages = set()
        
        for product in products:
            if product.get('brand') and product['brand'] != 'N/A':
                brands.add(product['brand'])
            
            if product.get('page'):
                pages.add(product['page'])
            
            # Extraer precios numéricos
            price_text = product.get('price', '')
            if price_text and price_text != 'N/A':
                # Extraer números del precio
                price_match = re.search(r'(\d+[.,]\d+|\d+)', price_text.replace(',', '.'))
                if price_match:
                    try:
                        price_value = float(price_match.group(1))
                        prices.append(price_value)
                    except ValueError:
                        pass
        
        # Calcular rango de precios
        price_range = {"min": None, "max": None}
        if prices:
            price_range["min"] = min(prices)
            price_range["max"] = max(prices)
        
        return {
            "total_products": len(products),
            "brands": sorted(list(brands)),
            "price_range": price_range,
            "pages": sorted(list(pages))
        }

    def close(self):
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()
            print("✓ Navegador cerrado")


def search_by_product_number(oe_number: str, page_number: Optional[int] = None, max_pages: int = 10, headless: bool = True):
    """
    Función para buscar productos por número OE
    
    Args:
        oe_number: Número OE del producto a buscar
        page_number: Página específica a buscar (opcional)
        max_pages: Máximo número de páginas a buscar si no se especifica página
        headless: Si ejecutar en modo headless
    """
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium no está disponible. Instala con: pip install selenium")
        return
    
    scraper = None
    try:
        print("🚀 Iniciando scraper con Selenium...")
        scraper = RecambiosCocheSelenium(headless=headless)
        
        if page_number:
            # Buscar en página específica
            print(f"\n🔍 Buscando producto {oe_number} en página {page_number}")
            products = scraper.search_product_by_number_with_page(oe_number, page_number)
        else:
            # Buscar en múltiples páginas
            print(f"\n🔍 Buscando producto {oe_number} en hasta {max_pages} páginas")
            products = scraper.search_product_by_number(oe_number, max_pages)
        
        # Generar resumen
        summary = scraper.get_product_info_summary(products)
        
        print(f"\n📊 Resumen de búsqueda para '{oe_number}':")
        print(f"Total de productos encontrados: {summary['total_products']}")
        print(f"Marcas encontradas: {', '.join(summary['brands']) if summary['brands'] else 'Ninguna'}")
        print(f"Páginas procesadas: {', '.join(map(str, summary['pages'])) if summary['pages'] else 'Ninguna'}")
        
        if summary['price_range']['min'] and summary['price_range']['max']:
            print(f"Rango de precios: {summary['price_range']['min']:.2f}€ - {summary['price_range']['max']:.2f}€")
        
        if products:
            print(f"\n📦 Productos encontrados:")
            for i, product in enumerate(products):
                print(f"\n--- Producto {i+1} ---")
                print(f"   Título: {product.get('title', 'N/A')}")
                print(f"   Artículo: {product.get('article_number', 'N/A')}")
                print(f"   ID Genérico: {product.get('generic_article_id', 'N/A')}")
                print(f"   Marca: {product.get('brand', 'N/A')}")
                print(f"   Precio: {product.get('price', 'N/A')}")
                print(f"   Página: {product.get('page', 'N/A')}")
                print(f"   Posición: {product.get('position', 'N/A')}")
                if product.get('link', 'N/A') != 'N/A':
                    print(f"   Enlace: {product['link'][:80]}...")
                if product.get('image', 'N/A') != 'N/A':
                    print(f"   Imagen: {product['image'][:80]}...")
        else:
            print("❌ No se encontraron productos")
    
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
    
    finally:
        if scraper:
            scraper.close()


def main():
    """Función principal para probar el scraper"""
    import sys
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium no está disponible. Instala con: pip install selenium")
        return
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        oe_number = sys.argv[1]
        page_number = None
        max_pages = 10
        headless = True
        
        # Procesar argumentos adicionales
        if len(sys.argv) > 2:
            try:
                page_number = int(sys.argv[2])
            except ValueError:
                print("⚠ El segundo argumento debe ser un número de página válido")
                return
        
        if len(sys.argv) > 3:
            try:
                max_pages = int(sys.argv[3])
            except ValueError:
                print("⚠ El tercer argumento debe ser un número máximo de páginas válido")
                return
        
        if len(sys.argv) > 4:
            headless = sys.argv[4].lower() in ['true', '1', 'yes', 'si']
        
        # Ejecutar búsqueda
        search_by_product_number(oe_number, page_number, max_pages, headless)
    else:
        # Modo de prueba por defecto
        print("🧪 Modo de prueba - Buscando producto de ejemplo")
        print("💡 Uso: python recambioscoche_selenium.py <numero_oe> [pagina] [max_paginas] [headless]")
        print("💡 Ejemplo: python recambioscoche_selenium.py 55190993 2")
        print("💡 Ejemplo: python recambioscoche_selenium.py 55190993 None 5 False")
        
        # Ejecutar búsqueda de prueba
        search_by_product_number("55190993", page_number=2, headless=False)


if __name__ == "__main__":
    main()