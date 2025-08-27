#!/usr/bin/env python3
"""
Test script to verify web scraper setup
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import requests
        print("✓ requests imported")
    except ImportError as e:
        print(f"✗ requests failed: {e}")
        return False
    
    try:
        import bs4
        print("✓ beautifulsoup4 imported")
    except ImportError as e:
        print(f"✗ beautifulsoup4 failed: {e}")
        return False
    
    try:
        import newspaper
        print("✓ newspaper3k imported")
    except ImportError as e:
        print(f"✗ newspaper3k failed: {e}")
        return False
    
    try:
        import feedparser
        print("✓ feedparser imported")
    except ImportError as e:
        print(f"✗ feedparser failed: {e}")
        return False
    
    try:
        from enhanced_scraper import EnhancedWebScraper
        print("✓ EnhancedWebScraper imported")
    except ImportError as e:
        print(f"✗ EnhancedWebScraper failed: {e}")
        return False
    
    try:
        from config import get_selectors_for_domain
        print("✓ config module imported")
    except ImportError as e:
        print(f"✗ config module failed: {e}")
        return False
    
    return True


def test_scraper_creation():
    """Test that scraper can be created"""
    print("\nTesting scraper creation...")
    
    try:
        from enhanced_scraper import EnhancedWebScraper
        scraper = EnhancedWebScraper()
        print("✓ EnhancedWebScraper created successfully")
        scraper.close()
        return True
    except Exception as e:
        print(f"✗ Failed to create scraper: {e}")
        return False


def test_config_functions():
    """Test configuration functions"""
    print("\nTesting configuration functions...")
    
    try:
        from config import get_selectors_for_domain, get_user_agent
        
        # Test selectors
        selectors = get_selectors_for_domain('medium.com')
        if selectors and 'article' in selectors:
            print("✓ Domain selectors working")
        else:
            print("✗ Domain selectors failed")
            return False
        
        # Test user agent
        ua = get_user_agent('chrome')
        if ua and 'Chrome' in ua:
            print("✓ User agent functions working")
        else:
            print("✗ User agent functions failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Web Scraper Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test scraper creation
    if not test_scraper_creation():
        all_passed = False
    
    # Test configuration
    if not test_config_functions():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your web scraper is ready to use.")
        print("\nYou can now run:")
        print("  python web_scraper.py")
        print("  python enhanced_scraper.py")
        print("  python scrape_cli.py")
        print("  python example.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 50)


if __name__ == "__main__":
    main()
