# 📁 Refactorización del Código Multi-Agente

## 📋 Resumen

Se ha reorganizado el código del sistema multi-agente para mejorar la mantenibilidad y seguir mejores prácticas de organización de código.

## 🎯 Objetivo

Dividir el monolítico archivo `chain.py` en módulos más pequeños y organizados, donde:
- Cada agente tiene su propio archivo
- El estado compartido está en un módulo dedicado
- El grafo está claramente definido en un archivo separado
- Se mantiene la retrocompatibilidad con código existente

## 📂 Nueva Estructura

```
backend/gen_ui_backend/
├── agents/
│   ├── __init__.py              # Exporta todos los agentes y el estado
│   ├── state.py                 # MultiAgentState - Estado compartido
│   ├── agente_clasificador.py  # Agente 1: Clasificador de intención
│   ├── agente_buscador.py       # Agente 2: Buscador en Mercadona API
│   ├── agente_calculador.py    # Agente 3: Calculador de precios
│   └── nodo_final.py            # Nodo final de respuesta con streaming
├── graph.py                     # Definición y construcción del grafo
└── chain.py                     # [DEPRECATED] Mantiene retrocompatibilidad
```

## 📝 Descripción de Archivos

### 1. `agents/state.py`
Define el `MultiAgentState` (TypedDict) que contiene:
- Mensajes del usuario y sistema
- Datos del Agente 1 (intención, productos, cantidades)
- Datos del Agente 2 (productos encontrados/no encontrados)
- Datos del Agente 3 (precio_info, ticket, archivos)
- Control de flujo (current_agent, final_result)

### 2. `agents/agente_clasificador.py`
**Agente 1: Clasificador de Intención**
- Analiza el mensaje del usuario
- Clasifica la intención (compra/consulta)
- Extrae productos mencionados
- Detecta cantidades exactas
- Usa GPT-4o con tool calling

### 3. `agents/agente_buscador.py`
**Agente 2: Buscador de Productos**
- Busca productos en la API de Mercadona
- Extrae información de precios y disponibilidad
- Separa productos encontrados vs no encontrados
- Maneja errores de búsqueda

### 4. `agents/agente_calculador.py`
**Agente 3: Calculador de Precios**
- Calcula el precio total de la compra
- Genera el ticket de compra formateado
- Crea archivos descargables (JSON, TXT, CSV)
- Construye mensaje consolidado con info de los 3 agentes

### 5. `agents/nodo_final.py`
**Nodo Final de Respuesta**
- Genera respuesta usando GPT-3.5-turbo para streaming
- Actúa como "eco" para devolver el mensaje procesado
- Permite que el frontend capture eventos de streaming

### 6. `agents/__init__.py`
Exporta todos los componentes para facilitar imports:
```python
from gen_ui_backend.agents import (
    MultiAgentState,
    agente_1_clasificador,
    agente_2_buscador,
    agente_3_calculador,
    nodo_respuesta_final,
)
```

### 7. `graph.py`
Define la construcción del grafo multi-agente:
- `create_multi_agent_graph()`: Crea el grafo principal
- `create_graph()`: Función legacy para retrocompatibilidad

**Flujo del Grafo:**
```
START 
  ↓
Agente 1: Clasificador
  ↓
Agente 2: Buscador
  ↓
Agente 3: Calculador
  ↓
Nodo Final: Respuesta
  ↓
END
```

### 8. `chain.py` [DEPRECATED]
Mantiene retrocompatibilidad importando desde los nuevos módulos.
Se recomienda usar los nuevos imports:
```python
# ✅ Nuevo (recomendado)
from gen_ui_backend.graph import create_multi_agent_graph
from gen_ui_backend.agents import MultiAgentState

# ❌ Legacy (funciona pero deprecated)
from gen_ui_backend.chain import create_multi_agent_graph
```

## 🔄 Archivos Actualizados

Los siguientes archivos fueron actualizados para usar los nuevos imports:

1. `test_multi_agent_flow.py` - Test del flujo completo
2. `server.py` - Servidor FastAPI
3. `utils/visualizar_sistema.py` - Visualización del sistema
4. `test/test_multi_agent.py` - Tests de agentes

## ✅ Validación

### Test Exitoso
```bash
python -m gen_ui_backend.test_multi_agent_flow 1
```

**Resultado:** ✅ Prueba completada exitosamente
- Agente 1: Clasificó correctamente "Quiero 2 leches y un pan"
- Agente 2: Encontró 2 productos en Mercadona
- Agente 3: Calculó total de 2.01€ y generó archivos

### Retrocompatibilidad
El código antiguo que importaba desde `chain.py` sigue funcionando correctamente gracias al módulo de compatibilidad.

## 🎨 Beneficios de la Refactorización

1. **Modularidad**: Cada agente es independiente y fácil de modificar
2. **Mantenibilidad**: Código más fácil de leer y mantener
3. **Testabilidad**: Se puede probar cada agente por separado
4. **Escalabilidad**: Fácil agregar nuevos agentes
5. **Organización**: Estructura clara y lógica
6. **Reutilización**: Los agentes pueden ser usados en otros contextos
7. **Retrocompatibilidad**: No rompe código existente

## 📚 Cómo Usar la Nueva Estructura

### Importar el grafo:
```python
from gen_ui_backend.graph import create_multi_agent_graph

graph = create_multi_agent_graph()
result = graph.invoke({"messages": [HumanMessage(content="Quiero 2 leches")]})
```

### Importar agentes individuales:
```python
from gen_ui_backend.agents import (
    agente_1_clasificador,
    agente_2_buscador,
    agente_3_calculador
)
```

### Importar el estado:
```python
from gen_ui_backend.agents import MultiAgentState

estado: MultiAgentState = {
    "messages": [HumanMessage(content="...")],
    "intencion": None,
    # ...
}
```

## 🚀 Siguientes Pasos

La refactorización está completa y probada. El sistema mantiene toda su funcionalidad original con una estructura mucho más organizada y profesional.

---

**Fecha de Refactorización:** 06/10/2025  
**Versión:** 1.0  
**Estado:** ✅ Completado y Validado

