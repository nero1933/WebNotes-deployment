from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from .forms import *
from .utils import *

menu = [
    {'title': 'Private Notes', 'url_name': 'private_notes'},
]


def index(request):
    return render(request, 'notes/index.html', {'menu': menu, 'title': 'Home Page'})


class PrivateNotes(LoginRequiredMixin, PrivateNoteMixin, ListView):
    model = Note
    template_name = 'notes/private_notes.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Private Notes', selected='private_notes')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        self.kwargs['username'] = self.request.user
        return Note.objects.filter(user__username=self.kwargs['username']).select_related('user')


class ShowNote(LoginRequiredMixin, PrivateNoteMixin, GetObjMixin, DetailView):
    model = Note
    template_name = 'notes/show_note.html'
    context_object_name = 'note'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.folder:
            context['folder_selected'] = self.object.folder.pk
            context['folder_link'] = True

        c_def = self.get_user_context(title='Note: ' + str(context['note']),
                                      note_selected=self.object.pk)

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return super().get_object()  # inherits form GetNoteMixin


class AddPrivateNote(LoginRequiredMixin, PrivateNoteMixin, DataAssignMixin, CreateView):
    form_class = PrivateNoteFormMixin
    template_name = 'notes/add_private_note.html'
    context_object_name = 'note'
    success_url = reverse_lazy('private_notes')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add note', selected='add_private_note')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form, *args):
        return super().form_valid(Note, form, 'private_notes')

    def get_form_kwargs(self):
        kwargs = super(AddPrivateNote, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class UpdatePrivateNote(LoginRequiredMixin, PrivateNoteMixin, GetObjMixin, UpdateView):
    model = Note
    form_class = PrivateNoteFormMixin
    template_name = 'notes/update_private_note.html'
    context_object_name = 'note'
    success_url = reverse_lazy('private_notes')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Change note')
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return super().get_object()  # inherits form GetNoteMixin

    def get_form_kwargs(self):
        kwargs = super(UpdatePrivateNote, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class DeletePrivateNote(LoginRequiredMixin, PrivateNoteMixin, GetObjMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_object.html'
    success_url = reverse_lazy('private_notes')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Delete note')
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return super().get_object()  # inherits form GetNoteMixin


class DeleteAllPrivateNotes(LoginRequiredMixin, PrivateNoteMixin, DeleteListView):
    model = Note
    template_name = 'notes/delete_object.html'
    login_url = reverse_lazy('login')
    paginate_by = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Delete all notes', object='All notes')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Note.objects.filter(user__username=self.request.user.username).select_related('user')

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'username': self.request.user.username})


class AllFolders(LoginRequiredMixin, PrivateNoteMixin, ListView):
    model = Folder
    template_name = 'notes/all_folders.html'
    context_object_name = 'folders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='All Folders', selected='all_folders')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Folder.objects.filter(user__username=self.request.user).select_related('user')


class ShowFolder(LoginRequiredMixin, PrivateNoteMixin, ListView):
    model = Note
    template_name = 'notes/private_notes.html'
    context_object_name = 'notes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        f = Folder.objects.get(user=self.request.user.id, slug=self.kwargs.get('slug', None))
        c_def = self.get_user_context(title='Folder: ' + str(f.title), folder_selected=f.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Note.objects.filter(user__username=self.kwargs['username'],
                                   folder__slug=self.kwargs['slug']
                                   ).select_related('user').select_related('folder')

    def get(self, *args, **kwargs):
        try:
            return super().get(self, *args, **kwargs)
        except Folder.DoesNotExist:
            raise Http404('No such folder')


class DeleteFolder(LoginRequiredMixin, PrivateNoteMixin, GetObjMixin, DeleteView):
    model = Folder
    template_name = 'notes/delete_object.html'
    success_url = reverse_lazy('all_folders')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Delete note')
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return super().get_object()  # inherits form GetObjMixin

    # def get_object(self, queryset=None):
    #     try:
    #         return Folder.objects.get(user=self.request.user.pk, slug=self.kwargs.get('slug', None))
    #     except self.model.DoesNotExist:
    #         raise Http404("No such folder")


class DeleteAllFolders(LoginRequiredMixin, PrivateNoteMixin, DeleteListView):
    model = Folder
    template_name = 'notes/delete_object.html'
    login_url = reverse_lazy('login')
    paginate_by = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Delete all folder', object='All folder')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Folder.objects.filter(user__username=self.request.user.username).select_related('user')

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'username': self.request.user.username})


class AddFolder(LoginRequiredMixin, PrivateNoteMixin, DataAssignMixin, CreateView):
    form_class = AddFolderForm
    template_name = 'notes/add_folder.html'
    success_url = reverse_lazy('all_folders')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add Folder', selected='add_folder')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form, *args):
        return super().form_valid(Folder, form, 'all_folders')


class SignInUser(PrivateNoteMixin, CreateView):
    form_class = SignInUserForm
    template_name = 'notes/log_sign_in.html'
    success_url = reverse_lazy('user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign in', selected='sign_in')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('private_notes')

    def get(self, request, *args, **kwargs):
        # Restricted authenticated users to sign in
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('private_notes'))

        return super().get(request, *args, **kwargs)


class LoginUser(PrivateNoteMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'notes/log_sign_in.html'
    redirect_authenticated_user = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login', selected='login')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('private_notes')


def logout_user(request):
    logout(request)
    return redirect('home')


class UserPage(PrivateNoteMixin, LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/user_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=self.request.user.username, user_selected=True)
        c_def.pop('selected_menu', None)
        context['total_notes'] = len(Note.objects.filter(user__username=
                                                         self.kwargs['username']).select_related('user'))
        context['total_folders'] = len(Folder.objects.filter(user__username=
                                                             self.kwargs['username']).select_related('user'))

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return self.request.user


class DeleteUser(LoginRequiredMixin, PrivateNoteMixin, DeleteView):
    model = User
    template_name = 'notes/delete_object.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Delete user')
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


def about_us(request):
    return render(request, 'notes/about_us.html', {'menu': menu, 'title': 'About Us'})


def contact_us(request):
    return render(request, 'notes/contact_us.html', {'menu': menu, 'title': 'Contact Us'})
