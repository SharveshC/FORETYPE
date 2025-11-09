<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>FORETYPE – Multi-Domain Autocomplete and Project Workspace</title>
  <style>
    :root{--bg:#0f1720;--card:#0b1220;--muted:#9aa4b2;--accent:#60a5fa;color-scheme:dark}
    body{font-family:Inter,system-ui,Segoe UI,Roboto,"Helvetica Neue",Arial,sans-serif;background:var(--bg);color:#e6eef6;margin:0;padding:32px;line-height:1.5}
    .container{max-width:900px;margin:0 auto;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));padding:28px;border-radius:12px;box-shadow:0 6px 30px rgba(2,6,23,0.6)}
    h1{font-size:1.6rem;margin:0 0 10px}
    p.lead{color:var(--muted);margin-top:0}
    hr{border:0;border-top:1px solid rgba(255,255,255,0.04);margin:20px 0}
    h2{margin:18px 0 8px;font-size:1.05rem}
    ul{margin:8px 0 12px 20px;color:var(--muted)}
    pre{background:#071226;padding:12px;border-radius:8px;overflow:auto;color:#dbeafe;font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", "Courier New", monospace}
    code{background:rgba(255,255,255,0.02);padding:0 6px;border-radius:4px}
    .grid{display:grid;gap:12px}
    .meta{color:var(--muted);font-size:0.95rem}
    .footer{margin-top:18px;color:var(--muted);font-size:0.9rem}
    .pill{display:inline-block;background:rgba(96,165,250,0.12);color:var(--accent);padding:4px 8px;border-radius:999px;font-weight:600;font-size:0.85rem}
  </style>
</head>
<body>
  <main class="container" role="main">
    <header>
      <h1>🔤 FORETYPE – Multi-Domain Autocomplete and Project Workspace</h1>
      <p class="lead">This repository combines an intelligent <strong>Autocomplete System using Trie &amp; Bloom Filter</strong> with a structured <strong>multi-domain project workspace</strong>. It serves as both a technical demo and a practical development environment.</p>
      <div class="meta"><span class="pill">Python</span> <span style="margin-left:8px" class="pill">Automation</span></div>
    </header>

    <hr />

    <section>
      <h2>🧩 Autocomplete System Overview</h2>
      <p>An adaptive <strong>Autocomplete System</strong> built in Python that suggests words based on user input. It combines <strong>Trie</strong> and <strong>Bloom Filter</strong> for fast lookups and uses persistent frequency tracking.</p>

      <h3>Features</h3>
      <ul>
        <li><strong>Trie</strong> for efficient prefix-based storage and search</li>
        <li><strong>Bloom Filter</strong> for probabilistic membership testing</li>
        <li><strong>Frequency Dictionary</strong> to track and learn user preferences</li>
        <li><strong>CLI Interface</strong> for interactive suggestions</li>
      </ul>

      <h3>Implementation Details</h3>
      <ul>
        <li>Python 3.8+</li>
        <li>Uses <code>pybloom-live</code>, <code>pickle</code>, and <code>os</code></li>
        <li>Persists learning data in <code>word_freq.pkl</code></li>
      </ul>
    </section>

    <hr />

    <section>
      <h2>🧱 FORETYPE Project Structure</h2>
      <p>A structured workspace for organizing multiple engineering and data projects.</p>
      <pre><code>FORETYPE/
 ├─ FINAL/                 # Completed builds
 │   ├─ avi/               # Aviation system files and reports
 │   ├─ mydb/              # Database schema and seed data
 │   ├─ plots/             # Charts and visual outputs
 │   ├─ scripts/           # Automation and processing scripts
 │   └─ others/            # Docs, logs, and support files
 ├─ Typr/                  # Typing automation script and docs
 ├─ LICENSE
 └─ README.md
</code></pre>

      <h3>Tech &amp; Tools</h3>
      <ul>
        <li>Python</li>
        <li>SQL</li>
        <li>Automation scripts</li>
        <li>Data processing utilities</li>
        <li>Visualization tools</li>
      </ul>
    </section>

    <hr />

    <section>
      <h2>▶️ Usage</h2>

      <h4>Run Autocomplete System</h4>
      <pre><code>python autocomplete.py</code></pre>

      <h4>Run a Python Utility</h4>
      <pre><code>python filename.py</code></pre>

      <h4>Apply DB Schema</h4>
      <pre><code>mysql -u root -p &lt; schema.sql</code></pre>
    </section>

    <hr />

    <section>
      <h2>📦 Contents</h2>
      <ul>
        <li>Database exports &amp; seed files</li>
        <li>Frequency/usage datasets</li>
        <li>System logs and documentation</li>
        <li>Plots and visual outputs</li>
      </ul>

      <h3>🔧 Future Improvements</h3>
      <ul>
        <li>Convert manual modules into reusable services</li>
        <li>Add CLI interface for automation</li>
        <li>Integrate logging and test coverage</li>
        <li>Docker setup for reproducibility</li>
      </ul>
    </section>

    <hr />

    <footer class="footer">
      <div><strong>License</strong>: MIT License for Autocomplete System. Educational and development use for FORETYPE.</div>
    </footer>
  </main>
</body>
</html>
