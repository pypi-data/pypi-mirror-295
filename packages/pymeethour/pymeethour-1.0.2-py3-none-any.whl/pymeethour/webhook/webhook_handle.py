import json
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from key import SECRET_KEY
from webhooks import WebhookHandler  # Import WebhookHandler from webhooks.py


class MyHandler(BaseHTTPRequestHandler):
    """ """

    # Initialize WebhookHandler with SECRET_KEY
    webhook_handler = WebhookHandler(SECRET_KEY)

    def do_POST(self):
        """ """
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()

        # Handle the request and get the response and status code
        response, status = self.webhook_handler.handle_request(
            post_data, self.headers)

        # Log the incoming data using WebhookHandler's log_data method
        self.webhook_handler.log_data(post_data)

        # Print server response (optional)
        print(f"Server response: {response}")

        # Send HTTP response back to the client
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())


def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    """

    :param server_class: Default value = HTTPServer)
    :param handler_class: Default value = MyHandler)
    :param port: Default value = 8080)

    """
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")  # Server port details
    httpd.serve_forever()


if __name__ == "__main__":
    run()
