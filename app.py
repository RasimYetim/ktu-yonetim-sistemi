from crypt import methods

from flask import Flask, render_template, request, redirect, url_for
from models import db, Ogrenci, PC, Dersler
from config import Config
from models import db, Akademisyen, Yonetici
from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pc_ekle', methods=['GET', 'POST'])
def pc_ekle():
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz giriş.")
        return redirect(url_for('ygiris'))

    if request.method == 'POST':
        baslik = request.form['baslik']
        aciklama = request.form['aciklama']

        yeni_pc = PC(baslik=baslik, aciklama=aciklama)
        db.session.add(yeni_pc)
        db.session.commit()
        flash("Program Çıktısı başarıyla eklendi.")
        return redirect(url_for('pc_ekle'))

    pc_listesi = PC.query.all()
    return render_template('pc_ekle.html', pc_listesi=pc_listesi)

@app.route('/agiris', methods=['GET', 'POST'])
def agiris():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Akademisyen.query.filter_by(kullanici_adi=username, sifre=password).first()
        if user:
            session['kullanici_adi'] = user.kullanici_adi
            session['rol'] = 'akademisyen'
            return render_template('amenu.html')
        else:
            flash('Kullanıcı adı veya şifre hatalı')
    return render_template('agiris.html')

@app.route('/ygiris', methods=['GET', 'POST'])
def ygiris():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Yonetici.query.filter_by(kullanici_adi=username, sifre=password).first()
        if user:
            session['kullanici_adi'] = user.kullanici_adi
            session['rol'] = 'yonetici'
            return render_template('ymenu.html')
        else:
            flash('Yönetici giriş bilgileri hatalı')
    return render_template('ygiris.html')
@app.route('/yoneticiekle')
def yoneticiekle():
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz erişim.")
        return redirect(url_for('ygiris'))

    yoneticiler = Yonetici.query.all()
    return render_template('yoneticiekle.html', yoneticiler=yoneticiler)


@app.route('/akademisyenekle')
def akademisyenekle():
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz erişim.")
        return redirect(url_for('ygiris'))

    akademisyenler = Akademisyen.query.all()
    return render_template('akademisyenekle.html', akademisyenler=akademisyenler)

@app.route('/raporlar')
def raporlar():
    return render_template('raporlar.html')
@app.route('/pc_ekle')
def pcekle():
    return render_template('pc_ekle.html')
@app.route('/akademisyen-ekle', methods=['POST'])
def akademisyen_ekle():
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz giriş.")
        return redirect(url_for('ygiris'))

    adSoyad = request.form['adSoyad']
    kullanici_adi = request.form['kullanici_adi']
    sifre = request.form['sifre']
    title = request.form['title']

    # Kullanıcı adı var mı kontrolü
    varsa = Akademisyen.query.filter_by(kullanici_adi=kullanici_adi).first()
    if varsa:
        flash("Bu kullanıcı adı zaten akademisyen olarak kayıtlı.")
        return redirect(url_for('akademisyenekle'))

    yeni = Akademisyen(adSoyad=adSoyad, kullanici_adi=kullanici_adi, sifre=sifre, title=title)
    db.session.add(yeni)
    db.session.commit()
    flash("Akademisyen başarıyla eklendi.")
    return redirect(url_for('akademisyenekle'))
@app.route('/yonetici-ekle', methods=['POST'])
def yonetici_ekle():
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz giriş.")
        return redirect(url_for('ygiris'))

    AdSoyad = request.form['AdSoyad']
    kullanici_adi = request.form['kullanici_adi']
    sifre = request.form['sifre']

    # Kullanıcı adı kontrolü
    varsa = Yonetici.query.filter_by(kullanici_adi=kullanici_adi).first()
    if varsa:
        flash("Bu kullanıcı adı zaten yönetici olarak kayıtlı.")
        return redirect(url_for('yoneticiekle'))

    yeni = Yonetici(AdSoyad=AdSoyad, kullanici_adi=kullanici_adi, sifre=sifre)
    db.session.add(yeni)
    db.session.commit()
    flash("Yönetici başarıyla eklendi.")
    return redirect(url_for('yoneticiekle'))

@app.route('/akademisyen-sil/<int:aID>', methods=['POST'])
def akademisyen_sil(aID):
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz erişim.")
        return redirect(url_for('ygiris'))

    akademisyen = Akademisyen.query.get(aID)
    if akademisyen:
        db.session.delete(akademisyen)
        db.session.commit()
        flash("Akademisyen silindi.")
    else:
        flash("Akademisyen bulunamadı.")
    return redirect(url_for('akademisyenekle'))
@app.route('/yonetici-sil/<int:yID>', methods=['POST'])
def yonetici_sil(yID):
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz erişim.")
        return redirect(url_for('ygiris'))

    yonetici = Yonetici.query.get(yID)

    # Admin kendi kendini silmeye çalışıyorsa engelle
    if yonetici and yonetici.kullanici_adi == session['kullanici_adi']:
        flash("Kendi hesabınızı silemezsiniz.")
        return redirect(url_for('yoneticiekle'))

    if yonetici:
        db.session.delete(yonetici)
        db.session.commit()
        flash("Yönetici silindi.")
    else:
        flash("Yönetici bulunamadı.")
    return redirect(url_for('yoneticiekle'))
@app.route('/pc_sil/<int:pcID>', methods=['POST'])
def pc_sil(pcID):
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz işlem.")
        return redirect(url_for('ygiris'))

    pc = PC.query.get(pcID)
    if pc:
        db.session.delete(pc)
        db.session.commit()
        flash("Program çıktısı silindi.")
    else:
        flash("Program çıktısı bulunamadı.")
    return redirect(url_for('pc_ekle'))
@app.route('/dersekle', methods=['GET', 'POST'])
def dersekle():
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz erişim.")
        return redirect(url_for('ygiris'))

    dersler = Dersler.query.all()
    akademisyenler = Akademisyen.query.all()
    return render_template('ders_ekle.html', dersler=dersler, akademisyenler=akademisyenler)


@app.route('/ders_ekle', methods=['GET', 'POST'])
def ders_ekle():
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz erişim.")
        return redirect(url_for('ygiris'))

    if request.method == 'POST':
        dersAd = request.form.get('dersAd')
        bolum = request.form.get('bolum')
        sorumluID = request.form.get('sorumluID')

        if not dersAd or not bolum or not sorumluID:
            flash("Tüm alanları doldurmanız gerekiyor.")
            return redirect(url_for('ders_ekle'))

        try:
            sorumluID = int(sorumluID)
            yeni_ders = Dersler(dersAd=dersAd, bolum=bolum, sorumluID=sorumluID)
            db.session.add(yeni_ders)
            db.session.commit()
            flash("Ders başarıyla eklendi.")
        except Exception as e:
            flash(f"Hata oluştu: {str(e)}")

        return redirect(url_for('ders_ekle'))

    dersler = Dersler.query.all()
    akademisyenler = Akademisyen.query.all()
    return render_template('ders_ekle.html', dersler=dersler, akademisyenler=akademisyenler)

@app.route('/ders_sil/<int:dID>', methods=['POST'])
def ders_sil(dID):
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz işlem.")
        return redirect(url_for('ygiris'))

    ders = Dersler.query.get(dID)
    if ders:
        db.session.delete(ders)
        db.session.commit()
        flash("Ders silindi.")
    else:
        flash("Ders bulunamadı.")
    return redirect(url_for('dersekle'))

@app.route('/pciliski')
def pciliski():
    return render_template('pciliski.html')


@app.route('/ogrekle', methods=['GET', 'POST'])
def ogrekle():
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz giriş.")
        return redirect(url_for('ygiris'))

    if request.method == 'POST':
        adSoyad = request.form.get('adSoyad')
        bolum = request.form.get('bolum')

        if not adSoyad or not bolum:
            flash("Tüm alanları doldurun.")
            return redirect(url_for('ogrekle'))

        try:
            ogrenci = Ogrenci(adSoyad=adSoyad, bolum=bolum)
            db.session.add(ogrenci)
            db.session.commit()
            flash("Öğrenci başarıyla eklendi.")
        except Exception as e:
            flash(f"Hata oluştu: {e}")

        return redirect(url_for('ogrekle'))

    ogrenciler = Ogrenci.query.all()
    return render_template('ogrekle.html', ogrenciler=ogrenciler)
@app.route('/ogrenci-sil/<int:ogrID>', methods=['POST'])
def ogrenci_sil(ogrID):
    if 'rol' not in session or session['rol'] != 'yonetici':
        flash("Yetkisiz işlem.")
        return redirect(url_for('ygiris'))

    ogr = Ogrenci.query.get(ogrID)
    if ogr:
        db.session.delete(ogr)
        db.session.commit()
        flash("Öğrenci silindi.")
    else:
        flash("Öğrenci bulunamadı.")
    return redirect(url_for('ogrekle'))
