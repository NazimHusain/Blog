from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from typing import Optional, Any


def paginator(
    queryset: "QuerySet", page_num: Optional[int] = 1, page_size: Optional[int] = 5
) -> Any:
    paginator = Paginator(queryset, page_size)
    return paginator.get_page(page_num)


class ApiPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"

    def get_paginated_response(self: "ApiPaginator", data: Any) -> dict:
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


