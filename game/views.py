import json
from django.shortcuts import render
from rest_framework import viewsets, status # class view
from rest_framework.renderers import JSONRenderer # class view
from rest_framework.response import Response # update database
from rest_framework.decorators import action # update database
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .spiel import Spiel
from .models import Score
from .serializers import SerializerScore

# Initialize the board
# centerx, centery, distcc = 10, 10, 5  # Replace with actual values
spiel1 = Spiel()
lst1 = [(1, 2), (50, 50), (20, 30)]  # Example positions

def test_react(request):
    return render(request, "index.html")

def index(request):
    return render(request, "game/index.html", {"lst_board": lst1})

def return_board(request):
    return JsonResponse(spiel1.board.lst_board, safe=False)

@csrf_exempt
def starten(request):
    # this should start game. Front should send nr_player here and reset game
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            nr_player = int(data.get("nrPlayer", 0))
            spiel1.reset(nr_player)
            return JsonResponse(spiel1.get_ll_piece(), safe=False)

        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # This disables CSRF for this view
def klicken(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))  # Parse JSON
            coord_round = (int(data.get("xr", 0)), int(data.get("yr", 0)))
            selected, valid_pos, neue_figuren, order, gewonnen = spiel1.klicken(coord_round)

            return JsonResponse({
                "selected": selected,
                "validPos": valid_pos,
                "neueFiguren": neue_figuren,
                # "coordFrom": coord_from,
                # "coordTo": coord_to,
                "order": order,
                "gewonnen": gewonnen
            })
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

# def reset(request):
#     spiel1.reset(3)
#     return JsonResponse({})

# def return_score(request):
#     return JsonResponse({'scores':Score.objects.all()})

class ViewsetScore(viewsets.ModelViewSet):
    queryset = Score.objects.all().order_by('score')[:5]
    serializer_class = SerializerScore
    renderer_classes = [JSONRenderer] # otherwise it will search for html template, which doesn't exist
    
    @action(detail=False, methods=['post'])
    def add_score(self, request):
        score = request.data.get('score')
        name = request.data.get('name')

        if not score or not name or len(name) > 20:
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the new score to the database
        Score.objects.create(score=score, name=name)

        # Maintain a maximum of 5 rows in the database, remove the highest score if needed
        scores = Score.objects.all().order_by('score')
        if scores.count() > 5:
            scores.last().delete()

        return Response({'success': 'Score added'}, status=status.HTTP_201_CREATED)

# def home(request):
#     context = {
#         'posts': Score.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

# def klicken(request):
#     if request.method == "POST":
#         data = request.POST
#         coord_round = (int(data.get("xr", 0)), int(data.get("yr", 0)))
#         selected, valid_pos, coord_from, coord_to = board1.klicken(coord_round)
#         print(data)
#         return JsonResponse({"selected": selected, "validPos": valid_pos, "coordFrom": coord_from, "coordTo": coord_to})
#     return JsonResponse({"error": "Invalid request"}, status=400)
