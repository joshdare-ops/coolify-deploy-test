import io
import unittest
from http.client import HTTPResponse

from server import Handler


class InMemoryConnection:
    def __init__(self, request):
        self.request = io.BytesIO(request)
        self.response = io.BytesIO()

    def makefile(self, mode, *args):
        return self.request

    def sendall(self, data):
        self.response.write(data)


class ResponseSocket:
    def __init__(self, data):
        self.data = data

    def makefile(self, mode):
        return io.BytesIO(self.data)


class ServerTests(unittest.TestCase):
    def get(self, path):
        connection = InMemoryConnection(
            f"GET {path} HTTP/1.0\r\n\r\n".encode("ascii")
        )
        Handler(connection, ("127.0.0.1", 0), None)
        response = HTTPResponse(ResponseSocket(connection.response.getvalue()))
        response.begin()
        return response.status, response.read().decode("utf-8")

    def test_root(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("VERSION=2", body)

    def test_health(self):
        for path in ("/health", "/health/"):
            with self.subTest(path=path):
                status, _ = self.get(path)
                self.assertEqual(status, 200)

    def test_missing(self):
        status, _ = self.get("/missing")
        self.assertEqual(status, 404)
