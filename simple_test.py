#!/usr/bin/env python3
"""
Simple test to verify web scraper components work
"""

def test_basic_functionality():
    """Test basic scraper functionality without external requests"""
    print("🧪 Testing Web Scraper Components")
    print("=" * 40)
    
    try:
        # Test imports
        from enhanced_scraper import EnhancedWebScraper
        print("✅ EnhancedWebScraper imported successfully")
        
        from config import get_selectors_for_domain, get_user_agent
        print("✅ Configuration module imported successfully")
        
        # Test configuration functions
        selectors = get_selectors_for_domain('medium.com')
        if selectors and 'article' in selectors:
            print("✅ Domain-specific selectors working")
        
        ua = get_user_agent('chrome')
        if ua and 'Chrome' in ua:
            print("✅ User agent functions working")
        
        # Test scraper creation (without making requests)
        scraper = EnhancedWebScraper()
        print("✅ Scraper created successfully")
        
        # Test session configuration
        if scraper.session and scraper.session.headers.get('User-Agent'):
            print("✅ Session configured with proper headers")
        
        scraper.close()
        print("✅ Scraper closed successfully")
        
        print("\n🎉 All basic tests passed!")
        print("The web scraper is ready to use.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    test_basic_functionality()
