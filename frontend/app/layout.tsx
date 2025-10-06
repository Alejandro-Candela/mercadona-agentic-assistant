import "./globals.css";
import type { Metadata } from "next";

import { EndpointsContext } from "./agent";
import { ReactNode } from "react";

export const metadata: Metadata = {
  title: "asistente de compras de Mercadona",
  description: "Asistente de compras de Mercadona mediante flujo de agentes",
};

export default function RootLayout(props: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="flex flex-col p-4 md:p-12 h-[100vh]">
          <EndpointsContext>{props.children}</EndpointsContext>
        </div>
      </body>
    </html>
  );
}
