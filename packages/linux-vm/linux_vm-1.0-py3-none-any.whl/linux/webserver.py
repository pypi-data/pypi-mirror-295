from http.server import BaseHTTPRequestHandler, HTTPServer

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello from Linux VM!")

def start_webserver():
    """Start the HTTP server on port 8000."""
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, WebServer)
    print("Starting server on port 8000...")
    httpd.serve_forever()