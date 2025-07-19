#!/bin/bash

# Create the main project directories
echo "Creating root directories: src, app, documents..."
mkdir -p src/services documents

# Create the core Python files in the 'src' directory
echo "Creating core application files..."
touch src/__init__.py
touch src/orchestrator.py

# Create the service class files in the 'services' subdirectory
echo "Creating service modules..."
touch src/services/__init__.py
touch src/services/web_scraper.py
touch src/services/document_parser.py
touch src/services/ai_engine.py

# Create the Streamlit UI file
echo "Creating Streamlit app file..."
touch app.py

# Create the resume and styling files
echo "Creating document files..."
touch documents/resume.md
touch documents/style.css

echo "\nProject structure created successfully!"