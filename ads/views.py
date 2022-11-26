from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Selection
from ads.permissions import IsOwnerSelection, IsOwnerAdOrStaff
from ads.serializers import (AdCreateSerializer, AdSerializer, AdUpdateSerializer, AdImageSerializer,
                             AdDetailSerializer, SelectionCreateSerializer, SelectionListSerializer,
                             SelectionDetailSerializer, CategorySerializer)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def root(request):
    return JsonResponse({"status": "ok"})


class CategoryViewSet(ModelViewSet):
    """
    Реализовал CRUD с помощью ModelViewSet,
    тем самым нет необходимости писать каждый метод для категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        """Фильтр по id категории"""
        categories = request.GET.getlist('cat', None)
        cat_query = None

        for cat_id in categories:
            if cat_query is None:
                cat_query = Q(category__id__exact=cat_id)
            else:
                cat_query |= Q(category__id__exact=cat_id)

        if cat_query:
            self.queryset = self.queryset.filter(cat_query)

        """Фильтр по тексту объявления"""
        ad_name = request.GET.get('text', None)
        if ad_name:
            self.queryset = self.queryset.filter(
                name__icontains=ad_name
            )

        """Фильтр по местоположению пользователя"""
        user_location = request.GET.get('location', None)
        if user_location:
            self.queryset = self.queryset.filter(
                author__location__name__icontains=user_location
            )

        """Фильтр по цене"""
        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        if price_from:
            self.queryset = self.queryset.filter(
                price__gte=price_from
            )
        if price_to:
            self.queryset = self.queryset.filter(
                price__lte=price_to
            )

        return super().get(self, *args, **kwargs)



class AdCreateView(CreateAPIView):
    """Создание пользователя"""
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerAdOrStaff]


class AdUploadImageView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdImageSerializer


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerAdOrStaff]


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerSelection]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer
