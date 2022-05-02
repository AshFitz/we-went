from django.shortcuts import render

def about(request):
    """
    View to render the about template
    """
    page_title = "About Us"
    template = "about.html"
    context = {
        'page_title': page_title,
    }
    return render(request, template, context)
