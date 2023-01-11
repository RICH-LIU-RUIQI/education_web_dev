from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from django.shortcuts import render_to_response
from django.http import JsonResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.organizations.models import CourseOrg
from apps.organizations.models import CityDict
from apps.organizations.forms import AddAskForm
from apps.operations.models import UserFavorite
from mx_online.settings import MEDIA_URL


class OrgHomeView(View):
    def get(self, request, org_id): # org_id will pass to url
        current_page = 'org_home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_favored = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_favored = True
        # show course, teacher, and description of selected org
        all_courses = course_org.get_all_courses(num=3)
        all_teacher = course_org.get_all_teachers(num=1)

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,  # course class
            'all_teachers': all_teacher,  # teacher class
            'course_org': course_org,  # organization class
            'current_page': current_page,  # page type
            'has_favored': has_favored,  # if favored
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'org_teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_favored = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_favored = True
        all_teacher = course_org.get_all_teachers()  # obtain all teachers in one org
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teacher,  # teacher class
            'course_org': course_org,  # organization class
            'current_page': current_page,
            'has_favored': has_favored,  # if favored
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'org_desc '
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_favored = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_favored = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,  # organization class
            'current_page': current_page,
            'has_favored': has_favored,  # if favored
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'org_course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_course = course_org.get_all_courses()  # obtain all courses in one org
        has_favored = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_favored = True

        # pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_course, per_page=5, request=request)
        courses = p.page(page)

        return render(request, 'org-detail-course.html', {
            'all_course': courses,  # teacher class
            'course_org': course_org,   # organization class
            'current_page': current_page,
            'has_favored': has_favored,  # if favored
        })


class AddAskView(View):
    def post(self, request):
        user_ask_form = AddAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': 'invalid input'
            })


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_cities = CityDict.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # filter organization
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        # filter organization district/city
        city_id = request.GET.get('city', '')
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))
        # sort orgs
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')  # - means descending
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        orgs_num = all_orgs.count()
        # pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {'all_orgs': orgs,
                                                 'orgs_num': orgs_num,
                                                 'all_cities': all_cities,
                                                 'category': category,
                                                 'city_id': city_id,
                                                 'sort': sort,
                                                 'hot_orgs': hot_orgs})

