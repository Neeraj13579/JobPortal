from nltk.tokenize import sent_tokenize
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from App.models import Hirer, JobSeeker, JobSeekerAddress, JobSeekerEducation, JobSeekerWorkExperience, HirerPost, HirerAddress, User, HirerSocialMedia, JobSeekerSocialMedia, JobApplication, Notification
from .models import ContactUs
from django.contrib.auth.decorators import login_required
from App.form import PostForm, ResponseChoice
from django.db.models import Count, Case, When, IntegerField
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from App.lists import LOCATION_CHOICES
from .recommendation import SkillsBasedRecommendation
from django.contrib.contenttypes.models import ContentType



from urllib.parse import urlparse
import nltk

# nltk.download('punkt')
# nltk.download('punkt', download_dir=False)



def landingPage(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = ContactUs.objects.create()

        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.message = message

        contact.save()

        context = {
            'success': "Thanks for contacting us! We will contact you shortly.",
        }
        return render(request, 'landingPage.html', context)

    return render(request, 'landingPage.html')


@login_required
def view_profile(request, username):
    user_profile = User.objects.get(username=username)

    if user_profile.is_jobseeker:
        user_job_seeker = JobSeeker.objects.get(user=user_profile)
        user_job_seeker_address = JobSeekerAddress.objects.filter(
            jobSeeker=user_job_seeker).first()
        user_job_seeker_education = JobSeekerEducation.objects.filter(
            jobSeeker=user_job_seeker).all()
        user_job_seeker_experience = JobSeekerWorkExperience.objects.filter(
            jobSeeker=user_job_seeker).all()
        
        context = {
            'user_job_seeker': user_job_seeker,
            'skills': user_job_seeker.skills.split(','),
            'user_job_seeker_address': user_job_seeker_address,
            'user_job_seeker_education': user_job_seeker_education,
            'user_job_seeker_experience': user_job_seeker_experience,
        }

        return render(request, 'viewJobSeekerProfile.html', context)

    if user_profile.is_hirer:
        user_hirer = Hirer.objects.get(user=user_profile)
        user_hirer_address = HirerAddress.objects.filter(
            hirer=user_hirer).first()

        context = {
            'user_hirer': user_hirer,
            'user_hirer_address': user_hirer_address,
        }

        return render(request, 'viewHirerProfile.html', context)


@login_required(login_url='../account/login')
def home(request):
    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')


    if request.user.is_jobseeker:
        user = User.objects.get(id=request.user.id)
        user_job_seeker = JobSeeker.objects.get(user=request.user)
        user_job_seeker_address = JobSeekerAddress.objects.filter(jobSeeker=user_job_seeker).first()
        job_applications = JobApplication.objects.filter(applicant=user_job_seeker)

        pending_response, received_response = 0, 0
        for job_application in job_applications:
            if job_application.response == 'None':
                pending_response += 1
            else:
                received_response += 1

        user_job_seeker_first_education = JobSeekerEducation.objects.filter(jobSeeker=user_job_seeker).first()
        user_job_seeker_first_experience = JobSeekerWorkExperience.objects.filter(jobSeeker=user_job_seeker).first()

        user_completeness_percentage = user.calculate_user_completeness()
        completeness_percentage_user_job_seeker = user_job_seeker.calculate_jobseeker_completeness()
        if user_job_seeker_address:
            completeness_percentage_user_job_seeker_address = user_job_seeker_address.calculate_jobseekeraddress_completeness()
        else:
            completeness_percentage_user_job_seeker_address = 0

        if user_job_seeker_first_education:
            completeness_percentage_user_job_seeker_first_education = user_job_seeker_first_education.calculate_jobseekereducation_completeness()
        else:
            completeness_percentage_user_job_seeker_first_education = 0

        percentage_user = (user_completeness_percentage + completeness_percentage_user_job_seeker + completeness_percentage_user_job_seeker_address +
                           completeness_percentage_user_job_seeker_first_education ) / 4
        
        user_profile = JobSeeker.objects.get(user=request.user) 
        recommended_jobs = ''
        if HirerPost.objects.all():
            content_based_recommendation = SkillsBasedRecommendation(HirerPost.objects.all())    
        
            recommended_jobs = content_based_recommendation.recommend_jobs(user_profile, 6)



        
        context = {
            'user_notifications': user_notifications,

            'job_applications': job_applications,

            'recommended_jobs': recommended_jobs,

            'user_job_seeker': user_job_seeker,
            'user_job_seeker_address': user_job_seeker_address,
            'user_job_seeker_first_education': user_job_seeker_first_education,

            'percentage_user': percentage_user,


            'received_response': received_response,
            'pending_response': pending_response,
        }

        return render(request, 'home.html', context)

    if request.user.is_hirer:
        user = User.objects.get(id=request.user.id)
        user_hirer = Hirer.objects.get(user=request.user)
        user_hirer_address = HirerAddress.objects.filter(hirer=user_hirer).first()
        user_hirer_posts = HirerPost.objects.filter(hirer_id=request.user.id).all()

        num_applications, pending_response = 0, 0
        for item in user_hirer_posts:
            try:
                job_application = JobApplication.objects.filter(job_post=item.id)
                for res in job_application:
                    num_applications += 1
                
                    if res.response == 'None':
                        pending_response += 1
            except JobApplication.DoesNotExist:
                print('JobApplication DoesNotExist')
            # except JobApplication.MultipleObjectsReturned:
            #     print('JobApplication MultipleObjectsReturned')

        
        user_completeness_percentage = user.calculate_user_completeness()
        completeness_percentage_user_hirer = user_hirer.calculate_hirer_completeness()
        if user_hirer_address:
            completeness_percentage_user_hirer_address = user_hirer_address.calculate_hireraddress_completeness()
        else:
            completeness_percentage_user_hirer_address = 0
        percentage_user = (user_completeness_percentage + completeness_percentage_user_hirer + completeness_percentage_user_hirer_address) / 3

        context = {
            'user_notifications': user_notifications,

            'user_hirer': user_hirer,
            'user_hirer_address': user_hirer_address,

            'pending_response': pending_response,

            'user_hirer_posts': user_hirer_posts,
            'num_applications': num_applications,

            'percentage_user': percentage_user,

            'pending_response': pending_response,
        }

        return render(request, 'home.html', context)


@login_required(login_url='../account/login')
def create_post(request):
    if request.user.is_jobseeker:
        return redirect('home')
    

    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')


    user = User.objects.get(id=request.user.id)
    user_hirer = Hirer.objects.get(user=request.user)
    user_hirer_address = HirerAddress.objects.filter(hirer=user_hirer).first()
    user_hirer_posts = HirerPost.objects.filter(hirer_id=request.user.id).all()

    num_applications, pending_response = 0, 0
    for item in user_hirer_posts:
        try:
            job_application = JobApplication.objects.filter(job_post=item.id)
            for res in job_application:
                num_applications += 1
            
                if res.response == 'None':
                    pending_response += 1
        except JobApplication.DoesNotExist:
            print('JobApplication DoesNotExist')
        # except JobApplication.MultipleObjectsReturned:
        #     print('JobApplication MultipleObjectsReturned')

    
    user_completeness_percentage = user.calculate_user_completeness()
    completeness_percentage_user_hirer = user_hirer.calculate_hirer_completeness()
    if user_hirer_address:
        completeness_percentage_user_hirer_address = user_hirer_address.calculate_hireraddress_completeness()
    else:
        completeness_percentage_user_hirer_address = 0
    percentage_user = (user_completeness_percentage + completeness_percentage_user_hirer + completeness_percentage_user_hirer_address) / 3

    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            hirer_post = form.save(commit=False)
            hirer_post.hirer = request.user.hirer
            hirer_post.save()
            return redirect('my-post')
    else:
        form = PostForm()

    context = {
        'percentage_user': percentage_user,

        'user_notifications': user_notifications,

        'form': form,
    }

    return render(request, 'createPost.html', context)


@login_required(login_url='../account/login')
def update_post(request, post_id):
    if request.user.is_jobseeker:
        return redirect('home')
    
    user = User.objects.get(id=request.user.id)
    user_hirer = Hirer.objects.get(user=request.user)
    user_hirer_address = HirerAddress.objects.filter(hirer=user_hirer).first()
    user_hirer_posts = HirerPost.objects.filter(hirer_id=request.user.id).all()

    user_completeness_percentage = user.calculate_user_completeness()
    completeness_percentage_user_hirer = user_hirer.calculate_hirer_completeness()
    if user_hirer_address:
        completeness_percentage_user_hirer_address = user_hirer_address.calculate_hireraddress_completeness()
    else:
        completeness_percentage_user_hirer_address = 0
    percentage_user = (user_completeness_percentage + completeness_percentage_user_hirer + completeness_percentage_user_hirer_address) / 3

    
    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')
    
    post = get_object_or_404(HirerPost, id=post_id)

    

    if request.user != post.hirer.user:
        return HttpResponseForbidden("You do not have permission to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my-post')
    else:
        form = PostForm(instance=post)

    context = {
        'percentage_user': percentage_user,
        'form': form,
        'user_notifications': user_notifications,
    }

    return render(request, 'createPost.html', context)


@login_required(login_url='../account/login')
def delete_post(request, post_id):
    if request.user.is_jobseeker:
        return redirect('home')

    post = get_object_or_404(HirerPost, id=post_id)

    if request.user == post.hirer.user:
        post.delete()
        return redirect('my-post')
    else:
        return HttpResponseForbidden("You do not have permission to delete this post.")


@login_required(login_url='../account/login')
def post_view(request, post_id):    
    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')

    post = get_object_or_404(HirerPost, id=post_id)

    if JobApplication.objects.filter(applicant=request.user.id, job_post=post_id).exists():
        has_applied = True
    else:
        has_applied = False


    job_application = 'None'
    user_job_seeker = 'None'
    user_job_seeker_application = 'None'
    if request.user.is_jobseeker:
        user_job_seeker_application = JobApplication.objects.filter(applicant=request.user.id, job_post=post_id)
        user_job_seeker = JobSeeker.objects.get(user=request.user)
    else:
        job_application = JobApplication.objects.filter(job_post_id=post_id)

        if request.method == 'POST':
            for item in job_application:
                key = 'myResponse-' + str(item.id)
                result = request.POST[key]
                application = JobApplication.objects.get(pk=item.id)
                application.response = result
                application.save()
                send_response_notification(application.applicant.user, application.job_post.hirer, application.job_post, application.response)
                # def send_response_notification(job_seeker, hirer, job_post, response_message):
                
            
            return redirect('view-post', post_id)


    user_hirer = Hirer.objects.get(user=post.hirer.user)
    companyAddress = HirerAddress.objects.filter(hirer=user_hirer).first()
    socialMedia = HirerSocialMedia.objects.filter(hirer=user_hirer).first()

    aboutData = user_hirer.about_company

    if not aboutData is None:
        if '.' in aboutData:
            aboutData = "<p>" + "<br>".join(aboutData.split("\n")) + "</p>"

    purpose = post.job_purpose
    highlight = post.job_highlights
    skills = post.skills_requirement.split(',')

    purposeDatas = sent_tokenize(purpose)

    highlightDatas = sent_tokenize(highlight)

    new_context = request.session.pop('new_context', {})

    message = new_context.get('message', None)

    context = {
        'user_notifications': user_notifications,

        'message': message,

        'post': post,

        'user_job_seeker': user_job_seeker,
        'user_job_seeker_application': user_job_seeker_application,

        'has_applied': has_applied,

        'job_application': job_application,

        'user_hirer': user_hirer,
        'company_address': companyAddress,
        'social_media': socialMedia,
        'aboutData': aboutData,

        'purposeDatas': purposeDatas,
        'highlightDatas': highlightDatas,
        'skills': skills,
    }

    return render(request, 'postView.html', context)


@login_required(login_url='../account/login')
def my_post(request):
    if request.user.is_jobseeker:
        return redirect('home')
    
    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')


    posts = HirerPost.objects.filter(hirer_id=request.user.id).all()
    
    if posts.exists() == False:
        posts = False

    context = {
        'user_notifications': user_notifications,

        'posts': posts,
    }

    return render(request, 'myPost.html', context)


@login_required(login_url='../account/login')
def find_job(request):
    if request.user.is_hirer:
        return redirect('home')
    
    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')

    posts = HirerPost.objects.all()
    user_job_seeker = JobSeeker.objects.get(user=request.user)

    employee_types = (
        posts.values('employee_type')
        .annotate(count_emp=Count('employee_type'))
        .order_by('-count_emp')
    )

    experiences = (
        posts.values('experience')
        .annotate(count_exp=Count('experience'))
        .annotate(
            experience_order=Case(
                When(experience='None', then=0),
                When(experience='0-1 year', then=1),
                When(experience='1-2 years', then=2),
                When(experience='2-3 years', then=3),
                When(experience='3-4 years', then=4),
                When(experience='4-5 years', then=5),
                When(experience='5-10 years', then=6),
                When(experience='10-15 years', then=7),
                When(experience='15+ years', then=8),
                default=999,
                output_field=IntegerField(),
            )
        )
        .order_by('experience_order')
    )
    
    top_departments = (
        posts.values('department')
        .annotate(count_dept=Count('department'))
        .order_by('-count_dept')[:4]
    )
    remaining_departments = (
        posts.exclude(department__in=[dep['department'] for dep in top_departments])
        .values('department')
        .annotate(count_dept=Count('department'))
        .order_by('department')
    )


    top_locations = (
        posts.values('location')
        .annotate(count_loc=Count('location'))
        .order_by('-count_loc')[:4]
    )
    remaining_locations = (
        posts.exclude(location__in=[loc['location'] for loc in top_locations])
        .values('location')
        .annotate(count_loc=Count('location'))
        .order_by('location')
    )


    top_roles = (
        posts.values('role')
        .annotate(count_role=Count('role'))
        .order_by('-count_role')[:4]
    )
    remaining_roles = (
        posts.exclude(role__in=[role['role'] for role in top_roles])
        .values('role')
        .annotate(count_role=Count('role'))
        .order_by('role')
    )

    # selected_salary_ranges = request.GET.getlist('salary')

    salary_ranges = {
        'threeL': (0, 300000),
        'sixL': (300001, 600000),
        'tenL': (600001, 1000000),
        'fiviteenL': (1000001, 1500000),
        'fiviteenPlusL': (1500001, None),
    }
    salary_counts = {}

    for label, (min_salary, max_salary) in salary_ranges.items():
        # if label in selected_salary_ranges:
        if max_salary is None:
            count = HirerPost.objects.filter(salary__gte=min_salary).count()
        else:
            count = HirerPost.objects.filter(salary__gte=min_salary, salary__lte=max_salary).count()
        salary_counts[label] = count


    if request.method == "GET":
        is_filter = False


        selected_employee_types = request.GET.getlist('employee-type')
        
        employee_type_filter = {}
        filtered_employee_posts = ''
        if selected_employee_types:
            is_filter = 'run'
            employee_type_filter['employee_type__in'] = selected_employee_types

            filtered_employee_posts = HirerPost.objects.filter(**employee_type_filter)
            if filtered_employee_posts:
                is_filter = True

        selected_experiences = request.GET.getlist('experience')

        experience_filter = {}
        filtered_experience_posts = ''
        if selected_experiences:
            is_filter = 'run'
            experience_filter['experience__in'] = selected_experiences

            filtered_experience_posts = HirerPost.objects.filter(**experience_filter)
            if filtered_experience_posts:
                is_filter = True

        selected_departments = request.GET.getlist('department')

        department_filter = {}
        filtered_department_posts = ''
        if selected_departments:
            is_filter = 'run'
            department_filter['department__in'] = selected_departments

            filtered_department_posts = HirerPost.objects.filter(**department_filter)
            if filtered_department_posts:
                is_filter = True

        selected_locations = request.GET.getlist('location')
        # selected_locations = request.GET.getlist('locationInput')

        location_filter = {}
        filtered_location_posts = ''
        if selected_locations:
            is_filter = 'run'
            location_filter['location__in'] = selected_locations

            filtered_location_posts = HirerPost.objects.filter(**location_filter)
            if filtered_location_posts:
                is_filter = True

        selected_salary = request.GET.getlist('salary')

        filtered_salary_posts = ''
        if selected_salary:
            is_filter = 'run'
            selected_salary = [int(salary) for salary in selected_salary]

            salary_conditions = [Q(salary__gte=salary) for salary in selected_salary]

            combined_conditions = Q()

            for condition in salary_conditions:
                combined_conditions |= condition

            filtered_salary_posts = HirerPost.objects.filter(combined_conditions)
            if filtered_salary_posts:
                is_filter = True

        selected_role = request.GET.getlist('role')

        role_filter = {}
        filtered_role_posts = ''
        if selected_role:
            is_filter = 'run'
            role_filter['role__in'] = selected_role

            filtered_role_posts = HirerPost.objects.filter(**role_filter)
            if filtered_role_posts:
                is_filter = True

        freshness = ''
        filtered_freshiness_posts = ''
        if 'freshness' in request.GET:
            is_filter = 'run'
            freshness = request.GET['freshness']
            filtered_freshiness_posts = HirerPost.objects.all()

            try:
                freshness = int(freshness)
                if freshness > 0:
                    threshold_date = timezone.now() - timedelta(days=freshness)
                    filtered_freshiness_posts = filtered_freshiness_posts.filter(created_at__gte=threshold_date)
            except ValueError:
                pass
            if filtered_freshiness_posts:
                is_filter = True


        keywordInput = request.GET.get('keywordInput', '')

        searchResults = ''
        companyNameSearch = ''
        if keywordInput:
            is_filter = 'run'
            search_fields = ['title', 'salary', 'role', 'industry_type', 'department', 'employee_type', 'education', 'job_highlights', 'job_purpose', 'skills_requirement'] 

            # Create a Q object that combines multiple OR conditions for each field
            filter_conditions = Q()
            for field in search_fields:
                filter_conditions |= Q(**{f'{field}__icontains': keywordInput})


            searchResults = HirerPost.objects.filter(filter_conditions)


            companyName = Hirer.objects.filter(company_name__icontains=keywordInput)
            for result in companyName:
                companyNameSearch = HirerPost.objects.filter(hirer=result)
            if searchResults or companyNameSearch:
                is_filter = True
            # print(companyNameSearch)

        experienceInput = request.GET.get('experienceInput', '')

        searchExperienceResults = ''
        if experienceInput:
            is_filter = 'run'
            searchExperienceResults = HirerPost.objects.filter(experience=experienceInput)
            if searchExperienceResults:
                is_filter = True

        locationInput = request.GET.get('locationInput', '')
        
        searchLocationResults = ''
        if locationInput:
            is_filter = 'run'
            searchLocationResults = HirerPost.objects.filter(location__icontains=locationInput)
            if searchLocationResults:
                is_filter = True

    user_profile = JobSeeker.objects.get(user=request.user) 
    recommended_jobs = ''
    if HirerPost.objects.all():
        content_based_recommendation = SkillsBasedRecommendation(HirerPost.objects.all())    
        
        recommended_jobs = content_based_recommendation.recommend_jobs(user_profile, 3)

    context = {
        'user_notifications': user_notifications,

        'posts': posts,
        'user_job_seeker': user_job_seeker,

        'employee_types': employee_types,
        'experiences': experiences,
        
        'top_departments': top_departments,
        'top_locations': top_locations,
        'top_roles': top_roles,

        'remaining_departments': remaining_departments,
        'remaining_locations': remaining_locations,
        'remaining_roles': remaining_roles,

        'salary_counts': salary_counts,

        'is_filter': is_filter,

        'recommended_jobs': recommended_jobs,


        'keywordInput': keywordInput,
        'experienceInput': experienceInput,
        'locationInput': locationInput,

        'searchResults': searchResults,
        'companyNameSearch': companyNameSearch,

        'searchExperienceResults': searchExperienceResults,
        'searchLocationResults': searchLocationResults,

        'filtered_employee_posts': filtered_employee_posts,
        'filtered_experience_posts': filtered_experience_posts,
        'filtered_department_posts': filtered_department_posts,
        'filtered_location_posts': filtered_location_posts,
        'filtered_salary_posts': filtered_salary_posts,
        'filtered_role_posts': filtered_role_posts,
        'filtered_freshiness_posts': filtered_freshiness_posts,

        'selected_employee_types': selected_employee_types,
        'selected_experiences': selected_experiences,
        'selected_departments': selected_departments,
        'selected_locations': selected_locations,
        'selected_salary': selected_salary,
        'selected_role': selected_role,
        'freshness': freshness,
    }


    return render(request, 'findJob.html', context)



@login_required(login_url='../account/login')
def save_unsave_post(request, post_id):
    user_job_seeker = JobSeeker.objects.get(user=request.user)
    post = HirerPost.objects.get(pk=post_id)

    if user_job_seeker.saved_posts.filter(id=post_id).exists():
        user_job_seeker.saved_posts.remove(post)
        saved = False
    else:
        user_job_seeker.saved_posts.add(post)
        saved = True

    data = {'saved': saved}
    return JsonResponse(data)



@login_required(login_url='../account/login')
def view_saved_post(request):
    if request.user.is_hirer:
        return redirect('home')
    
    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')
    
    user_job_seeker = JobSeeker.objects.get(user=request.user)
    posts =  user_job_seeker.saved_posts.all()

    context = {
        'user_notifications': user_notifications,

        'posts': posts,
        'user_job_seeker': user_job_seeker,
    }

    return render(request, 'savedNappliedPosts.html', context)


@login_required(login_url='../account/login')
def apply_job(request, post_id):
    if request.user.is_hirer:
        return redirect('home')
    
    user = User.objects.get(id=request.user.id)
    user_job_seeker = JobSeeker.objects.get(user=request.user)
    user_job_seeker_address = JobSeekerAddress.objects.filter(jobSeeker=user_job_seeker).first()
    job_applications = JobApplication.objects.filter(applicant=user_job_seeker)

    pending_response, received_response = 0, 0
    for job_application in job_applications:
        if job_application.response == 'None':
            pending_response += 1
        else:
            received_response += 1

    user_job_seeker_first_education = JobSeekerEducation.objects.filter(jobSeeker=user_job_seeker).first()
    user_job_seeker_first_experience = JobSeekerWorkExperience.objects.filter(jobSeeker=user_job_seeker).first()

    user_completeness_percentage = user.calculate_user_completeness()
    completeness_percentage_user_job_seeker = user_job_seeker.calculate_jobseeker_completeness()
    if user_job_seeker_address:
        completeness_percentage_user_job_seeker_address = user_job_seeker_address.calculate_jobseekeraddress_completeness()
    else:
        completeness_percentage_user_job_seeker_address = 0

    if user_job_seeker_first_education:
        completeness_percentage_user_job_seeker_first_education = user_job_seeker_first_education.calculate_jobseekereducation_completeness()
    else:
        completeness_percentage_user_job_seeker_first_education = 0

    percentage_user = (user_completeness_percentage + completeness_percentage_user_job_seeker + completeness_percentage_user_job_seeker_address +
                        completeness_percentage_user_job_seeker_first_education ) / 4
    
    if percentage_user != 100:
        new_context = {'message': 'You need to complete profile to 100% then only you can apply for jobs.'}

        # Save the context data to the session
        request.session['new_context'] = new_context

        # Redirect to the target view
        return redirect('view-post', post_id)

        # return render(request, 'postView.html', context)

    user_job_seeker = JobSeeker.objects.get(user=request.user)
    post = HirerPost.objects.get(id=post_id)
    
    jobApplication = JobApplication(applicant=user_job_seeker, job_post=post, resume=user_job_seeker.resume)
    jobApplication.save()

    send_application_notification(post.hirer.user, user_job_seeker.user, post)
    # def send_application_notification(hirer, job_seeker, job_post):


    previous_url = request.META.get('HTTP_REFERER', None)

    return redirect(previous_url)


@login_required(login_url='../account/login')
def applied_job(request):
    if request.user.is_hirer:
        return redirect('home')
    
    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')
    
    user_job_seeker = JobSeeker.objects.get(user=request.user)
    job_application = JobApplication.objects.filter(applicant=user_job_seeker).all()

    saved_post = user_job_seeker.saved_posts.all()

    context = {
        'user_notifications': user_notifications,

        'job_application': job_application,
        'saved_post': saved_post,
    }

    return render(request, 'savedNappliedPosts.html', context)

@login_required(login_url='../account/login')
def get_location_suggestions(request):
    locationInput = request.GET.get('locationInput', '')
    
    suggestions = [item for item in LOCATION_CHOICES if locationInput.lower() in item.lower()]
    return JsonResponse({'suggestions': suggestions})




def job_recommendations(request):
    user_content_type = ContentType.objects.get_for_model(request.user)

    user_notifications  = Notification.objects.filter(
        receiver_content_type=user_content_type,
        receiver_object_id=request.user.id,
        read = False
    ).order_by('-created_at')


    user_profile = JobSeeker.objects.get(user=request.user) 
    
    content_based_recommendation = SkillsBasedRecommendation(HirerPost.objects.all())    
    
    recommended_jobs = content_based_recommendation.recommend_jobs(user_profile, 9)
    
    context = {
        'user_notifications': user_notifications,

        'recommended_jobs': recommended_jobs    
    }
    
    return render(request, 'recommendation.html', context)




def send_application_notification(hirer, job_seeker, job_post):
    message = f"Job seeker {job_seeker.name} applied for your job: {job_post.title}"
    notification = Notification(sender=job_seeker, receiver=hirer, message=message, post=job_post)
    notification.save()

def send_response_notification(job_seeker, hirer, job_post, response_message):
    message = f"Hirer {hirer.company_name} responded to your application for the job '{job_post.title}': {response_message}"
    notification = Notification(sender=hirer, receiver=job_seeker, message=message, post=job_post)
    notification.save()

def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        print(notification)
        notification.read = True
        notification.save()
        print(notification.read)
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})

def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})