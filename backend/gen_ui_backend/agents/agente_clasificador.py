"""
Agente 1: Clasificador de intención y productos.

Analiza el mensaje del usuario para:
- Clasificar la intención (compra, consulta, etc.)
- Extraer productos mencionados
- Detectar cantidades
"""
from typing import Literal
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.types import Command

from gen_ui_backend.agents.state import MultiAgentState
from gen_ui_backend.tools.clasificador_intencion import clasificar_intencion


def agente_1_clasificador(
    state: MultiAgentState, 
    config: RunnableConfig
) -> Command[Literal["agente_2_buscador", "respuesta_final"]]:
    """
    Agente 1: Clasificador de intención y productos.
    
    Analiza el mensaje del usuario para:
    - Clasificar la intención (compra, consulta, etc.)
    - Extraer productos mencionados
    - Detectar cantidades
    """
    print("\n=== AGENTE 1: CLASIFICADOR ===")
    
    # Compatibilidad: convertir 'input' a 'messages' si es necesario
    messages = state.get("messages")
    if not messages and "input" in state:
        messages = state["input"]
    
    if not messages:
        return Command(
            goto="respuesta_final",
            update={
                "final_result": "❌ No se recibieron mensajes",
                "current_agent": "agente_1"
            }
        )
    
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Preparar el prompt para el clasificador
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """Eres un asistente especializado en clasificar intenciones de compra y detectar cantidades exactas.

Tu trabajo es:
1. Identificar si el usuario quiere comprar productos
2. Extraer la lista de productos mencionados
3. Detectar las cantidades EXACTAS de cada producto

REGLAS IMPORTANTES PARA DETECTAR CANTIDADES:
- Busca números antes o después del producto: "2 leches", "leche x 3", "tres panes"
- Busca cantidades en formato texto: "dos", "tres", "cuatro", "cinco", etc.
- Busca patrones con "de": "3 de leche", "2 de pan"
- Si el usuario menciona varios productos separados, detecta la cantidad individual de cada uno
- Por defecto asigna 1 SOLO si no se menciona ninguna cantidad
- Presta especial atención a cada producto y su cantidad específica

EJEMPLOS:
Entrada: "quiero 2 leches y 3 panes"
Salida: {{"intencion": "compra", "productos": ["leche", "pan"], "cantidades": {{"leche": 2, "pan": 3}}}}

Entrada: "dame tres leches, dos panes y cinco huevos"
Salida: {{"intencion": "compra", "productos": ["leche", "pan", "huevos"], "cantidades": {{"leche": 3, "pan": 2, "huevos": 5}}}}

Entrada: "necesito leche x 4 y pan x 2"
Salida: {{"intencion": "compra", "productos": ["leche", "pan"], "cantidades": {{"leche": 4, "pan": 2}}}}

Responde en formato JSON con:
- intencion: "compra" o "consulta"
- productos: lista de nombres de productos
- cantidades: diccionario con producto -> cantidad (número entero)"""
        ),
        MessagesPlaceholder("messages")
    ])
    
    # Vincular herramienta de clasificación
    tools = [clasificar_intencion]
    model_with_tools = model.bind_tools(tools)
    chain = prompt | model_with_tools
    
    # Invocar el modelo
    result = chain.invoke({"messages": messages}, config)
    
    # Procesar resultado
    if isinstance(result, AIMessage) and result.tool_calls:
        # Extraer información de la herramienta
        tool_call = result.tool_calls[0]
        clasificacion = clasificar_intencion.invoke(tool_call["args"])
        
        print(f"Intención: {clasificacion.get('intencion')}")
        print(f"Productos: {clasificacion.get('productos')}")
        print(f"Cantidades: {clasificacion.get('cantidades')}")
        
        # Si hay productos, ir al agente buscador
        productos = clasificacion.get("productos", [])
        cantidades = clasificacion.get("cantidades", {})
        intencion = clasificacion.get("intencion")
        
        if productos:
            return Command(
                goto="agente_2_buscador",
                update={
                    "intencion": intencion,
                    "productos_mencionados": productos,
                    "cantidades": cantidades,
                    "current_agent": "agente_1"
                }
            )
        else:
            # No hay productos, terminar
            return Command(
                goto="respuesta_final",
                update={
                    "final_result": "❌ No he identificado productos en tu mensaje. ¿Podrías especificar qué necesitas?",
                    "current_agent": "agente_1"
                }
            )
    else:
        # Respuesta sin herramientas
        return Command(
            goto="respuesta_final",
            update={
                "final_result": str(result.content),
                "current_agent": "agente_1"
            }
        )

