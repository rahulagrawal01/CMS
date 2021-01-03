from django.shortcuts import render
from .models import Data
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
import re
from django.contrib.auth import logout


def home(request):
  data= Data.objects.all()
  return render(request, 'index.html',{'data':data})

def login(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      from django.contrib.auth import login
      login(request, user)
      return redirect('/')
    else:
        message = "Invalid username or password"
        return render(request, "login.html", {"mess": message})
  return render(request, "login.html")

def signup(request):
  if request.method == "POST":
    email = request.POST['email']
    username = request.POST['username']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']
    if User.objects.filter(username=username).exists():
      messages.error(request, "Username is  already taken. pleasetry another one !")
      return redirect('signup')
    if len(username) > 15:
      messages.error(request, "Username must be less tahn 15 characters")
      return redirect('signup')
    if not username.isalnum():
      messages.error(request, "Username should only contain letters")
      return redirect('signup')
    if pass1 != pass2:
      messages.error(request, "Password Do not Match")
      return redirect('signup')
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, pass1)
    if len(pass1) > 5 and len(pass1) < 21:
      if mat:
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.error(request, "Successfully registerd Your Account")
        return redirect('login')
      else:
        messages.error(request,"Password should have at least one uppercase letter,lowercse,one number and one special symbol.")
        return redirect('signup')
    else:
      messages.error(request, "Password lengnth shoul be 6-20.")
      return redirect('signup')
  return render(request, "signup.html")


def logout_user(request):
  logout(request)
  return redirect('/')


def upload_article(request):
  if request.user.is_authenticated == True:
    if request.method == "POST":
      title = request.POST['title']
      image = request.FILES['image']
      desc = request.POST['desc']
      data = Data(title=title, img=image, desc=desc, user=request.user)
      try:
        data.save()
        messages.success(request, "successfully uploaded")
        return render(request, 'upload_article.html')
      except:
        mess = "Something went wrong"
        return render(request, 'upload_article.html', {"mess": mess})
    return render(request, 'upload_article.html')
  else:
    return redirect('login')


def my_article(request):
  if request.user.is_authenticated == True:
    data = Data.objects.filter(user=request.user)
    name= User.objects.get(username=request.user).first_name
    return render(request, "my_articles.html", {"data":data,"user_name":name})
  else:
    return redirect('login')


def all_article(request):
  if request.user.is_authenticated == True:
    data = Data.objects.all()
    dict= {}
    id = 1
    for x in data:
      dict[id] = {}
      dict[id]['data'] = x
      name= User.objects.get(id=x.user_id).first_name
      dict[id]['name'] = name
      id += 1
    return render(request, "all_articles.html", {"data": dict})
  else:
    return redirect('login')


def delete_article(request,id):
  if request.user.is_authenticated == True:
    song = Data.objects.filter(id=id).delete()
    messages.success(request, "successfully removed")
    return redirect('my_article')
  else:
    return redirect('login')


def update_article(request,id):
  if request.user.is_authenticated == True:
    if request.method == "POST":
      title = request.POST['title']
      image = request.FILES['image']
      desc = request.POST['desc']
      data = Data(id=id, title=title, img=image, desc=desc, user=request.user)
      try:
        data.save()
        messages.success(request, "successfully updated")
        return redirect('my_article')
      except:
        mess = "Something went wrong"
        return render(request, 'upload_article.html', {"mess": mess})
    data = Data.objects.get(id=id)
    return render(request, 'update_article.html',{"data":data})
  else:
    return redirect('login')


def about_us(request):
  return render(request, 'about_us.html')


def contact_us(request):
  if request.method == "POST":
    mess = "Thanks for contacting us"
    return render(request, 'contact_us.html', {"mess": mess})
  return render(request, 'contact_us.html')