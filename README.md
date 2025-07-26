# Resume Optimizer with PDF Generation

An intelligent resume optimization tool that analyzes job descriptions, optimizes resumes, and generates professional PDF resumes with customizable templates.

## Features

### Core Functionality
- **Job Description Analysis**: Extract keywords and requirements from job postings
- **Resume Optimization**: Rewrite resume content to match job requirements
- **PDF Resume Generation**: Create professional PDF resumes with custom HTML templates
- **Template Customization**: Modify fonts, spacing, and styling to match your preferences
- **Custom Keywords**: Use your own keywords for optimization
- **Example Templates**: Built-in examples for testing

### File Management
- **Automatic Saving**: All analyses and optimizations are automatically saved
- **Organized Storage**: Separate folders for different output types
- **Web Interface**: View and manage saved files in the app

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**:
   Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

4. **Use the App**:
   - Paste a job description to analyze keywords
   - Use extracted keywords or add custom ones
   - Optimize your resume automatically
   - Generate professional PDF resumes
   - Customize template styling and formatting
   - View saved files in the management section

## PDF Resume Generation

The application generates professional PDF resumes using customizable HTML templates:

- **Template Customization**: Modify fonts (Garamond, Times New Roman), spacing, margins, and bullet styles
- **Professional Formatting**: Clean, ATS-friendly layouts with proper typography
- **Print Optimization**: CSS optimized for PDF generation and printing
- **Real-time Preview**: See changes as you customize the template
- **Multiple Formats**: Support for different resume styles and layouts

### Template Features
- Garamond font family for professional appearance
- Customizable section spacing and bullet indentation
- Square or circular bullet points
- Flexible margin and padding controls
- Print-ready CSS with proper page breaks

## File Management

### Automatic Saving
All generated content is automatically saved to:
- `outputs/job_analysis/` - Job description analysis results
- `outputs/resume_optimization/` - Resume optimization results

### File Naming
Files use this format: `<type>_<timestamp>_<unique_id>.json`
Example: `job_analysis_20250726_143052_a1b2c3d4.json`

### CLI Tool
Use the command-line interface for file management:
```bash
# View statistics
python file_cli.py stats

# List all files
python file_cli.py list

# Show file details
python file_cli.py show job_analysis <filename>
```

### Web Interface
The Streamlit app includes a "📁 Saved Files Management" section to:
- Browse all saved files
- View file details and metadata
- See summary statistics
- Compare different optimization results

## Documentation

- **[FILE_MANAGEMENT.md](resume-optimizer/FILE_MANAGEMENT.md)**: Comprehensive file management documentation
- **[API Documentation](resume-optimizer/src/)**: Source code and API details

## Project Structure

```
resume-optimizer/
├── app.py                     # Main Streamlit application
├── file_cli.py               # Command-line file management tool
├── requirements.txt          # Python dependencies
├── outputs/                  # Generated files (PDFs, analyses)
│   ├── job_analysis/        # Job description analyses
│   ├── resume_optimization/ # Resume optimizations
│   └── *.pdf               # Generated resume PDFs
└── src/
    ├── chains.py            # LangChain chains
    ├── parsers.py           # Pydantic models
    ├── prompts.py           # LLM prompts
    ├── resume_generator.py  # PDF generation utilities
    ├── file_manager.py      # File management utilities
    └── templates/
        └── resume_template.html # Customizable HTML template
```

## Benefits of File Management

1. **Historical Tracking**: Keep complete history of all analyses
2. **Comparison**: Compare different optimization strategies
3. **Reproducibility**: Easily recreate previous work
4. **Analytics**: Track patterns and effectiveness
5. **Backup**: Secure storage of generated content

## Keywords Source Tracking

The system tracks where keywords came from:
- `job_analysis`: From analyzed job descriptions
- `custom`: Manually entered keywords
- `example`: Built-in example keywords

This helps identify which approaches work best.

## Integration

The JSON format enables easy integration with:
- Data analysis tools (pandas, R)
- Visualization libraries (matplotlib, plotly)
- Database systems
- Version control
- CI/CD pipelines

## Future Enhancements

- **PDF Templates**: Additional resume template styles and layouts
- **Export Formats**: Multiple output formats (Word, LaTeX, etc.)
- **Advanced Customization**: More granular control over styling and formatting
- **Resume Analytics**: Track optimization effectiveness and keyword matching
- **Cloud Integration**: Cloud storage and sharing capabilities
- **Batch Processing**: Process multiple resumes simultaneously

## License

This project is for educational and personal use.