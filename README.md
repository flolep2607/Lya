# Lya
Artificial intelligence
--

### _*fichier à modifier*_
* [brain.yml](https://github.com/floflo2607/Lya/blob/master/brain.yml)

### info complementaires
* [tout plein de modules](https://bacardi55.org/kalliope.html)
* [toutes les infos](https://github.com/kalliope-project/kalliope)
* [toutes les info sur brain](https://github.com/kalliope-project/kalliope/blob/master/Docs/brain.md)
* [signel market](https://kalliope-project.github.io/signals_marketplace.html)
* [neuron market](https://kalliope-project.github.io/neurons_marketplace.html)
* [website](https://kalliope-project.github.io/)


### _*voici comment le modifier un module simple*_
<pre><code>---
  - name: "<strong>le nom de votre ordre</strong>"
    signals:
      - order: "<strong>la phrase qui doit etre dite</strong>"
      "<strong>la phrase qui doit etre dite</strong>"
    neurons:
      - say:
         message:
           - "<strong>la reponse 1</strong>"
           - "<strong>la reponse 2</strong>"
           .......
</pre></code>


# brain.yml: le cerveau de Kalliopé

On va à présent faire un tour sur la partie la plus importante de Kalliopé: son cerveau.
Comme expliqué plus haut, le cerveau (brain) de kalliopé est composé de synapses. Un synapse est l’association d’un signal avec une liste de neurones.
Les signaux
Il existe plusieurs type de signaux. Nous allons en décrire ici 2 couramment utilisés:
Un ordre (order)
un événement planifié (event)  
Il existe d’autres type de signaux comme le GPIO input qui peut vous permettre de déclencher vos actions suivant un changement d’état d’un port GPIO du RPI. Pour la liste des signaux disponible c’est par là.
Les ordres
Un ordre est une phrase capturée par le microphone et envoyé au moteur STT afin d’être analysé.
Voici un ordre simple:
<pre><code>
signals:
    - order: "effectue cette action"
</pre></code>
Nous allons voir maintenant un ordre avec argument. Les arguments sont important pour améliorer la flexibilité de votre bot.
Prenons un exemple avec le neuron Wikipédia qui, bien-sur, permet d’effectuer une recherche sur Wikipédia.
Nous pouvons créer un synapse avec un ordre simple comme ceci
<pre><code>
- name: "wikipedia-search"
  signals:
    - order: "cherche sur wikipédia Obama"    
  neurons:
    - wikipedia_searcher:
        language: "fr"        
        query: Obama
        say_template: "résultat de la recherche: {{ summary }}"
</pre></code>
Le synapse va fonctionner, mais cela revient à coder en dur chaque recherche que l’on voudrait effectuer. Pas franchement top pour impressionner les amis. C’est là qu’interviennent les arguments.
Modifions notre synapse
<pre><code>
- name: "wikipedia-search"
  signals:
    - order: "cherche sur wikipédia {{ma_recherche}}"    
  neurons:
    - wikipedia_searcher:
        language: "fr"        
        query: "{{ma_recherche}}"
        say_template: "résultat de la recherche: {{ summary }}"
</pre></code>
On ajoute un argument à l’ordre. Kalliopé va donc insérer tout ce qui est dit après la phrase “cherche sur wikipédia” dans une variable nommée “ma_recherche”.
Cette variable est ensuite utilisable dans les paramètres des neurones. Ici je le donne au paramètre “query”, qui est le nom de la page recherchée.
Les events
Le second type de signal est l’événement planifié (event).
Ce type de signal permet de planifier un événement suivant une fréquence. Par exemple, je veux que Kalliopé me dise bonjour tous les matins à 7h30 en semaine, qu’elle me donne l’heure et me lance ma web radio préférée. Je vais créer un synapse comme celui ci:
<pre><code>
- name: "wake-up"
  signals:
    - event:
        hour: "7"
        minute: "30"
        day_of_week: "1,2,3,4,5"
  neurons:
    - say:
        message:
          - "bonjour"
    - systemdate:
        say_template:
          - "il est {{ hours }} heures et {{ minutes }} minutes"
    - shell: 
        cmd: "mplayer http://192.99.17.12:6410/"
        async: True
</pre></code>
La liste complète des paramètres utilisables par un event sont dans la documentation.
Les neurones
Le dernier point, les neurones. Un neurone est un module, ou plugin, qui va effectuer une action.
Syntaxe
Vous pouvez définir autant de neuron que nécessaire dans un seul synapse sous forme de liste.
La syntaxe est la suivante:
<pre><code>
neurons:
  - neuron_name_1:
      parameter1: "value1"
      parameter2: "value2"
  - neuron_name_2:
      parameter1: "value1"
      parameter2: "value2"
</pre></code>
Paramètres en entrée
Un neuron demande parfois des paramètres en entrée pour fonctionner. Nous trouverez la liste des paramètres dans la documentation du neurone. Certains sont obligatoires, d’autres optionnels.
Un paramètre peut être donné directement dans la configuration du synapse en dur comme ici
<pre><code>
- name: "turn-on"
  signals:
    - order: "allume le couloir"
  neurons:
    - hue:
        bridge_ip: "192.168.0.7"
        group_name:  "couloir"
        state: "on"
</pre></code>
Ici, les paramètres “bridge_ip”, “group_name” et “state” sont codés en dur dans le synapse.
Un paramètre peut être récupéré depuis l’ordre comme ceci:
<pre><code>
- name: "turn-on"
  signals:
    - order: "allume le {{ group_name }}"
  neurons:
    - hue:
        bridge_ip: "192.168.0.7"
        group_name:  "{{ group_name }}"
        state: "on"
</pre></code>
Ou alors récupéré depuis une variable globale comme cela:
<pre><code>
  - name: "run-simple-sleep"
    signals:
      - order: "endors toi un moment"
    neurons:
      - sleep:
          seconds: "{{variable}}"
</pre></code>
Note importante: Si vous utilisez une variable dans un paramètre, il est obligatoire d’utilisez les doubles guillemets pour encadrer celui-ci.
Cette syntaxe est fausse:
<pre><code>
 seconds: {{variable}}
</pre></code>
Celle-ci est correct:
<pre><code>
 seconds: "{{variable}}"
</pre></code>
Paramètres en sortie
Kalliopé est un framework, cela signifie que c’est un outil pour concevoir votre assistant comme vous le souhaitez.
Chaque neuron possède sa propre configuration en entrée, et retourne des variables en sortie que vous pouvez utiliser pour concevoir votre réponse.
Prenons un exemple avec le neurone “systemdate”, qui permet de donner l’heure. La documentation de ce neurone vous donne la liste des variables qui seront retournées et que vous pouvez utiliser dans votre template.
Les variables instanciées qui serons retournées sont: hours, minutes, weekday, month, day_month et year.
On peut donc écrire un synapse avec un template de réponse comme suit:
<pre><code>
- name: "say-local-date"
  signals:
    - order: "quelle heure est-il"
  neurons:
    - systemdate:
        say_template:
          - "il est {{ hours }} heure et {{ minutes }} minute"
</pre></code>
Ici, Kalliopé instanciera les valeurs “hours” et “minutes” au moment de l’appel et les transmettra au template “say_template”.
Ce qui donnera un résultat du genre: “il est 9 heures et 32 minutes”.
Vous pouvez donc choisir ce que va répondre vôtre bot, et ce dans la langue que vous souhaitez du moment que le moteur TTS gère cette langue.
Le templating est basé sur un moteur nommé Jinja. Ce moteur vous permet de jouer avec les variables comme bon vous semble.
Par exemple, je modifie mon synapse pour que cette fois il utilise un fichier de template.
<pre><code>
- name: "gouter-time"
  signals:
    - order: "est-ce qu'il est l'heure du goûter"
  neurons:
    - systemdate:
        file_template: "gouter.j2"
</pre></code>
Je créé à présent un fichier gouter.j2 avec le contenu suivant
<pre><code>
{% if hours|int() in range(16,17) %}
oui il est l'heure
{% else %}
non pas encore
{% endif %}
</pre></code>
J’utilise ici le moteur et sa structure de contrôle afin de faire dire à mon bot si il est l’heure du goûter en fonction des variables retournées par le neurones au moment de l’utilisation.
Jinja propose de multiples structures de contrôles (if, else, boucle for, etc..) vous permettant de créer un nombre illimité de combinaison pour les réponses de vôtre assistant.
Mise en mémoire de variable avec Kalliope Memory
Kalliopé peut stocker en mémoire à court terme:
des paramètres de sortie des neurones
des variables provenant d’un ordre
Exemple 1: mise en mémoire de paramètres de sortie d’un neuron. 
<pre><code>
- name: "say-local-date"
    signals:
      - order: "quelle heure est-il"
    neurons:
      - systemdate:
          say_template:
            - "il est {{ hours }} heure et {{ minutes }} minute"
          kalliope_memory:
            hours_when_asked: "{{ hours }}"
            minutes_when_asked: "{{ minutes }}"
</pre></code>
Ici, le neuron systemdate génère des variables qui sont données en sortie au template pour faire parler kalliopé et également passés à la mémoire temporaire de Kalliopé.
La mémoire peut être utilisée dans un autre appel d’un autre synapse comme ceci
<pre><code>
- name: "synapse-name-2"
  signals:
    - order: "a qu'elle heure ai-je demandé l'heure?"
  neurons:
    - say:
        message:
          - "a {{ kalliope_memory['hours_when_asked']}} heures et {{ kalliope_memory['minutes_when_asked']}} minutes"
</pre></code>
Etant basé sur un système de Template, la valeur peut être modifié en ajoutant d’autres mots  au moment de la mise en mémoire:
<pre><code>
kalliope_memory:
  my_saved_key: "{{ neuron_parameter_name }} avec d'autres mots"
</pre></code>
Ou concaténer plusieurs variables de sortie du neuron dans la même variables en mémoire:
<pre><code>
kalliope_memory:
  my_saved_key: "{{ neuron_parameter_name1 }} et {{ neuron_parameter_name2 }}"
</pre></code>
Exemple 2: mise en mémoire de paramètres capturés dans l’ordre

<pre><code>- name: "synapse-id"
  signals:
    - order: "dis bonjour à {{ name }}"
  neurons:
    - say:
        message: "bonjour {{ name }}"
        kalliope_memory:
          friend: "{{ name }}"
</pre></code>
Ici, la variable “name”  est utilisée dans le template au moment de faire parler Kalliopé et est également placée en mémoire sous une variable nommée “friend”.
On peut par la suite accéder à la mémoire pour faire répéter le nom de nôtre ami
<pre><code>
- name: "synapse-id"
  signals:
    - order: "quel est le nom de mon ami?"
  neurons:
    - say:
        message:
          - "C'est {{ kalliope_memory['friend'] }} 
</pre></code>
Un dernier exemple pour comprendre la mécanique de mémoire de Kalliopé. Dans le scénario suivant, on veut que Kalliopé nous rappelle d’appeler nôtre maman dans 15 minutes
Moi: rappel moi de téléphoner à maman dans 15 minutes 
Kalliopé: Je vous le rappel dans 15 minutes 
15 minutes plus tard… 
Kalliopé: Vous m’avez demandé de vous rappeler de téléphoner à maman il y a 15 minutes
Voici le brain que l’on peut écrire

<pre><code>
  - name: "remember-synapse"
    signals:
      - order: "rappel-moi de {{ remember }} dans {{ time }} minutes"
    neurons:
      - neurotimer:
          minutes: "{{ time }}"
          synapse: "remember-todo"
          kalliope_memory:
            remember: "{{ remember }}"
            minutes_ago: "{{ time }}"
      - say:
          message:
            - "Je vous le rappel dans {{ time }} minutes"

  - name: "remember-todo"
    signals: {}
    neurons:
      - say:
          message:
            - "Vous m'avez demandé de vous rappeler de {{ kalliope_memory['remember'] }} il y a {{ kalliope_memory['minutes_ago'] }} minutes"
</pre></code>


[En savoir plus] (https://www.framboise314.fr/kalliope-assistant-personnel-customisable/#HSWJ7mVkAlKU8xEt.99)
