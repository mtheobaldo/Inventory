
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Item, Category

# Create your views here.
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX
    Must be used with an object-based FormView
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = model_to_dict(self.object)
            return JsonResponse(data)
        else:
            return response


class CategoryListView(ListView):
    model = Category

class CategoryDetailView(DetailView):
    model = Category

class CreateCategoryView(CreateView):
    model = Category
    fields = ['parent', 'name', 'descripton']
    
    def get_success_url(self):
        return reverse('inventory:categorydetail', args=(self.object.pk,))

class UpdateCategoryView(UpdateView):
    model = Category
    fields = ['parent', 'name', 'descripton']
    
    def get_success_url(self):
        return reverse('inventory:categorydetail', args=(self.object.pk,))

class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('inventory:deletecategorysuccess')

class CreateItemView(CreateView):
    model = Item
    fields = ['name', 'quantity', 'sku', 'category']

    def get_success_url(self):
        return reverse('inventory:categorydetail', args=(self.object.category.id,))

class UpdateItemView(UpdateView):
    model = Item
    fields = ['name', 'quantity', 'sku', 'category']


class DeleteItemView(DeleteView):
    model = Item
    success_url = reverse_lazy('inventory:deleteitemsuccess')