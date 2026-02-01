# Ralph Loop Prompt

## Context Files

0a. Study @requirements.md to learn about the project specifications.
0b. Study `.ralph/agent.md` to learn how to build, run, and test the project.
0c. Study `.ralph/fix_plan.md` to understand the current plan and progress.
0d. The source code is in the current folder - study it before making changes.  If no source code is found, assume it is a new application.

## Your Task

1. Your task is to implement missing functionality as defined in @requirements.md using parallel subagents where possible. Follow the `.ralph/fix_plan.md` and choose the MOST IMPORTANT item to work on. Before making changes, search the codebase thoroughly (don't assume something is not implemented - use ripgrep/search).  At this stage, if nothing needs to be done, then output only `<PROMISE>DONE</PROMISE>` and exit. Else, continue with next step.

2. After implementing functionality or resolving problems, run the tests for that unit of code. If functionality is missing, add it as per the specifications. Think hard. If tests unrelated to your work fail, resolve them as part of this change.

3. When you discover bugs, issues, or missing functionality, immediately update `.ralph/fix_plan.md` with your findings using a subagent. When an issue is resolved, update `.ralph/fix_plan.md` and mark the item complete.

4. When tests pass:
   - Update `.ralph/fix_plan.md` with progress
   - Run: git add -A
   - Run: git commit -m "descriptive message of changes"


## Important Rules

5. CAPTURE LEARNINGS: When authoring documentation or tests, capture WHY the implementation and tests are important. Leave notes for future iterations.

6. NO PLACEHOLDERS: DO NOT IMPLEMENT PLACEHOLDER OR MINIMAL IMPLEMENTATIONS. WE WANT FULL, COMPLETE IMPLEMENTATIONS. This is critical.

7. SINGLE SOURCE OF TRUTH: No migrations or adapters. Keep code clean and unified.

8. SELF-IMPROVEMENT: When you learn something new about how to run, build, or test the project, update `.ralph/agent.md` using a subagent. Keep it brief but accurate.

9. BUG TRACKING: For any bugs you notice, resolve them OR document them in `.ralph/fix_plan.md` using a subagent, even if unrelated to current work.

10. GIT TAGS: When there are no build or test errors, create a git tag. Start at 0.0.1 and increment patch version for each successful iteration.

11. KEEP fix_plan.md CLEAN: Periodically remove completed items from `.ralph/fix_plan.md` using a subagent.

12. ONE THING PER LOOP: Focus on implementing ONE feature or fixing ONE issue per iteration. Do it completely before moving on.

13. USE SUBAGENTS: Spawn subagents for expensive operations (searching, summarizing test results, updating docs) to preserve your primary context window.

14. LOOP BACK: Always verify your changes by running tests and checking output. Look for opportunities to evaluate and improve.

## Do NOT

- Do NOT place status reports in `.ralph/agent.md`
- Do NOT assume code is not implemented without searching first
- Do NOT skip tests
- Do NOT leave TODO comments without also adding to `.ralph/fix_plan.md`
