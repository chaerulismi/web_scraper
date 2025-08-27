# Python Web Scraper

A powerful and flexible Python web scraper designed to extract main articles from websites using multiple extraction methods.

## Features

- **Multiple Extraction Methods**: Automatically tries different methods to extract articles
- **Smart Fallbacks**: Falls back to alternative methods if the primary method fails
- **Domain-Specific Configuration**: Pre-configured selectors for popular websites
- **Rate Limiting**: Built-in rate limiting to be respectful to websites
- **Batch Processing**: Extract articles from multiple URLs at once
- **Multiple Output Formats**: Save results in JSON format
- **Command-Line Interface**: Easy-to-use CLI for quick scraping tasks

## Extraction Methods

1. **newspaper3k**: Best for news sites and blogs
2. **RSS Feeds**: Extract from RSS/Atom feeds when available
3. **Manual Selectors**: Use CSS selectors with domain-specific configurations
4. **Auto-Detection**: Automatically chooses the best method for each website

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd web_scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from web_scraper import WebScraper

# Initialize scraper
scraper = WebScraper()

# Extract articles from a website
articles = scraper.extract_articles_auto("https://example.com")

# Save articles
filename = scraper.save_articles(articles)
print(f"Articles saved to: {filename}")

# Clean up
scraper.close()
```

### Command Line Usage

```bash
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
```

## Advanced Usage

### Enhanced Scraper with Configuration

```python
from enhanced_scraper import EnhancedWebScraper

# Initialize enhanced scraper
scraper = EnhancedWebScraper(
    user_agent="custom-user-agent",
    timeout=60,
    rate_limit=1.0  # 1 request per second
)

# Extract articles from multiple URLs
urls = [
    "https://news.ycombinator.com/",
    "https://dev.to/",
    "https://medium.com/"
]

# Batch extraction
results = scraper.extract_articles_batch(urls, method='auto')

# Save batch results
filename = scraper.save_batch_results(results)
print(f"Batch results saved to: {filename}")

scraper.close()
```

### Custom Selectors

```python
from web_scraper import WebScraper

scraper = WebScraper()

# Define custom selectors
custom_selectors = {
    'article': '.my-article, .post-item',
    'title': 'h2, .post-title',
    'content': '.post-content, .article-body',
    'author': '.author-name, .byline',
    'date': '.publish-date, time',
    'summary': '.excerpt, .post-summary'
}

# Extract using custom selectors
articles = scraper.extract_articles_manual(
    "https://example.com", 
    selectors=custom_selectors
)
```

## Supported Websites

The scraper comes with pre-configured selectors for popular websites:

- **Medium** (`medium.com`)
- **Dev.to** (`dev.to`)
- **Hashnode** (`hashnode.dev`)
- **Hacker News** (`news.ycombinator.com`)
- **Reddit** (`reddit.com`)
- **GitHub** (`github.com`)

## Output Format

Articles are extracted with the following structure:

```json
{
  "title": "Article Title",
  "text": "Full article content...",
  "summary": "Article summary or excerpt",
  "author": "Author name",
  "date": "Publication date",
  "url": "Article URL",
  "extraction_method": "Method used to extract",
  "publish_date": "ISO formatted date",
  "authors": ["Author 1", "Author 2"],
  "top_image": "Featured image URL",
  "meta_description": "Meta description",
  "meta_keywords": "Meta keywords",
  "tags": ["tag1", "tag2"]
}
```

## Configuration

### Rate Limiting

```python
# 1 request per second (default)
scraper = EnhancedWebScraper(rate_limit=1.0)

# 2 requests per second
scraper = EnhancedWebScraper(rate_limit=2.0)

# 0.5 requests per second (every 2 seconds)
scraper = EnhancedWebScraper(rate_limit=0.5)
```

### Timeouts

```python
# 30 seconds (default)
scraper = EnhancedWebScraper(timeout=30)

# 60 seconds for slow sites
scraper = EnhancedWebScraper(timeout=60)
```

### User Agents

```python
from config import get_user_agent

# Use different browser user agents
chrome_ua = get_user_agent('chrome')
firefox_ua = get_user_agent('firefox')
safari_ua = get_user_agent('safari')
edge_ua = get_user_agent('edge')

scraper = EnhancedWebScraper(user_agent=chrome_ua)
```

## Best Practices

1. **Be Respectful**: Use rate limiting and delays between requests
2. **Check robots.txt**: Respect website crawling policies
3. **Handle Errors**: Always use try-catch blocks and handle exceptions
4. **Clean Up**: Close scraper sessions when done
5. **Test First**: Test on a small number of URLs before large-scale scraping

## Error Handling

```python
try:
    articles = scraper.extract_articles_auto(url)
    if articles:
        print(f"Successfully extracted {len(articles)} articles")
    else:
        print("No articles found")
except Exception as e:
    print(f"Error extracting articles: {e}")
finally:
    scraper.close()
```

## Troubleshooting

### Common Issues

1. **No articles found**: Try different extraction methods or check if the website structure has changed
2. **Rate limiting**: Reduce the rate limit or add delays between requests
3. **Timeout errors**: Increase the timeout value for slow-loading websites
4. **Permission denied**: Check if the website blocks scraping or requires authentication

### Debug Mode

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)

# Or use verbose mode in CLI
python scrape_cli.py https://example.com -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Update tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes. Always respect website terms of service and robots.txt files. Be mindful of rate limiting and don't overload websites with requests.