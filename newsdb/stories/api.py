from rest_framework.response import Response
#from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from models import Story


@api_view(['GET'])
def hello(request):
    return Response("Hello!")


@api_view(['GET'])
def stories(request):
    return Response(Story.objects.all())
