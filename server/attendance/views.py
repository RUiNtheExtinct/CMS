from datetime import datetime
from users.models import Branch
from django.shortcuts import render
from django.utils.translation import override
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from attendance.serializers import AttendanceSerializer, IssueSerializer
from attendance.models import Attendance, Issue
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

# from vendors.models import Gunmen
# from vendors.serializers import GunmenSerializer


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "page_size": self.page_size,
                "results": data,
            }
        )


class AttendanceList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["^gunmen__first_name", "^gunmen__last_name"]
    filterset_fields = ["gunmen", "branch"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        new_attendance = AttendanceSerializer(data=request.data)
        if new_attendance.is_valid():
            today = datetime.now()
            attendance = Attendance.objects.filter(
                entry_time__year=today.date().year,
                entry_time__month=today.date().month,
                entry_time__day=today.date().day,
                gunmen=new_attendance.data["gunmen"]["id"],
                branch=new_attendance.data["branch"]["id"],
            ).first()

            if attendance:
                attendance.entry_time = today
                if "exit_time" in new_attendance.data:
                    attendance.exit_time = new_attendance.data.get("exit_time")
                attendance.save()
                return Response(data=AttendanceSerializer(attendance).data)
            else:
                return self.create(request, *args, **kwargs)


class AttendanceDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class IssueList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class IssueDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
