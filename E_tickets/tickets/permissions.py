from rest_framework import permissions

class IsOrganisationUserOrReadOnly(permissions.BasePermission):
    """
    Permission qui autorise tout le monde à voir les détails de l'organisation
    et les événements, mais seulement les utilisateurs liés peuvent éditer.
    """

    def has_object_permission(self, request, view, obj):
        # Si c'est une méthode sécurisée (GET, HEAD ou OPTIONS), tout le monde peut accéder
        if request.method in permissions.SAFE_METHODS:
            return True

        # Seuls les utilisateurs liés à l'organisation peuvent modifier
        return request.user in obj.organisation.users.all()