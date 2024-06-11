from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import SubPod, Brigad, Task, CustomUser
from .forms import SubPodForm, BrigadForm, TaskForm


class CustomLoginView(LoginView):
    template_name = 'cms_app/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/cms/gen_pod_dashboard/'
        elif user.role == 'sub_pod':
            return '/cms/sub_pod_dashboard/'
        elif user.role == 'brigad':
            return '/cms/brigad_dashboard/'
        elif user.role == 'qa':
            return '/cms/qa_dashboard/'
        else:
            return '/'


class GenPodDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'cms_app/gen_pod_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_pods'] = SubPod.objects.all()
        context['form'] = SubPodForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SubPodForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = CustomUser.objects.create_user(username=username, password=password, role='sub_pod')
            sub_pod = form.save(commit=False)
            sub_pod.user = user
            sub_pod.save()
            return redirect('gen_pod_dashboard')
        return self.get(request, *args, **kwargs)


class SubPodDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'cms_app/sub_pod_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brigads'] = Brigad.objects.filter(sub_pod=self.request.user.sub_pod)
        context['tasks'] = Task.objects.all()
        context['brigad_form'] = BrigadForm()
        context['task_form'] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'create_brigad' in request.POST:
            brigad_form = BrigadForm(request.POST)
            if brigad_form.is_valid():
                username = brigad_form.cleaned_data['username']
                password = brigad_form.cleaned_data['password']
                user = CustomUser.objects.create_user(username=username, password=password, role='brigad')
                brigad = brigad_form.save(commit=False)
                brigad.user = user
                brigad.save()
                return redirect('sub_pod_dashboard')

        elif 'create_task' in request.POST:
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                task_form.save()
                return redirect('sub_pod_dashboard')

        return self.get(request, *args, **kwargs)


class BrigadDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'cms_app/brigad_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unassigned_tasks'] = Task.objects.filter(responsible__isnull=True)
        context['tasks'] = Task.objects.filter(responsible=self.request.user.brigad)
        return context

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        are_tasks_done = Task.objects.filter(is_done=False, id__lt=task_id).exists()
        if are_tasks_done:
            return self.get(request, *args, **kwargs)
        task = Task.objects.get(id=task_id)
        if 'take_task' in request.POST:
            task.responsible = self.request.user.brigad
            task.save()
        elif 'set_done' in request.POST:
            task.is_done = request.POST.get('is_done') == 'true'
            task.save()
        return self.get(request, *args, **kwargs)


class QADashboard(LoginRequiredMixin, TemplateView):
    template_name = 'cms_app/qa_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        if 'set_done' in request.POST:
            task.is_done = request.POST.get('is_done') == 'true'
        elif 'set_checked' in request.POST:
            task.is_checked = request.POST.get('is_checked') == 'true'
        task.save()
        return self.get(request, *args, **kwargs)
