"""
Data ingestion script for the Humanoid Robotics Textbook.

This script processes textbook content and ingests it into the Qdrant vector database
for RAG functionality. It reads the textbook content, chunks it appropriately,
generates embeddings, and stores them in Qdrant for retrieval.
"""

import os
import sys
import hashlib
from pathlib import Path
from typing import List, Dict, Any

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.utils.gemini_client import embed_text
from api.utils.qdrant_client import add_document_to_qdrant, create_collection_if_not_exists


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split text into overlapping chunks for better retrieval.

    Args:
        text: The input text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of dictionaries containing chunk information
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If this is the last chunk, make sure we include all remaining text
        if end >= len(text):
            end = len(text)
        else:
            # Try to break at sentence boundary if possible
            while end > start + chunk_size - overlap and end < len(text) and text[end] not in '.!?':
                end += 1
            if end == start + chunk_size - overlap:
                end = start + chunk_size  # Just break at the limit if no sentence boundary found

        chunk_text = text[start:end].strip()
        if len(chunk_text) > 0:  # Only add non-empty chunks
            # Create a unique ID based on the chunk content
            chunk_id = hashlib.md5(f"{chunk_text}{start}".encode()).hexdigest()

            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "start_pos": start,
                "end_pos": end
            })

        # Move start position, considering overlap
        start = end - overlap if end < len(text) else end

        # Prevent infinite loop
        if start == end:
            start += chunk_size

    return chunks


def read_textbook_content() -> str:
    """
    Read the textbook content from documentation files.

    Returns:
        Combined text content from all textbook documents
    """
    content = []

    # Look for textbook content in docs directory
    docs_path = Path(__file__).parent.parent.parent / "website" / "docs"

    if docs_path.exists():
        for md_file in docs_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    # Remove markdown headers and metadata
                    lines = file_content.split('\n')
                    content_start = 0

                    # Skip frontmatter if present
                    if lines and lines[0].strip() == '---':
                        for i, line in enumerate(lines[1:], 1):
                            if line.strip() == '---':
                                content_start = i + 1
                                break

                    content.append('\n'.join(lines[content_start:]))
            except Exception as e:
                print(f"Error reading {md_file}: {e}")

    return '\n\n'.join(content)


def ingest_textbook():
    """
    Main function to ingest textbook content into Qdrant.
    """
    print("Starting textbook ingestion process...")

    # Create collection if it doesn't exist
    print("Creating Qdrant collection if it doesn't exist...")
    create_collection_if_not_exists()

    # Read textbook content
    print("Reading textbook content...")
    textbook_content = read_textbook_content()

    if not textbook_content.strip():
        print("Warning: No textbook content found. Looking for documentation files in website/docs/")
        return

    print(f"Found {len(textbook_content)} characters of textbook content")

    # Chunk the content
    print("Chunking content...")
    chunks = chunk_text(textbook_content)

    print(f"Created {len(chunks)} chunks")

    # Process each chunk
    successful = 0
    failed = 0

    for i, chunk in enumerate(chunks):
        try:
            print(f"Processing chunk {i+1}/{len(chunks)}...")

            # Generate embedding
            embedding = embed_text(chunk["text"])

            # Add to Qdrant
            add_document_to_qdrant(
                doc_id=chunk["id"],
                text=chunk["text"],
                embedding=embedding
            )

            successful += 1

            if i % 10 == 0:  # Progress update every 10 chunks
                print(f"Progress: {i+1}/{len(chunks)} chunks processed")

        except Exception as e:
            print(f"Error processing chunk {i+1}: {e}")
            failed += 1

    print(f"\nIngestion completed!")
    print(f"Successful: {successful} chunks")
    print(f"Failed: {failed} chunks")
    print(f"Total: {len(chunks)} chunks")


if __name__ == "__main__":
    # Check if required environment variables are set
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set")
        sys.exit(1)

    if not os.getenv("QDRANT_URL") or not os.getenv("QDRANT_API_KEY"):
        print("Error: QDRANT_URL and QDRANT_API_KEY environment variables are not set")
        sys.exit(1)

    ingest_textbook()