# Caching Proxy Server

This project implements a simple caching proxy server in Python. The server fetches content from a specified origin server, caches the responses, and serves cached content for subsequent requests, improving efficiency and reducing load on the origin server.

## Features

- Caches responses from the origin server to serve future requests faster.
- Stores cache persistently using pickle.
- Supports cache clearing functionality.
- Can be run with customizable port and origin URL parameters.

## Requirements

- Python 3.x
- `requests` library (can be installed via pip)

## Installation and Usage

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required libraries:
   ```bash
   pip install requests
    ```
4. Run the server:
5. ```bash
   python main.py --port <port> --origin <origin>
   ```
   
    Replace `<port>` with the desired port number (default is 8080) and `<origin>` with the URL of the origin server.
6. Access the proxy server at `http://localhost:<port>`.
7. To clear the cache:
   ```bash
   python main.py --clear-cache
   ```

Project url: https://roadmap.sh/projects/caching-server