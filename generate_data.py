import psycopg2
from psycopg2.extras import execute_batch
import random

conn_params = {
    "host": "localhost", "database": "ecommerce_db",
    "user": "admin", "password": "password123", "port": "5432"
}

# বড় প্রোডাক্ট লিস্ট (১০০+ প্রোডাক্টের আইডিয়া)
expanded_categories = {
    'Grocery': ['Basmati Rice', 'Chinigura Rice', 'Soybean Oil', 'Mustard Oil', 'Lentils', 'Moong Dal', 'Sugar', 'Brown Sugar', 'Iodized Salt', 'Pink Salt', 'Turmeric Powder', 'Chili Powder', 'Coriander Powder', 'Cumin', 'Tea Bags', 'Coffee Roast', 'Honey', 'Ghee', 'Atta', 'Maida', 'Suoji', 'Noodles', 'Pasta', 'Ketchup', 'Pickle'],
    'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Smart Watch', 'Bluetooth Speaker', 'Power Bank', 'Gaming Mouse', 'Mechanical Keyboard', 'LED Monitor', 'Router', 'Earbuds', 'Headphone', 'DSLR Camera', 'Webcam', 'Microphone', 'Hard Drive', 'SSD 500GB', 'USB Hub', 'Casing Fan', 'CPU Cooler', 'Graphic Card', 'RAM 16GB', 'Motherboard', 'UPS', 'Electric Kettle'],
    'Cosmetics': ['Face Wash', 'Sunscreen SPF 50', 'Moisturizer', 'Shampoo', 'Conditioner', 'Hair Oil', 'Lip Balm', 'Lipstick', 'Foundation', 'Eyeliner', 'Mascara', 'Body Lotion', 'Night Cream', 'Hand Cream', 'Face Mask', 'Serum', 'Toner', 'Perfume', 'Body Spray', 'Aftershave', 'Hair Gel', 'Scrub', 'Eye Cream', 'Cleanser', 'Nail Polish'],
    'Clothing': ['T-shirt', 'Polo Shirt', 'Panjabi', 'Pajama', 'Lungi', 'Salwar Kameez', 'Sari', 'Formal Shirt', 'Casual Shirt', 'Denim Jeans', 'Gabardine Pants', 'Socks', 'Leather Belt', 'Wallet', 'Hoodie', 'Jacket', 'Sweater', 'Cap', 'Scarf', 'Kurta', 'Leggings', 'Formal Trousers', 'Vest', 'Tie', 'Raincoat']
}

def seed_data():
    conn = None
    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        print("🧹 Cleaning old data...")
        cur.execute("TRUNCATE users, products, orders RESTART IDENTITY CASCADE;")

        # ১. ১০০,০০০ ইউজার তৈরি
        print("👤 Generating 100,000 Users...")
        users_data = []
        bd_names = ['Anika', 'Rahim', 'Sadiya', 'Tanvir', 'Mehedi', 'Sumaiya', 'Arif', 'Nusrat', 'Fahim', 'Jannat']
        last_names = ['Islam', 'Ahmed', 'Hossain', 'Akter', 'Rahman', 'Uddin', 'Khan']
        cities = ['Dhaka', 'Chittagong', 'Sylhet', 'Rajshahi', 'Khulna', 'Barisal', 'Gazipur', 'Narayanganj', 'Comilla', 'Bogura']

        for i in range(100000):
            name = f"{random.choice(bd_names)} {random.choice(last_names)}"
            email = f"user_{i}_{random.randint(10, 99)}@shonchoi.com"
            address = f"House {random.randint(1, 100)}, Road {random.randint(1, 20)}, Sector {random.randint(1, 15)}"
            city = random.choice(cities)
            users_data.append((name, email, address, city))

        execute_batch(cur, "INSERT INTO users (name, email, address, city) VALUES (%s, %s, %s, %s)", users_data, page_size=10000)

        # ২. ১০০+ প্রোডাক্ট তৈরি
        print("📦 Generating 100+ Products...")
        products_data = []
        for category, items in expanded_categories.items():
            for item in items:
                price = float(random.randint(40, 120000)) if category == 'Electronics' else float(random.randint(40, 5000))
                stock = random.randint(20, 500)
                products_data.append((item, category, price, stock))
        
        execute_batch(cur, "INSERT INTO products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)", products_data)

        conn.commit()
        print(f"✅ Success! 100,000 Users and {len(products_data)} Products added.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    seed_data()