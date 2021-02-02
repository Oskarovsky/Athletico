from django.shortcuts import render


def home(request):
    # add_exercise()
    context_dict = {'names_from_context': 'names_from_context'}
    return render(request, 'index.html', context_dict)

def exercise(request):
    return render(request, 'new_exercise.html')
