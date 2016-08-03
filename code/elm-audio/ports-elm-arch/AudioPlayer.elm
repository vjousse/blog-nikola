module AudioPlayer exposing (Model, Msg(..), init, update, view, subscriptions)

import Html exposing (audio, button, div, h2, text, Attribute, Html)
import Html.Attributes exposing (class, controls, id, type', src)
import Html.Events exposing (on, onClick)
import Json.Decode as Json exposing ((:=))
import Debug
import Ports


-- MODEL


type alias Model =
    { mediaUrl : String
    , mediaType : String
    , playing : Bool
    , currentTime : Float
    , controls : Bool
    }



-- MSG


type Msg
    = NoOp
    | TimeUpdate Float
    | Playing
    | Paused



-- INIT


init : ( Model, Cmd Msg )
init =
    { mediaUrl = "http://localhost/lcp_q_gov.mp3"
    , mediaType = "audio/mp3"
    , playing = False
    , currentTime = 0
    , controls = True
    }
        ! []



-- UPDATE


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case Debug.log (toString model) msg of
        TimeUpdate time ->
            ( { model | currentTime = Debug.log (toString time) time }, Cmd.none )

        Playing ->
            ( { model | playing = True }, Cmd.none )

        Paused ->
            ( { model | playing = False }, Cmd.none )

        _ ->
            Debug.log "test " ( model, Cmd.none )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- JSON decoders


onPause : msg -> Attribute msg
onPause msg =
    on "pause" (Json.succeed msg)


onPlaying : msg -> Attribute msg
onPlaying msg =
    on "playing" (Json.succeed msg)


onTimeUpdate : (Float -> msg) -> Attribute msg
onTimeUpdate msg =
    on "timeupdate" (Json.map msg targetCurrentTime)


{-| A `Json.Decoder` for grabbing `event.target.currentTime`. We use this to define
`onInput` as follows:

    import Json.Decoder as Json

    onInput : (String -> msg) -> Attribute msg
    onInput tagger =
      on "input" (Json.map tagger targetValue)

You probably will never need this, but hopefully it gives some insights into
how to make custom event handlers.
-}
targetCurrentTime : Json.Decoder Float
targetCurrentTime =
    Debug.log "in targetCurrentTime" Json.at [ "target", "currentTime" ] Json.float



-- VIEW


view : Model -> Html Msg
view model =
    div []
        [ div [ class "elm-audio-player" ]
            [ audio
                [ src model.mediaUrl
                , type' model.mediaType
                , controls model.controls
                , onTimeUpdate TimeUpdate
                , onPause Paused
                , onPlaying Playing
                , id "audio-player"
                ]
                []
            , div [] [ text ("Current time inside audio component: " ++ toString model.currentTime) ]
            ]
        ]
