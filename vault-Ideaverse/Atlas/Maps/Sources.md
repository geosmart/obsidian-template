---
up:
  - "[[Home]]"
created: 2020-06-01
in:
  - "[[Maps]]"
aliases:
  - Sources Map
---
This is where I keep tabs on some of the sources I have encountered. 
What "sources" should you track? 
How about books and movies?

> [!Book]- ### Books
> ```dataview
> TABLE WITHOUT ID
>  year as "Year",
>  file.link as Book
> 
> WHERE
> 	contains(in,link("Books")) and
> 	!contains(file.name, "Template")
> 
> SORT year asc
> ```

> [!video]- ### Movies
> ```dataview
> TABLE WITHOUT ID
>  year as "Year",
>  file.link as Movie
>  
> FROM -#x/readme
> 
> WHERE
> 	contains(in,link("Movies")) and
> 	!contains(file.name, "Template")
> 
> SORT year asc
> ```

I am playing around with a property field called `in`. It allows me a nice way to create a few passive maps for different types of sources into different collections. Here's what I have so far, feel free to make more:

- [[Books]] | [[Games]] | [[Movies]] | [[Papers]] | [[Songs]] | [[Speeches]]

> [!Script]- ## ALL SOURCES
> This is a simple data view pulling anything from the **Sources** folder.
> 
> ```dataview
> TABLE WITHOUT ID
>  year as "Year",
>  join(in) as Type,
>  file.link as Source
>  
> FROM -#x/readme 
> WHERE
> 	contains(in,link("Sources")) and
> 	!contains(file.name, "Template")
> 
> SORT year asc
> ```

Not included here, but in my personal vault, I enjoy checking out the comprehensive [[Source MOC]] and perusing my [[Bookshelf 📚]]. And to honor the old ones, I also keep a [[Commonplace Book]] based on tags.

> [!NOTE]+ This is a sanitized version of my actual note. 
> - Content and links have been removed.








