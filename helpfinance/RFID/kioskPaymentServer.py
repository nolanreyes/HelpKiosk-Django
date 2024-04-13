from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from rfid.rfid_reader import RFIDReader
import json

class RequestHandler(BaseHTTPRequestHandler):
    reader = RFIDReader()

    def do_GET(self):
        query = urlparse(self.path).query
        query_components = parse_qs(query)

        if '/read_card' in self.path:
            id, text = self.reader.read_card()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'id': id, 'text': text}).encode())

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

