---
name: windesk-desktopctl
description: execute desktopctl.bat file and desktop automation commands on a specified windows openclaw node by wrapping them in c:\windows\system32\cmd.exe /c, avoiding direct .bat execution, and turning json results into readable summaries. use when the user asks in natural language to list files, read files, take screenshots, open apps, click, type, or send hotkeys on a windows node such as windesk, and the node or tool paths may vary.
---

# WinDesk Desktopctl

Use this skill to run `desktopctl.bat` safely on a Windows OpenClaw node and present the result clearly.

## Required inputs

Before running anything, confirm or extract these values from the user's request:

- target node name, for example `WinDesk`
- desktopctl script path, default `C:\openclaw\desktopctl.bat`
- wrapper executable path, default `C:\Windows\System32\cmd.exe`
- the intended desktopctl subcommand and arguments

If the user gives a node name, use it exactly. Do not silently fall back to another node.

## Execution rule

Do not execute the batch file directly.
Always call desktopctl through:

`C:\Windows\System32\cmd.exe /c "<desktopctl.bat> <subcommand> <args>"`

When using the OpenClaw CLI, prefer this pattern:

```bash
openclaw nodes run --node <NODE> -- "C:\Windows\System32\cmd.exe" /c "<DESKTOPCTL> <SUBCOMMAND> <ARGS>"
```

Why this matters:

- direct `.bat` execution is less reliable
- forcing `cmd.exe` gives a stable executable path for approvals
- explicit `--node` prevents accidental routing to a Linux node

## Natural-language mapping

Map natural-language requests to desktopctl subcommands like this:

- list files in a folder → `list-files --path <PATH>`
- read a text file → `read-file --path <PATH>`
- open an app → `open-app --target <TARGET>`
- take a screenshot → `screenshot`
- click at coordinates → `mouse-click --x <X> --y <Y>`
- type text → `type-text --text <TEXT>`
- press keyboard shortcuts → `hotkey <KEYS...>`

If the request does not clearly map to one of the supported commands, say so and ask for a supported action.

## Output formatting

Convert raw JSON into readable results.

### Success

- start with a one-line summary of what ran, on which node
- for `list-files`, show directories first if practical, then files, including size when provided
- for `read-file`, show whether content was clipped and then show the content in a fenced block
- for `screenshot`, report the saved path
- for UI actions such as click, type, hotkey, or open-app, confirm the action and echo the main parameters

### Failure

- state that execution failed
- quote the most relevant error field or stderr
- explain the likely cause in plain language when clear, such as missing approvals, wrong node, or a blocked path
- include the exact wrapped command that was attempted when helpful for debugging

## Safety and routing checks

Before blaming desktopctl, check these common failure modes:

1. wrong node or missing `--node`
2. direct `.bat` execution instead of `cmd.exe /c`
3. malformed windows path quoting
4. approval, allowlist, or elevated-policy failures
5. path blocked by desktopctl safe-root rules

## Supported command reference

See `references/desktopctl-interface.md` for the currently supported desktopctl commands and path restrictions bundled with this skill.
