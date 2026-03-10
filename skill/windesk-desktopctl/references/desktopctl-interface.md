# Desktopctl interface reference

This reference summarizes the bundled desktop control script interface.

## Safe roots

Only paths under these roots are allowed:

- `C:\Github`
- `C:\Users`

## Commands

### list-files

```text
list-files --path <PATH>
```

Returns JSON with:

- `ok`
- `path`
- `items[]` with `name`, `path`, `is_dir`, and optional `size`

### read-file

```text
read-file --path <PATH> [--encoding utf-8] [--max-bytes 200000]
```

Returns decoded text content and a `clipped` flag when truncated.

### open-app

```text
open-app --target <TARGET>
```

Launches an executable path or a command found on PATH.

### screenshot

```text
screenshot
```

Saves a screenshot under `C:\openclaw\screenshots`.

### mouse-click

```text
mouse-click --x <X> --y <Y> [--button left] [--clicks 1]
```

### type-text

```text
type-text --text <TEXT>
```

### hotkey

```text
hotkey <KEYS...>
```

Example:

```text
hotkey ctrl s
```

## Notes

- `read-file` is intended for text-like content.
- Large file reads are clipped at the configured byte limit.
- For `list-files`, directory sizes are not returned.
