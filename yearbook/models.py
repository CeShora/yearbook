from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
        return f"Question: {QUESTIONS[self.question_number]}, Answer: {self.answer_text}, Student: {self.student}"


QUESTIONS = ["خنده دار ترین سوتیت چی بود؟",
"اگر به 4 سال پیش برگردی چه کاری رو انجام نمیدی؟ و چه کاری رو انجام میدی؟",
"چه کاری توی این 4 سال کردی که بهش افتخار میکنی؟",
"انتظار داری 10 سال دیگه کجا باشی؟ 20 سال دیگه چی؟",
"بهترین خاطره؟",
"آخرین حرفت با همدوره ای هات؟",
"توصیف این 4 سال با کلمات پراکنده؟",
"بجه های 98 در جند کلمه؟",
"دوست داری چه شغلی داشته باشی؟",
"فکر میکنی چه درسی رو اگر تو ارایه میدادی بهتر بود؟",
"دوست داشتی چه درسی رو پاس میکردی؟",
"دوست داشتی چه درسی رو پاس نمیکردی؟",
"باحال ترین استاد؟",
"بهترین استاد؟",
"رو مخ ترین پروژه؟",
"پیچوندنی ترین کلاس؟",
"اولین دوستت توی دانشگاه؟",
"بهترین دوستت توی این 4 سال؟",
"یعقوب یا یعقوب برقی؟",
"کورونا؟",
"پاتوق؟",
"روز اول دانشگاه؟",
"TA؟",
"سایت؟",
"پروژه؟",
"نتخاب واحد؟",
"طبقه ی اساتید؟",
]
