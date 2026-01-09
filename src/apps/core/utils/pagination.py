from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "message": "OK",
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "pagination": {
                "current_page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "page_size": self.get_page_size(self.request),
                "total_items": self.page.paginator.count,
            },
            "data": data,
        })

    def get_paginated_response_schema(self, schema):
        """
        Override this method to provide custom schema for drf-spectacular
        """
        return {
            'data': {
                'type': 'array',
                'items': schema,
            },
        }