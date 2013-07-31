from rest_framework import viewsets, routers
from .models import Story


# ViewSets define the view behavior.
class StoryViewSet(viewsets.ModelViewSet):
    model = Story


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'stories', StoryViewSet)
