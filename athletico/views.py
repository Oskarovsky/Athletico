from django.shortcuts import render
from django.http import HttpResponse
from athletico.firebase import send_to_firebase, update_firebase_snapshot, add_exercise


def home(request):
    add_exercise()
    context_dict = {'names_from_context': 'names_from_context'}
    return render(request, 'index.html', context_dict)
