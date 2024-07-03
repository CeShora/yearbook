from django import forms
from django.forms import inlineformset_factory
from .models import Student, Answer

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email',
            'github_link', 'linkedin_link', 'phone', 'description', 'one_liner'
        ]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question_number', 'answer_text']

AnswerFormSet = inlineformset_factory(Student, Answer, form=AnswerForm, extra=1)
