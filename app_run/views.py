from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

# @api_view(['GET'])
# def company_details_view(request):
#     return Response({
#         'company_name': 'Клуб дедов-бегунов',
#         'slogan': 'Бегаем в любую погоду!',
#         'contacts': 'Мы везде!'
#         }, status=status.HTTP_200_OK)


@api_view(['GET'])
def company_details(request):
    details = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(details)




