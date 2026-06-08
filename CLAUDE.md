# Project Rules

## Output Display Rule (MANDATORY)

After completing **every task** that produces or modifies a file (HTML, SVG, image, or any deliverable), you MUST call `SendUserFile` to display the file to the user.

- Call `SendUserFile` at the end of every task turn — no exceptions, no need to ask.
- Use `status: "normal"` for replies, `status: "proactive"` for background completions.
- Include a short `caption` describing what the file is.
- If multiple files were produced, send all of them in a single `SendUserFile` call.
