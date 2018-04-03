---
  - name: "Gmaps-distance"
    signals:
      - order: "distance entre {{origin}} et {{destination}}"
    neurons:
      - say:
          message: "Calcul en cours"
      - gmaps:
          gmaps_api_key: "************"
          mode: "driving"
          language: "fr"
          units: "metric"
          traffic_model: "pessimistic"
          args:
            - origin
            - destination
          file_template: "templates/fr_gmaps.j2"

  - name: "Gmaps-distance-from-home"
    signals: 
      - order: "distance pour aller à {{destination}}"
    neurons:
      - say:
          message: "Calcul en cours"
      - gmaps:
          gmaps_api_key: "************"
          mode: "driving"
          language: "fr"
          units: "metric"
          origin: "***************"
          mode: "driving"
          args:
            - destination
          file_template: "templates/fr_gmaps.j2"

  - name: "Gmaps-place-address"
    signals: 
      - order: "adresse de {{search}}"
    neurons:
      - say:
          message: "Calcul en cours"
      - gmaps:
          gmaps_api_key: "************"
          language: "fr"
          units: "metric"
          args:
            - search
          file_template: "templates/fr_gmaps.j2"

  - name: "Gmaps-distance-from-home-by-tube"
    signals: 
      - order: "métro {{destination}}"
    neurons:
      - say:
          message: "Calcul en cours"
      - gmaps:
          gmaps_api_key: "************"
          mode: "transit"
          language: "fr"
          units: "metric"
          origin: "***************"
          direction: True
          args:
            - destination
          file_template: "templates/fr_gmaps.j2"

  - name: "Gmaps-directions-by-care"
    signals: 
      - order: "directions {{destination}}"
    neurons:
      - say:
          message: "Calcul en cours"
      - gmaps:
          gmaps_api_key: "************"
          mode: "driving"
          language: "fr"
          units: "metric"
          origin: "***************"
          direction: True
          args:
            - destination
          file_template: "templates/fr_gmaps.j2"
