from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .serializers import RunSerializer, UserSerializer
from rest_framework import viewsets
from .models import Run, User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination



@api_view(['GET'])
def company_details(request):
    details = {'company_name': settings.COMPANY_NAME,
               'slogan': settings.SLOGAN,
               'contacts': settings.CONTACTS}
    return Response(details)


class RunPagination(PageNumberPagination):
    page_size_query_param = 'size'


class UserPagination(PageNumberPagination):
    page_size_query_param = 'size'


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']
    pagination_class = RunPagination


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']
    filter_backends = ['date_joined']
    pagination_class = UserPagination

    def get_queryset(self):
        qs = User.objects.filter(is_superuser=False)
        user_type = self.request.query_params.get('type')
        if user_type == 'coach':
            qs = qs.filter(is_staff=True)
        elif user_type == 'athlete':
            qs = qs.filter(is_staff=False)
        return qs


class RunStartView(APIView):
    def post(self, request, **kwargs):
        try:
            run = Run.objects.get(pk=kwargs.get('id'))
        except Run.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if run.status == 'in_progress':
            return Response({"detail": "Bad request."}, status=status.HTTP_400_BAD_REQUEST)
        elif run.status == 'finished':
            return Response({"detail": "Run already finished."}, status=status.HTTP_400_BAD_REQUEST)

        run.status = 'in_progress'
        run.save()
        return Response(RunSerializer(run).data, status=status.HTTP_200_OK)


class RunStopView(APIView):
    def post(self, request, **kwargs):
        try:
            run = Run.objects.get(pk=kwargs.get('id'))
        except Run.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if run.status == 'init':
            return Response({"detail": "Run not started yet."}, status=status.HTTP_400_BAD_REQUEST)
        if run.status == 'finished':
            return Response({"detail": "Run already finished."}, status=status.HTTP_400_BAD_REQUEST)

        run.status = 'finished'
        run.save()
        return Response(RunSerializer(run).data, status=status.HTTP_200_OK)





