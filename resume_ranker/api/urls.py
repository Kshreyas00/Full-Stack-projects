# from django.urls import path
# from . import views

# urlpatterns = [
#     path('api/rank-resumes/', views.rank_resumes, name='rank_resumes'),
#     path('api/upload/', views.upload_resume, name='upload_resume'),  # Added this line for file upload
# ]
# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('rank-resumes/', views.rank_resumes, name='rank_resumes'),  # Remove the 'api/' from the path
    path('upload/', views.upload_resume, name='upload_resume'),  # Correct the upload path
]
