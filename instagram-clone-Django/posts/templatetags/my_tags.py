from django import template
from posts.models import CommentLikeModel, PostLikeModel, ReplyCommentLikeModel
from users.models import Follow

register = template.Library()

@register.simple_tag
def comment_like_icon(comment, user):
    return "fa-solid fa-heart" if CommentLikeModel.objects.filter(commentID=comment,
                                                                  userID=user).exists() else "fa-regular fa-heart"

@register.filter
def is_comment_liked_by_user(comment, user):
    if not user.is_authenticated:
        return False
    return CommentLikeModel.objects.filter(commentID=comment, userID=user).exists()


@register.simple_tag
def reply_comment_like_icon(reply, user):
    return "fa-solid fa-heart" if ReplyCommentLikeModel.objects.filter(reply_commentID=reply, userID=user).exists() else "fa-regular fa-heart"


@register.filter
def is_reply_liked_by_user(reply, user):
    if not user.is_authenticated:
        return False
    return ReplyCommentLikeModel.objects.filter(reply_commentID=reply, userID=user).exists()


@register.filter
def is_liked_by_user(content_object, request):
    return PostLikeModel.objects.filter(postID=content_object, userID=request.user).exists()


@register.simple_tag
def is_reels_liked_by_user(post, user):
    return "fa-solid fa-heart" if PostLikeModel.objects.filter(postID=post,
                                                               userID=user).exists() else "fa-regular fa-heart"


@register.simple_tag
def is_saved_by_user(request, content_object):
    if not hasattr(request, "user") or not hasattr(content_object, "saved"):
        return "fa-regular"

    if not request.user.is_authenticated:
        return "fa-regular"

    return "fa-solid" if request.user in content_object.saved.all() else "fa-regular"



@register.filter
def is_comment_liked_by_user(comment, user):
    if not user.is_authenticated:
        return False
    return CommentLikeModel.objects.filter(commentID=comment, userID=user).exists()


@register.filter
def is_following(request, following_user):
    if not request.user.is_authenticated:
        return False
    return Follow.objects.filter(follower=request.user, following=following_user).exists()


@register.simple_tag
def split_after_second_underscore(room_name, request):
    parts = room_name.split('_')
    if len(parts) > 2:
        if parts[2] == request.user.username:
            return parts[1]
        else:
            return parts[2]
    return room_name

