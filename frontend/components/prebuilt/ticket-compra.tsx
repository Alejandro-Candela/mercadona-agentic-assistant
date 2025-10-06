"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Download, FileText, FileJson, FileSpreadsheet } from "lucide-react";

export interface ProductoItem {
  nombre: string;
  cantidad: number;
  precio_unitario: number;
  precio_total: number;
  packaging?: string;
  categoria?: string;
}

export interface TicketData {
  items: ProductoItem[];
  subtotal: number;
  descuentos: number;
  total: number;
  num_items: number;
  num_productos: number;
  fecha?: string;
}

export interface ArchivosDescargables {
  json_path?: string;
  txt_path?: string;
  csv_path?: string;
  timestamp?: string;
  success?: boolean;
}

export interface TicketCompraProps {
  ticketData: TicketData;
  archivos?: ArchivosDescargables;
}

export function TicketCompraLoading() {
  return (
    <Card className="w-full max-w-3xl mx-auto my-4">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
          Generando ticket de compra...
        </CardTitle>
      </CardHeader>
    </Card>
  );
}

export function TicketCompra({ ticketData, archivos }: TicketCompraProps) {
  const handleDownload = async (filePath: string, fileName: string) => {
    try {
      // Obtener solo el nombre del archivo de la ruta completa
      const fileNameOnly = getFileNameFromPath(filePath);
      
      // Hacer petición al backend para descargar el archivo
      const response = await fetch(`http://localhost:8000/download/${fileNameOnly}`);
      
      if (!response.ok) {
        throw new Error("Error al descargar el archivo");
      }
      
      // Crear un blob del archivo
      const blob = await response.blob();
      
      // Crear URL temporal para el blob
      const url = window.URL.createObjectURL(blob);
      
      // Crear elemento <a> temporal para iniciar la descarga
      const a = document.createElement("a");
      a.href = url;
      a.download = fileNameOnly;
      document.body.appendChild(a);
      a.click();
      
      // Limpiar
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Error al descargar archivo:", error);
      alert("Error al descargar el archivo. Por favor, intenta de nuevo.");
    }
  };

  const getFileNameFromPath = (path: string) => {
    return path.split(/[\\/]/).pop() || path;
  };

  const formatTimestamp = (timestamp?: string) => {
    if (!timestamp) {
      return new Date().toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    }
    
    // Convertir timestamp formato YYYYMMDD_HHMMSS a fecha legible
    const year = timestamp.substring(0, 4);
    const month = timestamp.substring(4, 6);
    const day = timestamp.substring(6, 8);
    const hour = timestamp.substring(9, 11);
    const minute = timestamp.substring(11, 13);
    const second = timestamp.substring(13, 15);
    
    return `${day}/${month}/${year} ${hour}:${minute}:${second}`;
  };

  const fechaHora = ticketData.fecha || formatTimestamp(archivos?.timestamp);

  return (
    <Card className="w-full max-w-3xl mx-auto my-4 shadow-lg">
      <CardHeader className="bg-gradient-to-r from-green-600 to-green-700 text-white">
        <CardTitle className="text-2xl font-bold">
          🛒 Lista de la Compra - Mercadona
        </CardTitle>
        <div className="flex justify-between items-center mt-2">
          <p className="text-sm text-green-100">
            {ticketData.num_items} artículos diferentes • {ticketData.num_productos} unidades totales
          </p>
          <p className="text-sm text-green-100 font-mono">
            📅 {fechaHora}
          </p>
        </div>
      </CardHeader>
      
      <CardContent className="p-6">
        {/* Tabla de Productos */}
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b-2 border-gray-300">
                <th className="text-left p-2 font-semibold">Nº</th>
                <th className="text-left p-2 font-semibold">Producto</th>
                <th className="text-center p-2 font-semibold">Cantidad</th>
                <th className="text-right p-2 font-semibold">Precio Unit.</th>
                <th className="text-right p-2 font-semibold">Precio Total</th>
              </tr>
            </thead>
            <tbody>
              {ticketData.items.map((item, index) => (
                <tr 
                  key={index} 
                  className="border-b border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <td className="p-2 text-gray-600">{index + 1}</td>
                  <td className="p-2">
                    <div>
                      <p className="font-medium text-gray-900">{item.nombre}</p>
                      {item.packaging && (
                        <p className="text-xs text-gray-500">{item.packaging}</p>
                      )}
                    </div>
                  </td>
                  <td className="text-center p-2">
                    <Badge variant="secondary" className="font-mono">
                      {item.cantidad}
                    </Badge>
                  </td>
                  <td className="text-right p-2 font-mono text-gray-700">
                    {item.precio_unitario.toFixed(2)}€
                  </td>
                  <td className="text-right p-2 font-mono font-semibold text-gray-900">
                    {item.precio_total.toFixed(2)}€
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Resumen de Precios */}
        <div className="mt-6 pt-4 border-t-2 border-gray-300">
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-700">Subtotal:</span>
            <span className="font-mono text-gray-900">{ticketData.subtotal.toFixed(2)}€</span>
          </div>
          
          {ticketData.descuentos > 0 && (
            <div className="flex justify-between items-center mb-2 text-green-600">
              <span>Descuentos:</span>
              <span className="font-mono">-{ticketData.descuentos.toFixed(2)}€</span>
            </div>
          )}
          
          <div className="flex justify-between items-center pt-3 border-t border-gray-300">
            <span className="text-xl font-bold text-gray-900">TOTAL A PAGAR:</span>
            <span className="text-2xl font-bold font-mono text-green-600">
              {ticketData.total.toFixed(2)}€
            </span>
          </div>
        </div>

        {/* Sección de Archivos Descargables */}
        {archivos && archivos.success && (
          <div className="mt-6 pt-4 border-t border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <Download className="h-5 w-5" />
              Archivos Descargables
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {/* JSON */}
              {archivos.json_path && (
                <Button
                  variant="outline"
                  className="flex items-center gap-2 justify-start h-auto py-3"
                  onClick={() => handleDownload(archivos.json_path!, getFileNameFromPath(archivos.json_path!))}
                >
                  <FileJson className="h-5 w-5 text-blue-600" />
                  <div className="text-left flex-1">
                    <p className="font-semibold text-sm">JSON</p>
                    <p className="text-xs text-gray-500 truncate">
                      {getFileNameFromPath(archivos.json_path)}
                    </p>
                  </div>
                </Button>
              )}

              {/* TXT */}
              {archivos.txt_path && (
                <Button
                  variant="outline"
                  className="flex items-center gap-2 justify-start h-auto py-3"
                  onClick={() => handleDownload(archivos.txt_path!, getFileNameFromPath(archivos.txt_path!))}
                >
                  <FileText className="h-5 w-5 text-gray-600" />
                  <div className="text-left flex-1">
                    <p className="font-semibold text-sm">TXT</p>
                    <p className="text-xs text-gray-500 truncate">
                      {getFileNameFromPath(archivos.txt_path)}
                    </p>
                  </div>
                </Button>
              )}

              {/* CSV */}
              {archivos.csv_path && (
                <Button
                  variant="outline"
                  className="flex items-center gap-2 justify-start h-auto py-3"
                  onClick={() => handleDownload(archivos.csv_path!, getFileNameFromPath(archivos.csv_path!))}
                >
                  <FileSpreadsheet className="h-5 w-5 text-green-600" />
                  <div className="text-left flex-1">
                    <p className="font-semibold text-sm">CSV</p>
                    <p className="text-xs text-gray-500 truncate">
                      {getFileNameFromPath(archivos.csv_path)}
                    </p>
                  </div>
                </Button>
              )}
            </div>

            <p className="text-xs text-gray-500 mt-3 text-center">
              Los archivos están disponibles en el sistema local.
              Haz clic en cualquier botón para ver la ubicación.
            </p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-6 pt-4 border-t border-gray-200 text-center">
          <p className="text-sm text-gray-600">
            ¡Gracias por su compra! 🎉
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Vuelva pronto a Mercadona
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

