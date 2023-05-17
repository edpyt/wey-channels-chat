from django.http import HttpResponse
from django.core.exceptions import ValidationError

from account.models import User


def activateemail(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    try:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()

        message = ('The user is now activated.'
                   ' You can go ahead and log in!')
    except ValidationError:
        message = 'The parameters is not valid!'

    return HttpResponse(message)
