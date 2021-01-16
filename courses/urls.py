from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('explore', views.explore, name="explore"),
    path('course/<str:id>', views.course, name="course"),
    path('enrolled', views.enrolled, name="enrolled"),
    path('teach', views.teach, name="teach"),
    path('create', views.create, name="create"),
    path('delete', views.deleteCourse, name="deleteCourse"),
    path('create-unit', views.createUnit, name="createUnit"),
    path('delete-unit', views.deleteUnit, name="deleteUnit"),
    path('my-courses', views.mine, name="mine"),
    path('my-courses/<str:title>', views.one, name="one"),
    path('course/<str:id>/<str:uid>', views.unit, name="unit"),
    path('comment', views.comment, name="comment"),
    path('category/<str:id>', views.category, name="category"),

    path('enroll', views.enroll, name="enroll"),
    path('like', views.like, name="like"),
    path('edit', views.edit, name="edit"),
    path('edit-unit', views.editUnit, name="editUnit")
]