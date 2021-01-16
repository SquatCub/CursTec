from django.contrib import admin

from .models import User
from .models import Course
from .models import Unit
from .models import Category
from .models import Comment

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Comment)