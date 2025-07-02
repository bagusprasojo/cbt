from rest_framework import serializers
from .models import Soal, PaketSoal, Jawaban

class SoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soal
        exclude = ['jawaban_benar']  # jangan bocorkan jawabannya


class PaketSoalSerializer(serializers.ModelSerializer):
    soal = SoalSerializer(many=True, read_only=True)
    class Meta:
        model = PaketSoal
        fields = '__all__'

class JawabanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jawaban
        fields = ['id', 'peserta', 'soal', 'jawaban', 'waktu_submit']
        read_only_fields = ['waktu_submit']


class PaketSoalDetailSerializer(serializers.ModelSerializer):
    soal = SoalSerializer(many=True, read_only=True)

    class Meta:
        model = PaketSoal
        fields = ['id', 'nama', 'waktu_menit', 'soal']

