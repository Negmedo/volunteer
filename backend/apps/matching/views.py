from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def matching_stub(request):
    return render(request, "matching/index.html")