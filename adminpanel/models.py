from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('peserta', 'Peserta'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='peserta')
    kelas = models.CharField(max_length=50, blank=True, null=True)

class PaketSoal(models.Model):
    nama = models.CharField(max_length=100)
    waktu_menit = models.PositiveIntegerField()

    def __str__(self):
        return self.nama

class Soal(models.Model):
    paket = models.ForeignKey(PaketSoal, on_delete=models.CASCADE, related_name='soal')
    teks = RichTextUploadingField()
    pilihan_a = models.CharField(max_length=255)
    pilihan_b = models.CharField(max_length=255)
    pilihan_c = models.CharField(max_length=255)
    pilihan_d = models.CharField(max_length=255)
    jawaban_benar = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

class Jawaban(models.Model):
    peserta = models.ForeignKey('User', on_delete=models.CASCADE)
    soal = models.ForeignKey('Soal', on_delete=models.CASCADE)
    jawaban = models.CharField(max_length=1)
    waktu_submit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.peserta.username} - {self.soal.id} = {self.jawaban}"
    
class PesertaPaket(models.Model):
    peserta = models.ForeignKey(User, on_delete=models.CASCADE)
    paket = models.ForeignKey(PaketSoal, on_delete=models.CASCADE)
    waktu_mulai = models.DateTimeField(null=True, blank=True)
    sudah_selesai = models.BooleanField(default=False)

class PesertaSoalUrutan(models.Model):
    peserta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paket = models.ForeignKey(PaketSoal, on_delete=models.CASCADE)
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE)
    urutan = models.PositiveIntegerField()

    class Meta:
        unique_together = ('peserta', 'urutan')
        ordering = ['urutan']

    def __str__(self):
        return f"{self.peserta.username} - Soal {self.urutan}"



