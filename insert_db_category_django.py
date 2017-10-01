# HOW TO RUN THIS SCRIPT
# python manage.py shell
# >> execfile("insert_db_category_django.py")

import django

import sys
sys.path.insert(0, 'F:\OneDrive\Documents\Elearning\Nam 4\TTTN\Code')
import os
os.chdir('F:\OneDrive\Documents\Elearning\Nam 4\TTTN\Code')
from category_generation import *

django.setup()
from categories.models import Category

def insert_to_db(node, level, parent_id):
  cate_id = node.id
  cate_name = node.cate_name

  if (cate_id != -1):
    # insert to db here if not exist
    # print cate_id
    if not Category.objects.filter(id = cate_id).exists():
      cate = Category(id = cate_id, name = cate_name, level = level, parent_id = parent_id)
      cate.save()

  if node.children:
    for child_node in node.children:
      insert_to_db(child_node, level + 1, node.id)

tree = CategoryTree()
insert_to_db(tree.root, 0, None)
