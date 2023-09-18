from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q
from django.shortcuts import render,get_object_or_404,redirect
from .models import Task
from .serializers import TaskSerializer
from .forms import TaskForm , RegistrationForm
from django.contrib.auth.decorators import login_required


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    # queryset = Task.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Task.objects.all()

        search_query = self.request.query_params.get('search', None)
        priority_filter = self.request.query_params.get('priority', None)
        due_date_filter = self.request.query_params.get('due_date', None)
        completed_filter = self.request.query_params.get('completed', None)

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))

        if priority_filter:
            if priority_filter == 'high':
                queryset = queryset.order_by('-priority', 'created_date')
            elif priority_filter == 'low':
                queryset = queryset.order_by('priority', 'created_date')

        if due_date_filter:
            if due_date_filter == 'asc':
                queryset = queryset.order_by('due_date')
            elif due_date_filter == 'desc':
                queryset = queryset.order_by('-due_date')

        if completed_filter:
            queryset = queryset.filter(completed=(completed_filter.lower() == 'true'))

        return queryset
    

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

@login_required(login_url='user_login')
def index(request):
    return render(request, 'index.html')


def task_detail(request, pk=None):
    task = Task.objects.get(pk=pk)
    return render(request, 'taskView.html', {'task': task})




def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')  
    else:
        form = TaskForm(instance=task)

    return render(request, 'taskUpdate.html', {'form': form, 'task': task})

from django.contrib.auth import login,logout,authenticate
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request,user)
            return redirect('index')
    else:
        form = RegistrationForm()
        return render(request,'registration.html', {'form': form})
        

from django.http import JsonResponse
from rest_framework.authtoken.models import Token



def user_login(request):
    # if request.user.is_authenticated():
    #     return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                login(request, user)
            except:
                
                return redirect('index')
            return redirect('index')
        else:
            return redirect('login')
            # token, created = Token.objects.get_or_create(user=user)
            # return JsonResponse({'token': token.key, 'user_id': user.id})
        
    return render(request,'login.html')

@login_required(login_url='user_login')
def logout_view(request):
    logout(request)
    return redirect('user_login')