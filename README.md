# Analisis Sentralitas Jaringan Percakapan Publik Terhadap Topik Artificial Intelligence pada Platform X (Twitter)

Repositori ini berisi data dan skrip pemrosesan untuk penelitian **Social Network Analysis (SNA)** yang mengkaji struktur percakapan publik berbahasa Indonesia mengenai isu *Artificial Intelligence* (AI, ChatGPT, Gemini, OpenAI, Claude) di platform X (Twitter).

Penelitian ini memetakan interaksi antar-pengguna berdasarkan sebutan (*@mention*) untuk mengidentifikasi aktor kunci (*opinion leader*), perantara informasi (*bridge*), serta pola penyebaran wacana AI di Indonesia.

---

## 🚀 Alur Kerja Pemrosesan Data

```text
[ X (Twitter) API / Twscrape ]
              │
              ▼
  dataset_ai_indonesia_400.csv (374 raw tweets)
              │
              ▼
        cleandata.py (Python Parsing & Extraction)
              │
      ┌───────┴───────┐
      ▼               ▼
  nodes.csv       edges.csv
  (432 Aktor)    (128 Interaksi Mention)
      │               │
      └───────┬───────┘
              ▼
      [ Gephi 0.10+ Visualisasi & SNA ]

Data sudah disediakan jadi bisa diambil secara gratis dan open source
