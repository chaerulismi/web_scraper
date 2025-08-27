#!/usr/bin/env python3
"""
Quick demo of the web scraper
"""

from enhanced_scraper import EnhancedWebScraper
import json


def quick_demo():
    """Quick demo of article extraction"""
    print("🚀 Web Scraper Quick Demo")
    print("=" * 40)
    
    scraper = EnhancedWebScraper()
    
    try:
        # Try to extract articles from Hacker News (usually fast)
        url = "https://id.wikipedia.org/wiki/Sureq_Galigo"
        print(f"Extracting articles from: {url}")
        
        articles = scraper.extract_articles_auto(url)
        
        if articles:
            print(f"✅ Successfully extracted {len(articles)} articles!")
            
            # Show first 3 articles
            print("\n📰 Sample Articles:")
            for i, article in enumerate(articles[:3], 1):
                print(f"\n{i}. {article['title']}")
                if article.get('summary'):
                    summary = article['summary'][:80] + '...' if len(article['summary']) > 80 else article['summary']
                    print(f"   {summary}")
                print(f"   Method: {article['extraction_method']}")
            
            # Save articles
            filename = scraper.save_articles(articles)
            print(f"\n💾 Articles saved to: {filename}")
            
            # Show file info
            with open(filename, 'r') as f:
                data = json.load(f)
                print(f"📊 File contains {len(data)} articles")
                
        else:
            print("❌ No articles found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        scraper.close()
        print("\n✨ Demo completed!")


if __name__ == "__main__":
    quick_demo()
