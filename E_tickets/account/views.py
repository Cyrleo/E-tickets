from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Permet uniquement l'accès aux utilisateurs authentifiés

    def get(self, request):
        return Response({'message': 'Vous êtes authentifié !'})