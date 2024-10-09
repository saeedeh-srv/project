from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from .models import Project, Task, SubTask
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectForm, ProjectUpdateForm, TaskForm,SubTaskForm


class ProjectListView(LoginRequiredMixin, ListView):
    """
    this view will return all of the projects
    """
    login_url = 'accounts/login/'

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(user=request.user)
        context = {
            'projects': projects
        }
        return render(request, 'Projects/projects.html', context)



class ProjectCreateView(CreateView):
    """
    this view give us create function for project model
    """

    form_class = ProjectForm
    template_name = 'Projects/create_project.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, request.FILES, )
        if form.is_valid():
            data = form.cleaned_data
            project = Project.objects.create(
                user=user,
                title=data['title'], image=data['image'],
                description=data['description'], color=data['color'],
                start_date=data['start_date'], end_date=data['end_date'],
                budget=data['budget']
            )
            if project:
                messages.success(request, 'your project saved', 'success')
                return redirect('projects:projects_list')
            messages.error(request, 'something went wrong !!!', 'danger')
        else:
            form = self.form_class()
        return render(request, 'Projects/create_project.html', {"form": form})


class ProjectDeleteView(DeleteView):
    """
        delete project
    """
    model = Project
    pk_url_kwarg = 'pk'
    template_name = 'Projects/confirm_delete_pj.html'
    success_url = '/'


class UpdateProjectView(UpdateView):
    """
    update projectes
    """
    model = Project
    form_class = ProjectUpdateForm
    pk_url_kwarg = 'pk'
    template_name = 'Projects/update.html'
    success_url = '/'



class TaskCreateView(CreateView):
    """
    this view give us create Task for project
    """
    form_class = TaskForm
    template_name = 'Projects/create_task.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = Project.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            task = Task.objects.create(
                project=self.project,
                title=data['title'],
                image=data['image'],
                description=data['description'],
                color=data['color'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                budget=data['budget']
            )
            if task:
                messages.success(request, 'Your task saved successfully.', 'success')
                return redirect('projects:task_view', pk=self.project.pk)
            messages.error(request, 'Something went wrong!', 'danger')
        else:
            form = self.form_class()
        return render(request, 'Projects/create_task.html', {"form": form})


class TaskView(ListView):
    """
        this view will return all of the tasks
        """
    model = Task
    template_name = 'Projects/tasks.html'

    def get(self, request, *args, **kwargs):
        project_pk = kwargs.get('pk')
        tasks = Task.objects.filter(project=project_pk)
        context = {
            'tasks': tasks,
            'project': Project.objects.get(pk=project_pk),
        }
        return render(request, 'Projects/tasks.html', context)



class TaskUpdateView(UpdateView):
    """
    update task
    """
    model = Task
    form_class = TaskForm
    pk_url_kwarg = 'pk'
    template_name = 'Projects/update_task.html'
    success_url = '/'


class TaskDeleteView(DeleteView):
    """delete task"""
    model = Task
    pk_url_kwarg = 'pk'
    template_name = 'Projects/confirm_delete_task.html'
    success_url = '/'
class SubTaskView(ListView):
    """
           this view will return all of the subtasks
           """
    model = SubTask
    template_name = 'Projects/subtasks.html'

    def get(self, request, *args, **kwargs):
        project_pk = kwargs.get('pk')
        subtasks = SubTask.objects.filter(project=project_pk)
        context = {
            'subtasks': subtasks,
            'project': Project.objects.get(pk=project_pk),
        }
        return render(request, 'Projects/subtasks.html', context)
class SubTaskCreateView(CreateView):
    """
    this view give us create subTask for project
    """
    form_class = SubTaskForm
    template_name = 'Projects/create_subtask.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = Project.objects.get(pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            subtask = SubTask.objects.create(
                project=self.project,
                title=data['title'],
                image=data['image'],
                description=data['description'],
                color=data['color'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                budget=data['budget']
            )
            if subtask:
                messages.success(request, 'Your task saved successfully.', 'success')
                return redirect('projects:subtask_view', pk=self.project.pk)
            messages.error(request, 'Something went wrong!', 'danger')
        else:
            form = self.form_class()
        return render(request, 'Projects/create_subtask.html', {"form": form})
class SubTaskDeleteView(DeleteView):
    """delete subtask"""
    model = SubTask
    pk_url_kwarg = 'pk'
    template_name = 'Projects/confirm_delete_subtask.html'
    success_url = '/'

class SubTaskUpdateView(UpdateView):
    """
    update subtask
    """
    model = SubTask
    form_class = SubTaskForm
    pk_url_kwarg = 'pk'
    template_name = 'Projects/update_subtask.html'
    success_url = '/'



class ProjectDetailView(DetailView):
    """
    Detail view for a project
    """
    model = Project
    template_name = 'Projects/project_detail.html'
    context_object_name = 'project'

class TaskDetailView(DetailView):
    """
    Detail view for a task
    """
    model = Task
    template_name = 'Projects/task_detail.html'
    context_object_name = 'task'

class SubTaskDetailView(DetailView):
    """
    Detail view for a subtask
    """
    model = SubTask
    template_name = 'Projects/subtask_detail.html'
    context_object_name = 'subtask'