import pandas as pd

# আপনার ফাইলের আসল নাম এখানে দিন (যেমন: 'data/daraz_master_reviews.csv')
file_path = 'data/Daraz_Master_Reviews_bd.csv' 

try:
    df = pd.read_csv(file_path)
    
    # ১. অপ্রয়োজনীয় কলাম বাদ দেওয়া
    df = df[['review_text', 'rating']]
    
    # ২. মিসিং ভ্যালু থাকলে ড্রপ করা
    df = df.dropna()

    # ৩. রেটিং থেকে সেন্টিমেন্ট তৈরি (Labeling)
    # ৫ আর ৪ কে আমরা ১ (Positive) ধরবো, ১ আর ২ কে ০ (Negative)
    # ৩ রেটিং সচরাচর কনফিউজিং হয়, তাই প্রজেক্টের একুরেসির জন্য আমরা শুধু ৪, ৫ এবং ১, ২ নিয়ে কাজ করবো
    def label_sentiment(rating):
        if rating >= 4:
            return 1 # Positive
        elif rating <= 2:
            return 0 # Negative
        else:
            return None # Neutral

    df['sentiment'] = df['rating'].apply(label_sentiment)
    
    # ৩ রেটিং (None) গুলো বাদ দেওয়া
    df = df.dropna(subset=['sentiment'])
    
    # ডাটা টাইপ ঠিক করা
    df['sentiment'] = df['sentiment'].astype(int)

    print("✅ ডাটা ক্লিনিং এবং লেবেলিং শেষ!")
    print(df.head())
    print("\nSentiment Distribution:")
    print(df['sentiment'].value_counts())

    # পরিষ্কার করা ডাটা সেভ করে রাখা পরবর্তী ধাপের জন্য
    df.to_csv('data/cleaned_reviews.csv', index=False)
    print("\n💾 'data/cleaned_reviews.csv' নামে ফাইলটি সেভ হয়েছে।")

except Exception as e:
    print(f"❌ Error: {e}")