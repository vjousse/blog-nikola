<!-- 
.. title: Interacting with a DOM element using Elm (audio/video tag example)
.. slug: interacting-with-dom-element-using-elm-audio-video
.. date: 2016-07-07 12:38:20 UTC+02:00
.. tags: elm
.. category: 
.. link: 
.. description: 
.. type: text
-->

So, you want to write some [Elm](http://elm-lang.org/) code because you're a Hipster and want to be _in_. Fair enough. But being a Hipster has some downsides too. You soon realize that, even if __Elm__ is cool, it's still in development and doesn't provide all the things you may need. For example, how can you __interact with the HTML Audio element or any element not yet covered by the Elm core modules__? Don't worry, uncle Vince is here.

<!-- TEASER_END -->

# Preamble

The goal of the [@elm-lang organization](https://github.com/elm-lang) is to cover the entire [webplatform](https://platform.html5.org/) as described in [this blog post](http://elm-lang.org/blog/farewell-to-frp#what-is-next-). But in the meantine, how should we interact with basic elements such as the Audio element?  
We could do everything using [JS ports](http://guide.elm-lang.org/interop/javascript.html). But as we want to stay in the Elm world as much as we can, we will _read_ the values of the element using __DOM events__ inside Elm. Unfortunately, for _writing_ values (calling functions and/or updating an element property) we have no choice but using __JavaScript port interop__.

_Note_: Another alternative would be writing [Native modules](https://github.com/elm-lang/core/tree/master/src/Native) to wrap the missing parts into some Elm greatness. But as doing so should be avoided (Native is subject to change and is not documented), this will not be covered here.

## Reading element values: DOM events


## Calling functions : Javascript ports
