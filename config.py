"""
Configuration file for the web scraper
Contains predefined selectors for popular websites
"""

# Predefined selectors for popular websites
WEBSITE_SELECTORS = {
    'medium.com': {
        'article': 'article, [data-testid="storyPreview"]',
        'title': 'h1, [data-testid="storyTitle"]',
        'content': '[data-testid="storyBody"], .story-content',
        'author': '[data-testid="authorName"], .author-name',
        'date': 'time, [data-testid="storyPublishDate"]',
        'summary': '[data-testid="storyDescription"], .story-description'
    },
    
    'dev.to': {
        'article': 'article, .crayons-story',
        'title': 'h2, .crayons-story__title',
        'content': '.crayons-story__snippet, .story-snippet',
        'author': '.crayons-story__author, .story-author',
        'date': 'time, .crayons-story__date',
        'summary': '.crayons-story__snippet, .story-snippet'
    },
    
    'hashnode.dev': {
        'article': '.blog-post-card, .post-card',
        'title': 'h2, .blog-post-card-title',
        'content': '.blog-post-card-excerpt, .post-excerpt',
        'author': '.blog-post-card-author, .author-name',
        'date': '.blog-post-card-date, .publish-date',
        'summary': '.blog-post-card-excerpt, .post-excerpt'
    },
    
    'news.ycombinator.com': {
        'article': '.athing, .storylink',
        'title': '.storylink, .titleline a',
        'content': '.subtext, .story-subtext',
        'author': '.hnuser, .author',
        'date': '.age, .time',
        'summary': '.subtext, .story-subtext'
    },
    
    'reddit.com': {
        'article': '[data-testid="post-container"], .Post',
        'title': 'h3, [data-testid="post-title"]',
        'content': '[data-testid="post-content"], .Post-content',
        'author': '[data-testid="post-author"], .Post-author',
        'date': 'time, [data-testid="post-timestamp"]',
        'summary': '[data-testid="post-content"], .Post-content'
    },
    
    'github.com': {
        'article': '.Box-row, .issue-row',
        'title': 'h3, .issue-title',
        'content': '.issue-body, .issue-description',
        'author': '.author, .issue-author',
        'date': 'time, .issue-date',
        'summary': '.issue-body, .issue-description'
    }
}

# Default selectors for unknown websites
DEFAULT_SELECTORS = {
    'article': 'article, .article, .post, .entry, .content, .story, .news-item',
    'title': 'h1, h2, h3, .title, .headline, .post-title, .entry-title',
    'content': '.content, .body, .text, .post-content, .entry-content, .story-content, .article-content',
    'author': '.author, .byline, .writer, .post-author, .entry-author',
    'date': '.date, .published, .time, .timestamp, .post-date, .entry-date',
    'summary': '.summary, .excerpt, .description, .post-excerpt, .entry-summary'
}

# RSS feed patterns for common websites
RSS_PATTERNS = {
    'medium.com': '/feed',
    'dev.to': '/feed',
    'hashnode.dev': '/rss.xml',
    'news.ycombinator.com': '/rss',
    'reddit.com': '/.rss',
    'github.com': '/releases.atom'
}

# User agents for different browsers
USER_AGENTS = {
    'chrome': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'firefox': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
    'safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'edge': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}

# Rate limiting settings (requests per second)
RATE_LIMITS = {
    'default': 1,  # 1 request per second
    'news_sites': 2,  # 2 requests per second for news sites
    'social_media': 0.5,  # 0.5 requests per second for social media
}

# Timeout settings
TIMEOUTS = {
    'default': 30,
    'slow_sites': 60,
    'fast_sites': 15
}

def get_selectors_for_domain(domain: str) -> dict:
    """
    Get selectors for a specific domain
    
    Args:
        domain: Domain name (e.g., 'medium.com')
        
    Returns:
        Dictionary of selectors or default selectors if not found
    """
    # Clean domain
    domain = domain.lower().replace('www.', '')
    
    # Check for exact match
    if domain in WEBSITE_SELECTORS:
        return WEBSITE_SELECTORS[domain]
    
    # Check for partial matches
    for key in WEBSITE_SELECTORS:
        if key in domain or domain in key:
            return WEBSITE_SELECTORS[key]
    
    # Return default selectors
    return DEFAULT_SELECTORS

def get_rss_url(base_url: str) -> str:
    """
    Get RSS feed URL for a website
    
    Args:
        base_url: Base URL of the website
        
    Returns:
        RSS feed URL or None if not found
    """
    from urllib.parse import urlparse
    
    domain = urlparse(base_url).netloc.lower().replace('www.', '')
    
    for pattern_domain, rss_path in RSS_PATTERNS.items():
        if pattern_domain in domain:
            return base_url.rstrip('/') + rss_path
    
    return None

def get_user_agent(browser: str = 'chrome') -> str:
    """
    Get user agent string for a specific browser
    
    Args:
        browser: Browser name ('chrome', 'firefox', 'safari', 'edge')
        
    Returns:
        User agent string
    """
    return USER_AGENTS.get(browser.lower(), USER_AGENTS['chrome'])

def get_rate_limit(domain: str) -> float:
    """
    Get rate limit for a specific domain
    
    Args:
        domain: Domain name
        
    Returns:
        Rate limit (requests per second)
    """
    domain = domain.lower()
    
    if any(site in domain for site in ['news', 'blog', 'article']):
        return RATE_LIMITS['news_sites']
    elif any(site in domain for site in ['reddit', 'twitter', 'facebook', 'instagram']):
        return RATE_LIMITS['social_media']
    else:
        return RATE_LIMITS['default']

def get_timeout(domain: str) -> int:
    """
    Get timeout for a specific domain
    
    Args:
        domain: Domain name
        
    Returns:
        Timeout in seconds
    """
    domain = domain.lower()
    
    if any(site in domain for site in ['github', 'stackoverflow', 'reddit']):
        return TIMEOUTS['slow_sites']
    elif any(site in domain for site in ['news', 'blog']):
        return TIMEOUTS['fast_sites']
    else:
        return TIMEOUTS['default']
