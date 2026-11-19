import pandas as pd
import re

# Membaca file dataset 375 yang sudah ada
df = pd.read_csv("dataset_ai_indonesia_375.csv")

# Otomatis mendeteksi kolom username dan isi tweet
col_user = next((c for c in df.columns if c.lower() in ['username', 'user', 'author', 'screen_name', 'user_screen_name']), df.columns[0])
col_text = next((c for c in df.columns if c.lower() in ['full_text', 'text', 'tweet', 'content', 'rawcontent']), df.columns[1])

df = df.dropna(subset=[col_user, col_text]).drop_duplicates(subset=[col_text])

# Fungsi untuk membuat nodes & edges dari hasil filter kata kunci
def ekstrak_jaringan(data_filter, label_file):
    edges = []
    for _, row in data_filter.iterrows():
        source = str(row[col_user]).replace('@', '').strip().lower()
        text = str(row[col_text])
        mentions = re.findall(r'@([A-Za-z0-9_]+)', text)
        for target in mentions:
            target = target.lower()
            if source != target:
                edges.append({'Source': source, 'Target': target})
    
    df_edges = pd.DataFrame(edges)
    df_edges.to_csv(f"edges_{label_file}.csv", index=False)
    
    unique_nodes = set(df_edges['Source']).union(set(df_edges['Target'])) if not df_edges.empty else set()
    df_nodes = pd.DataFrame({'Id': list(unique_nodes), 'Label': list(unique_nodes)})
    df_nodes.to_csv(f"nodes_{label_file}.csv", index=False)
    print(f"Kata kunci '{label_file}': {len(data_filter)} tweet -> {len(df_nodes)} Nodes, {len(df_edges)} Edges")

# 1. Filter Kata Kunci Kedua (misal: "chatgpt" atau "gemini")
df_kata2 = df[df[col_text].str.contains('chatgpt|gemini|grok', case=False, na=False)]
ekstrak_jaringan(df_kata2, "kata2_tools_ai")

# 2. Filter Kata Kunci Pertama (sisanya yang membahas "artificial intelligence" / "ai" secara umum)
df_kata1 = df[~df[col_text].str.contains('chatgpt|gemini|grok', case=False, na=False)]
ekstrak_jaringan(df_kata1, "kata1_ai_umum")