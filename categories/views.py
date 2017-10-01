from django.shortcuts import render
from categories.models import Category


# Create your views here.

def index(request):
  categories = Category.objects.filter(level = 1)
  context = {
    'categories' : categories
  }

  return render(request, 'categories/index.html', context)

def show(request, category_id):
  sub_categories = Category.objects.filter(parent_id = category_id)
  current_category = Category.objects.get(id = category_id)
  list_parent = []

  while current_category.parent_id != -1:
    list_parent.append(current_category)
    current_category = current_category.parent
  list_parent.append(current_category)
  list_parent.reverse()

  context = {
    'list_parent' : list_parent,
    'categories' : sub_categories
  }

  return render(request, 'categories/index.html', context)
