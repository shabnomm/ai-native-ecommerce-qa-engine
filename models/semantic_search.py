import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# ১. মডেল এবং ডাটা লোড করা (একবার লোড হবে যাতে বারবার সময় না লাগে)
print("⏳ Loading Semantic Search Engine...")
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("models/products_faiss.index")

with open("models/product_mapping.pkl", "rb") as f:
    mapping = pickle.load(f)

product_names = mapping['names']
product_ids = mapping['ids']

def search_products(query, k=5):
    """
    এই ফাংশনটি কুয়েরি নিয়ে টপ k সংখ্যক রেজাল্ট একটি লিস্ট হিসেবে রিটার্ন করে।
    এটি এখন ai_qa_agent.py এর সাথে কাজ করার জন্য উপযুক্ত।
    """
    # ইউজারের কুয়েরিকে ভেক্টরে রূপান্তর
    query_vector = model.encode([query]).astype('float32')
    
    # ভেক্টর ডাটাবেসে সার্চ করা
    distances, indices = index.search(query_vector, k)
    
    results = []
    for i in range(k):
        idx = indices[0][i]
        results.append({
            "product_id": int(product_ids[idx]),
            "product_name": product_names[idx],
            "confidence_score": round(float(distances[0][i]), 4)
        })
    
    return results

# ২. স্ক্রিপ্টটি যদি সরাসরি রান করা হয় (Testing purpose)
if __name__ == "__main__":
    while True:
        user_query = input("\n👉 কি প্রোডাক্ট খুঁজছেন? (Exit লিখে বের হয়ে যান): ")
        if user_query.lower() == 'exit':
            break
            
        search_res = search_products(user_query)
        
        print(f"\n🔍 Search Results for: '{user_query}'")
        print("-" * 50)
        for res in search_res:
            print(f"ID: {res['product_id']} | Name: {res['product_name']} | Score: {res['confidence_score']}")