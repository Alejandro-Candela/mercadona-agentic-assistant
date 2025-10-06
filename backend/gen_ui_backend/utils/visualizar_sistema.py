"""
Script para visualizar la estructura del sistema multi-agente.
"""
from gen_ui_backend.graph import create_multi_agent_graph


def mostrar_estructura():
    """Muestra la estructura del sistema multi-agente."""
    
    print("\n" + "="*70)
    print(" SISTEMA MULTI-AGENTE - MERCADONA")
    print("="*70)
    
    print("""
┌────────────────────────────────────────────────────────────────────┐
│                     FLUJO DEL SISTEMA                               │
└────────────────────────────────────────────────────────────────────┘

  Usuario envía: "Quiero 2 leches y un pan"
       │
       ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  START                                                        │
  └─────────────────┬───────────────────────────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  🤖 AGENTE 1: CLASIFICADOR                                   │
  │  ─────────────────────────────────────────────────────────  │
  │  • Clasifica intención: "compra"                            │
  │  • Extrae productos: ["leche", "pan"]                       │
  │  • Detecta cantidades: {"leche": 2, "pan": 1}              │
  │  • Tool: clasificar_intencion()                             │
  │  ─────────────────────────────────────────────────────────  │
  │  → Si hay productos: goto agente_2_buscador                 │
  │  → Si no: END con mensaje de error                          │
  └─────────────────┬───────────────────────────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  🔍 AGENTE 2: BUSCADOR                                       │
  │  ─────────────────────────────────────────────────────────  │
  │  • Busca "leche" → ✓ Leche Entera 1L - 1.20€              │
  │  • Busca "pan" → ✓ Pan de Molde - 0.85€                   │
  │  • Tools: buscar_producto_mercadona()                       │
  │           buscar_multiples_productos()                      │
  │  ─────────────────────────────────────────────────────────  │
  │  → Si encuentra productos: goto agente_3_calculador         │
  │  → Si no encuentra: END con mensaje de error                │
  └─────────────────┬───────────────────────────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  💰 AGENTE 3: CALCULADOR                                     │
  │  ─────────────────────────────────────────────────────────  │
  │  • Calcula: 2 × 1.20€ + 1 × 0.85€ = 3.25€                  │
  │  • Aplica descuentos (si hay)                               │
  │  • Genera ticket formateado                                 │
  │  • Tools: calcular_precio_total()                           │
  │           generar_ticket_compra()                           │
  │  ─────────────────────────────────────────────────────────  │
  │  → Siempre: goto END con ticket generado                    │
  └─────────────────┬───────────────────────────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  END - Ticket generado                                       │
  │                                                              │
  │  ================================                            │
  │  MERCADONA - TICKET DE COMPRA                               │
  │  ================================                            │
  │  2x Leche Entera 1L .... 2.40€                             │
  │  1x Pan de Molde ....... 0.85€                             │
  │  --------------------------------                            │
  │  TOTAL ................. 3.25€                              │
  │  ================================                            │
  └─────────────────────────────────────────────────────────────┘
    """)
    
    print("="*70)
    print(" ESTADO COMPARTIDO (MultiAgentState)")
    print("="*70)
    print("""
┌──────────────────────────────────────────────────────────────┐
│  input: List[Messages]              # Del servidor           │
│  messages: List[Messages]           # Entre agentes          │
│  ──────────────────────────────────────────────────────────  │
│  intencion: str                     # Agente 1 → Agente 2   │
│  productos_mencionados: List[str]   # Agente 1 → Agente 2   │
│  cantidades: Dict[str, int]         # Agente 1 → Agente 2   │
│  ──────────────────────────────────────────────────────────  │
│  productos_encontrados: List[Dict]  # Agente 2 → Agente 3   │
│  productos_no_encontrados: List[str]                         │
│  ──────────────────────────────────────────────────────────  │
│  precio_info: Dict                  # Agente 3 → END         │
│  ticket: str                        # Agente 3 → END         │
│  ──────────────────────────────────────────────────────────  │
│  current_agent: str                 # Tracking               │
│  final_result: str                  # Resultado final        │
└──────────────────────────────────────────────────────────────┘
    """)
    
    print("="*70)
    print(" HERRAMIENTAS (TOOLS)")
    print("="*70)
    print("""
📁 backend/gen_ui_backend/tools/
  ├── clasificador_intencion.py
  │   └── clasificar_intencion(user_input: str) → Dict
  │       ├─ intencion: str
  │       ├─ productos: List[str]
  │       └─ cantidad: Dict[str, int]
  │
  ├── buscador_mercadona.py
  │   ├── buscar_producto_mercadona(producto: str) → Dict
  │   │   ├─ id: str
  │   │   ├─ nombre: str
  │   │   ├─ precio: float
  │   │   ├─ disponible: bool
  │   │   └─ categoria: str
  │   │
  │   └── buscar_multiples_productos(productos: List[str]) → List[Dict]
  │
  └── calculador_ticket.py
      ├── calcular_precio_total(productos, cantidades) → Dict
      │   ├─ subtotal: float
      │   ├─ descuentos: float
      │   ├─ total: float
      │   └─ items: List[Dict]
      │
      └── generar_ticket_compra(...) → str
    """)
    
    print("="*70)
    print(" COMUNICACIÓN ENTRE AGENTES")
    print("="*70)
    print("""
Cada agente usa Command para enrutar:

    return Command(
        goto="agente_siguiente",  # O "__end__"
        update={                   # Actualizar estado
            "campo1": valor1,
            "campo2": valor2
        }
    )

Ventajas:
  ✓ Control explícito del flujo
  ✓ Estado compartido y tipado
  ✓ Debugging fácil
  ✓ Modular y extensible
    """)
    
    print("="*70)
    print(" PRÓXIMOS PASOS")
    print("="*70)
    print("""
1. ⏳ Implementar lógica de clasificación (Agente 1)
   → NLP para extraer productos y cantidades

2. ⏳ Integrar API real de Mercadona (Agente 2)
   → Endpoints, autenticación, caché

3. ⏳ Desarrollar cálculo de precios (Agente 3)
   → Lógica de descuentos y promociones

4. ⏳ Agregar tests unitarios
   → Probar cada agente independientemente

5. ⏳ Implementar logging y métricas
   → Observabilidad del sistema
    """)
    
    print("="*70)
    print("\n✅ Sistema listo para desarrollo!")
    print("\nPara probar: python test_multi_agent.py")
    print("Para iniciar servidor: python server.py\n")


def informacion_tecnica():
    """Muestra información técnica del grafo."""
    print("\n" + "="*70)
    print(" INFORMACIÓN TÉCNICA DEL GRAFO")
    print("="*70 + "\n")
    
    try:
        graph = create_multi_agent_graph()
        
        print("✓ Grafo creado exitosamente")
        print(f"✓ Tipo: {type(graph).__name__}")
        print(f"✓ Framework: LangGraph + LangChain")
        print(f"✓ Modelo: GPT-4o (OpenAI)")
        
        print("\nNodos del grafo:")
        nodos = ["agente_1_clasificador", "agente_2_buscador", "agente_3_calculador"]
        for i, nodo in enumerate(nodos, 1):
            print(f"  {i}. {nodo}")
        
        print("\nPunto de entrada:")
        print("  START → agente_1_clasificador")
        
        print("\nEnrutamiento:")
        print("  • Dinámico usando Command")
        print("  • Cada agente decide el siguiente paso")
        print("  • Puede terminar en cualquier agente si hay error")
        
    except Exception as e:
        print(f"❌ Error al crear el grafo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    mostrar_estructura()
    informacion_tecnica()


