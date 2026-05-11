import psycopg2
from psycopg2.extras import execute_batch
import random
from datetime import datetime, timedelta

conn_params = {
    "host": "localhost", "database": "ecommerce_db",
    "user": "admin", "password": "password123", "port": "5432"
}

def generate_orders():
    conn = None
    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # ১. ইউজার এবং প্রোডাক্টের আইডিগুলো নিয়ে আসা
        cur.execute("SELECT user_id FROM users;")
        user_ids = [row[0] for row in cur.fetchall()]
        
        cur.execute("SELECT product_id, price FROM products;")
        products = cur.fetchall() # List of tuples (id, price)

        print(f"🛒 Generating 200,000 Orders for {len(user_ids)} users...")
        
        orders_data = []
        start_date = datetime.now() - timedelta(days=365) # গত ১ বছরের ডাটা

        for i in range(200000):
            u_id = random.choice(user_ids)
            p_id, price = random.choice(products)
            
            # র্যান্ডম তারিখ তৈরি করা
            random_days = random.randint(0, 365)
            order_date = start_date + timedelta(days=random_days)
            
            # কেনাকাটার পরিমাণ (টোটাল অ্যামাউন্ট)
            total_amount = float(price) # এখানে চাইলে কোয়ান্টিটি দিয়ে গুণ করা যায়
            
            orders_data.append((u_id, order_date, total_amount))

            # প্রতি ২০,০০০ অর্ডারে একবার ব্যাচ ইনসার্ট করা
            if len(orders_data) >= 20000:
                execute_batch(cur, "INSERT INTO orders (user_id, order_date, total_amount) VALUES (%s, %s, %s)", orders_data)
                orders_data = []
                print(f"✅ {i+1} orders inserted...")

        conn.commit()
        print("🎉 Success! 200,000 realistic orders generated.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    generate_orders()