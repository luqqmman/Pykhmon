from django.shortcuts import redirect
from django.urls import reverse


class SessionRequiredMixin:
    session_key = 'pk' 

    def dispatch(self, request, *args, **kwargs):
        if self.session_key not in request.session:
            return redirect(reverse('select_session')) 
        return super().dispatch(request, *args, **kwargs)