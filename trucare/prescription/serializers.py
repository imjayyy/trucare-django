from .models import PrimaryDrug, SecondaryDrug, PrescribeAbleItem, PrescriptionItem, Prescription
from rest_framework import serializers


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'




class PrescribeAbleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescribeAbleItem
        fields = '__all__'


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = '__all__'

class PrimaryDrugSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer(read_only=True)
    drug = PrescribeAbleItemSerializer(read_only=True)
    class Meta:
        model = PrimaryDrug
        fields = '__all__'



class SecondaryDrugSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer(read_only=True)
    drug = PrescribeAbleItemSerializer(read_only=True)
    
    class Meta:
        model = SecondaryDrug
        fields = '__all__'
