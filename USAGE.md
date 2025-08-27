# Web Scraper Usage Guide

## 🚀 **How to Use the Virtual Environment**

### **Method 1: Use the Run Script (Recommended)**
```bash
# Run any Python script with virtual environment automatically activated
./run.sh demo.py
./run.sh example.py
./run.sh scrape_cli.py https://example.com
```

### **Method 2: Manual Activation**
```bash
# Activate virtual environment
source venv/bin/activate

# Your prompt will change to show (venv)
(venv) ➜ web_scraper

# Run Python scripts
python demo.py
python example.py
python scrape_cli.py https://example.com

# Deactivate when done
deactivate
```

### **Method 3: Use the Activation Script**
```bash
# Run the activation script
./activate.sh

# This will activate the environment and show you available commands
# Then run your scripts normally
python demo.py
```

## 📋 **Available Scripts**

| Script | Description | Usage |
|--------|-------------|-------|
| `demo.py` | Quick demo (fastest) | `./run.sh demo.py` |
| `example.py` | Full examples | `./run.sh example.py` |
| `scrape_cli.py` | Command-line interface | `./run.sh scrape_cli.py <url>` |
| `enhanced_scraper.py` | Advanced scraper | `./run.sh enhanced_scraper.py` |
| `web_scraper.py` | Basic scraper | `./run.sh web_scraper.py` |
| `test_setup.py` | Test setup | `./run.sh test_setup.py` |

## 🔧 **Quick Start Examples**

### **1. Quick Demo (Fastest)**
```bash
./run.sh demo.py
```

### **2. Extract Articles from a Website**
```bash
./run.sh scrape_cli.py https://news.ycombinator.com
```

### **3. Extract with Specific Method**
```bash
./run.sh scrape_cli.py https://example.com --method newspaper3k
```

### **4. Extract from Multiple Sites**
```bash
./run.sh scrape_cli.py https://site1.com https://site2.com
```

### **5. Save to Specific File**
```bash
./run.sh scrape_cli.py https://example.com -o my_articles.json
```

## ⚠️ **Important Notes**

1. **Always use the virtual environment** - either through `./run.sh` or by activating it manually
2. **Some websites may block scraping** - this is normal and expected
3. **Be respectful** - the scraper includes rate limiting by default
4. **Results are saved as JSON** - check the output for filenames

## 🐛 **Troubleshooting**

### **"Module not found" Error**
- Make sure you're using the virtual environment
- Use `./run.sh script.py` instead of `python script.py`

### **No Articles Found**
- Try different extraction methods
- Some websites block automated access
- Check if the website structure has changed

### **Permission Denied**
- Make sure scripts are executable: `chmod +x run.sh`
- Check if the virtual environment exists: `ls venv/`

## 📁 **Output Files**

- Articles are automatically saved to JSON files
- Filenames include timestamps (e.g., `articles_1756278229.json`)
- Use `-o filename.json` to specify custom filenames

## 🎯 **Best Practices**

1. **Start with demo.py** to verify everything works
2. **Use scrape_cli.py** for most scraping tasks
3. **Check the output** for any error messages
4. **Respect rate limits** - don't overload websites
5. **Always deactivate** the virtual environment when done
