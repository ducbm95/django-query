from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from categories.models import Category

from backend.query_classification import *

queryClf = QueryClassification()

def index(request):
  query = request.GET.get('query')
  context = {}
  if query:
    context['query'] = query

    global queryClf
    best_classes = queryClf.predict_best_classes_with_score(query)
    context['predicted_categories'] = []
    for a_class in best_classes:
      context['predicted_categories'].append(
        { 'category' : Category.objects.get(id = a_class['class']), 'score' : a_class['score'] })

  return render(request, 'queries/index.html', context)
