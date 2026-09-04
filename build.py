from pathlib import Path
from datetime import datetime
import re
import shutil

POSTS_DIR = Path("posts")
INDEX_FILE = Path("index.html")
DIST_DIR = Path("dist")
DIST_INDEX = DIST_DIR / "index.html"

POSTS_START = "<!-- POSTS_START -->"
POSTS_END = "<!-- POSTS_END -->"

def wrap_post(html_text):
    html_text = html_text.strip()
    if not html_text.startswith("<article>"):
        raise ValueError("Post does not start with <article>")

    if not html_text.endswith("</article>"):
        raise ValueError("Post does not end with </article>")

    # Find the end of the opening <article> tag
    article_end = html_text.find(">") + 1
    content = html_text[article_end:-len("</article>")].strip()

    return f"""<article class="post">
    <div class="window-content">
    <div class="info-box">
    {content}
    </div>
    </div>
    </article>"""

def get_post_date(html_text):
    """Extract the date and time from the <time>-element."""
    match = re.search(r'<time\s+datetime="([^"]+)"', html_text)

    if not match:
        raise ValueError("this post has no <time datetime=\"...\"> element or contains syntax errors.")
    return datetime.fromisoformat(match.group(1))

def build():
    # start with clean dist directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir()

    # copy static files
    shutil.copytree("css", DIST_DIR / "css")
    shutil.copytree("js", DIST_DIR / "js")
    
    # read source index.html
    index_text = INDEX_FILE.read_text(encoding="utf-8")
    
    posts = []

    for path in POSTS_DIR.glob("*.html"):
        html_text = path.read_text(encoding="utf-8")
        
        date = get_post_date(html_text)

        posts.append({
            "path": path, 
            "html": html_text,
            "date": date,
            })

        # sort by newest post-date
    posts.sort(key=lambda post:post["date"], reverse=True)

    generated = "\n\n".join(
            wrap_post(post["html"])
            for post in posts
            )

    start = index_text.index(POSTS_START) + len(POSTS_START)
    end = index_text.index(POSTS_END) + len(POSTS_END)

    new_index_text = (index_text[:start]
                 + "\n"
                 + generated
                 + "\n"
                 + index_text[end:]
                 )
    # write new index.html
    DIST_INDEX.write_text(new_index_text, encoding="utf-8")

    print(f"Built {DIST_INDEX} with {len(posts)} posts.")

    
if __name__ == "__main__":
    build()
