from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db.models import Q
from django.shortcuts import render,get_object_or_404,redirect
from .models import Task
from .serializers import TaskSerializer


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


def index(request):
    return render(request, 'index.html')


def task_detail(request, pk=None):
    task = Task.objects.get(pk=pk)
    return render(request, 'taskView.html', {'task': task})


from .forms import TaskForm  # Create a form for updating tasks

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the task list after updating
    else:
        form = TaskForm(instance=task)

    return render(request, 'taskUpdate.html', {'form': form, 'task': task})