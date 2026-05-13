"""
Core app views - Error pages and utility views.
"""

from django.shortcuts import render


def error_404(request, exception):
    """
    Custom 404 error page handler.
    
    Args:
        request: HTTP request object
        exception: The exception that triggered the error
        
    Returns:
        Rendered 404 error template
    """
    return render(request, 'core/404.html', status=404)


def error_500(request):
    """
    Custom 500 error page handler.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered 500 error template
    """
    return render(request, 'core/500.html', status=500)
