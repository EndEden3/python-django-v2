from django.db import models
from django.contrib.auth import get_user_model
from common import models as common_models
# Create your models here.
User = get_user_model()

class CVManager(models.Model):
    STATUS_STATE_CHOICES = (
        ('new', 'New'),
        ('header', 'Header'),
        ('experience', 'Experience'),
        ('education', 'Education'),
        ('skills', 'Skills'),
        ('final', 'Final'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    state = models.CharField('Status type', default='new', max_length=300, choices=STATUS_STATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    name = models.CharField(max_length=100, default='', blank=True)
    template_name = models.ForeignKey(common_models.TemplatesName, related_name='templates_cv', null=True, on_delete=models.SET_NULL)

class CVManagerHeader(models.Model):
    cv_manager = models.ForeignKey(CVManager, related_name='header', on_delete=models.CASCADE)
    nume = models.CharField(max_length=100, default='')
    prenume = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20, default='')
    photo = models.ImageField(upload_to='user_photo', default=None)
    city = models.CharField(max_length=500, default='')
    country = models.CharField(max_length=100, default='')
    postcode = models.CharField(max_length=10, default='')
    specialty = models.CharField(max_length=100, default='')
    profile_details = models.TextField(default='')

class CVManagerExperience(models.Model):
    cv_manager = models.ForeignKey(CVManager, related_name='experience', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    details = models.TextField()
    order = models.PositiveIntegerField(default=0)

class CVManagerEducation(models.Model):
    cv_manager = models.ForeignKey(CVManager, related_name='education', on_delete=models.CASCADE)
    city = models.CharField(max_length=100, default='')
    details = models.TextField(default='')
    name = models.CharField(max_length=100, default='')
    order = models.PositiveIntegerField(default=0)

class CVManagerSkill(models.Model):
    cv_manager = models.ForeignKey(CVManager, related_name='skills', on_delete=models.CASCADE)
    skill = models.CharField(max_length=100, default='')
    point = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    def get_width(self):
        return int(self.point * 100)/5