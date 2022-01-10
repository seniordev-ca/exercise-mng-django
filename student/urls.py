from datetime import timedelta
import json
from django.urls import path
from django.conf.urls import url, include
from . import views

from django.shortcuts import render

# Create your views here.
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from django.http import HttpResponse
from calendar import timegm
from django.contrib.auth import get_user_model
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def studentTokenObtain(request):
    body = json.loads(request.body)
    User = get_user_model()
    email = body['email']
    username = body['firstName'] + " " + body['lastName']
    my_user = User(email=email, username=username, password="qwer")
    payload = jwt_payload_handler(my_user)
    payload1 = payload
    payload1["exp"] = payload["exp"] + timedelta(days=1)
    data = jwt_encode_handler(payload)
    data1 = jwt_encode_handler(payload1)

    response = HttpResponse(json.dumps(
        {"access": data, "refresh": data1, 'role': 'student'}))
    response['Content-Type'] = "application/json"
    return response


def studentTokenRefresh(request):
    return


def getExerciseName(request):
    exercise_id = request.GET.get('exercise')
    if exercise_id == "12345":
        response = HttpResponse(json.dumps({"name": "Firsts Exercise"}))
    else:
        response = HttpResponse(json.dumps({"name": "Second Exercise"}))
    response['Content-Type'] = "application/json"
    return response


def jsonFromFile(filename):
    f = open("./data/" + filename, 'r')

    return HttpResponse(f.read())


def student_exercise(request, exercise_id):
    return jsonFromFile("student_exercise.json")


def submit_exercise(request):
    data = json.loads(request.body)
    if data["exercise"] == "12345":
        return jsonFromFile("exercise_result_hidden.json")
    # if data.exercise == "qwert":
    else:
        return jsonFromFile("exercise_result_shown.json")


urlpatterns = [
    url(r'^auth/token/refresh/$', studentTokenRefresh),
    url(r'^auth/token/obtain/$', studentTokenObtain),
    url(r'^get-exercise-name$', getExerciseName),
    url(r'^exercise-data/(.+)$', student_exercise),
    url(r'^submit$', submit_exercise),
]
