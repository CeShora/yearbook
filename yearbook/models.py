from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, student_id, email, first_name, last_name, password=None, **extra_fields):
        if not student_id:
            raise ValueError('The Student ID must be set')
        if not email:
            raise ValueError('The Email must be set')
        
        email = self.normalize_email(email)
        user = self.model(student_id=student_id, email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(student_id, email, first_name, last_name, password, **extra_fields)



class Student(AbstractUser):
    username = None  # Remove the username field
    student_id = models.CharField(max_length=7, unique=True, validators=[MinLengthValidator(7)])
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    one_liner = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.student_id


class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name='answers')
    question_number = models.IntegerField()
    answer_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.answer_text}"


class Comment(models.Model):
    student = models.ForeignKey(Student, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.student}'

QUESTIONS = ["خنده دار ترین سوتیت چی بود؟",
"اگر به 4 سال پیش برگردی چه کاری رو انجام نمیدی؟\n و چه کاری رو انجام میدی؟",
"چه کاری توی این 4 سال کردی که بهش افتخار میکنی؟",
"انتظار داری 10 سال دیگه کجا باشی؟\n 20 سال دیگه چی؟",
"بهترین خاطره؟",
"آخرین حرفت با همدوره ای هات؟",
"توصیف این 4 سال با کلمات پراکنده؟",
"بچه های دورت در جند کلمه؟",
"دوست داری چه شغلی داشته باشی؟",
"فکر میکنی چه درسی رو اگر تو ارائه میدادی بهتر بود؟",
"دوست داشتی چه درسی رو پاس میکردی؟",
"دوست داشتی چه درسی رو پاس نمیکردی؟",
"باحال ترین استاد از نظرت کی بود؟",
"بهترین استاد از نظرت کی بود؟",
"رو مخ ترین پروژه از نظرت کی بود؟",
"پیچوندنی ترین کلاس از نظرت کدوم بود؟",
"اولین دوستت توی دانشگاه کی بود؟",
"بهترین دوستت توی این 4 سال کی بود؟",
"یعقوب یا یعقوب برقی؟",
"اولین چیزی که به ذهنت میاد وقتی میشنوی کورونا؟",
"اولین چیزی که به ذهنت میاد وقتی میشنوی پاتوق؟",
"روز اول دانشگاه؟",
"اولین چیزی که به ذهنت میاد وقتی میشنوی تی ای؟",
"اولین چیزی که به ذهنت میاد وقتی میشنوی سایت؟",
"اولین چیزی که به ذهنت میاد وقتی میشنوی پروژه؟",
"اولین چیزی که به ذهنت میاد وقتی میشنوی انتخاب واحد؟",
"اولین چیزی که به ذهنت میاد وقتی میشنوی طبقه ی اساتید؟",
]
