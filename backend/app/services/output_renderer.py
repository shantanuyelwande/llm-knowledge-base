import logging
from pathlib import Path
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class OutputRenderer:
    """Renders query results in various formats"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_markdown(self, content: str, filename: str) -> str:
        """Save content as markdown file"""
        filepath = self.output_dir / f"{filename}.md"
        filepath.write_text(content, encoding="utf-8")
        logger.info(f"Saved markdown output to {filepath}")
        return str(filepath)
    
    def save_json(self, data: dict, filename: str) -> str:
        """Save data as JSON file"""
        filepath = self.output_dir / f"{filename}.json"
        filepath.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.info(f"Saved JSON output to {filepath}")
        return str(filepath)
    
    def save_html(self, content: str, filename: str, title: str = "Output") -> str:
        """Save content as HTML file"""
        import markdown
        
        # Convert markdown to HTML if needed
        if content.startswith("#"):
            html_content = markdown.markdown(content)
        else:
            html_content = content
        
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #f9f9f9;
        }}
        h1, h2, h3 {{
            color: #1a73e8;
            margin-top: 20px;
        }}
        code {{
            background-color: #f1f1f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        a {{
            color: #1a73e8;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .metadata {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="metadata">
        Generated: {datetime.now().isoformat()}
    </div>
    <div>
        {html_content}
    </div>
</body>
</html>"""
        
        filepath = self.output_dir / f"{filename}.html"
        filepath.write_text(full_html, encoding="utf-8")
        logger.info(f"Saved HTML output to {filepath}")
        return str(filepath)
    
    def save_marp_slides(self, content: str, filename: str) -> str:
        """Save content as Marp slides"""
        marp_content = f"""---
marp: true
theme: default
paginate: true
---

# Knowledge Base Query Results

{content}

---

*Generated: {datetime.now().isoformat()}*
"""
        
        filepath = self.output_dir / f"{filename}.md"
        filepath.write_text(marp_content, encoding="utf-8")
        logger.info(f"Saved Marp slides to {filepath}")
        return str(filepath)
    
    def create_report(
        self,
        query: str,
        answer: str,
        sources: list = None,
        output_format: str = "markdown",
    ) -> str:
        """Create a complete report with metadata"""
        
        report_data = {
            "query": query,
            "answer": answer,
            "sources": sources or [],
            "generated_at": datetime.now().isoformat(),
        }
        
        if output_format == "json":
            return self.save_json(report_data, f"report-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        elif output_format == "html":
            md_content = f"""# Query Report

## Question
{query}

## Answer
{answer}

## Sources
"""
            if sources:
                for source in sources:
                    md_content += f"- {source}\n"
            
            return self.save_html(md_content, f"report-{datetime.now().strftime('%Y%m%d_%H%M%S')}", title=query)
        
        else:  # markdown
            md_content = f"""# Query Report

**Query:** {query}

**Generated:** {datetime.now().isoformat()}

## Answer

{answer}

## Sources

"""
            if sources:
                for source in sources:
                    md_content += f"- {source}\n"
            
            return self.save_markdown(md_content, f"report-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
