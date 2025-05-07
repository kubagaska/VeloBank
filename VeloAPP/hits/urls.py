from django.urls import path
from .views import HitListView, HitDetailView, HitCreateView, HitUpdateView, HitDeleteView

urlpatterns = [
    path('api/v1/hits', HitListView.as_view(), name='hit-list'),
    path('api/v1/hits/<slug:title_url>', HitDetailView.as_view(), name='hit-detail'),
    path('api/v1/hits', HitCreateView.as_view(), name='hit-create'),
    path('api/v1/hits/<slug:title_url>', HitUpdateView.as_view(), name='hit-update'),
    path('api/v1/hits/<slug:title_url>', HitDeleteView.as_view(), name='hit-delete'),
]
