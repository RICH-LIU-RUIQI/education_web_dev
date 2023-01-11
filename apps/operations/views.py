from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse

from apps.operations.models import UserFavorite
from apps.operations.forms import AddFavorForm
from apps.courses.models import Course, Teacher
from apps.organizations.models import CourseOrg


class AddFavorView(View):
    def post(self, request):
        """
        add/cancel favor
        :param request:
        :return: JsonResponse
        """
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': 'not login',
            })
        user_fav_form = AddFavorForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data['fav_id']
            fav_type = user_fav_form.cleaned_data['fav_type']
            # whether favored before
            exist_record = UserFavorite.objects.filter(user=request.user,
                                                       fav_id=fav_id, fav_type=fav_type)
            if exist_record:
                # cancel favor
                exist_record.delete()
                # course
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_num -= 1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums -= 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '收藏',
                })
            else:
                user_favor = UserFavorite()
                user_favor.fav_id = fav_id
                user_favor.user = request.user
                user_favor.fav_type = fav_type
                user_favor.save()

                return JsonResponse({
                    'status': 'success',
                    'msg': '已收藏',
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': 'favor fail',
            })




