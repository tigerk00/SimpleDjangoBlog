from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F

#user profile page
@login_required
def user(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }

    return render(request,"blog/profile.html", context)

#new user registration
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"Register successful, now Log in")
            logout(request)
            return redirect("login")
        else:
            messages.error(request,"Register Error!")
    else:
        form = UserRegisterForm()
    return render(request,"blog/register.html", {"form":form})


#user logging
def user_login(request):
	if request.method == "POST":
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			return redirect("home")
	else:
		form = UserLoginForm()

	return render(request,"blog/login.html",{"form":form})


def user_logout(request):
	logout(request)
	return redirect("login")



class Home(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Classic Blog Design"
        return context


class PostsByCategory(ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs["slug"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["slug"]
        return context


class GetPost(DetailView, CreateView):
    model = Post
    template_name = "blog/single.html"
    context_object_name = "post"

    form_class = CommentForm

    def get_initial(self):
        return {"name":self.request.user.username, "post":self.get_object()}

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F("views")+1
        self.object.save()
        self.object.refresh_from_db()
        return context



class PostsByTag(ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs["slug"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Записи по тeгу: " + str(Tag.objects.get(slug=self.kwargs["slug"]))
        return context

class Search(ListView):
    template_name = "blog/search.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get("s"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["s"] = f"s={self.request.GET.get('s')}&"  # & Поможет нам использовать два GET запроса в поисковой строке - ?s= и ?page=
        return context




