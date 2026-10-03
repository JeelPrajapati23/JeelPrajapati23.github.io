# jeelprajapati23.github.io

My portfolio site, served by GitHub Pages at **https://jeelprajapati23.github.io**.

Plain HTML, CSS and a little JavaScript. No framework and no build step needed to deploy.

```
index.html              home page
about.html              about page (generated)
projects/*.html         one page per project (generated)
404.html                not-found page (generated)
assets/styles.css       all styles, light and dark
assets/main.js          terminal tabs and copy-email button
assets/video/           demo video and poster image per project
build.py                regenerates projects/*.html and 404.html
```

## Editing

- **Home page:** edit `index.html` directly.
- **Project pages:** edit the `PROJECTS` list in `build.py`, then run `python3 build.py`.
- **Always run `python3 build.py` before pushing.** It also stamps every page with a version tag for the CSS and JS, so browsers never keep a stale copy.
- **Preview locally:** `python3 -m http.server` and open http://localhost:8000.

Pushing to `main` publishes the site.
