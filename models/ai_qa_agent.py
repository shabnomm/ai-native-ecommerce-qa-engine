import json
from langchain_ollama import OllamaLLM
import semantic_search  # আপনার আগের সার্চ স্ক্রিপ্টটি ইমপোর্ট করছি

# ১. ওলামা মডেল সেটআপ (নিশ্চিত করুন llama3 ডাউনলোড করা আছে)
print("⏳ Initializing AI Auditor (Llama 3)...")
llm = OllamaLLM(model="llama3")

def run_agentic_qa_test(query):
    print(f"\n🚀 Starting Agentic QA Audit for query: '{query}'")
    print("=" * 60)

    # ২. আপনার লোকাল সিম্যান্টিক সার্চ ইঞ্জিন থেকে রেজাল্ট সংগ্রহ
    try:
        # k=3 মানে আমরা টপ ৩টি রেজাল্ট ভ্যালিডেশন করবো
        search_results = semantic_search.search_products(query, k=3)
        
        if not search_results:
            print("⚠️ No results found to audit.")
            return

    except Exception as e:
        print(f"❌ Error fetching search results: {e}")
        return

    # ৩. এআই এজেন্টের জন্য প্রম্পট (QA Roleplay)
    prompt = f"""
    SYSTEM ROLE: Senior Software Quality Assurance (SQA) Specialist.
    TASK: Audit the relevance of Semantic Search results for an E-commerce platform.

    USER SEARCH INPUT: "{query}"
    SEARCH ENGINE OUTPUT (JSON): {json.dumps(search_results, indent=2)}

    AUDIT CRITERIA:
    1. CONTEXTUAL RELEVANCE: Do the product names align with the user's intent?
    2. SCORE ANALYSIS: Assess if the L2 distance scores (lower is better) justify the ranking.
    3. FALSE POSITIVES: Identify any products that are completely unrelated.
    4. IMPROVEMENTS: Suggest how to improve the search accuracy for this specific case.

    OUTPUT FORMAT: 
    Please provide a structured 'QA AUDIT REPORT' with a final verdict: [PASS] or [FAIL].
    """

    # ৪. ওলামার মাধ্যমে অডিট রিপোর্ট জেনারেট করা
    print("🤖 AI Agent is analyzing the search logic...")
    report = llm.invoke(prompt)

    print("\n" + "📊" + " " + "FINAL QA AUDIT REPORT")
    print("-" * 60)
    print(report)
    print("-" * 60)

if __name__ == "__main__":
    # আপনি এখানে যেকোনো কি-ওয়ার্ড দিয়ে আপনার সিস্টেমকে চ্যালেঞ্জ করতে পারেন
    test_queries = [
        "Smart electronics for home",
        "Summer casual outfits",
        "Professional office wear"
    ]

    for q in test_queries:
        run_agentic_qa_test(q)