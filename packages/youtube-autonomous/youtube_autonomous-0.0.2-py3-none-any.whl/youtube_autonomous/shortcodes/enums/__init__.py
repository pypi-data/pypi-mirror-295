from enum import Enum

class ShortcodeType(Enum):
    """
    This Enum represents the different type of shortcodes that
    we can handle according to their scopes. It could be simple
    [tag] shortcode or a block-scoped one [tag] ... [/tag].
    """
    BLOCK = 'block'
    SIMPLE = 'simple'