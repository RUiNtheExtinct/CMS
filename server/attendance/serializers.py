from datetime import date
from vendors.models import Vehicle
from vendors.serializers import CustodianSerializer, VehicleSerializer
from vendors.models import Vendor
from django.contrib.auth.models import User
from users.models import Branch
from vendors.models import Gunmen, Custodian
from django.db.models import fields
from rest_framework import serializers
from users.serializers import BranchSerializer, UserSerializer
from vendors.serializers import VendorSerializer, GunmenSerializer
from .models import Attendance, AttendanceSheet, Issue, Trip


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop("serializer", None)
        if self.serializer is not None and not issubclass(
            self.serializer, serializers.Serializer
        ):
            raise TypeError('"serializer" is not a valid serializer class')
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)


class AttendanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSheet
        fields = ["id", "sheet_created", "invoice", "verified"]


class AttendanceSerializer(serializers.ModelSerializer):
    gunmen = RelatedFieldAlternative(
        queryset=Gunmen.objects.all(), serializer=GunmenSerializer
    )
    attendance_sheet = RelatedFieldAlternative(
        queryset=AttendanceSheet.objects.all(), serializer=AttendanceSheetSerializer
    )
    branch = RelatedFieldAlternative(
        queryset=Branch.objects.all(), serializer=BranchSerializer
    )
    added_by = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "gunmen",
            "entry_time",
            "exit_time",
            "branch",
            "added_by",
            "attendance_sheet",
        ]


class TripSerializer(serializers.ModelSerializer):
    vehicle = RelatedFieldAlternative(
        queryset=Vehicle.objects.all(), serializer=VehicleSerializer
    )
    custodian_1 = RelatedFieldAlternative(
        queryset=Custodian.objects.all(), serializer=CustodianSerializer
    )
    custodian_2 = RelatedFieldAlternative(
        queryset=Custodian.objects.all(), serializer=CustodianSerializer
    )
    custodian_3 = RelatedFieldAlternative(
        queryset=Custodian.objects.all(), serializer=CustodianSerializer
    )
    branch = RelatedFieldAlternative(
        queryset=Branch.objects.all(), serializer=BranchSerializer
    )
    added_by = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "vehicle",
            "custodian_1",
            "custodian_2",
            "custodian_3",
            "entry_time",
            "exit_time",
            "start_location",
            "end_location",
            "branch",
            "added_by",
        ]


class IssueSerializer(serializers.ModelSerializer):
    reverted_by = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer
    )
    vendor = RelatedFieldAlternative(
        queryset=Vendor.objects.all(), serializer=VendorSerializer
    )
    sheet = RelatedFieldAlternative(
        queryset=AttendanceSheet.objects.all(), serializer=AttendanceSheetSerializer
    )

    class Meta:
        model = Issue
        fields = ["id", "comment", "reverted_by", "vendor", "sheet", "created_at"]
