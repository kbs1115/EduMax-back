from community.model.models import Like


def check_like_inst_exist_with_post_id(inst_id, user):
    return Like.objects.filter(post=inst_id, user=user).exists()


def check_like_inst_exist_with_comment_id(inst_id, user):
    return Like.objects.filter(comment=inst_id, user=user).exists()
