from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import *
from base.forms import *


class HomeView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                    Q(name__icontains=q) |
                                    Q(description__icontains=q))
        topics = Topic.objects.all()[0:5]
        room_count = rooms.count()
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
        context['rooms'] = rooms
        context['topics'] = topics
        context['room_count'] = room_count
        context['room_messages'] = room_messages
        return context


class CustomLoginView(FormView):
    template_name = 'base/login_register.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.method == 'POST':
            email = self.request.POST.get('email').lower()
            password = self.request.POST.get('password')

            try:
                user = User.objects.get(email=email)
            except:
                messages.error(self.request, 'User does not exist')

            user = authenticate(self.request, email=email, password=password)

            if user is not None:
                login(self.request, user)
                return redirect('home')
            else:
                messages.error(self.request, 'Email OR password does not exit')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        page = 'login'
        if self.request.user.is_authenticated:
            return redirect('home')
        context = {'page': page}
        return context


class CustomLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')


class RoomPage(UpdateView):
    model = Room
    template_name = 'base/room.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        room = Room.objects.get(id=pk)
        room_messages = room.message_set.all().order_by('-created')
        participants = room.participants.all()
        context = {'room': room,
                   'room_messages': room_messages,
                   'participants': participants}
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        room = Room.objects.get(id=pk)
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


class TopicsPage(ListView):
    template_name = 'base/topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        topics = Topic.objects.filter(name__icontains=q)
        return topics


class ActivitiesPage(ListView):
    template_name = 'base/activity.html'
    queryset = Message.objects.all()
    context_object_name = 'room_messages'


class RegisterPage(FormView):
    template_name = 'base/login_register.html'
    form_class = MyUserCreationForm
    success_url = 'home'

    def form_valid(self, form):
        if self.request.method == 'POST':
            form = MyUserCreationForm(self.request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(self.request, user)
                return redirect('home')
            else:
                messages.error(self.request, 'Ann error occured during registration')
        return super().form_valid(form)


# @method_decorator(login_required, name='post')
class CreateRoom(LoginRequiredMixin, CreateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topics = Topic.objects.all()
        context['topics'] = topics
        return context

    def post(self, request, *args, **kwargs):
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('/')


class UpdateRoom(LoginRequiredMixin,UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'base/room_form.html'
    success_url = reverse_lazy('home')
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        room = Room.objects.get(id=pk)
        topics = Topic.objects.all()
        context['topics'] = topics
        context['room'] = room
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = RoomForm(request.POST)
        room = Room.objects.get(id=pk)
        topic_name = request.POST.get('topic')
        topic = Topic.objects.get(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')


class DeleteRoomPage(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'base/delete.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('home')


class DeleteMessageRoom(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'base/delete.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('home')


class UserProfile(TemplateView):
    template_name = 'base/profile.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        user = User.objects.get(id=pk)
        rooms = user.room_set.all()
        room_messages = user.message_set.all()
        topics = Topic.objects.all()
        context = {
            'user': user, 'rooms': rooms,
            'room_messages': room_messages,
            'topics': topics
        }
        return context


class UpdateUser(LoginRequiredMixin, CreateView):
    form_class = UserForm
    template_name = 'base/update-user.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        form = UserForm(instance=user)
        context ={
            'user': user,
            'form': form
        }
        return context

    def post(self, request, *args, **kwargs):
        user = User.objects.get(name=request.user.name)
        form = UserForm(request.POST, request.FILES, instance=user)
        form.save()
        return redirect('home')
