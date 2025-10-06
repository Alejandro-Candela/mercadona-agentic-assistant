import requests
import json

# Probar si las subcategorías incluyen productos
url = "https://tienda.mercadona.es/api/categories/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers, timeout=10)
data = response.json()

# Buscar la categoría "Carne" (ID 3)
for cat in data['results']:
    if cat['id'] == 3:
        print(f"Categoría: {cat['name']} (ID: {cat['id']})")
        print(f"Tiene {len(cat.get('categories', []))} subcategorías\n")
        
        # Ver la subcategoría "Conejo y cordero"
        for subcat in cat.get('categories', []):
            if 'conejo' in subcat['name'].lower():
                print(f"Subcategoría: {subcat['name']} (ID: {subcat['id']})")
                print(f"Claves disponibles: {list(subcat.keys())}")
                print(f"¿Tiene productos? {'products' in subcat}")
                
                if 'products' in subcat:
                    print(f"Número de productos: {len(subcat['products'])}")
                else:
                    print("❌ No tiene clave 'products' en la respuesta inicial")
                    print("\n🔄 Intentando petición directa a la subcategoría...")
                    
                    # Intentar petición directa
                    subcat_url = f"https://tienda.mercadona.es/api/categories/{subcat['id']}"
                    print(f"URL: {subcat_url}")
                    
                    try:
                        import time
                        time.sleep(0.3)
                        subcat_response = requests.get(subcat_url, headers=headers, timeout=10)
                        print(f"Status: {subcat_response.status_code}")
                        
                        if subcat_response.status_code == 200:
                            subcat_data = subcat_response.json()
                            print("✅ Respuesta exitosa!")
                            print(f"Claves: {list(subcat_data.keys())}")
                            
                            if 'categories' in subcat_data:
                                for sub_subcat in subcat_data['categories']:
                                    if 'products' in sub_subcat:
                                        print(f"\n📦 {sub_subcat['name']}: {len(sub_subcat['products'])} productos")
                                        print(f"   Primer producto: {sub_subcat['products'][0]['display_name']}")
                        else:
                            print(f"❌ Error: {subcat_response.text[:200]}")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                break
        break

