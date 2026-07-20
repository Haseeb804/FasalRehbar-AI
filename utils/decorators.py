"""
Decorator utilities for common patterns.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def ajax_required(function):
    """Decorator to require AJAX request"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.headers.get("x-requested-with") == "XMLHttpRequest":
            return redirect("home")
        return function(request, *args, **kwargs)
    return wrap
