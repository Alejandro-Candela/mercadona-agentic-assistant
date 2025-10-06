import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langserve import add_routes

from gen_ui_backend.chain import create_graph
from gen_ui_backend.utils.input_types import ChatInputType

# Load environment variables from .env file
load_dotenv()


def start() -> None:
    app = FastAPI(
        title="Gen UI Backend",
        version="1.0",
        description="A simple api server using Langchain's Runnable interfaces",
    )

    # Configure CORS
    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Endpoint para descargar archivos del ticket
    @app.get("/download/{filename}")
    async def download_ticket(filename: str):
        """
        Endpoint para descargar archivos de tickets generados.
        Los archivos deben estar en el directorio 'tickets'.
        """
        # Directorio de tickets
        tickets_dir = os.path.join(os.getcwd(), "tickets")
        file_path = os.path.join(tickets_dir, filename)
        
        # Validar que el archivo existe
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        # Validar que el archivo está dentro del directorio de tickets (seguridad)
        if not os.path.abspath(file_path).startswith(os.path.abspath(tickets_dir)):
            raise HTTPException(status_code=403, detail="Acceso denegado")
        
        # Determinar el tipo de contenido según la extensión
        _, ext = os.path.splitext(filename)
        media_types = {
            ".json": "application/json",
            ".txt": "text/plain",
            ".csv": "text/csv"
        }
        media_type = media_types.get(ext.lower(), "application/octet-stream")
        
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename
        )

    graph = create_graph()

    runnable = graph.with_types(input_type=ChatInputType, output_type=dict)

    add_routes(app, runnable, path="/chat", playground_type="chat")
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start()