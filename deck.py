"""
Class defining a deck of flashcards that may be divided into chapters.
Includes functionality to:
    - deal cards from a deck
    - parse deck(s) from sanitized deck file(s)
    - retrieve deck information

Written by techn0mancr.
"""

# Standard library imports
from os import listdir

# Custom library imports
from helper import path_join, shuffle
from json import load

# Constant definitions
REQUIRED_KEYS = {
    "name": str(),
    "cards": None
}
VALID_KEYS = {
    "description": str()
}

class Deck:

    """ Object default methods """
    
    def __init__(self, *, json_path=None):
        """
        Initialises an empty deck with default attribute values,
        optionally loading deck information from the given deck file.

        Parameters
        ----------
        json_path : str, optional
            Path specifying a JSON-formatted deck file to parse,
            by default None
        """

        self.__name         = REQUIRED_KEYS["name"]
        self.__description  = VALID_KEYS["description"]
        self.__cards        = REQUIRED_KEYS["cards"]
        self.__has_chapters = False

        # Load information from JSON file
        if json_path:
            self.parse_from_json(json_path)

    """ Object properties """

    @property
    def name(self):
        """
        Accesses this deck's name.

        Returns
        -------
        str
            Name of this deck.
        """

        return self.__name
    
    @property
    def description(self):
        """
        Accesses this deck's description.

        Returns
        -------
        str
            Description of this deck.
        """

        return self.__description

    """ Class methods """
    @staticmethod
    def parse_decks(base_path="."):
        """
        Parses data from deck files within the working directory
        and populates them into corresponding decks,
        optionally loading deck files from the given directory path.

        Parameters
        ----------
        base_path : str, optional
            Path specifying a directory containing deck files to load,
            by default .
        
        Returns
        -------
        List[Deck]
            List of populated decks.
        """
        
        decks = []

        # Load decks from *JSON* files in base_path
        for deck_file in listdir(base_path):
            json_path = path_join(base_path, deck_file)
            parsed_deck = Deck(json_path=json_path)
            decks.append(parsed_deck)

        return decks
    
    @staticmethod
    def __cast_cards(cards):
        """
        Casts parsed cards into their appropriate types,
        based on whether the cards are divided into chapters.

        Parameters
        ----------
        cards : List[List[str...]] | Dict[str, List[List[str...]]]
            Either:
                - a list of string lists corresponding to cards, or
                - a dictionary of strings mapped to lists of
                  string lists corresponding to chapters of cards

        Returns
        -------
        Tuple[
            List[Tuple[str...]] | Dict[str, List[Tuple[str...]]],
            bool
        ]
            Tuple of either:
                - cards represented by a list of tuple lists, or
                - cards divided into chapters represented by a
                  dictionary of chapter strings mapped to
                  lists of tuple lists
            and a boolean value specifying whether
            the cards are divided into chapters.

        """

        casted_cards = REQUIRED_KEYS["cards"]
        has_chapters = (type(cards) is dict)

        if has_chapters:
            # Cards is a dictionary of lists corresponding to chapters
            casted_cards = {
                chapter: [tuple(card) for card in cards[chapter]]
                for chapter in cards.keys()
            }
        else:
            # Cards is a list
            casted_cards = [tuple(card) for card in cards]
        
        return casted_cards, has_chapters

    @staticmethod
    def __sanitize_data(data):
        """
        Sanitizes the given data object to satisfy the deck schema
        defined by REQUIRED_KEYS and VALID_KEYS.

        Parameters
        ----------
        data : Any
            Data object to sanitize.
        
        Returns
        -------
        Dict[
            str,
            str | List[List[str...]] | Dict[str, List[List[str...]]]
        ], optional
            Dictionary mapping data key strings to either:
                - another string for informational fields
                - a list of string lists for cards
                - another dictionary mapping strings to
                  lists of string lists for chapters of cards
            or None if data sanitization failed.
        """

        # Check data's type
        if type(data) is not dict:
            return None

        key_set      = set(data)
        required_set = set(REQUIRED_KEYS)
        valid_set    = set(VALID_KEYS)

        # Check if all REQUIRED_KEYS are present
        if key_set < required_set:
            return None
        
        # Remove invalid keys
        sanitized_data = {
            key: data[key]
            for key in data
            if key in (required_set | valid_set)
        }

        # Initialise missing VALID_KEYS
        for valid_key, default_value in VALID_KEYS.items():
            if valid_key not in sanitized_data:
                sanitized_data[valid_key] = default_value
        
        return sanitized_data

    """ Object methods """

    def cards(self, *, chapter=None, random=False):
        """
        Deals this deck's cards, optionally:
            - drawing cards from the given chapter
            - shuffling them in random order

        Parameters
        ----------
        chapter : str, optional
            Chapter to draw cards from, by default None
        random : bool, optional
            Flag denoting whether dealt cards are randomly shuffled,
            by default False

        Returns
        -------
        List[Tuple[str...]]
            Cards represented by a list of string tuples.
        """

        dealt_cards = []

        # Draw cards according to input parameters
        cards = self.__cards
        if self.__has_chapters:
            if chapter:
                # Draw cards from the given chapter
                dealt_cards += \
                    (cards[chapter] if cards.get(chapter) else [])
            else:
                # Draw cards from all chapters
                for chapter in cards.keys():
                    dealt_cards += cards[chapter]
        else:
            # Draw all cards
            dealt_cards += (cards if cards else [])
        
        # Shuffle cards
        if random:
            shuffle(dealt_cards)
        
        return dealt_cards

    def parse_from_json(self, json_path):
        """
        Loads deck information into this deck from
        a JSON-formatted deck file.

        Parameters
        ----------
        json_path : str
            Path specifying a JSON-formatted deck file to parse

        Returns
        -------
        bool
            True if the deck information was successfully loaded, or
            False otherwise.
        """

        sanitized_data = None
 
        # Load and sanitize data
        with open(json_path) as json_stream:
            data_dict = load(json_stream)
            sanitized_data = Deck.__sanitize_data(data_dict)
        
        # Verify data sanitization result
        if not sanitized_data:
            return False  # TODO: throw an exception?
        
        # Load sanitized data into object
        name, description, cards = \
            sanitized_data["name"], \
            sanitized_data["description"], \
            sanitized_data["cards"]
        self.__name = name
        self.__description = (description if description else "")
        self.__cards, self.__has_chapters = Deck.__cast_cards(cards)

        return True