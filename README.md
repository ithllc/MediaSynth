## MediaSynth — Proof-of-Concept

This repository contains a small proof-of-concept (PoC) that demonstrates how agentic, multimodal
LLMs can be used to help content creators by analyzing photos and automatically generating a
single LinkedIn post that summarizes the images. This project is an experimental demo — not a
production system.

### Key changes applied
- `main.py` was updated to analyze multiple images concurrently using `ThreadPoolExecutor`.
- A global, thread-safe `RateLimiter` was added to ensure the script makes no more than 20
  requests per second to the LLM/CLI. This prevents accidental bursts when running many
  workers in parallel.
- `analyze_image()` now waits on the rate limiter before calling the Gemini CLI, extracts
  JSON output from the LLM response, and returns a parsed dictionary for each photo.
- The final `generate_linkedin_post()` call compiles all photo analyses into a summarized
  JSON and asks the LLM to produce a single LinkedIn post (returned as `post_text` and
  `image_to_post`).

Files changed
- `main.py` — concurrency, rate limiting, JSON extraction, and orchestration.

### How it works (high level)
1. The script finds image files in the `photos/` directory (`.png`, `.jpg`, `.jpeg`).
2. Images are analyzed concurrently by worker threads; each worker calls `analyze_image()`.
3. Before each Gemini CLI invocation the worker calls the shared `RateLimiter.wait()` so
   overall requests do not exceed 20/sec.
4. Each `analyze_image()` call requests a strict JSON response from the LLM, parses the
   JSON, and returns a structured analysis: `description`, `inferred_location`, `subjects`,
   and `dominant_emotion`.
5. When all analyses complete, the script calls `generate_linkedin_post()` with a summarized
   list of results (description + dominant_emotion). The LLM returns a JSON object containing
   `post_text` and `image_to_post`.
6. The generated `post_text` is written to `outputs/linkedin_post.txt` and a debug log is
   written to `debug.log` in the same folder as `main.py`.

### Usage
Requirements: Python 3.8+ and the Gemini CLI (or another LLM CLI the script is adapted to).

Run the script from the `MediaSynth` folder:

```bash
python3 main.py
```

Outputs:
- `outputs/linkedin_post.txt` — the generated LinkedIn post text.
- `debug.log` — detailed per-image logs and LLM stdout/stderr for debugging.

### Design notes — concurrency & rate limiting
- The script uses a `ThreadPoolExecutor` with a conservative default worker count: `min(8, max(2, os.cpu_count()))`.
- The `RateLimiter` implements a simple sliding-window/token-bucket-like mechanism using timestamps.
  It blocks a worker until a slot is available which ensures no more than `max_calls` are made
  in any `period` window (default: 20 calls per 1 second).

### Caveats and limitations (PoC warning)
- This is explicitly a proof-of-concept. It is intended to show that agentic and multimodal
  LLMs can be orchestrated to automate content-creation tasks. It is not hardened for
  production use: security, robust retries, backoff, authentication, rate-limit coordination
  across machines, and extensive input validation are out of scope.
- The Gemini CLI or LLM may require additional flags to actually upload/attach image files —
  currently the script passes the filename in the prompt; adapt the `command` list in
  `analyze_image()` if your CLI supports an image attachment flag (for example `-i <path>`).
- The LLM output parsing is robust for common JSON-wrapped outputs but can still fail if the
  model emits unexpected text. Adding stricter system prompts, output schemas, or a post-
  processing repair loop is recommended for production.

### Suggested improvements (next steps)
- Add retry + exponential backoff with jitter inside `analyze_image()` for transient API errors.
- Add a mock / dry-run mode for local testing (avoids calling Gemini during development).
- Add unit tests that mock `subprocess.run` for deterministic CI tests.
- Add configuration to surface the Gemini/LLM CLI image-attachment flag and credentials.

### Final reminder
This project is a demonstration: a PoC that proves the concept of using agentic, multimodal
LLMs to automate content workflows for creators. Do not use this script as-is for sensitive
or production workloads.

If you want, I can: add retries+backoff, implement a mock mode, or wire explicit image
attachment flags for the Gemini CLI — tell me which to do next.

## Install from GitHub
Clone this repository and prepare a Python virtual environment:

```bash
git clone https://github.com/ithllc/MediaSynth.git
cd MediaSynth
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# On Windows (PowerShell): .\venv\Scripts\Activate.ps1
# On Windows (cmd.exe): venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
```

After dependencies are installed, run the script from the project folder:

```bash
python3 main.py
```

### Gemini CLI (required)
This project invokes an external `gemini` command-line client. You must install and configure
the vendor's Gemini CLI before running the script. The exact installation method depends on
your platform and the vendor distribution channel; below are common options and guidance.

macOS (suggested)
- Install Homebrew (if you don't have it): https://brew.sh
- If the vendor publishes a Homebrew formula, you can install via Homebrew. Otherwise, follow
  the official Gemini CLI installer or Python package instructions from the vendor.
- Example (if available from vendor):

```bash
# (only if a Homebrew formula exists)
brew install gemini
# or (if the vendor distributes a pip package)
pip install gemini-cli
```

Windows 10 or newer
- Use the vendor MSI installer (if provided) or a package manager such as Chocolatey/Scoop if
  the vendor supports it. Alternatively, some vendors publish a Python package which can be
  installed into the project's virtualenv via `pip`.
- Example (PowerShell):

```powershell
# If vendor provides an installer: run the MSI or follow vendor instructions
# If using pip in the activated venv:
pip install gemini-cli
```

Important: the `gemini` CLI often requires authentication (credentials or API key). After
installing the CLI, follow the vendor's authentication/setup steps so that running `gemini`
from your shell is authorized and returns expected outputs.

If you don't have access to the Gemini CLI or prefer to test locally, add a mock/dry-run
implementation (I can help add that) so the script can be tested without calling the real
service.

Content / Media Synth

Overview

Creators, executives, and community leaders capture endless photos, clips, and documents during event-heavy weeks—but rarely turn them into content. Posts are delayed, inconsistent, or shallow. The backlog grows, and the narrative is lost.

Content / Media Synth is a local-first content strategist agent built on Gemini CLI + MCP. It transforms a chaotic week of media into polished, platform-ready posts in the user’s own voice.

⸻

Features
	•	Local-first: Reads directly from a user’s hard drive (photos, PDFs, notes) with privacy by default.
	•	Voice-trained: Learns from past posts to match tone and cadence.
	•	Smart curation: Recommends the right photos, cross-references downloaded reports, and selects safe images.
	•	POV generation: Produces LinkedIn longform and X/Warpcast variants that emphasize thought leadership over fluff.

⸻

Example Workflow

A VC attends six events in four days and downloads a new AI infrastructure whitepaper.
By Monday morning, Content / Media Synth produces:
	•	A polished LinkedIn POV post referencing the whitepaper.
	•	2 curated photos ready to publish.

⸻

Ideal Users
	•	Pro Creator–Strategist: A newsletter + speaking creator who needs consistent, high-signal posts without spending 10+ hours editing.
	•	Operator Exec/VC: A partner or GTM exec who wants authoritative posts (citations, insights, safe images) without the time burden.

⸻

Why It Matters

In a world where 54% of marketers cite lack of resources and 45% lack a scalable content model, our agent helps professionals stay consistent, credible, and human online—without burnout.
