#!/usr/bin/env python3
"""
Minimal static site generator.
Reads content from _content/, applies _templates/, writes HTML to root.
"""

import json
import os
import sys
from datetime import datetime

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(SITE_DIR, "_content")
TEMPLATE_DIR = os.path.join(SITE_DIR, "_templates")
POSTS_CONTENT = os.path.join(CONTENT_DIR, "posts")
PAGES_CONTENT = os.path.join(CONTENT_DIR, "pages")
POSTS_OUTPUT = os.path.join(SITE_DIR, "posts")
PAGES_OUTPUT = os.path.join(SITE_DIR, "pages")


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_template(name):
    path = os.path.join(TEMPLATE_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_site_config():
    return load_json(os.path.join(SITE_DIR, "site.json"))


def render_navigation(nav_items, current_href=""):
    links = []
    for item in nav_items:
        # Calculate relative path depth
        active = ' class="active"' if item["href"] == current_href else ""
        links.append(f'<li><a href="/{item["href"]}"{active}>{item["label"]}</a></li>')
    return "\n        ".join(links)


def body_to_html(body_text):
    """Convert body text to HTML paragraphs."""
    if "<p>" in body_text or "<h2>" in body_text or "<div" in body_text:
        # Already contains HTML, return as-is
        return body_text
    paragraphs = body_text.split("\n\n")
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<"):
            html_parts.append(p)
        else:
            html_parts.append(f"<p>{p}</p>")
    return "\n".join(html_parts)


def render_template(template_str, variables):
    """Simple template rendering: replaces {{variable}} with values."""
    result = template_str
    for key, value in variables.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result


SOCIAL_LABELS = {
    "github": "GitHub",
    "soundcloud": "SoundCloud",
    "youtube": "YouTube",
    "email": None,
    "facebook": "Facebook",
    "instagram": "Instagram",
    "mastodon": "Mastodon",
}


def render_footer_social(social_config):
    """Build HTML list items for non-empty social links."""
    items = []
    for key, url in social_config.items():
        if not url or key == "email":
            continue
        label = SOCIAL_LABELS.get(key, key.capitalize())
        items.append(f'<li><a href="{url}" aria-label="{label}">{label}</a></li>')
    return "\n          ".join(items)


def build_posts(site_config, base_template, post_template):
    """Build all blog post pages and return post metadata list."""
    os.makedirs(POSTS_OUTPUT, exist_ok=True)
    posts = []

    if not os.path.exists(POSTS_CONTENT):
        return posts

    for filename in sorted(os.listdir(POSTS_CONTENT)):
        if not filename.endswith(".json"):
            continue
        post_data = load_json(os.path.join(POSTS_CONTENT, filename))
        posts.append(post_data)

        body_html = body_to_html(post_data.get("body", ""))
        tags_html = ""
        if post_data.get("tags"):
            tag_spans = [f'<span class="tag">{t}</span>' for t in post_data["tags"]]
            tags_html = '<div class="tags">' + " ".join(tag_spans) + "</div>"

        post_html = render_template(post_template, {
            "title": post_data["title"],
            "date": post_data["date"],
            "body": body_html,
            "tags": tags_html,
        })

        nav_html = render_navigation(site_config["navigation"], "posts/index.html")
        page_html = render_template(base_template, {
            **base_vars(site_config),
            "page_title": post_data["title"] + " — " + site_config["title"],
            "description": post_data.get("description", site_config["description"]),
            "navigation": nav_html,
            "content": post_html,
        })

        slug = post_data.get("slug", filename.replace(".json", ""))
        output_path = os.path.join(POSTS_OUTPUT, f"{slug}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  Built post: posts/{slug}.html")

    # Sort posts by date descending
    posts.sort(key=lambda x: x.get("date", ""), reverse=True)
    return posts


def build_post_index(site_config, base_template, posts):
    """Build the blog index page listing all posts."""
    if not posts:
        list_html = "<p>No posts yet.</p>"
    else:
        items = []
        for post in posts:
            slug = post.get("slug", "untitled")
            items.append(
                f'<article class="post-summary">\n'
                f'  <time datetime="{post["date"]}">{post["date"]}</time>\n'
                f'  <h2><a href="/posts/{slug}.html">{post["title"]}</a></h2>\n'
                f'</article>'
            )
        list_html = "\n".join(items)

    content = f'<h1>Blog</h1>\n<div class="post-list">\n{list_html}\n</div>'

    nav_html = render_navigation(site_config["navigation"], "posts/index.html")
    page_html = render_template(base_template, {
        **base_vars(site_config),
        "page_title": "Blog — " + site_config["title"],
        "description": "Blog posts by " + site_config["author"],
        "navigation": nav_html,
        "content": content,
    })

    output_path = os.path.join(POSTS_OUTPUT, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(page_html)
    print("  Built posts/index.html")


def build_pages(site_config, base_template, page_template):
    """Build all static pages."""
    os.makedirs(PAGES_OUTPUT, exist_ok=True)

    if not os.path.exists(PAGES_CONTENT):
        return

    for filename in sorted(os.listdir(PAGES_CONTENT)):
        if not filename.endswith(".json"):
            continue
        page_data = load_json(os.path.join(PAGES_CONTENT, filename))

        body_html = body_to_html(page_data.get("body", ""))
        page_content = render_template(page_template, {
            "title": page_data["title"],
            "body": body_html,
        })

        slug = page_data.get("slug", filename.replace(".json", ""))
        nav_html = render_navigation(site_config["navigation"], f"pages/{slug}.html")
        page_html = render_template(base_template, {
            **base_vars(site_config),
            "page_title": page_data["title"] + " — " + site_config["title"],
            "description": page_data.get("description", site_config["description"]),
            "navigation": nav_html,
            "content": page_content,
        })

        output_path = os.path.join(PAGES_OUTPUT, f"{slug}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  Built page: pages/{slug}.html")


def build_tag_pages(site_config, base_template, posts):
    """Build index pages for each tag."""
    tags = {}
    for post in posts:
        for tag in post.get("tags", []):
            tags.setdefault(tag, []).append(post)

    tags_dir = os.path.join(POSTS_OUTPUT, "tags")
    os.makedirs(tags_dir, exist_ok=True)

    for tag, tag_posts in tags.items():
        slug = tag.lower().replace(" ", "-")
        if not tag_posts:
            list_html = "<p>No posts yet.</p>"
        else:
            items = []
            for post in tag_posts:
                post_slug = post.get("slug", "untitled")
                items.append(
                    f'<article class="post-summary">\n'
                    f'  <time datetime="{post["date"]}">{post["date"]}</time>\n'
                    f'  <h2><a href="/posts/{post_slug}.html">{post["title"]}</a></h2>\n'
                    f'</article>'
                )
            list_html = "\n".join(items)

        content = f'<h1>{tag}</h1>\n<div class="post-list">\n{list_html}\n</div>'

        nav_html = render_navigation(site_config["navigation"], f"posts/tags/{slug}.html")
        page_html = render_template(base_template, {
            **base_vars(site_config),
            "page_title": tag + " — " + site_config["title"],
            "description": f"Posts tagged {tag}",
            "navigation": nav_html,
            "content": content,
        })

        output_path = os.path.join(tags_dir, f"{slug}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  Built tag page: posts/tags/{slug}.html")


def build_home(site_config, base_template, posts):
    """Build the home page."""
    index_template = load_template("index.html")

    recent_html = ""
    if posts:
        items = []
        for post in posts[:5]:
            slug = post.get("slug", "untitled")
            items.append(
                f'<article class="post-summary">\n'
                f'  <time datetime="{post["date"]}">{post["date"]}</time>\n'
                f'  <h2><a href="/posts/{slug}.html">{post["title"]}</a></h2>\n'
                f'</article>'
            )
        recent_html = "\n".join(items)
    else:
        recent_html = "<p>No posts yet.</p>"

    categories = site_config.get("categories", [])
    if categories:
        cat_items = []
        for cat in categories:
            cat_items.append(
                f'<li><a href="/posts/tags/{cat["slug"]}.html">{cat["label"]}</a></li>'
            )
        categories_html = "\n      ".join(cat_items)
    else:
        categories_html = ""

    content = render_template(index_template, {
        "site_title": site_config["title"],
        "subtitle": site_config.get("subtitle", ""),
        "description": site_config["description"],
        "recent_posts": recent_html,
        "categories": categories_html,
    })

    nav_html = render_navigation(site_config["navigation"], "index.html")
    page_html = render_template(base_template, {
        **base_vars(site_config),
        "page_title": site_config["title"],
        "description": site_config["description"],
        "navigation": nav_html,
        "content": content,
    })

    output_path = os.path.join(SITE_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(page_html)
    print("  Built index.html")


def base_vars(site_config):
    """Return common variables for the base template."""
    return {
        "site_title": site_config["title"],
        "year": str(datetime.now().year),
        "author": site_config["author"],
        "footer_social": render_footer_social(site_config.get("social", {})),
    }


def main():
    print("Building site...")
    site_config = load_site_config()
    base_template = load_template("base.html")
    post_template = load_template("post.html")
    page_template = load_template("page.html")

    posts = build_posts(site_config, base_template, post_template)
    build_post_index(site_config, base_template, posts)
    build_tag_pages(site_config, base_template, posts)
    build_pages(site_config, base_template, page_template)
    build_home(site_config, base_template, posts)

    print("Done! Site built successfully.")


if __name__ == "__main__":
    main()
