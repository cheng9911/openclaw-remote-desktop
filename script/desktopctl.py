import argparse
import base64
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pyautogui
import pyperclip
from mss import mss

SAFE_ROOTS = [
    Path(r"C:\Github"),
    Path(r"C:\Users"),
]

SCREENSHOT_DIR = Path(r"C:\openclaw\screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15


def ok(**kwargs):
    print(json.dumps({"ok": True, **kwargs}, ensure_ascii=False))


def fail(message, **kwargs):
    print(json.dumps({"ok": False, "error": message, **kwargs}, ensure_ascii=False))
    sys.exit(1)


def resolve_safe_path(p: str) -> Path:
    path = Path(p).expanduser().resolve()
    for root in SAFE_ROOTS:
        try:
            path.relative_to(root.resolve())
            return path
        except ValueError:
            continue
    fail("path not allowed", path=str(path))


def cmd_list_files(path: str):
    p = resolve_safe_path(path)
    if not p.exists():
        fail("path not exists", path=str(p))
    if not p.is_dir():
        fail("path is not a directory", path=str(p))

    items = []
    for item in p.iterdir():
        items.append({
            "name": item.name,
            "path": str(item),
            "is_dir": item.is_dir(),
            "size": item.stat().st_size if item.is_file() else None,
        })
    ok(path=str(p), items=items)


def cmd_read_file(path: str, encoding: str = "utf-8", max_bytes: int = 200000):
    p = resolve_safe_path(path)
    if not p.exists() or not p.is_file():
        fail("file not found", path=str(p))

    data = p.read_bytes()
    clipped = False
    if len(data) > max_bytes:
        data = data[:max_bytes]
        clipped = True

    try:
        text = data.decode(encoding, errors="replace")
        ok(path=str(p), encoding=encoding, clipped=clipped, content=text)
    except Exception as e:
        fail("decode failed", detail=str(e))


def cmd_open_app(target: str):
    # 可传 exe 路径，也可传已在 PATH 中的命令
    try:
        subprocess.Popen(target, shell=True)
        ok(opened=target)
    except Exception as e:
        fail("open app failed", detail=str(e))


def cmd_screenshot():
    ts = time.strftime("%Y%m%d-%H%M%S")
    out = SCREENSHOT_DIR / f"shot-{ts}.png"
    with mss() as sct:
        shot = sct.shot(output=str(out))
    ok(path=str(out), file=shot)


def cmd_mouse_click(x: int, y: int, button: str = "left", clicks: int = 1):
    pyautogui.click(x=x, y=y, button=button, clicks=clicks)
    ok(x=x, y=y, button=button, clicks=clicks)


def cmd_type_text(text: str):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    ok(chars=len(text))


def cmd_hotkey(keys):
    pyautogui.hotkey(*keys)
    ok(keys=list(keys))


def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("list-files")
    p1.add_argument("--path", required=True)

    p2 = sub.add_parser("read-file")
    p2.add_argument("--path", required=True)
    p2.add_argument("--encoding", default="utf-8")
    p2.add_argument("--max-bytes", type=int, default=200000)

    p3 = sub.add_parser("open-app")
    p3.add_argument("--target", required=True)

    sub.add_parser("screenshot")

    p5 = sub.add_parser("mouse-click")
    p5.add_argument("--x", type=int, required=True)
    p5.add_argument("--y", type=int, required=True)
    p5.add_argument("--button", default="left")
    p5.add_argument("--clicks", type=int, default=1)

    p6 = sub.add_parser("type-text")
    p6.add_argument("--text", required=True)

    p7 = sub.add_parser("hotkey")
    p7.add_argument("keys", nargs="+")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list-files":
        cmd_list_files(args.path)
    elif args.command == "read-file":
        cmd_read_file(args.path, args.encoding, args.max_bytes)
    elif args.command == "open-app":
        cmd_open_app(args.target)
    elif args.command == "screenshot":
        cmd_screenshot()
    elif args.command == "mouse-click":
        cmd_mouse_click(args.x, args.y, args.button, args.clicks)
    elif args.command == "type-text":
        cmd_type_text(args.text)
    elif args.command == "hotkey":
        cmd_hotkey(args.keys)
    else:
        fail("unknown command")


if __name__ == "__main__":
    main()