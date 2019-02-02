# Neural Note

Organize "streams of consciousness" types of writing (e.g. when brainstorming) into a progression of distinct ideas. Make it easy to pick up on an earlier thought without losing momentum on the current one.

## Progress
* Sentences are parsed for entities using POS (part of speech) list by series of POS and individual acceptable POS terms "food" and "breakfast food" are entities.
* As of 7AM Saturday, we have an algorithm to evaluate the similarity between nouns without context, which we expect to be the main predictors to the current thread of thought. Our first test will be to see how well we can cluster sentences based on the nouns within them to other sentences. This will be tested on Reddit comments by seeing if the grouped sentences correspond to the same branches in the comment tree. Here, we're modelling trains of thought as paths along the branches of the comment tree, since replies tend to relate to their parents.

## Alex Todo

It seems that the main UI challenge will be to relate the sentences as the user wrote them to the organization that we will create. Broadly, a promising approach seems to be  organizing the content as concepts under an idea. I think that ideally, as the user types or dictates to the system, the UI begins to populate suggestions of relationships to previous parts of the text. We're mulling over another view of the hierarchy of ideas as a visual hierarchy will be. This might be a nice visual for demo.

We were thinking to base the way that we cluster "concepts" and the size of a "concept" (ranging from a sentence fragment to a paragraph say) on the most intuitive way we can come up with for a user to see the relationships. On Saturday, could you:

1. create a way to show relationships between sentence-ish bits of text between each other. We're going with some rough numbers that could be, say, up to ~10 ideas for a whole document, and ~3 concepts of an idea that aren't in the same place.
2. create a view clumping concepts under the same idea that preserves the initial ordering in the text, to show progression. Depending on how flexible this is, it might open or close the door on some block of sentence[s] tying to more than one idea. That's definitely a stretch goal.
3. create a workflow to add to existing ideas in both the raw text view and the hierarchical view. A design stretch goal is to ask whether there's a design that would allow the user to start writing or talking about a separate idea as they're appending, and for the UI to suggest splitting off into a new idea in an unintrusive way.