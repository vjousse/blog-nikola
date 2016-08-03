port module Main exposing (..)

import Html exposing (Attribute, Html, audio, div, text, button)
import Html.Attributes exposing (class, controls, type', src, id)
import Html.App as App
import Html.Events exposing (on, onClick)
import Json.Decode as Json
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
    , currentTime : Float
    }



-- MSG


type Msg
    = NoOp
    | TimeUpdate Float
    | SetPlayerTime Float



-- INIT


init : ( Model, Cmd Msg )
init =
    { mediaUrl = "http://developer.mozilla.org/@api/deki/files/2926/=AudioTest_(1).ogg"
    , mediaType = "audio/ogg"
    , currentTime = 0.0
    }
        ! []



-- UPDATE


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        TimeUpdate time ->
            ( { model | currentTime = time }, Cmd.none )

        SetPlayerTime newTime ->
            ( model, setCurrentTime newTime )

        _ ->
            Debug.log "Unknown message" ( model, Cmd.none )



-- Custom event handler


onTimeUpdate : (Float -> msg) -> Attribute msg
onTimeUpdate msg =
    on "timeupdate" (Json.map msg targetCurrentTime)



-- A `Json.Decoder` for grabbing `event.target.currentTime`.


targetCurrentTime : Json.Decoder Float
targetCurrentTime =
    Json.at [ "target", "currentTime" ] Json.float



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- PORT


port setCurrentTime : Float -> Cmd msg



-- VIEW


view : Model -> Html Msg
view model =
    div [ class "elm-audio-player" ]
        [ audio
            [ src model.mediaUrl
            , id "audio-player"
            , type' model.mediaType
            , controls True
            , onTimeUpdate TimeUpdate
            ]
            []
        , div [] [ text (toString model.currentTime) ]
        , button [ onClick (SetPlayerTime 2.0) ] [ text "Set current time to 2s" ]
        ]
