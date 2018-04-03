---
  - name: "play-music-hiphop"
    signals:
      - order: "mets de la bonne musique"
    neurons:
      - kalliopempd:
          mpd_action: "playlist"
          mpd_url: "******"
          mpd_port: "****"
          mpd_random: 1
          query: "HipHop"

  - name: "search-fashion-music"
    signals:
      - order: "Mets de la musique à la mode"
    neurons:
      - kalliopempd:
          mpd_url: "******"
          mpd_port: "****"
          mpd_action: "playlist_spotify"
          mpd_random: 0
          query: "Spotify/Top tracks/Global"

  - name: "play-toggle"
    signals:
      - order: "mets la musique en pause"
      - order: "enlève pause"
    neurons:
      - kalliopempd:
          mpd_url: "******"
          mpd_port: "****"
          mpd_action: "toggle_play"
          mpd_random: 1

  - name: "play-next"
    signals:
      - order: "chanson suivante"
    neurons:
      - kalliopempd:
          mpd_url: "******"
          mpd_port: "****"
          mpd_action: "play_next"

  - name: "play-previous"
    signals:
      - order: "chanson précédente"
    neurons:
      - kalliopempd:
          mpd_url: "******"
          mpd_port: "****"
          mpd_action: "play_previous"

  - name: "play-stop"
    signals:
      - order: "stop la musique"
    neurons:
      - kalliopempd:
          mpd_url: "******"
          mpd_port: "****"
          mpd_action: "play_stop"

  - name: "search-music"
    signals:
      - order: "mets de la musique de {{query}}"
    neurons:
      - kalliopempd:
          mpd_action: "search"
          mpd_random: 0
          mpd_url: "******"
          mpd_port: "****"
          args:
            - query

  - name: "play-radio-rire-chanson"
    signals:
      - order: "radio rire et chansons"
    neurons:
      - kalliopempd:
          mpd_url: "******"
          mpd_port: "****"
          mpd_action: "file"
          mpd_random: 0
          query: "tunein:station:s*****"

  - name: "play-radio-voltage"
    signals:
      - order: "radio voltage"
    neurons:
      - kalliopempd:
          mpd_url: "******"
          mpd_port: "****"
          mpd_action: "file"
          mpd_random: 0
          query: "tunein:station:s*****"
