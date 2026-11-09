from aiohttp import web
import markdown
import os

routes = web.RouteTableDef()

# README.md repo root la irukku (plugins folder la illa)
README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")


@routes.get("/health", allow_head=True)
async def health_handler(request):
    return web.Response(text="ok")


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    if not os.path.exists(README_PATH):
        return web.Response(text="Bot is running.")
    with open(README_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()
    html = markdown.markdown(md_text, extensions=["fenced_code", "tables"])
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GokuStark FileStore</title>
<style>body{{font-family:sans-serif;max-width:900px;margin:auto;padding:2rem;background:#f9f9f9;color:#333}}
pre{{background:#282c34;color:#f8f8f2;padding:1em;overflow-x:auto;border-radius:8px}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ccc;padding:.5rem}}</style>
</head><body>{html}</body></html>"""
    return web.Response(text=page, content_type="text/html")
