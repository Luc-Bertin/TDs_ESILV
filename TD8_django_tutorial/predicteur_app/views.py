from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io

from .models import House

def index(request):
    # This is a view
    return HttpResponse("Your are on the main page: isn't it beautiful ?")

def i_want_a_list(request):
    if request.method == "GET":
        houses = House.objects.all()
        serializer = HouseSerializer(houses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        content = JSONParser().parse(io.BytesIO(request))
        serializer = HouseSerializer(data = content)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def house_detail(request, pk):
    try:
        house = House.objects.get(pk)
    except House.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = HouseSerializer(house)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        # je recup le content du request et parse en JSON
        content = JSONParser().parse(io.BytesIO(request))
        # je serialise le JSON en instance de House
        serializer = HouseSerializer(data = house)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        house.delete()
        return HttpResponse("Suppression faite!", status=204)
