from django.contrib import admin
from .models import User, JobSeeker, JobSeekerAddress, JobSeekerEducation, JobSeekerWorkExperience, Hirer, HirerAddress, HirerPost, JobApplication, JobSeekerSocialMedia, HirerSocialMedia, Notification

class UserAdmin(admin.ModelAdmin):
    list_display=('username', 'is_superuser', 'is_jobseeker', 'is_hirer', 'name', 'email', 'phone_number')
admin.site.register(User, UserAdmin)


class JobSeekerAdmin(admin.ModelAdmin):
    list_display=('user', 'profile_image', 'skills', 'about', 'resume')
admin.site.register(JobSeeker, JobSeekerAdmin)


admin.site.register(JobSeekerAddress)

admin.site.register(JobSeekerEducation)
admin.site.register(JobSeekerWorkExperience)
admin.site.register(JobSeekerSocialMedia)

class HirerAdmin(admin.ModelAdmin):
    list_display=('user', 'profile_image', 'company_name', 'about_company')
admin.site.register(Hirer, HirerAdmin)


admin.site.register(HirerAddress)
admin.site.register(HirerSocialMedia)
admin.site.register(HirerPost)
admin.site.register(JobApplication)
admin.site.register(Notification)




