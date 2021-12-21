import os.path

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404,HttpResponseRedirect,redirect,Http404
from .models import *
from .forms import PostForm
from django.contrib import messages
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import time
# Create your views here.

def post_index(request):
    posts = Post.objects.all().filter(user_id=request.user.id)
    return render(request, 'post/index.html', {'posts': posts})


def post_detail(request,id):
    post = get_object_or_404(Post, id=id)
    postname=str(Post.objects.get(id=id).file).replace('.pdf','').replace('_',' ')
    anatabloinstance=AnaTablo.objects.filter(proje_adi__exact=postname)
    return render(request, 'post/detail.html', {'post': post,'tablolar':anatabloinstance})


def post_create(request):
    if not request.user.is_authenticated:
        raise Http404

    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
       post = form.save(commit=False)
       post.user = request.user
       post.save()
       messages.success(request,'Post başarılı şekilde oluşturuldu')
       for filename, file in request.FILES.items():
           name = request.FILES[filename].name
       functionformining(name)
       return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'post/form.html', context)

def post_update(request,id):
    if not request.user.is_authenticated:
        raise Http404
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None,instance=post)
    if form.is_valid():
       form.save()
       messages.success(request,'Post başarılı şekilde güncellendi')
       return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'post/form.html', context)

def post_delete(request,id):
    if not request.user.is_authenticated:
        raise Http404
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.success(request, 'Post başarılı şekilde silindi',extra_tags='mesaj-basarili')
    return redirect('post:index')

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text
def functionformining(path):

    sayfalar = convert_pdf_to_txt('C:\\Users\\Acer\\Desktop\\yazlab3\\media\\'+str(path)).rsplit('\x0c')
    ####SAYFA1######
    sayfa1 = sayfalar[0]
    sayfa1_1 = sayfa1.splitlines(False)
    Proje_Adi = sayfa1_1[7]
    YazarAdi1 = ""
    YazarAdi2 = ""
    Yazar1Numara = ""
    Yazar2Numara = ""
    Yazar1Ogretim = ""
    Yazar2Ogretim = ""

    if (len(sayfa1_1) == 14):
        YazarAdi1 = sayfa1_1[9]
        Yazar1Numara = sayfa1_1[10]

    else:
        YazarAdi1 = sayfa1_1[9]
        YazarAdi2 = sayfa1_1[10]
        Yazar1Numara = sayfa1_1[12]
        Yazar2Numara = sayfa1_1[13]

    if (Yazar2Numara == ""):
        if (Yazar1Numara[5] == '1'):
            Yazar1Ogretim = '1.Öğretim'
        else:
            Yazar1Ogretim = '2.Öğretim'
    else:
        if (Yazar1Numara[5] == '1'):
            Yazar1Ogretim = '1.Öğretim'
        else:
            Yazar1Ogretim = '2.Öğretim'
        if (Yazar2Numara[5] == '1'):
            Yazar2Ogretim = '1.Öğretim'
        else:
            Yazar2Ogretim = '2.Öğretim'
    ####SAYFA1######
    ####SAYFA2######
    sayfa2 = sayfalar[1]
    sayfa2_2 = sayfa2.splitlines(False)
    Ders_Adi = sayfa2_2[5]
    Danisman_unvan = ""
    Danisman_isim = ""
    Danisman_soyisim = ""
    Juri1_unvan = ""
    Juri1_isim = ""
    Juri1_soyisim = ""
    Juri2_unvan = ""
    Juri2_isim = ""
    Juri2_soyisim = ""
    Teslim_Tarihi = ""
    Teslim_Donemi = ""
    if len(sayfa2_2) != 30:
        Danisman = sayfa2_2[12].split(' ')
        Danisman_unvan = Danisman[0]
        Danisman_isim = Danisman[1]
        Danisman_soyisim = Danisman[2]

        Juri1 = sayfa2_2[14].split(' ')
        Juri1_unvan = Juri1[0]
        Juri1_isim = Juri1[1]
        Juri1_soyisim = Juri1[2]

        Juri2 = sayfa2_2[16].split(' ')
        Juri2_unvan = Juri2[0]
        Juri2_isim = Juri2[1]
        Juri2_soyisim = Juri2[2]
        Teslim_Tarihi = sayfa2_2[25].split(':')[1].lstrip()


    else:
        Danisman = sayfa2_2[15].split(' ')
        Danisman_unvan = Danisman[0]
        Danisman_isim = Danisman[1]
        Danisman_soyisim = Danisman[2]

        Juri1 = sayfa2_2[17].split(' ')
        Juri1_unvan = Juri1[0]
        Juri1_isim = Juri1[1]
        Juri1_soyisim = Juri1[2]

        Juri2 = sayfa2_2[19].split(' ')
        Juri2_unvan = Juri2[0]
        Juri2_isim = Juri2[1]
        Juri2_soyisim = Juri2[2]
        Teslim_Tarihi = sayfa2_2[28].split(':')[1].lstrip()

    if Teslim_Tarihi.lstrip()[4] == '6':
        Teslim_Yılı = Teslim_Tarihi.split('.')[2]
        Teslim_Donemi = str(int(Teslim_Yılı) - 1) + "-" + Teslim_Yılı + ' Bahar'
    else:
        Teslim_Yılı = Teslim_Tarihi.split('.')[2]
        Teslim_Donemi = str(int(Teslim_Yılı) - 1) + "-" + Teslim_Yılı + ' Güz'

    ####SAYFA2######
    ####SAYFA4######
    sayfa4 = sayfalar[3]
    sayfa4_4 = sayfa4.split('ÖZET')
    Ozet = sayfa4_4[1].split('Anahtar kelimeler:')[0]
    AnahtarKelimeler = sayfa4_4[1].split('Anahtar kelimeler:')[1]
    ####SAYFA4######

    try:
        yazar_instance1 = YazarBilgi.objects.get(first_name=YazarAdi1.split(" ")[0],last_name=YazarAdi1.split(" ")[1])
    except ObjectDoesNotExist:
        yazar_instance1 = YazarBilgi()
        yazar_instance1.first_name = YazarAdi1.split(" ")[0]
        yazar_instance1.last_name = YazarAdi1.split(" ")[1]
        yazar_instance1.ogretim_turu = Yazar1Ogretim
        yazar_instance1.save()

    try:
        danisman_instance=DanismanBilgi.objects.get(first_name=Danisman_isim,last_name=Danisman_soyisim)
    except ObjectDoesNotExist:
        danisman_instance = DanismanBilgi()
        danisman_instance.first_name = Danisman_isim
        danisman_instance.last_name = Danisman_soyisim
        danisman_instance.unvan = Danisman_unvan
        danisman_instance.save()

    try:
        juri_istancane1 =JuriBilgi.objects.get(first_name=Juri1_isim,last_name=Juri1_soyisim)
    except ObjectDoesNotExist:
        juri_istancane1 = JuriBilgi()
        juri_istancane1.first_name = Juri1_isim
        juri_istancane1.last_name = Juri1_soyisim
        juri_istancane1.unvan = Juri1_unvan
        juri_istancane1.save()
    try:
        juri_istancane2=JuriBilgi.objects.get(first_name=Juri2_isim,last_name=Juri2_soyisim)
    except ObjectDoesNotExist:
        juri_istancane2 = JuriBilgi()
        juri_istancane2.first_name = Juri2_isim
        juri_istancane2.last_name = Juri2_soyisim
        juri_istancane2.unvan = Juri2_unvan
        juri_istancane2.save()

    if YazarAdi2 != "":
        try:
            yazar_instance2=YazarBilgi.objects.get(first_name=YazarAdi2.split(" ")[0], last_name=YazarAdi2.split(" ")[1])
        except ObjectDoesNotExist:
            yazar_instance2 = YazarBilgi()
            yazar_instance2.first_name = YazarAdi2.split(" ")[0]
            yazar_instance2.last_name = YazarAdi2.split(" ")[1]
            yazar_instance2.ogretim_turu = Yazar2Ogretim
            yazar_instance2.save()


    if YazarAdi2 != "":
        for i in range(2):
            for j in range(2):
                for x in AnahtarKelimeler.split(','):
                    if j ==0 and i==0:
                        main_table_istance = AnaTablo()
                        main_table_istance.ders_adi = Ders_Adi
                        main_table_istance.proje_adi = Proje_Adi
                        main_table_istance.teslim_donemi = Teslim_Donemi
                        main_table_istance.danisman_bilgi = danisman_instance
                        main_table_istance.ozet = Ozet
                        main_table_istance.yazar_bilgi = yazar_instance1
                        main_table_istance.juri_bilgi = juri_istancane1
                        main_table_istance.anahtar= x
                        main_table_istance.save()
                    elif j ==1 and i==0:
                        main_table_istance = AnaTablo()
                        main_table_istance.ders_adi = Ders_Adi
                        main_table_istance.proje_adi = Proje_Adi
                        main_table_istance.teslim_donemi = Teslim_Donemi
                        main_table_istance.danisman_bilgi = danisman_instance
                        main_table_istance.ozet = Ozet
                        main_table_istance.yazar_bilgi = yazar_instance1
                        main_table_istance.juri_bilgi = juri_istancane2
                        main_table_istance.anahtar= x
                        main_table_istance.save()

                    elif j ==0 and i==1:
                        main_table_istance = AnaTablo()
                        main_table_istance.ders_adi = Ders_Adi
                        main_table_istance.proje_adi = Proje_Adi
                        main_table_istance.teslim_donemi = Teslim_Donemi
                        main_table_istance.danisman_bilgi = danisman_instance
                        main_table_istance.ozet = Ozet
                        main_table_istance.yazar_bilgi = yazar_instance2
                        main_table_istance.juri_bilgi = juri_istancane1
                        main_table_istance.anahtar= x
                        main_table_istance.save()

                    elif j == 1 and i == 1:
                        main_table_istance = AnaTablo()
                        main_table_istance.ders_adi = Ders_Adi
                        main_table_istance.proje_adi = Proje_Adi
                        main_table_istance.teslim_donemi = Teslim_Donemi
                        main_table_istance.danisman_bilgi = danisman_instance
                        main_table_istance.ozet = Ozet
                        main_table_istance.yazar_bilgi = yazar_instance2
                        main_table_istance.juri_bilgi = juri_istancane2
                        main_table_istance.anahtar= x
                        main_table_istance.save()
    else:
        for j in range(2):
            for x in AnahtarKelimeler.split(','):
                if j == 0:
                    main_table_istance = AnaTablo()
                    main_table_istance.ders_adi = Ders_Adi
                    main_table_istance.proje_adi = Proje_Adi
                    main_table_istance.teslim_donemi = Teslim_Donemi
                    main_table_istance.danisman_bilgi = danisman_instance
                    main_table_istance.ozet = Ozet
                    main_table_istance.yazar_bilgi = yazar_instance1
                    main_table_istance.juri_bilgi = juri_istancane1
                    main_table_istance.anahtar = x
                    main_table_istance.save()
                elif j == 1:
                    main_table_istance = AnaTablo()
                    main_table_istance.ders_adi = Ders_Adi
                    main_table_istance.proje_adi = Proje_Adi
                    main_table_istance.teslim_donemi = Teslim_Donemi
                    main_table_istance.danisman_bilgi = danisman_instance
                    main_table_istance.ozet = Ozet
                    main_table_istance.yazar_bilgi = yazar_instance1
                    main_table_istance.juri_bilgi = juri_istancane2
                    main_table_istance.anahtar = x
                    main_table_istance.save()



