import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Spiel

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
def return_pieces(request):
    # this should be start game. Front should send nr_player here and reset game
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            nr_player = int(data.get("nrPlayer", 0))
            spiel1.reset(nr_player)
            return JsonResponse(spiel1.get_ll_piece(), safe=False)

        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


# def find_valid_pos(request):
#     if request.method == "POST":
#         data = request.POST
#         coord_round = (int(data.get("xr", 0)), int(data.get("yr", 0)))
#         lst_valid_pos = board1.find_valid_pos(coord_round)
#         return JsonResponse(lst_valid_pos, safe=False)
#     return JsonResponse({"error": "Invalid request"}, status=400)

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

def reset(request):
    spiel1.reset(3)
    return JsonResponse({})
# def klicken(request):
#     if request.method == "POST":
#         data = request.POST
#         coord_round = (int(data.get("xr", 0)), int(data.get("yr", 0)))
#         selected, valid_pos, coord_from, coord_to = board1.klicken(coord_round)
#         print(data)
#         return JsonResponse({"selected": selected, "validPos": valid_pos, "coordFrom": coord_from, "coordTo": coord_to})
#     return JsonResponse({"error": "Invalid request"}, status=400)
