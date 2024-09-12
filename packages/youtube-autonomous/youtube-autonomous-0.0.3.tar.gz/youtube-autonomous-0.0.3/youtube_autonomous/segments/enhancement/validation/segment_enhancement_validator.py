from youtube_autonomous.segments.enums import SegmentElementField, SegmentElementType, SegmentElementDuration, SegmentElementStart, SegmentElementMode, SegmentElementOrigin


class SegmentEnhancementValidator:
    """
    This class is to validate the Segment enhancement elements that
    are terms that the user register to enhance (to improve) the
    project video experience.

    These terms need to have a valid structure and that's what we
    check here.
    """
    def is_valid(enhancement_terms):
        """
        We will receive the content of a enhancement term and will raise an
        Exception if some structure element or value is not valid according
        to our rules.

        TODO: Write a little bit more about what we are receiving here.
        """
        # TODO: Maybe refactor the terms to simplify them
        for enhancement_term_key in enhancement_terms:
            enhancement_term = enhancement_terms[enhancement_term_key]
            for type in enhancement_term:
                content = enhancement_term[type]
                if type not in SegmentElementType.ALL.value:
                    # TODO: Make custom exception
                    raise Exception('Segment element type "' + type + '" not accepted.')

                # Lets check values
                active = content.get(SegmentElementField.ACTIVE.value)
                keywords = content.get(SegmentElementField.KEYWORDS.value)
                start = content.get(SegmentElementField.START.value)
                duration = content.get(SegmentElementField.DURATION.value)
                mode = content.get(SegmentElementField.MODE.value)
                origin = content.get(SegmentElementField.ORIGIN.value)

                if not 'active' in content:
                    # TODO: Make custom exception
                    raise Exception('No "' + SegmentElementField.ACTIVE.value + '" field provided in "' + enhancement_term_key + '" term. This field is mandatory and must be "true" if you want to be applied or "false" if not, but it must be set.')

                # Validate fields (even if it is not active)
                if not keywords:
                    # TODO: Make custom exception
                    raise Exception('No "' + SegmentElementField.KEYWORDS.value + '" provided in "' + enhancement_term_key + '" term. This field is mandatory.')

                if not start or start not in SegmentElementStart.ALL.value:
                    # TODO: Make custom exception
                    raise Exception('No "' + SegmentElementField.START.value + '" provided or not valid in "' + enhancement_term_key + '" term. These are the valid ones: "' + ', '.join(SegmentElementStart.ALL.value) + '"')

                
                if not (duration and (duration in [SegmentElementDuration.END_OF_CURRENT_WORD.value, SegmentElementDuration.FILE_DURATION.value] or duration.startswith(SegmentElementDuration.END_OF_SUBSEQUENT_WORD.value))):
                    # TODO: Make custom exception
                    raise Exception('No "' + SegmentElementField.DURATION.value + '" provided or not valid in "' + enhancement_term_key + '" term. These are the valid ones: "' + ', '.join(SegmentElementDuration.ALL.value) + '"')
                
                if duration.startswith(SegmentElementDuration.END_OF_SUBSEQUENT_WORD.value):
                    try:
                        aux = duration.split('_')
                        int(aux[len(aux) - 1])
                    except:
                        raise Exception('The "' + SegmentElementField.DURATION.value + '" field you provided must be like "' + SegmentElementDuration.END_OF_SUBSEQUENT_WORD.value + 'X" format, where the "X" must be an integer number that represent the subsequent word index that must be used in calculations.')

                if not mode or mode not in SegmentElementMode.ALL.value:
                    # TODO: Make custom exception
                    raise Exception('No "' + SegmentElementField.MODE.value + '" provided or not valid in "' + enhancement_term_key + '" term. These are the valid ones: "' + ', '.join(SegmentElementMode.ALL.value) + '"')

                if not origin or origin not in SegmentElementOrigin.ALL.value:
                    # TODO: Make custom exception
                    raise Exception('No "' + SegmentElementField.ORIGIN.value + '" provided or not valid in "' + enhancement_term_key + '" term. These are the valid ones: "' + ', '.join(SegmentElementOrigin.ALL.value) + '"')