from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator, PageNotAnInteger


from apps.courses.models import Course, CourseOrg, CourseResource, Teacher, CourseTag
from apps.operations.models import UserFavorite, UserCourse
from mx_online.settings import MEDIA_URL


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id):
        """
        detail of course and lesson
        """
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()
        # CONNECT course with user
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        # create new connectiong
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        # load course resource
        course_resource = CourseResource.objects.filter(parent_course=course)
        return render(request, 'course-video.html',
                      {'course': course,
                       'course_resource': course_resource,
                       })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()
        # favor
        has_favored_course = False
        has_favored_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_favored_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org_id, fav_type=2):
                has_favored_org = True

        # recommendation by tag
        tag_list = course.get_all_tags()
        related_courses_tag = CourseTag.objects.filter(tag__in=tag_list).exclude(tar_course__name=course.name)
        # related_courses = [course_tag.tar_course for course_tag in related_courses_tag]
        related_courses = set(course_tag.tar_course for course_tag in related_courses_tag)

        return render(request, 'course-detail.html', {
            'course': course,
            'course_favor': has_favored_course,
            'org_favor': has_favored_org,
            'related_courses': related_courses,
        })


class CourseListView(View):
    def get(self, request):  # org_id will pass to url

        # order by release time/ fav number / joined number
        sort = request.GET.get('sort', '')  # cuz sort is in url
        if sort == 'student':
            all_courses = Course.objects.order_by('-students')
        elif sort == 'hot':
            all_courses = Course.objects.order_by('-click_num')
        else:
            all_courses = Course.objects.order_by('-add_time')

        # get the first three hottest courses
        hot_courses = Course.objects.order_by('-click_num')[:3]


        # pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, per_page=2, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


