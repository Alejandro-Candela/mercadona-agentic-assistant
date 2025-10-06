"""
Módulo de herramientas para el sistema multi-agente.
"""

# Herramientas existentes
from gen_ui_backend.tools.github import github_repo
from gen_ui_backend.tools.invoice import invoice_parser
from gen_ui_backend.tools.weather import weather_data

# Nuevas herramientas para sistema multi-agente de compra Mercadona
from gen_ui_backend.tools.clasificador_intencion import clasificar_intencion
from gen_ui_backend.tools.buscador_mercadona import (
    buscar_producto_mercadona,
    buscar_multiples_productos
)
from gen_ui_backend.tools.calculador_ticket import (
    calcular_precio_total,
    generar_ticket_compra
)

__all__ = [
    # Herramientas existentes
    "github_repo",
    "invoice_parser",
    "weather_data",
    # Herramientas multi-agente
    "clasificar_intencion",
    "buscar_producto_mercadona",
    "buscar_multiples_productos",
    "calcular_precio_total",
    "generar_ticket_compra",
]


