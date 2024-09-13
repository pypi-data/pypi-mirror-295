from django.shortcuts import render
from .models import UserLog
# import get_template



def userlog_view(request):
    logs = UserLog.objects.all().order_by('-timestamp')
    return render(request, 'logs.html', {'logs': logs})
