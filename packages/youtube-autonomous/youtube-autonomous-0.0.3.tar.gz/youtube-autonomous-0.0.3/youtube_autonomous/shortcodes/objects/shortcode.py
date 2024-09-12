from youtube_autonomous.shortcodes.enums import ShortcodeType


class Shortcode:
    """
    Class that represent a shortcode detected in a text, containing 
    its attributes and values and also the content if block-scoped.
    """
    def __init__(self, tag: str, type: ShortcodeType, attributes: dict, context, content: str):
        """
        The shortcode has a 'type' and could include some 'attributes' that
        are the parameters inside the brackets, that could also be simple or
        include an associated value. If it is a block-scoped shortcode, it
        will have some 'content' inside of it.
        """
        if not tag:
            raise Exception('No "tag" provided.')
        
        if not type:
            raise Exception('No "type" provided.')
        
        # TODO: Do more checkings

        self.tag = tag
        self.type = type
        # TODO: Maybe do some checks with the attributes, they could be wrong
        # or incomplete. Remember we have 'SegmentElementField' to handle
        # this parameters in a strict way
        self.attributes = attributes
        # TODO: Do we actually need the context (?)
        self.context = context
        # TODO: Do we actually need the content (?)
        self.content = content

        # TODO: We need to include more information to handle them properly
        # 'shortcode': 'sticker',
        # 'previous_word_index': -1,
        self.previous_start_word_index = None
        self.previous_end_word_index = None

        # TODO: Maybe we need to create an abstract Shortcode class to inherit
        # in specific shortcode classes

