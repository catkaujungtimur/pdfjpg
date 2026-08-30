#!/usr/bin/env python3
"""
pdf2a4.py — Convert file PDF (biasanya 2 halaman) menjadi SATU gambar
berukuran kertas A4, dengan halaman-halaman ditumpuk atas-bawah.

Cara pakai:
    python3 pdf2a4.py input.pdf
    python3 pdf2a4.py input.pdf -o hasil.png
    python3 pdf2a4.py *.pdf                # proses banyak file sekaligus
    python3 pdf2a4.py folder_download/      # proses semua PDF dalam folder

Output otomatis disimpan di sebelah file PDF asal, dengan nama yang sama
tapi berekstensi .png (kecuali -o dipakai untuk 1 file saja).

Install dependency sekali saja:
    pip install pymupdf pillow
"""

import sys
import argparse
from pathlib import Path

import pymupdf as fitz  # PyMuPDF
from PIL import Image

# Ukuran A4 di 300 DPI (resolusi cetak yang bagus)
DPI = 300
A4_WIDTH_PX = round(8.27 * DPI)   # ≈ 2481 px
A4_HEIGHT_PX = round(11.69 * DPI)  # ≈ 3507 px

# Jarak antar halaman saat ditumpuk (dalam px), biar ada pemisah tipis
GAP_PX = 12
BG_COLOR = (255, 255, 255)


def render_pdf_pages(pdf_path: Path, dpi: int = DPI) -> list[Image.Image]:
    """Render setiap halaman PDF menjadi objek PIL Image."""
    doc = fitz.open(pdf_path)
    zoom = dpi / 72  # PDF default = 72 DPI
    matrix = fitz.Matrix(zoom, zoom)

    images = []
    for page in doc:
        pix = page.get_pixmap(matrix=matrix)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        images.append(img)
    doc.close()
    return images


def stack_onto_a4(images: list[Image.Image]) -> Image.Image:
    """
    Tumpuk beberapa gambar halaman secara vertikal (atas-bawah) ke dalam
    satu kanvas A4 portrait, masing-masing di-scale proporsional supaya
    muat berdampingan tanpa terpotong.
    """
    n = len(images)
    if n == 0:
        raise ValueError("PDF tidak punya halaman.")

    canvas = Image.new("RGB", (A4_WIDTH_PX, A4_HEIGHT_PX), BG_COLOR)

    # Tinggi yang tersedia untuk tiap halaman (dikurangi jarak antar halaman)
    total_gap = GAP_PX * (n - 1)
    slot_height = (A4_HEIGHT_PX - total_gap) // n

    y_cursor = 0
    for img in images:
        # Scale proporsional supaya muat di dalam slot (lebar penuh, tinggi <= slot_height)
        scale = min(A4_WIDTH_PX / img.width, slot_height / img.height)
        new_w = max(1, round(img.width * scale))
        new_h = max(1, round(img.height * scale))
        resized = img.resize((new_w, new_h), Image.LANCZOS)

        x = (A4_WIDTH_PX - new_w) // 2
        y = y_cursor + (slot_height - new_h) // 2
        canvas.paste(resized, (x, y))

        y_cursor += slot_height + GAP_PX

    return canvas


def convert_one(pdf_path: Path, output_path: Path | None = None) -> Path:
    images = render_pdf_pages(pdf_path)
    result = stack_onto_a4(images)

    if output_path is None:
        output_path = pdf_path.with_suffix(".png")

    result.save(output_path, "PNG")
    return output_path


def collect_pdf_files(inputs: list[str]) -> list[Path]:
    files = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            files.extend(sorted(p.glob("*.pdf")))
        elif p.is_file() and p.suffix.lower() == ".pdf":
            files.append(p)
        else:
            print(f"⚠️  Lewati (bukan PDF atau tidak ditemukan): {item}")
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF (2 halaman) menjadi satu gambar PNG ukuran A4."
    )
    parser.add_argument("inputs", nargs="+", help="File PDF, beberapa file, atau folder")
    parser.add_argument("-o", "--output", help="Nama file output (hanya untuk 1 file input)")
    args = parser.parse_args()

    pdf_files = collect_pdf_files(args.inputs)

    if not pdf_files:
        print("Tidak ada file PDF yang ditemukan.")
        sys.exit(1)

    if args.output and len(pdf_files) > 1:
        print("⚠️  -o hanya bisa dipakai kalau input cuma 1 file. Diabaikan.")
        args.output = None

    for pdf_path in pdf_files:
        out = Path(args.output) if args.output else None
        result_path = convert_one(pdf_path, out)
        print(f"✅ {pdf_path.name} -> {result_path.name}")


if __name__ == "__main__":
    main()
