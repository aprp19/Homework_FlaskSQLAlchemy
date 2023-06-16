from flask import Flask, request
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
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
    if check_auth.is_admin:
        if id_buku == 'all':
            getall = ModelKategoriBuku.query.all()
            response = [{
                "ID Buku": get.id_buku,
                "Nama Buku": get.buku.nama_buku,
                "Kategori Buku": get.kategori.nama_kategori
            } for get in getall]
            return {"Message": "Success", "Count": len(response), "Data": response,
                    "Admin Authority": check_auth.is_admin}, \
                200
        check_kategori_buku = ModelKategoriBuku.query.get(id_buku)
        if not check_kategori_buku:
            return {"Message": "ID Buku tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            response = {
                "ID Buku": check_kategori_buku.id_buku,
                "Nama Buku": check_kategori_buku.buku.nama_buku,
                "Kategori Buku": check_kategori_buku.kategori.nama_kategori
            }
            return {"Message": "Success", "Data": response, "Admin Authority": check_auth.is_admin}, 200
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


@app.route('/kategori_buku', methods=['POST'])
@basic_auth
def handle_post_kategoribuku():
    check_auth = ModelUsers.query.filter_by(username=request.authorization.username).first()
    if check_auth.is_admin:
        if request.is_json:
            json = request.get_json()
            check_kategori_buku = ModelKategoriBuku.query.join(ModelBuku).filter_by(nama_buku=json['Nama Buku']).join(ModelKategori).filter_by(nama_kategori=json['Kategori']).first()
            if check_kategori_buku is not None:
                return {"Message": "Kategori buku sudah ada", "Admin Authority": check_auth.is_admin}, 406
            else:
                check_buku = ModelBuku.query.filter_by(nama_buku=json['Nama Buku']).first()
                check_kategori = ModelKategori.query.filter_by(nama_kategori=json['Kategori']).first()
                if not check_buku or not check_kategori:
                    return {"Message": "ID Buku/ID Kategori tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
                else:
                    get_buku = ModelBuku.query.filter_by(nama_buku=json['Nama Buku']).first()
                    get_kategori = ModelKategori.query.filter_by(nama_kategori=json['Kategori']).first()
                    add_kategori_buku = ModelKategoriBuku(
                        id_buku=get_buku.id_buku,
                        id_kategori=get_kategori.id_kategori
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
    if check_auth.is_admin:
        if request.is_json:
            json = request.get_json()
            check_kategori_buku = ModelKategoriBuku.query.join(ModelBuku).filter_by(id_buku=id_buku).\
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
    if check_auth.is_admin:
        check_kategori_buku = ModelKategoriBuku.query.filter_by(id_buku=id_buku, id_kategori=id_kategori).first()
        if not check_kategori_buku:
            return {"Message": "ID Buku tidak ditemukan", "Admin Authority": check_auth.is_admin}, 404
        else:
            delete_kategoribuku = ModelKategoriBuku.query.filter_by(id_buku=id_buku, id_kategori=id_kategori).first()
            db_session.delete(delete_kategoribuku)
            db_session.commit()
            return {"Message": "Success", "Admin Authority": check_auth.is_admin}, 201
    else:
        return {"Message": "Admin Access Only", "Admin Authority": check_auth.is_admin}, 403


if __name__ == '__main__':
    app.run()
