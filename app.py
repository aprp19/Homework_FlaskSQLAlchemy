from flask import Flask, request
from datetime import date
from models.database import db, db_session
from models.models import ModelUsers, ModelBuku, ModelKategori, ModelTransaksi, ModelPenulis, ModelKategoriBuku
from auth.authentication import basic_auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/perpus"
db.init_app(app)


@app.route('/penulis/<id_penulis>', methods=['GET'])
@basic_auth
def handle_get_penulis(id_penulis):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if id_penulis == 'all':
            getall = ModelPenulis.query.all()
            response = [{
                "ID Penulis": get.id_penulis,
                "Nama": get.nama_penulis,
                "Asal": get.asal
            } for get in getall]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        get = ModelPenulis.query.get(id_penulis)
        if not get:
            return {"Message": "ID Penulis tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            response = {
                "ID Penulis": get.id_penulis,
                "Nama": get.nama_penulis,
                "Asal": get.asal
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/penulis', methods=['POST'])
@basic_auth
def handle_post_penulis():
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            json = request.get_json()
            add_penulis = ModelPenulis(
                nama_penulis=json['Nama Penulis'],
                asal=json['Asal'],
            )
            db_session.add(add_penulis)
            db_session.commit()
            return {"Message": "Success", "Data": f"{add_penulis.nama_penulis}",
                    "Admin Authority": check_auth.is_admin}, \
                201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/penulis/<id_penulis>', methods=['PUT'])
@basic_auth
def handle_put_penulis(id_penulis):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            data_penulis = ModelPenulis.query.get(id_penulis)
            json = request.get_json()
            data_penulis.nama_penulis = json['Nama Penulis']
            data_penulis.asal = json['Asal']
            db_session.add(data_penulis)
            db_session.commit()
            return {"Message": "Success", "Data": f"{data_penulis.nama_penulis}",
                    "Admin Authority": check_auth.is_admin}, \
                201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/penulis/<id_penulis>', methods=['DELETE'])
@basic_auth
def handle_delete_penulis(id_penulis):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        check_penulis = ModelPenulis.query.filter_by(id_penulis=id_penulis).first()
        if not check_penulis:
            return {"Message": "ID Penulis tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            delete_penulis = ModelPenulis.query.filter_by(id_penulis=id_penulis).first()
            db_session.delete(delete_penulis)
            db_session.commit()
            return {"Message": "Success", "Admin Authority": check_auth.is_admin}, 201
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori/<id_kategori>', methods=['GET'])
@basic_auth
def handle_get_kategori(id_kategori):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if id_kategori == 'all':
            getall = ModelKategori.query.all()
            response = [{
                "ID Kategori": get.id_kategori,
                "Nama Kategori": get.nama_kategori
            } for get in getall]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        get = ModelKategori.query.get(id_kategori)
        if not get:
            return {"Message": "ID Kategori tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            response = {
                "ID Kategori": get.id_kategori,
                "Nama": get.nama_kategori
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori', methods=['POST'])
@basic_auth
def handle_post_kategori():
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            json = request.get_json()
            add_kategori = ModelKategori(
                nama_kategori=json['Nama Kategori']
            )
            db_session.add(add_kategori)
            db_session.commit()
            return {"Message": "Success", "Data": f"{add_kategori.nama_kategori}",
                    "Admin Authority": check_auth.is_admin}, \
                201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori/<id_kategori>', methods=['PUT'])
@basic_auth
def handle_put_kategori(id_kategori):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            data_kategori = ModelKategori.query.get(id_kategori)
            json = request.get_json()
            data_kategori.nama_kategori = json['Nama kategori']
            db_session.add(data_kategori)
            db_session.commit()
            return {"Message": "Success", "Data": f"{data_kategori.nama_kategori}",
                    "Admin Authority": check_auth.is_admin}, \
                201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori/<id_kategori>', methods=['DELETE'])
@basic_auth
def handle_delete_kategori(id_kategori):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        check_kategori = ModelKategori.query.filter_by(id_kategori=id_kategori).first()
        if not check_kategori:
            return {"Message": "ID Kategori tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            delete_kategori = ModelKategori.query.filter_by(id_kategori=id_kategori).first()
            db_session.delete(delete_kategori)
            db_session.commit()
            return {"Message": "Success", "Admin Authority": check_auth.is_admin}, 201
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/buku/<id_buku>', methods=['GET'])
@basic_auth
def handle_get_buku(id_buku):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if id_buku == 'all':
            getall = ModelBuku.query.all()
            response = [{
                "ID Buku": get.id_buku,
                "Nama Buku": get.nama_buku,
                "Nama Penulis": get.penulis.nama_penulis
            } for get in getall]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        get = ModelBuku.query.get(id_buku)
        if not get:
            return {"Message": "ID Buku tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            response = {
                "ID Buku": get.id_buku,
                "Nama Buku": get.nama_buku,
                "Nama Penulis": get.penulis.nama_penulis
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/buku', methods=['POST'])
@basic_auth
def handle_post_buku():
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            json = request.get_json()
            check_buku = ModelBuku.query.filter_by(nama_buku=json['Nama Buku']).first()
            if check_buku is not None:
                return {"Message": "ID Buku sudah ada", "Admin Authority": check_auth.is_admin}, 406
            else:
                check_penulis = ModelPenulis.query.filter_by(id_penulis=json['ID Penulis']).first()
                if not check_penulis:
                    return {"Message": "ID Penulis tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
                else:
                    add_buku = ModelBuku(
                        nama_buku=json['Nama Buku'],
                        id_penulis=json['ID Penulis']
                    )
                    db_session.add(add_buku)
                    db_session.commit()
                    return {"Message": "Success", "Data": f"{add_buku.nama_buku}",
                            "Admin Authority": check_auth.is_admin}, \
                        201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/buku/<id_buku>', methods=['PUT'])
@basic_auth
def handle_put_buku(id_buku):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            data_buku = ModelBuku.query.get(id_buku)
            json = request.get_json()
            data_buku.nama_buku = json['Nama Buku']
            data_buku.id_penulis = json['ID Penulis']
            db_session.add(data_buku)
            db_session.commit()
            return {"Message": "Success", "Data": f"{data_buku.nama_buku}",
                    "Admin Authority": check_auth.is_admin}, \
                201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/buku/<id_buku>', methods=['DELETE'])
@basic_auth
def handle_delete_buku(id_buku):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        check_buku = ModelBuku.query.filter_by(id_buku=id_buku).first()
        if not check_buku:
            return {"Message": "ID buku tidak ditemukan", "Admin Authority": check_auth.is_admin}, 200
        else:
            delete_buku = ModelBuku.query.filter_by(id_buku=id_buku).first()
            db_session.delete(delete_buku)
            db_session.commit()
            return {"Message": "Success", "Admin Authority": check_auth.is_admin}, 201
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori_buku/<id_buku>', methods=['GET'])
@basic_auth
def handle_get_kategoribuku(id_buku):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if id_buku == 'all':
            getall = ModelKategoriBuku.query.all()
            response = [{
                "ID Buku": get.id_buku,
                "Nama Buku": get.buku.nama_buku,
                "Kategori Buku": [data.nama_kategori for data in ModelKategori.query.filter(ModelKategoriBuku.id_buku==get.id_buku, ModelKategori.id_kategori==ModelKategoriBuku.id_kategori).all()]
            } for get in getall]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        check_kategori_buku = ModelKategoriBuku.query.get(id_buku)
        if not check_kategori_buku:
            return {"Message": "ID Buku tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            get_kategoribuku = ModelKategoriBuku.query.get(id_buku)
            response = {
                "ID Buku": get_kategoribuku.id_buku,
                "Nama Buku": get_kategoribuku.buku.nama_buku,
                "List Kategori": [data.nama_kategori for data in ModelKategori.query.filter(ModelKategoriBuku.id_buku==get_kategoribuku.id_buku, ModelKategori.id_kategori==ModelKategoriBuku.id_kategori)]
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori_buku', methods=['POST'])
@basic_auth
def handle_post_kategoribuku():
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            json = request.get_json()
            check_kategori_buku = ModelKategoriBuku.query.join(ModelBuku).filter_by(nama_buku=json['Nama Buku']).join(
                ModelKategori).filter_by(nama_kategori=json['Kategori']).first()
            if check_kategori_buku is not None:
                return {"Message": "Kategori buku sudah ada", "Admin Authority": check_auth.is_admin}, 406
            else:
                buku = ModelBuku.query.filter_by(nama_buku=json['Nama Buku']).first()
                kategori = ModelKategori.query.filter_by(nama_kategori=json['Kategori']).first()
                if not buku or not kategori:
                    return {"Message": "ID Buku/ID Kategori tidak ditemukan",
                            "Admin Authority": check_auth.is_admin}, 404
                else:
                    add_kategori_buku = ModelKategoriBuku(
                        id_buku=buku.id_buku,
                        id_kategori=kategori.id_kategori
                    )
                    db_session.add(add_kategori_buku)
                    db_session.commit()
                    return {"Message": "Success", "Data": f"{add_kategori_buku.buku.nama_buku}",
                            "Admin Authority": check_auth.is_admin}, \
                        201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori_buku/<id_buku>/<id_kategori>', methods=['PUT'])
@basic_auth
def handle_put_kategoribuku(id_buku, id_kategori):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            json = request.get_json()
            check_kategori_buku = ModelKategoriBuku.query.join(ModelBuku).filter_by(id_buku=id_buku). \
                join(ModelKategori).filter_by(nama_kategori=json['Kategori']).first()
            if check_kategori_buku is not None:
                return {"Message": "Kategori buku sudah ada", "Admin Authority": check_auth.is_admin}, 406
            else:
                kategori_buku = ModelKategoriBuku.query.filter_by(id_buku=id_buku, id_kategori=id_kategori).first()
                get_kategori = ModelKategori.query.filter_by(nama_kategori=json['Kategori']).first()
                kategori_buku.id_buku = id_buku
                kategori_buku.id_kategori = get_kategori.id_kategori
                db_session.add(kategori_buku)
                db_session.commit()
            return {"Message": "Success", "Data": f"{kategori_buku.buku.nama_buku}",
                    "Admin Authority": check_auth.is_admin}, \
                201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori_buku/<id_buku>/<id_kategori>', methods=['DELETE'])
@basic_auth
def handle_delete_kategoribuku(id_buku, id_kategori):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        kategori_buku = ModelKategoriBuku.query.filter_by(id_buku=id_buku, id_kategori=id_kategori).first()
        if not kategori_buku:
            return {"Message": "ID Buku tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            db_session.delete(kategori_buku)
            db_session.commit()
            return {"Message": "Success", "Admin Authority": check_auth.is_admin}, 201
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/users/<id_user>', methods=['GET'])
@basic_auth
def handle_get_users(id_user):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if id_user == 'all':
            query = ModelUsers.query.all()
            print(query)
            response = [{
                "ID User": data.id_user,
                "Nama User": data.nama_user,
                "Username": data.username,
                "password": data.passwords,
                "Role": data.is_admin
            } for data in query]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        query = ModelUsers.query.get(id_user)
        if not query:
            return {"Message": "User tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            response = {
                "ID User": query.id_user,
                "Nama User": query.nama_user,
                "Username": query.username,
                "password": query.passwords,
                "Role": query.is_admin
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/users', methods=['POST'])
@basic_auth
def handle_post_users():
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            json = request.get_json()
            check_users = ModelUsers.query.filter_by(username=json['username']).first()
            if check_users is not None:
                return {"Message": "User sudah ada", "Admin Authority": check_auth.is_admin}, 406
            else:
                add_user = ModelUsers(
                    username=json['username'],
                    passwords=json['password'],
                    nama_user=json['nama_user'],
                    is_admin=json['is_admin'],
                )
                db_session.add(add_user)
                db_session.commit()
                return {"Message": "Success", "Data": f"{add_user.nama_user}",
                        "Admin Authority": check_auth.is_admin}, \
                    201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/users/<username>', methods=['PUT'])
@basic_auth
def handle_put_users(username):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        if request.is_json:
            json = request.get_json()
            check_users = ModelUsers.query.filter_by(username=username).first()
            if not check_users:
                return {"Message": "User tidak ditemukan", "Admin Authority": check_auth.is_admin}, 406
            else:
                query = ModelUsers.query.get(check_users.id_user)
                query.nama_user = json['nama_user']
                query.passwords = json['password']
                query.is_admin = json['is_admin']
                db_session.add(query)
                db_session.commit()
            return {"Message": "Success", "Data": f"{query.nama_user}",
                    "Admin Authority": check_auth.is_admin}, \
                201
        else:
            return {"Message": "Invalid Request", "Admin Authority": check_auth.is_admin}, 400
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/users/<username>', methods=['DELETE'])
@basic_auth
def handle_delete_users(username):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        check_users = ModelUsers.query.filter_by(username=username).first()
        if not check_users:
            return {"Message": "User tidak ditemukan", "Admin Authority": check_auth.is_admin}, 406
        else:
            db_session.add(check_users)
            db_session.commit()
        return {"Message": "Success", "Admin Authority": check_auth.is_admin}, \
            201
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/transaksi/<id_transaksi>', methods=['GET'])
@basic_auth
def handle_get_transaksi(id_transaksi):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[6:] == 'Terima':
        query_terima = ModelTransaksi.query.filter(ModelTransaksi.status == 'Requested').all()
        if id_transaksi == 'all':
            response = [{
                "ID Transaksi": data.id_transaksi,
                "ID Buku": data.id_buku,
                "Nama Buku": data.buku.nama_buku,
                "ID User": data.id_user,
                "Nama Peminjam": data.users.nama_user,
                "Tanggal Pinjam": data.tgl_pinjam,
                "Tanggal Kembali": data.tgl_kembali,
                "Admin Pinjam": data.admin_pinjam,
                "Admin Kembali": data.admin_kembali,
                "Status": data.status
            } for data in query_terima]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        query_terima = ModelTransaksi.query.filter(ModelTransaksi.id_transaksi == id_transaksi,
                                                   ModelTransaksi.status == 'Requested').first()
        if not query_terima:
            return {"Message": "Transaksi tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            response = {
                "ID Transaksi": query_terima.id_transaksi,
                "ID Buku": query_terima.id_buku,
                "Nama Buku": query_terima.buku.nama_buku,
                "ID User": query_terima.id_user,
                "Nama Peminjam": query_terima.users.nama_user,
                "Tanggal Pinjam": query_terima.tgl_pinjam,
                "Tanggal Kembali": query_terima.tgl_kembali,
                "Admin Pinjam": query_terima.admin_pinjam,
                "Admin Kembali": query_terima.admin_kembali,
                "Status": query_terima.status
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200

    elif check_auth.is_admin[6:] == 'Kembali':
        query_kembali = ModelTransaksi.query.filter(ModelTransaksi.status == 'Approved').all()
        if id_transaksi == 'all':
            response = [{
                "ID Transaksi": data.id_transaksi,
                "ID Buku": data.id_buku,
                "Nama Buku": data.buku.nama_buku,
                "ID User": data.id_user,
                "Nama Peminjam": data.users.nama_user,
                "Tanggal Pinjam": data.tgl_pinjam,
                "Tanggal Kembali": data.tgl_kembali,
                "Admin Pinjam": data.admin_pinjam,
                "Admin Kembali": data.admin_kembali,
                "Status": data.status
            } for data in query_kembali]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        query_kembali = ModelTransaksi.query.filter(ModelTransaksi.id_transaksi == id_transaksi,
                                                    ModelTransaksi.status == 'Approved').first()
        if query_kembali:
            response = {
                "ID Transaksi": query_kembali.id_transaksi,
                "ID Buku": query_kembali.id_buku,
                "Nama Buku": query_kembali.buku.nama_buku,
                "ID User": query_kembali.id_user,
                "Nama Peminjam": query_kembali.users.nama_user,
                "Tanggal Pinjam": query_kembali.tgl_pinjam,
                "Tanggal Kembali": query_kembali.tgl_kembali,
                "Admin Pinjam": query_kembali.admin_pinjam,
                "Admin Kembali": query_kembali.admin_kembali,
                "Status": query_kembali.status
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200
        else:
            return {"Message": "Transaksi tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
    else:

        query_user = ModelTransaksi.query.filter_by(id_user=check_auth.id_user).all()
        if id_transaksi == 'all':
            response = [{
                "ID Transaksi": data.id_transaksi,
                "ID Buku": data.id_buku,
                "Nama Buku": data.buku.nama_buku,
                "ID User": data.id_user,
                "Nama Peminjam": data.users.nama_user,
                "Tanggal Pinjam": data.tgl_pinjam,
                "Tanggal Kembali": data.tgl_kembali,
                "Admin Pinjam": data.admin_pinjam,
                "Admin Kembali": data.admin_kembali,
                "Status": data.status
            } for data in query_user]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        elif query_user.id_transaksi == id_transaksi:
            response = {
                "ID Transaksi": query_user.id_transaksi,
                "ID Buku": query_user.id_buku,
                "Nama Buku": query_user.buku.nama_buku,
                "ID User": query_user.id_user,
                "Nama Peminjam": query_user.users.nama_user,
                "Tanggal Pinjam": query_user.tgl_pinjam,
                "Tanggal Kembali": query_user.tgl_kembali,
                "Admin Pinjam": query_user.admin_pinjam,
                "Admin Kembali": query_user.admin_kembali,
                "Status": query_user.status
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200
        else:
            return {"Message": "Transaksi tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404


@app.route('/transaksi', methods=['POST'])
@basic_auth
def handle_post_transaksi():
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin == 'false':
        if request.is_json:
            json = request.get_json()
            add_transaksi = ModelTransaksi(
                id_buku=json['ID Buku'],
                id_user=check_auth.id_user,
                nama_peminjam=check_auth.nama_user,
                tgl_pinjam=date.today().strftime("%d-%m-%Y"),
                status='Requested'
            )
            db_session.add(add_transaksi)
            db_session.commit()
            return {"Message": "Success", "Data": f"{ModelBuku.query.filter_by(id_buku=json['ID Buku']).first().nama_buku} berhasil dipinjam",
                    "Admin Authority": check_auth.is_admin}, \
                201
        else:
            return {"Message": "Data tidak valid"}, 400
    else:
        return {"Message": "Anda tidak memiliki akses"}, 403


@app.route('/transaksi/<id_transaksi>', methods=['PUT'])
@basic_auth
def handle_put_transaksi(id_transaksi):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[6:] == 'Terima':
        query_terima = ModelTransaksi.query.filter(ModelTransaksi.id_transaksi == id_transaksi,
                                                   ModelTransaksi.status == 'Requested').first()
        if not query_terima:
            return {"Message": "Transaksi tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            query_terima.admin_pinjam = check_auth.nama_user
            query_terima.status = 'Approved'
            db_session.add(query_terima)
            db_session.commit()
            return {"Message": "Success", "Data": 'Approved',
                    "Admin Authority": check_auth.is_admin}, \
                200

    elif check_auth.is_admin[6:] == 'Kembali':
        query_kembali = ModelTransaksi.query.filter(ModelTransaksi.id_transaksi == id_transaksi,
                                                    ModelTransaksi.status == 'Approved').first()
        if not query_kembali:
            return {"Message": "Transaksi tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            query_kembali.tgl_kembali = date.today().strftime("%d-%m-%Y")
            query_kembali.admin_kembali = check_auth.nama_user
            query_kembali.status = 'Returned'
            db_session.add(query_kembali)
            db_session.commit()
            return {"Message": "Success", "Data": 'Returned',
                    "Admin Authority": check_auth.is_admin}, \
                200
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/transaksi/<id_transaksi>', methods=['DELETE'])
@basic_auth
def handle_delete_transaksi(id_transaksi):
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin[:5] == 'Admin':
        check_transaksi = ModelTransaksi.query.filter_by(id_transaksi=id_transaksi).first()
        if not check_transaksi:
            return {"Message": "Transaksi tidak ditemukan", "Admin Authority": check_auth.is_admin}, 406
        else:
            db_session.delete(check_transaksi)
            db_session.commit()
        return {"Message": "Success", "Admin Authority": check_auth.is_admin}, \
            201
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


if __name__ == '__main__':
    app.run()
