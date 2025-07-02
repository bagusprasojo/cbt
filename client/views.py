from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from adminpanel.models import PesertaPaket, Soal, Jawaban, PesertaSoalUrutan
import random
from django.utils.timezone import now

import random
from adminpanel.models import PesertaSoalUrutan



@login_required
def tinjau_soal(request):
    try:
        peserta_paket = PesertaPaket.objects.get(peserta=request.user, sudah_selesai=False)
    except PesertaPaket.DoesNotExist:
        return redirect('ujian')

    urutan_soal = PesertaSoalUrutan.objects.filter(
        peserta=request.user,
        paket=peserta_paket.paket
    ).select_related('soal')

    jawaban_dict = {}
    jawaban_qs = Jawaban.objects.filter(peserta=request.user).select_related('soal')
    for j in jawaban_qs:
        opsi = j.jawaban  # misal: 'B'
        soal = j.soal
        teks = getattr(soal, f'pilihan_{opsi.lower()}', '(pilihan tidak ditemukan)')
        jawaban_dict[soal.id] = {
            'huruf': opsi,
            'teks': teks,
        }

    # print("Jawaban Dictionary:", jawaban_dict)
    semua_terjawab = all(soal.soal.id in jawaban_dict for soal in urutan_soal)

    if request.method == "POST" and semua_terjawab:
        peserta_paket.sudah_selesai = True
        peserta_paket.save()
        return redirect('hasil_ujian')

    return render(request, 'client/tinjau.html', {
        'urutan_soal': urutan_soal,
        'jawaban_dict': jawaban_dict,
        'semua_terjawab': semua_terjawab,
    })

@login_required
def ujian(request):
    try:
        peserta_paket = PesertaPaket.objects.get(peserta=request.user, sudah_selesai=False)
    except PesertaPaket.DoesNotExist:
        return render(request, 'client/ujian.html', {'error': 'Anda belum mendapatkan paket soal.'})

    # Cek apakah sudah diacak
    
    urutan_soal = PesertaSoalUrutan.objects.filter(peserta=request.user, paket=peserta_paket.paket)
    if not urutan_soal.exists():
        soal_ids = list(peserta_paket.paket.soal.values_list('id', flat=True))
        random.shuffle(soal_ids)
        for idx, soal_id in enumerate(soal_ids, start=1):
            PesertaSoalUrutan.objects.create(
                peserta=request.user,
                paket=peserta_paket.paket,
                soal_id=soal_id,
                urutan=idx
            )
        urutan_soal = PesertaSoalUrutan.objects.filter(peserta=request.user, paket=peserta_paket.paket)

    total_soal = urutan_soal.count()
    nomor = int(request.GET.get('nomor', 1))
    nomor = max(1, min(nomor, total_soal))

    urutan_soal_obj = urutan_soal.get(urutan=nomor)
    current_soal = urutan_soal_obj.soal

    if request.method == 'POST':
        jawaban_user = request.POST.get('jawaban')
        if jawaban_user:
            Jawaban.objects.update_or_create(
                peserta=request.user,
                soal=current_soal,
                defaults={'jawaban': jawaban_user}
            )

            if (nomor == total_soal):
                return redirect(f'/tinjau')    
            else:
                next_nomor = nomor + 1
                return redirect(f'/ujian/?nomor={next_nomor}')

        if 'kumpulkan' in request.POST:
            peserta_paket.sudah_selesai = True
            peserta_paket.save()
            return redirect('hasil_ujian')
        else:
            next_nomor = nomor + 1 if 'selanjutnya' in request.POST else nomor - 1
            return redirect(f'/ujian/?nomor={next_nomor}')

    existing_jawaban = Jawaban.objects.filter(peserta=request.user, soal=current_soal).first()
    
    opsi_dict = {}
    for kode in ['A', 'B', 'C', 'D']:
        field = f"pilihan_{kode.lower()}"
        opsi_dict[kode] = getattr(current_soal, field)

    return render(request, 'client/ujian.html', {
        'ujian': peserta_paket.paket,
        'soal': current_soal,
        'nomor': nomor,
        'total': total_soal,
        'jawaban': existing_jawaban.jawaban if existing_jawaban else '',
        'opsi_dict': opsi_dict,
    })




@login_required
def hasil(request):
    jawaban_qs = Jawaban.objects.filter(peserta=request.user).select_related('soal')
    jumlah_benar = sum(1 for j in jawaban_qs if j.jawaban == j.soal.jawaban_benar)

    return render(request, 'client/hasil.html', {
        'jawaban': jawaban_qs,
        'jumlah_benar': jumlah_benar,
        'jumlah_total': jawaban_qs.count()
    })

