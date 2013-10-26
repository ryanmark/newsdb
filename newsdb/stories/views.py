from rest_framework.response import Response
#from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from .models import Piece
from .serializers import PieceSerializer


@api_view(['GET'])
def hello(request):
    return Response("Hello!")


@api_view(['GET', 'POST'])
def pieces(request):
    if request.method == 'GET':
        pieces = Piece.objects.all()
        serializer = PieceSerializer(
            pieces, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        piece_data = PieceSerializer(data=request.DATA)
        print("valid" if piece_data.is_valid() else "bad")
        print(piece_data.errors)

        piece = piece_data.object
        piece.save()

        serializer = PieceSerializer(piece, context={'request': request})
        return Response(serializer.data)


def piece_detail(request):
    pass
