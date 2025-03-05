import json
import pickle
import base64
from django.shortcuts import render
# from rest_framework import viewsets, status # class view
from rest_framework.renderers import JSONRenderer # class view
from rest_framework.response import Response # update database
from rest_framework.decorators import api_view, renderer_classes #action, update database
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from .spiel import Spiel
from .models import Score
from .serializers import SerializerScore

# spiel1 = Spiel()
# Um ein Server für mehrere Spieler zu erstellen, darf man Spiel nicht als eine globale Variable erstellen

def home(request):
    return render(request, "index.html") # from react build

def return_board(request):
    request.session['test_home']='test_home'
    if 'spiel' in request.session.keys():
        print('Spiel has ben created')
    else:
        print('Create new game')
        spiel1 = Spiel()
        request.session["spiel"]= base64.b64encode(pickle.dumps(spiel1)).decode('utf-8')
    return JsonResponse(spiel1.board.lst_board_round, safe=False)

# @csrf_exempt
@api_view(['POST'])
def starten(request):
    """this should start game. Front should send nr_player here and reset game"""
    print(request.session.keys())
    try:
        nr_player = int(request.data.get("nrPlayer", 0))  # DRF auto-parses JSON
        spiel1 = pickle.loads(base64.b64decode(request.session.get('spiel').encode('utf-8')))
        spiel1.reset(nr_player)
        request.session["spiel"]= base64.b64encode(pickle.dumps(spiel1)).decode('utf-8')
        return Response(spiel1.get_ll_piece())  # DRF auto-handles JSON response
    except (TypeError, ValueError):
        return Response({"error": "Invalid input"}, status=400)

# @csrf_exempt  # This disables 'Cross-site request forgery' for this view
@api_view(['POST'])  # DRF handles JSON & CSRF protection
def klicken(request):
    try:
        coord_round = (int(request.data.get("xr", 0)), int(request.data.get("yr", 0)))
        spiel1 = pickle.loads(base64.b64decode(request.session.get('spiel').encode('utf-8')))
        selected, valid_pos, neue_figuren, order, gewonnen = spiel1.klicken(coord_round)
        request.session["spiel"]= base64.b64encode(pickle.dumps(spiel1)).decode('utf-8')
        return Response({
            "selected": selected,
            "validPos": valid_pos,
            "neueFiguren": neue_figuren,
            "order": order,
            "gewonnen": gewonnen
        })
    except (TypeError, ValueError):
        return Response({"error": "Invalid JSON data"}, status=400)

@api_view(['GET'])
@renderer_classes([JSONRenderer])  # Ensure response is JSON
def get_scores(request):
    scores = Score.objects.all().order_by('score')[:5]
    serializer = SerializerScore(scores, many=True) # serializing multiple object
    return Response(serializer.data)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def add_score(request):
    score = request.data.get('score')
    name = request.data.get('name')

    if not score or not name or len(name) > 20:
        return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
    Score.objects.create(score=score, name=name)
    scores = Score.objects.all().order_by('score')
    if scores.count() > 5:
        scores.last().delete()

    return Response({'success': 'Score added'}, status=status.HTTP_201_CREATED)

# class ViewsetScore(viewsets.ModelViewSet):
#     queryset = Score.objects.all().order_by('score')[:5]
#     serializer_class = SerializerScore
#     renderer_classes = [JSONRenderer] # otherwise it will search for html template, which doesn't exist
    
#     @action(detail=False, methods=['post'])
#     def add_score(self, request):
#         score = request.data.get('score')
#         name = request.data.get('name')

#         if not score or not name or len(name) > 20:
#             return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

#         # Add the new score to the database
#         Score.objects.create(score=score, name=name)

#         # Maintain a maximum of 5 rows in the database, remove the highest score if needed
#         scores = Score.objects.all().order_by('score')
#         if scores.count() > 5:
#             scores.last().delete()

#         return Response({'success': 'Score added'}, status=status.HTTP_201_CREATED)
