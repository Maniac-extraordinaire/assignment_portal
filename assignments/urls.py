from django.urls import path
from .views import RegisterView, LoginView, UploadAssignmentView, AdminListView, AdminAssignmentsView, UpdateAssignmentStatusView


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('upload', UploadAssignmentView.as_view()),
    path('admins', AdminListView.as_view()),
    path('assignments', AdminAssignmentsView.as_view()),
    path('assignments/<str:id>/accept', UpdateAssignmentStatusView.as_view()),
    path('assignments/<str:id>/reject', UpdateAssignmentStatusView.as_view()),
]