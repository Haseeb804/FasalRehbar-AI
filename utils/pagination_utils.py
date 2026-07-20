"""
Pagination utilities.
"""

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(queryset, page, per_page=10):
    """
    Paginate a queryset.
    
    Args:
        queryset: Django queryset
        page: Page number
        per_page: Items per page
    
    Returns:
        Tuple of (paginated_items, paginator, page_obj)
    """
    paginator = Paginator(queryset, per_page)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj.object_list, paginator, page_obj
