from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import JobSeekerSignUpForm, HirerSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from App.models import Hirer, JobSeeker, JobSeekerAddress, JobSeekerEducation, JobSeekerWorkExperience, JobApplication, JobSeekerSocialMedia, HirerAddress, HirerPost, HirerSocialMedia
from django.contrib.auth.decorators import login_required


def register(request):
    return render(request, 'register.html')


class job_seeker_register(CreateView):
    model = User
    form_class = JobSeekerSignUpForm
    template_name = 'jobseekerRegister.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('../login')


class hirer_register(CreateView):
    model = User
    form_class = HirerSignUpForm
    template_name = 'hirerRegister.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('../login')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html', context={'form': AuthenticationForm()})


@login_required(login_url='../login')
def logout_view(request):
    logout(request)
    return redirect('../login/')


@login_required(login_url='../login')
def profile(request):

    if request.user.is_jobseeker:
        user_job_seeker = JobSeeker.objects.get(user=request.user)
        user_job_seeker_address = JobSeekerAddress.objects.filter(
            jobSeeker=user_job_seeker).first()
        user_job_seeker_education = JobSeekerEducation.objects.filter(
            jobSeeker=user_job_seeker).all()
        user_job_seeker_experience = JobSeekerWorkExperience.objects.filter(
            jobSeeker=user_job_seeker).all()
        user_job_seeker_social_media = JobSeekerSocialMedia.objects.filter(
            jobSeeker=user_job_seeker).first()

        user_job_seeker_first_education = JobSeekerEducation.objects.filter(
            jobSeeker=user_job_seeker).first()
        user_job_seeker_first_experience = JobSeekerWorkExperience.objects.filter(
            jobSeeker=user_job_seeker).first()

        completeness_percentage_user_job_seeker = user_job_seeker.calculate_jobseeker_completeness()
        if user_job_seeker_address:
            completeness_percentage_user_job_seeker_address = user_job_seeker_address.calculate_jobseekeraddress_completeness()
        else:
            completeness_percentage_user_job_seeker_address = 0

        if user_job_seeker_first_education:
            completeness_percentage_user_job_seeker_first_education = user_job_seeker_first_education.calculate_jobseekereducation_completeness()
        else:
            completeness_percentage_user_job_seeker_first_education = 0
        
        if user_job_seeker_first_experience:
            completeness_percentage_user_job_seeker_first_experience = user_job_seeker_first_experience.calculate_jobseekerworkexperience_completeness()
        else:
            completeness_percentage_user_job_seeker_first_experience = 0
        
        percentage_user = (completeness_percentage_user_job_seeker + completeness_percentage_user_job_seeker_address +
                           completeness_percentage_user_job_seeker_first_education + completeness_percentage_user_job_seeker_first_experience) / 4
        
        percentage_user = round(percentage_user, 2)

        context = {
            'skills': user_job_seeker.skills.split(','),
            'user_job_seeker': user_job_seeker,
            'user_job_seeker_address': user_job_seeker_address,
            'user_job_seeker_education': user_job_seeker_education,
            'user_job_seeker_experience': user_job_seeker_experience,
            'user_job_seeker_social_media': user_job_seeker_social_media,

            'percentage_user': percentage_user,
        }

        if request.method == 'POST':
            if 'form_img' in request.POST:
                profile_img = request.FILES['imageInput']

                user_job_seeker = JobSeeker.objects.get(user=request.user)

                user_job_seeker.profile_image = profile_img

                user_job_seeker.save()
                return redirect('../profile')

            elif 'form1_submit' in request.POST:
                username = request.POST['username']
                name = request.POST['name']
                email = request.POST['email']
                phone_number = request.POST['phone_number']
                date_of_birth = request.POST['date_of_birth']

                user_job_seeker = JobSeeker.objects.get(user=request.user)

                user_job_seeker.user.name = name
                user_job_seeker.user.email = email
                user_job_seeker.user.phone_number = phone_number
                user_job_seeker.date_of_birth = date_of_birth
                # user_job_seeker.about = about

                user_job_seeker.save()

                if User.objects.filter(username=username).exists() and username != request.user.username:
                    context = {
                        'user_job_seeker': user_job_seeker,
                        'error': "Username Already Exist"
                    }
                    # return render(request, 'newProfile.html', context)
                else:
                    user_job_seeker.user.username = username

                user_job_seeker.user.save()
                return redirect('../profile')

            elif 'form2_submit' in request.POST:
                about = request.POST['about']
                skills = request.POST['skills']

                user_job_seeker = JobSeeker.objects.get(user=request.user)

                if request.FILES:
                    resume = request.FILES['file']
                    user_job_seeker.resume = resume

                user_job_seeker.about = about
                user_job_seeker.skills = skills

                user_job_seeker.save()
                return redirect('../profile')

            elif 'form3_submit' in request.POST:
                street_address = request.POST['street_address']
                city = request.POST['city']
                state = request.POST['state']
                postal_code = request.POST['postal_code']
                country = request.POST['country']

                user_job_seeker_address, user_job_seeker_address_create = JobSeekerAddress.objects.get_or_create(
                    jobSeeker_id=request.user.id)

                user_job_seeker_address.street_address = street_address
                user_job_seeker_address.city = city
                user_job_seeker_address.state = state
                user_job_seeker_address.postal_code = postal_code
                user_job_seeker_address.country = country

                user_job_seeker_address.save()
                return redirect('../profile')

            elif 'form4_submit' in request.POST:
                school_name = request.POST['school_name']
                field_of_study = request.POST['field_of_study']
                degree = request.POST['degree']
                start_date = request.POST['start_date_edu']
                end_date = request.POST['end_date_edu']

                # user_job_seeker_education, user_job_seeker_education_create = JobSeekerEducation.objects.get_or_create(jobSeeker_id=request.user.id)
                user_job_seeker_education = JobSeekerEducation.objects.create(
                    jobSeeker_id=request.user.id)

                user_job_seeker_education.school_name = school_name
                user_job_seeker_education.field_of_study = field_of_study
                user_job_seeker_education.degree = degree
                user_job_seeker_education.start_date = start_date
                user_job_seeker_education.end_date = end_date

                user_job_seeker_education.save()
                return redirect('../profile')

            elif 'form5_submit' in request.POST:
                company_name = request.POST['company_name']
                position = request.POST['position']
                start_date = request.POST['start_date_exp']
                end_date = request.POST['end_date_exp']
                description = request.POST['description_exp']

                user_job_seeker_expreience = JobSeekerWorkExperience.objects.create(
                    jobSeeker_id=request.user.id)

                user_job_seeker_expreience.company_name = company_name
                user_job_seeker_expreience.position = position
                user_job_seeker_expreience.start_date = start_date
                user_job_seeker_expreience.end_date = end_date
                user_job_seeker_expreience.description = description

                user_job_seeker_expreience.save()
                return redirect('../profile')

            elif 'form6_submit' in request.POST:
                facebook_url = request.POST['facebook']
                linkedin_url = request.POST['linkedin']
                twitter_url = request.POST['twitter']

                user_job_seeker_social_media, user_job_seeker_social_media_create = JobSeekerSocialMedia.objects.get_or_create(
                    jobSeeker_id=request.user.id)

                user_job_seeker_social_media.facebook_url = facebook_url
                user_job_seeker_social_media.linkedin_url = linkedin_url
                user_job_seeker_social_media.twitter_url = twitter_url

                user_job_seeker_social_media.save()
                return redirect('../profile')
            else:
                pass

        return render(request, 'jobSeekerProfile.html', context)

    if request.user.is_hirer:
        user_hirer = Hirer.objects.get(user=request.user)
        user_hirer_address = HirerAddress.objects.filter(hirer=user_hirer).first()
        user_hirer_social_media = HirerSocialMedia.objects.filter(hirer=user_hirer).first()

        completeness_percentage_user_hirer = user_hirer.calculate_hirer_completeness()
        if user_hirer_address:
            completeness_percentage_user_hirer_address = user_hirer_address.calculate_hireraddress_completeness()
        else:
            completeness_percentage_user_hirer_address = 0

        percentage_user = (completeness_percentage_user_hirer +
                           completeness_percentage_user_hirer_address) / 2
        percentage_user = round(percentage_user, 2)

        context = {
            'user_hirer': user_hirer,
            'user_hirer_address': user_hirer_address,
            'user_hirer_social_media': user_hirer_social_media,

            'percentage_user': percentage_user,
        }

        if request.method == 'POST':
            if 'form1_submit' in request.POST:
                username = request.POST['username']
                name = request.POST['name']
                email = request.POST['email']
                phone_number = request.POST['phone_number']
                # company_name = request.POST['company_name']

                user_hirer = Hirer.objects.get(user=request.user)

                user_hirer.user.name = name
                user_hirer.user.email = email
                user_hirer.user.phone_number = phone_number
                # user_hirer.company_name = company_name
                # user_job_seeker.about = about

                user_hirer.save()

                if User.objects.filter(username=username).exists() and username != request.user.username:
                    context = {
                        'error': "Username Already Exist"
                    }
                    # return render(request, 'newProfile.html', context)
                else:
                    user_hirer.user.username = username

                user_hirer.user.save()
                return redirect('../profile')

            elif 'form2_submit' in request.POST:
                company_name = request.POST['company_name']
                about_company = request.POST['about_company']

                user_hirer = Hirer.objects.get(user=request.user)

                user_hirer.company_name = company_name
                user_hirer.about_company = about_company

                user_hirer.save()
                return redirect('../profile')

            elif 'form3_submit' in request.POST:
                street_address = request.POST['street_address']
                city = request.POST['city']
                state = request.POST['state']
                postal_code = request.POST['postal_code']
                country = request.POST['country']

                user_hirer_address, user_hirer_address_create = HirerAddress.objects.get_or_create(
                    hirer_id=request.user.id)

                user_hirer_address.street_address = street_address
                user_hirer_address.city = city
                user_hirer_address.state = state
                user_hirer_address.postal_code = postal_code
                user_hirer_address.country = country

                user_hirer_address.save()
                return redirect('../profile')

            elif 'form4_submit' in request.POST:
                facebook_url = request.POST['facebook']
                linkedin_url = request.POST['linkedin']
                twitter_url = request.POST['twitter']

                user_hirer_social_media, user_hirer_social_media_create = HirerSocialMedia.objects.get_or_create(
                    hirer_id=request.user.id)

                user_hirer_social_media.facebook_url = facebook_url
                user_hirer_social_media.linkedin_url = linkedin_url
                user_hirer_social_media.twitter_url = twitter_url

                user_hirer_social_media.save()
                return redirect('../profile')

            elif 'form_img' in request.POST:
                profile_img = request.FILES['imageInput']
                user_hirer = Hirer.objects.get(user=request.user)

                user_hirer.profile_image = profile_img
                user_hirer.save()
                return redirect('../profile')

            else:
                print("Error!")

        return render(request, 'hirerProfile.html', context)
