from django.urls import path
from . import views

app_name = 'demo'

urlpatterns = [
    path('start/', views.start, name='start'),
    path('challenge/', views.challenge, name='challenge'),
    path('transition/', views.transition, name='transition'),
    path('ocr-image/', views.ocr_image, name='ocr_image'),
    path('word-vectors/', views.word_vectors, name='word_vectors'),
    path('two-nodes/', views.two_nodes, name='two_nodes'),
    path('two-nodes-video/', views.two_nodes_video, name='two_nodes_video'),
    path('video-explanation/', views.video_explanation, name='video_explanation'),
    path('conclusions-one/', views.conclusions_one, name='conclusions_one'),
    path('conclusions-two/', views.conclusions_two, name='conclusions_two'),
    path('teaching/', views.teaching, name='teaching'),
    path('llm/', views.llm, name='llm'),
    path('anthropic/', views.anthropic, name='anthropic'),
    path('five-nodes/', views.five_nodes, name='five_nodes'),
    path('student-plot/', views.student_plot, name='student_plot'),
]
