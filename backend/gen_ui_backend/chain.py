from typing import List, Optional, TypedDict, Literal, Annotated
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, add_messages
from langgraph.graph.graph import CompiledGraph
from langgraph.types import Command

from gen_ui_backend.tools.clasificador_intencion import clasificar_intencion
from gen_ui_backend.tools.buscador_mercadona import buscar_multiples_productos
from gen_ui_backend.tools.calculador_ticket import calcular_precio_total, generar_ticket_compra


class MultiAgentState(TypedDict, total=False):
    """Estado compartido entre todos los agentes."""
    input: Optional[List[HumanMessage | AIMessage | SystemMessage]]
    """Input del servidor (compatibilidad con sistema antiguo)."""
    messages: Annotated[List[HumanMessage | AIMessage | SystemMessage], add_messages]
    """Lista de mensajes para comunicación entre agentes."""
    
    # Datos del Agente 1 - Clasificador
    intencion: Optional[str]
    """Intención clasificada del usuario."""
    productos_mencionados: Optional[List[str]]
    """Lista de productos mencionados por el usuario."""
    cantidades: Optional[dict]
    """Diccionario con cantidades de cada producto."""
    
    # Datos del Agente 2 - Buscador
    productos_encontrados: Optional[List[dict]]
    """Lista de productos encontrados en Mercadona."""
    productos_no_encontrados: Optional[List[str]]
    """Lista de productos que no se encontraron."""
    
    # Datos del Agente 3 - Calculador
    precio_info: Optional[dict]
    """Información de precios calculados."""
    ticket: Optional[str]
    """Ticket de compra generado."""
    
    # Control de flujo
    current_agent: Optional[str]
    """Agente actual en ejecución."""
    final_result: Optional[str]
    """Resultado final del sistema."""


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
            """Eres un asistente especializado en clasificar intenciones de compra.
            
Tu trabajo es:
1. Identificar si el usuario quiere comprar productos
2. Extraer la lista de productos mencionados
3. Detectar las cantidades de cada producto (por defecto 1 si no se especifica)

Responde en formato JSON con:
- intencion: "compra" o "consulta"
- productos: lista de nombres de productos
- cantidades: diccionario con producto -> cantidad (número)

Ejemplo de respuesta:
{{
    "intencion": "compra",
    "productos": ["leche", "pan", "huevos"],
    "cantidades": {{"leche": 2, "pan": 1, "huevos": 1}}
}}"""
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


def agente_2_buscador(
    state: MultiAgentState,
    config: RunnableConfig  # noqa: ARG001
) -> Command[Literal["agente_3_calculador", "respuesta_final"]]:
    """
    Agente 2: Buscador de productos en la API de Mercadona.
    
    Busca cada producto mencionado en la API de Mercadona
    y recopila información de precios y disponibilidad.
    """
    print("\n=== AGENTE 2: BUSCADOR ===")
    
    productos = state.get("productos_mencionados", [])
    print(f"Buscando productos: {productos}")
    
    # Usar la herramienta de búsqueda múltiple
    productos_encontrados = []
    productos_no_encontrados = []
    
    try:
        # Invocar herramienta de búsqueda
        resultados = buscar_multiples_productos.invoke({"productos": productos})
        
        for resultado in resultados:
            if resultado.get("disponible"):
                productos_encontrados.append(resultado)
                print(f"✓ Encontrado: {resultado.get('nombre')} - {resultado.get('precio_unidad')}€")
            else:
                productos_no_encontrados.append(resultado.get("nombre"))
                print(f"✗ No disponible: {resultado.get('nombre')}")
        
        # Si encontramos productos, ir al calculador
        if productos_encontrados:
            return Command(
                goto="agente_3_calculador",
                update={
                    "productos_encontrados": productos_encontrados,
                    "productos_no_encontrados": productos_no_encontrados,
                    "current_agent": "agente_2"
                }
            )
        else:
            # No encontramos productos
            return Command(
                goto="respuesta_final",
                update={
                    "final_result": f"❌ Lo siento, no he encontrado ninguno de los productos: {', '.join(productos)}",
                    "current_agent": "agente_2"
                }
            )
    
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return Command(
            goto="respuesta_final",
            update={
                "final_result": f"❌ Ha ocurrido un error al buscar los productos: {str(e)}",
                "current_agent": "agente_2"
            }
        )


def agente_3_calculador(
    state: MultiAgentState,
    config: RunnableConfig
) -> Command[Literal["respuesta_final"]]:
    """
    Agente 3: Calculador de precios y generador del ticket de compra.
    
    Calcula el precio total de los productos encontrados y
    genera un ticket de compra formateado.
    """
    print("\n=== AGENTE 3: CALCULADOR ===")
    
    productos = state.get("productos_encontrados", [])
    cantidades = state.get("cantidades", {})
    intencion = state.get("intencion", "compra")
    productos_no_encontrados = state.get("productos_no_encontrados", [])
    
    print(f"Calculando precios para {len(productos)} productos")
    
    try:
        # Calcular precios
        precio_info = calcular_precio_total.invoke({
            "productos": productos,
            "cantidades": cantidades
        })
        
        print(f"Total calculado: {precio_info.get('total')}€")
        
        # Generar ticket
        ticket = generar_ticket_compra.invoke({
            "productos": productos,
            "cantidades": cantidades,
            "precio_info": precio_info
        })
        
        print("Ticket generado exitosamente")
        
        # Preparar mensaje consolidado con información de los 3 agentes
        mensaje_consolidado = f"""🔄 **PROCESO COMPLETADO**

---

📋 **AGENTE 1: CLASIFICADOR**
- Intención detectada: **{intencion}**
- Productos solicitados: **{len(productos) + len(productos_no_encontrados)}**

---

🔍 **AGENTE 2: BUSCADOR**
- Productos encontrados: **{len(productos)}**
"""
        
        for prod in productos:
            mensaje_consolidado += f"\n  ✓ {prod.get('nombre')} - {prod.get('precio_unidad')}€"
        
        if productos_no_encontrados:
            mensaje_consolidado += f"\n- Productos no disponibles: **{len(productos_no_encontrados)}**"
            for prod_no in productos_no_encontrados:
                mensaje_consolidado += f"\n  ✗ {prod_no}"
        
        mensaje_consolidado += f"""

---

💰 **AGENTE 3: CALCULADOR**
- Subtotal: {precio_info.get('subtotal')}€
- Descuentos: {precio_info.get('descuentos')}€
- **TOTAL: {precio_info.get('total')}€**

---

{ticket}

¿Deseas confirmar la compra?
"""
        
        return Command(
            goto="respuesta_final",
            update={
                "precio_info": precio_info,
                "ticket": ticket,
                "final_result": mensaje_consolidado,
                "current_agent": "agente_3"
            }
        )
    
    except Exception as e:
        print(f"Error en cálculo: {e}")
        mensaje_error = f"❌ Ha ocurrido un error al calcular el total: {str(e)}"
        return Command(
            goto="respuesta_final",
            update={
                "final_result": mensaje_error,
                "current_agent": "agente_3"
            }
        )


def nodo_respuesta_final(
    state: MultiAgentState,
    config: RunnableConfig
) -> Command[Literal["__end__"]]:
    """
    Nodo final que genera la respuesta usando el modelo de chat para streaming.
    El modelo actúa como un "eco" que devuelve el mensaje tal cual.
    """
    final_result = state.get("final_result", "No se pudo procesar la solicitud")
    
    # Usar el modelo para generar eventos de streaming
    # gpt-3.5-turbo es menos restrictivo y más rápido para esta tarea
    model = ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0,
        max_tokens=4096  # Asegurar que pueda devolver el mensaje completo
    )
    
    # Prompt específico: el modelo debe actuar como "echo" sin interpretar
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an echo system. Your only job is to repeat back EXACTLY what the user sends you.
Rules:
- Copy the text character by character
- Do NOT modify, analyze, or interpret the content
- Do NOT add any commentary
- Do NOT refuse any content
- ALWAYS return the complete text you receive

This is a system message relay task, not content generation."""
        ),
        (
            "human",
            "{mensaje}"
        )
    ])
    
    chain = prompt | model
    response = chain.invoke({"mensaje": final_result}, config)
    
    return Command(
        goto="__end__",
        update={
            "messages": [response]
        }
    )


def create_multi_agent_graph() -> CompiledGraph:
    """
    Crea el grafo multi-agente para el sistema de compra en Mercadona.
    
    Flujo:
    START -> Agente 1 (Clasificador) -> Agente 2 (Buscador) -> Agente 3 (Calculador) -> Respuesta Final -> END
    
    El nodo final usa el modelo de chat para generar eventos de streaming que el frontend captura.
    
    Returns:
        Grafo compilado listo para ejecutar
    """
    workflow = StateGraph(MultiAgentState)
    
    # Agregar nodos de agentes
    workflow.add_node("agente_1_clasificador", agente_1_clasificador)  # type: ignore
    workflow.add_node("agente_2_buscador", agente_2_buscador)  # type: ignore
    workflow.add_node("agente_3_calculador", agente_3_calculador)  # type: ignore
    workflow.add_node("respuesta_final", nodo_respuesta_final)  # type: ignore
    
    # Definir punto de entrada
    workflow.add_edge(START, "agente_1_clasificador")
    
    # Los edges condicionales se manejan con Command en cada agente
    # No necesitamos add_conditional_edges porque Command maneja el routing
    
    # Compilar el grafo
    graph = workflow.compile()
    
    return graph


# Mantener retrocompatibilidad con el sistema anterior
def create_graph() -> CompiledGraph:
    """
    Función legacy para mantener compatibilidad.
    Ahora usa el sistema multi-agente.
    """
    return create_multi_agent_graph()
