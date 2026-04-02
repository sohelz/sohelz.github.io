# Website Management Instructions

This is the personal website of Soheil Zarrinpour, hosted on GitHub Pages.
Claude Code manages this site through simple commands.

## Site Structure

- `site.json` — site configuration: title, navigation, social links
- `build.py` — Python build script that generates HTML from content and templates
- `_templates/` — HTML templates (base layout, post template, page template, index)
- `_content/posts/` — blog post source files as JSON (metadata + body text)
- `_content/pages/` — page source files as JSON (metadata + body text)
- `css/style.css` — all site styling
- `js/` — optional JavaScript files
- `images/` — image files
- `posts/` — generated blog post HTML (do not edit directly)
- `pages/` — generated page HTML (do not edit directly)
- `index.html` — generated home page (do not edit directly)
- `posts/index.html` — generated blog index (do not edit directly)
- `CNAME` — custom domain file

## Important Rules

- NEVER edit generated HTML files directly. Always edit templates or content files, then rebuild.
- After any content or template change, run: python3 build.py
- After rebuilding, commit and push: git add . && git commit -m "description" && git push

## Commands Reference

When the user says any of the following, do exactly what is described:

### post <filepath>
1. Read the text file at the given path.
2. Correct any spelling or grammar errors.
3. Ask the user for a title if not obvious from the content.
4. Create a new JSON file in `_content/posts/` with this format:
   ```
   {
     "title": "Post Title",
     "date": "YYYY-MM-DD",
     "slug": "post-title",
     "tags": [],
     "body": "The corrected text content here. Use \\n for line breaks."
   }
   ```
5. Run `python3 build.py`
6. Run `git add . && git commit -m "New post: Post Title" && git push`
7. Confirm to the user that the post is live.

### update post <slug or title>
1. Find the matching JSON file in `_content/posts/`.
2. Make the requested changes.
3. Rebuild and push.

### delete post <slug or title>
1. Remove the JSON file from `_content/posts/`.
2. Rebuild and push.

### create page <name>
1. Create a new JSON file in `_content/pages/` with the given name.
2. Ask the user what content to put on the page.
3. Rebuild and push.

### update page <name>
1. Find the matching JSON file in `_content/pages/`.
2. Make the requested changes.
3. Rebuild and push.

### embed youtube <url> on <page>
1. Find the target page or post.
2. Add an iframe embed for the YouTube video to the body content.
3. Use this format: <div class="video-embed"><iframe src="https://www.youtube.com/embed/VIDEO_ID" title="YouTube video" allowfullscreen></iframe></div>
4. Rebuild and push.

### embed soundcloud <url> on <page>
1. Find the target page or post.
2. Add a SoundCloud iframe embed to the body content.
3. Rebuild and push.

### embed code <language> on <page>
1. Find the target page or post.
2. Add a readonly code block using <pre><code> tags.
3. Rebuild and push.

### link github <repo-url> on <page>
1. Find the target page or post.
2. Add a styled link to the GitHub repository.
3. Rebuild and push.

### update graphic <description of change>
1. Edit `css/style.css` to make the described visual change.
2. Rebuild and push.

### update nav <description>
1. Edit the navigation array in `site.json`.
2. Rebuild and push.

### rebuild
1. Run `python3 build.py`
2. Run `git add . && git commit -m "Rebuild site" && git push`

### status
1. List all posts with their dates and titles.
2. List all pages.
3. Report the last git commit date and message.

## Consultation Syntax

When the user writes text wrapped in `#` characters (e.g., `#this is a note to Claude#`), that text is a private instruction or consultation with Claude. It should NOT appear in any published content, page, or post. Strip it out and use it only as guidance for completing the task.

## Content Formatting

In the body field of content JSON files, use these conventions:
- `\n\n` for paragraph breaks
- `<h2>Title</h2>` for section headings within content
- `<a href="url">text</a>` for links
- `<strong>text</strong>` for bold
- `<em>text</em>` for italic
- `<pre><code>code here</code></pre>` for code blocks
- `<div class="video-embed"><iframe src="url" title="desc" allowfullscreen></iframe></div>` for video
- `<img src="images/filename.jpg" alt="description">` for images
- `<blockquote>text</blockquote>` for quotes

## Accessibility

This site must always maintain proper semantic HTML structure:
- Correct heading hierarchy (h1 > h2 > h3)
- Alt text on all images
- Title attributes on all iframes
- Descriptive link text (never "click here")
- ARIA labels where needed
- Skip navigation link
- Proper lang attribute on html tag
