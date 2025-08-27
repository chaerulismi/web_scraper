#!/usr/bin/env python3
"""
Enhanced web scraper with configuration-based selectors and better extraction
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
from config import (
    get_selectors_for_domain, 
    get_rss_url, 
    get_user_agent, 
    get_rate_limit, 
    get_timeout
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EnhancedWebScraper:
    """Enhanced web scraper with configuration-based selectors"""
    
    def __init__(self, user_agent: str = None, timeout: int = None, rate_limit: float = None):
        """
        Initialize the enhanced web scraper
        
        Args:
            user_agent: Custom user agent string
            timeout: Request timeout in seconds
            rate_limit: Rate limit (requests per second)
        """
        self.session = requests.Session()
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.last_request_time = 0
        
        # Set default user agent if none provided
        if user_agent is None:
            user_agent = get_user_agent('chrome')
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def _rate_limit(self):
        """Apply rate limiting between requests"""
        if self.rate_limit:
            time_since_last = time.time() - self.last_request_time
            min_interval = 1.0 / self.rate_limit
            
            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page with rate limiting
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            # Apply rate limiting
            self._rate_limit()
            
            # Get domain-specific timeout
            domain = urlparse(url).netloc
            timeout = self.timeout or get_timeout(domain)
            
            logger.info(f"Fetching content from: {url} (timeout: {timeout}s)")
            response = self.session.get(url, timeout=timeout)
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
        Extract articles using newspaper3k library
        
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
        Extract articles using manual CSS selectors with domain-specific configuration
        
        Args:
            url: URL to extract articles from
            selectors: Dictionary of CSS selectors for different elements
            
        Returns:
            List of article dictionaries
        """
        # Get domain-specific selectors if none provided
        if selectors is None:
            domain = urlparse(url).netloc
            selectors = get_selectors_for_domain(domain)
        
        soup = self.get_page_content(url)
        if not soup:
            return []
        
        try:
            logger.info(f"Extracting articles using manual selectors from: {url}")
            
            # Find all potential article containers
            article_containers = soup.select(selectors['article'])
            
            if not article_containers:
                # Fallback: look for any div with substantial text content
                article_containers = soup.find_all('div', class_=lambda x: x and any(word in x.lower() for word in ['article', 'post', 'content', 'entry', 'story', 'news']))
            
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
                
                # Try configuration-based RSS URL
                rss_url = get_rss_url(url)
                if rss_url:
                    articles = self.extract_articles_rss(rss_url)
                    if articles:
                        logger.info("Successfully extracted articles from configuration-based RSS feed")
                        return articles
        except Exception as e:
            logger.warning(f"RSS extraction failed: {e}")
        
        # Fallback to manual extraction with domain-specific selectors
        try:
            articles = self.extract_articles_manual(url)
            if articles:
                logger.info("Successfully extracted articles using manual selectors")
                return articles
        except Exception as e:
            logger.warning(f"Manual extraction failed: {e}")
        
        logger.warning("All extraction methods failed")
        return []
    
    def extract_articles_batch(self, urls: List[str], method: str = 'auto') -> Dict[str, List[Dict]]:
        """
        Extract articles from multiple URLs in batch
        
        Args:
            urls: List of URLs to extract articles from
            method: Extraction method to use
            
        Returns:
            Dictionary mapping URLs to lists of articles
        """
        results = {}
        
        for url in urls:
            logger.info(f"Processing URL {urls.index(url) + 1}/{len(urls)}: {url}")
            
            try:
                if method == 'auto':
                    articles = self.extract_articles_auto(url)
                elif method == 'newspaper3k':
                    articles = self.extract_articles_newspaper3k(url)
                elif method == 'rss':
                    articles = self.extract_articles_rss(url)
                elif method == 'manual':
                    articles = self.extract_articles_manual(url)
                else:
                    articles = self.extract_articles_auto(url)
                
                results[url] = articles
                
                # Be respectful - add delay between requests
                if len(urls) > 1:
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Failed to extract articles from {url}: {e}")
                results[url] = []
        
        return results
    
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
    
    def save_batch_results(self, batch_results: Dict[str, List[Dict]], filename: str = None) -> str:
        """
        Save batch extraction results to a JSON file
        
        Args:
            batch_results: Dictionary mapping URLs to lists of articles
            filename: Output filename (optional)
            
        Returns:
            Filename where results were saved
        """
        if filename is None:
            timestamp = int(time.time())
            filename = f"batch_articles_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(batch_results, f, indent=2, ensure_ascii=False)
            
            total_articles = sum(len(articles) for articles in batch_results.values())
            logger.info(f"Saved batch results with {total_articles} total articles to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to save batch results to {filename}: {e}")
            raise
    
    def close(self):
        """Close the session"""
        self.session.close()


def main():
    """Example usage of the EnhancedWebScraper class"""
    
    # Example websites to test
    test_urls = [
        "https://news.ycombinator.com/",
        "https://dev.to/",
        "https://medium.com/"
    ]
    
    # Initialize scraper with domain-specific settings
    scraper = EnhancedWebScraper()
    
    try:
        # Extract articles from each URL
        batch_results = scraper.extract_articles_batch(test_urls, method='auto')
        
        # Save results
        filename = scraper.save_batch_results(batch_results)
        
        # Print summary
        print(f"\n{'='*60}")
        print("EXTRACTION SUMMARY")
        print(f"{'='*60}")
        
        total_articles = 0
        for url, articles in batch_results.items():
            print(f"\n{url}: {len(articles)} articles")
            total_articles += len(articles)
            
            # Show first few articles
            for i, article in enumerate(articles[:2], 1):
                print(f"  {i}. {article['title']}")
                if article.get('summary'):
                    summary = article['summary'][:80] + '...' if len(article['summary']) > 80 else article['summary']
                    print(f"     {summary}")
        
        print(f"\nTotal articles extracted: {total_articles}")
        print(f"Results saved to: {filename}")
        
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
