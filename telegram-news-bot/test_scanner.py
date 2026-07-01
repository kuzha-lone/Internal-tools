"""
test_scanner.py — Quick standalone test to verify RSS feeds are working.
Run this BEFORE setting up Telegram to confirm articles are being fetched.

Usage:
  python test_scanner.py
"""
import sys
import io
# Force UTF-8 output on Windows to handle emoji in terminal
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from pathlib import Path

# Add bot root to path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from research.scanner import fetch_all

def main():
    print("=" * 60)
    print("  Telegram News Bot — RSS Scanner Test")
    print("=" * 60)
    print()

    articles = fetch_all()

    if not articles:
        print("❌ No articles found! Check your internet connection")
        print("   and verify the RSS feeds in config/sources.json")
        return

    print(f"\n✅ Found {len(articles)} total articles\n")
    print("-" * 60)

    # Show top 10
    for i, art in enumerate(articles[:10], 1):
        age = art.get("age_hours", 0)
        if age < 1:
            age_label = f"{int(age * 60)} min ago"
        else:
            age_label = f"{int(age)}h ago"

        print(f"{i:2}. [{art['source']}]")
        print(f"    {art['title']}")
        print(f"    Category: {art['category']}  |  Age: {age_label}")
        if art.get("summary"):
            preview = art["summary"][:100].replace("\n", " ")
            print(f"    Summary: {preview}...")
        print()

    print("-" * 60)
    print(f"Showing top 10 of {len(articles)} articles")
    print("If you see articles above, the scanner is working ✅")
    print("Next: fill in .env with your Telegram Bot Token and Channel ID")
    print("Then run: python main.py")

if __name__ == "__main__":
    main()
