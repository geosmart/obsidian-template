---
up:
  - "[[Efforts]]"
created: 2020-01-01
rank: "4"
in: 
- "[[Maps]]"
---
This note is a simple example of how you can consolidate all of your notes related to an effort into a single spot.

> [!Watch]+ ###### Videos on Deck
> This filters for `#output/youtube◻️` with a rank above `3`.
> 
> ```dataview
> TABLE WITHOUT ID
>  file.link as "",
>  rank as "Rank"
> 
> FROM #output/youtube◻️ 
> 
> WHERE rank > 3
> 
> SORT rank desc
> ```

> [!Video]+ ###### Published Youtube Videos
> ```dataview
> TABLE WITHOUT ID
>  file.link as "",
>  created as "Published"
>  
> FROM #output/youtube☑️  and -#x/readme
> 
> SORT created desc
>  ```

---

See the [[Communicate]] note for a broader view of both videos and newsletters.

