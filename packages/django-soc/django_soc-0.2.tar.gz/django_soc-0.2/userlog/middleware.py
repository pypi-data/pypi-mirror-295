from .models import UserLog
import datetime

class UserLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR')
        # Get user country
        user_country = request.META.get('GEOIP_COUNTRY_NAME')

        path = request.path
        timestamp = datetime.datetime.now()
        # Log the data to the database
        host = request.get_host()
        # get the full path
        full_path = request.get_full_path()
        UserLog.objects.create(ip_address=full_path,country=user_country, path=path, timestamp=timestamp)
        response = self.get_response(request)
        return response
