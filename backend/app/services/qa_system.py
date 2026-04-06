import logging
from pathlib import Path
from typing import List, Optional, Dict
import json
import re

from .change_logger import ChangeLogger

logger = logging.getLogger(__name__)


class QASystem:
    """Q&A system that queries the wiki against LLM"""
    
    def __init__(self, wiki_dir: Path, llm_client, search_engine):
        self.wiki_dir = wiki_dir
        self.llm_client = llm_client
        self.search_engine = search_engine
        self.change_logger = ChangeLogger(self.wiki_dir)
    
    def query(
        self,
        question: str,
        max_sources: int = 5,
        output_format: str = "markdown",
        follow_links: bool = True,
        max_total_docs: int = 10,
    ) -> str:
        """Query the knowledge base with optional link traversal"""
        # Search for relevant documents
        search_results = self.search_engine.search(question, limit=max_sources)

        # Retrieve full content of relevant documents
        context_docs = []
        for result in search_results:
            try:
                doc_content = Path(result["path"]).read_text(encoding="utf-8")
                context_docs.append({
                    "title": Path(result["path"]).stem,
                    "content": doc_content,
                    "path": result["path"],
                })
            except Exception as e:
                logger.error(f"Error reading document {result['path']}: {e}")

        # Follow links to enrich context
        if follow_links:
            context_docs = self._collect_linked_docs(context_docs, max_total=max_total_docs)

        # Log the query
        self.change_logger.log_query(question, len(context_docs))

        # Generate answer using LLM
        answer = self._generate_answer(question, context_docs, output_format)
        return answer
    
    def _collect_linked_docs(
        self,
        seed_docs: List[dict],
        max_total: int = 10,
    ) -> List[dict]:
        """Follow [[wikilinks]] from seed_docs 1 hop deep and return expanded list"""
        seen_paths = {doc["path"] for doc in seed_docs}
        expanded_docs = seed_docs.copy()

        # Extract links from each seed document
        for doc in seed_docs:
            if len(expanded_docs) >= max_total:
                break

            # Extract [[topic]] links (before | to handle aliases)
            links = re.findall(r'\[\[([^\]|]+)', doc["content"])

            for link in links:
                if len(expanded_docs) >= max_total:
                    break

                # Resolve link to a file path (using same slug logic as wiki_compiler)
                link_slug = link.lower().replace(" ", "-").replace("_", "-")
                link_slug = "".join(c if c.isalnum() or c in "-" else "" for c in link_slug)
                linked_file = self.wiki_dir / f"{link_slug}.md"

                # If file exists and not already in context, add it
                if linked_file.exists() and str(linked_file) not in seen_paths:
                    try:
                        linked_content = linked_file.read_text(encoding="utf-8")
                        expanded_docs.append({
                            "title": linked_file.stem,
                            "content": linked_content,
                            "path": str(linked_file),
                        })
                        seen_paths.add(str(linked_file))
                        logger.debug(f"Added linked doc: {link_slug}")
                    except Exception as e:
                        logger.error(f"Error reading linked document {linked_file}: {e}")

        return expanded_docs

    def _generate_answer(
        self,
        question: str,
        context_docs: List[dict],
        output_format: str = "markdown",
    ) -> str:
        """Generate an answer using LLM with context"""
        
        # Build context string
        context_str = ""
        for doc in context_docs:
            context_str += f"\n### Document: {doc['title']}\n{doc['content']}\n---\n"
        
        format_instruction = {
            "markdown": "Respond in well-formatted markdown with clear headings, bullet points, and links.",
            "json": "Respond as a JSON object with fields for 'answer', 'sources', and 'confidence'.",
            "html": "Respond as valid HTML suitable for rendering in a browser.",
        }
        
        prompt = f"""Based on the following wiki documents, answer this question:

Question: {question}

Context from wiki:
{context_str}

{format_instruction.get(output_format, format_instruction['markdown'])}

Include citations to the source documents where relevant."""
        
        system_prompt = """You are an expert research assistant with access to a knowledge base.
Answer questions thoroughly based on the provided context.
Always cite your sources and indicate if information is not found in the knowledge base."""
        
        answer = self.llm_client.generate(
            prompt=prompt,
            system=system_prompt,
            max_tokens=2048,
        )
        
        return answer
    
    def search_and_summarize(self, topic: str) -> str:
        """Search for articles on a topic and generate a summary"""
        search_results = self.search_engine.search(topic, limit=10)

        # Log the summarize operation
        self.change_logger.log_query(f"summarize: {topic}", len(search_results))

        if not search_results:
            return f"No articles found about '{topic}'."

        # Collect content
        docs_content = ""
        for result in search_results:
            try:
                content = Path(result["path"]).read_text(encoding="utf-8")
                docs_content += f"\n## {Path(result['path']).stem}\n{content}\n---\n"
            except Exception as e:
                logger.error(f"Error reading {result['path']}: {e}")

        # Generate summary
        prompt = f"""Create a comprehensive summary of these articles about '{topic}':

{docs_content}

Generate a well-structured markdown summary that:
1. Covers the main themes and concepts
2. Identifies key definitions and important points
3. Suggests connections between articles
4. Lists any questions that remain unanswered
5. Recommends areas for further research"""

        system_prompt = "You are an expert at synthesizing and summarizing research materials into coherent overviews."

        summary = self.llm_client.generate(
            prompt=prompt,
            system=system_prompt,
            max_tokens=3000,
        )

        return summary
