from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Answer, Tag

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'desc')
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(UserAdmin):
    model = Student
    list_display = ('student_id', 'email', 'first_name', 'last_name')
    search_fields = ('student_id', 'email', 'first_name', 'last_name')
    ordering = ('student_id',)  
    filter_horizontal = ('tags',)  # Allows a nice UI for many-to-many fields in the admin
    
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('student_id', 'email', 'first_name', 'last_name', 'github_link', 'linkedin_link', 'phone', 'description', 'one_liner')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Tags', {'fields': ('tags',)}),  # Add this line to include the tags field
    )
    
    inlines = [AnswerInline]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student_id', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question_number', 'answer_text')
    search_fields = ('student__student_id', 'student__first_name', 'student__last_name', 'question_number')
    ordering = ('student__student_id',)
