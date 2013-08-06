from rest_framework.response import Response
#from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from .models import Story
from .serializers import StorySerializer


@api_view(['GET'])
def hello(request):
    return Response("Hello!")


@api_view(['GET', 'POST'])
def stories(request):
    if request.method == 'GET':
        stories = Story.objects.all()
        serializer = StorySerializer(
            stories, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        story_data = StorySerializer(data=request.DATA)
        print("valid" if story_data.is_valid() else "bad")
        print(story_data.errors)

        story = story_data.object
        story.save()

        serializer = StorySerializer(story, context={'request': request})
        return Response(serializer.data)


def story_detail(request):
    pass


