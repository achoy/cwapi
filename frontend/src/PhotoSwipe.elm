module PhotoSwipe exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)
import Http
import Json.Decode exposing (string, int, list, Decoder)
import Json.Decode.Pipeline exposing (decode, required, optional)

type alias PsPhoto =
  { pkey : String
   , fname : String
   , w : Int
   , h : Int
   , size : Int
   , title : String }


type alias PsOptions =
  { history : Bool
  , focus : Bool
  , showAnimationDuration : Int
  , hideAnimationDuration : Int }

type alias Model =
  { photos : List PsPhoto
   , options : PsOptions
   , loadingError : Maybe String }

type Msg
  = LoadPhotos (Result Http.Error (List PsPhoto))

psOptions : PsOptions
psOptions = { history = False
  , focus = False
  , showAnimationDuration = 0
  , hideAnimationDuration = 0 }

initialModel : Model
initialModel =
  { photos = []
  , options = psOptions
  , loadingError = Nothing }

psview : Model -> Html Msg
psview model =
  div [ class "content " ]
      [ h1 [] [ text "Photo Groove 2.0 for Albert "]
      , button
        [ onClick PhotoSwipe ]
        [ text "PhotoSwipe Slideshow"]
      ]
      [ class "pswp", attribute "aria-hidden" "true",  attribute "role" "dialog", attribute "tabindex" "-1" ]
      [ div [ class "pswp__bg" ] []
        , div [ class "pswp__scroll-wrap" ]
          [ div [ class "pswp__container" ]
            [ div [ class "pswp__item" ] []
            , div [ class "pswp__item" ] []
            , div [ class "pswp__item" ] []
            ]
        , div [ class "pswp__ui pswp__ui--hidden" ]
            [ div [ class "pswp__top-bar" ]
                [ div [ class "pswp__counter" ] []
                , button [ class "pswp__button pswp__button--close", title "Close (Esc)" ] []
                , button [ class "pswp__button pswp__button--share", title "Share" ] []
                , button [ class "pswp__button pswp__button--fs", title "Toggle fullscreen" ] []
                , button [ class "pswp__button pswp__button--zoom", title "Zoom in/out" ] []
                , div [ class "pswp__preloader" ]
                    [ div [ class "pswp__preloader__icn" ]
                        [ div [ class "pswp__preloader__cut" ]
                            [ div [ class "pswp__preloader__donut" ] [] ]
                        ]
                    ]
                ]
            , div [ class "pswp__share-modal pswp__share-modal--hidden pswp__single-tap" ]
                [ div [ class "pswp__share-tooltip" ] [] ]
            , button [ class "pswp__button pswp__button--arrow--left", title "Previous (arrow left)" ] []
            , button [ class "pswp__button pswp__button--arrow--right", title "Next (arrow right)" ] []
            , div [ class "pswp__caption" ]
                [ div [ class "pswp__caption__center" ] [] ]
            ]
          ]
        ]

urlPrefix : String
urlPrefix =
  "http://tardis.choycreative.com/photos"

photoDecoder : Decoder PsPhoto
photoDecoder =
  decode PsPhoto
    |> required "pkey" string
    |> required "fname" string
    |> required "w" int
    |> required "h" int
    |> required "size" int
    |> required "title" string

initialCmd : Cmd Msg
initialCmd =
  list photoDecoder
    |> Http.get (urlPrefix ++ "/list.json")
    |> Http.send LoadPhotos

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of

    LoadPhotos (Ok photos) ->
      ( { model | photos = photos }, Cmd.None )

     
