from django.shortcuts import render
from django.views.generic import CreateView
from owners.models import Branch

class BranchCreateView(CreateView):
    model = Branch
    fields = ['name', 'address', 'opening_hour', 'closing_hour']
