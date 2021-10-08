from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header()
        self.wfile.write(b'Replying to a response!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


if __name__ == '__main__':
    hostname = 'FILL_OUT'
    port_no = 4242

    httpd = HTTPServer(('hostname', port_no), HTTPRequestHandler)
    httpd.serve_forever()
