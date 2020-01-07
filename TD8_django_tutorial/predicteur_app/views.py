from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io

from .models import House
from .serializers import HouseSerializer
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # This is a view
    return HttpResponse("Your are on the main page: isn't it beautiful ?")

@csrf_exempt
def i_want_a_list(request):
    if request.method == "GET":
        houses = House.objects.all()
        serializer = HouseSerializer(houses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        content = JSONParser().parse(request)
        serializer = HouseSerializer(data = content)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def house_detail(request, house_id):
    try:
        house = House.objects.get(pk=house_id)
    except House.DoesNotExist:
        return HttpResponse(str(house_id), status=404)
    if request.method == "GET":
        serializer = HouseSerializer(house)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        # je recup le content du request et parse en JSON
        content = JSONParser().parse(request)
        # je serialise le JSON en instance de House
        serializer = HouseSerializer(house) # , data = content)
        #if serializer.is_valid():
        #    serializer.save()
        #    return JsonResponse(serializer.data, status=201)

        #return JsonResponse(serializer.errors, status=400)
        serializer.update(house, content)

        return JsonResponse(serializer.data, status=201)
    elif request.method == "DELETE":
        house.delete()
        return HttpResponse("Suppression faite!", status=204)

def predict_medv(unscaled_data):
    from sklearn.externals import joblib
    colonnes        = ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM",
                        "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B",
                        "LSTAT"]
    path_to_model   = "./ipynb/model_simple.sav"
    path_for_scaler = "./ipynb/scaler.sav"
    unscaled_data   = [unscaled_data[colonne] for colonne in colonnes]
    model           = joblib.load(path_to_model)
    scaler          = joblib.load(path_for_scaler)
    donnees_scalees = scaler.transform([unscaled_data])
    medv            = model.predict(donnees_scalees)
    return medv

@csrf_exempt
def predict(request):
    """
    Renvoie une house avec la MEDV completee
    (Attend une MEDV innexistante == null)
    """
    if request.method == 'GET':
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'POST':
        data        = JSONParser().parse(request)
        serializer  = HouseSerializer(data=data)
        if serializer.is_valid():
            data["MEDV"]        = predict_medv(data)
            serializer          = HouseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data  , status=201)
        return     JsonResponse(serializer.errors, status=400)
