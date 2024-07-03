from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import QUESTIONS, Answer, Student
from .forms import StudentProfileForm, AnswerFormSet, get_dynamic_answer_forms
from .forms import StudentRegistrationForm

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
    DynamicAnswerForm = get_dynamic_answer_forms()
    if request.method == 'POST':
        student_form = StudentRegistrationForm(request.POST)
        answer_form = DynamicAnswerForm(request.POST)
        if student_form.is_valid() and answer_form.is_valid():
            student = student_form.save()
            for i, question in enumerate(QUESTIONS):
                answer_text = answer_form.cleaned_data.get(f'question_{i}')
                if answer_text:
                    Answer.objects.create(
                        student=student,
                        question_number=i,
                        answer_text=answer_text
                    )
            return redirect('student_list')
    else:
        student_form = StudentRegistrationForm()
        answer_form = DynamicAnswerForm()
    
    return render(request, 'yearbook/student_create.html', {
        'student_form': student_form,
        'answer_form': answer_form,
    })



@login_required
def student_update(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student_form = StudentProfileForm(request.POST, instance=student)
        answer_formset = AnswerFormSet(request.POST, instance=student)
        if student_form.is_valid() and answer_formset.is_valid():
            student_form.save()
            answer_formset.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_detail', student_id=student.student_id)
    else:
        student_form = StudentProfileForm(instance=student)
        answer_formset = AnswerFormSet(instance=student)
    return render(request, 'yearbook/student_form.html', {
        'student_form': student_form,
        'answer_formset': answer_formset,
    })

@login_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'yearbook/student_confirm_delete.html', {'student': student})
