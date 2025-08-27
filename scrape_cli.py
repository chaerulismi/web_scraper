#!/usr/bin/env python3
"""
Command-line interface for the web scraper
"""

import argparse
import sys
from web_scraper import WebScraper
import json


def main():
    parser = argparse.ArgumentParser(
        description="Extract articles from websites using multiple methods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract articles from a single URL
  python scrape_cli.py https://example.com
  
  # Extract articles and save to specific file
  python scrape_cli.py https://example.com -o my_articles.json
  
  # Use specific extraction method
  python scrape_cli.py https://example.com --method newspaper3k
  
  # Extract from multiple URLs
  python scrape_cli.py https://site1.com https://site2.com
  
  # Show verbose output
  python scrape_cli.py https://example.com -v
        """
    )
    
    parser.add_argument('urls', nargs='+', help='URL(s) to scrape')
    parser.add_argument('-o', '--output', help='Output filename for articles')
    parser.add_argument('-m', '--method', 
                       choices=['auto', 'newspaper3k', 'rss', 'manual'],
                       default='auto',
                       help='Extraction method to use (default: auto)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Request timeout in seconds (default: 30)')
    parser.add_argument('--user-agent', 
                       help='Custom user agent string')
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize scraper
    scraper = WebScraper(
        user_agent=args.user_agent,
        timeout=args.timeout
    )
    
    all_articles = []
    
    try:
        for url in args.urls:
            print(f"\n{'='*60}")
            print(f"Processing: {url}")
            print(f"{'='*60}")
            
            # Extract articles based on method
            if args.method == 'auto':
                articles = scraper.extract_articles_auto(url)
            elif args.method == 'newspaper3k':
                articles = scraper.extract_articles_newspaper3k(url)
            elif args.method == 'rss':
                articles = scraper.extract_articles_rss(url)
            elif args.method == 'manual':
                articles = scraper.extract_articles_manual(url)
            
            if articles:
                print(f"✓ Found {len(articles)} articles")
                all_articles.extend(articles)
                
                # Show first few articles
                for i, article in enumerate(articles[:3], 1):
                    print(f"\n{i}. {article['title']}")
                    if article.get('summary'):
                        summary = article['summary'][:100] + '...' if len(article['summary']) > 100 else article['summary']
                        print(f"   Summary: {summary}")
                    print(f"   Method: {article['extraction_method']}")
                    if article.get('publish_date'):
                        print(f"   Date: {article['publish_date']}")
                
                if len(articles) > 3:
                    print(f"   ... and {len(articles) - 3} more articles")
            else:
                print("✗ No articles found")
        
        # Save all articles
        if all_articles:
            if args.output:
                filename = args.output
            else:
                filename = scraper.save_articles(all_articles)
            
            print(f"\n{'='*60}")
            print(f"Summary: Extracted {len(all_articles)} total articles")
            print(f"Saved to: {filename}")
            print(f"{'='*60}")
            
            # Show extraction method distribution
            methods = {}
            for article in all_articles:
                method = article.get('extraction_method', 'unknown')
                methods[method] = methods.get(method, 0) + 1
            
            print("\nExtraction method distribution:")
            for method, count in methods.items():
                print(f"  {method}: {count} articles")
        
        else:
            print("\nNo articles were extracted from any URL")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
