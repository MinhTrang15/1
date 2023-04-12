from hospital.models import BenhNhan, DanhSach, PhieuKham, DonThuoc, HoaDon, Thuoc, DonViThuoc, NhanVien
from hospital import db, app
from sqlalchemy import func, extract
import hashlib


def check_login(username, password, role):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return NhanVien.query.filter(NhanVien.username.__eq__(username.strip()),
                                 NhanVien.password.__eq__(password),
                                 NhanVien.user_role.__eq__(role)).first()


def get_staff_by_id(nhan_vien_id):
    return NhanVien.query.get(nhan_vien_id)


def load_tracuuthuoc(keyword=None, price=None):
    thuoc = Thuoc.query
    if keyword:
        thuoc = thuoc.filter(Thuoc.name.contains(keyword))
    if price:
        thuoc = thuoc.filter(Thuoc.price.contains(price))
    return thuoc.all()


def load_lichsu(keyword=None):
    lichsu = PhieuKham.query
    if keyword:
        lichsu = lichsu.filter(PhieuKham.benh_nhan_id.contains(keyword))
    return lichsu.all()


def add_patient(name, sex, birthday, phone, address):
    b = BenhNhan(name=name.strip(), sex=sex.strip(), birthday=birthday.strip(), phone=phone.strip(),
                 address=address.strip())

    db.session.add(b)
    db.session.commit()


def add_phieu_kham(trieu_chung, loai_benh, benh_nhan_id):
    p = PhieuKham(trieu_chung=trieu_chung, loai_benh=loai_benh, benh_nhan_id=benh_nhan_id)

    db.session.add(p)
    db.session.commit()


def add_don_thuoc(phieu_kham_id, thuoc_id, so_luong, cach_dung):
    pt = DonThuoc(phieu_kham_id=phieu_kham_id, thuoc_id=thuoc_id, so_luong=so_luong, cach_dung=cach_dung)

    db.session.add(pt)
    db.session.commit()


def add_date(ngay):
    d = DanhSach(ngay_kham=ngay)

    db.session.add(d)
    db.session.commit()


def update_date(benh_nhan_id, id):
    BenhNhan.query.filter_by(id=benh_nhan_id).first().danh_sach_id = id
    db.session.commit()


def tinh_tien(tienKham, tienthuoc):
    return tienKham + tienthuoc


def pay(tienkham, tienthuoc, tongtien, benh_nhan_id):
    p = HoaDon(tien_kham=tienkham, tien_thuoc=tienthuoc, tong_tien=tongtien, benh_nhan_id=benh_nhan_id)

    db.session.add(p)
    db.session.commit()


def total_bill(month):
    return db.session.query(func.sum(HoaDon.tien_kham + HoaDon.tien_thuoc))\
        .filter(extract('month', HoaDon.ngay_kham) == month).all()


def stats_revenue(month):
    query = total_bill(month)
    a = query[0]
    b = a[0]
    query = db.session.query(HoaDon.ngay_kham.distinct(), func.count(BenhNhan.id),
                             func.sum(HoaDon.tien_kham + HoaDon.tien_thuoc),
                             func.round(((func.sum(HoaDon.tien_kham + HoaDon.tien_thuoc) / b) * 100))) \
                            .join(HoaDon, HoaDon.benh_nhan_id.__eq__(BenhNhan.id)) \

    if month:
        query = query.filter(extract('month', HoaDon.ngay_kham).__eq__(month))

    return query.group_by(HoaDon.ngay_kham).all()


def count_thuoc_by_cate(month=None):
    query = db.session.query(Thuoc.name.distinct(), DonViThuoc.name, func.count(Thuoc.id)) \
        .join(DonThuoc, DonThuoc.thuoc_id.__eq__(Thuoc.id), isouter=True)\
        .join(PhieuKham, PhieuKham.id.__eq__(DonThuoc.phieu_kham_id))\
        .join(DonViThuoc, Thuoc.unit_id.__eq__(DonViThuoc.id))

    if month:
        query = query.filter(extract('month', HoaDon.ngay_kham).__eq__(month))

    return query.group_by(Thuoc.name, DonViThuoc.name).all()

