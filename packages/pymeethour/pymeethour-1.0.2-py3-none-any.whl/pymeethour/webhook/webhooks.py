import hmac
import json
import time
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac as CryptoHMAC


class WebhookHandler:
    """ """

    def __init__(self, secret):
        self.secret = secret

    def handle_request(self, request_body, headers):
        """

        :param request_body: param headers:
        :param headers:

        """
        payload = request_body
        signature = headers.get("X-Signature")

        if signature and self.validate_signature(payload, signature):
            try:
                data = json.loads(payload)
                self.log_data(data)
                response, status_code = self.process_event(data, payload)
            except json.JSONDecodeError:
                response = {
                    "status": False,
                    "code": 400,
                    "message": "Invalid JSON payload.",
                    "data": None,
                }
                status_code = 400
        else:
            response = {
                "status": False,
                "code": 400,
                "message": "Invalid signature or signature missing.",
                "data": None,
            }
            status_code = 400

        return json.dumps(response), status_code

    def validate_signature(self, payload, signature):
        """

        :param payload: param signature:
        :param signature:

        """
        h = CryptoHMAC.HMAC(self.secret.encode(),
                            hashes.SHA256(),
                            backend=default_backend())
        h.update(payload.encode())
        expected_signature = h.finalize().hex()
        return hmac.compare_digest(expected_signature, signature)

    def process_event(self, data, payload):
        """

        :param data: param payload:
        :param payload:

        """
        event_type = data.get("event_type")
        if event_type == "join_meeting":
            return self.handle_join_meeting(data)
        elif event_type == "exit_meeting":
            return self.handle_exit_meeting(data)
        elif event_type == "save_meeting_recording":
            return self.handle_save_meeting_recording(data)
        else:
            return {
                "status": False,
                "code": 400,
                "message": f"Unknown event type: {event_type}",
                "data": None,
            }, 400

    def handle_join_meeting(self, data):
        """

        :param data:

        """
        response = {
            "status": True,
            "code": 200,
            "message": "Join meeting event processed",
            "event_type": data.get("event_type"),
            "event_id": data.get("event_id"),
            "timestamp": data.get("timestamp"),
            "data": data,
        }
        return response, 200

    def handle_exit_meeting(self, data):
        """

        :param data:

        """
        response = {
            "status": True,
            "code": 200,
            "message": "Exit meeting event processed",
            "event_type": data.get("event_type"),
            "event_id": data.get("event_id"),
            "timestamp": data.get("timestamp"),
            "data": data,
        }
        return response, 200

    def handle_save_meeting_recording(self, data):
        """

        :param data:

        """
        response = {
            "status": True,
            "code": 200,
            "message": "Save meeting recording event processed",
            "event_type": data.get("event_type"),
            "event_id": data.get("event_id"),
            "timestamp": data.get("timestamp"),
            "data": data,
        }
        return response, 200

    def log_data(self, data):
        """

        :param data:

        """
        # Replace with your actual logging logic here
        pass  # No print statement or other logging method shown
