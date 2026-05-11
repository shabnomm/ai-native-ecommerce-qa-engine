import psycopg2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# ১. ডাটাবেস কানেকশন (ইউজার admin)
conn = psycopg2.connect(
    dbname="ecommerce_db", user="admin", password="password123", host="localhost", port="5432"
)
cur = conn.cursor()

# ২. প্রোডাক্টের নামগুলো নেওয়া (আমরা ১ লক্ষ প্রোডাক্টের ভেক্টর বানাবো)
print("📦 Fetching product names from database...")
cur.execute("SELECT product_id, product_name FROM products LIMIT 100000;")
data = cur.fetchall()
product_ids = [row[0] for row in data]
product_names = [row[1] for row in data]

# ৩. এআই মডেল দিয়ে নামগুলোকে ভেক্টরে রূপান্তর (Embedding)
# আমরা 'all-MiniLM-L6-v2' ব্যবহার করছি যা ছোট কিন্তু খুব ফাস্ট
print("⏳ Converting names to vectors (Embeddings)... This may take a few minutes.")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(product_names, show_progress_bar=True)

# ৪. FAISS ইনডেক্স তৈরি করা
dimension = embeddings.shape[1] # ভেক্টরের সাইজ (৩৮৪)
index = faiss.IndexFlatL2(dimension) # L2 Distance ব্যবহার করে মিল খুঁজবে
index.add(np.array(embeddings).astype('float32'))

# ৫. ইনডেক্স এবং আইডিগুলো সেভ করা (যাতে বারবার জেনারেট করতে না হয়)
print("💾 Saving Vector Database locally...")
faiss.write_index(index, "models/products_faiss.index")

with open("models/product_mapping.pkl", "wb") as f:
    pickle.dump({"ids": product_ids, "names": product_names}, f)

print("✅ Success! Your Vector DB is ready.")
cur.close()
conn.close()