# pdf2a4

Ubah file PDF (biasanya 2 halaman) dari kantor jadi **satu gambar PNG** ukuran A4,
dengan halaman ditumpuk atas-bawah. Cocok untuk kamu yang tiap hari download PDF
tapi butuhnya dalam bentuk gambar siap tempel/kirim.

## Install (sekali saja)

```bash
pip install pymupdf pillow
```

## Cara pakai

```bash
# satu file
python3 pdf2a4.py dokumen.pdf

# tentukan nama output sendiri
python3 pdf2a4.py dokumen.pdf -o hasil.png

# banyak file sekaligus
python3 pdf2a4.py file1.pdf file2.pdf file3.pdf

# semua PDF dalam satu folder (misal folder Downloads)
python3 pdf2a4.py ~/Downloads/
```

Hasil PNG otomatis tersimpan di sebelah file PDF aslinya dengan nama yang sama
(`dokumen.pdf` → `dokumen.png`), kecuali kamu pakai `-o`.

## Versi web (`index.html`) — untuk dipakai di banyak komputer

Kalau kamu sering pindah komputer, pakai `index.html` saja. Ini halaman
statis yang jalan 100% di browser (pakai pdf.js), tanpa install Python,
tanpa upload ke server manapun — semua proses terjadi lokal di browser kamu.

**Setup sekali (dari komputer manapun, sekali saja):**

1. Push repo ini ke GitHub.
2. Buka Settings → Pages di repo tersebut.
3. Pilih branch `main` (atau `master`), folder `/root` (atau `/docs` kalau
   `index.html` kamu taruh di situ) → Save.
4. GitHub akan kasih satu link, misalnya:
   `https://<username>.github.io/pdf2a4/`

**Pemakaian sehari-hari:** buka link itu di komputer manapun (kantor, rumah,
laptop lain) → drag-drop PDF → klik "Unduh PNG". Tidak perlu install atau
clone apapun lagi di komputer baru — cukup buka link, bahkan bisa
di-bookmark atau ditambahkan ke home screen HP.

Kalau mau lebih praktis lagi (misal tiap ada PDF baru masuk folder Download
langsung otomatis dikonversi tanpa buka browser sama sekali), itu perlu
script yang jalan di background per komputer — beri tahu aku kalau kamu mau
versi itu juga.

## Kenapa ditumpuk, bukan digabung 1 halaman = 1 gambar?

Karena kebutuhanmu: 2 halaman PDF → 1 lembar A4. Kalau ternyata kamu berubah
pikiran (misal mau tiap halaman jadi file gambar terpisah), tinggal ganti
parameter di `stack_onto_a4()` — atau minta aku buatkan mode `--split`.
