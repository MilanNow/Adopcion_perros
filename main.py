import http.server
import socketserver
import webbrowser
import os
import threading
import time

# -------------------------------
# CONFIGURACIÓN DEL SERVIDOR
# -------------------------------
PORT = 8000
DIRECTORIO = os.path.dirname(os.path.abspath(__file__))  # Ruta actual
os.chdir(DIRECTORIO)  # Cambia el directorio de trabajo al actual

# Manejador personalizado para mostrar logs de acceso
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Sobrescribe la función original para mostrar logs más bonitos"""
        print(f"[📂] Archivo solicitado: {self.path} | Desde: {self.client_address[0]}")

    def do_GET(self):
        """Sobrescribe GET para manejar errores 404 personalizados"""
        if not os.path.exists(self.translate_path(self.path)):
            self.send_error(404, f"Archivo no encontrado: {self.path}")
            print(f"[❌] 404 - No encontrado: {self.path}")
        else:
            super().do_GET()

# -------------------------------
# FUNCIÓN PARA ABRIR EL NAVEGADOR
# -------------------------------
def abrir_navegador():
    time.sleep(1)  # Espera un segundo a que el servidor esté listo
    url = f"http://localhost:{PORT}/index.html"
    print(f"[🌐] Abriendo {url} en tu navegador predeterminado...")
    webbrowser.open(url)

# -------------------------------
# INICIO DEL SERVIDOR
# -------------------------------
def iniciar_servidor():
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"[✅] Servidor corriendo en http://localhost:{PORT}")
            print(f"[📁] Directorio raíz: {DIRECTORIO}")
            print("[💡] Presiona Ctrl + C para detener el servidor.\n")

            # Abre el navegador en un hilo aparte
            threading.Thread(target=abrir_navegador, daemon=True).start()

            httpd.serve_forever()
    except OSError as e:
        print(f"[⚠️] Error al iniciar el servidor: {e}")
    except KeyboardInterrupt:
        print("\n[🛑] Servidor detenido manualmente.")
    finally:
        print("[👋] Hasta luego!")

# -------------------------------
# EJECUCIÓN
# -------------------------------
if __name__ == "__main__":
    iniciar_servidor()
