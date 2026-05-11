import psycopg2

conn_params = {
    "host": "localhost",
    "database": "ecommerce_db",
    "user": "admin",
    "password": "password123",
    "port": "5432"
}

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            address TEXT,
            city VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(200),
            category VARCHAR(100),
            price DECIMAL(10, 2),
            stock_quantity INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10, 2)
        )
        """
    )
    
    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        
        for command in commands:
            cur.execute(command)
        
        cur.close()
        conn.commit()
        print("✅ Success: Tables created in ecommerce_db!")
    except Exception as error:
        print(f"❌ Error: {error}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_tables()