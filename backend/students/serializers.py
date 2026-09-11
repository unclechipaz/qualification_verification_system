from rest_framework import serializers
from verification.utils import mask_national_id
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id', 'student_number', 'national_id', 'full_name',
            'programme', 'faculty', 'level', 'graduation_date',
            'qualification', 'degree_classification', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'national_id' in data and data['national_id']:
            data['national_id'] = mask_national_id(data['national_id'])
        return data

