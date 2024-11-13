# decorators.py
from functools import wraps
from django.http import HttpResponseForbidden

def group_required(group_names):
    
    def decorator(view_func):
        # O decorator `@wraps` para garantir que a função da view seja corretamente embrulhada
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verifica se o usuário está autenticado
            if not request.user.is_authenticated:
                # Se não estiver autenticado, retorna uma resposta HTTP proibida (403)
                return HttpResponseForbidden()

            # Verifica se o usuário pertence a algum dos grupos fornecidos
            if not request.user.groups.filter(name__in=group_names).exists():
                # Se não pertencer a um dos grupos, também retorna uma resposta HTTP proibida (403)
                return HttpResponseForbidden()

            # Se o usuário estiver autenticado e pertencer a um dos grupos, chama a view original
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
