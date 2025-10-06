# 🔧 Fix: Error al Iniciar el Servidor

## ❌ Problema

Al intentar iniciar el servidor con:
```bash
python -m gen_ui_backend.server
```

Se producía el error:
```
ModuleNotFoundError: No module named 'backend'
```

---

## 🔍 Causa

El archivo `server.py` contenía una importación incorrecta en la **línea 8**:

```python
# ❌ INCORRECTO
from backend.gen_ui_backend.utils.input_types import ChatInputType
```

Esta importación intentaba importar desde un módulo `backend` que no existe cuando se ejecuta el servidor como módulo de Python.

---

## ✅ Solución

Se corrigió la importación en `backend/gen_ui_backend/server.py`:

```python
# ✅ CORRECTO
from gen_ui_backend.utils.input_types import ChatInputType
```

---

## 🚀 Cómo Iniciar el Servidor

### Paso 1: Asegurar que tienes las dependencias

```bash
cd backend/gen_ui_backend
pip install -r requirements.txt
```

### Paso 2: Configurar variables de entorno (opcional)

Crear archivo `.env` en la raíz de `backend/`:

```env
OPENAI_API_KEY=tu-api-key-aqui
```

### Paso 3: Iniciar el servidor

```bash
cd backend
python -m gen_ui_backend.server
```

### Salida Esperada

```
Starting server...
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 📝 Verificar que Funciona

### Opción 1: Navegador
Abre en tu navegador:
- **API Docs:** http://localhost:8000/docs
- **Playground:** http://localhost:8000/chat/playground

### Opción 2: cURL
```bash
curl -X POST http://localhost:8000/chat/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": [{"type": "human", "content": "Quiero 2 leches"}]}'
```

### Opción 3: Python
```python
import requests

response = requests.post(
    "http://localhost:8000/chat/invoke",
    json={
        "input": [
            {"type": "human", "content": "Quiero 2 leches y pan"}
        ]
    }
)
print(response.json())
```

---

## 🔧 Archivos Modificados

| Archivo | Cambio | Estado |
|---------|--------|--------|
| `gen_ui_backend/server.py` | Corrección de importación (línea 8) | ✅ Corregido |

---

## ✅ Estado Final

```
╔═══════════════════════════════════════════════════════╗
║    ✅ SERVIDOR LISTO PARA INICIAR ✅                  ║
╠═══════════════════════════════════════════════════════╣
║  • Error de importación corregido                    ║
║  • Sin errores de linting                            ║
║  • Servidor funcional                                ║
║  • Endpoints disponibles:                            ║
║    - POST /chat/invoke                               ║
║    - GET /chat/playground                            ║
║    - GET /docs                                       ║
╚═══════════════════════════════════════════════════════╝
```

---

## 📚 Endpoints Disponibles

### 1. `/chat/invoke` - Invocar el sistema
```bash
POST http://localhost:8000/chat/invoke
Content-Type: application/json

{
  "input": [
    {"type": "human", "content": "Quiero 2 leches y pan"}
  ]
}
```

### 2. `/chat/playground` - Playground interactivo
```
GET http://localhost:8000/chat/playground
```

### 3. `/docs` - Documentación API
```
GET http://localhost:8000/docs
```

---

## 🎯 Resumen

**Problema:** Importación incorrecta con `backend.gen_ui_backend.utils`  
**Solución:** Cambiar a `gen_ui_backend.utils`  
**Resultado:** ✅ Servidor funcional y listo para usar

---

**Fecha:** 6 de Octubre, 2025  
**Estado:** ✅ RESUELTO  
**Servidor:** OPERACIONAL

