from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def company_details_view(request):
    return Response({
        'company_name': 'Клуб дедов-бегунов',
        'slogan': 'Бегаем в любую погоду!',
        'contacts': 'Мы везде!'
        })


