from django.urls import path
from . import views

app_name = "history"

urlpatterns = [
    path("", views.HistoryListView.as_view(), name="list"),
    path("<int:pk>/", views.HistoryDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.HistoryUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.history_delete, name="delete"),
    path("<int:pk>/archive/", views.history_archive, name="archive"),
    path("<int:pk>/export/", views.export_report, name="export"),
]
