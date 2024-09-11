from youtube_autonomous.shortcodes.objects.shortcode_tag import ShortcodeTag
from shortcodes import Parser

class ShortcodeParser:
    """
    This class parses the shortcodes from a text, classifies
    them and is capable of handling the information inside.
    """
    def __init__(self, shortcode_tags: list[ShortcodeTag]):
        # TODO: Check that 'shortcode_tags' elements are ShortcodeTags
        # TODO: Maybe we don't want to 'ignore_unknown' and we need
        # to handle them and set as empty return to ignore them
        # TODO: Or maybe we can ignore them and them, at the end, 
        # remove all remaining shortcodes with a regexp
        self.parser = Parser(start = '[', end = ']', ignore_unknown = True)
        
        # We register each shortcode in provided 'shortcode_tags'
        for shortcode_tag in shortcode_tags:
            # We have a different handler for each ShortcodeTag type
            if shortcode_tag.is_block_scoped():
                self.parser.register(self.__block_shortcode_handler, shortcode_tag, '/' + shortcode_tag)
            else:
                self.parser.register(self.__simple_shortcode_handler, shortcode_tag)

        # We register the unknown shortcodes handler to avoid them
        # TODO: Is wildcard working here (?)
        self.parser.register(self.__unknown_shortcode_handler, '*')

    def parse(self, text: str):
        if not text:
            raise Exception('No "text" provided.')
        
        self.text = text
        self.text_without_shortcodes = ''
        self.shortcodes = []

        
        output = self.parser.parse(text, context = None)

    def __simple_shortcode_handler(self, pargs, kwargs, context):
        """
        Handles a simple [tag] shortcode.
        """
        # We want to extract any field and value
        for parg in pargs:
            print(parg)

        for kwarg in kwargs:
            print(kwarg)

        pass

    def __block_shortcode_handler(text, pargs, kwargs, context):
        """
        Handles a block [tag] ... [/tag] shortcode.
        """
        # We want to extract any field and value
        for parg in pargs:
            print(parg)

        for kwarg in kwargs:
            print(kwarg)

        pass

    def __unknown_shortcode_handler(self, pargs, kwargs, context):
        # We just empty and ignore them
        return ''
