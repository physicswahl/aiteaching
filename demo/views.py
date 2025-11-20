from django.shortcuts import render
from django.http import JsonResponse
from .models import Student
import json

def start(request):
    return render(request, 'demo/start.html')

def challenge(request):
    return render(request, 'demo/challenge.html')

def transition(request):
    return render(request, 'demo/transition.html')

def ocr_image(request):
    return render(request, 'demo/ocr_image.html')

def word_vectors(request):
    return render(request, 'demo/word_vectors.html')

def two_nodes(request):
    # Get all students
    students = list(Student.objects.all().values('name', 'math_performance', 'reading_writing_performance', 'eligible_for_support'))
    students_json = json.dumps(students)
    return render(request, 'demo/two_nodes.html', {'students_json': students_json})

def two_nodes_video(request):
    # Get all students
    students = list(Student.objects.all().values('name', 'math_performance', 'reading_writing_performance', 'eligible_for_support'))
    students_json = json.dumps(students)
    return render(request, 'demo/two_nodes_video.html', {'students_json': students_json})

def video_explanation(request):
    return render(request, 'demo/video_explanation.html')

def conclusions_one(request):
    return render(request, 'demo/conclusions_one.html')

def conclusions_two(request):
    return render(request, 'demo/conclusions_two.html')

def teaching(request):
    return render(request, 'demo/teaching.html')

def llm(request):
    return render(request, 'demo/llm.html')

def anthropic(request):
    return render(request, 'demo/anthropic.html')

def five_nodes(request):
    # Get all students
    students = list(Student.objects.all().values('name', 'math_performance', 'reading_writing_performance', 'eligible_for_support'))
    students_json = json.dumps(students)
    return render(request, 'demo/five_nodes.html', {'students_json': students_json})

def student_plot(request):
    import math
    
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))
    
    def neural_network(x1, x2):
        """Same neural network as in populate_students"""
        w11 = 2.0
        w21 = 2.0
        w12 = 5.0
        w22 = -2.0
        b1 = -15.7
        b2 = -0.3
        wo1 = 3.0
        wo2 = 2.4
        bo = -2.9
        
        h1 = sigmoid(w11 * x1 + w21 * x2 + b1)
        h2 = sigmoid(w12 * x1 + w22 * x2 + b2)
        
        z = wo1 * h1 + wo2 * h2 + bo
        y = sigmoid(z)
        
        return y <= 0.5
    
    # Get all students and check if they're misclassified
    students = list(Student.objects.all().values('name', 'math_performance', 'reading_writing_performance', 'eligible_for_support'))
    
    for student in students:
        predicted = neural_network(student['math_performance'], student['reading_writing_performance'])
        student['misclassified'] = (predicted != student['eligible_for_support'])
    
    students_json = json.dumps(students)
    return render(request, 'demo/student_plot.html', {'students_json': students_json})
