# Mejora en la Detección de Cantidades

## 📋 Resumen

Se han implementado mejoras significativas en el **Agente 1 (Clasificador)** para mejorar la detección de cantidades de productos solicitados por el usuario.

## 🔧 Cambios Realizados

### 1. Mejoras en el Prompt del GPT-4o (`chain.py`)

**Antes:**
- Prompt básico que pedía detectar cantidades
- Sin ejemplos específicos
- Instrucciones generales

**Después:**
- Prompt detallado con reglas explícitas sobre cómo detectar cantidades
- **5 patrones específicos** mencionados:
  - Números antes/después del producto: "2 leches", "leche x 3"
  - Cantidades en texto: "dos", "tres", "cuatro"
  - Patrones con "de": "3 de leche", "2 de pan"
  - Detección individual por producto en listas
- **3 ejemplos prácticos** incluidos en el prompt
- Instrucciones claras sobre cuándo asignar cantidad 1 por defecto

### 2. Mejoras en los Patrones Regex (`clasificador_intencion.py`)

#### Expansión del Diccionario de Números
```python
# Antes: 1-10 + media/medio
# Después: 1-20 + variaciones con acento
NUMEROS_TEXTO = {
    "un": 1, "una": 1, "uno": 1,
    "dos": 2, "tres": 3, ..., "veinte": 20,
    "dieciseis": 16, "dieciséis": 16,  # Con y sin acento
    "media": 0.5, "medio": 0.5
}
```

#### Implementación de 5 Patrones de Detección

Los patrones se evalúan en orden hasta encontrar una coincidencia:

1. **Patrón número antes del producto**
   - Ejemplos: `"2 leches"`, `"3 panes"`, `"5 huevos"`
   - Regex: `(\d+)\s*(?:de\s+)?{producto}s?`
   - Soporta plural automáticamente

2. **Patrón texto número antes del producto**
   - Ejemplos: `"dos leches"`, `"tres panes"`, `"cinco huevos"`
   - Regex: `(dos|tres|cuatro...)\s*(?:de\s+)?{producto}s?`
   - Convierte texto a número

3. **Patrón "x" después del producto**
   - Ejemplos: `"leche x 2"`, `"pan x3"`, `"huevos x 5"`
   - Regex: `{producto}s?\s*x\s*(\d+)`
   - Soporta con o sin espacios

4. **Patrón con "de"**
   - Ejemplos: `"3 de leche"`, `"cinco de pan"`
   - Regex: `(\d+|dos|tres...)\s+de\s+{producto}s?`
   - Soporta números y texto

5. **Patrón de proximidad (fallback)**
   - Busca el número más cercano antes del producto
   - Útil para listas: `"2 leches, 3 panes, 4 huevos"`
   - Analiza hasta 20 caracteres antes del producto

#### Mejoras en el Procesamiento
- **Escapado de caracteres especiales** en nombres de productos
- **Flags de cantidad encontrada** para evitar conflictos entre patrones
- **Logging detallado** de qué patrón detectó cada cantidad
- **Manejo robusto** de plurales y variaciones

## ✅ Casos de Uso Soportados

El sistema ahora detecta correctamente cantidades en estos formatos:

```python
✅ "quiero 2 leches"                           → leche: 2
✅ "dame 3 panes y 2 leches"                   → pan: 3, leche: 2
✅ "necesito tres leches, dos panes y cinco huevos" → leche: 3, pan: 2, huevos: 5
✅ "comprar leche x 4 y pan x 2"               → leche: 4, pan: 2
✅ "3 de leche y 5 de pan"                     → leche: 3, pan: 5
✅ "quiero cinco de leche"                     → leche: 5
✅ "dame 10 huevos y 6 leches"                 → huevos: 10, leche: 6
✅ "necesito leche"                            → leche: 1 (por defecto)
✅ "2 leches, 3 panes, 4 huevos"               → leche: 2, pan: 3, huevos: 4
```

## 🧪 Tests

Se ha creado un archivo de tests completo: `backend/gen_ui_backend/test/test_cantidades.py`

**Resultado:** ✅ **9/9 tests pasados (100% success rate)**

## 📊 Flujo de Detección

```
Usuario: "quiero 2 leches, 3 panes y 5 huevos"
                    ↓
┌──────────────────────────────────────────────┐
│  GPT-4o (con prompt mejorado)                │
│  - Analiza el mensaje completo               │
│  - Entiende contexto semántico               │
│  - Llama a clasificar_intencion              │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  clasificar_intencion (patrones regex)       │
│  1. Busca productos comunes                  │
│  2. Para cada producto:                      │
│     - Patrón 1: número antes                 │
│     - Patrón 2: texto antes                  │
│     - Patrón 3: x después                    │
│     - Patrón 4: "de" patrón                  │
│     - Patrón 5: proximidad                   │
└──────────────────────────────────────────────┘
                    ↓
         Resultado Estructurado
┌──────────────────────────────────────────────┐
│  {                                           │
│    "productos": ["leche", "pan", "huevos"],  │
│    "cantidades": {                           │
│      "leche": 2,                             │
│      "pan": 3,                               │
│      "huevos": 5                             │
│    }                                         │
│  }                                           │
└──────────────────────────────────────────────┘
```

## 🚀 Cómo Usar

El sistema funciona automáticamente. Simplemente envía mensajes como:
- "quiero 3 leches"
- "dame 5 panes y 2 huevos"
- "necesito tres de leche"

El agente clasificador detectará correctamente las cantidades y las pasará al agente buscador y calculador.

## 📝 Notas

- **Doble capa de detección:** GPT-4o + Regex para máxima precisión
- **Fallback inteligente:** Si no se especifica cantidad, asigna 1 por defecto
- **Logging detallado:** Para debugging y monitoreo
- **Soporta variaciones:** Plurales, con/sin espacios, diferentes formatos
- **Expandible:** Fácil agregar más patrones o números

## 🔍 Debug

Para ver cómo se detectan las cantidades, el sistema imprime logs como:

```
📊 [Patrón número antes] leche: 2
📊 [Patrón texto antes] pan: 3
📊 [Patrón x después] huevos: 5
📊 [Por defecto] agua: 1
```

Esto permite identificar rápidamente qué patrón se usó para cada producto.

