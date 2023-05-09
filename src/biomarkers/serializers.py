from rest_framework import serializers
from feature_selection.models import TrainedModel
from .models import Biomarker, MRNAIdentifier, MethylationIdentifier, CNAIdentifier, MiRNAIdentifier
from tags.serializers import TagSerializer
from drf_writable_nested import WritableNestedModelSerializer

class MRNAIdentifierSerializer(serializers.ModelSerializer):
    """MRNAIdentifier serializer"""

    class Meta:
        model = MRNAIdentifier
        exclude = ['biomarker']

class MiRNAIdentifierSerializer(serializers.ModelSerializer):
    """MiRNAIdentifier serializer"""

    class Meta:
        model = MiRNAIdentifier
        exclude = ['biomarker']

class CNAIdentifierSerializer(serializers.ModelSerializer):
    """CNAIdentifier serializer"""

    class Meta:
        model = CNAIdentifier
        exclude = ['biomarker']

class MethylationIdentifierSerializer(serializers.ModelSerializer):
    """MethylationIdentifier serializer"""

    class Meta:
        model = MethylationIdentifier
        exclude = ['biomarker']


class BiomarkerSerializer(WritableNestedModelSerializer):
    """Biomarker model serializer"""
    number_of_mrnas = serializers.SerializerMethodField(method_name='get_number_of_mrnas')
    number_of_mirnas = serializers.SerializerMethodField(method_name='get_number_of_mirnas')
    number_of_cnas = serializers.SerializerMethodField(method_name='get_number_of_cnas')
    number_of_methylations = serializers.SerializerMethodField(method_name='get_number_of_methylations')
    has_fs_experiment = serializers.SerializerMethodField(method_name='get_has_fs_experiment')

    mrnas = MRNAIdentifierSerializer(many=True, required=False)
    mirnas = MiRNAIdentifierSerializer(many=True, required=False)
    cnas = CNAIdentifierSerializer(many=True, required=False)
    methylations = MethylationIdentifierSerializer(many=True, required=False)
    origin = serializers.IntegerField(required=False)
    state = serializers.IntegerField(required=False)

    tag = TagSerializer(required=False)

    class Meta:
        model = Biomarker
        exclude = ['user']

    @staticmethod
    def get_number_of_mrnas(ins: Biomarker) -> int:
        """Gets the number of genes in this Biomarker"""
        return ins.number_of_mrnas

    @staticmethod
    def get_number_of_mirnas(ins: Biomarker) -> int:
        """Gets the number of miRNAs in this Biomarker"""
        return ins.number_of_mirnas

    @staticmethod
    def get_number_of_cnas(ins: Biomarker) -> int:
        """Gets the number of CNAs in this Biomarker"""
        return ins.number_of_cnas

    @staticmethod
    def get_number_of_methylations(ins: Biomarker) -> int:
        """Gets the number of Methylations in this Biomarker"""
        return ins.number_of_methylations

    @staticmethod
    def get_has_fs_experiment(ins: Biomarker) -> bool:
        """Gets if the current Biomarker was created from a Feature Selection experiment"""
        return ins.has_fs_experiment


class TrainedModelSerializer(serializers.ModelSerializer):
    """TrainedModel serializer"""

    class Meta:
        model = TrainedModel
        fields = ['id', 'name', 'fitness_function', 'description', 'state', 'created', 'best_fitness_value']
