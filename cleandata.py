import pandas as pd
import re
from collections import Counter

# 1. GANTI NAMA FILE INI sesuai dengan nama file dataset 375 kamu
nama_file_mentah = "dataset.ai.indonesia_375.csv" 

# Membaca dataset
df = pd.read_csv(nama_file_mentah)
print("Kolom yang tersedia di dataset:", df.columns.tolist())
print(f"Total baris data awal: {len(df)}")

# Otomatis mendeteksi kolom username (Source) dan isi tweet
# (Sesuaikan jika nama kolom di CSV kamu berbeda, misal 'username' atau 'full_text')
col_user = next((c for c in df.columns if c.lower() in ['username', 'user', 'author', 'screen_name', 'user_screen_name']), df.columns[0])
col_text = next((c for c in df.columns if c.lower() in ['full_text', 'text', 'tweet', 'content', 'rawcontent']), df.columns[1])

print(f"Menggunakan kolom '{col_user}' sebagai Source dan '{col_text}' sebagai Teks Tweet.\n")

# Hapus baris kosong atau duplikat
df = df.dropna(subset=[col_user, col_text]).drop_duplicates(subset=[col_text])

edges = []
all_hashtags = []
all_words = []

# Daftar kata umum (stopwords sederhana) agar tidak ikut terhitung di topik populer
stopwords = {'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'untuk', 'dengan', 'pada', 'adalah', 
             'ada', 'tidak', 'yg', 'ga', 'gak', 'bisa', 'ya', 'aja', 'kalo', 'kalau', 'sama', 
             'jadi', 'juga', 'atau', 'akan', 'dalam', 'lebih', 'sudah', 'udah', 'saya', 'aku', 
             'kamu', 'dia', 'mereka', 'kita', 'nya', 'tp', 'tapi', 'karena', 'karna', 'buat', 
             'amp', 'rt', 'via', 'https', 'http', 'co', 't'}

for _, row in df.iterrows():
    # Bersihkan username pengirim (hapus @ dan spasi, ubah ke huruf kecil)
    source = str(row[col_user]).replace('@', '').strip().lower()
    text = str(row[col_text])
    
    # A. Ekstrak Mention (@username) -> menjadi Target
    mentions = re.findall(r'@([A-Za-z0-9_]+)', text)
    for target in mentions:
        target = target.lower()
        # Hindari self-loop (akun me-mention dirinya sendiri) jika tidak diperlukan
        if source != target:
            edges.append({'Source': source, 'Target': target})
            
    # B. Ekstrak Hashtag (#topik) -> untuk analisis "apa yang di-mention"
    hashtags = re.findall(r'#([A-Za-z0-9_]+)', text)
    all_hashtags.extend([f"#{h.lower()}" for h in hashtags])
    
    # C. Bersihkan teks untuk melihat kata/topik yang sering dibahas
    clean_text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) # hapus link
    clean_text = re.sub(r'@\w+|#\w+', '', clean_text) # hapus mention & hashtag
    clean_text = re.sub(r'[^a-zA-Z\s]', '', clean_text).lower() # hanya ambil huruf
    
    words = [w for w in clean_text.split() if len(w) > 2 and w not in stopwords]
    all_words.extend(words)

# 2. Simpan EDGES.CSV (Untuk di-import ke Gephi)
df_edges = pd.DataFrame(edges)
df_edges.to_csv("edges.csv", index=False)

# 3. Simpan NODES.CSV (Daftar unik semua aktor yang terlibat)
unique_nodes = set(df_edges['Source']).union(set(df_edges['Target']))
df_nodes = pd.DataFrame({'Id': list(unique_nodes), 'Label': list(unique_nodes)})
df_nodes.to_csv("nodes.csv", index=False)

# 4. Simpan HASHTAG & KATA POPULER (Untuk bahan pembahasan di Jurnal)
df_hashtags = pd.DataFrame(Counter(all_hashtags).most_common(20), columns=['Hashtag', 'Jumlah'])
df_hashtags.to_csv("top_hashtags.csv", index=False)

df_words = pd.DataFrame(Counter(all_words).most_common(20), columns=['Kata_Kunci', 'Jumlah'])
df_words.to_csv("top_topik_kata.csv", index=False)

print("=== PROSES SELESAI ===")
print(f"1. Total Nodes (Aktor unik): {len(df_nodes)}")
print(f"2. Total Edges (Interaksi Mention): {len(df_edges)}")
print("File 'edges.csv', 'nodes.csv', 'top_hashtags.csv', dan 'top_topik_kata.csv' berhasil dibuat!")