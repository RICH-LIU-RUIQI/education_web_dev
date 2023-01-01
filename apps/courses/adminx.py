import xadmin

from apps.courses.models import Course, Lesson, CourseResource, Video


class GlobalSettings(object):
    site_title = 'IMooc Back Management'
    site_footer = 'IMooc'
    menu_style = 'accordion'  # foldable


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


# no succession
class CourseAdmin(object):
    ''' foreign key + __ + feature name '''
    list_display = ['name', 'descr', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'descr', 'detail', 'degree', 'students']
    list_filter = ['name', 'course_teacher__name', 'descr', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "descr"]


class LessonAdmin(object):
    list_display = ['parent_course', 'name', 'add_time']
    search_fields = ['parent_course', 'name']
    list_filter = ['parent_course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['parent_lesson', 'name', 'add_time']
    search_fields = ['parent_lesson', 'name']
    list_filter = ['parent_lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['parent_course', 'name', 'download', 'add_time']
    search_fields = ['parent_course', 'name', 'download']
    list_filter = ['parent_course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
