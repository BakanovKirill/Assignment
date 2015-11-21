import os
import tempfile
import zipfile
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from datetime import datetime


def validate_url(url):
    if not url:
        return {'status': False, 'message': 'No url provided'}
    url_validator = URLValidator()
    try:
        url_validator(url)
    except ValidationError:
        return {'status': False, 'message': 'Invalid url'}
    return {'status': True}


def add_hash_to_file(source, order_hash):
    tempdir = tempfile.mkdtemp()
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S:%f')

    tempname = os.path.join(tempdir, 'new_%s.epub' % timestamp)
    with zipfile.ZipFile(tempname, 'w') as zipwrite:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == 'META-INF/container.xml':
                data += '<!-- %s %s -->' % (order_hash, timestamp)
            zipwrite.writestr(item, data)
    return tempname