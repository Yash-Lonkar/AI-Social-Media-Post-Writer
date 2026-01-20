import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def clean_text(obj):
    if isinstance(obj, str):
        return obj.encode("utf-8", "ignore").decode("utf-8")
    elif isinstance(obj, list):
        return [clean_text(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: clean_text(v) for k, v in obj.items()}
    return obj


def process_posts(raw_file_path, processed_file_path):
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)

    enriched_posts = []

    for post in posts:
        metadata = extract_metadata(post["text"])
        post_with_metadata = {**post, **metadata}
        enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post.get("tags", [])
        post["tags"] = list({
            unified_tags.get(tag, tag) for tag in current_tags
        })

    # 🔥 CLEAN INVALID EMOJIS BEFORE SAVING
    enriched_posts = clean_text(enriched_posts)

    with open(processed_file_path, "w", encoding="utf-8") as outfile:
        json.dump(
            enriched_posts,
            outfile,
            indent=4,
            ensure_ascii=False
        )


def extract_metadata(post_text):
    template = """
You are given a LinkedIn post. You need to extract:
1. Number of lines
2. Language of the post
3. Tags

Rules:
- Return ONLY valid JSON. No preamble.
- JSON must have exactly 3 keys:
  line_count (number),
  language ("English" or "Hinglish"),
  tags (array, max 2 items)

Post:
{post}
"""

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"post": post_text})

    try:
        parser = JsonOutputParser()
        return parser.parse(response.content)
    except OutputParserException as e:
        raise OutputParserException(f"Failed to parse metadata: {e}")


def get_unified_tags(posts):
    unique_tags = set()
    for post in posts:
        unique_tags.update(post.get("tags", []))

    tag_list = ", ".join(unique_tags)

    template = """
You are given a list of tags.
Unify similar tags.

Rules:
1. Merge similar tags into one.
2. Use Title Case.
3. Output ONLY JSON.
4. Output format:
{{
  "Old Tag": "Unified Tag"
}}

Tags:
{tags}
"""

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"tags": tag_list})

    try:
        parser = JsonOutputParser()
        return parser.parse(response.content)
    except OutputParserException as e:
        raise OutputParserException(f"Failed to parse unified tags: {e}")


if __name__ == "__main__":
    process_posts(
        "data/raw_posts.json",
        "data/processed_posts.json"
    )
