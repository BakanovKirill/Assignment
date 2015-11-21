import zipfile
from django.test import TestCase
from StringIO import StringIO
from rest_framework.test import APIRequestFactory, APIClient
import hashlib

client = APIClient()


class CommonTestCase(TestCase):
    def test_watermark_adding(self):
        """
        Make the request to the watermarking view and
        check if the order hash is really added to the container.xml
        """

        m = hashlib.md5()
        m.update('some random string')
        order_hash = m.hexdigest()
        book_url = 'https://s3.eu-central-1.amazonaws.com/saxo-static/ebooks/line-vindernovelle-i-krimidysten.epub'
        # Getting the actual view response
        response = client.get('/add_watermark/%s/?url=%s' % (order_hash, book_url))
        self.assertEqual(200, response.status_code)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=line-vindernovelle-i-krimidysten.epub"
        )
        zipped_file = zipfile.ZipFile(StringIO(response.content), 'r')
        try:
            self.assertIsNone(zipped_file.testzip())
            self.assertIn('META-INF/container.xml', zipped_file.namelist())
            for item in zipped_file.infolist():
                if item.filename == 'META-INF/container.xml':
                    data = zipped_file.read(item.filename)
                    # Checking if the watermark is in the file contents
                    self.assertTrue(order_hash in data)
        finally:
            zipped_file.close()