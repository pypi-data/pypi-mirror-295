# fh_utils

A collection of utilities for FastHTML projects.

## Dev

```bash
uv sync
uv run pytest
uv run demo
```

## Docs

Installation

```bash
pip install fh_utils
uv add fh_utils
```

### Tailwindcss and Daisycss

Add Tailwind / Daisy to your app

```python
from fh_utils.tailwind import add_daisy_and_tailwind, add_tailwind, tailwind_compile

app, rt = fast_app(pico=False, static_path="public")

# Usage 1
add_tailwind(app)

# Usage 2: If you use Daisycss
add_daisy_and_tailwind(app)

# Usage 3: To customize
add_tailwind(app, cfg=Path("tailwind.config.js").read_text(), css="your custom css")

# Usage 4: Serve via fasthtml static_route
# Attention: Don't forget to put public/app.css to your .gitignore
tailwind_compile("public/app.css")
app, rt = fast_app(hdrs=[Link(rel="stylesheet", href="app.css")], pico=False, static_path="public")
```

The tailwind CLI is downloaded. Your css are compiled, served and integrated.

#### Bonus: Use Tailwind CSS IntelliSense in vscode

- Step 1: Install the [extension](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)

- Step 2: Create `tailwind.config.js` file at the root of your project

- Step 3: Add to your `.vscode/settings.json`

```json
{
  // ...
  "tailwindCSS.classAttributes": ["class", "cls"],
  "tailwindCSS.includeLanguages": {
    "python": "html"
  }
}
```
