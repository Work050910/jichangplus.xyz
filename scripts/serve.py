import http.server
import socketserver
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8099
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRECTORY = os.path.join(BASE_DIR, "public")

class Handler(http.server.SimpleHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=DIRECTORY, **kwargs)

socketserver.TCPServer.allow_reuse_address = True

print(f"JichangPlus Preview Server running at: http://localhost:{PORT}")
print(f"Serving directory: {DIRECTORY}")

with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("\nServer stopped.")
