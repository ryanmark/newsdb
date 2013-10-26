from rest_framework.response import Response
#from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from .models import Taxonomy
from .serializers import TaxonomySerializer


@api_view(['GET', 'POST'])
def taxonomies(request):
    if request.method == 'GET':
        pieces = Taxonomy.objects.all()
        serializer = TaxonomySerializer(
            pieces, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        piece_data = TaxonomySerializer(data=request.DATA)
        print("valid" if piece_data.is_valid() else "bad")
        print(piece_data.errors)

        piece = piece_data.object
        piece.save()

        serializer = TaxonomySerializer(piece, context={'request': request})
        return Response(serializer.data)


def taxonomy_detail(request):
    pass


def terms(request):
    pass


def term_detail(request):
    pass
