from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Redirect to 'home' if user is already logged in
            return redirect('home')
        else:
            # Allow access to the view if the user is not authenticated
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            # Check if the user is in any groups
            if request.user.groups.exists():
                # Get the name of the first group
                group = request.user.groups.all()[0].name
            
            # Check if the user's group is in the list of allowed roles
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                # Return an unauthorized response if the user’s group is not allowed
                return HttpResponse("You are not authorized to view this page")
        
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        # Check if the user is in any groups
        if request.user.groups.exists():
            # Get the name of the first group
            group = request.user.groups.all()[0].name
        
        # Redirect to 'user' page if the user is in the 'customer' group
        if group == "customer":
            return redirect("user")
        
        # Allow access if the user is in the 'admin' group
        if group == "admin":
            return view_func(request, *args, **kwargs)
        
        # Return an unauthorized response if the user is not an admin
        return HttpResponse('You are not authorized to view this page', status=403)

    return wrapper_func

