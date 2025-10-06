"""
Módulo de herramientas para el sistema multi-agente.
"""

# Herramientas multi-agente de compra Mercadona
from gen_ui_backend.tools.clasificador_intencion import clasificar_intencion
from gen_ui_backend.tools.buscador_mercadona import (
    buscar_producto_mercadona,
    buscar_multiples_productos
)
from gen_ui_backend.tools.calculador_ticket import (
    calcular_precio_total,
    generar_ticket_compra
)

# Herramientas existentes (importación opcional para evitar errores)
try:
    from gen_ui_backend.tools.github import github_repo
    from gen_ui_backend.tools.invoice import invoice_parser
    from gen_ui_backend.tools.weather import weather_data
    _legacy_tools_available = True
except ImportError:
    github_repo = None
    invoice_parser = None
    weather_data = None
    _legacy_tools_available = False

__all__ = [
    # Herramientas multi-agente (siempre disponibles)
    "clasificar_intencion",
    "buscar_producto_mercadona",
    "buscar_multiples_productos",
    "calcular_precio_total",
    "generar_ticket_compra",
]

# Agregar herramientas legacy si están disponibles
if _legacy_tools_available:
    __all__.extend([
        "github_repo",
        "invoice_parser",
        "weather_data",
    ])


