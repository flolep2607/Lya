---
  - name: "Google-agenda-next"
    signals:
      - order: "quels sont mes prochains rendez-vous"
    neurons:
      - say: 
          message: "Recherche des prochains rendez-vous en cours monsieur"
      - google_calendar:
          credentials_file: "/path/to/file"
          client_secret_file: "/path/to/file"
          scopes: "https://www.googleapis.com/auth/calendar.readonly"
          application_name: "kalliope"
          max_results: 3
          locale: fr_FR.UTF-8
          no_meeting_msg: "Vous n'avez pas de prochain rendez vous"
          meeting_intro_msg: "Vos 3 prochains rendez vous sont"
          file_template: "templates/fr_google_calendar.j2"
