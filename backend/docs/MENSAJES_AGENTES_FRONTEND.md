# Mensajes de Agentes en Frontend - SOLUCIÓN FINAL

## Problema Original

Los mensajes informativos de los agentes solo aparecían en la consola del backend pero no llegaban al frontend. El error era:

```
Error: Only plain objects, and a few built-ins, can be passed to Client Components from Server Components. 
Classes or null prototypes are not supported.
```

Este error se producía porque los objetos `AIMessage` de LangChain son clases que no pueden serializarse para React Server Components.

## Solución Implementada

### Resumen

La solución final combina dos elementos:

1. **Mensaje consolidado**: El Agente 3 genera UN mensaje final con toda la información de los 3 agentes
2. **Nodo de respuesta final**: Usa el modelo de chat para generar eventos de streaming que el frontend captura
3. **Serialización JSON**: Convierte el `lastEvent` a JSON plano para evitar errores de serialización RSC

### Backend: Mensaje Consolidado + Nodo Final

#### 1. Agente 3 genera mensaje consolidado

El Agente 3 recopila información de todos los agentes y genera un mensaje completo:

```python
def agente_3_calculador(state, config):
    # ... cálculos ...
    
    # Mensaje consolidado con información de los 3 agentes
    mensaje_consolidado = f"""🔄 **PROCESO COMPLETADO**

---

📋 **AGENTE 1: CLASIFICADOR**
- Intención detectada: **{intencion}**
- Productos solicitados: **{len(productos)}**

---

🔍 **AGENTE 2: BUSCADOR**
- Productos encontrados: **{len(productos_encontrados)}**
  ✓ {producto.nombre} - {producto.precio}€

---

💰 **AGENTE 3: CALCULADOR**
- Subtotal: {subtotal}€
- **TOTAL: {total}€**

---

{ticket_completo}

¿Deseas confirmar la compra?
"""
    
    return Command(
        goto="respuesta_final",
        update={"final_result": mensaje_consolidado}
    )
```

#### 2. Nodo de Respuesta Final

Este nodo usa el modelo de chat para generar eventos de streaming:

```python
def nodo_respuesta_final(state, config):
    final_result = state.get("final_result", "No se pudo procesar la solicitud")
    
    # El modelo "repite" el mensaje, pero genera eventos de streaming
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Devuelve el siguiente mensaje exactamente como está."),
        ("human", "{mensaje}")
    ])
    
    chain = prompt | model
    response = chain.invoke({"mensaje": final_result}, config)
    
    return Command(goto="__end__", update={"messages": [response]})
```

**¿Por qué funciona?**
- El modelo genera eventos `on_chat_model_stream` mientras procesa
- El frontend YA tiene un handler para estos eventos
- El modelo simplemente "repite" el mensaje (temperatura=0)
- Genera streaming real con efecto "typing"

### Frontend: Serialización JSON del lastEvent

#### Fix en `frontend/utils/server.tsx`

```typescript
// Serialize to plain JSON to avoid RSC serialization errors
const serializedValue = resolveValue ? JSON.parse(JSON.stringify(resolveValue)) : null;
resolve(serializedValue);
```

**¿Por qué funciona?**
- `JSON.stringify()` convierte clases de LangChain a string
- `JSON.parse()` reconstruye como **plain object** (sin prototipos ni clases)
- Esto elimina el error "Only plain objects can be passed..."

## Flujo Completo

```
Usuario: "Quiero comprar leche"
    ↓
[AGENTE 1: CLASIFICADOR]
    → Clasifica intención
    → Extrae productos y cantidades
    ↓
[AGENTE 2: BUSCADOR]
    → Busca en API de Mercadona
    → Encuentra productos con precios
    ↓
[AGENTE 3: CALCULADOR]
    → Calcula totales
    → Genera ticket
    → Crea mensaje consolidado con INFO DE LOS 3 AGENTES
    ↓
[NODO RESPUESTA FINAL]
    → Usa modelo de chat para streaming
    → Genera eventos on_chat_model_stream
    ↓
[FRONTEND]
    → Captura eventos de streaming
    → Muestra mensaje con efecto typing
    → Serializa lastEvent a JSON plano
```

## Ejemplo de Mensaje Final

```
🔄 PROCESO COMPLETADO

---

📋 AGENTE 1: CLASIFICADOR
- Intención detectada: **compra**
- Productos solicitados: **1**

---

🔍 AGENTE 2: BUSCADOR
- Productos encontrados: **1**
  ✓ Leche desnatada Hacendado - 0.84€

---

💰 AGENTE 3: CALCULADOR
- Subtotal: 0.84€
- **TOTAL: 0.84€**

---

╔═══════════════════════════════════════════════════════╗
║              MERCADONA - TICKET DE COMPRA             ║
╚═══════════════════════════════════════════════════════╝

Fecha: 06/10/2025 14:30:15

───────────────────────────────────────────────────────
PRODUCTOS
───────────────────────────────────────────────────────
1. Leche desnatada Hacendado
   Botella 1L
   1 x 0.84€ = 0.84€

───────────────────────────────────────────────────────
RESUMEN
───────────────────────────────────────────────────────
TOTAL A PAGAR:       0.84€
═══════════════════════════════════════════════════════

¿Deseas confirmar la compra?
```

## Ventajas de Esta Solución

1. ✅ **Sin errores RSC**: La serialización JSON elimina objetos de clase
2. ✅ **Un solo mensaje consolidado**: Más fácil de leer para el usuario
3. ✅ **Streaming real**: El modelo genera eventos que el frontend captura
4. ✅ **Usa infraestructura existente**: No requiere cambios mayores
5. ✅ **Información completa**: Muestra el trabajo de los 3 agentes
6. ✅ **Formato rico**: Markdown, emojis, ticket ASCII formateado
7. ✅ **Sin cambios complejos**: No requiere LangGraph SDK client

## Archivos Modificados

### Backend
- `backend/gen_ui_backend/chain.py`:
  - `agente_3_calculador()` - Genera mensaje consolidado con info de los 3 agentes
  - **Nuevo:** `nodo_respuesta_final()` - Usa modelo de chat para streaming
  - `create_multi_agent_graph()` - Agregado nodo `respuesta_final` al grafo
  - Todos los agentes ahora van a `respuesta_final` en lugar de `__end__`

### Frontend
- `frontend/utils/server.tsx`:
  - Agregada serialización JSON del `lastEvent` para evitar errores RSC
- `frontend/app/agent.tsx`:
  - Sin cambios (usa los handlers existentes)

## Testing

1. Iniciar el backend:
   ```bash
   cd backend
   python -m gen_ui_backend.server
   ```

2. Iniciar el frontend:
   ```bash
   cd frontend
   yarn dev
   ```

3. Abrir http://localhost:3000 y la consola del navegador (F12)

4. Enviar: "Quiero comprar leche"

5. Verificar:
   - ✅ NO hay error "Only plain objects..." en consola
   - ✅ Aparece UN mensaje consolidado con toda la información
   - ✅ El mensaje muestra:
     - Información del Agente 1 (clasificación)
     - Información del Agente 2 (búsqueda)
     - Información del Agente 3 (cálculo y ticket)
   - ✅ Tiene efecto de "typing" (streaming)

## ¿Por Qué get_stream_writer() No Funcionó?

`get_stream_writer()` es la solución recomendada por LangGraph, PERO:

- `RemoteRunnable.streamEvents()` no captura eventos custom de LangGraph
- Se necesitaría usar `LangGraph SDK Client` con `stream_mode="custom"`
- Esto requiere cambios mayores en el cliente y configuración de LangServe
- La solución del nodo final es más simple y funciona con RemoteRunnable

## Referencias

- [LangGraph Streaming Documentation](https://langchain-ai.github.io/langgraph/how-tos/streaming/)
- [React Server Components Serialization](https://nextjs.org/docs/app/building-your-application/rendering/server-components#passing-props-from-server-to-client-components-serialization)
