from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


def menu_blog_links(request):
    blog_links = Category.objects.all()
    return dict(blog_links=blog_links)
