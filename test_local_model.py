from transformers import pipeline
import os

# আপনার লোকাল মডেলের পাথ
model_path = "./models/daraz_sentiment_model"

try:
    print("⏳ Loading local model, please wait...")
    # মডেল লোড করা
    classifier = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
    
    # টেস্ট রিভিউ
    test_text = "অসাধারণ সার্ভিস, আমি খুবই সন্তুষ্ট!"
    result = classifier(test_text)
    
    print(f"\nReview: {test_text}")
    print(f"Prediction: {result}")
    
    if result[0]['label'] == 'LABEL_1':
        print("Final Verdict: Positive 😊")
    else:
        print("Final Verdict: Negative 😞")

except Exception as e:
    print(f"❌ Error: {e}")