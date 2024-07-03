from django.shortcuts import render, get_object_or_404, redirect
from .models import QUESTIONS, Student
from .forms import StudentForm, AnswerFormSet

def home(request):
    return render(request, "yearbook/home.html")

def student_list(request):
    students = Student.objects.all()
    return render(request, 'yearbook/student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    answers = student.answers.all()  # Fetch all related answers for the student
    return render(request, 'yearbook/student_detail.html', {'student': student, 'answers': answers, 'questions': QUESTIONS})

def student_create(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)
        if student_form.is_valid() and answer_formset.is_valid():
            student = student_form.save()
            answers = answer_formset.save(commit=False)
            for answer in answers:
                answer.student = student
                answer.save()
            return redirect('student_list')  # Redirect to student list upon successful form submission
    else:
        student_form = StudentForm()
        answer_formset = AnswerFormSet()
    return render(request, 'yearbook/student_form.html', {
        'student_form': student_form,
        'answer_formset': answer_formset,
    })

def student_update(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student_form = StudentForm(request.POST, instance=student)
        answer_formset = AnswerFormSet(request.POST, instance=student)
        if student_form.is_valid() and answer_formset.is_valid():
            student_form.save()
            answer_formset.save()
            return redirect('student_detail', student_id=student.student_id)
    else:
        student_form = StudentForm(instance=student)
        answer_formset = AnswerFormSet(instance=student)
    return render(request, 'yearbook/student_form.html', {
        'student_form': student_form,
        'answer_formset': answer_formset,
    })

def student_delete(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'yearbook/student_confirm_delete.html', {'student': student})