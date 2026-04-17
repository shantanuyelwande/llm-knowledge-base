import logging
from pathlib import Path
from typing import List
import re

logger = logging.getLogger(__name__)


class WikiTagger:
    """Auto-generate and update tags for wiki articles"""

    def __init__(self, wiki_dir: Path, llm_client):
        self.wiki_dir = wiki_dir
        self.llm_client = llm_client

    def tag_all_articles(self) -> dict:
        """Analyze all articles and add tags"""
        wiki_files = sorted(self.wiki_dir.rglob("*.md"))
        wiki_files = [f for f in wiki_files if f.name != "index.md" and f.name != "log.md"]

        results = {
            "total": len(wiki_files),
            "tagged": 0,
            "skipped": 0,
            "failed": 0,
            "errors": [],
        }

        for file_path in wiki_files:
            try:
                if self._update_article_tags(file_path):
                    results["tagged"] += 1
                else:
                    results["skipped"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(str(e))
                logger.error(f"Error tagging {file_path}: {e}")

        return results

    def _update_article_tags(self, file_path: Path) -> bool:
        """Update tags for a single article"""
        content = file_path.read_text(encoding="utf-8")

        # Skip if already has tags
        if self._has_tags(content):
            logger.info(f"Skipping {file_path.name} (already tagged)")
            return False

        # Extract content for analysis
        if content.startswith("---"):
            end = content.find("\n---\n", 4)
            if end > 0:
                body = content[end + 5:]
            else:
                body = content
        else:
            body = content

        # Get title
        title_match = re.search(r"^# (.+)$", body, re.MULTILINE)
        title = title_match.group(1) if title_match else "Unknown"

        # Get first few paragraphs for context
        text_preview = body[:1000]

        # Ask Claude to generate tags
        prompt = f"""Analyze this wiki article and suggest 3-5 relevant tags.

Title: {title}

Preview:
{text_preview}

Return ONLY a JSON array of tags (strings), like: ["tag1", "tag2", "tag3"]
Do not include explanations, just the JSON array."""

        try:
            tags_response = self.llm_client.generate(
                prompt=prompt,
                system="You are an expert at categorizing knowledge base articles. Return only JSON.",
                max_tokens=100,
            )

            # Parse JSON response
            tags = self._parse_tags_json(tags_response)

            if tags:
                # Update frontmatter with tags
                self._add_tags_to_frontmatter(file_path, content, tags)
                logger.info(f"✓ Tagged {file_path.name}: {tags}")
                return True
        except Exception as e:
            logger.error(f"Error generating tags for {file_path}: {e}")

        return False

    def _has_tags(self, content: str) -> bool:
        """Check if article already has non-empty tags in frontmatter"""
        if not content.startswith("---"):
            return False

        end = content.find("\n---\n", 4)
        if end <= 0:
            return False

        frontmatter = content[4:end]
        for line in frontmatter.split("\n"):
            if line.startswith("tags:"):
                tags_str = line.replace("tags:", "").strip()
                if tags_str and tags_str != "[]" and tags_str != "":
                    return True
        return False

    def _parse_tags_json(self, response: str) -> List[str]:
        """Extract tags from Claude's JSON response"""
        try:
            # Find JSON array in response
            match = re.search(r'\[.*?\]', response, re.DOTALL)
            if match:
                json_str = match.group(0)
                # Simple JSON parsing
                json_str = json_str.strip("[]").replace('"', '').replace("'", '')
                tags = [tag.strip() for tag in json_str.split(",")]
                return [t for t in tags if t]
        except Exception as e:
            logger.warning(f"Could not parse tags JSON: {e}")

        return []

    def _add_tags_to_frontmatter(self, file_path: Path, content: str, tags: List[str]):
        """Add tags to article's frontmatter"""
        tags_str = ', '.join(f'"{t}"' for t in tags)
        tags_line = f"tags: [{tags_str}]"

        if content.startswith("---"):
            end = content.find("\n---\n", 4)
            if end > 0:
                frontmatter = content[4:end]
                body = content[end + 5:]

                # Replace existing tags line or add new one
                lines = frontmatter.split("\n")
                new_lines = []
                tags_found = False

                for line in lines:
                    if line.startswith("tags:"):
                        new_lines.append(tags_line)
                        tags_found = True
                    else:
                        new_lines.append(line)

                if not tags_found:
                    new_lines.append(tags_line)

                new_frontmatter = "\n".join(new_lines)
                new_content = f"---\n{new_frontmatter}\n---\n{body}"
                file_path.write_text(new_content, encoding="utf-8")
                return

        # No frontmatter, create one
        new_content = f"---\n{tags_line}\n---\n\n{content}"
        file_path.write_text(new_content, encoding="utf-8")
