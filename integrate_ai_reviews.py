import pandas as pd
import psycopg2
from transformers import pipeline
import random
from tqdm import tqdm
import os

# ১. পাথ এবং কনফিগারেশন সেটআপ
MODEL_PATH = "./models/daraz_sentiment_model"
REVIEWS_CSV = "data/Daraz_Master_Reviews_bd.csv"

# ২. লোকাল এআই মডেল লোড করা
print("⏳ Loading your local AI model from models folder...")
try:
    classifier = pipeline("sentiment-analysis", model=MODEL_PATH, tokenizer=MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit()

# ৩. ডাটাবেস কানেকশন (ইউজার: admin)
try:
    conn = psycopg2.connect(
        dbname="ecommerce_db", 
        user="admin",         # আপনার ইনস্পেক্ট করা ইউজার
        password="password123", # আপনার ডাটাবেসের পাসওয়ার্ড এখানে দিন
        host="localhost", 
        port="5432"
    )
    cur = conn.cursor()
    print("✅ Connected to PostgreSQL database as 'admin'")

    # ৪. ডাটাবেস কলাম চেক ও তৈরি (সেফটি চেক)
    cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS review_text TEXT;")
    cur.execute("ALTER TABLE orders ADD COLUMN IF NOT EXISTS sentiment INT;")
    conn.commit()

    # ৫. Kaggle থেকে রিভিউ ডাটা লোড করা
    if os.path.exists(REVIEWS_CSV):
        reviews_df = pd.read_csv(REVIEWS_CSV)
        # শুধু বাংলা রিভিউগুলো নেওয়া (NaN বাদ দিয়ে)
        bangla_reviews = reviews_df['review_text'].dropna().tolist()
        print(f"✅ Loaded {len(bangla_reviews)} reviews from CSV.")
    else:
        print(f"❌ CSV file not found at {REVIEWS_CSV}")
        exit()

    # ৬. ডাটাবেস থেকে অর্ডার আইডি সংগ্রহ করা
    # টেস্টের জন্য প্রথমে ১০০ বা ৫০০ দিয়ে ট্রাই করতে পারেন (LIMIT 500)
    limit_count = 1000 
    cur.execute(f"SELECT order_id FROM orders WHERE review_text IS NULL LIMIT {limit_count};")
    order_ids = [row[0] for row in cur.fetchall()]

    if not order_ids:
        print("ℹ️ No orders found that need reviews.")
    else:
        print(f"🚀 Processing {len(order_ids)} orders with AI...")

        # ৭. লুপ চালিয়ে রিভিউ জেনারেট ও আপডেট করা
        for o_id in tqdm(order_ids):
            # র্যান্ডমলি একটি বাংলা রিভিউ পছন্দ করা
            random_review = random.choice(bangla_reviews)
            
            # এআই দিয়ে সেন্টিমেন্ট প্রেডিক্ট করা (৫১২ অক্ষরের বেশি হলে কেটে ছোট করা)
            prediction = classifier(random_review[:512])[0]
            
            # LABEL_1 হলে ১ (Positive), অন্যথায় ০ (Negative)
            sentiment_value = 1 if prediction['label'] == 'LABEL_1' else 0
            
            # ডাটাবেস আপডেট কমান্ড
            cur.execute(
                "UPDATE orders SET review_text = %s, sentiment = %s WHERE order_id = %s",
                (random_review, sentiment_value, o_id)
            )

        # সব পরিবর্তন সেভ করা
        conn.commit()
        print(f"\n✨ Success! {len(order_ids)} orders updated with AI reviews and sentiments.")

except Exception as db_err:
    print(f"❌ Database error: {db_err}")

finally:
    if 'conn' in locals():
        cur.close()
        conn.close()
        print("🔌 Database connection closed.")