---
up:
  - "[[Ideaverse Map]]"
related: []
created: 2022-05-11
modified: 2023-08-25
---
# Ideaverse Lite 1.5 - Release Notes
## Major Changes
- Added [[Home Basic]].
	- It's a simple and clean home note. It's the non-flashy, but highly functional alternative to [[Home]]. It's intentionally easy to edit, so we expect you to edit it to your personal tastes—just try to keep the formatting simple!
- Formally introducing **Folder x**.
	- *The "x" folder stands for "extras"*. It works incredibly well in Obsidian and in your computer's file folder system as well. 
	- It's a release valve, an easy way to tuck away those "extra" types of notes, such as "notes about notes" (meta notes, vault-related notes), utility notes, archived notes, and less immediately relevant "placeholder folders" that, while not overly important now, still serve you as a tucked away reminder of a topic or area of simmering or potential interest. 
	- Keen observers with notice that some folders have been shuffled around as a result.
- Installed the highly customized Soft Paper Theme.
    - This alternative to the default Prism theme will put you in a calmer and more reflective state of mind.
- Updated `Atlas` folder structures and organization
	- Renamed `Atlas/Notes` folder to `Atlas/Dots` folder
		- Renamed `Atlas/Dots/Ideas` folder to `Atlas/Dots/Things` folder
		- Created a new folder `Atlas/Dots/Statements` and moved all statements there
		- This is to reflect how [[Evergreen notes are things or statements about things]]
- **Metadata power shift** from tags ➡️ properties to organize notes and collections
	- Notes that had a `type` property for the subtype it was (ex. for sources notes there was `type: Book`) were instead converted into the `in` property and a link to the related note (ex. `[[Books]]`).
	- `#concept` tag replaced with `in` property to `[[Concepts]]`.
	- Notes with subtags like `#map/view` were replaced by the `in` property with links to both `[[Maps]]` and `[[Views]]`.
		- This was also the case for source notes like `#source/article`, which were turned into the links to notes `[[Sources]]` and `[[Articles]]`
		- For an example on this, you can visit [[The Almagest]]
	- Instead of Dataview queries using tags to search for notes, the new main filter criteria is through a note's `in` property.
- Quickly and powerfully find your most important notes by using the new [[Maps]] and [[Views]] collection notes
- Updated [[Ideaverse Map]]
	- Added mention of other folders beyond ACE in "How to customize your ACE headspace"
	- Added new callout under "Extra gifts" for acknowledging the intentional usage of styles in the Ideaverse
- Simplified the [[Library]] note's formatting.
	- By taking the text out of the callouts, we are encouraging you to actually edit the Library note to make it your own.
## Minor changes
- Removed `Excalibrain` community plugin due to unexpected behavior on initial load
- Embedded LYT YouTube videos into relevant notes for further learning
- Replaced all previous mentions of "Ideaverse for Obsidian" with "Ideaverse Lite" to avoid confusion with [[Ideaverse Pro]]
- Fixed unrequited notes callouts to still work even if the file name changes
## New Notes in this Version
```dataview
list
from ""
where contains(version, "1.5")
sort file.name
```
## Major Note Updates
```dataview
TABLE updates as "Updates"
FROM ""
WHERE updates
sort file.name
```


---

# Ideaverse Lite 1.0 - Release Notes
*Released 2023-08-30*
**Headlines**
- Introduced the [[Home]] note with ACE head spaces.
	- Provide multiple examples of 
	- Provided a basic ARC Framework (Add, Relate, Communicate) for developing ideas into outputs.
- Introduced the [[ACE Folder Framework]].
	- Provided ACE with multiple notes and examples.
- Introduced a working system for [[Efforts]] based on intensities. 
	- Provided "Efforts" with multiple examples.

**Details**
- 310 notes 
- Improved several data views to power up your navigating experience.
- Did general clean-up. 
- Changed the name of the kit from LYT Kit to Ideaverse Lite because Ideaverse evokes the connected, yet wide open nature of notes and ideas.
	- Further, this release is called Ideaverse Lite. But the name opens the door for other versions such as of Ideaverse for Organizations and Ideaverse for XYZ. So the name change allows the principles to naturally transcend the tool. 


---

# LYT Kit 7 - Release Notes
*Released 2022-09-13*

**Headlines**
- Vintage Home note
- 16 empowered maps in the Home note
- ACCESS folders streamlined to 10 folders
- Introducing "Efforts"

**Details**
- 286 notes 
- Vintage Home note. 
	- Remade the Home note to match the original version that brought me so much joy.
- 16 empowered maps in the Home note. Rebuilt every map for clarity and power.
	- Thinking MOC, Inbox, Notebox, Outbox, Daily Notes
	- Library, People MOC, Sources MOC, Concepts MOC
	- Efforts, Plan and Review
	- Health MOC, Finance MOC, Life Map, LYT Kit and Meta PKM
- Streamlined ACCESS folder structure for an easier start.
- Introduced "Efforts" as an alternative to "Projects".
	- Added the "Efforts" map to the Home note.
- Improved several data views to power up your navigating experience.
- Did general clean-up. 

---

# LYT Kit 6 - Release Notes
*Released 2022-05-11*

- 309 notes
- ACCESS folder structure
- Revised many of the notes for clarity
- Added Callouts explaining the broken links in some notes leading to parts of my personal PKM unavailable in Ideaverse Lite
- Recorded a series of e-mail lessons exploring some PKM fundamentals as well as working within the ACCESS folder structure to offer a bit more guidance in exploring this vault
- Added several new MOCs, indexes, and data views
- General clean-up