from django.contrib import admin
from .models import User, PaketSoal, Soal, Jawaban, PesertaPaket
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "kelas")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "kelas")

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "email", "kelas", "is_staff", "is_active"]
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Pribadi', {'fields': ('first_name','last_name', 'email', 'kelas')}),
        ('Hak Akses', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Tanggal Penting', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name','last_name', 'kelas', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


class PaketSoalAdmin(admin.ModelAdmin):
    list_display = ('nama', 'waktu_menit')
    search_fields = ('nama',)   

class SoalAdmin(admin.ModelAdmin): 
    list_display = ('paket', 'teks', 'jawaban_benar')
    search_fields = ('teks',)
    list_filter = ('paket',)

class JawabanAdmin(admin.ModelAdmin):
    list_display = ('peserta', 'soal', 'jawaban', 'waktu_submit')
    search_fields = ('peserta__username', 'soal__teks')
    list_filter = ('peserta', 'soal')   

@admin.register(PesertaPaket)
class PesertaPaketAdmin(admin.ModelAdmin):
    list_display = ['peserta', 'paket', 'waktu_mulai', 'sudah_selesai']


admin.site.register(Jawaban, JawabanAdmin)
admin.site.register(User, CustomUserAdmin)

admin.site.register(PaketSoal, PaketSoalAdmin)
admin.site.register(Soal, SoalAdmin)

