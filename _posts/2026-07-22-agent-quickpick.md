---
layout: post
kind: theory
title: "The Hard Part Was Seven Markdown Files in a Folder."
subtitle: "Dev tools used to be things you adopted. They're becoming things you write, and the gap between wanting one and having it just collapsed to an evening."
date: 2026-07-22
tags:
  - "ai & tech"
---

[My Neovim config](https://github.com/dataguyofprocol/nvim-config) is 753 lines of Lua across 20 files and thirty-eight plugins. A function picks one of five colorschemes at random when I open the editor, because I couldn't decide. There's a keybinding that runs Conway's Game of Life on my buffer, and a plugin I wrote and published, [hexwitch]({% post_url 2025-12-07-i-shipped-a-neovim-plugin-in-lua %}), that turns a plain-English description into a whole colorscheme. None of it shipped with Vim. All of it is load-bearing. Nobody else could sit down at my machine and find anything.

For thirty years, doing this to your editor was a Vim thing. Practically a personality disorder with a plugin manager. You bent the tool to fit you, and everyone else adopted whatever came in the box. That split, the tinkerers and the adopters, was stable for my entire career.

It just ended. Not because more people found Vim. Because building the exact tool you want stopped being expensive.

There's a name for the tinkerer side, and it isn't mine. TJ DeVries, who works on Neovim itself, calls it a PDE. Personalized Development Environment. He coined it to make a point: Vim was never an IDE, it's a thing you bend until it fits one person, you, and only you. The term was built to describe the *opposite* of VS Code. Which is the whole joke, because VS Code is where this is happening now.

Three out of four developers use VS Code. 75.9% in last year's Stack Overflow survey, ninth year running at number one, and that undercounts it, because Cursor, Windsurf, and the whole wave of AI editors people are switching to are VS Code underneath, forks of the same open-source core. A hundred thousand extensions in the marketplace as of May. A hundred thousand ways people have already bent the default until it stops being anyone's default. The tinkerer instinct TJ was describing in a niche editor now sits under three-quarters of the profession. Most of them just don't know they're allowed to use it.

I found out I was allowed at work, building agents.

The project I spend my days on runs eight code-review agents on the same diff at once. Seven I wrote, an eighth hands off to CodeRabbit. Architecture, security, concurrency, database performance, each one a specialist reading the change in parallel, an orchestrator merging what they find and dropping the low-confidence noise so I'm not drowning. Here's the part worth staring at: the seven agents are seven markdown files in a folder. The hard part, the thing that sounds like a product, is text shaped like colleagues, and the CLI just reads it. Once you've seen that, you stop waiting for anyone to build it for you.

So the interesting question stopped being which tool to adopt. Look at what exists for running many agents at once: cmux, herdr, Conductor, the orchestration baked into Cursor and Windsurf. They're good, and they're all the same signal, the tools racing to hold your fleet of agents. I'm not betting against any of them. I'm saying I didn't have to pick one.

I wanted my agents living in the editor, in tabs, next to the code, not in a separate window I check like a build server. So one afternoon I [built that](https://github.com/dataguyofprocol/agent-quickpick). A keybinding, a picker, each agent opens in its own tab with its own icon and its own color, Claude and Aider and Codex side by side, the ones I run most floating to the top. It runs on Cursor and Windsurf too, because they're the same editor underneath. I didn't file an issue. I didn't wait for a roadmap. The distance from wanting it to having it was one evening.

![Two agents open as side-by-side editor tabs, Claude on the left and OpenCode on the right, each with its own icon and label.](/assets/images/agent-quickpick-terminals.png)

![Hitting the keybinding, picking an agent, and watching it open in its own tab.](/assets/images/agent-quickpick-demo.gif)

I should be honest about how far it goes, which is not very. Right now it launches agents and then forgets about them. The tab that would make it actually useful, one that shows every agent and what it's doing so you can watch the fleet without leaving the window where you'd fix what it broke, I haven't built yet. That's next. So take the confidence with the appropriate discount.

***

For most of software history, if you wanted your tools to work differently you had two moves: switch to something else someone built, or file a request and wait. Building it yourself was a real third option, and almost nobody took it, because it cost more than it was worth. That's the part that changed. The cost fell through the floor, and it took the whole build-versus-adopt calculation down with it.

The story here isn't which agent tool wins. It's that the gap between wanting a tool and having it collapsed to an evening, and most of us are still standing in the line we've always stood in.

The word came from the editor that refused to be an IDE. It turned out it was never really about the editor. It was about who gets to decide how your tools work. For thirty years that was a small club. The door's open now, and admission costs an afternoon.

*TJ DeVries coined "PDE" for the editor that isn't an IDE. The idea outgrew the editor.*
