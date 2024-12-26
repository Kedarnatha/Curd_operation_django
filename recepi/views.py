from django.shortcuts import render, redirect
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username already exists')
            return redirect('/register/')


        user = User.objects.create(
            first_name =  first_name,
            last_name = last_name,
            username = username
         )
        user.set_password(password)
        user.save()
        messages.info(request,'Account created successfully')
        return redirect('/register/')


    return render(request,'register.html')




def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'invalid username')
            return redirect('login_page')

        user = authenticate(request,username=username,password=password)

        if user is None:
            messages.error(request,'invalid password')
            return redirect('login_page')
        else:
            login(request,user)
            return redirect('recipes')


    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('login_page')




@login_required(login_url='login_page')
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image,
        )
        return redirect('/recipes/')


    queryset = Recipe.objects.all()
    context = {'recipes':queryset}
    return render(request,'recipe.html',context)


@login_required(login_url='login_page')
def delete_recipes(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')

@login_required(login_url='login_page')
def update_recipes(request,id):
    queryset = Recipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect('/recipes/')

    context = {'recipe':queryset}
    return render(request,'update_recipe.html',context)