"""
Lokal HTTPS-server for utvikling og testing av sommerferie2026/index.html.

Sertifikatene (mkcert-cert.pem og mkcert-key.pem) skal ligge i samme mappe
som dette skriptet: setup/test-server/

Generer sertifikater med mkcert (kjores fra WSL):
  wsl mkcert -install
  wsl bash -c "cd /mnt/e/Git/sommerferie2026/setup/test-server && mkcert -key-file mkcert-key.pem -cert-file mkcert-cert.pem localhost 127.0.0.1 ::1"

Start serveren fra repo-roten:
  python setup/test-server/https_server.py
Aapne i nettleser: https://localhost:3000/index.html
"""

import http.server
import ssl
import os

# Skriptets egen mappe (setup/test-server/) -- her ligger sertifikatene
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Serv filer fra repo-roten (to niva opp fra setup/test-server/)
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
os.chdir(REPO_ROOT)

PORT = 3000
CERT = os.path.join(SCRIPT_DIR, 'mkcert-cert.pem')
KEY  = os.path.join(SCRIPT_DIR, 'mkcert-key.pem')

if not os.path.exists(CERT) or not os.path.exists(KEY):
    raise FileNotFoundError(
        f"Sertifikatfiler ikke funnet i {SCRIPT_DIR}.\n"
        "Kjoer kommandoene ovenfor for aa generere dem."
    )

server = http.server.HTTPServer(('localhost', PORT), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)
server.socket = ctx.wrap_socket(server.socket, server_side=True)
print(f"Serverer filer fra: {REPO_ROOT}")
print(f"HTTPS server kjoer paa https://localhost:{PORT}")
print(f"Aapne: https://localhost:{PORT}/index.html")
server.serve_forever()
