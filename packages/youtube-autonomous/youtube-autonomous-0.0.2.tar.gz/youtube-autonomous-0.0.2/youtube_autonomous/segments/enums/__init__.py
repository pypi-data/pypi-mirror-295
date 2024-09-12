from enum import Enum

class SegmentType(Enum):
    """
    These Enums represent the types that a Segment could be, allowing
    us to check and detect if it is valid.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
    MY_STOCK = 'my_stock'
    STOCK = 'stock'
    AI_IMAGE = 'ai_image'
    IMAGE = 'image'
    YOUTUBE_VIDEO = 'youtube_video'
    YOUTUBE_SEARCH = 'youtube_search'
    GOOGLE_SEARCH = 'google_search'
    TEXT = 'text'
    MEME = 'meme'
    
class SegmentField(Enum):
    """
    These Enums represent the fields that a Segment has, allowing us
    to check that any required field is provided and/or to detect 
    which one is missing.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
    TYPE = 'type'
    KEYWORDS = 'keywords'
    URL = 'url'
    TEXT = 'text'
    VOICE = 'voice'
    DURATION = 'duration'
    AUDIO_NARRATION_FILENAME = 'audio_narration_filename'

class SegmentElementType(Enum):
    """
    These Enums represent the type of elements we can use to enhance
    a segment.
    """
    MEME = 'meme'
    STICKER = 'sticker'
    IMAGE = 'image'
    SOUND = 'sound'
    GREEN_SCREEN = 'green-scren'
    EFFECT = 'effect'
    ALL = [MEME, STICKER, IMAGE, SOUND, GREEN_SCREEN, EFFECT]
    """
    This enum must be used only for validation process. This has been made to 
    check if some provided type is valid as it is one of the valid and 
    available ones.
    """

class SegmentElementField(Enum):
    """
    These Enums represent the type of fields we can use with the
    segment enhancement elements to fit correctly the segment.
    """
    ACTIVE = 'active'
    KEYWORDS = 'keywords'
    DURATION = 'duration'
    START = 'start'
    MODE = 'mode'
    ORIGIN = 'origin'
    ALL = [ACTIVE, KEYWORDS, DURATION, START, MODE, ORIGIN]
    """
    This enum must be used only for validation process. This has been made to
    check if some provided enhancement field is valid or not and that all fields
    are given.
    """

class SegmentConstants(Enum):
    """
    These Enums are constants we need to use during the project
    and segments processing.
    """
    FILE_DURATION = 9999
    """
    This is the duration, as int value, that will be considered as
    the original video duration and will be used to set the original
    clip (that can be downloaded or load from local storage) duration
    as the final duration. This amount is just to be recognized and 
    will be replaced, when file processed, by the real duration.
    """

class SegmentElementMode(Enum):
    """
    These Enums represent the different ways in which the project
    segment elements can be built according to the way they are
    included in the segment.
    """
    INLINE = 'inline'
    """
    Those segment elements that will be displayed in 'inline' mode, that
    means they will interrupt the main video, be played, and then go back
    to the main video. This will modify the clip length, so we need to 
    refresh the other objects start times.
    """
    OVERLAY = 'overlay'
    """
    Those segment elements that will be displayed in 'overlay' mode, that
    means they will be shown in the foreground of the main clip, changing
    not the main video duration, so they don't force to do any refresh.
    """
    DEFAULT = INLINE
    """
    This is the default value I want (me, the developer, is the one who
    sets it by now). This one will be pointing to another of the available
    Enums. This Enum has been created to make it easy building objects in
    code and having the default value in only one strict place.
    """
    ALL = [INLINE, OVERLAY]
    """
    This is for validation purposes only.
    """

class SegmentElementOrigin(Enum): 
    """
    These Enums represent the way in which the project segment elements
    are searched and obtained from.
    """   
    YOUTUBE = 'youtube'
    """
    Those segment elements that will be searched in Youtube and downloaded
    if found and available.
    """
    FILE = 'file'
    """
    Those segment elements that will be load from local storage. The 
    location must be set in the segment building object.
    """
    DEFAULT = YOUTUBE
    """
    This is the default value I want (me, the developer, is the one who
    sets it by now). This one will be pointing to another of the available
    Enums. This Enum has been created to make it easy building objects in
    code and having the default value in only one strict place.
    """
    ALL = [YOUTUBE, FILE]
    """
    This is for validation purposes only.
    """

class SegmentElementStart(Enum):
    """
    These Enums represent the moment of the segment in which the 
    elements will be included.
    """
    START_OF_CURRENT_WORD = 'start_of_current_word'
    """
    This will make the segment object appear in the same moment that the 
    word that is before the shortcode starts (attending to transcription
    'start' timestamped field).
    """
    END_OF_CURRENT_WORD = 'end_of_current_word'
    """
    This will make the segment object appear in the same moment that the
    word that is before the shortcode ends (attending to transcription
    'end' timestamped field).
    """
    BEFORE_NEXT_WORD = 'before_next_word'
    """
    This will make the segment object appear in between the word that is
    before the shortcode and the next one. This one should start in the 
    silence gap between words.
    """
    DEFAULT = START_OF_CURRENT_WORD
    ALL = [START_OF_CURRENT_WORD, END_OF_CURRENT_WORD, BEFORE_NEXT_WORD]
    """
    This is for validation purposes only.
    """

class SegmentElementDuration(Enum):
    """
    These Enums represent the time, during a segment lifetime, that
    the elements are going to last (be shown).
    """
    END_OF_CURRENT_WORD = 'end_of_current_word'
    """
    This will make the segment object last until the end of the word
    that this literal says. This has a ':' because it must have
    a number after the ':' to work. The number means the amount of
    words that the segment object will last. If 'end_of_current_word:0', it 
    will last until the end of the word that is just before the 
    shortcode. If 'end_of_current_word:2', it will last until the end of the
    next of the next word (2nd word after the shortcode).
    """
    END_OF_SUBSEQUENT_WORD = 'end_of_subsequent_word_'
    """
    This will make the segment object last until the end of one of
    the subsequent words. This string will be end with a number 
    just after the last underscore, and that will be the number of
    words we need to wait to end. For example, if the value is
    'end_of_subsequent_word_2', we will count 2 more words to
    wait for the end of that one (if available).
    """
    FILE_DURATION = 'file_duration'
    """
    This will make the segment last the clip duration. It will be
    considered when the file is downloaded, and that duration will
    be flagged as 9999. This is for videos or audios that have a
    duration based on file.
    """
    ALL = [END_OF_CURRENT_WORD, END_OF_SUBSEQUENT_WORD, FILE_DURATION]
    """
    This is for validation purposes only.
    """