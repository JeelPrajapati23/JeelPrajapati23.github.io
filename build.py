"""Builds the project pages and 404 page from shared templates.

Run `python3 build.py` after editing page content below. index.html is edited by hand.
"""
from pathlib import Path

ROOT = Path(__file__).parent
FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">"""


def head(title, desc, root):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{root}assets/styles.css">
</head>
<body>
<div class="wrap">
  <nav aria-label="Primary">
    <a class="mark" href="{root}index.html">jeel.</a>
    <ul>
      <li><a href="{root}index.html#projects" aria-current="page">Projects</a></li>
      <li><a href="{root}index.html#approach">Approach</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
  </nav>
"""


CONTACT = """
  <section id="contact" aria-labelledby="contact-h" style="border-top:0">
    <div class="contact">
      <h2 id="contact-h">Hiring for backend or applied AI?</h2>
      <p>I'm looking for software engineering roles. Email is the fastest way to reach me.</p>
      <div class="mailrow">
        <span class="mail" id="email">jeelprajapati2006@gmail.com</span>
        <button class="copy" id="copy-email" type="button">Copy</button>
      </div>
      <a href="https://github.com/JeelPrajapati23">github.com/JeelPrajapati23 ↗</a>
    </div>
  </section>
"""


def foot(root):
    return f"""
  <footer><span>© 2026 Jeel Prajapati</span><a href="https://github.com/JeelPrajapati23">GitHub</a></footer>
</div>
<script src="{root}assets/main.js"></script>
</body>
</html>
"""


PROJECTS = [
    {
        "slug": "pr-review-agent",
        "name": "PR Review Agent",
        "desc": "A multi-agent GitHub App that reviews pull requests and posts one-click fixes. 14 of 15 injected bugs caught with zero false positives.",
        "kicker": "LLM agents · GitHub App",
        "pitch": "Two AI reviewers read every pull request and post fixes you can apply with one click.",
        "links": [("Source ↗", "https://github.com/JeelPrajapati23/PR-Review-Agent")],
        "stack": ["Python", "FastAPI", "Celery", "Redis", "LangGraph", "MCP", "Groq gpt-oss-120b", "Docker", "Caddy"],
        "stats": [("14/15", "injected bugs caught across security, performance and structure"),
                  ("0", "false positives across all 15 test cases"),
                  ("0.946", "F2 score, weighting recall 4× over precision")],
        "problem": [
            "A single generic prompt makes a poor code reviewer. It either misses real bugs or buries them in vague advice. I wanted reviews that are specific and actionable, and cheap enough to run on Groq's free tier.",
            "There's a harder problem underneath. A reviewer that can verify its claims has to run the PR's tests, which means executing code written by whoever opened the PR. So the system is built around two real risks: running out of API budget, and running untrusted code.",
        ],
        "steps": [
            ("Receive the webhook", "GitHub sends a <code>pull_request</code> event. The body is HMAC-SHA256 verified, and only <code>opened</code> and <code>synchronize</code> actions continue."),
            ("Deduplicate", "A Redis lock (<code>SET NX EX 900</code>) turns GitHub's redeliveries of the same commit into no-ops instead of second reviews."),
            ("Queue and return", "The job goes to Celery and the webhook returns <code>202</code> immediately. Nothing waits on the analysis."),
            ("Check budget and clone", "The worker skips drafts, checks the shared daily token budget, posts a pending status, and shallow-clones the branch with a short-lived GitHub App token."),
            ("Security review", "The Security Warden looks for injection, OWASP issues, vulnerable dependencies and data leaks, using read-only MCP tools scoped to the changed files."),
            ("Performance and logic review", "A second specialist looks at complexity, correctness, races and off-by-ones. It runs sequentially to stay under Groq's per-minute limit."),
            ("Synthesize", "A Synthesizer merges both reports into one structured review and removes overlap."),
            ("Ground or fail", "If every claim references a file the panel actually read, inline suggestions and the review are posted. Otherwise it posts a failure status."),
        ],
        "decisions": [
            ("Specialists over one prompt", "Each agent has a narrow scope and its own tools, so findings are sharper and the Synthesizer can route them into the right section.", "Quality"),
            ("Fail closed", "A review that mentions a file nobody opened is treated as a hallucination. The PR gets a failure status, never a degraded review.", "Trust"),
            ("Sandboxed test runs", "The MCP server that runs the PR's tests uses a stripped environment and dropped privileges, so a malicious PR can't leak secrets through its test output into the model's context.", "Security"),
            ("Crash-safe and budget-aware", "Every agent step is checkpointed to Redis through LangGraph, so a crashed worker resumes instead of re-spending tokens. A daily budget gate skips new reviews with a neutral status when quota runs low.", "Cost"),
        ],
        "table": {
            "head": ["Category", "Recall", "Precision", "F2"],
            "rows": [["Security", "5/5 (100%)", "1.000", "1.000"],
                     ["Performance", "5/5 (100%)", "1.000", "1.000"],
                     ["Structural", "4/5 (80%)", "1.000", "0.833"]],
            "total": ["Overall", "14/15 (93.3%)", "1.000", "0.946"],
        },
        "fine": "Measured on a 15-fixture golden dataset of deliberately injected bugs (SQL injection, race conditions, off-by-one errors and more), graded by an independent LLM judge (Gemini). The harness is in <code>evaluation/</code>.",
        "extra_title": "Deployment",
        "extra": "<p>Runs with Docker Compose on an Oracle Cloud Always Free VM behind Caddy for automatic HTTPS. GitHub Actions redeploys over SSH on every push. The test suite is fully mocked and makes no live Redis, Groq or GitHub calls, with a separate opt-in integration suite.</p>",
    },
    {
        "slug": "clauseiq",
        "name": "ClauseIQ",
        "desc": "Multi-tenant RAG for legal contracts with claim-level answer verification. 0.89 faithfulness on 68 CUAD questions.",
        "kicker": "Retrieval-augmented generation · Legal",
        "pitch": "Ask questions about your contracts, or compare several at once, and every answer is fact-checked against the source.",
        "links": [("Live app ↗", "https://clauseiq-rag.vercel.app"), ("Source ↗", "https://github.com/JeelPrajapati23/ClauseIQ")],
        "stack": ["Python", "FastAPI", "Qdrant", "BM25", "Cohere Rerank", "Gemini 2.5 Flash", "Postgres", "React", "Vite", "Ragas", "Docker"],
        "stats": [("0.89", "faithfulness on 68 questions from real CUAD contracts"),
                  ("0.83", "context recall, up from 0.69 with the previous model"),
                  ("6/6", "out-of-scope questions refused with zero LLM calls")],
        "problem": [
            "Contracts are long and precise, and a confident wrong answer about a clause is worse than no answer. Most RAG demos stop at \"the answer sounds right\".",
            "ClauseIQ is built so that every answer is grounded in the user's own documents, checked claim by claim before it's trusted, and kept private to the account that uploaded them.",
        ],
        "steps": [
            ("Classify the question", "Keyword rules label it <code>FACT</code> or <code>ANALYTICAL</code>, which picks the retrieval width and system prompt without an extra LLM call."),
            ("Rewrite follow-ups", "Questions like \"what about that clause?\" are rewritten into standalone queries using the conversation, only when needed."),
            ("Hybrid retrieve", "Qdrant vector search and BM25 are fused with Reciprocal Rank Fusion, filtered to the user's own documents."),
            ("Rerank and expand", "Cohere reranks the hits, then each small child chunk is swapped for its full parent clause."),
            ("Refuse if empty", "If nothing relevant came back, a canned refusal streams with zero LLM calls."),
            ("Stream the answer", "Gemini 2.5 Flash streams the answer token by token over Server-Sent Events, with sources alongside."),
            ("Verify claims", "A second pass extracts each factual claim and checks it against the retrieved text for a supporting quote, giving PASS, PARTIAL or FAIL and a 0 to 1 score."),
        ],
        "decisions": [
            ("Parent-child chunking", "Small 350-character chunks give precise search hits. The model then sees the 2,000-character parent section, so it reads whole clauses instead of fragments.", "Retrieval"),
            ("Claims extracted blind", "The claim extractor doesn't see the retrieved context, so it can't be biased toward claims that happen to be supported.", "Trust"),
            ("Same-origin cookie auth", "The frontend proxies <code>/api/*</code> to the backend, so the auth cookie can be <code>SameSite=Lax</code>. That survives Brave, Safari and Firefox tracking protection without moving tokens into headers.", "Security"),
            ("Isolation at the vector layer", "Every Qdrant query, write and delete is filtered by <code>user_id</code>, and chat history lives in Postgres, so data follows the account across devices and never crosses tenants.", "Multi-tenancy"),
        ],
        "table": {
            "head": ["Metric", "Gemini 2.5 Flash", "Previous (gpt-oss-20b)"],
            "rows": [["Faithfulness", "0.89", "0.68"],
                     ["Answer relevancy", "0.69", "0.69"],
                     ["Context precision", "0.66", "0.59"],
                     ["Context recall", "0.83", "0.69"]],
            "total": None,
        },
        "fine": "68 questions derived from CUAD commercial contracts, run through the real production pipeline and scored offline with Ragas. A separate Groq-hosted judge does the grading, so no model grades its own answers. By type: factual 0.85 (44), analytical 0.97 (18), out-of-scope 1.00 (6).",
        "extra_title": "Production",
        "extra": "<p>The live app runs across four managed services: Vercel for the frontend, Render for the API, Neon for Postgres and Qdrant Cloud for vectors, all redeploying on every push to <code>main</code>. Security includes httponly JWT cookies, per-IP rate limiting plus per-account lockout, CSP and HSTS headers, filename sanitizing against path traversal, and an audit log of every account and data action.</p>",
    },
    {
        "slug": "reachfix",
        "name": "reachfix",
        "desc": "A dependency and vulnerability knowledge graph that finds how a CVE reaches your project and the smallest upgrade that fixes it.",
        "kicker": "Supply-chain security · Knowledge graph",
        "pitch": "Finds which of your projects a vulnerability reaches, through which dependencies, and the smallest upgrade that fixes it.",
        "links": [("Live demo ↗", "https://reachfix-latest.onrender.com"), ("Source ↗", "https://github.com/JeelPrajapati23/reachfix")],
        "stack": ["Python", "NetworkX", "OSV.dev", "npm registry", "MiniLM embeddings", "Groq gpt-oss-120b", "MCP", "uv", "Docker"],
        "stats": [("556/556", "version matches agree with OSV's own matching"),
                  ("20/20", "uploaded lockfile scans identical to the graph"),
                  ("24/24", "answers cite the graph facts and advisories they use")],
        "problem": [
            "\"Is my project affected by this CVE?\" sounds like a search question, but it isn't. The vulnerable package is usually several hops down the dependency tree, and the obvious fix often breaks a version range some other package declares.",
            "Similarity search over advisory text can't follow those chains. reachfix combines a dependency graph with semantic search, and keeps the LLM on two narrow, checkable jobs.",
        ],
        "steps": [
            ("Resolve pinned trees", "Each project is resolved with <code>npm install --before=&lt;date&gt;</code>, so the tree matches what a real project would have installed at the time."),
            ("Rebuild real edges", "Lockfile nesting isn't dependency depth because npm hoists packages. Edges are rebuilt with Node's own resolution rule."),
            ("Match vulnerabilities", "OSV advisories are matched with reachfix's own semver logic, which agrees with OSV's matching 556 out of 556 times."),
            ("Read the advisories", "An LLM extracts exploitability conditions from advisory text, and windowed MiniLM embeddings make that text searchable."),
            ("Route the question", "A router sends each question to semantic search, a relational graph query, or graph-guided hybrid retrieval."),
            ("Plan the fix", "For each vulnerable copy, find the lowest fixed version every dependent accepts. If one blocks it, upgrade the blocker, repeating up to the project."),
            ("Answer with citations", "Answers cite <code>[G#]</code> graph facts and <code>[A#]</code> advisory text, and are checked for any version or advisory ID that isn't in the evidence."),
        ],
        "decisions": [
            ("Date-pinned dependency trees", "A tree resolved today pulls the latest patches, so most historical vulnerabilities vanish. Pinning each install to its release date gives realistic, reproducible trees.", "Data"),
            ("“Fixed” means really fixed", "For CVE-2024-45296, the planner picks express 4.22.0 over 4.20.0, because 4.20.0 still allows a path-to-regexp version hit by a follow-up advisory.", "Correctness"),
            ("Deterministic first, LLM second", "Edges come from lockfiles and version ranges come from OSV. The LLM only extracts conditions and writes cited answers, both of which can be checked.", "Trust"),
            ("An npm override as a fallback", "When no clean upgrade exists, the plan still gives an npm <code>overrides</code> entry, clearly flagged as forcing a version outside a declared range.", "Usability"),
        ],
        "table": {
            "head": ["Check", "Result"],
            "rows": [["Semver matching vs OSV's own matching", "556/556 agree"],
                     ["Uploaded lockfile scans vs the graph (20 projects)", "20/20 identical"],
                     ["Router: route / relational pattern (24 questions)", "23/24 · 22/24"],
                     ["Answers citing evidence / fully grounded", "24/24 · 23/24"],
                     ["Answers mentioning every expected fact", "24/24"],
                     ["Advisory search precision@5 (package / vuln class)", "0.735 · 0.775"]],
            "total": None,
        },
        "fine": "Every check is derived from the graph or from OSV, not hand-labelled. The corpus is 20 date-pinned npm projects: 2,466 package versions and 296 OSV advisories. The question set is small, so the router prompt is never tuned against it.",
        "extra_title": "Example",
        "extra": """<pre class="example"><span class="p">$</span> uv run python scripts/ask_depgraph.py "How do I fix CVE-2024-45296 in express@4.17.1?"

my-api
└─ express@4.17.1
   └─ path-to-regexp@0.1.7   <span class="r">CVE-2024-45296</span>

fix: upgrade express to <span class="g">4.22.0</span>, or add an npm override</pre>
<p>You can try this in the hosted demo, scan your own <code>package-lock.json</code>, or connect it to Claude Code as an MCP server with tools like <code>project_exposure</code>, <code>dependency_path</code> and <code>plan_fix</code>.</p>""",
    },
]


def project_page(i):
    p = PROJECTS[i]
    prev_p = PROJECTS[i - 1]
    next_p = PROJECTS[(i + 1) % len(PROJECTS)]
    root = "../"
    links = "".join(
        f'<a class="btn{" solid" if j == 0 else ""}" href="{u}">{t}</a>' for j, (t, u) in enumerate(p["links"])
    )
    stack = "".join(f"<span>{s}</span>" for s in p["stack"])
    stats = "".join(f"<div><b>{n}</b><span>{t}</span></div>" for n, t in p["stats"])
    problem = "".join(f"<p>{t}</p>" for t in p["problem"])
    steps = "".join(f"<li><div><b>{t}</b><p>{d}</p></div></li>" for t, d in p["steps"])
    decisions = "".join(
        f'<div class="decision"><span class="why">{w}</span><h3>{t}</h3><p>{d}</p></div>' for t, d, w in p["decisions"]
    )
    tb = p["table"]
    th = "".join(f"<th>{h}</th>" for h in tb["head"])
    num = ' class="n"'

    def cells(r):
        return "".join(f"<td{num if k else ''}>{c}</td>" for k, c in enumerate(r))

    rows = "".join(f"<tr>{cells(r)}</tr>" for r in tb["rows"])
    if tb["total"]:
        rows += f'<tr class="total">{cells(tb["total"])}</tr>'

    body = f"""
  <div class="crumbs"><a href="{root}index.html#projects">Projects</a> / {p["name"]}</div>
  <header class="p-hero">
    <div class="kicker">{p["kicker"]}</div>
    <h1>{p["name"]}</h1>
    <p class="pitch">{p["pitch"]}</p>
    <div class="row">{links}</div>
    <div class="stack" style="margin-top:0">{stack}</div>
    <div class="stats3">{stats}</div>
  </header>

  <section class="split" aria-labelledby="why-h">
    <h2 id="why-h">The problem</h2>
    <div class="prose">{problem}</div>
  </section>

  <section class="split" aria-labelledby="how-h">
    <h2 id="how-h">How it works</h2>
    <ol class="steps">{steps}</ol>
  </section>

  <section aria-labelledby="dec-h">
    <div class="sec-title"><h2 id="dec-h">Design<br>decisions</h2><p>The choices that shaped the system, and why.</p></div>
    <div class="decisions">{decisions}</div>
  </section>

  <section class="split" aria-labelledby="res-h">
    <h2 id="res-h">Results</h2>
    <div>
      <div class="table-wrap"><table class="res"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
      <p class="fine">{p["fine"]}</p>
    </div>
  </section>

  <section class="split" aria-labelledby="extra-h">
    <h2 id="extra-h">{p["extra_title"]}</h2>
    <div class="prose">{p["extra"]}</div>
  </section>

  <section aria-label="More projects">
    <div class="pager">
      <a href="{prev_p["slug"]}.html"><span>← Previous project</span><b>{prev_p["name"]}</b></a>
      <a class="next" href="{next_p["slug"]}.html"><span>Next project →</span><b>{next_p["name"]}</b></a>
    </div>
  </section>
"""
    html = head(f'{p["name"]} · Jeel Prajapati', p["desc"], root) + body + CONTACT + foot(root)
    (ROOT / "projects" / f'{p["slug"]}.html').write_text(html)


def not_found():
    # 404.html is served at any missing path, so it uses absolute asset URLs.
    body = """
  <div class="lost">
    <h1>404</h1>
    <p class="lede" style="font-size:22px;max-width:28em">This page doesn't exist. It may have moved, or the link has a typo.</p>
    <div class="actions"><a class="btn solid" href="/">Back to the home page</a><a class="btn" href="/#projects">See projects</a></div>
  </div>
"""
    html = head("Page not found · Jeel Prajapati", "This page doesn't exist.", "/") + body + foot("/")
    (ROOT / "404.html").write_text(html)


if __name__ == "__main__":
    for i in range(len(PROJECTS)):
        project_page(i)
    not_found()
    print("built", len(PROJECTS), "project pages + 404")
