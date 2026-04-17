import sys
import typer
import logging
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llm_knowledge_base.core.config import settings
from llm_knowledge_base.core.llm import LLMClient
from llm_knowledge_base.core.search import SimpleSearchEngine
from llm_knowledge_base.services.wiki_compiler import WikiCompiler
from llm_knowledge_base.services.qa_system import QASystem
from llm_knowledge_base.services.output_renderer import OutputRenderer
from llm_knowledge_base.services.metadata_tracker import MetadataTracker
from llm_knowledge_base.services.duplicate_detector import DuplicateDetector
from llm_knowledge_base.services.wiki_merger import WikiMerger
from llm_knowledge_base.services.embeddings import EmbeddingsService
from llm_knowledge_base.services.export import ExportService


console = Console()
app = typer.Typer(help="LLM Knowledge Base CLI")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy initialization - services only created when needed
_llm_client = None
_embeddings_service = None
_search_engine = None
_wiki_compiler = None
_qa_system = None
_output_renderer = None


def _init_services():
    global _llm_client, _embeddings_service, _search_engine, _wiki_compiler, _qa_system, _output_renderer

    if _llm_client is None:
        if not settings.anthropic_api_key:
            console.print("[red]✗ ANTHROPIC_API_KEY not set in .env![/red]")
            console.print("   Get one from: https://console.anthropic.com")
            raise typer.Exit(1)

        _llm_client = LLMClient(
            api_key=settings.anthropic_api_key,
            model=settings.model,
        )
        _embeddings_service = EmbeddingsService()
        _search_engine = SimpleSearchEngine(settings.wiki_path, embeddings_service=_embeddings_service)
        _wiki_compiler = WikiCompiler(settings.raw_data_path, settings.wiki_path, _llm_client)
        _qa_system = QASystem(settings.wiki_path, _llm_client, _search_engine)
        _output_renderer = OutputRenderer(settings.output_path)


def get_services():
    _init_services()
    return _llm_client, _embeddings_service, _search_engine, _wiki_compiler, _qa_system, _output_renderer


@app.command()
def compile(
    source_path: str = typer.Argument(..., help="Path to source file (relative to raw/ directory)"),
    title: str = typer.Option(None, help="Custom title for the article"),
):
    """Compile a raw document into wiki format"""
    _, _, search_engine, wiki_compiler, _, _ = get_services()
    try:
        console.print(f"[cyan]Compiling {source_path}...[/cyan]")
        wiki_path = wiki_compiler.compile_document(source_path, title)
        search_engine.refresh()
        # Update backlinks for connection strength
        backlinks = wiki_compiler.generate_backlinks_index()
        search_engine.set_backlinks(backlinks)
        console.print(f"[green]✓ Successfully compiled to {wiki_path}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def compile_all():
    """Compile all raw documents into the wiki"""
    _, _, search_engine, wiki_compiler, _, _ = get_services()
    try:
        console.print("[cyan]Compiling all documents...[/cyan]")
        count = wiki_compiler.compile_all()
        search_engine.refresh()
        # Update backlinks for connection strength
        backlinks = wiki_compiler.generate_backlinks_index()
        search_engine.set_backlinks(backlinks)
        console.print(f"[green]✓ Successfully compiled {count} documents[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def backlinks():
    """Apply forward links (Referenced by) to all wiki articles"""
    _, _, _, wiki_compiler, _, _ = get_services()
    try:
        console.print("[cyan]Applying forward links to wiki articles...[/cyan]")
        result = wiki_compiler.apply_forward_links()

        table = Table(title="Forward Links Applied")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")

        table.add_row("Updated Articles", str(result["total_updated"]))
        table.add_row("Broken Links", str(result["total_broken"]))

        console.print(table)

        if result["broken_links"]:
            console.print(f"\n[yellow]⚠ Broken links found:[/yellow]")
            for link in result["broken_links"][:10]:
                console.print(f"  - [[{link}]]")
            if len(result["broken_links"]) > 10:
                console.print(f"  ... and {len(result['broken_links']) - 10} more")

        console.print(f"[green]✓ Forward links applied successfully[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, help="Maximum number of results"),
):
    """Search the wiki"""
    _, _, search_engine, _, _, _ = get_services()
    try:
        results = search_engine.search(query, limit=limit)
        
        if not results:
            console.print(f"[yellow]No results found for '{query}'[/yellow]")
            return
        
        table = Table(title=f"Search Results for '{query}'")
        table.add_column("File", style="cyan")
        table.add_column("Relevance", style="magenta")
        table.add_column("Preview", style="white")
        
        for result in results:
            rel_path = Path(result["path"]).relative_to(settings.wiki_path)
            table.add_row(
                str(rel_path),
                f"{result['relevance']:.2f}",
                result["content_preview"][:80] + "..." if len(result["content_preview"]) > 80 else result["content_preview"],
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def query(
    question: str = typer.Argument(..., help="Question to ask"),
    format: str = typer.Option("markdown", help="Output format (markdown, json, html)"),
    save: bool = typer.Option(True, help="Save output to file"),
    follow_links: bool = typer.Option(True, help="Follow [[links]] to enrich context"),
):
    """Query the knowledge base"""
    _, _, _, _, qa_system, output_renderer = get_services()
    try:
        console.print(f"[cyan]Processing query: {question}[/cyan]")
        answer = qa_system.query(
            question=question,
            max_sources=5,
            output_format=format,
            follow_links=follow_links,
        )
        
        console.print("\n[bold]Answer:[/bold]")
        console.print(answer)
        
        if save:
            output_path = output_renderer.save_markdown(
                answer,
                f"query-{len(list(settings.output_path.glob('*.md')))}",
            )
            console.print(f"\n[green]✓ Saved to {output_path}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def summarize(
    topic: str = typer.Argument(..., help="Topic to summarize"),
    save: bool = typer.Option(True, help="Save output to file"),
):
    """Search and summarize a topic"""
    _, _, _, _, qa_system, output_renderer = get_services()
    try:
        console.print(f"[cyan]Summarizing '{topic}'...[/cyan]")
        summary = qa_system.search_and_summarize(topic)
        
        console.print("\n[bold]Summary:[/bold]")
        console.print(summary)
        
        if save:
            output_path = output_renderer.save_markdown(
                summary,
                f"summary-{topic.replace(' ', '-')[:30]}",
            )
            console.print(f"\n[green]✓ Saved to {output_path}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def index():
    """Generate wiki index"""
    _, _, _, wiki_compiler, _, _ = get_services()
    try:
        console.print("[cyan]Generating wiki index...[/cyan]")
        index_content = wiki_compiler.generate_index()
        
        wiki_index_path = settings.wiki_path / "INDEX.md"
        wiki_index_path.write_text(index_content, encoding="utf-8")
        
        console.print(f"[green]✓ Index generated and saved to {wiki_index_path}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def health():
    """Check system health"""
    try:
        wiki_count = len(list(settings.wiki_path.rglob("*.md")))
        raw_count = len(list(settings.raw_data_path.rglob("*"))) if settings.raw_data_path.exists() else 0
        
        table = Table(title="System Health")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Wiki Articles", str(wiki_count))
        table.add_row("Raw Documents", str(raw_count))
        table.add_row("API Key Set", "✓" if settings.anthropic_api_key else "✗")
        table.add_row("Model", settings.model)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def init():
    """Initialize the knowledge base directory structure"""
    try:
        console.print("[cyan]Initializing knowledge base...[/cyan]")
        
        # Create directories
        settings.raw_data_path.mkdir(parents=True, exist_ok=True)
        settings.wiki_path.mkdir(parents=True, exist_ok=True)
        settings.output_path.mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep files
        for dir_path in [settings.raw_data_path, settings.wiki_path, settings.output_path]:
            (dir_path / ".gitkeep").touch()
        
        console.print("[green]✓ Knowledge base initialized[/green]")
        console.print(f"  Raw data directory: {settings.raw_data_path}")
        console.print(f"  Wiki directory: {settings.wiki_path}")
        console.print(f"  Output directory: {settings.output_path}")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def lint(
    find_duplicates: bool = typer.Option(False, "--find-duplicates", help="Find potential duplicate articles"),
    find_stale: bool = typer.Option(False, "--find-stale", help="Find articles with outdated sources"),
):
    """Health check and maintenance commands for the wiki"""
    try:
        _init_services()
        metadata_dir = settings.wiki_path.parent / ".metadata"
        
        findings = []
        
        # Find duplicates
        if find_duplicates:
            console.print("[cyan]Searching for duplicate articles...[/cyan]")
            duplicate_detector = DuplicateDetector(settings.wiki_path, metadata_dir)
            duplicates = duplicate_detector.find_duplicates()
            
            if duplicates:
                findings.append(f"Found {len(duplicates)} potential duplicates:\n")
                for dup in duplicates:
                    if "similarity" in dup:
                        findings.append(f"  • {dup['file1']} ↔ {dup['file2']} (similarity: {dup['similarity']})")
                    else:
                        findings.append(f"  • {dup['title']}: {', '.join([str(f) for f in dup['files']])}")
            else:
                console.print("[green]✓ No duplicates found[/green]")
        
        # Find stale articles
        if find_stale:
            console.print("[cyan]Checking for stale wiki articles...[/cyan]")
            metadata_tracker = MetadataTracker(settings.wiki_path, metadata_dir)
            stale = metadata_tracker.get_stale_articles()
            
            if stale:
                findings.append(f"Found {len(stale)} stale articles:\n")
                for item in stale:
                    findings.append(f"  • {item['wiki_file']} (version {item['version']}, compiled: {item['compiled_at']})")
                    findings.append(f"    Source: {item['source_file']}")
            else:
                console.print("[green]✓ All articles are up-to-date[/green]")
        
        # Display findings
        if findings:
            console.print("\n[yellow]Lint Results:[/yellow]")
            for finding in findings:
                console.print(finding)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def merge(
    source: str = typer.Argument(..., help="Source article to merge FROM (filename)"),
    target: str = typer.Argument(..., help="Target article to merge INTO (filename)"),
    strategy: str = typer.Option("append", "--strategy", help="Merge strategy: append, prepend, or section"),
):
    """Merge two wiki articles"""
    try:
        _init_services()
        console.print(f"[cyan]Merging {source} into {target}...[/cyan]")
        
        metadata_dir = settings.wiki_path.parent / ".metadata"
        wiki_merger = WikiMerger(settings.wiki_path, metadata_dir)
        
        source_file = settings.wiki_path / source
        target_file = settings.wiki_path / target
        
        if not source_file.exists():
            console.print(f"[red]✗ Source file not found: {source}[/red]")
            raise typer.Exit(1)
        
        if not target_file.exists():
            console.print(f"[red]✗ Target file not found: {target}[/red]")
            raise typer.Exit(1)
        
        if wiki_merger.merge_articles(source_file, target_file, strategy=strategy):
            console.print(f"[green]✓ Successfully merged {source} into {target}[/green]")
            console.print(f"  Strategy: {strategy}")
            console.print(f"  Original {source} archived to: .archives/")
        else:
            console.print("[red]✗ Merge failed[/red]")
            raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def export(
    formats: str = typer.Option("html", help="Export formats: html, jsonl, sqlite, metadata, or 'all'"),
):
    """Export knowledge base to static files"""
    try:
        export_service = ExportService(settings.wiki_path, settings.output_path)

        if formats.lower() == "all":
            console.print("[cyan]Exporting all formats...[/cyan]")
            results = export_service.export_all()
            for fmt, path in results.items():
                console.print(f"[green]✓ {fmt.upper()}: {path}[/green]")
        else:
            format_list = [f.strip() for f in formats.lower().split(",")]
            for fmt in format_list:
                if fmt == "html":
                    path = export_service.export_html()
                    console.print(f"[green]✓ HTML: {path}[/green]")
                elif fmt == "jsonl":
                    path = export_service.export_jsonl()
                    console.print(f"[green]✓ JSONL: {path}[/green]")
                elif fmt == "sqlite":
                    path = export_service.export_sqlite()
                    console.print(f"[green]✓ SQLite: {path}[/green]")
                elif fmt == "metadata":
                    path = export_service.export_metadata()
                    console.print(f"[green]✓ Metadata: {path}[/green]")
                else:
                    console.print(f"[yellow]⚠ Unknown format: {fmt}[/yellow]")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
