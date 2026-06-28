# core — soheilzarrinpour.com
# Site Management Reference v1.0
# Read this file at the start of every site management session.

================================================================================
SITE
================================================================================
Owner:      Soheil Zarrinpour
URL:        https://soheilzarrinpour.com
Repo:       https://github.com/sohelz/sohelz.github.io
Host:       GitHub Pages
Generator:  build.py (custom Python static site generator)
Config:     site.json

Build:   python3 build.py
Deploy:  git add . && git commit -m "..." && git push

NEVER edit generated HTML files directly.
NEVER permanently delete content — move to _trash/ instead (see TRASH section).

================================================================================
DIRECTORY LAYOUT
================================================================================
_content/
  posts/          ← blog post source JSON (input to build)
  pages/          ← page source JSON (input to build)
_templates/
  base.html       ← master layout: header, nav, footer, {{content}}
  page.html       ← wraps a page: {{back_link}}, {{title}}, {{body}}
  post.html       ← wraps a post: title, date, {{body}}, {{tags}}
  index.html      ← homepage sections: hero, categories, recent posts
_trash/
  posts/          ← removed posts go here (not built)
  pages/          ← removed pages go here (not built)
site.json         ← nav, categories, social, title, description
build.py          ← reads _content/, applies _templates/, writes HTML
core.md           ← THIS FILE
CLAUDE.md         ← minimal Claude instructions (points here)
css/style.css     ← all styling
images/           ← image assets
js/               ← JavaScript files
CNAME             ← custom domain

Generated (do not edit):
  index.html
  pages/          ← built from _content/pages/
  posts/          ← built from _content/posts/
  listen/         ← built from listen-*.json pages with "path" field

================================================================================
PAGE JSON SCHEMA
================================================================================
File location: _content/pages/<slug>.json

Required fields:
  "title"         string   — display title, used in <h1> and <title>
  "slug"          string   — URL identifier, lowercase-hyphenated

Optional fields:
  "description"   string   — meta description (falls back to site description)
  "path"          string   — custom output path relative to site root
                             e.g. "listen/index.html" → outputs to /listen/
                             if absent, outputs to /pages/<slug>.html
  "parent"        object   — renders a back-link above the <h1>
                             {"title": "Listen", "href": "/listen/"}
  "body"          string   — HTML content (see BODY FORMAT section)

Example — standard page:
{
  "title": "Industrial Fantasia",
  "slug": "industrial-fantasia",
  "description": "Electronic music composition by Soheil Zarrinpour.",
  "parent": {"title": "Electroacoustic", "href": "/listen/electroacoustic/"},
  "body": "<p>Description here.</p>"
}

Example — section index page (custom path):
{
  "title": "Electroacoustic",
  "slug": "listen-electroacoustic",
  "path": "listen/electroacoustic/index.html",
  "parent": {"title": "Listen", "href": "/listen/"},
  "body": "<h2><a href=\"/pages/piece-slug.html\">Piece Title</a></h2>"
}

================================================================================
POST JSON SCHEMA
================================================================================
File location: _content/posts/YYYY-MM-DD-<slug>.json

Required fields:
  "title"         string       — post title
  "date"          string       — YYYY-MM-DD
  "slug"          string       — URL identifier, lowercase-hyphenated
  "tags"          array        — list of category slugs
  "body"          string       — HTML content

Optional fields:
  "description"   string       — meta description

Valid tags (must match a slug in site.json categories):
  "daily-synth-experience"
  "braille-screen-reader-access-tools"

Example:
{
  "title": "My Post Title",
  "date": "2026-06-25",
  "slug": "my-post-title",
  "tags": ["daily-synth-experience"],
  "body": "<p>Post content here.</p>"
}

================================================================================
SITE.JSON SCHEMA
================================================================================
{
  "title":       string,
  "subtitle":    string,
  "url":         string,
  "author":      string,
  "description": string,
  "navigation":  [{"label": string, "href": string}, ...],
  "categories":  [{"label": string, "slug": string}, ...],
  "social": {
    "github":    string or "",
    "soundcloud": string or "",
    "youtube":   string or "",
    "email":     string or "",
    "instagram": string or "",
    "mastodon":  string or ""
  }
}

================================================================================
CURRENT SITE STATE
================================================================================
Navigation:  Home | About | Listen | Blog | Contact
Subtitle:    Composer | Audio Programmer

Listen structure:
  /listen/                     — Acoustic + Electroacoustic headings
  /listen/acoustic/            — Three Miniatures for Wind Quintet
  /listen/electroacoustic/     — Industrial Fantasia, Trapped Wind, Resurrection,
                                  Lapis Bubbles, Submarine, Spectrafull,
                                  Piano and Live Electronic

Blog categories: Daily Synth Experience | Braille & Screen Reader Access Tools
Posts: reading-post-window-supercollider-voiceover

================================================================================
COMMANDS
================================================================================

--- post <filepath> ---
1. Read the file at the given path.
2. Correct spelling and grammar errors.
3. Ask for a title if not obvious.
4. Create _content/posts/YYYY-MM-DD-<slug>.json using POST SCHEMA above.
5. python3 build.py
6. git add . && git commit -m "New post: <Title>" && git push
7. Confirm to user that the post is live.

--- update post <slug or title> ---
1. Find matching JSON in _content/posts/.
2. Apply requested changes.
3. python3 build.py && git add . && git commit -m "Update post: <Title>" && git push

--- remove post <slug or title> ---
1. Find matching JSON in _content/posts/.
2. Move file to _trash/posts/ (do not delete permanently).
3. python3 build.py && git add . && git commit -m "Remove post: <Title>" && git push

--- add piece <Title> to <acoustic|electroacoustic> ---
1. Create _content/pages/<slug>.json using PAGE SCHEMA above.
   Set "parent" to the appropriate section.
2. Add an <h2> heading link to the section listing page:
   - Electroacoustic: _content/pages/listen-electroacoustic.json
   - Acoustic:        _content/pages/listen-acoustic.json
   Append:  "<h2><a href=\"/pages/<slug>.html\"><Title></a></h2>"
3. python3 build.py && git add . && git commit -m "Add piece: <Title>" && git push

--- remove piece <slug or title> ---
1. Remove the <h2> heading link from the section listing page JSON.
2. Move the piece JSON from _content/pages/ to _trash/pages/.
3. python3 build.py && git add . && git commit -m "Remove piece: <Title>" && git push

--- update page <name> ---
1. Find matching JSON in _content/pages/.
2. Apply requested changes.
3. python3 build.py && git add . && git commit -m "Update page: <Name>" && git push

--- embed youtube <url> on <page> ---
1. Find the target page or post JSON.
2. Add to body: <div class="video-embed"><iframe src="https://www.youtube.com/embed/VIDEO_ID" title="YouTube video" allowfullscreen></iframe></div>
3. python3 build.py && git add . && git commit && git push

--- embed soundcloud <url> on <page> ---
1. Find the target page or post JSON.
2. Add SoundCloud iframe embed to body.
3. python3 build.py && git add . && git commit && git push

--- embed code <language> on <page> ---
1. Find the target page or post JSON.
2. Add to body: <pre><code>code here</code></pre>
3. python3 build.py && git add . && git commit && git push

--- link github <repo-url> on <page> ---
1. Find the target page or post JSON.
2. Add to body: <a href="<url>" class="github-link">GitHub: <repo-name></a>
3. python3 build.py && git add . && git commit && git push

--- update graphic <description> ---
1. Edit css/style.css.
2. python3 build.py && git add . && git commit -m "Update style: <description>" && git push

--- update nav <description> ---
1. Edit navigation array in site.json.
2. python3 build.py && git add . && git commit -m "Update nav" && git push

--- rebuild ---
1. python3 build.py
2. git add . && git commit -m "Rebuild site" && git push

--- status ---
1. List all posts in _content/posts/ with dates and titles.
2. List all pages in _content/pages/.
3. List trashed items in _trash/.
4. Report last git commit.

================================================================================
BODY FORMAT (HTML conventions for JSON body fields)
================================================================================
Paragraph break:   \n\n (between paragraphs in JSON string)
Section heading:   <h2>Title</h2>
Piece listing:     <h2><a href="/pages/slug.html">Title</a></h2>
                   ← ALWAYS use h2 headings for listing pieces, never <ul><li>
Link:              <a href="url">text</a>
Bold:              <strong>text</strong>
Italic:            <em>text</em>
Code block:        <pre><code>code here</code></pre>
Video embed:       <div class="video-embed"><iframe src="url" title="desc" allowfullscreen></iframe></div>
Audio embed:       <div class="audio-embed"><iframe ...></iframe></div>
Image:             <img src="/images/filename.jpg" alt="description">
Quote:             <blockquote>text</blockquote>

================================================================================
CONVENTIONS
================================================================================
1. LISTING PIECES: Always use <h2><a href="...">Title</a></h2> — never <ul><li>.

2. BACK-LINKS: Any page JSON with a "parent" field gets a "← Parent Title" link
   rendered above its <h1>. Set "parent" on:
   - All section index pages (acoustic, electroacoustic) → parent = Listen
   - All individual piece pages → parent = their section

3. CUSTOM PATH: Pages with a "path" field output to that path at the site root.
   Used for /listen/, /listen/acoustic/, /listen/electroacoustic/.
   Without "path", pages output to /pages/<slug>.html.

4. HEADING HIERARCHY: h1 = page title (auto), h2 = section/piece, h3 = sub-section.
   Never skip levels.

5. ACCESSIBILITY: Alt text on all images. Title on all iframes. Descriptive link text.

6. CONSULTATION SYNTAX: Text the user wraps in # characters (e.g. #note#) is a
   private instruction to Claude — strip it from all published content.

================================================================================
TRASH SYSTEM
================================================================================
_trash/posts/   ← moved-here posts (not built, not deleted from history)
_trash/pages/   ← moved-here pages (not built, not deleted from history)

Rules:
- "remove" always means: move to _trash/, rebuild, push.
- Never use rm to permanently delete content files.
- To restore: move file back from _trash/ to _content/, rebuild, push.
- For section listing pages (listen-electroacoustic.json etc.),
  also remove the <h2> link entry when removing a piece.

================================================================================
ACCESSIBILITY
================================================================================
- Correct heading hierarchy (h1 > h2 > h3)
- Alt text on all images
- Title attribute on all iframes
- Descriptive link text (never "click here")
- ARIA labels where needed
- Proper lang attribute on html element
