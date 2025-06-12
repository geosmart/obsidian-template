---
up: 
related: 
created: 2024-09-02
version:
  - "1.5"
---

"Views" are maps whose main purpose is ***to show auto-updating, dynamic results of custom searches.*** 


> [!map]+ # Views
> This note collects all notes where the `in` property says `Views`. 
> 
> ```dataview
> TABLE WITHOUT ID
> 	file.link as View
> WHERE
> 	contains(in,this.file.link) and
> 	!contains(file.name, "Template")
> SORT file.name asc
> LIMIT 222
> ```
