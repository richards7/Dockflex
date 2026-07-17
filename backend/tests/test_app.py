"""Smoke tests executed against the built Docker image by Jenkins."""

import io
import unittest

from docx import Document
from PIL import Image

from app import app


class DocFlexAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_frontend_and_manifest_are_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        response.close()
        response = self.client.get("/static/manifest.json")
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_image_upload_converts_to_pdf(self):
        image = Image.new("RGB", (48, 32), "#3157d5")
        payload = io.BytesIO()
        image.save(payload, "PNG")
        payload.seek(0)

        response = self.client.post(
            "/upload",
            data={"file": (payload, "jenkins-test.png")},
            content_type="multipart/form-data",
        )

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, "application/pdf")
            self.assertTrue(response.data.startswith(b"%PDF"))
        finally:
            response.close()

    def test_docx_upload_converts_to_pdf(self):
        document = Document()
        document.add_heading("DocFlex Jenkins test", 0)
        payload = io.BytesIO()
        document.save(payload)
        payload.seek(0)

        response = self.client.post(
            "/upload",
            data={"file": (payload, "jenkins-test.docx")},
            content_type="multipart/form-data",
        )

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, "application/pdf")
            self.assertTrue(response.data.startswith(b"%PDF"))
        finally:
            response.close()

    def test_rejects_unsupported_upload(self):
        response = self.client.post(
            "/upload",
            data={"file": (io.BytesIO(b"not a document"), "file.txt")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
