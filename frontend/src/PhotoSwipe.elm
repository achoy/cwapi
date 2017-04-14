module PhotoSwipe exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick)

type alias PsPhoto =
  { src : String
   , w : Int
   , h : Int
   , msrc : String
   , title : String }

type alias Model =
  { photos : List PsPhoto
   , options : Any
   , loadingError : Maybe String }

type Msg
  = LoadPhotos (Result Http.Error (List PsPhoto))

initialModel : Model
initialModel =
  { photos = []
  , options =
    { history = False
      , focus = False
      , showAnimationDuration = 0
      , highAnimationDuration = 0 }
  , loadingError = Nothing }

psview : Model -> Html Msg
psview model =
  div [ class "pswp", attribute "aria-hidden" "true",  attribute "role" "dialog", attribute "tabindex" "-1" ]
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
