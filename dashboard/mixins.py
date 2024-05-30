from django.shortcuts import redirect
from django.urls import reverse


class SessionRequiredMixin:
    session_key = 'mikrotik'  # Default session key

    def dispatch(self, request, *args, **kwargs):
        if self.session_key not in request.session:
            return redirect(reverse('select_session'))  # Ganti dengan URL atau view yang sesuai
        return super().dispatch(request, *args, **kwargs)