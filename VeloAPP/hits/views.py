from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from .models import Hit, Artist
from .serializers import HitSerializer

# Create your views here.

class HitListView(APIView):
    def get(self, request):
        hits = Hit.objects.all().order_by('-created_at')[:20]
        serializer = HitSerializer(hits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HitDetailView(APIView):
    def get(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        serializer = HitSerializer(hit)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HitCreateView(APIView):
    def post(self, request):
        data = request.data.copy()
        # Automatyczne generowanie title_url
        if 'title' in data:
            data['title_url'] = slugify(data['title'])
        serializer = HitSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 201 przy utworzeniu
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 przy błędnych danych

class HitUpdateView(APIView):
    def put(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        data = request.data.copy()
        # Jeśli aktualizujemy tytuł, generujemy nowy title_url
        if 'title' in data:
            data['title_url'] = slugify(data['title'])
        serializer = HitSerializer(hit, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # 200 przy sukcesie
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 przy błędnych danych

class HitDeleteView(APIView):
    def delete(self, request, title_url):
        hit = get_object_or_404(Hit, title_url=title_url)
        hit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # 204 po usunięciu
