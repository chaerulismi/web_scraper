#!/usr/bin/env python3
"""
Web Scraper for extracting main articles from websites
Supports multiple extraction methods and website types
"""

import requests
from bs4 import BeautifulSoup
import newspaper
import feedparser
from urllib.parse import urljoin, urlparse
import time
import json
from typing import List, Dict, Optional, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WebScraper:
    """Main web scraper class for extracting articles from websites"""
    
    def __init__(self, user_agent: str = None, timeout: int = 30):
        """
        Initialize the web scraper
        
        Args:
            user_agent: Custom user agent string
            timeout: Request timeout in seconds
        """
        self.session = requests.Session()
        self.timeout = timeout
        
        # Set default user agent if none provided
        if user_agent is None:
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            logger.info(f"Fetching content from: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Check if content is HTML
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                logger.warning(f"Content is not HTML: {content_type}")
                return None
            
            soup = BeautifulSoup(response.content, 'lxml')
            return soup
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None
    
    def extract_articles_newspaper3k(self, url: str) -> List[Dict]:
        """
        Extract articles using newspaper3k library (good for news sites)
        
        Args:
            url: URL to extract articles from
            
        Returns:
            List of article dictionaries
        """
        try:
            logger.info(f"Extracting articles using newspaper3k from: {url}")
            
            # Build the newspaper
            paper = newspaper.build(url, memoize_articles=False)
            
            articles = []
            for article in paper.articles:
                try:
                    # Download and parse the article
                    article.download()
                    article.parse()
                    
                    if article.title and article.text:
                        article_data = {
                            'title': article.title.strip(),
                            'text': article.text.strip(),
                            'url': article.url,
                            'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                            'authors': list(article.authors) if article.authors else [],
                            'top_image': article.top_image,
                            'meta_description': article.meta_description,
                            'meta_keywords': list(article.meta_keywords) if article.meta_keywords else [],
                            'tags': list(article.tags) if article.tags else [],
                            'extraction_method': 'newspaper3k'
                        }
                        articles.append(article_data)
                        
                except Exception as e:
                    logger.warning(f"Failed to process article {article.url}: {e}")
                    continue
            
            logger.info(f"Extracted {len(articles)} articles using newspaper3k")
            return articles
            
        except Exception as e:
            logger.error(f"Failed to extract articles using newspaper3k from {url}: {e}")
            return []
    
    def extract_articles_rss(self, url: str) -> List[Dict]:
        """
        Extract articles from RSS feeds
        
        Args:
            url: RSS feed URL
            
        Returns:
            List of article dictionaries
        """
        try:
            logger.info(f"Extracting articles from RSS feed: {url}")
            
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries:
                article_data = {
                    'title': entry.title.strip() if hasattr(entry, 'title') else None,
                    'text': entry.summary.strip() if hasattr(entry, 'summary') else None,
                    'url': entry.link if hasattr(entry, 'link') else None,
                    'publish_date': entry.published if hasattr(entry, 'published') else None,
                    'authors': [author.name for author in entry.authors] if hasattr(entry, 'authors') else [],
                    'extraction_method': 'rss'
                }
                
                if article_data['title'] and article_data['text']:
                    articles.append(article_data)
            
            logger.info(f"Extracted {len(articles)} articles from RSS feed")
            return articles
            
        except Exception as e:
            logger.error(f"Failed to extract articles from RSS feed {url}: {e}")
            return []
    
    def extract_articles_manual(self, url: str, selectors: Dict[str, str] = None) -> List[Dict]:
        """
        Extract articles using manual CSS selectors
        
        Args:
            url: URL to extract articles from
            selectors: Dictionary of CSS selectors for different elements
            
        Returns:
            List of article dictionaries
        """
        # Default selectors for common article patterns
        if selectors is None:
            selectors = {
                'article': 'article, .article, .post, .entry, .content',
                'title': 'h1, h2, .title, .headline',
                'content': '.content, .body, .text, .post-content, .entry-content',
                'author': '.author, .byline, .writer',
                'date': '.date, .published, .time, .timestamp',
                'summary': '.summary, .excerpt, .description'
            }
        
        soup = self.get_page_content(url)
        if not soup:
            return []
        
        try:
            logger.info(f"Extracting articles using manual selectors from: {url}")
            
            # Find all potential article containers
            article_containers = soup.select(selectors['article'])
            
            if not article_containers:
                # Fallback: look for any div with substantial text content
                article_containers = soup.find_all('div', class_=lambda x: x and any(word in x.lower() for word in ['article', 'post', 'content', 'entry']))
            
            articles = []
            
            for container in article_containers:
                try:
                    # Extract title
                    title_elem = container.select_one(selectors['title'])
                    title = title_elem.get_text(strip=True) if title_elem else None
                    
                    # Extract content
                    content_elem = container.select_one(selectors['content'])
                    if not content_elem:
                        # Fallback: use the container itself
                        content_elem = container
                    
                    content = content_elem.get_text(strip=True) if content_elem else None
                    
                    # Extract author
                    author_elem = container.select_one(selectors['author'])
                    author = author_elem.get_text(strip=True) if author_elem else None
                    
                    # Extract date
                    date_elem = container.select_one(selectors['date'])
                    date = date_elem.get_text(strip=True) if date_elem else None
                    
                    # Extract summary
                    summary_elem = container.select_one(selectors['summary'])
                    summary = summary_elem.get_text(strip=True) if summary_elem else None
                    
                    # Only add if we have at least title and some content
                    if title and content and len(content) > 100:
                        article_data = {
                            'title': title,
                            'text': content,
                            'summary': summary,
                            'author': author,
                            'date': date,
                            'url': url,
                            'extraction_method': 'manual_selectors'
                        }
                        articles.append(article_data)
                        
                except Exception as e:
                    logger.warning(f"Failed to process article container: {e}")
                    continue
            
            logger.info(f"Extracted {len(articles)} articles using manual selectors")
            return articles
            
        except Exception as e:
            logger.error(f"Failed to extract articles using manual selectors from {url}: {e}")
            return []
    
    def extract_articles_auto(self, url: str) -> List[Dict]:
        """
        Automatically detect and extract articles using multiple methods
        
        Args:
            url: URL to extract articles from
            
        Returns:
            List of article dictionaries
        """
        logger.info(f"Attempting automatic article extraction from: {url}")
        
        articles = []
        
        # Try newspaper3k first (best for news sites)
        try:
            articles = self.extract_articles_newspaper3k(url)
            if articles:
                logger.info("Successfully extracted articles using newspaper3k")
                return articles
        except Exception as e:
            logger.warning(f"newspaper3k failed: {e}")
        
        # Try RSS feed detection
        try:
            # Check if the page has RSS feed links
            soup = self.get_page_content(url)
            if soup:
                rss_links = soup.find_all('link', {'type': 'application/rss+xml'})
                if rss_links:
                    rss_url = urljoin(url, rss_links[0]['href'])
                    articles = self.extract_articles_rss(rss_url)
                    if articles:
                        logger.info("Successfully extracted articles from RSS feed")
                        return articles
        except Exception as e:
            logger.warning(f"RSS extraction failed: {e}")
        
        # Fallback to manual extraction
        try:
            articles = self.extract_articles_manual(url)
            if articles:
                logger.info("Successfully extracted articles using manual selectors")
                return articles
        except Exception as e:
            logger.warning(f"Manual extraction failed: {e}")
        
        logger.warning("All extraction methods failed")
        return []
    
    def save_articles(self, articles: List[Dict], filename: str = None) -> str:
        """
        Save extracted articles to a JSON file
        
        Args:
            articles: List of article dictionaries
            filename: Output filename (optional)
            
        Returns:
            Filename where articles were saved
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"articles_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(articles)} articles to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to save articles to {filename}: {e}")
            raise
    
    def close(self):
        """Close the session"""
        self.session.close()


def main():
    """Example usage of the WebScraper class"""
    
    # Example websites to test
    test_urls = [
        "https://news.ycombinator.com/",
        "https://techcrunch.com/",
        "https://www.theverge.com/"
    ]
    
    scraper = WebScraper()
    
    try:
        for url in test_urls:
            print(f"\n{'='*60}")
            print(f"Extracting articles from: {url}")
            print(f"{'='*60}")
            
            # Try automatic extraction
            articles = scraper.extract_articles_auto(url)
            
            if articles:
                print(f"Found {len(articles)} articles:")
                for i, article in enumerate(articles[:3], 1):  # Show first 3 articles
                    print(f"\n{i}. {article['title']}")
                    if article.get('summary'):
                        print(f"   Summary: {article['summary'][:100]}...")
                    print(f"   Method: {article['extraction_method']}")
                
                # Save articles
                filename = scraper.save_articles(articles)
                print(f"\nArticles saved to: {filename}")
            else:
                print("No articles found")
            
            # Be respectful - add delay between requests
            time.sleep(2)
    
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
