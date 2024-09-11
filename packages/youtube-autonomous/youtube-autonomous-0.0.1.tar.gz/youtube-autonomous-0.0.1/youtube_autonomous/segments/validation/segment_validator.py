from youtube_autonomous.exceptions.invalid_segment_exception import InvalidSegmentException
from youtube_autonomous.segments.enums import SegmentType, SegmentField
from youtube_autonomous.segments.validation.consts import VALID_SEGMENT_TYPES, NEED_KEYWORDS_SEGMENT_TYPES, URL_SEGMENT_TYPES, NARRATION_SEGMENT_TYPES, NEED_TEXT_SEGMENT_TYPES
from yta_general_utils.file_processor import file_exists, file_is_audio_file
from yta_general_utils.url_checker import url_is_image, url_is_ok


class SegmentValidator:
    def __init__(self):
        pass

    # TODO: We need to build a 'validate_pre' and a 'validate_post'
    # because we first need to know if we have the basic structure
    # to build a Segment, but then we need to validate that the
    # provided data is also valid (images are downloadable, etc.)

    # TODO: Apply 'segment' type
    def validate(self, segment):
        """
        Validates the provided 'segment' to check if it is a processable one
        so we can store it to be processed later when requested. Checks if 
        the provided 'segment' is valid or not. It returns True if yes or 
        raises a detailed InvalidSegmentException if not.
        """
        # No type provided
        if not SegmentField.TYPE.value in segment:
            raise InvalidSegmentException('Field "' + SegmentField.TYPE.value + '" not provided.')
        
        # Is a non-accepted type
        if self.__is_invalid_type(segment):
            raise InvalidSegmentException('Type "' + segment[SegmentField.TYPE.value] + '" not valid.')
        
        # Need keywords but doesn't have
        if self.__has_no_keywords(segment):
            raise InvalidSegmentException('No "' + SegmentField.KEYWORDS.value + '" field provided.')

        # Need url but doesn't have
        if self.__has_no_url(segment):
            raise InvalidSegmentException('No "' + SegmentField.URL.value + '" field provided.')
        
        # Need text but doesn't have
        if self.__has_no_text(segment):
            raise InvalidSegmentException('No "' + SegmentField.TEXT.value + '" field provided.')
        
        # Need voice and text at the same time, but only one
        if self.__has_no_voice_and_text(segment):
            raise InvalidSegmentException('Fields "' + SegmentField.VOICE.value + '" and "' + SegmentField.TEXT + '" must exist at the same time to be able to narrate.')
        
        # Need to calculate duration but cannot
        if self.__has_no_duration(segment):
            raise InvalidSegmentException('We need "' + SegmentField.TEXT.value + '", "' + SegmentField.DURATION.value + '" or "' + SegmentField.AUDIO_NARRATION_FILENAME.value + '". We need something to know how much time in some way.')
        
        # Need url but is not available
        if self.__has_invalid_url(segment):
            raise InvalidSegmentException('Provided "' + SegmentField.URL.value + '" is not available.')
        
        # Need image url but is not valid
        if self.__has_no_image_url(segment):
            raise InvalidSegmentException('Provided "' + SegmentField.URL.value + '" is not a valid image.')
        
        # Has narration file but is not valid
        if self.__has_no_valid_file(segment):
            raise InvalidSegmentException('Provided ' + SegmentField.AUDIO_NARRATION_FILENAME.value + ' "' + segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value) + '" is not a valid file.')
        
        # Has narration file but is not audio file
        if self.__has_no_audio_file(segment):
            raise InvalidSegmentException('Provided ' + SegmentField.AUDIO_NARRATION_FILENAME.value + ' "' + segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value) + '" is not an audio file.')
        
        return True
        
    def __is_invalid_type(self, segment):
        """
        Returns True if the provided 'segment' has an invalid type.
        """
        return segment[SegmentField.TYPE.value] not in VALID_SEGMENT_TYPES

    def __has_no_keywords(self, segment):
        """
        Returns True if the provided 'segment' needs the keywords field but
        doesn't have it.
        """
        return segment[SegmentField.TYPE.value] in NEED_KEYWORDS_SEGMENT_TYPES and not segment.get(SegmentField.KEYWORDS.value)

    def __has_no_url(self, segment):
        """
        Returns True if the provided 'segment' needs the url field but doesn't
        have it.
        """
        return segment[SegmentField.TYPE.value] in URL_SEGMENT_TYPES and not segment.get(SegmentField.URL.value)

    def __has_no_text(self, segment):
        """
        Returns True if the provided 'segment' needs the text field but doesn't
        have it.
        """
        return segment[SegmentField.TYPE.value] in NEED_TEXT_SEGMENT_TYPES and not segment.get(SegmentField.TEXT.value)

    def __has_no_voice_and_text(self, segment):
        """
        Returns True if the provided 'segment' is a narration type segment
        but has only one narration field (voice or text) but not both at
        the same time.
        """
        return segment[SegmentField.TYPE.value] in NARRATION_SEGMENT_TYPES and ((segment.get(SegmentField.TEXT.value) and not segment.get(SegmentField.VOICE.value)) or (segment.get(SegmentField.VOICE.value) and not segment.get(SegmentField.TEXT.value)))

    def __has_no_duration(self, segment):
        """
        Returns True if the provided 'segment' has no field to calculate
        the duration.
        """
        return not segment.get(SegmentField.TEXT.value) and not segment.get(SegmentField.DURATION.value) and not segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value)

    def __has_invalid_url(self, segment):
        """
        Returns True if the provided 'segment' has an invalid url.
        """
        return segment.get(SegmentField.TYPE.value) in URL_SEGMENT_TYPES and not url_is_ok(segment.get(SegmentField.URL.value))

    def __has_no_image_url(self, segment):
        """
        Returns True if the provided 'segment' is an image segment but has
        no valid image url.
        """
        # TODO: Maybe we could handle this with an array like the other ones
        # and not as a simple possible value (image) to do in the same way
        return segment.get(SegmentField.TYPE.value) == SegmentType.IMAGE.value and not url_is_image(segment.get(SegmentField.URL.value))

    def __has_no_valid_file(self, segment):
        """
        Returns True if the provided 'segment' has a narration file but is 
        not a valid file.
        """
        return segment.get(SegmentField.TYPE.value) in NARRATION_SEGMENT_TYPES and segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value) and not file_exists(segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value))

    def __has_no_audio_file(self, segment):
        """
        Returns True if the provided 'segment' has a narration file but is
        not an audio file.
        """
        return segment.get(SegmentField.TYPE.value) in NARRATION_SEGMENT_TYPES and segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value) and not file_is_audio_file(segment.get(SegmentField.AUDIO_NARRATION_FILENAME.value))
    
    # TODO: Keep working with these below:
    # TODO: Check if 'youtube_video' language exist and is valid
    # TODO: Check if 'youtube_video' duration is valid (not str, not negative nor excesive)
    # TODO: Check if effects provided are valid