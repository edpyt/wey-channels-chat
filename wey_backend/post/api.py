from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer

from .forms import PostForm, AttachmentForm
from .models import Comment, Like, Post, Trend
from .serializers import (
    CommentSerializer,
    PostDetailSerializer,
    PostSerializer,
    TrendSerializer,
)


def user_friends(user):
    user_ids = [user.id for user in user.friends.all()]
    return user_ids


@api_view(['GET'])
def post_list(request):
    user_ids = user_friends(request.user)
    user_ids.append(request.user.id)
    posts = Post.objects.filter()

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend)\
            .filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    user_ids = user_friends(request.user)

    user_ids.append(request.user.id)

    post = Post.objects.filter(
        Q(created_by_id__in=user_ids) | Q(is_private=False)
    ).get(pk=pk)

    return JsonResponse({'post': PostDetailSerializer(post).data})


@api_view(['GET'])
def post_list_profile(request, id):
    user_ids = user_friends(request.user)

    user = User.objects.get(pk=id)

    posts = Post.objects.filter(created_by__id=id)

    if request.user not in user.friends.all() and\
            request.user.id != id:
        posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(
        created_by=user
    )
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(
        created_by=request.user
    )

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse(
        {
            'posts': posts_serializer.data,
            'user': user_serializer.data,
            'can_send_friendship_request': can_send_friendship_request,
        },
        safe=False,
    )


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user

        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count += 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({'error': 'add something here later'})


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.likes.filter(created_by=request.user).exists():
        like = Like.objects.create(created_by=request.user)
        post = Post.objects.get(pk=pk)
        post.likes_count += 1
        post.likes.add(like)
        post.save()

        return JsonResponse({'message': 'like created'})
    return JsonResponse({'message': 'post already liked'})


@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(
        body=request.data.get('body'), created_by=request.user
    )

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user)\
                       .get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})


@api_view(['POST'])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()
    return JsonResponse({'message': 'post reported'})


@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)
