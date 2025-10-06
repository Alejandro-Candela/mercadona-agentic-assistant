# Asistente de Compras para Mercadona 🛒

Sistema multi-agente inteligente basado en LangGraph que permite gestionar compras en Mercadona mediante conversaciones naturales. El sistema procesa solicitudes de compra, busca productos, calcula precios y genera tickets descargables.

## 🎯 Características

- **Sistema Multi-Agente**: Flujo orquestado de 3 agentes especializados usando LangGraph
- **Procesamiento de Lenguaje Natural**: Comprende peticiones de compra en español
- **Búsqueda de Productos**: Integración con API de Mercadona para búsqueda en tiempo real
- **Cálculo Automático**: Calcula precios totales, descuentos y genera tickets formateados
- **Tickets Descargables**: Genera tickets en formato JSON, TXT y CSV
- **UI Generativa**: Interfaz moderna con componentes React renderizados dinámicamente
- **Streaming en Tiempo Real**: Respuestas en tiempo real mediante streaming de eventos

## 🏗️ Arquitectura

### Sistema Multi-Agente

```text
START → Agente 1 (Clasificador) → Agente 2 (Buscador) → Agente 3 (Calculador) → END
```

1. **Agente Clasificador**: Analiza la intención del usuario y extrae productos y cantidades
1. **Agente Buscador**: Busca productos en la API de Mercadona y verifica disponibilidad
1. **Agente Calculador**: Calcula precios totales y genera el ticket de compra

### Stack Tecnológico

**Backend:**

- FastAPI + LangServe para el servidor API
- LangGraph para orquestación multi-agente
- LangChain + OpenAI para procesamiento de lenguaje natural
- Python 3.11+

**Frontend:**

- Next.js 14 (App Router)
- React 18 con TypeScript
- Tailwind CSS + shadcn/ui
- LangGraph SDK para streaming

## 🚀 Getting Started

### Prerequisitos

- Node.js 18+ y Yarn
- Python 3.11+
- Cuenta de OpenAI con API key

### Instalación

1. **Instalar dependencias del frontend**

```bash
cd frontend
yarn install
```

2. **Instalar dependencias del backend**

```bash
cd ../backend
pip install -r gen_ui_backend/requirements.txt
```

### Variables de Entorno

Copia el archivo de ejemplo y configura tus claves API:

```bash
cd backend
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```bash
# REQUERIDO: OpenAI API Key
OPENAI_API_KEY=sk-...

# OPCIONAL: LangSmith para trazabilidad (recomendado para desarrollo)
LANGCHAIN_API_KEY=...
LANGCHAIN_CALLBACKS_BACKGROUND=true
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=mercadona-assistant
```

**Obtener las claves:**

- OpenAI API Key: [OpenAI Dashboard](https://platform.openai.com/api-keys)
- LangSmith API Key: [LangSmith](https://smith.langchain.com/)

### Ejecutar la Aplicación

1. **Iniciar el backend** (en una terminal):

```bash
cd backend
python gen_ui_backend/server.py
```

El servidor estará disponible en `http://localhost:8000`

1. **Iniciar el frontend** (en otra terminal):

```bash
cd frontend
yarn dev
```

La aplicación estará disponible en `http://localhost:3000`

## 📖 Uso

### Ejemplo de Conversación

```text
Usuario: "Quiero comprar 2 leches y un pan"

Agente Clasificador: Detecta intención de compra
                     Productos: ["leche", "pan"]
                     Cantidades: {leche: 2, pan: 1}

Agente Buscador: Busca en Mercadona
                 ✓ Leche Entera 1L - 1.20€
                 ✓ Pan de Molde - 0.85€

Agente Calculador: Calcula total
                   2×1.20 + 1×0.85 = 3.25€
                   Genera ticket descargable

Sistema: Muestra ticket interactivo con opción de descarga
```

### Uso Programático

```python
from langchain_core.messages import HumanMessage
from gen_ui_backend.graph import create_graph

graph = create_graph()

resultado = graph.invoke({
    "messages": [
        HumanMessage(content="Quiero 2 leches y pan")
    ]
})

print(resultado["final_result"])
```

## 🛠️ Desarrollo

### Estructura del Proyecto

```text
gen-ui-pythonv3/
├── backend/
│   ├── gen_ui_backend/
│   │   ├── agents/          # Agentes especializados
│   │   ├── tools/           # Herramientas de los agentes
│   │   ├── utils/           # Utilidades
│   │   ├── graph.py         # Definición del grafo multi-agente
│   │   └── server.py        # Servidor FastAPI
│   └── docs/                # Documentación técnica
└── frontend/
    ├── app/                 # App Router de Next.js
    ├── components/          # Componentes React
    │   ├── prebuilt/        # Componentes pre-construidos
    │   └── ui/              # Componentes UI (shadcn)
    └── utils/               # Utilidades del cliente
```

### Ejecutar Tests

```bash
cd backend/gen_ui_backend
python test_multi_agent.py
```

### Scripts Útiles

```bash
# Formatear código frontend
cd frontend
yarn format

# Verificar imports del backend
cd backend
python scripts/check_imports.py
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🙏 Agradecimientos

- [LangGraph](https://langchain-ai.github.io/langgraph/) por el framework multi-agente
- [shadcn/ui](https://ui.shadcn.com/) por los componentes UI