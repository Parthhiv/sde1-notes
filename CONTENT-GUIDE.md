# Content & Notes Generation Guide for AI Models

> This file instructs AI models on how to generate learning content and notes
> that follow the SDE-1 syllabus methodology exactly.

---

## PART 1 — THE PHILOSOPHY

### The One Rule

**Every concept must answer "Why does this exist?" BEFORE explaining "What is it?"**

If you can't articulate the failure mode (in production or in an interview) that this knowledge prevents, the learner will forget the what. The why is the hook that makes knowledge sticky.

### The Four States of Knowing (applied to content generation)

Every piece of content must move the learner toward **State 3 (Explained)** minimum:

1. **Recognised** — "I've seen that word." → Content must NOT leave learner here.
2. **Recalled** — Can define from memory. → Content must go beyond definitions.
3. **Explained** — Can teach it to someone else including WHY it works that way. → This is the minimum target.
4. **Applied** — Reaches for it unprompted while solving something new. → Build projects push here.

### The Tier-3 Gap Framework

Content must address the four specific gaps the syllabus targets:

| Gap | What it looks like | How content fixes it |
|-----|-------------------|---------------------|
| No mental model of the machine | Knows `async/await` but not what a thread is | Explain the machine underneath every abstraction |
| No exposure to scale | College project had 1 user and 50 rows | Show what breaks at scale (N+1, cache stampede) |
| No design vocabulary | Can make it work but can't defend a choice | Name the trade-off, not just the pattern |
| No "why" behind tooling | Uses React/EF Core as magic boxes | Show what happens underneath |

---

## PART 2 — HOW TO TEACH A CONCEPT

### The Concept Teaching Template

For EVERY concept (atom), follow this sequence:

```
1. THE PROBLEM (1-2 paragraphs)
   - What failure mode exists without this knowledge?
   - What does a developer NOT know that causes bugs/interview failures?
   - Concrete scenario: "Here's what goes wrong..."

2. THE MENTAL MODEL (1 paragraph, no jargon)
   - How should the learner THINK about this?
   - Use an analogy if possible
   - This is the paragraph they should be able to recite

3. THE EXPLANATION (the actual content)
   - Code examples (show, don't just tell)
   - Break it deliberately — show the wrong way, then the right way
   - Connect to something they already know

4. THE GOTCHAS
   - What bites people in practice?
   - What's the common misconception?
   - What would a senior interviewer probe?

5. INTERVIEW SHAPED QUESTIONS
   - "Why does X work this way?" (not "What is X?")
   - Questions that test understanding, not recall
```

### Code Example Rules

- **Always show the broken version first** — then fix it
- **Use variable names that explain themselves** — `userArray` not `arr`
- **Add comments that explain WHY, not WHAT** — `// Hoisted as undefined, not declared`
- **Show output inline** — don't make the learner guess
- **Progress complexity** — simple → medium → real-world

### Explanation Style

- **Write as if explaining to a junior developer who knows basic syntax**
- **Use "you" language** — "You'll see this when..." not "Developers will see..."
- **Be direct** — no filler phrases like "It's important to note that..."
- **Use concrete numbers** — "a context switch costs ~1-10 microseconds" not "it's expensive"
- **Connect modules** — "This is exactly what Atom 10.4.11 explains about cache lines"

---

## PART 3 — HOW TO GENERATE NOTES (For the Notes Agent)

### File Structure

One file per unit. Filename format:
```
{module-number}-{unit-number}-{unit-name-slug}.md
```
Example: `01-01-the-execution-model.md`

### Required Sections (in order)

```markdown
# Unit {number} — {Name}

> **Why this exists.** {this is non-negotiable}

## The Problem This Solves

{2-3 paragraphs. What goes wrong without this knowledge? 
Concrete failure scenario. Interview failure mode.}

## The Mental Model

{One paragraph. How to THINK about this concept. 
No jargon. Should be recitable in 90 seconds.}

## The Details

### {Sub-topic 1}
{Explanation + code examples}

### {Sub-topic 2}  
{Explanation + code examples}

{Continue for each atom/sub-topic in the unit}

## The Gotchas / Things That Bit Me

- {Gotcha 1 — explanation}
- {Gotcha 2 — explanation}
- {Gotcha 3 — explanation}

## Interview-Shaped Questions I Can Now Answer

1. **"Why does {concept} work this way?"**
   {Answer in 2-3 sentences, demonstrating understanding not just recall}

2. **"What happens when {edge case}?"**
   {Answer with concrete example}

{5-10 questions per unit}

## Code I Wrote

{Links to or inline code snippets of things the learner built during the session}

## Proof of Learning

{What the learner built/demonstrated to prove they reached State 3+}
```

### Notes Quality Checklist

Before finalizing any notes file, verify:

- [ ] Every section header has content (no empty sections)
- [ ] "Why this exists" is at the top
- [ ] Code examples exist for every concept
- [ ] Gotchas are specific, not generic
- [ ] Interview questions are "why" shaped, not "what" shaped
- [ ] The mental model paragraph can be recited in <90 seconds
- [ ] No jargon in the mental model section
- [ ] Code is broken-then-fixed (shows the wrong way first)

---

## PART 4 — HOW TO GENERATE REVIEW CARDS

### Card Format (for Anki or spreadsheet)

| Field | Content |
|-------|---------|
| Question | A "why" shaped question |
| Answer | 2-4 sentences explaining the WHY |
| Unit | Which unit this belongs to |
| Date Learned | When the learner studied this |
| Next Review | Day 1, Day 7, Day 30 schedule |

### Bad vs Good Questions

| Bad (recall) | Good (understanding) |
|--------------|---------------------|
| "What is a closure?" | "Why does `for (var i...)` with setTimeout print the same number, and what exactly changes with `let`?" |
| "What is hoisting?" | "Why does `console.log(x)` before `var x = 5` give `undefined` instead of a ReferenceError?" |
| "What is the event loop?" | "Why does `setTimeout(fn, 0)` execute AFTER all synchronous code, even though the delay is 0?" |
| "What is `this`?" | "Why does an arrow function NOT get its own `this`, and when is that a problem?" |

### Target: 10 review cards per unit minimum

---

## PART 5 — THE SESSION WORKFLOW

### For the Teaching AI (opencode)

1. **Before teaching an atom**: Ask the learner to predict what it is ("What do you think hoisting is?") — State 0.1 step 1
2. **Teach using the concept template** (Section 2 above)
3. **After each atom**: Pause and ask "Can you explain that back to me in your own words?"
4. **After the unit**: Assign the proof-of-learning build task
5. **After proof is done**: Trigger the Notes Agent

### For the Notes Agent

1. **Input**: Receive the conversation summary from the teaching session
2. **Process**: Extract concepts, code, gotchas, and interview questions
3. **Format**: Apply the notes template from Section 3
4. **Quality check**: Run the checklist from Section 3
5. **Output**: Write the .md file to the correct folder
6. **Update**: Mark atoms as complete in PROGRESS.md
7. **Generate**: Create 10+ review cards for the unit

---

## PART 6 — MODULE-SPECIFIC INSTRUCTIONS

### MODULE 1 — JavaScript

**Special focus areas:**
- Every concept should connect to React later (why this matters for a frontend engineer)
- Show the C# comparison where relevant (since learner knows C#)
- The execution model is the foundation — take extra time here
- Emphasize: "JS is single-threaded" as the root of async

**Key connections to make:**
- Hoisting → why React hooks must be called at top level
- Closures → stale closures in React (the #1 React bug)
- Event loop → why blocking the main thread freezes the UI
- Prototype chain → how React component inheritance works

### MODULE 2 — CSS/SCSS
- Start every concept with "this is what the browser does"
- Show the layout algorithm, not just the property

### MODULE 3 — C# + OOP
- Compare to JavaScript where relevant
- Focus on runtime behavior, not syntax
- GC and memory model are critical

### MODULE 5 — DSA
- Always state the pattern name
- Always state the complexity
- Always state the "when to use this" signal

### MODULE 6 — React
- Every concept ties back to the execution model (Module 1)
- Show the mental model first: "UI as a function of state"

---

## PART 7 — CONTENT GENERATION RULES

### Do's
- Use code examples liberally
- Show broken code → fixed code progression
- Connect to real interview questions
- Use the learner's existing knowledge (C#, React basics)
- Include "why this matters for interviews" context
- Reference other modules when relevant
- Keep mental model paragraphs under 90 seconds to recite

### Don'ts
- Never explain a concept without the "why" first
- Never use jargon in the mental model section
- Never skip the gotchas section
- Never write "what" questions — always "why" questions
- Never leave code unexplained
- Never assume knowledge that hasn't been taught yet
- Never skip the proof-of-learning assignment

### Tone
- Direct, like a senior engineer explaining to a junior
- No filler phrases ("It's important to note that...")
- Use "you" language
- Be honest about complexity ("This is tricky — here's why...")
- Use analogies from everyday life when helpful

---

## PART 8 — PROGRESS TRACKING

### PROGRESS.md Format

```markdown
## MODULE {n} — {Name}

### Unit {n}.{m} — {Unit Name}
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| {n}.{m}.{k} | {Topic} | Not Started/In Progress/Notes Generated/Review Complete | {filename} |
```

### Status Definitions
- **Not Started**: Atom not yet taught
- **In Progress**: Currently being taught in this session
- **Notes Generated**: Notes .md file exists and passes quality checklist
- **Review Complete**: Learner has done spaced repetition (day 7, day 30)

---

*This guide is the source of truth for content generation. All AI models producing learning content or notes for this syllabus must follow these instructions exactly.*
