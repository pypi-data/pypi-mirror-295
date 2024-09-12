# ansi-esc
`ansi-esc` is a python library for ANSI escape characters.

# Install
```bash
python3 -m pip install ansi-esc --upgrade
```

# Usage

## Colors
```python
from ansi_esc.font.colors import background as bg
from ansi_esc.font.colors import foreground as fg

print(fg.red+bg.blue + "Hello" + bg.off + " World!")
```

## Effects
```python
from ansi_esc.font import effects as eff

print(eff.underline + "Hello" + eff.underline_off + eff.blink + " World!")
```

# License
MIT
