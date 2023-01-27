import warnings

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured
from django.forms import Form
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import BaseListView

from .models import *

from slugify import slugify

menu = [
    {'title': 'Private Notes', 'url_name': 'private_notes'},
]

sidebar_notes_menu = [
    {'name': 'All', 'url_name': 'private_notes'},
    {'name': 'Add', 'url_name': 'add_private_note'},
]

sidebar_folder_menu = [
    {'name': 'All', 'url_name': 'all_folders'},
    {'name': 'Add', 'url_name': 'add_folder'},
]


class PrivateNoteMixin:
    paginate_by = 9

    @staticmethod
    def get_sidebar_manu(context_item, sidebar_menu):
        """
        If there are no notes the function will remove 'all' link and
        return dict with only 'add' link. If there are notes the function
        will return 'all' and 'add'. Same with the folders.
        context_item - queryset,
        sidebar_menu - dict
        """
        m = sidebar_menu.copy()
        if len(context_item) == 0:
            m.pop(0)

        return m

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['selected_menu'] = 'private_notes'
        self.kwargs['username'] = self.request.user
        context['sidebar_notes'] = Note.objects.filter(user__username=
                                                       self.kwargs['username']).select_related('user')[:5]
        context['sidebar_folders'] = Folder.objects.filter(user__username=
                                                           self.kwargs['username']).select_related('user')[:5]

        context['sidebar_notes_menu'] = self.get_sidebar_manu(context['sidebar_notes'], sidebar_notes_menu)
        context['sidebar_folder_menu'] = self.get_sidebar_manu(context['sidebar_folders'], sidebar_folder_menu)

        return context


class GetObjMixin:
    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(user=self.request.user.pk, slug=self.kwargs.get('slug', None))
        except self.model.DoesNotExist:
            raise Http404("No such obj")


class DataAssignMixin:
    @staticmethod
    def slug_check(model, user_id, slug):
        """
        Method is checking is there an object in db with this slug.
        If True: add to slug '-02', if slug with '-02' exists try '-03'.
        Continue until slug will be uniq for the user.
        """
        try:
            obj = model.objects.get(user=user_id, slug=slug)
            slug = obj.slug + '-02'
            obj = model.objects.get(user=user_id, slug=slug)

            while obj:
                duplicate_number = slug[-2:]
                slug = slug[:-2] + str(int(duplicate_number) + 1).rjust(2, '0')
                obj = model.objects.get(user=user_id, slug=slug)

        except model.DoesNotExist:
            return slug

    def form_valid(self, model, form, url):
        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.slug = self.slug_check(model, self.request.user.pk, slugify(form_obj.title))
        form_obj.save()
        return redirect(url)


#
#
#


class ListDeletionMixin:
    """Provide the ability to delete list of objects."""

    success_url = None

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.queryset = self.get_queryset()
        success_url = self.get_success_url()
        self.queryset.delete()
        return HttpResponseRedirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url.format(**self.queryset.__dict__)
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")


class BaseListDeleteView(ListDeletionMixin, FormMixin, BaseListView):
    """
    Base view for deleting an object.

    Using this base class requires subclassing to provide a response mixin.
    """

    form_class = Form

    def post(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.queryset.delete()
        return HttpResponseRedirect(success_url)


class DeleteListView(BaseListDeleteView, SingleObjectTemplateResponseMixin):
    """
    View for deleting a queryset retrieved with self.get_queryset(), with a
    response rendered by a template.
    """

    template_name_suffix = "_confirm_delete"


#
#
#
