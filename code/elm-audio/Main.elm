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
