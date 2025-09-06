**Prompt:**

Review the contest rules, understanding the rules, the time is currently 1 PM eastern standard time on 09/06/2025. We only have 2 hours to get this project done.

My group has an idea of building a content media agent that uses Gemini CLI that accesses photos from from google cloud, then see if you get the digital footprint of the photo and then try to categorize those photos by the digital footprint starting with location, type of photo (subject based and then emotion based), data and anything else I may have missed. Then from there, we need the content media agent to be able to do two things, write a script for a podcast based on the photos and also make textual posts along with photos to instagram automatically.

Build a workplan for this idea based on the contest rules:

"AI Tinkerers × Google — Gemini CLI Buildathon  
Saturday Sep 6, 2025 ⋅ 11am – 4pm (Eastern Time \- New York)  
Important reminders (day‑of):

* Arrive before the 11:00 AM kick‑off so you don’t miss the live Google quickstart. The event is a focused 4‑hour in‑person sprint (approx. 11:00 AM–3:00 PM local).  
* Bring a laptop, power, and any local data you’re comfortable using (synthetic/sample data is fine). Be prepared to prototype and demo working code.  
* RSVP now — space is limited. Check the event page for the venue and any additional logistics.  
  Event at a glance:  
* Title: AI Tinkerers × Google — Gemini CLI Buildathon  
* Theme: Creative, Personal & Local  
* Format: 4‑hour in‑person buildathon (fast, focused, ship‑something energy). Teams prototype headless AI agents/workflows that use the Google Gemini CLI/API to interact with local files, data, scripts, sensors, and shell tools. Production deployment is not required.

Kick‑off:

* Live Google session at 11:00 AM: lightning demo \+ quickstart from Jerop Kipruto (Google) to get you started with Gemini CLI.

What to build / examples:

* Research Wrangler: extract findings from PDFs and produce structured notes.  
* Story Forge: generate a custom story \+ image assets saved to disk.  
* Writing Stitcher: assemble a cohesive story from an outline \+ scattered markdown.  
* CLI Lab Assistant: natural‑language wrapper around shell commands to search/transform/summarize files.  
* Data‑Aware Agents: use local CSVs/logs/configs to personalize outputs, alerts, or dashboards.

Judging (100 points total):

* 30% Impact & Innovation — meaningful problem solved, new pattern, personal/local workflow others can adopt.  
* 30% Gemini Integration — depth/creativity of Gemini usage (tool calling, multimodal, chaining, eval loops, etc.).  
* 20% Technical Excellence — robust, working code; reliable end‑to‑end demo.  
* 20% Solution Architecture & Documentation — clear repo structure, install/run steps, README and inline docs for reproducibility.  
* Ties broken by Impact. Tip: focus on a compelling prototype that clearly demonstrates Gemini CLI capabilities.

Submission requirements (must be submitted by 3:00 PM local on September 6th to be eligible):

1. Code repository — public or invite‑only (grant judge access). Include install and run instructions.  
2. ≤ 3‑minute demo video (screen capture is fine). The video must show the project running and demonstrate how Gemini is used.

Quick tips:

* Prioritize a working end‑to‑end prototype over polish.  
* Use local files/data to show grounded, personal workflows.  
* Documentation and reproducibility help scoring significantly."

**Response:**

Excellent idea\! A content media agent is a fantastic fit for the "Creative, Personal & Local" theme. Given the 2-hour time limit, we need a focused, realistic, and aggressive work plan that prioritizes a demonstrable prototype over polished features.

Here is a work plan built for speed and to maximize your score based on the contest rules.

### **Project Title: "Photo Scribe"**

**Core Concept (The 2-Hour MVP):** A command-line agent that ingests a **local folder of photos**, uses the Gemini CLI's multimodal capabilities to analyze and understand them, and then chains that understanding into a second Gemini CLI call to generate a creative podcast script.

This MVP is focused, hits all the key judging criteria, and is achievable in the time remaining. We are intentionally replacing Google Cloud access with local file access and dropping the Instagram integration to ensure a working end-to-end demo.

---

### **Work Plan: 1:00 PM \- 3:00 PM EST**

#### **Phase 1: Setup & Scoping (1:00 PM \- 1:15 PM | 15 Minutes)**

* **\[5 mins\] Finalize MVP & Roles:**  
  * **Decision:** Agree to use a local /photos directory, not Google Cloud. Agree to generate a podcast script as the primary output, not Instagram posts.  
  * **Assign Roles:**  
    * **Lead Coder:** Responsible for writing the main Python script.  
    * **Docs & PM:** Creates the GitHub repo, writes the README *in parallel* with development, and keeps the team on schedule.  
    * **Demo & QA:** Gathers sample photos, tests the script, and prepares to record the demo video.  
  *   
*   
* **\[10 mins\] Project Initialization:**  
  * **Docs & PM:** Create a public GitHub repository.

**Docs & PM:** Create the basic project structure:  
 code Code  
downloadcontent\_copy  
expand\_less  
    photo-scribe/  
├── main.py  
├── photos/  
│   └── sample1.jpg  
│   └── sample2.png  
├── outputs/  
└── README.md

*    
  * **Everyone:** Confirm gcloud and the Gemini CLI are installed and authenticated on their machines.  
* 

#### **Phase 2: Core Development Sprint (1:15 PM \- 2:20 PM | 65 Minutes)**

* **\[25 mins\] Task 1: Single Image Analysis (Gemini Multimodal Vision)**  
  * **Lead Coder:** Write a Python function that takes a single image file path as an argument.  
  * Inside the function, use subprocess to call the Gemini CLI.

**Focus on the Prompt:** This is critical for the "Gemini Integration" score.  
 code Bash  
downloadcontent\_copy  
expand\_less  
IGNORE\_WHEN\_COPYING\_START  
IGNORE\_WHEN\_COPYING\_END  
    gemini chat "Analyze this photo. Return a JSON object with the following keys: 'description', 'inferred\_location', 'subjects', and 'dominant\_emotion'. Be descriptive. Photo to analyze:" \--model "gemini-1.5-pro" \--content ./photos/sample1.jpg

*    
  * The function should parse the JSON output from the CLI and return it as a Python dictionary.  
  * **Demo & QA:** Provide 3-5 diverse sample photos for testing.  
*   
* **\[20 mins\] Task 2: Batch Processing & Data Aggregation**  
  * **Lead Coder:** Wrap the function from Task 1 in a loop that iterates through all images in the /photos directory.  
  * Store the resulting JSON dictionary from each photo in a single list.  
  * At the end of the loop, convert the entire list of dictionaries into a single JSON string.  
*   
* **\[20 mins\] Task 3: LinkedIn Post Generation and Publishing (Gemini Chaining)**  
  * **Lead Coder (Python):** Create a second function that takes the aggregated JSON string of photo analyses as input.  
  * Make another subprocess call to the Gemini CLI, feeding it this data.

**Focus on the Chaining Prompt:** This demonstrates creative Gemini usage.  
    gemini chat "You are a social media manager. I'll provide a JSON array of photo analyses. Create a professional and engaging LinkedIn post that weaves these photos into a narrative. Use the descriptions, locations, and emotions to build the story. Include relevant hashtags. Format the output as a JSON object with 'post_text' and 'image_to_post' keys. Here is the photo data: [PASTE JSON STRING HERE]" \--model "gemini-1.5-pro"

* The function should parse the JSON output and then use a Python library (e.g., `requests` or a dedicated LinkedIn API library) to post the `post_text` and the corresponding image to LinkedIn. **(Note: For the demo, you can mock the final API call and print the post content to the console).**  
* Save the post text to a file in the /outputs directory (e.g., `linkedin_post.txt`).

#### **Phase 3: Frontend Wrapper Development (1:15 PM - 2:20 PM | 65 Minutes)**

* **[65 mins] Task 4: Node.js/TypeScript Frontend Wrapper**
    * **Lead Coder (Node.js):** Develop a simple web interface using TypeScript and Node.js (e.g., with Express and React/Vue).
    * The frontend should provide a button to trigger the Python script (`main.py`).
    * It should display the generated LinkedIn post text from the `outputs/linkedin_post.txt` file.
    * This demonstrates a more complete solution architecture.

#### **Phase 4: Documentation & Demo Prep (2:20 PM - 2:45 PM | 25 Minutes)**

* **\[15 mins\] Finalize README & Code Comments**  
  * **Docs & PM:** Complete the README.md. It **must** include:  
    * Project title and a one-sentence description.  
    * How it uses Gemini CLI (multimodal analysis, text generation).  
    * **Installation:** `git clone ...`, `pip install ...`, `npm install`  
    * **How to Run:**  
      1. Place your .jpg or .png files in the /photos folder.  
      2. Run `python main.py`.  
      3. Run `npm start` in the `frontend` directory.  
      4. Open your browser to `http://localhost:3000`.  
      5. Find your post text in the `outputs` folder.  
  * **Lead Coders:** Clean up the scripts and add inline comments explaining the Gemini CLI calls. This is crucial for the "Documentation" score.  
* **\[10 mins\] End-to-End Test & Demo Rehearsal**  
  * **Everyone:** Do a full run-through. Delete the output file, run `python main.py`, run the frontend, and check the result.  
  * **Demo & QA:** Prepare the screen for recording. Have the code editor, the terminal, the /photos folder, the (empty) /outputs folder, and the web browser visible.  

#### **Phase 5: Record & Submit (2:45 PM - 3:00 PM | 15 Minutes)**

* **\[10 mins\] Record the 3-Minute Video**  
  * **(0:00 - 0:30):** Introduction. "We built Photo Scribe, an AI agent that uses the Gemini CLI to turn a local folder of photos into a LinkedIn post."  
  * **(0:30 - 2:00):** Live Demo.  
    * Show the sample photos in the /photos folder.  
    * Show the frontend wrapper in the browser.  
    * Click the button to trigger the script.  
    * Show the script executing in the terminal.  
    * Show the generated post in the browser and in the `outputs` folder.  
  * **(2:00 - 2:30):** Technical Showcase. Briefly show the two Gemini CLI prompts in your code, explaining the multimodal analysis and the chaining logic.  
  * **(2:30 - 3:00):** Conclusion. "This project demonstrates a personal and creative workflow, directly aligning with the buildathon's theme, and showcases the power of Gemini CLI for multimodal understanding and content generation."  
* **\[5 mins\] Final Submission**  
  * Push the final code and README to GitHub.  
  * Submit the repository link and video link. **Double-check that you have granted judge access if the repository is private.**  

**Good luck, Tinkerers\! This is a tight schedule, but by focusing on the core MVP, you can deliver a high-scoring project.**