# Sistema de Tickets Descargables

## 📋 Resumen

Se ha implementado un sistema completo para mostrar listas de compra y generar tickets descargables en múltiples formatos.

## ✨ Nuevas Funcionalidades

### 1. Tabla de Productos en el Chat

Cuando el usuario solicita productos, el sistema ahora muestra una **tabla visual** en el chat con:

- **Producto**: Nombre completo del producto
- **Cantidad**: Unidades solicitadas
- **Precio Unitario**: Precio por unidad
- **Precio Total**: Precio total (cantidad × precio unitario)

La tabla se genera automáticamente en formato Markdown y se muestra en el chat.

### 2. Archivos Descargables

El sistema genera automáticamente **3 formatos de archivo** para cada compra:

#### 📄 JSON (`ticket_YYYYMMDD_HHMMSS.json`)
```json
{
  "fecha": "06/10/2025 15:30:45",
  "timestamp": "20251006_153045",
  "resumen": {
    "articulos_diferentes": 3,
    "unidades_totales": 7,
    "subtotal": 15.50,
    "descuentos": 0.00,
    "total": 15.50
  },
  "productos": [
    {
      "producto_id": "12345",
      "nombre": "Leche Entera Hacendado 1L",
      "cantidad": 2,
      "precio_unitario": 0.95,
      "precio_total": 1.90,
      "packaging": "1 L",
      "categoria": "Lácteos"
    }
  ]
}
```

#### 📝 TXT (`ticket_YYYYMMDD_HHMMSS.txt`)
```
╔═══════════════════════════════════════════════════════╗
║              MERCADONA - TICKET DE COMPRA             ║
╚═══════════════════════════════════════════════════════╝

Fecha: 06/10/2025 15:30:45

───────────────────────────────────────────────────────
PRODUCTOS
───────────────────────────────────────────────────────
1. Leche Entera Hacendado 1L
   1 L
   2 x 0.95€ = 1.90€

───────────────────────────────────────────────────────
RESUMEN
───────────────────────────────────────────────────────
Artículos diferentes: 3
Unidades totales: 7

Subtotal:           15.50€
Descuentos:          0.00€
───────────────────────────────────────────────────────
TOTAL A PAGAR:      15.50€
═══════════════════════════════════════════════════════
```

#### 📊 CSV (`ticket_YYYYMMDD_HHMMSS.csv`)
```csv
MERCADONA - TICKET DE COMPRA
Fecha: 06/10/2025 15:30:45

Nº,Producto,Cantidad,Precio Unitario (€),Precio Total (€),Packaging
1,Leche Entera Hacendado 1L,2,0.95,1.90,1 L

RESUMEN
Artículos diferentes,3
Unidades totales,7

Subtotal,15.50€
Descuentos,0.00€
TOTAL A PAGAR,15.50€
```

### 3. Interfaz de Descarga

El frontend incluye un **componente visual** que muestra:

- ✅ Tabla completa de productos con estilo moderno
- 💰 Resumen de precios (subtotal, descuentos, total)
- 📥 Botones de descarga para cada formato (JSON, TXT, CSV)
- 🎨 Diseño responsive y atractivo

## 🔧 Arquitectura Técnica

### Backend

#### 1. Nueva Herramienta: `generador_archivos.py`

```python
from gen_ui_backend.tools.generador_archivos import generar_archivos_ticket

# Genera archivos en 3 formatos
resultado = generar_archivos_ticket.invoke({
    "productos": productos,
    "cantidades": cantidades,
    "precio_info": precio_info
})
```

**Retorna:**
```python
{
    "json_path": "/ruta/absoluta/ticket_20251006_153045.json",
    "txt_path": "/ruta/absoluta/ticket_20251006_153045.txt",
    "csv_path": "/ruta/absoluta/ticket_20251006_153045.csv",
    "timestamp": "20251006_153045",
    "success": True
}
```

#### 2. Modificaciones en `chain.py`

El `agente_3_calculador` ahora:

1. Calcula precios
2. Genera ticket de texto
3. **NUEVO**: Genera archivos descargables
4. **NUEVO**: Crea tabla Markdown para el chat
5. Incluye rutas de archivos en el mensaje final

#### 3. Endpoint de Descarga en `server.py`

```python
@app.get("/download/{filename}")
async def download_ticket(filename: str):
    """Descarga archivos del directorio 'tickets'"""
    # Validaciones de seguridad
    # Retorna FileResponse con el archivo
```

**Seguridad:**
- ✅ Valida que el archivo exista
- ✅ Verifica que esté dentro del directorio permitido
- ✅ Protege contra path traversal attacks

### Frontend

#### 1. Nuevo Componente: `ticket-compra.tsx`

```tsx
<TicketCompra 
  ticketData={{
    items: [...],
    subtotal: 15.50,
    descuentos: 0.00,
    total: 15.50,
    num_items: 3,
    num_productos: 7
  }}
  archivos={{
    json_path: "...",
    txt_path: "...",
    csv_path: "..."
  }}
/>
```

**Características:**
- 🎨 Diseño con Tailwind CSS
- 📱 Responsive
- ⚡ Descarga asíncrona con fetch API
- 🔄 Manejo de errores

#### 2. Parsing Inteligente en `message.tsx`

El componente `AIMessage` ahora:

1. Detecta automáticamente si el mensaje contiene un ticket
2. Parsea la tabla Markdown y extrae datos
3. Extrae rutas de archivos
4. Renderiza el componente `TicketCompra` si corresponde

## 🚀 Flujo de Uso

### Usuario solicita productos

```
Usuario: "Quiero 2 leches, 3 panes y 1 aceite"
```

### El Sistema Procesa

1. **Agente 1 (Clasificador)**: Detecta intención de compra y cantidades
2. **Agente 2 (Buscador)**: Busca productos en Mercadona API
3. **Agente 3 (Calculador)**: 
   - Calcula precios
   - Genera tabla Markdown
   - **Genera archivos en tickets/**
   - Incluye rutas en respuesta

### Frontend Muestra

1. Mensaje con resumen del proceso
2. **Tabla visual de productos**
3. **Componente de ticket con botones de descarga**

### Usuario Descarga

1. Click en botón (JSON/TXT/CSV)
2. Fetch a `/download/{filename}`
3. Browser descarga el archivo

## 📁 Estructura de Archivos

```
backend/
├── gen_ui_backend/
│   ├── tools/
│   │   ├── generador_archivos.py  ← NUEVO
│   │   └── calculador_ticket.py
│   ├── chain.py                    ← MODIFICADO
│   └── server.py                   ← MODIFICADO
└── tickets/                        ← NUEVO (generado automáticamente)
    ├── ticket_20251006_153045.json
    ├── ticket_20251006_153045.txt
    └── ticket_20251006_153045.csv

frontend/
├── components/
│   └── prebuilt/
│       └── ticket-compra.tsx       ← NUEVO
└── ai/
    └── message.tsx                 ← MODIFICADO
```

## 🔄 Formato de Datos

### `TicketData` (Frontend)

```typescript
interface TicketData {
  items: ProductoItem[];
  subtotal: number;
  descuentos: number;
  total: number;
  num_items: number;
  num_productos: number;
}

interface ProductoItem {
  nombre: string;
  cantidad: number;
  precio_unitario: number;
  precio_total: number;
  packaging?: string;
  categoria?: string;
}
```

### `precio_info` (Backend)

```python
{
    "subtotal": float,
    "descuentos": float,
    "total": float,
    "items": [
        {
            "producto_id": str,
            "nombre": str,
            "producto_buscado": str,
            "cantidad": int,
            "precio_unitario": float,
            "precio_total": float,
            "packaging": str,
            "categoria": str
        }
    ],
    "num_items": int,
    "num_productos": int
}
```

## 🧪 Testing

### Probar la Funcionalidad

1. **Iniciar Backend:**
   ```bash
   cd backend
   python -m gen_ui_backend.server
   ```

2. **Iniciar Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Realizar Compra:**
   ```
   "Quiero 2 leches y 3 panes"
   ```

4. **Verificar:**
   - ✅ Tabla de productos aparece en el chat
   - ✅ Componente de ticket se renderiza
   - ✅ Archivos se generan en `backend/tickets/`
   - ✅ Botones de descarga funcionan
   - ✅ Archivos se descargan correctamente

## 📊 Ejemplo de Salida Completa

```markdown
🔄 **PROCESO COMPLETADO**

---

📋 **AGENTE 1: CLASIFICADOR**
- Intención detectada: **compra**
- Productos solicitados: **3**

---

🔍 **AGENTE 2: BUSCADOR**
- Productos encontrados: **3**
  ✓ Leche Entera Hacendado - 0.95€
  ✓ Pan de Molde Integral - 1.25€
  ✓ Aceite de Oliva Virgen Extra - 4.50€

---

💰 **AGENTE 3: CALCULADOR**
- Subtotal: 15.50€
- Descuentos: 0.00€
- **TOTAL: 15.50€**

---

📦 **LISTA DE LA COMPRA**

| Nº | Producto | Cantidad | Precio Unit. | Precio Total |
|---|---|---|---|---|
| 1 | Leche Entera Hacendado 1L | 2 | 0.95€ | **1.90€** |
| 2 | Pan de Molde Integral 450g | 3 | 1.25€ | **3.75€** |
| 3 | Aceite de Oliva Virgen Extra 1L | 1 | 4.50€ | **4.50€** |

---

📥 **ARCHIVOS DESCARGABLES**

Los archivos del ticket han sido generados y están listos para descargar:

- 📄 **JSON**: `C:\...\tickets\ticket_20251006_153045.json`
- 📝 **TXT**: `C:\...\tickets\ticket_20251006_153045.txt`
- 📊 **CSV**: `C:\...\tickets\ticket_20251006_153045.csv`

---

[TICKET COMPLETO EN FORMATO TEXTO...]
```

## 🎯 Ventajas del Sistema

1. **Múltiples Formatos**: JSON para APIs, TXT para impresión, CSV para Excel
2. **Persistencia**: Los archivos se guardan localmente
3. **Compartible**: Fácil de enviar por email o compartir
4. **Imprimible**: Formato TXT optimizado para impresión
5. **Procesable**: JSON/CSV para análisis de datos
6. **Visual**: Componente atractivo en el chat
7. **Seguro**: Validaciones en el backend

## 🔒 Consideraciones de Seguridad

- ✅ Path traversal protection en el endpoint de descarga
- ✅ Validación de extensiones de archivo
- ✅ Archivos solo accesibles desde directorio específico
- ✅ CORS configurado correctamente
- ✅ No se exponen rutas absolutas del sistema al cliente

## 🚀 Mejoras Futuras

- [ ] Envío de tickets por email
- [ ] Generación de PDF
- [ ] Historial de compras
- [ ] Compartir tickets por link
- [ ] Integración con calendario
- [ ] Exportar a Google Sheets
- [ ] Vista previa antes de descargar
- [ ] Comprimir múltiples tickets en ZIP

## 📝 Notas

- Los archivos se generan con timestamp único para evitar conflictos
- El directorio `tickets/` se crea automáticamente si no existe
- Los archivos antiguos deben limpiarse manualmente o con script
- Compatible con Windows, Linux y macOS

