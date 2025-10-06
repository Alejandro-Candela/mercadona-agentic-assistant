"use client";

import { AIMessageText } from "@/components/prebuilt/message";
import { TicketCompra, TicketData, ArchivosDescargables } from "@/components/prebuilt/ticket-compra";
import { StreamableValue, useStreamableValue } from "ai/rsc";

function parseTicketData(content: string): { 
  hasTicket: boolean; 
  ticketData?: TicketData; 
  archivos?: ArchivosDescargables;
  cleanContent: string;
} {
  // Buscar patrones que indiquen que hay información de ticket
  if (!content.includes("AGENTE 3: CALCULADOR") || !content.includes("LISTA DE LA COMPRA")) {
    return { hasTicket: false, cleanContent: content };
  }

  // Extraer datos de la tabla
  const tableMatch = content.match(/\| Nº \| Producto \| Cantidad \| Precio Unit\. \| Precio Total \|([\s\S]*?)(?=\n\n---|\n---)/);
  
  if (!tableMatch) {
    return { hasTicket: false, cleanContent: content };
  }

  const tableRows = tableMatch[1].trim().split('\n').filter(row => !row.includes('---|---'));
  const items: any[] = [];

  for (const row of tableRows) {
    const cols = row.split('|').map(c => c.trim()).filter(c => c);
    if (cols.length >= 5) {
      items.push({
        nombre: cols[1],
        cantidad: parseInt(cols[2]) || 1,
        precio_unitario: parseFloat(cols[3].replace('€', '')) || 0,
        precio_total: parseFloat(cols[4].replace('€', '').replace('**', '')) || 0,
        packaging: "",
        categoria: ""
      });
    }
  }

  // Extraer totales
  const subtotalMatch = content.match(/Subtotal:\s*([\d.]+)€/);
  const descuentosMatch = content.match(/Descuentos:\s*([\d.]+)€/);
  const totalMatch = content.match(/TOTAL:\s*\*?\*?([\d.]+)€/);

  const subtotal = subtotalMatch ? parseFloat(subtotalMatch[1]) : 0;
  const descuentos = descuentosMatch ? parseFloat(descuentosMatch[1]) : 0;
  const total = totalMatch ? parseFloat(totalMatch[1]) : 0;

  // Extraer rutas de archivos
  const jsonPathMatch = content.match(/JSON\*\*:\s*`([^`]+)`/);
  const txtPathMatch = content.match(/TXT\*\*:\s*`([^`]+)`/);
  const csvPathMatch = content.match(/CSV\*\*:\s*`([^`]+)`/);

  // Extraer timestamp de la ruta del archivo (formato: ticket_YYYYMMDD_HHMMSS.ext)
  let timestamp: string | undefined;
  if (jsonPathMatch) {
    const timestampMatch = jsonPathMatch[1].match(/ticket_(\d{8}_\d{6})/);
    if (timestampMatch) {
      timestamp = timestampMatch[1];
    }
  }

  const archivos: ArchivosDescargables = {
    success: true,
    json_path: jsonPathMatch ? jsonPathMatch[1] : undefined,
    txt_path: txtPathMatch ? txtPathMatch[1] : undefined,
    csv_path: csvPathMatch ? csvPathMatch[1] : undefined,
    timestamp: timestamp,
  };

  const ticketData: TicketData = {
    items,
    subtotal,
    descuentos,
    total,
    num_items: items.length,
    num_productos: items.reduce((sum, item) => sum + item.cantidad, 0)
  };

  return { 
    hasTicket: true, 
    ticketData, 
    archivos,
    cleanContent: content 
  };
}

export function AIMessage(props: { value: StreamableValue<string> }) {
  const [data] = useStreamableValue(props.value);

  if (!data) {
    return null;
  }

  // Parse el contenido para detectar si hay un ticket
  const parsed = parseTicketData(data);

  if (parsed.hasTicket && parsed.ticketData) {
    return (
      <div>
        <AIMessageText content={parsed.cleanContent} />
        <TicketCompra ticketData={parsed.ticketData} archivos={parsed.archivos} />
      </div>
    );
  }

  return <AIMessageText content={data} />;
}
