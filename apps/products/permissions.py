from typing import Iterable

from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin


class PermissionsRequiredMixin(PermissionRequiredMixin, AccessMixin):
    permission_required: tuple = (None,)

    def dispatch(self, request, *args, **kwargs):
        if request.user.type not in self.get_permission_required():
            return self.handle_no_permission()
        return super(AccessMixin, self).dispatch(request, *args, **kwargs)

    def get_permission_required(self):
        """overridden function that validate and then returns permissions"""
        if self.permission_required == (None,):
            raise ImproperlyConfigured

        if not isinstance(self.permission_required, (list, tuple, set)):
            raise TypeError(f'must be List, Tuple or Set '
                            f'not {type(self.permission_required)}')

        return self.permission_required


def permissions_required(usertypes: Iterable[str]):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and user.type in usertypes:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return _wrapped_view

    return decorator
