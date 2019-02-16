import random
import string

from pytils.translit import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(inst, new_slug=None):

    slug = new_slug if new_slug else slugify(inst.title)

    if slug.isdigit():
        slug += '_'

    model = inst.__class__
    qs_exists = model.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"

        return unique_slug_generator(inst, new_slug=new_slug)

    return slug
