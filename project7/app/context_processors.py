from .models import  Sub_Cat,Category, FacebookPost

def custom_context(request):

    categories = Category.objects.all()
    size = len(Sub_Cat.objects.all())
    fb_post = FacebookPost.objects.all().order_by('-date')[:5]
    print(fb_post)

    context = {
        'categories': categories,
        'rang':range(size),
        'fb_post':fb_post,

    }
    return context

