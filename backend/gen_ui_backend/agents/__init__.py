"""
Módulo de agentes para el sistema multi-agente de Mercadona.
"""
from gen_ui_backend.agents.state import MultiAgentState
from gen_ui_backend.agents.agente_clasificador import agente_1_clasificador
from gen_ui_backend.agents.agente_buscador import agente_2_buscador
from gen_ui_backend.agents.agente_calculador import agente_3_calculador
from gen_ui_backend.agents.nodo_final import nodo_respuesta_final

__all__ = [
    "MultiAgentState",
    "agente_1_clasificador",
    "agente_2_buscador",
    "agente_3_calculador",
    "nodo_respuesta_final",
]

