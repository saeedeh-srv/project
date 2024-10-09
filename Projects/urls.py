from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectDeleteView, UpdateProjectView, TaskView, TaskCreateView, \
    TaskUpdateView, TaskDeleteView, SubTaskView,SubTaskDeleteView,SubTaskUpdateView,SubTaskCreateView,ProjectDetailView,TaskDetailView,SubTaskDetailView

app_name = 'projects'

urlpatterns = [
    # path('', ProjectListView.as_view(), name='projects_list'),
    path('', ProjectListView.as_view(), name='projects_list'),
    path('create/project', ProjectCreateView.as_view(), name='project_create'),
    path('delete/project/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('update/project/<int:pk>/', UpdateProjectView.as_view(), name='project_update'),
    path('task/view/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('create/tasks/<int:pk>/', TaskCreateView.as_view(), name='create_tasks'),
    path('task/update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('subtask/view/<int:pk>/', SubTaskView.as_view(), name='subtask_view'),
    path('create/subtasks/<int:pk>/', SubTaskCreateView.as_view(), name='create_subtasks'),
    path('subtask/update/<int:pk>/', SubTaskUpdateView.as_view(), name='update_subtask'),
    path('subtask/delete/<int:pk>/', SubTaskDeleteView.as_view(), name='delete_subtask'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('subtasks/<int:pk>/', SubTaskDetailView.as_view(), name='subtask_detail'),

]



