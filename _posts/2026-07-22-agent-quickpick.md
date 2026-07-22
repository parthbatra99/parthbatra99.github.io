---
layout: post
kind: theory
title: "My Editor Runs Conway's Game of Life. Last Week I Taught It to Run Eight Agents."
subtitle: "The word for bending your editor to fit you came from Neovim. It describes most of the profession now, and nobody says it out loud."
date: 2026-07-22
tags:
  - "ai & tech"
---

My Neovim config is 753 lines of Lua across 20 files and thirty-eight plugins. A function picks one of five colorschemes at random when I open the editor, because I couldn't decide. There's a keybinding that runs Conway's Game of Life on my buffer, and a plugin I wrote and published, hexwitch, that does exactly one thing: flip a value between hex and text. None of it shipped with Vim. All of it is load-bearing. Nobody else could sit down at my machine and find anything.

There's a name for this, and it isn't mine. TJ DeVries, who works on Neovim itself, calls it a PDE. Personalized Development Environment. He coined it to make a point: Vim was never an IDE, it's a thing you bend until it fits one person, you, and only you. The term was invented to describe the opposite of VS Code.

Which is why what's happening now is funny. The IDE is becoming a PDE.

Three out of four developers use VS Code. 75.9% in last year's Stack Overflow survey, ninth year running at number one. And that number undercounts it, because Cursor, Windsurf, the whole wave of AI editors people are switching to, are VS Code underneath, forks of the same open-source core. The extension I wrote runs on all of them without a change, because it's one chassis wearing different logos. The marketplace crossed a hundred thousand extensions in May: a hundred thousand ways to bend the default until it stops being anyone's default. The impulse TJ was describing in a niche editor is now the daily behavior of most of the profession. They just don't call it anything.

I caught myself doing it at work, and the thing I bent it around was agents.

The project I spend my days on has eight code-review agents that run on the same diff at the same time. Seven I wrote, an eighth hands off to CodeRabbit. Architecture, security, concurrency, database performance, each one a specialist reading the change in parallel, and an orchestrator that merges what they find and drops the low-confidence noise so I'm not drowning. I didn't install this. The seven agents are seven markdown files in a folder. The intelligence isn't software, it's text shaped like colleagues, and the CLI reads it.

Running many agents at once is the actual new thing here. And the way everyone is building for it is the part I find strange.

Open a new tab and look around. cmux. herdr. Conductor. Superset. Warp. Five tools, one impulse: run a fleet of coding agents and watch them work. They're good tools. They also all live outside the editor. Terminals, desktop apps, dashboards. You check on them the way you check on a build server, which is another way of saying you left the window where your code is to go somewhere else and mind your machines.

I didn't want to leave. So one afternoon I added it to the editor instead. A keybinding, a picker, and each agent opens in its own tab with its own icon and its own color, Claude and Aider and Codex side by side, the ones I run most floating to the top. It took under ninety minutes, and the reason it took under ninety minutes is the whole point. VS Code hands you an API for tabs, an API for commands, an API for theming, and you bolt your own taste onto it. It's the same loop TJ was describing, except the chassis now has three-quarters of the world's developers sitting on it.

![Two agents open as side-by-side editor tabs, Claude on the left and OpenCode on the right, each with its own icon and label.](/assets/images/agent-quickpick-terminals.png)

![Hitting the keybinding, picking an agent, and watching it open in its own tab.](/assets/images/agent-quickpick-demo.gif)

I should be honest about how far it goes, which is not very. Right now it launches agents and then forgets about them. The part that would make it genuinely useful, a tab that shows every agent and what it's doing so you can watch the fleet without leaving the window where you'd fix what it broke, I haven't built yet. That's next. So take the confidence with the appropriate discount.

***

Maybe the dashboards win. Maybe we all migrate to some new app the way we all migrated to VS Code, and this whole idea ages badly. But I don't think people move to new surfaces. They make the surface they're already on more like the one they wish they had. That's the entire history of Vim, it's why a hundred thousand extensions exist, and it's what three-quarters of us are quietly doing without a word for it.

The word came from the editor that refused to be an IDE. The joke is that the IDE is turning into one anyway.

*TJ DeVries coined "PDE" for Neovim, the editor that isn't an IDE. Nobody warned VS Code.*
