# 🚀 Cómo Iniciar el Servidor Correctamente

## ❌ Error Común

Si ves este error:
```
ModuleNotFoundError: No module named 'gen_ui_backend'
```

**Causa:** Estás ejecutando el comando desde el directorio incorrecto.

---

## ✅ Solución Paso a Paso

### Opción 1: Cambiar al Directorio Correcto (Recomendado)

```powershell
# 1. Navegar al directorio backend
cd C:\Users\ALEX\Desktop\gen-ui-pythonv3\backend

# 2. Iniciar el servidor
python -m gen_ui_backend.server
```

### Opción 2: Desde la Raíz del Proyecto

```powershell
# Desde: C:\Users\ALEX\Desktop\gen-ui-pythonv3\

# Cambiar a backend e iniciar
cd backend
python -m gen_ui_backend.server
```

---

## 📁 Estructura de Directorios

Tu estructura debería verse así:

```
C:\Users\ALEX\Desktop\gen-ui-pythonv3\
├── backend\                      👈 DEBES ESTAR AQUÍ
│   ├── gen_ui_backend\
│   │   ├── __init__.py
│   │   ├── server.py            👈 El servidor
│   │   ├── chain.py
│   │   ├── tools\
│   │   └── utils\
│   └── ...
└── frontend\
```

---

## 🎯 Verificar el Directorio Correcto

### En PowerShell:

```powershell
# Ver directorio actual
pwd

# Debería mostrar:
# Path
# ----
# C:\Users\ALEX\Desktop\gen-ui-pythonv3\backend
```

### Si estás en el directorio incorrecto:

```powershell
# Si estás en: C:\Users\ALEX\Desktop\gen-ui-pythonv3\
cd backend

# Verificar de nuevo
pwd
```

---

## 🚀 Iniciar el Servidor

### Comando Completo:

```powershell
# Paso 1: Ir al directorio
cd C:\Users\ALEX\Desktop\gen-ui-pythonv3\backend

# Paso 2: Iniciar servidor
python -m gen_ui_backend.server
```

### Salida Esperada:

```
Starting server...
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🌐 Acceder al Servidor

Una vez iniciado, el servidor estará disponible en:

- **API Documentation:** http://localhost:8000/docs
- **Chat Playground:** http://localhost:8000/chat/playground
- **API Endpoint:** http://localhost:8000/chat/invoke

---

## 🔧 Solución de Problemas

### Problema 1: ModuleNotFoundError: No module named 'gen_ui_backend'

**Causa:** Directorio incorrecto

**Solución:**
```powershell
cd C:\Users\ALEX\Desktop\gen-ui-pythonv3\backend
python -m gen_ui_backend.server
```

### Problema 2: No module named 'uvicorn' o 'fastapi'

**Causa:** Dependencias no instaladas

**Solución:**
```powershell
cd backend\gen_ui_backend
pip install -r requirements.txt
```

### Problema 3: No OPENAI_API_KEY

**Causa:** Variable de entorno no configurada

**Solución:**

Crear archivo `.env` en `backend/`:
```env
OPENAI_API_KEY=tu-api-key-aqui
```

---

## 📝 Checklist de Inicio

Antes de iniciar el servidor, verifica:

- [ ] Estás en el directorio `backend/`
  ```powershell
  pwd  # Debería mostrar: .../gen-ui-pythonv3/backend
  ```

- [ ] Dependencias instaladas
  ```powershell
  pip list | findstr "fastapi uvicorn langserve"
  ```

- [ ] Archivo `.env` configurado (opcional)
  ```powershell
  ls .env  # Debería existir
  ```

- [ ] Python 3.8+ disponible
  ```powershell
  python --version  # Debería mostrar Python 3.8+
  ```

---

## 🎯 Comando Final (Copia y Pega)

```powershell
# Todo en uno - Copia esta línea completa:
cd C:\Users\ALEX\Desktop\gen-ui-pythonv3\backend; python -m gen_ui_backend.server
```

---

## 🔥 Tips Adicionales

### Detener el Servidor
```
CTRL + C  (en la terminal donde corre el servidor)
```

### Verificar que el Servidor Está Corriendo
```powershell
# En otra terminal:
curl http://localhost:8000/docs
# O abrir en el navegador
```

### Logs del Servidor
Los logs aparecerán automáticamente en la terminal donde ejecutaste el servidor.

---

## ✅ Resumen Rápido

```powershell
# 1. Ir al directorio correcto
cd C:\Users\ALEX\Desktop\gen-ui-pythonv3\backend

# 2. Verificar que estás en el lugar correcto
pwd

# 3. Iniciar el servidor
python -m gen_ui_backend.server

# 4. Abrir en el navegador
# http://localhost:8000/docs
```

---

**📌 IMPORTANTE:** Siempre ejecuta el servidor desde el directorio `backend/`, no desde la raíz del proyecto.

---

**Fecha:** 6 de Octubre, 2025  
**Estado:** ✅ DOCUMENTADO

