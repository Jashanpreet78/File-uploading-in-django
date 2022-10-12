from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import FileForm
from .models import File
from django.contrib.auth.forms import User

from django.core.exceptions import *
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'

# uploading the file
@login_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

# listing
def file_list(request):
    try:
        files = File.objects.filter(user=request.user)
        return render(request, 'file_list.html', {
            'files': files
        })
    except ObjectDoesNotExist:
        print('not found')

# upload the file along with showing of list of files
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_form = form.save(commit=False)
            file_form.user = request.user
            file_form.save()
            return redirect('file_list')
    else:
        form = FileForm()
    return render(request, 'upload_file.html', {
        'form': form
    })

# deleting the file view
def delete_file(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
    return redirect('file_list')

#view for sign in authentication
def signup(request):
    form=UserCreationForm()
    if request.method== 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect('home')
    
    return render(request,'signup.html',{'form':form})
