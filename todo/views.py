
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo


def inscription(request):
    if request.method == 'GET':
        return render(request, 'todo/inscription.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('todoactuels')

            except IntegrityError:
                return render(request, 'todo/inscription.html',
                              {'form': UserCreationForm(),
                               'erreur': 'ce nom dutilisateur est deja pris,choisir un  autre utilisateur'})

        else:
            return render(request, 'todo/inscription.html',
                          {'form': UserCreationForm(), 'erreur': 'le mot de passe ne correspond pas!'})


def deconnecxion(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    return render(request, 'todo/home.html')


def connecxion(request):
    if request.method == 'GET':
        return render(request, 'todo/connexion.html', {'form': AuthenticationForm()})

    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/connexion.html',
                          {'form': AuthenticationForm(), 'erreur': 'nom dutilisateur ou '
                                                                   'mot de passe  ne '
                                                                   'correspond pas'})
        else:
            login(request, user)
            return redirect('todoactuels')


def creation(request):
    if request.method == 'GET':
        return render(request, 'todo/creation.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return render(request, 'todo/todoactuels.html')

        except ValueError:
            return render(request, 'todo/creation.html', {'form': TodoForm(), 'erreur': 'erreur'})


def todoactuels(request):
    todos = Todo.objects.filter(user=request.user, dateacheve__isnull=True)
    return render(request, 'todo/todoactuels.html', {'todos': todos})


def consultation(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/consultation.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('todoactuels')
        except ValueError:
            return render(request, 'todo/consultation.html', {'todo': todo, 'form': form ,'erreur' :'mauvaise infos'})
