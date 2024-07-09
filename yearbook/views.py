from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import QUESTIONS, Answer, Student
from .forms import CommentForm, StudentProfileForm, AnswerFormSet, get_dynamic_answer_forms
from .forms import StudentRegistrationForm
from django.contrib.auth.views import LoginView

#for messages:
from django.contrib import messages

def home(request):
    return render(request, "yearbook/home.html")

def about(request):
    return render(request, "yearbook/about.html")

def remembrancehall(request):
    students = Student.objects.filter(tags__isnull=False).distinct()
    return render(request, "yearbook/remembrancehall.html",{'students': students})

def reminiscencewall(request):
    answers = Answer.objects.filter(question_number=0)
    return render(request, "yearbook/reminiscencewall.html", {'answers': answers})


def student_list(request):
    students = Student.objects.all()
    return render(request, 'yearbook/student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    answers = student.answers.all()  
    comments = student.comments.all()
    questions = QUESTIONS

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.student = student
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('student_detail', student_id=student_id)
    else:
        comment_form = CommentForm()

    return render(request, 'yearbook/student_detail.html', {
        'student': student,
        'answers': answers,
        'comments': comments,
        'comment_form': comment_form,
        'questions': questions,
        'num_questions': len(questions),
    })


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
            # Authenticate the user
            student = authenticate(student_id=student.student_id, password=student_form.cleaned_data.get('password1'))
            if student is not None:
                login(request, student)
                messages.success(request, 'ثبت نام با موفقیت انجام شد و شما وارد شدید.')
                return redirect('student_list')
            else:
                messages.error(request, 'مشکلی در ورود به سیستم وجود دارد.')
                return redirect('login')  # Redirect to login page if authentication fails
    else:
        student_form = StudentRegistrationForm()
        answer_form = DynamicAnswerForm()
    
    return render(request, 'yearbook/student_create.html', {
        'student_form': student_form,
        'answer_form': answer_form,
    })


@login_required
def student_update(request):
    DynamicAnswerForm = get_dynamic_answer_forms()  
    student = request.user 

    answers = Answer.objects.filter(student=student)
    answer_dict = {answer.question_number: answer for answer in answers}

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'آپدیت شد')

        # Process answer forms for each question
        for i, question in enumerate(QUESTIONS):
            answer_text = request.POST.get(f'question_{i}')
            if answer_text:
                if i in answer_dict:
                    answer = answer_dict[i]
                    answer.answer_text = answer_text
                    answer.save()
                else:
                    Answer.objects.create(
                        student=student,
                        question_number=i,
                        answer_text=answer_text
                    )

        return redirect('student_list')  
    else:
        # Initialize profile form and answer forms
        form = StudentProfileForm(instance=student)
        initial_answers = {f'question_{i}': answer_dict[i].answer_text if i in answer_dict else '' for i, _ in enumerate(QUESTIONS)}
        answer_form = DynamicAnswerForm(initial=initial_answers)

    return render(request, 'yearbook/student_update.html', {
        'form': form,
        'answer_form': answer_form,
    })

@login_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'yearbook/student_confirm_delete.html', {'student': student})

class StudentLoginView(LoginView):
    template_name = 'yearbook/login.html'


class PostCommentView(LoginRequiredMixin, View):
    def post(self, request, student_id):
        student = get_object_or_404(Student, student_id=student_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.student = student
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted.')
        return redirect('student_detail', student_id=student_id)