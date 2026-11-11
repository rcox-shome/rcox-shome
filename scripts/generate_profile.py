#!/usr/bin/env python3
"""Render an original terminal profile from public GitHub data. No API token needed."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"


def api(path):
    request = Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "rcox-shome-profile",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def collect_snapshot(config):
    user = config["username"]
    profile = api(f"/users/{user}")
    repos = []
    for page in range(1, 101):
        batch = api(f"/users/{user}/repos?type=owner&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError("Expected a public repository list")
        if any(repo.get("private") is not False for repo in batch):
            raise ValueError("Refusing non-public repository data")
        repos.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise ValueError("Repository pagination did not finish")

    language_bytes = {}
    for repo in repos:
        # Profile-generation code and forks are excluded from the language summary.
        if repo["name"] == user or repo["fork"] or not repo.get("language"):
            continue
        languages = api(f"/repos/{user}/{repo['name']}/languages")
        for language, count in languages.items():
            if not isinstance(count, int) or count < 0:
                raise ValueError("Invalid language byte count")
            language_bytes[language] = language_bytes.get(language, 0) + count

    releases = {}
    for name in config["releases"]:
        # The releases list includes public prereleases; /releases/latest excludes them.
        candidates = api(f"/repos/{user}/{name}/releases?per_page=10")
        published = [r for r in candidates if not r["draft"] and r.get("published_at")]
        if not published:
            raise ValueError(f"No public release found for {name}")
        latest = max(published, key=lambda r: r["published_at"])
        releases[name] = {"tag": latest["tag_name"], "prerelease": latest["prerelease"]}

    return {
        "username": user,
        "updated": datetime.now(timezone.utc).date().isoformat(),
        "created_at": profile["created_at"],
        "public_repos": len(repos),
        "languages": [key for key, _ in sorted(language_bytes.items(), key=lambda x: (-x[1], x[0]))],
        "releases": releases,
    }


def validate_snapshot(data, config):
    if data.get("username") != config["username"]:
        raise ValueError("Snapshot belongs to another account")
    if not isinstance(data.get("public_repos"), int) or data["public_repos"] < 0:
        raise ValueError("Invalid public repository count")
    if not isinstance(data.get("languages"), list) or not all(isinstance(x, str) for x in data["languages"]):
        raise ValueError("Invalid languages")
    datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
    datetime.strptime(data["updated"], "%Y-%m-%d")
    for name in config["releases"]:
        release = data["releases"][name]
        if not isinstance(release.get("tag"), str) or not isinstance(release.get("prerelease"), bool):
            raise ValueError("Invalid release data")


def clip(value, limit=46):
    value = str(value)
    return value if len(value) <= limit else value[:limit - 1] + "…"


def render(config, data, art, dark=True, mobile=False):
    colors = ({"bg": "#0d1117", "bar": "#161b22", "border": "#30363d", "text": "#d7e0ea", "muted": "#8b9aab", "accent": "#75e4cd", "key": "#c4a2f5", "white": "#f0f6fc"}
              if dark else {"bg": "#f6f8fa", "bar": "#eaeef2", "border": "#c7ced7", "text": "#283342", "muted": "#5d6b7a", "accent": "#087c6c", "key": "#7550ad", "white": "#17212d"})
    width, height = (560, 1092) if mobile else (1120, 682)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Reese Cox — native Mac apps and local-first tools</title>',
           f'<desc id="desc">ASCII artwork of the current GitHub robot avatar. {data["public_repos"]} public repositories. ChordShot {escape(data["releases"]["chordshot-releases"]["tag"])} Nodetaker {escape(data["releases"]["nodetaker-releases"]["tag"])}, and Folder Reader {escape(data["releases"]["folder-reader-releases"]["tag"])}. Public data updated {data["updated"]}.</desc>',
           '<style>text{font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace;font-variant-ligatures:none}.cursor{animation:blink 1.4s steps(1) infinite}@keyframes blink{50%{opacity:0}}@media(prefers-reduced-motion:reduce){.cursor{animation:none}}</style>',
           f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="14" fill="{colors["bg"]}" stroke="{colors["border"]}"/>',
           f'<path d="M15 1H{width-15}Q{width-1} 1 {width-1} 15V49H1V15Q1 1 15 1" fill="{colors["bar"]}"/>',
           f'<path d="M1 49H{width-1}" stroke="{colors["border"]}"/>']

    def text(x, y, value, size=16, color="text", weight="400", extra=""):
        out.append(f'<text x="{x}" y="{y}" fill="{colors[color]}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>')

    def rule(x1, y, x2):
        out.append(f'<path d="M{x1} {y}H{x2}" stroke="{colors["border"]}"/>')

    for x, color in [(27, "#ff5f57"), (47, "#febc2e"), (67, "#28c840")]:
        out.append(f'<circle cx="{x}" cy="25" r="5" fill="{color}"/>')
    text(width/2, 30, "reese@workbench: ~", 13, "muted", extra='text-anchor="middle"')
    text(28, 89, "~ % profile --public", 16 if not mobile else 18, "accent")

    if mobile:
        art_x, art_y, art_size, art_step = 119, 127, 9.3, 9.7
    else:
        art_x, art_y, art_size, art_step = 34, 130, 10.5, 10.6
    for i, line in enumerate(art):
        text(art_x, round(art_y+i*art_step, 2), line, art_size, "accent", extra='xml:space="preserve"')
    text(280 if mobile else 205, 554 if mobile else 596, "AVATAR / ASCII", 10, "muted", extra='text-anchor="middle" letter-spacing="2"')

    x = 30 if mobile else 435
    start = 601 if mobile else 142
    text(x, start, config["prompt"], 25 if mobile else 23, "accent", "600")
    rule(x, start+18, width-30)
    if not mobile:
        out.append(f'<path d="M398 116V595" stroke="{colors["border"]}"/>')

    chord = data["releases"]["chordshot-releases"]
    node = data["releases"]["nodetaker-releases"]
    folder = data["releases"]["folder-reader-releases"]
    rows = [
        ("Name", config["name"]),
        ("Focus", config["focus"]),
        ("Desktop", config["desktop"]),
        ("Approach", config["approach"]),
        ("ChordShot", clip(chord["tag"], 20) + (" / public beta" if chord["prerelease"] else " / Mac release")),
        ("Nodetaker", clip(node["tag"], 20) + (" / public beta" if node["prerelease"] else " / Mac release")),
        ("Folder Reader", clip(folder["tag"], 20) + (" / preview" if folder["prerelease"] else " / Mac release")),
        ("Open code", config["open_code"]),
    ]
    for i, (label, value) in enumerate(rows):
        y = start + 54 + i*(29 if mobile else 32)
        text(x, y, label, 15 if mobile else 15, "key")
        text(x+142, y, clip(value, 35 if mobile else 46), 16, "text")

    stat_y = 925 if mobile else 490
    rule(x, stat_y-24, width-30)
    text(x, stat_y, "PUBLIC GITHUB", 11, "muted", extra='letter-spacing="2"')
    langs = ["JS" if n == "JavaScript" else n for n in data["languages"]]
    language_text = " / ".join(langs[:4]) or "No public code yet"
    if len(langs) > 4:
        language_text += f" / +{len(langs)-4}"
    since = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")).strftime("%b %Y")
    stats = [("Repos", f'{data["public_repos"]:02d} public / joined {since}'),
             ("Languages", language_text),
             ("Updated", data["updated"]+" UTC")]
    for i, (label, value) in enumerate(stats):
        y = stat_y+32+i*29
        text(x, y, label, 15, "key")
        text(x+142, y, clip(value, 35 if mobile else 46), 16, "text")

    rule(22, height-48, width-22)
    text(28, height-20, "~ % build something useful", 13, "muted")
    out.append(f'<rect class="cursor" x="239" y="{height-31}" width="8" height="14" rx="1" fill="{colors["accent"]}"/>')
    if not mobile:
        text(width-28, height-20, "LOCAL TOOLS. REAL WORK.", 10, "muted", extra='text-anchor="end" letter-spacing="2"')
    out.append('</svg>')
    return "\n".join(out)+"\n"


def update(input_path=None, root=ROOT):
    config = json.loads((root/"profile.json").read_text())
    art = (root/"art/avatar.txt").read_text().splitlines()
    if not art or len(art) > 43 or max(map(len, art)) > 56:
        raise ValueError("ASCII art must fit 56 columns by 43 rows")
    data = json.loads(Path(input_path).read_text()) if input_path else collect_snapshot(config)
    validate_snapshot(data, config)
    # Finish all fetches and renders before replacing the last known-good artifacts.
    files = {}
    for theme in ["dark", "light"]:
        for size in ["desktop", "mobile"]:
            files[f"assets/terminal-{size}-{theme}.svg"] = render(config, data, art, theme == "dark", size == "mobile")
    files["data/public-profile.json"] = json.dumps(data, indent=2)+"\n"
    for relative, content in files.items():
        target = root/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix+".tmp")
        temporary.write_text(content)
        temporary.replace(target)
    print(f'Rendered four terminal cards from public data dated {data["updated"]}.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Render an existing public-data snapshot without network access")
    args = parser.parse_args()
    update(args.input)
