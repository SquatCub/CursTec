from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import User, Course, Unit, Category, Comment
from django.core.paginator import Paginator

def index(request):
    categories = Category.objects.all()
    return render(request, "courses/index.html", {
        "categories": categories
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "courses/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "courses/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "courses/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "courses/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "courses/register.html")


def explore(request):
    courses = Course.objects.all().order_by("-date")
    paginator = Paginator(courses, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "courses/index.html", {
        "type": "explore",
        "page_courses": page_obj
    })
def category(request, id):
    category = Category.objects.get(id=id)
    courses = Course.objects.filter(category=category).order_by("-date")
    paginator = Paginator(courses, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "courses/index.html", {
        "type": "category",
        "category": category,
        "page_courses": page_obj
    })

def course(request, id):
    course = Course.objects.get(id=id)
    units = Unit.objects.filter(course=id)
    comments = Comment.objects.filter(course=id).order_by("-id")
    return render(request, "courses/index.html", {
        "type": "course",
        "course": course,
        "units": units,
        "comments": comments
    })
@login_required
def unit(request, id, uid):
    course = Course.objects.get(id=id)
    units = Unit.objects.filter(course=id)
    current = Unit.objects.get(id=uid)
    return render(request, "courses/index.html", {
        "type": "unit",
        "course": course,
        "units": units,
        "current": current
    })

@login_required
def enrolled(request):
    user = request.user
    courses = user.enrolled.all().order_by("-date")
    paginator = Paginator(courses, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "courses/index.html", {
        "type": "enrolled",
        "page_courses": page_obj
    })

@login_required
def teach(request):
    return render(request, "courses/index.html", {
        "type": "teach",
        "categories": Category.objects.all()
    })

@login_required
def create(request):
    if request.method == "POST":
        name = request.POST["name"]
        desc = request.POST["desc"]
        category = request.POST["category"]
        img = request.POST["img"]
        if(img == ""):
            img = "https://es.talentlms.com/wp-content/uploads/2018/10/talentlms-content-library.png"

        course = Course(user=request.user, title=name, description=desc, category=Category.objects.get(pk=category), img=img)
        course.save()
        return HttpResponseRedirect(reverse("teach"))
    else:
        return render(request, "courses/teach.html")
        
@login_required
def comment(request):
    if request.method == "POST":
        user = request.user
        course_id = request.POST["course"]
        content = request.POST["content"]
        course = Course.objects.get(id=course_id)
        comment = Comment(user=user, course=course, content=content)
        comment.save()
        return HttpResponseRedirect(reverse("course", args=(course_id, )))
    else:
        return HttpResponseRedirect(reverse("course", args=(course_id, )))

@login_required
def mine(request):
    courses = Course.objects.filter(user=request.user).order_by("-date")
    return render(request, "courses/index.html", {
        "type": "mine",
        "courses": courses
    })
@login_required
def one(request, title):
    course = Course.objects.get(title=title)
    return render(request, "courses/index.html", {
        "type": "one",
        "course": course
    })

@login_required
@csrf_exempt
def enroll(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    data = json.loads(request.body)

    enroll = data.get("enroll", "")

    course_id = data.get("course_id", "")
    course = Course.objects.get(id=course_id)

    choice = 1
    if enroll:
        if request.user in course.enrolled.all():
            course.enrolled.remove(request.user)
            choice = 0
        else:
            course.enrolled.add(request.user)
    course.save()
    total = course.enrolled.all().count()
    
    return JsonResponse({"message": "Enroll successfully.", "enrolled": choice, "total": total}, status=201) 

@login_required
@csrf_exempt
def like(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    data = json.loads(request.body)

    course_id = data.get("course_id", "")
    course = Course.objects.get(id=course_id)

    choice = 1
    if enroll:
        if request.user in course.like.all():
            course.like.remove(request.user)
            choice = 0
        else:
            course.like.add(request.user)
    course.save()
    total = course.likes()
    
    return JsonResponse({"message": "Like successfully.", "like": choice, "total": total}, status=201)

@csrf_exempt
@login_required
def edit(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    data = json.loads(request.body)
    course_id = data.get("course_id", "")
    title = data.get("title", "")
    desc = data.get("desc", "")
    img = data.get("img", "")
    
    course = Course.objects.get(id=course_id)

    if request.user != course.user:
        return JsonResponse({"error": "Edit only your own courses"})
    course.title = title
    course.description = desc
    course.img = img
    course.save()
    return JsonResponse({"message": "Course edited"}, status=201)

@login_required
def createUnit(request):
    if request.method == "POST":
        name = request.POST["name"]
        type = request.POST["type"]
        id = request.POST["id"]
        course = Course.objects.get(id=id)

        unit = Unit(user=request.user, title=name, course=course)
        unit.save()
        if type == "unit":
            uid = request.POST["uid"]
            return HttpResponseRedirect(reverse("unit", args=(id, uid)))
        return HttpResponseRedirect(reverse("course", args=(id, )))
    else:
        return render(request, "courses/explore.html")
@login_required
def deleteCourse(request):
    if request.method == "POST":
        id = request.POST["id"]
        course = Course.objects.get(id=id)
        if request.user != course.user:
            return HttpResponseRedirect(reverse("course", args=(id, )))
        course.delete()
    return HttpResponseRedirect(reverse ('mine'))
@login_required
def deleteUnit(request):
    if request.method == "POST":
        id = request.POST["id"]
        course = request.POST["course-id"]
        unit = Unit.objects.get(id=id)
        if request.user != unit.user:
            return HttpResponseRedirect(reverse("unit", args=(id, )))
        unit.delete()
    return HttpResponseRedirect(reverse("course", args=(course, )))

@csrf_exempt
@login_required
def editUnit(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    data = json.loads(request.body)
    unit_id = data.get("unit_id", "")
    title = data.get("title", "")
    desc = data.get("desc", "")
    notes = data.get("notes", "")
    video = data.get("vid", "")
    
    unit = Unit.objects.get(id=unit_id)

    if request.user != unit.user:
        return JsonResponse({"error": "Edit only your own units"})

    unit.title = title
    unit.description = desc
    unit.notes = notes
    unit.video = video
    unit.save()
    return JsonResponse({"message": "Unit edited"}, status=201)


