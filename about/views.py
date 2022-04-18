from django.shortcuts import render

# Create your views here.
def about(request):
    page_title = "About Us"
    template = "about.html"
    context = {
        'page_title': page_title,
    }
    return render(request, template, context)