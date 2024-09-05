from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir que apenas administradores possam
    criar, editar ou deletar. Usuários não autenticados ou não-admins podem
    apenas visualizar (GET).
    """
    def has_permission(self, request, view):
        # Permite apenas visualizações (GET, HEAD, OPTIONS) para usuários não administradores
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Apenas administradores podem criar, editar ou deletar
        return request.user and request.user.is_staff