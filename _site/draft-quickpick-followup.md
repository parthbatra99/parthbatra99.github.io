At 23:32 on August 31 I pushed a commit that added 2,643 lines to a project I cannot read.

36 files. A new agent I have never opened, an old one removed, a hook schema bumped to v4, eight hundred lines of tests I will never run by hand. The message says `feat: v0.10.0: add antigravity and codex support` in the steady voice of a release engineer who does not exist. The AI wrote it. Then I clicked publish like a user.

That is the whole job now.

## the appropriate discount

On July 22 I wrote that building the exact tool you want had collapsed to an evening. The example was Agent Quickpick, a keybinding and a picker that opened each agent in its own tab with its own color. At the end I hedged. It launched agents and then forgot about them. The tab that would make it actually useful, a place to watch the fleet, I had not built yet. I told you to take the confidence with the appropriate discount.

The discount has cleared.

Since then there have been 47 commits. The version went from 0.1 to 0.10.0 in five weeks, on maybe fourteen days I touched it. The thing I said I had not built now exists in three forms: a live status bar per repo, a sessions picker you get by double tapping the same keybinding within 250ms, and native OS notifications that find you when VS Code is behind another app. There are 412 tests across 20 files. There is a bundled universal binary inside a VS Code extension because macOS only respects bundle icons. A single evening became a small product, and I am still the maintainer who cannot read it.

[FIGURE: 47 commits from July 20 to August 31 as a compressed timeline, dense clusters on seven dates, with callouts for the notification fix cluster and the final antigravity commit, caption in lowercase italic: *the evening that kept going*]

## my colleagues broke the notifications

No one from the 2.9k strangers on OpenVSX has filed an issue or a PR. The entire feedback channel for a tool with [PLACEHOLDER: download count on publish day, 2.9k as of Aug 31] installs has been people I sit next to.

They said two things. Notifications were unstable. And could it support Antigravity, because Antigravity has generous free limits and they use it for personal projects.

The most frugal reason imaginable. That is why the most sophisticated code in the repo is the Antigravity adapter, the one that knows the difference between `terminationReason: "error"` meaning crashed and `fullyIdle: false` meaning still working and a PreToolUse on `ask_permission` meaning blocked and waiting for approval. I did not specify any of that. I use Antigravity myself. I asked its EI to research on the internet and implement it, then tested it as a QA user. I do not know the exact details of it, to be honest. That sentence is, as far as I can tell, still the most accurate description of my job.

Notifications are where the month went. Between 0.9.0 and 0.9.2 there are three releases in five days about banner clicks. One tried `-sender` with `-open` and the click did nothing. The next tried `-execute` to keep the icon and make clicks work. The third dropped `-sender` so clicks would reliably reach the handler. In there the extension started shipping its own `terminal-notifier` as a universal binary, x86_64 plus arm64, because Notification Center shows the icon of the sending bundle and offers no override. Without it a fresh Mac credits the banner to Script Editor. I learned this without reading a line of the code.

If you ask for the biggest debugging story of the last month, I do not have one. The commits do. I think there were plenty. I do not remember any of them. The fuzz suite remembers for me. There is a test called `install → remove === strip-only, for random configs (fixed seed)` and another that says `user hooks always survive install + remove`. The suite is a bill of rights for `~/.claude/settings.json`. It exists because an earlier round trip could delete a user's empty hook array even though it never held one of ours. I did not ask for fuzz tests by name. The AI did, after it nearly ate someone's config.

## the repo learned how to raise itself

Earlier this month I asked Claude Code to deep research whatever I would need to make development as autonomous as possible. Not a feature. The autonomy itself. One item it brought back was a skill for open sourcing.

I copied it from the Trail of Bits plugins repo on GitHub. 224 lines, plus reference files and a script that runs gitleaks over your history before you flip a repo public, because history rewriting does not reach forks. It now lives in `.agent/skills/open-sourcing/` inside a repo whose code the owner cannot read.

Running it is how `CONTRIBUTING.md` and `SECURITY.md` and `CODE_OF_CONDUCT.md` appeared. How `.editorconfig` and `dependabot.yml` appeared. The repo now contains a manual, written for agents, about how to be a responsible maintainer. The agents read it. I move the files where they tell me.

The division of labor that made this sustainable was not planned. I have used Neovim for three years. My config is 753 lines of Lua across 20 files. I know some Lua because Neovim held me hostage long enough. When I shipped hexwitch in Lua I could at least half read what I shipped. This time the agents were writing TypeScript so clean that even third party review agents from different harnesses were not picking many errors. So I made a call. I would focus on the logic, the maintainability, the QA part, and let the AI handle the coding part.

In practice I own the decisions and the clicking. Which agents to add, which to remove when Gemini moved to Antigravity, whether to ship notifications on by default, whether one keybinding with a double tap is better than two bindings. My QA is I open the picker, launch Claude, make it ask a permission, and see if the banner says "Claude wants to run a command, approve?" and clicking it jumps to the right tab. If it does, I ship.

***

For most of software history the expensive part was not writing code. It was keeping it alive while people used it, then proving you had not broken anything, then proving you were safe to depend on. Each of those is a prompt now. The Trail of Bits checklist is copy pasteable. The fuzz suite is generatable. The binary is downloadable. This week I will publish the extension to the VS Code Marketplace at [PLACEHOLDER: marketplace link] and Microsoft will show it next to a hundred thousand others. The admission ticket used to be proof you had earned it. Now it is the next prompt.

The one line that did not get cheaper is `"publisher": "dataguyofprocol"` in package.json. Everything else I can generate or copy or have an agent research. That line still points at me. Two thousand nine hundred strangers and the colleagues at the next desk run code I cannot read, and when the hook that writes into `~/.claude/settings.json` misfires, that truncated write the changelog warns will break every agent session and not just mine, the notification will not say the AI did it. It will say I did. I am confident enough to ship to the Marketplace this week, and that confidence is a new shape. It is trust in the loop, not understanding of the internals. It is boarding a plane without auditing the engine. As far as I can tell the loop is sound. The flight is usually uneventful. I have not earned the right to say I know which kind of flight this is yet. Ask me in a year.
