---
up:
  - "[[Calendar]]"
created: 2023-08-21
---
What's your time-style? I'm a more of a "monthly note" kind of person, but many people love their Daily Note workflow. I will still randomly capture sparks in a daily note, but I like to work from a monthly note.

In the [LYT Workshop](https://www.linkingyourthinking.com/), we go over:

- The "Daily Spark to Weekly Arc" workflow for Gardeners
- The "Monthly Map" workflow for Architects

But for now, you can just play around on your own to figure out what might work for you:

- Open today's note by hitting `Cmd-d` (or `Ctrl-d` on Windows).
- Open this week's note by hitting `Cmd-shift-d` (or `Ctrl-shift-d` on Windows).
- Open this month's note by hitting `Cmd-shift-m` (or `Ctrl-shift-m` on Windows).

A daily note practice is great for many people. Try it out. Just never feel obligated to make a daily note every day. But do use them. Sometimes I log things like meetings, stuff I've watched, and notable workouts. Daily notes are great for a mixture of uses, such as: 

- planning your day
- jotting down ideas
- taking meeting notes
- reflecting on your day

Here's an example of a simple view that just searches your `Calendar` folder.

> [!Calendar]+ ## Daily Notes
> While I prefer to click on the Calendar tab (in one of the side tabs), below is a simple view of the `20` latest daily notes—including a few from the future:
> 
> ```dataview
> LIST
> FROM "Calendar" and -#x/readme 
> SORT file.name desc
> LIMIT 20
> ```
