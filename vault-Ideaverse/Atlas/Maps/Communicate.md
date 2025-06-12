---
up:
  - "[[Home]]"
related:
  - "[[Add]]"
  - "[[Relate]]"
created: 2022-01-01
in: 
- "[[Views]]"
---
This **Communicate** notes is a place to track your various *outputs*.

Below are simple examples using the tag `output` to track my, well, outputs. 

This is enough to get you started. Over time, you might to customize your views.

> [!Script]- ###### Newsletters
> ```dataview
> TABLE WITHOUT ID
>  file.link as "",
>  created as "Published"
>  
> FROM #output/newsletter and -#x/readme
> 
> SORT created desc
>  ```

# Videos

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


> [!Video]- ###### Published Youtube Videos
> ```dataview
> TABLE WITHOUT ID
>  file.link as "",
>  created as "Published"
>  
> FROM #output/youtube☑️  and -#x/readme
> 
> SORT created desc
>  ```


