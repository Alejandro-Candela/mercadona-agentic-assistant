"""
Nodo final del grafo multi-agente.

Genera la respuesta final usando el modelo de chat para streaming.
"""
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.types import Command

from gen_ui_backend.agents.state import MultiAgentState


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

