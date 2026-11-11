import pandas as pd
import re

# 1. Baca dataset 400 data yang ada di folder VS Code
INPUT_FILE = "dataset_ai_indonesia_400.csv"
print(f"📖 Membaca file: {INPUT_FILE}...")

try:
    df = pd.read_csv(INPUT_FILE)
    print(f"✅ Total baris tweet terbaca: {len(df)}")
except FileNotFoundError:
    print(f"❌ File '{INPUT_FILE}' tidak ditemukan di folder yang sama!")
    exit()

edges = []
nodes = set()

# 2. Ekstraksi Source (pembuat tweet) dan Target (user yang dimention)
for idx, row in df.iterrows():
    source = str(row['username']).strip()
    tweet_text = str(row['tweet'])
    
    # Tambahkan pembuat tweet sebagai Node
    if source and source != 'nan':
        nodes.add(source)
    
    # Cari semua @mention di dalam teks tweet
    mentions = re.findall(r'@([A-Za-z0-9_]+)', tweet_text)
    for target in mentions:
        target = target.strip()
        # Cegah self-mention (me-mention akun sendiri)
        if target and target.lower() != source.lower():
            nodes.add(target)
            edges.append({
                'Source': source,
                'Target': target,
                'Type': 'Directed'
            })

# 3. Buat DataFrame untuk Nodes dan Edges
df_nodes = pd.DataFrame(list(nodes), columns=['Id'])
df_nodes['Label'] = df_nodes['Id']  # Label disamakan dengan Username/Id

df_edges = pd.DataFrame(edges)

# 4. Simpan ke file CSV khusus untuk Gephi
df_nodes.to_csv("nodes.csv", index=False)
df_edges.to_csv("edges.csv", index=False)

print("\n==========================================")
print("🎉 EKSTRAKSI GEPHI SELESAI!")
print("==========================================")
print(f"📊 Total Nodes (Aktor Unik)     : {len(df_nodes)}")
print(f"🔗 Total Edges (Interaksi Mention): {len(df_edges)}")
print("📁 File 'nodes.csv' dan 'edges.csv' berhasil dibuat di folder proyek!")