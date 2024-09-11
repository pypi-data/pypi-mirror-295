

class SegmentContentBuilder:
    def __init__(self):
        # TODO: These objects below are special ones of this project
        # to handle Youtube and Stock elements. I cannot import
        # directly from libraries to use them because it has more
        # logic
        self.youtube_handler = Youtube(True)
        self.stock_handler = Stock(True)

    # TODO: Continue