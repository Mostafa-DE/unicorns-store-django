from random import randrange


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{randrange(0, 1000, 2)}".lower()
    return unique_slug
