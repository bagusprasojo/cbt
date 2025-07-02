from rest_framework import viewsets
from .models import PaketSoal, PesertaPaket
from .serializers import PaketSoalSerializer, JawabanSerializer, PaketSoalDetailSerializer, SoalSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, views
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ambil_soal_peserta(request):
    try:
        entry = PesertaPaket.objects.select_related('paket').get(peserta=request.user, sudah_selesai=False)
        serializer = PaketSoalDetailSerializer(entry.paket)
        return Response(serializer.data)
    except PesertaPaket.DoesNotExist:
        return Response({"error": "Tidak ada paket soal untuk Anda."}, status=404)
    
class PaketSoalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaketSoal.objects.all()
    serializer_class = PaketSoalSerializer
    permission_classes = [IsAuthenticated]

class JawabanSubmitView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        # Jika data adalah list (submit banyak)
        if isinstance(data, list):
            for jawaban in data:
                jawaban['peserta'] = request.user.id
            serializer = JawabanSerializer(data=data, many=True)
        else:
            data['peserta'] = request.user.id
            serializer = JawabanSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Jawaban berhasil disimpan'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
