#!/usr/bin/env python3
"""
Example script demonstrating the web scraper usage
"""

from enhanced_scraper import EnhancedWebScraper
import json


def example_single_site():
    """Example: Extract articles from a single website"""
    print("=" * 60)
    print("EXAMPLE: Single Website Extraction")
    print("=" * 60)
    
    scraper = EnhancedWebScraper()
    
    try:
        # Extract articles from Hacker News
        url = "https://news.ycombinator.com/"
        print(f"Extracting articles from: {url}")
        
        articles = scraper.extract_articles_auto(url)
        
        if articles:
            print(f"✓ Found {len(articles)} articles")
            
            # Show first 3 articles
            for i, article in enumerate(articles[:3], 1):
                print(f"\n{i}. {article['title']}")
                if article.get('summary'):
                    summary = article['summary'][:100] + '...' if len(article['summary']) > 100 else article['summary']
                    print(f"   Summary: {summary}")
                print(f"   Method: {article['extraction_method']}")
            
            # Save articles
            filename = scraper.save_articles(articles)
            print(f"\nArticles saved to: {filename}")
        else:
            print("✗ No articles found")
    
    finally:
        scraper.close()


def example_multiple_sites():
    """Example: Extract articles from multiple websites"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Multiple Website Extraction")
    print("=" * 60)
    
    scraper = EnhancedWebScraper(rate_limit=1.0)  # 1 request per second
    
    try:
        # List of websites to scrape
        urls = [
            "https://dev.to/",
            "https://medium.com/"
        ]
        
        print(f"Extracting articles from {len(urls)} websites...")
        
        # Batch extraction
        results = scraper.extract_articles_batch(urls, method='auto')
        
        # Process results
        total_articles = 0
        for url, articles in results.items():
            print(f"\n{url}: {len(articles)} articles")
            total_articles += len(articles)
            
            # Show first article from each site
            if articles:
                article = articles[0]
                print(f"  Sample: {article['title']}")
                if article.get('summary'):
                    summary = article['summary'][:80] + '...' if len(article['summary']) > 80 else article['summary']
                    print(f"         {summary}")
        
        # Save all results
        filename = scraper.save_batch_results(results)
        print(f"\nTotal articles extracted: {total_articles}")
        print(f"Results saved to: {filename}")
    
    finally:
        scraper.close()


def example_custom_selectors():
    """Example: Using custom CSS selectors"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Custom CSS Selectors")
    print("=" * 60)
    
    scraper = EnhancedWebScraper()
    
    try:
        # Define custom selectors for a specific website
        custom_selectors = {
            'article': '.post, .entry, .article',
            'title': 'h1, h2, .post-title, .entry-title',
            'content': '.post-content, .entry-content, .article-content',
            'author': '.author, .byline, .post-author',
            'date': '.date, .published, .post-date',
            'summary': '.excerpt, .summary, .post-excerpt'
        }
        
        url = "https://example.com"  # Replace with actual website
        print(f"Extracting articles using custom selectors from: {url}")
        
        articles = scraper.extract_articles_manual(url, selectors=custom_selectors)
        
        if articles:
            print(f"✓ Found {len(articles)} articles using custom selectors")
            for article in articles[:2]:
                print(f"  - {article['title']}")
        else:
            print("✗ No articles found with custom selectors")
    
    finally:
        scraper.close()


def example_different_methods():
    """Example: Using different extraction methods"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Different Extraction Methods")
    print("=" * 60)
    
    scraper = EnhancedWebScraper()
    
    try:
        url = "https://news.ycombinator.com/"
        
        # Try different methods
        methods = ['newspaper3k', 'rss', 'manual']
        
        for method in methods:
            print(f"\nTrying method: {method}")
            try:
                if method == 'newspaper3k':
                    articles = scraper.extract_articles_newspaper3k(url)
                elif method == 'rss':
                    articles = scraper.extract_articles_rss(url)
                elif method == 'manual':
                    articles = scraper.extract_articles_manual(url)
                
                if articles:
                    print(f"  ✓ {method}: Found {len(articles)} articles")
                else:
                    print(f"  ✗ {method}: No articles found")
                    
            except Exception as e:
                print(f"  ✗ {method}: Failed - {e}")
    
    finally:
        scraper.close()


def main():
    """Run all examples"""
    print("Python Web Scraper - Examples")
    print("This script demonstrates various usage patterns of the web scraper.")
    print("Note: Some examples may fail if websites are unavailable or block scraping.")
    
    try:
        # Run examples
        example_single_site()
        example_multiple_sites()
        example_custom_selectors()
        example_different_methods()
        
        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\nError running examples: {e}")


if __name__ == "__main__":
    main()
