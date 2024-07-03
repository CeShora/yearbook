from django import forms
from django.forms import inlineformset_factory
from .models import Student, Answer

class StudentRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email',
            'github_link', 'linkedin_link', 'phone', 'description', 'one_liner'
        ]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class StudentProfileForm(forms.ModelForm):
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
