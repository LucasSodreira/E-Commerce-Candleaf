from functools import wraps
from django.http import HttpResponseForbidden

# Decorator personalizado que restringe acesso a views com base em grupos do usuário
def group_required(group_names):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verifica se o usuário está autenticado
            if not request.user.is_authenticated:
                # Retorna 403 se não estiver logado
                return HttpResponseForbidden()

            # Verifica se o usuário pertence a pelo menos um dos grupos exigidos
            if not request.user.groups.filter(name__in=group_names).exists():
                # Retorna 403 se não tiver permissão
                return HttpResponseForbidden()

            # Libera o acesso se o usuário estiver autenticado e no grupo correto
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
