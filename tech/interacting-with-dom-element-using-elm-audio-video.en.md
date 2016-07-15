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

## Preamble

The goal of the [@elm-lang organization](https://github.com/elm-lang) is to cover the entire [webplatform](https://platform.html5.org/) as described in [this blog post](http://elm-lang.org/blog/farewell-to-frp#what-is-next-). But in the meantine, how should we interact with basic elements such as the Audio element?  
We could do everything using [JS ports](http://guide.elm-lang.org/interop/javascript.html). But as we want to stay in the Elm world as much as we can, we will _read_ the values of the element using __DOM events__ inside Elm. Unfortunately, for _writing/mutating_ values (calling functions and/or updating a DOM element property) we have no choice but using __JavaScript port interop__.

_Note_: Another alternative would be writing [Native modules](https://github.com/elm-lang/core/tree/master/src/Native) to wrap the missing parts into some Elm greatness. But as doing so should be avoided (Native is subject to change and is not documented), this will not be covered here.

# Basic example

For this tutorial, we ar using Elm `0.17`.

## Reading element values: DOM events

We will take the [`<audio />` tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio) as an example for this blog post, but keep in mind that the techniques described here apply to every DOM element.

### App skeleton

Let's start with a minimal Elm program:

`Main.elm`
```Elm
module Main exposing (..)

import Html exposing (Attribute, Html, audio, div, text)
import Html.Attributes exposing (class, controls, type', src)
import Html.App as App
import Debug

main =
    App.program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }

-- MODEL

type alias Model =
    { mediaUrl : String
    , mediaType : String
    }

-- MSG

type Msg
    = NoOp

-- INIT

init : ( Model, Cmd Msg )
init =
    { mediaUrl = "http://developer.mozilla.org/@api/deki/files/2926/=AudioTest_(1).ogg"
    , mediaType = "audio/ogg"
    }
        ! []

-- UPDATE

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        _ ->
            Debug.log "Unknown message" ( model, Cmd.none )

-- SUBSCRIPTIONS

subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none

-- VIEW

view : Model -> Html Msg
view model =
    div [ class "elm-audio-player" ]
        [ audio
            [ src model.mediaUrl
            , type' model.mediaType
            , controls True
            ]
            []
        ]
```

Compile it using:

    elm make Main.elm

Open the generated `index.html` in your browser. You should see the default audio player of your browser showing up.

### Reading the currentTime property

Let's say that we want to display the `currentTime` property of the audio element just below it. Let's add it to the model as a `Float`:

```Elm
type alias Model =
    { mediaUrl : String
    , mediaType : String
    , currentTime : Float
    }
```

We could as well use a `Maybe Float` here (and we certainly should). It would allow us to differenciate between _no value_ and the value _0_. But let's keep that for later.

Then init the currentTime to `0`:

```Elm
init =
    { mediaUrl = "http://developer.mozilla.org/@api/deki/files/2926/=AudioTest_(1).ogg"
    , mediaType = "audio/ogg"
    , currentTime = 0.0
    }
        ! []
```

And display it in the view:

```Elm

view : Model -> Html Msg
view model =
    div [ class "elm-audio-player" ]
        [ audio
            [ src model.mediaUrl
            , type' model.mediaType
            , controls True
            ]
            []
        , div [] [ text (toString model.currentTime) ]
        ]
```

Compile your program and you should see a `0` displayed below the audio player. That's cool, but how should we do to update it? By writing a [__custom event handler__](http://package.elm-lang.org/packages/elm-lang/html/1.1.0/Html-Events#custom-event-handlers).

Everytime the `timeupdate` event of the `audio` tag will be triggered, we will catch it and read the value of the `currentTime` attribute. The magic trick here is that every event contains the DOM element that triggered the event as the `target` attribute.

Start by importing the needed module:

```Elm
import Html.Events exposing (on)
```

Create a new message type that will be triggered at each timeupdate:

```Elm
-- MSG

type Msg
    = NoOp
    | TimeUpdate Float
```

Update the model when such a message is received:

```Elm
-- UPDATE

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        TimeUpdate time ->
            ( { model | currentTime = time }, Cmd.none )

        _ ->
            Debug.log "Unknown message" ( model, Cmd.none )
```

Then add the custom event handler and the JSON decoder below your update function:

```Elm
-- Custom event handler

onTimeUpdate : (Float -> msg) -> Attribute msg
onTimeUpdate msg =
    on "timeupdate" (Json.map msg targetCurrentTime)

-- A `Json.Decoder` for grabbing `event.target.currentTime`.


targetCurrentTime : Json.Decoder Float
targetCurrentTime =
    Json.at [ "target", "currentTime" ] Json.float

```

Here we write a custom event handler called `onTimeUpdate` using the [`on` function of the `Html.Events` module](http://package.elm-lang.org/packages/elm-lang/html/1.1.0/Html-Events#custom-event-handlers).

This custom event handler uses the Json decoder `targetCurrentTime` to read a `Float` value from the event located at `target.currentTime`.

Finally, make use of this new event handler in your `view`:

```Elm
-- VIEW


view : Model -> Html Msg
view model =
    div [ class "elm-audio-player" ]
        [ audio
            [ src model.mediaUrl
            , type' model.mediaType
            , controls True
            , onTimeUpdate TimeUpdate
            ]
            []
        , div [] [ text (toString model.currentTime) ]
        ]
```

Now, compile your file and you should see the `currentTime` value update when you play the file.

## Calling functions : Javascript ports

# Advanced example: components

# Wrapping Up

Citing @debois medium post about DOM manipulation
