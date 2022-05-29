from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def get_page_range(p, number, on_each_side=1, on_ends=1):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(
        number=number, on_each_side=on_each_side, on_ends=on_ends
    )


@register.simple_tag
def proper_paginate(paginator, current_page, limit=5):
    total_pages = paginator.num_pages
    start_page = int((current_page - 1) // limit) * limit
    last_page = min(start_page + limit, total_pages)
    return range(start_page + 1, last_page + 1)
