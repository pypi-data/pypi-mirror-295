from .models import UserLog
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_country(ip):
    g = GeoIP2()
    try:
        country = g.country(ip)['country_name']
    except:
        country = 'Unknown'
    return country


class UserLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        ip_address = get_client_ip(request)
        country = get_user_country(ip_address)
        full_path = request.build_absolute_uri()

        # Save the log
        UserLog.objects.create(
            ip_address=ip_address,
            country=country,
            path=full_path,
            timestamp=timezone.now(),
        )

        return response
