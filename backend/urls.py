from django.http import Http404
import os
from django.urls import include, path
from io import StringIO
from wsgiref.util import FileWrapper

from io import BytesIO
"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views import generic
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
import json
from django.http import HttpResponse
from rest_framework import views, serializers, status
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)


host = 'http://localhost:8000'
profile_data = {
    "name": "Dean Stevenson",
    "profile": host + "/static/img/profile.jpg"
}


def jsonFromFile(filename):
    f = open("./data/" + filename, 'r')
    return HttpResponse(f.read())


def profile(request):
    return HttpResponse(json.dumps(profile_data))


def exercise_list(request):
    return jsonFromFile("exercise_list.json")


def download_answer(request):
    id = request.GET.get('id', None)
    start_date = request.GET.get('startDate', None)
    end_date = request.GET.get('endDate', None)
    f = open("./data/exercise_list.json", "r")
    f = f.read()

    content = json.loads(f)
    content = [row for row in content if row["date"] >=
               start_date and row["date"] <= end_date]
    content = json.dumps(content)
    print(id)
    print(start_date)
    print(end_date)

    json_file = StringIO()
    json_file.write(content)
    json_file.seek(0)
    wrapper = FileWrapper(json_file)
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachement; filename=dump.json'

    return response


def matrix_file(request):
    return jsonFromFile("matrix_data.json")


def edit_exercise(request):
    file = request.FILES['file']
    fs = FileSystemStorage()
    fs.save('upload/' + file.name, file)
    data = request.POST.get('data')
    print(data)
    # data = json.loads(data)

    # if "id" in body:
    #     exercise = getExercise(body["id"])
    #     exercise = edit(exercise, body)
    # else:
    #     exercise = createNewExercise()
    return HttpResponse("OK")


def exercise_data(request, id):
    return jsonFromFile('exercise_data.json')


def download(request, path):

    file_path = os.path.join("./static/upload", path)
    print(path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404


urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(
        url='/api/', permanent=False)),
    url(r'^api/$', get_schema_view()),
    url(r'^api/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
    url(r'^api/profile$', profile),
    url(r'^api/exercise-list$', exercise_list),
    url(r'^api/exercise/download-answer$', download_answer),
    url(r'^api/exercise/(\d+)$', exercise_data),
    url(r'^api/upload/matrixfile$', matrix_file),
    url(r'^api/create-exercise/', edit_exercise),
    url(r'^api/edit-exercise/', edit_exercise),
    url(r'^api/download/(.+)$', download),
    url(r'^api/student/', include('student.urls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
