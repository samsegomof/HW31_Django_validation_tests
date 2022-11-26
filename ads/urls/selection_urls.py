from django.urls import path
from ads.views import SelectionCreateView, SelectionListView, SelectionDetailView, SelectionDeleteView, SelectionUpdateView


urlpatterns = [
    path('', SelectionListView.as_view(), name='all_selections'),
    path('create/', SelectionCreateView.as_view(), name='create_selection'),
    path('<int:pk>/', SelectionDetailView.as_view(), name='detail_selection'),
    path('<int:pk>/update/', SelectionUpdateView.as_view(), name='update_selection'),
    path('<int:pk>/delete/', SelectionDeleteView.as_view(), name='delete_selection'),
]