from urllib2 import urlopen
from zipfile import ZipFile
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from StringIO import StringIO
from django.core.servers.basehttp import FileWrapper

from .utils import validate_url, add_hash_to_file


@api_view(['GET'])
def add_watermark(request, order_hash):
    url = request.query_params.get('url', False)
    validation_data = validate_url(url)
    if validation_data['status']:
        try:
            filename = url.split('/')[-1]
            if '.epub' not in filename:
                raise Exception('File must be in .epub format.')
            url_data = urlopen(url)
            zipfile = ZipFile(StringIO(url_data.read()))
            new_filename = add_hash_to_file(zipfile, order_hash)
            response = HttpResponse(FileWrapper(open(new_filename, 'rb')),
                                    content_type='application/x-zip-compressed')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            zipfile.close()
            return response
        except Exception as e:
            validation_data['status'] = False
            validation_data['message'] = str(e)
    return Response(validation_data, status=status.HTTP_400_BAD_REQUEST)