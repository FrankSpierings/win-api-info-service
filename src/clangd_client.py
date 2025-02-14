import subprocess
import threading
import queue
import json

class ClangdClient:
    def __init__(self, clangd_path="clangd"):
        self.process = subprocess.Popen(
            [clangd_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.request_id = 1
        self.response_queue = queue.Queue()
        self._start_listener()

    def _start_listener(self):
        """Starts a background thread to listen for responses from clangd."""
        def listen():
            while True:
                try:
                    length_line = self.process.stdout.readline()
                    if not length_line.startswith("Content-Length: "):
                        continue
                    content_length = int(length_line.strip().split(": ")[1])
                    self.process.stdout.readline()  # Empty line
                    content = self.process.stdout.read(content_length)
                    response = json.loads(content)
                    self.response_queue.put(response)
                except Exception as e:
                    print("Error reading from clangd:", e)
                    break
        
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def send_request(self, method, params):
        """Sends a request to clangd and waits for a response."""
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }
        self.request_id += 1
        self._send_message(json.dumps(request))
        return self.response_queue.get()

    def send_notification(self, method, params):
        """Sends a notification (no response expected)."""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self._send_message(json.dumps(notification))

    def _send_message(self, message):
        """Formats and sends a message to clangd."""
        full_message = f"Content-Length: {len(message)}\r\n\r\n{message}"
        self.process.stdin.write(full_message)
        self.process.stdin.flush()

    def initialize(self):
        """Initializes clangd LSP connection."""
        params = {
            "processId": None,
            "rootUri": None,
            "capabilities": {
                "textDocument": {
                    "completion": {
                        "completionItem": {
                            "snippetSupport": True
                        },
                    },
                },
            },
            "trace": "off"
        }
        return self.send_request("initialize", params)

    def open_file(self, filepath, text):
        """Notifies clangd about opening a file."""
        params = {
            "textDocument": {
                "uri": f"file://{filepath}",
                "languageId": "c",
                "version": 1,
                "text": text
            }
        }
        self.send_notification("textDocument/didOpen", params)

    def request_signature(self, filepath, line, character):
        """Requests code completion at a given position."""
        params = {
            "textDocument": {"uri": f"file://{filepath}"},
            "position": {"line": line, "character": character},
        }
        return self.send_request("textDocument/signatureHelp", params)

    def shutdown(self):
        """Shuts down clangd gracefully."""
        self.send_request("shutdown", {})
        self.send_notification("exit", {})