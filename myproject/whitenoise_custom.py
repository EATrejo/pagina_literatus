# whitenoise_custom.py
from whitenoise import WhiteNoise
from django.conf import settings


class CustomWhiteNoise(WhiteNoise):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL.strip('/'))

application = CustomWhiteNoise(get_wsgi_application())