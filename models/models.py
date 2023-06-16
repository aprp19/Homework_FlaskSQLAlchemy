from models.database import db


class ModelUsers(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(25), nullable=False)
    passwords = db.Column(db.String(25), nullable=False)
    nama_user = db.Column(db.String(25), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    relasi_transaksi = db.relationship('ModelTransaksi', backref='users')


class ModelPenulis(db.Model):
    __tablename__ = 'penulis'

    id_penulis = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    nama_penulis = db.Column(db.String(10), nullable=False)
    asal = db.Column(db.String(10), nullable=False)
    relasi_buku = db.relationship('ModelBuku', backref='penulis')


class ModelBuku(db.Model):
    __tablename__ = 'buku'

    id_buku = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    nama_buku = db.Column(db.String(25), nullable=False)
    id_penulis = db.Column(db.String(25), db.ForeignKey('penulis.id_penulis'), nullable=False)
    relasi_kategori_buku = db.relationship('ModelKategoriBuku', backref='buku')


class ModelKategori(db.Model):
    __tablename__ = 'kategori'

    id_kategori = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    nama_kategori = db.Column(db.String(25), nullable=False)
    relasi_kategori_buku = db.relationship('ModelKategoriBuku', backref='kategori')


class ModelKategoriBuku(db.Model):
    __tablename__ = 'kategoribuku'

    id_buku = db.Column(db.Integer, db.ForeignKey('buku.id_buku'), primary_key=True, nullable=False)
    id_kategori = db.Column(db.Integer, db.ForeignKey('kategori.id_kategori'), nullable=False)


class ModelTransaksi(db.Model):
    __tablename__ = 'transaksi'

    id_transaksi = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    id_buku = db.Column(db.Integer, db.ForeignKey('buku.id_buku'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    nama_peminjam = db.Column(db.String(25), nullable=False)
    tgl_pinjam = db.Column(db.String(25), nullable=False)
    tgl_kembali = db.Column(db.String(25))
    nama_admin = db.Column(db.String(25))
    status = db.Column(db.String(25), nullable=False)
