import http.server
import socketserver
import os

PORT = 8000

web_dir = os.path.join('/home/pi/stericonnect/logs')
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.serve_forever()