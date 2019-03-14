from django import template

register = template.Library()


@register.filter
def truncate(paginator, number):
    """
    :param paginator: paginator.num_pages
    :param number: current page number
    :return: pages range to show
    """
    if number < 5:
        truncated_paginator = range(1, min(paginator + 1, number + 3))
    elif 4 < number < (paginator - 3):
        truncated_paginator = range(number - 3, number + 3)
    else:
        truncated_paginator = range(number - 3, paginator + 1)
    return truncated_paginator
