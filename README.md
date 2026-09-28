# jeelprajapati23.github.io

My portfolio site, served by GitHub Pages at **https://jeelprajapati23.github.io**.

Plain HTML, CSS and a little JavaScript. No framework and no build step needed to deploy.

```
index.html              home page
projects/*.html         one page per project (generated)
404.html                not-found page (generated)
assets/styles.css       all styles, light and dark
assets/main.js          terminal tabs and copy-email button
build.py                regenerates projects/*.html and 404.html
```

## Editing

- **Home page:** edit `index.html` directly.
- **Project pages:** edit the `PROJECTS` list in `build.py`, then run `python3 build.py`.
- **Preview locally:** `python3 -m http.server` and open http://localhost:8000.

Pushing to `main` publishes the site.
