import logging
from pathlib import Path
from typing import List, Optional
import json

logger = logging.getLogger(__name__)


class QASystem:
    """Q&A system that queries the wiki against LLM"""
    
    def __init__(self, wiki_dir: Path, llm_client, search_engine):
        self.wiki_dir = wiki_dir
        self.llm_client = llm_client
        self.search_engine = search_engine
    
    def query(
        self,
        question: str,
        max_sources: int = 5,
        output_format: str = "markdown",
    ) -> str:
        """Query the knowledge base"""
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
        
        # Generate answer using LLM
        answer = self._generate_answer(question, context_docs, output_format)
        return answer
    
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
