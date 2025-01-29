from django.db import models
from django.contrib.auth.models import AbstractUser
from .lists import EXPERIENCE_CHOICES, LOCATION_CHOICES, ROLE_CHOICES, DEPARTMENT_CHOICES, EMPLOYEE_CHOICES, APPLICATION_RESPONSE_CHOICES
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from uuid import uuid4



class User(AbstractUser):
    is_jobseeker = models.BooleanField(default=False)
    is_hirer = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)
    phone_number = models.CharField(max_length=20, null=False)

    def calculate_user_completeness(self):
        required_fields = ['name', 'email', 'phone_number',]

        completed_fields = 0

        # checked
        if self.name and self.email and self.phone_number:
            completed_fields = 3

        total_fields = len(required_fields)

        return (completed_fields / total_fields) * 100


class Hirer(models.Model):
    id = models.UUIDField(default=uuid4, editable=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/defaultProfileImage.png', blank=True, null=True)

    company_name = models.CharField(max_length=100, null=True)

    about_company = models.TextField(null=True, blank=True)

    def calculate_hirer_completeness(self):
        required_fields = ['profile_image', 'company_name', 'about_company']

        total_fields = len(required_fields)

        completed_fields = 0

        if self.company_name == 'None' or not self.company_name:
            pass
        else:
            completed_fields += 1

        if self.about_company == 'None' or not self.about_company:
            pass
        else:
            completed_fields += 1

        if not self.profile_image.name == 'profile_images/defaultProfileImage.png':
            completed_fields += 1

        return (completed_fields / total_fields) * 100

    def __str__(self):
        return self.user.username


class HirerAddress(models.Model):
    hirer = models.ForeignKey(Hirer, on_delete=models.CASCADE)

    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def calculate_hireraddress_completeness(self):
        # Define the fields that are required for a complete profile
        required_fields = ['street_address', 'city',
                           'state', 'postal_code', 'country']

        # Calculate the percentage of completed fields
        completed_fields = sum(
            1 for field in required_fields if self.field_is_complete(getattr(self, field)))
        total_fields = len(required_fields)

        # Calculate the percentage
        return (completed_fields / total_fields) * 100

    def field_is_complete(self, field_value):
        if field_value is None:
            return False
        if isinstance(field_value, str) and not field_value.strip():
            return False
        return True

    def __str__(self):
        return self.hirer.user.username


class HirerSocialMedia(models.Model):
    hirer = models.ForeignKey(Hirer, on_delete=models.CASCADE)

    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.hirer.user.username
    

class HirerPost(models.Model):
    hirer = models.ForeignKey(Hirer, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    experience = models.CharField(choices=[(choice, choice) for choice in EXPERIENCE_CHOICES], max_length=100)
    salary = models.DecimalField(max_digits=15, decimal_places=0, default='Not Disclosed')
    intake = models.DecimalField(max_digits=15, decimal_places=0, default='Not Disclosed')
    location = models.CharField(choices=[(choice, choice) for choice in LOCATION_CHOICES], max_length=100)
    role = models.CharField(choices=[(choice, choice) for choice in ROLE_CHOICES], max_length=100)
    industry_type = models.CharField(max_length=100)
    department = models.CharField(choices=[(choice, choice) for choice in DEPARTMENT_CHOICES], max_length=100)
    employee_type = models.CharField(choices=[(choice, choice) for choice in EMPLOYEE_CHOICES], max_length=100)
    education = models.TextField()
    job_highlights = models.TextField()
    job_purpose = models.TextField()
    skills_requirement = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class JobSeeker(models.Model):
    id = models.UUIDField(default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(blank=True, null=True)
    # About me
    about = models.TextField(blank=True, null=True)
    # skills
    skills = models.TextField(blank=True, null=True, default='None')
    # resume
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    # profile image
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/defaultProfileImage.png', blank=True, null=True)

    saved_posts = models.ManyToManyField(HirerPost, blank=True)

    def calculate_jobseeker_completeness(self):
        required_fields = ['about', 'date_of_birth',
                           'skills', 'profile_image', 'resume']

        completed_fields = 0

        # checked
        if self.resume:
            completed_fields += 1

        # checked
        if not self.profile_image.name == 'profile_images/defaultProfileImage.png':
            completed_fields += 1

        # checked
        if not self.skills == 'None':
            completed_fields += 1
        if not self.skills:
            completed_fields -= 1

        # checked
        if not self.date_of_birth == None:
            completed_fields += 1

        # checked
        if not self.about == 'None':
            completed_fields += 1
        if not self.about:
            completed_fields -= 1

        total_fields = len(required_fields)

        return (completed_fields / total_fields) * 100

    def __str__(self):
        return self.user.username


class JobSeekerSocialMedia(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.jobSeeker.user.username


class JobSeekerAddress(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def calculate_jobseekeraddress_completeness(self):
        # Define the fields that are required for a complete profile
        required_fields = ['street_address', 'city',
                           'state', 'postal_code', 'country']

        # Calculate the percentage of completed fields
        completed_fields = sum(
            1 for field in required_fields if self.field_is_complete(getattr(self, field)))
        total_fields = len(required_fields)

        # Calculate the percentage
        return (completed_fields / total_fields) * 100

    def field_is_complete(self, field_value):
        if field_value is None:
            return False
        if isinstance(field_value, str) and not field_value.strip():
            return False
        return True

    def __str__(self):
        return self.jobSeeker.user.username


class JobSeekerEducation(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

    school_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100, null=True)
    field_of_study = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def calculate_jobseekereducation_completeness(self):
        # Define the fields that are required for a complete profile
        required_fields = ['school_name', 'degree', 'field_of_study', 'start_date', 'end_date']

        # Calculate the percentage of completed fields
        completed_fields = sum(1 for field in required_fields if self.field_is_complete(getattr(self, field)))
        total_fields = len(required_fields)

        # Calculate the percentage
        return (completed_fields / total_fields) * 100

    def field_is_complete(self, field_value):
        if field_value is None:
            return False
        if isinstance(field_value, str) and not field_value.strip():
            return False
        return True

    def __str__(self):
        return self.jobSeeker.user.username


class JobSeekerWorkExperience(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.TextField()

    def calculate_jobseekerworkexperience_completeness(self):
        # Define the fields that are required for a complete profile
        required_fields = ['company_name', 'position', 'start_date', 'end_date', 'description']

        # Calculate the percentage of completed fields
        completed_fields = sum(1 for field in required_fields if self.field_is_complete(getattr(self, field)))
        total_fields = len(required_fields)

        # Calculate the percentage
        return (completed_fields / total_fields) * 100

    def field_is_complete(self, field_value):
        if field_value is None:
            return False
        if isinstance(field_value, str) and not field_value.strip():
            return False
        return True

    def __str__(self):
        return self.jobSeeker.user.username





class JobApplication(models.Model):
    job_post = models.ForeignKey(HirerPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    applied_date = models.DateTimeField(auto_now_add=True)
    response = models.CharField(choices=[(choice, choice) for choice in APPLICATION_RESPONSE_CHOICES], max_length=100, null=True, blank=True, default='None')



    
class Notification(models.Model):
    sender_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='sender_notifications')
    sender_object_id = models.PositiveIntegerField()
    sender = GenericForeignKey('sender_content_type', 'sender_object_id')

    receiver_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='receiver_notifications')
    receiver_object_id = models.PositiveIntegerField()
    receiver = GenericForeignKey('receiver_content_type', 'receiver_object_id')

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    post = models.ForeignKey(HirerPost, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.message