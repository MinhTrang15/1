from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from hospital import db, app
from sqlalchemy.orm import relationship
from datetime import date
from enum import Enum as UserEnum
from flask_login import UserMixin


tienKham = int(100000)


class UserRole(UserEnum):
    STAFF = 1
    CUSTOMER = 2


class BaseModel(db.Model):
    __abstract__ = True


class NhanVien(BaseModel, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole))
    thuoc = relationship('Thuoc', backref='nhanvien', lazy=True)
    quydinh = relationship('QuyDinh', backref='nhanvien')


class QuyDinh(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    content = Column(Integer)
    admin_id = Column(Integer, ForeignKey(NhanVien.id))

    def __str__(self):
        return self.name


class DanhSach(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_kham = Column(String(50))
    benh_nhan = relationship('BenhNhan', backref='list', lazy=True)

    def __str__(self):
        return self.name


class BenhNhan(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    sex = Column(String(50), nullable=False)
    birthday = Column(String(50), nullable=False)
    phone = Column(String(12), nullable=False)
    address = Column(String(100))
    danh_sach_id = Column(Integer, ForeignKey(DanhSach.id))
    phieu_kham = relationship('PhieuKham', backref='benhnhan', lazy=True)
    hoa_don = relationship('HoaDon', backref='benhnhan', lazy=True)

    def __str__(self):
        return self.name


class PhieuKham(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_kham = Column(DateTime, default=date.today())
    trieu_chung = Column(String(50))
    loai_benh = Column(String(50))
    don_thuoc_id = relationship("DonThuoc", backref='phieukham')
    benh_nhan_id = Column(Integer, ForeignKey(BenhNhan.id))

    def __str__(self):
        return self.name


class LoaiThuoc(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    thuoc = relationship('Thuoc', backref='loaithuoc', lazy=True)


class DonViThuoc(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    thuoc = relationship('Thuoc', backref='donvithuoc', lazy=True)


class Thuoc(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer)
    thuoc = relationship("DonThuoc", backref='thuoc')
    unit_id = Column(Integer, ForeignKey(DonViThuoc.id))
    category_id = Column(Integer, ForeignKey(LoaiThuoc.id))
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id))

    def __str__(self):
        return self.name


class DonThuoc(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    phieu_kham_id = Column(Integer, ForeignKey(PhieuKham.id), primary_key=True)
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), primary_key=True)
    so_luong = Column(Integer, default=1)
    cach_dung = Column(String(100))


class HoaDon(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_kham = Column(DateTime, default=date.today())
    tien_kham = Column(Float, default=tienKham)
    tien_thuoc = Column(Float)
    tong_tien = Column(Float)
    benh_nhan_id = Column(Integer, ForeignKey(BenhNhan.id))

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        # password = str(hashlib.md5('admin'.encode('utf-8')).hexdigest())
        # a = NhanVien(username="admin", password=password, user_role="STAFF")
        # db.session.add(a)
        # db.session.commit()
        #
        #
        # c1 = QuyDinh(name='Tiền khám', content=100000, admin_id=1)
        # c2 = QuyDinh(name='Bệnh nhân', content=40, admin_id=1)
        # db.session.add_all([c1, c2])
        # db.session.commit()
        #
        #
        # u1 = DonViThuoc(name='Viên')
        # u2 = DonViThuoc(name='Chai')
        # u3 = DonViThuoc(name='Vỉ')
        # db.session.add(u1)
        # db.session.add(u2)
        # db.session.add(u3)
        #
        # c1 = LoaiThuoc(name='Thuốc sát khuẩn')
        # c2 = LoaiThuoc(name='Thuốc hạ sốt')
        # c3 = LoaiThuoc(name='Thuốc chống dị ứng')
        # c4 = LoaiThuoc(name='Thuốc đau đầu')
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)
        # db.session.add(c4)
        #
        #
        # t1 = Thuoc(name='Paracetamol', price=20000, unit_id=3,category_id=4, nhan_vien_id=1)
        # t2 = Thuoc(name='Hapacol', price=30000, unit_id=3,category_id=2, nhan_vien_id=1)
        # t3 = Thuoc(name='Oxy già', price=10000, unit_id=2,category_id=1, nhan_vien_id=1)
        # t4 = Thuoc(name='Allergex', price=15000, unit_id=1,category_id=3, nhan_vien_id=1)
        # db.session.add(t1)
        # db.session.add(t2)
        # db.session.add(t3)
        # db.session.add(t4)
        # db.session.commit()




