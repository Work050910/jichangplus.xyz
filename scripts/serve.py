import http.server
import socketserver
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 1313
DIRECTORY = "public"

class Handler(http.server.SimpleHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"JichangPlus (Clean White) Preview Server running at: http://localhost:{PORT}")
print("Press Ctrl+C to stop.")

try:
  with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
except KeyboardInterrupt:
  print("\nServer stopped.")
