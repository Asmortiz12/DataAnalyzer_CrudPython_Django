import json
from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student  
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import BytesIO
import base64
from django.shortcuts import render

API_URL = 'http://localhost:5000/api-student-543c3/us-central1/app/api/students/'

def student_list(request):
    if request.method == 'POST':
        carrer_filter = request.POST.get('carrer', None)
        if carrer_filter:
            response = requests.get(API_URL)
            students = response.json()
            filtered_students = [student for student in students if student['carrer'] == carrer_filter]
            return render(request,'student_list.html', {'students': filtered_students, 'carrer_filter': carrer_filter})
    
    response = requests.get(API_URL)
    students = response.json()

    # Generar datos para los gráficos
    carrer_counts = {}
    for student in students:
        carrer = student['carrer']
        if carrer in carrer_counts:
            carrer_counts[carrer] += 1
        else:
            carrer_counts[carrer] = 1

    # Crear gráfico con Matplotlib
    plt.figure(figsize=(6, 4))
    plt.bar(carrer_counts.keys(), carrer_counts.values())
    plt.xlabel('Carrera')
    plt.ylabel('Cantidad de Estudiantes')
    buffer_matplotlib = BytesIO()
    plt.savefig(buffer_matplotlib, format='png')
    plt.close()
    plot_data_matplotlib = base64.b64encode(buffer_matplotlib.getvalue()).decode()

    # Crear gráfico con Seaborn
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 4))
    sns.barplot(x=list(carrer_counts.keys()), y=list(carrer_counts.values()))
    plt.xlabel('Carrera')
    plt.ylabel('Cantidad de Estudiantes')
    buffer_seaborn = BytesIO()
    plt.savefig(buffer_seaborn, format='png')
    plt.close()
    plot_data_seaborn = base64.b64encode(buffer_seaborn.getvalue()).decode()

    # Crear gráfico con Plotly
    fig = px.bar(x=list(carrer_counts.keys()), y=list(carrer_counts.values()), labels={'x': 'Carrera', 'y': 'Cantidad de Estudiantes'})
    plotly_html = fig.to_html(full_html=False)

    return render(request, 'student_list.html', {'students': students, 'plot_data_matplotlib': plot_data_matplotlib, 'plot_data_seaborn': plot_data_seaborn, 'plotly_html': plotly_html})

def add_student(request):
    if request.method == 'POST':
        data = {
            'id': request.POST['id'],
            'names': request.POST['names'],
            'surnames': request.POST['surnames'],
            'carrer': request.POST['carrer'],
            'semester': request.POST['semester']
        }
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            return redirect('student_list')
    
    return render(request, 'add_student.html')

def edit_student(request, student_id):
    response = requests.get(f'{API_URL}{student_id}/')

    if response.status_code == 200:
        student = response.json()
    else:
        student = None

    if request.method == 'POST' and student is not None:
        data = {
            'names': request.POST['names'],
            'surnames': request.POST['surnames'],
            'carrer': request.POST['carrer'],
            'semester': request.POST['semester']
        }
        response = requests.put(f'{API_URL}{student_id}/', data=data)

        if response.status_code == 200:
            return redirect('student_list')
    
    return render(request, 'edit_student.html', {'student': student})

def delete_student(request, student_id):
    response = requests.delete(f'{API_URL}{student_id}/')
    if response.status_code == 204:
        return redirect('student_list')

    return redirect('student_list')
