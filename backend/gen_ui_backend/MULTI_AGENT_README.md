# Sistema Multi-Agente para Compra en Mercadona

## 📋 Descripción

Sistema de agentes inteligentes basado en LangGraph que permite gestionar compras en Mercadona mediante un flujo automatizado de tres agentes especializados.

## 🏗️ Arquitectura

El sistema implementa una arquitectura **Custom Multi-Agent Workflow** siguiendo las mejores prácticas de [LangGraph](https://langchain-ai.github.io/langgraph/concepts/multi_agent/#network).

### Agentes

```
┌─────────────────────────────────────────────────────────────────┐
│                    SISTEMA MULTI-AGENTE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  START                                                           │
│    │                                                             │
│    ▼                                                             │
│  ┌──────────────────────────────────────────┐                   │
│  │  AGENTE 1: Clasificador                   │                   │
│  │  - Clasifica intención del usuario        │                   │
│  │  - Extrae productos mencionados           │                   │
│  │  - Detecta cantidades                     │                   │
│  └──────────────┬───────────────────────────┘                   │
│                 │                                                │
│                 ▼                                                │
│  ┌──────────────────────────────────────────┐                   │
│  │  AGENTE 2: Buscador                       │                   │
│  │  - Busca productos en API Mercadona       │                   │
│  │  - Verifica disponibilidad                │                   │
│  │  - Obtiene precios                        │                   │
│  └──────────────┬───────────────────────────┘                   │
│                 │                                                │
│                 ▼                                                │
│  ┌──────────────────────────────────────────┐                   │
│  │  AGENTE 3: Calculador                     │                   │
│  │  - Calcula precios totales                │                   │
│  │  - Aplica descuentos                      │                   │
│  │  - Genera ticket de compra                │                   │
│  └──────────────┬───────────────────────────┘                   │
│                 │                                                │
│                 ▼                                                │
│                END                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Estado Compartido

El sistema utiliza un estado compartido (`MultiAgentState`) que contiene:

- **messages**: Lista de mensajes entre agentes
- **intencion**: Intención clasificada (compra, consulta, etc.)
- **productos_mencionados**: Lista de productos del usuario
- **cantidades**: Diccionario producto → cantidad
- **productos_encontrados**: Productos disponibles en Mercadona
- **productos_no_encontrados**: Productos no disponibles
- **precio_info**: Información de precios y descuentos
- **ticket**: Ticket de compra generado
- **final_result**: Resultado final del sistema

## 🛠️ Herramientas (Tools)

### 1. Clasificador de Intención (`clasificador_intencion.py`)

```python
@tool
def clasificar_intencion(user_input: str) -> Dict[str, any]:
    """
    Clasifica la intención del usuario y extrae productos.
    
    Returns:
        - intencion: tipo de intención
        - productos: lista de productos
        - cantidad: dict producto → cantidad
    """
```

**TODO**: Implementar lógica de clasificación con NLP.

### 2. Buscador de Mercadona (`buscador_mercadona.py`)

```python
@tool
def buscar_producto_mercadona(producto: str) -> Dict[str, any]:
    """Busca un producto en la API de Mercadona."""

@tool
def buscar_multiples_productos(productos: List[str]) -> List[Dict]:
    """Busca múltiples productos en paralelo."""
```

**TODO**: 
- Implementar integración con API de Mercadona
- Manejar rate limiting
- Implementar caché de productos

### 3. Calculador de Ticket (`calculador_ticket.py`)

```python
@tool
def calcular_precio_total(productos: List[Dict], cantidades: Dict) -> Dict:
    """Calcula subtotal, descuentos y total."""

@tool
def generar_ticket_compra(...) -> str:
    """Genera ticket formateado."""
```

**TODO**:
- Implementar lógica de cálculo de precios
- Aplicar descuentos y promociones
- Formatear ticket con estilo Mercadona

## 🚀 Uso

### Instalación

```bash
cd backend
pip install -r gen_ui_backend/requirements.txt
```

### Uso Básico

```python
from langchain_core.messages import HumanMessage
from gen_ui_backend.chain import create_multi_agent_graph

# Crear el grafo
graph = create_multi_agent_graph()

# Ejecutar una compra
estado = {
    "messages": [
        HumanMessage(content="Quiero comprar 2 litros de leche y un pan")
    ]
}

resultado = graph.invoke(estado)

print(resultado["final_result"])
print(resultado["ticket"])
```

### Pruebas

```bash
cd backend/gen_ui_backend
python test_multi_agent.py
```

## 📊 Flujo de Ejecución

1. **Usuario** envía mensaje: "Quiero comprar 2 leches y pan"

2. **Agente 1** (Clasificador):
   - Clasifica intención: "compra"
   - Extrae productos: ["leche", "pan"]
   - Detecta cantidades: {"leche": 2, "pan": 1}
   - → Navega a **Agente 2**

3. **Agente 2** (Buscador):
   - Busca "leche" → Encuentra: Leche Entera 1L - 1.20€
   - Busca "pan" → Encuentra: Pan de Molde - 0.85€
   - → Navega a **Agente 3**

4. **Agente 3** (Calculador):
   - Calcula: 2×1.20 + 1×0.85 = 3.25€
   - Genera ticket formateado
   - → Termina con resultado

## 🔧 Configuración

### Variables de Entorno

```bash
# OpenAI API Key (requerido)
OPENAI_API_KEY=sk-...

# Mercadona API (cuando se implemente)
MERCADONA_API_KEY=...
MERCADONA_API_URL=https://api.mercadona.com
```

### Modelos Soportados

- **Por defecto**: GPT-4o (OpenAI)
- **Alternativo**: Llama2 (Ollama) - comentado en el código

Para usar Ollama:
```python
# En chain.py, línea 39, descomentar:
model = ChatOllama(model="llama2", temperature=0, streaming=True)
```

## 🔄 Comunicación entre Agentes

Los agentes se comunican usando `Command` de LangGraph:

```python
return Command(
    goto="agente_2_buscador",  # Siguiente agente
    update={                    # Actualización del estado
        "productos_mencionados": ["leche", "pan"],
        "cantidades": {"leche": 2, "pan": 1}
    }
)
```

### Ventajas de este enfoque:

✅ **Control explícito** del flujo de ejecución  
✅ **Estado compartido** entre agentes  
✅ **Debugging fácil** con prints en cada agente  
✅ **Modular** - cada agente es independiente  
✅ **Extensible** - fácil agregar más agentes  

## 📝 Próximos Pasos

### Prioridad Alta
- [ ] Implementar integración real con API de Mercadona
- [ ] Desarrollar lógica de clasificación de intención con NLP
- [ ] Implementar cálculo de precios y descuentos

### Prioridad Media
- [ ] Añadir caché de productos con Redis
- [ ] Implementar manejo de errores robusto
- [ ] Agregar tests unitarios para cada agente
- [ ] Implementar logging estructurado

### Prioridad Baja
- [ ] Añadir agente de recomendaciones
- [ ] Implementar sistema de promociones
- [ ] Agregar soporte para múltiples supermercados
- [ ] Crear interfaz web con Gradio

## 🤝 Contribuir

Para agregar un nuevo agente:

1. Crear las tools necesarias en `/tools/`
2. Definir el agente en `chain.py`:
   ```python
   def agente_4_nuevo(state, config) -> Command[Literal[...]]:
       # Tu lógica aquí
       return Command(goto="siguiente_agente", update={...})
   ```
3. Agregar el nodo al grafo:
   ```python
   workflow.add_node("agente_4_nuevo", agente_4_nuevo)
   ```
4. Actualizar los tipos de retorno de Command de otros agentes

## 📚 Referencias

- [LangGraph Multi-Agent Documentation](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- [LangGraph Command API](https://langchain-ai.github.io/langgraph/concepts/low_level/#command)
- [LangChain Tools](https://python.langchain.com/docs/modules/agents/tools/)

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles.


