import http.server
import time
from prometheus_client import start_http_server, Histogram

REQUEST_RESPOND_TIME = Histogram('app_response_latency_seconds', 'Response latency in seconds', buckets=[0.1,0.5,1,2,3,4,5,10])

APP_PORT = 8300
METRICS_PORT = 8301

class HandleRequests(http.server.BaseHTTPRequestHandler):

    @REQUEST_RESPOND_TIME.time()
    def do_GET(self):
        time.sleep(1)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>First Application</title></head><body style='color: #333; margin-top: 30px;'><center><h2>Welcome to our first Prometheus-Python application.</center></h2></body></html>", "utf-8"))
        self.wfile.close()
        REQUEST_RESPOND_TIME.observe(time_taken)


if __name__ == "__main__":
    start_http_server(METRICS_PORT)
    server = http.server.HTTPServer(('0.0.0.0', APP_PORT), HandleRequests)
    server.serve_forever()
