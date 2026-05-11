import psycopg2

conn_params = {
    "host": "localhost",
    "database": "ecommerce_db",
    "user": "admin",
    "password": "password123",
    "port": "5432"
}

def verify():
    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # ১. ইউজার সংখ্যা চেক
        cur.execute("SELECT COUNT(*) FROM users;")
        user_count = cur.fetchone()[0]

        # ২. প্রোডাক্ট সংখ্যা চেক
        cur.execute("SELECT COUNT(*) FROM products;")
        product_count = cur.fetchone()[0]

        # ৩. প্রতিটি ক্যাটাগরিতে কয়টি করে প্রোডাক্ট আছে
        cur.execute("SELECT category, COUNT(*) FROM products GROUP BY category;")
        categories = cur.fetchall()

        print("📊 --- Database Verification Report ---")
        print(f"Total Users: {user_count}")
        print(f"Total Products: {product_count}")
        print("\nProducts per Category:")
        for cat, count in categories:
            print(f"- {cat}: {count}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify()