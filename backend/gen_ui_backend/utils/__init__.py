"""
Módulo de utilidades para el backend.
"""

from .mercadona_api import (  # noqa: F401
    normalizar_nombre,
    hacer_peticion_api,
    crear_diccionario_categorias,
    encontrar_numero_categoria,
    extraer_productos_de_categoria,
    mostrar_productos_seleccionados,
)

__all__ = [
    "normalizar_nombre",
    "hacer_peticion_api",
    "crear_diccionario_categorias",
    "encontrar_numero_categoria",
    "extraer_productos_de_categoria",
    "mostrar_productos_seleccionados",
]

