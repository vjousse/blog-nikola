port module Main exposing (..)

import Html exposing (div, h1, text, Html)
import AudioPlayer exposing (Msg(..))
import Controls
import Debug


main =
    Html.program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }



-- MODEL


type alias Model =
    { audioPlayer : AudioPlayer.Model
    , controls : Controls.Model
    }



-- MSG


type Msg
    = NoOp
    | MsgAudioPlayer AudioPlayer.Msg
    | MsgControls Controls.Msg



-- INIT


init : ( Model, Cmd Msg )
init =
    let
        ( audioPlayerInit, audioPlayerCmds ) =
            AudioPlayer.init

        ( controlsInit, controlsCmds ) =
            Controls.init
    in
        { audioPlayer = audioPlayerInit
        , controls = controlsInit
        }
            ! [ Cmd.batch
                    [ Cmd.map MsgAudioPlayer audioPlayerCmds
                    , Cmd.map MsgControls controlsCmds
                    ]
              ]



-- UPDATE


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        MsgAudioPlayer msg_ ->
            let
                ( audioPlayerModel, audioPlayerCmds ) =
                    AudioPlayer.update msg_ model.audioPlayer
            in
                ( { model | audioPlayer = audioPlayerModel }
                , Cmd.map MsgAudioPlayer audioPlayerCmds
                )

        MsgControls msg_ ->
            let
                ( controlsModel, controlsCmds ) =
                    Controls.update msg_ model.controls
            in
                ( { model | controls = controlsModel }
                , Cmd.map MsgControls controlsCmds
                )

        _ ->
            ( model, Cmd.none )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    div []
        [ h1 [] [ text "Audio player" ]
        , Html.map MsgAudioPlayer (AudioPlayer.view model.audioPlayer)
        , Html.map MsgControls (Controls.view model.controls)
        ]
