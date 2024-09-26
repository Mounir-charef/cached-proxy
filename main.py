import argparse
import http.server
import socketserver
import requests
from urllib.parse import urlparse
import os
import pickle

CACHE_FILE = 'proxy_cache.pkl'


class CachingProxy(http.server.SimpleHTTPRequestHandler):
    cache = {}

    def __init__(self, *args, origin=None, **kwargs):
        self.origin_url = origin
        super().__init__(*args, **kwargs)

    def save_cache(self):
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(self.cache, f)

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as f:
                self.cache = pickle.load(f)

    @classmethod
    def clear_cache(cls):
        cls.cache = {}
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        print("Cache cleared.")

    def do_GET(self):
        parsed_path = urlparse(self.path)
        request_url = f"{self.origin_url}{parsed_path.path}"

        # Load cache from file if not already loaded
        if not CachingProxy.cache:
            self.load_cache()

        if request_url in self.cache:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("X-Cache", "HIT")
            self.end_headers()
            self.wfile.write(self.cache[request_url])
        else:
            print(f"Cache miss for {request_url}. Fetching from origin.")
            response = requests.get(request_url)

            if response.status_code != 200:
                return self.send_error(response.status_code, response.reason)

            self.cache[request_url] = response.content
            self.save_cache()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("X-Cache", "MISS")
            self.end_headers()
            self.wfile.write(response.content)


def run_server(port, origin):
    def handle_factory(*args, **kwargs):
        return CachingProxy(*args, origin=origin, **kwargs)

    with socketserver.TCPServer(("", port), handle_factory) as httpd:
        print(f"Proxy server running on port {port}")
        httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Caching Proxy Server")
    parser.add_argument("--port", type=int, help="Port on which the proxy will run")
    parser.add_argument("--origin", type=str, help="Origin server URL")
    parser.add_argument("--clear-cache", action="store_true", help="Clear the cache and exit")

    arguments = parser.parse_args()

    if arguments.clear_cache:
        CachingProxy.clear_cache()
    else:
        if not arguments.port or not arguments.origin:
            parser.error("--port and --origin are required if not using --clear-cache")
        run_server(arguments.port, arguments.origin)
