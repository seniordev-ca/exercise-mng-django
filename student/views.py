from django.shortcuts import render

# Create your views here.
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from django.http import HttpResponse

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def studentTokenObtain(request):
  my_user = User.objects.get(pk=1)
  payload = jwt_payload_handler(my_user)
  if api_settings.JWT_ALLOW_REFRESH:
    payload['orig_iat'] = timegm(
        datetime.utcnow().utctimetuple()
    )
  token = {'token': jwt_encode_handler(payload)}

  return HttpResponse(json.dumps(token))


def studentTokenRefresh(request):
  return 