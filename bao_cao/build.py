# -*- coding: utf-8 -*-
"""
Xuat ban BAO CAO TONG KET DE TAI NCKH theo Mau 2021-SVNCKH-04-BCTK.

Chay tu trong thu muc bao_cao/:
    python build.py

Cau truc bao cao theo dung trinh tu muc 3.1 - 3.13 cua mau:
    3.1  Bia bao cao
    3.2  Muc luc
    3.3  Danh muc bang bieu
    3.4  Danh muc nhung tu viet tat
    3.5  Mo dau
    3.6  Tong quan tinh hinh nghien cuu
    3.7  Ly do lua chon de tai
    3.8  Muc tieu, noi dung, phuong phap nghien cuu
    3.9  Doi tuong va pham vi nghien cuu
    3.10 Ket qua nghien cuu va thao luan (Chuong 1 - 4)
    3.11 Ket luan va kien nghi
    3.12 Tai lieu tham khao
    3.13 Phu luc
"""
import os
import sys

from engine import new_document, enable_update_fields
import phan_a
import phan_b
import phan_c

OUT = "BAO_CAO_TONG_KET_NCKH_Goldtrading.docx"


def main():
    doc = new_document()

    # ---- 3.1 Bia bao cao ----
    phan_a.trang_bia(doc)

    # ---- 3.2 - 3.4 Muc luc va cac danh muc (so trang i, ii, iii...) ----
    phan_a.muc_luc_va_danh_muc(doc)

    # ---- 3.5 - 3.9 Phan mo dau (so trang 1, 2, 3...) ----
    phan_a.mo_dau(doc)
    phan_a.tong_quan(doc)
    phan_a.ly_do_chon_de_tai(doc)
    phan_a.muc_tieu_noi_dung_phuong_phap(doc)
    phan_a.doi_tuong_pham_vi(doc)

    # ---- 3.10 Ket qua nghien cuu va thao luan ----
    phan_b.chuong_1(doc)
    phan_b.chuong_2(doc)
    phan_c.chuong_3(doc)
    phan_c.chuong_4(doc)

    # ---- 3.11 Ket luan va kien nghi ----
    phan_c.ket_luan_kien_nghi(doc)

    # ---- 3.12 Tai lieu tham khao ----
    phan_c.tai_lieu_tham_khao(doc)

    # ---- 3.13 Phu luc ----
    phan_c.phu_luc(doc)

    # Bat co de Word tu cap nhat MUC LUC / DANH MUC khi mo file
    enable_update_fields(doc)

    doc.save(OUT)

    size_kb = os.path.getsize(OUT) / 1024
    print(f"Da xuat: {OUT}  ({size_kb:.0f} KB)")
    print()
    print("LUU Y: Mo file trong Word, nhan Ctrl+A roi F9 (hoac bam Yes khi Word")
    print("hoi cap nhat truong) de sinh MUC LUC, DANH MUC BANG, DANH MUC HINH")
    print("va so trang.")


if __name__ == "__main__":
    main()
