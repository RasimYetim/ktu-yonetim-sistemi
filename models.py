from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Akademisyen(db.Model):
    __tablename__ = 'akademisyen'
    aID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adSoyad = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    sifre = db.Column(db.String, nullable=False)
    kullanici_adi = db.Column(db.String, nullable=False, unique=True)

    dersler = db.relationship('Dersler', backref='sorumlu', lazy=True)

class Yonetici(db.Model):
    __tablename__ = 'yonetici'
    yID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AdSoyad = db.Column(db.String, nullable=False)
    kullanici_adi = db.Column(db.String, nullable=False, unique=True)
    sifre = db.Column(db.String, nullable=False)

class Ogrenci(db.Model):
    __tablename__ = 'ogrenci'
    ogrID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adSoyad = db.Column(db.String, nullable=False)
    bolum = db.Column(db.String, nullable=False)

class Dersler(db.Model):
    __tablename__ = 'dersler'
    dID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dersAd = db.Column(db.String, nullable=False)
    sorumluID = db.Column(db.Integer, db.ForeignKey('akademisyen.aID'), nullable=False)
    bolum = db.Column(db.String)

class PC(db.Model):
    __tablename__ = 'pc'
    pcID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    baslik = db.Column(db.String, nullable=False)
    aciklama = db.Column(db.String, nullable=False)

class DersPC(db.Model):
    __tablename__ = 'derspc'
    dersID = db.Column(db.Integer, db.ForeignKey('dersler.dID'), primary_key=True)
    pcID = db.Column(db.Integer, db.ForeignKey('pc.pcID'), primary_key=True)

class OgrDers(db.Model):
    __tablename__ = 'ogrders'
    ogrID = db.Column(db.Integer, db.ForeignKey('ogrenci.ogrID'), primary_key=True)
    dersID = db.Column(db.Integer, db.ForeignKey('dersler.dID'), primary_key=True)

class Sinav(db.Model):
    __tablename__ = 'sinav'
    sinavID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dersID = db.Column(db.Integer, db.ForeignKey('dersler.dID'), nullable=False)

class Seminer(db.Model):
    __tablename__ = 'seminer'
    seminerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dersID = db.Column(db.Integer, nullable=False)
