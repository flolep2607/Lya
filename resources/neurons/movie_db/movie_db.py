import logging

import tmdbsimple as tmdb

from kalliope.core.NeuronModule import (NeuronModule,
                                        MissingParameterException,
                                        InvalidParameterException)

logging.basicConfig()
logger = logging.getLogger("kalliope")

MOVIEDB_ACTIONS = (
    "MOVIE",
    "PEOPLE",
    "POPULAR",
    "TOP_RATED",
    "UPCOMING",
    "NOW_PLAYING"
)

class Movie_db(NeuronModule):
    """
    Class used to search through The Movie Db API
    """
    def __init__(self, **kwargs):

        super(Movie_db, self).__init__(**kwargs)

        # parameters
        self.api_key = kwargs.get('api_key', None)
        self.language = kwargs.get('language', 'en-us')
        self.action = kwargs.get('action', None)
        self.region = kwargs.get('region', None)

        self.movie = kwargs.get('movie', None)
        self.movie_extra = kwargs.get('movie_extra', None)

        self.people = kwargs.get('people', None)

        logger.debug("Movie Db launch for action %s", self.action)

        # check parameters
        if self._is_parameters_ok():

            tmdb.API_KEY = self.api_key

            if self.action == MOVIEDB_ACTIONS[0]:  # MOVIE
                if self._is_movie_parameters_ok():
                    logger.debug("Searching for movies %s for language %s",
                                 self.movie,
                                 self.language)

                    result = dict()
                    result["query"] = self.movie
                    search = tmdb.Search()
                    search_response = search.movie(query=self.movie, language=self.language)

                    first_movie = next(iter(search_response["results"]), None)
                    if first_movie is None:
                        logger.debug("No movie matches the query")

                    else:
                        logger.debug("Movie db first result : %s with id %s",
                                     first_movie['title'],
                                     first_movie['id'])

                        movie = tmdb.Movies(first_movie['id'])
                        result['movie'] = movie.info(language=self.language,
                                                     append_to_response=self.movie_extra)

                    self.say(result)

            if self.action == MOVIEDB_ACTIONS[1]:  # PEOPLE
                if self.is_people_parameters_ok():
                    logger.debug("Searching for people with query %s", self.people)

                    search = tmdb.Search()
                    response = search.person(query=self.people)
                    first_people = search.results[0]
                    logger.debug("Movie db first result for people : %s", first_people)
                    self.say(first_people)

                    ##people = tmdb.People(firstPeople['id'])
                    ##peopleResponse = people.info()
                    ##self.say(peopleResponse)

            if self.action == MOVIEDB_ACTIONS[2]:  # POPULAR
                logger.debug("Searching for popular movies for language %s", self.language)
                movies = tmdb.Movies()
                popular_response = movies.popular(language=self.language)
                self.say(popular_response)

            if self.action == MOVIEDB_ACTIONS[3]:  # TOP_RATED
                logger.debug("Searching for top rated movies for language %s", self.language)
                movies = tmdb.Movies()
                top_rated_response = movies.top_rated(language=self.language)
                self.say(top_rated_response)

            if self.action == MOVIEDB_ACTIONS[4]:  # UPCOMING
                logger.debug("Searching for upcoming movies for language %s", self.language)
                movies = tmdb.Movies()
                upcoming = movies.upcoming(language=self.language, region=self.region)
                self.say(upcoming)

            if self.action == MOVIEDB_ACTIONS[5]:  # NOW_PLAYING
                logger.debug("Searching for now playing movies for language %s", self.language)
                movies = tmdb.Movies()
                now_playing_response = movies.now_playing(language=self.language,
                                                          region=self.region)
                self.say(now_playing_response)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron.
        :return: True if parameters are ok, raise an exception otherwise.

        .. raises:: MissingParameterException, InvalidParameterException
        """
        if self.api_key is None:
            raise MissingParameterException("MovieDb needs an api key")
        if self.action is None:
            raise MissingParameterException("MovieDb needs an action parameter")
        if self.action not in MOVIEDB_ACTIONS:
            raise InvalidParameterException("MovieDb: invalid actions")
        return True

    def _is_movie_parameters_ok(self):
        """
        Check if parameters required to action MOVIE are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.movie is None:
            raise MissingParameterException("MovieDB MOVIE action needs a movie")

        return True

    def is_people_parameters_ok(self):
        """
        Check if parameters required to action PEOPLE are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.people is None:
            raise MissingParameterException("MovieDb PEOPLE action needs a people to search")

        return True
