"""
Written by techn0mancr.
"""

# Card = NewType('Card', Tuple[str, ...])
# Cards = NewType('Cards', List[Card])

# Custom library imports
from helper import shuffle
from json import load

# Helper constant definitions
REQUIRED_KEYS = {"name", "cards"}
VALID_KEYS    = REQUIRED_KEYS | {"description"}

class Deck:

    """ Object default methods """
    
    def __init__(self):
        self.__name         = ""
        self.__description  = ""
        self.__cards        = None
        self.__has_chapters = False

    """ Object properties """

    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description

    """ Class methods """
    
    @staticmethod
    def __sanitize_data(data_dict):
        # Check if all REQUIRED_KEYS are present
        key_set = set(data_dict.keys())
        if key_set < REQUIRED_KEYS:
            return None
        
        # Remove invalid keys
        return {
            key: data_dict[key]
            for key in data_dict.keys()
            if key in VALID_KEYS
        }
    
    """ Object methods """

    def cards(self, *, chapter=None, random=False):
        dealt_cards = []

        # Draw cards according to input parameters
        cards = self.__cards
        if self.__has_chapters:
            if chapter:
                # Draw cards from the given chapter
                dealt_cards += (cards[chapter] if cards.get(chapter) else [])
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
        data_dict = None
 
        # Read data
        with open(json_path) as json_stream:
            data_dict = load(json_stream)
            data_dict = Deck.__sanitize_data(data_dict)
        
        # Verify data sanitization result
        if not data_dict:
            return False  # TODO: throw an exception?
        
        # Load data into object
        self.__name = data_dict["name"]
        self.__description = (data_dict["description"] if data_dict.get("description") else "")
        self.__has_chapters = (type(data_dict["cards"]) is dict)

        # Cast cards into its correct type
        cards = data_dict["cards"]
        if self.__has_chapters:
            self.__cards = {
                chapter: [tuple(card) for card in cards[chapter]]
                for chapter in cards.keys()
            }
        else:
            self.__cards = [tuple(card) for card in cards]
        
        return True