from django.urls import path, include
from rest_framework.routers import DefaultRouter
from adminpanel.views import PaketSoalViewSet, JawabanSubmitView, ambil_soal_peserta

router = DefaultRouter()
router.register(r'paket', PaketSoalViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('jawaban/', JawabanSubmitView.as_view(), name='submit_jawaban'),
    path('peserta/soal/', ambil_soal_peserta),

]
