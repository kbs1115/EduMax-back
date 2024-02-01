from rest_framework.exceptions import PermissionDenied

from community.domain.definition import PostCategories


def only_staff_can_create_post_notice(category, author):
    if category == PostCategories.NOTICE:
        if not (author.is_staff or author.is_superuser):
            raise PermissionDenied()
