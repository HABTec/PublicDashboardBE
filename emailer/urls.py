from django.urls import path
from .views import FormSubmissionView

urlpatterns = [
    path('submit-form/', FormSubmissionView.as_view(), name='submit-form'),
]
