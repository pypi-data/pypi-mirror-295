"""
This class represents a Segment that will handle all the information
that it contains to build the project segment video part.
"""
from exceptions.invalid_segment_exception import InvalidSegmentException
from objects.segment_content_builder import SegmentContentBuilder
from moviepy.editor import AudioFileClip
from yta_multimedia.audio.sound.generation import create_silence_audio_file
from yta_general_utils.logger import print_completed, print_error, print_in_progress
from yta_multimedia.audio.voice.generation.tts.google import narrate as generate_google_narration
from utils.shortcodes import handle_shortcodes
from utils.general import create_segment_filename
from yta_general_utils.url_checker import url_is_ok, url_is_image
from yta_general_utils.file_processor import file_exists, file_is_audio_file
from utils.video_utils import apply_effects, apply_sounds, apply_green_screens, apply_images, apply_stickers, apply_memes
from yta_ai_utils.transcription import get_transcription_with_timestamps
from utils.validation.segment.validator import VALID_SEGMENT_TYPES
from segments.building.objects.enums import *
from os import getenv as os_getenv
from dotenv import load_dotenv
from utils.mongo_utils import get_project_by_id, set_project_segment_audio_filename, set_project_segment_transcription, set_project_segment_full_filename, set_project_segment_as_finished
from segments.building.objects.enums import EnhancementField

import re
import segments.building.objects.green_screen
import segments.building.objects.image
import segments.building.objects.meme
import segments.building.objects.sticker
import segments.building.objects.sound
import segments.building.objects.effect

load_dotenv()

BAN_WORDS_PROBABILITY = os_getenv('BAN_WORDS_PROBABILITY')
ENHANCE_WORDS_PROBABILITY = os_getenv('ENHANCE_WORDS_PROBABILITY')


from youtube_autonomous.segments.validation.segment_validator import SegmentValidator
from youtube_autonomous.segments.builder.segment_content_builder import SegmentContentBuilder


class Segment:
    """
    This is a Segment to build itself. This is a post-processed segment. It
    will receive a json file that has been previously processed to fill any
    missing field that can be guessed by an AI.
    """
    def __init__(self, json, project_id, segment_index):
        self.segment_validator = SegmentValidator()
        self.builder = SegmentContentBuilder()

        self.project_id = project_id
        self.segment_index = segment_index

        self.__check_structure_is_valid(json)
        self.audio_narration_filename = json.get('audio_narration_filename')
        self.voice = json.get('voice')
        self.__check_resources_are_available(json)
        self.__check_others(json)
        # TODO: By now I'm not using effects in text
        self.effects = self.__check_and_format_effects(json)
        self.sounds = []
        self.green_screens = []
        self.images = []
        self.stickers = []
        self.memes = []

        self.type = json.get('type')
        self.keywords = json.get('keywords')
        self.text = json.get('text')
        self.text = self.__check_script_text()
        #self.effects = json.get('effects') # Parsed in __check_and_format_effects(json)
        self.frame = json.get('effects')
        self.duration = json.get('duration')
        self.url = json.get('url')

        # Post-processing fields
        """
        These below is for building the basics, the main video and audio. Shortcodes,
        inline and overlay elements and that stuffs comes after this.
        """
        self.shortcodes = []
        self.tmp_filenames = [] # For creation time, to preserve for failures
        self.audio_clip = None
        self.audio_filename = None # Filename of the used audio
        self.transcription = None # Audio transcription
        self.video_clip = None
        self.video_filename = None # Filename of the used video
        self.full_clip = None
        self.full_filename = None

        
    """
            [  F U N C T I O N A L I T Y  ]
    """
    def build(self):
        """
        Builds the segment files and returns the 'full_clip'.
        """
        print('Lets build it...')
        if self.type == 'meme':
            self.video_clip = self.__get_videoclip()
            self.full_clip = self.video_clip
        else:
            # TODO: I should handle manually written shortcodes and preserve them to add into
            # the transcription_text, but by now I'm just ignoring and removing them
            manual_shortcodes = handle_shortcodes(self.text)
            self.shortcodes = manual_shortcodes

            self.text = manual_shortcodes['text_without_shortcodes']
            db_project = get_project_by_id(self.project_id)

            # Look for audio narration filename if previously created
            if 'audio_filename' in db_project['segments'][self.segment_index] and self.__has_narration():
                print('Audio previously created and found in database. Reading it')
                self.audio_filename = db_project['segments'][self.segment_index]['audio_filename']
                self.audio_clip = AudioFileClip(self.audio_filename)
                self.calculated_duration = self.audio_clip.duration
            else:
                print('Generating audioclip as it has been not found in database')
                self.audio_clip = self.__get_audioclip()
                set_project_segment_audio_filename(self.project_id, self.segment_index, self.audio_filename)
            
            # Look for narration if previously handled
            if 'transcription' in db_project['segments'][self.segment_index] and self.__has_narration():
                print('Transcription previously created and found in database. Reading it')
                self.transcription = db_project['segments'][self.segment_index]['transcription']
            else:
                print('Generating transcription as it has been not found in database')
                self.transcription = self.__get_transcription()
                set_project_segment_transcription(self.project_id, self.segment_index, self.transcription)

            self.transcription_text = ''
            if self.transcription:
                for word in self.transcription:
                    self.transcription_text += word['text'] + ' '
                self.transcription_text = self.transcription_text.strip()
                # TODO: Maybe I should store this as 'self.transcription_text_with_shortcodes'
                # and handle the shortcodes from there, and also store it in database
                self.transcription_text = self.__insert_automated_shortcodes()

            shortcodes = handle_shortcodes(self.transcription_text)
            self.shortcodes = shortcodes['shortcodes_found']

            print(self.transcription_text)

            self.video_clip = self.__get_videoclip()
            # TODO: Do I really need the video clip? I have full_clip
            #from utils.mongo_utils import set_project_segment_video_filename
            #set_project_segment_video_filename(self.project_id, self.segment_index, self.transcription)
            self.full_clip = self.__get_fullclip()

            print('full clip duration pre everything')
            print(self.full_clip.duration)
            print('full clip audio duration pre everything')
            print(self.full_clip.audio.duration)

            # Then, with full_clip built, is time to process later elements

            # We could have some shortcodes that need to be processed and added
            self.effects += self.__extract_from_shortcodes(EnhancementType.EFFECT)
            self.full_clip = self.__apply_effects()

            print('full clip duration post effects')
            print(self.full_clip.duration)
            print('full clip audio duration post effects')
            print(self.full_clip.audio.duration)

            self.green_screens = self.__extract_from_shortcodes(EnhancementType.GREEN_SCREEN)
            self.full_clip = self.__apply_green_screens()

            print('full clip duration post green screens')
            print(self.full_clip.duration)
            print('full clip audio duration post green screens')
            print(self.full_clip.audio.duration)

            self.images = self.__extract_from_shortcodes(EnhancementType.IMAGE)
            self.full_clip = self.__apply_images()

            print('full clip duration post images')
            print(self.full_clip.duration)
            print('full clip audio duration post images')
            print(self.full_clip.audio.duration)

            self.stickers = self.__extract_from_shortcodes(EnhancementType.STICKER)
            self.full_clip = self.__apply_stickers()

            print('full clip duration post stickers')
            print(self.full_clip.duration)
            print('full clip audio duration post stickers')
            print(self.full_clip.audio.duration)

            self.sounds = self.__extract_from_shortcodes(EnhancementType.SOUND)
            self.full_clip = self.__apply_sounds()

            print('full clip duration post sounds')
            print(self.full_clip.duration)
            print('full clip audio duration post sounds')
            print(self.full_clip.audio.duration)

            self.memes = self.__extract_from_shortcodes(EnhancementType.MEME)
            self.full_clip = self.__apply_memes()
            
            # I apply memes at the end because they enlarge the video duration

            print('full clip duration post memes')
            print(self.full_clip.duration)
            print('full clip audio duration post memes')
            print(self.full_clip.audio.duration)

            #self.premades = self.__extract_premades_from_shortcodes()
            #self.full_clip = self.__apply_premades()
            
            # I apply premades at the end because they enlarge the video duration

            print('full clip duration post premades')
            print(self.full_clip.duration)
            print('full clip audio duration post premades')
            print(self.full_clip.audio.duration)

            self.full_clip = self.__fix_audio_glitch()

        # By now I only write the full clip and update it in database
        tmp_segment_full_filename = create_segment_filename('segment' + str(self.segment_index) + '.mp4')
        print('Audio file clip duration:')
        print(self.audio_clip.duration)
        print('Video file clip duration:')
        print(self.video_clip.duration)
        print('Full clip duration:')
        print(self.full_clip.duration)
        print('Full clip audio duration:')
        print(self.full_clip.audio.duration)
        self.full_clip.write_videofile(tmp_segment_full_filename)
        set_project_segment_full_filename(self.project_id, self.segment_index, tmp_segment_full_filename)
        set_project_segment_as_finished(self.project_id, self.segment_index)

        return self.full_clip

    def __get_shortcodes(self):
        """
        This method processes the received text looking for shortcodes, stores them
        and also cleans the text removing those shortcodes.

        This method returns the shortcodes.
        """
        if not self.shortcodes and self.__has_narration():
            if self.transcription:
                print_in_progress('Processing shortcodes (on transcription)')

                shortcodes = handle_shortcodes(self.transcription_text)
                #self.text = shortcodes['text_without_shortcodes']
                self.transcription_text = shortcodes['text_without_shortcodes']
                self.shortcodes = shortcodes['shortcodes_found']
                print_completed('Shortcodes processed = ' + str(len(self.shortcodes)) + '. Text cleaned')

        return self.shortcodes

    def __get_audioclip(self):
        """
        This method returns the 'audioclip' if existing, or generates it according
        to the other properties. It will also set 'audio_filename' and 
        'calculated_duration' fields that depend on this audio.
        """
        if not self.audio_clip:
            if self.audio_narration_filename:
                # 1. If 'audio_narration_filename'  ->  get audioclip from filename
                self.audio_filename = self.audio_narration_filename
                self.audio_clip = AudioFileClip(self.audio_narration_filename)
            elif self.text and self.voice:
                # 2. If 'text' and 'voice'  ->  get audioclip from generated narration
                print_in_progress('Creating voice narration of "' + self.text + '"')
                audio_filename = create_segment_filename('audio_filename.wav')
                #self.audio_filename = narrate(self.text, self.voice, audio_filename)
                self.audio_filename = generate_google_narration(self.text, output_filename = audio_filename)
                self.audio_clip = AudioFileClip(self.audio_filename)
                print_completed('Voice narration created successfully')
            elif self.duration:
                # 3. If 'duration'  ->  get audioclip from generated silence
                print_in_progress('Creating silence audioclip for silent segment')
                self.audio_filename = create_segment_filename('audio_filename.wav')
                create_silence_audio_file(self.duration, self.audio_filename)
                self.audio_clip = AudioFileClip(self.audio_filename)
                print_completed('Silent audio created successfully')

            # The audio is the one that determines the video length
            self.calculated_duration = self.audio_clip.duration

        return self.audio_clip

    def __get_transcription(self):
        """
        Returns the audio transcription if the segment is a narrated segment, or None
        if not.
        """
        if not self.transcription and (self.type == 'text' or self.__has_narration()):
            print_in_progress('Generating audio transcription')
            if self.audio_narration_filename:
                initial_prompt = None
                if self.text and len(self.text) > 0:
                    initial_prompt = self.text
                transcription = get_transcription_with_timestamps(self.audio_narration_filename, initial_prompt = initial_prompt)
            elif self.text and self.voice:
                transcription = get_transcription_with_timestamps(self.audio_filename, initial_prompt = self.text)

            # We join all words together as we don't need segments, just words with time
            words = []
            for transcription_segment in transcription['segments']:
                words += transcription_segment['words']
            self.transcription = words
            print_completed('Transcription obtained')

        return self.transcription
    
    def __get_videoclip(self):
        if not self.video_clip:
            # TODO: Create video according to type
            print_in_progress('Creating "' + self.type + '" video clip')
            if self.type == 'ia_image':
                self.video_clip = self.builder.build_ai_image_content_clip_from_segment(self)
            elif self.type == 'image':
                self.video_clip = self.builder.build_image_content_clip_from_segment(self)
            elif self.type == 'youtube_video':
                self.video_clip = self.builder.build_youtube_video_content_clip_from_segment(self)
            elif self.type == 'text':
                self.video_clip = self.builder.build_text_video_content_clip_from_segment(self)
            elif self.type == 'my_stock':
                self.video_clip = self.builder.build_my_stock_video_content_clip_from_segment(self)
            elif self.type == 'stock':
                self.video_clip = self.builder.build_stock_video_content_clip_from_segment(self)

            # Other types to create
            elif self.type == 'meme':
                # This can be None
                self.video_clip = self.builder.build_meme_content_clip_from_segment(self)

            # Custom easy premades below
            elif self.type == 'google_search':
                self.video_clip = self.builder.build_premade_google_search_from_segment(self)
            elif self.type == 'youtube_search':
                self.video_clip = self.builder.build_premade_youtube_search_from_segment(self)
            print_completed('Video content built successfully')

        # I force fps to 60fps because of some problems I found. We are working with those
        # 60fps everywhere, to also improve 'manim' animations, so force it
        self.video_clip = self.video_clip.set_fps(60)

        return self.video_clip

    def __apply_effects(self):
        """
        Applies the effects that we have to the full_clip that has been previously
        generated according to what the script said.

        We have main effects (written in 'effects' section in the script) and also
        shortcode effects that have been processed. The ones from the 'effects' 
        section are processed first, as are the "main" effects, and the ones from
        shortcodes are processed later.

        This method should be called after whole full_clip has been generated. As
        a reminder, the effects that we handle to this day, they should not modify
        the final clip duration as they are only aesthetic.
        """
        if self.effects:
            print_in_progress('Applying ' + str(len(self.effects)) + ' effects')
            self.full_clip = apply_effects(self.full_clip, self.effects)
            print_completed('All effects applied correctly')

        return self.full_clip
    
    def __apply_memes(self):
        if len(self.memes) > 0:
            index = 0
            while index < len(self.memes):
                meme = self.memes[index]
                video_filename = meme.download()
                if not video_filename:
                    # Remove any meme that was not found, we will ignore it
                    print_error('Meme "' + meme.keywords + '" not found, ignoring it')
                    del self.memes[index]
                else:
                    index += 1

        # Add all found green screens to our 'self.full_clip'
        if len(self.memes) > 0:
            print_in_progress('Applying ' + str(len(self.memes)) + ' memes')
            # Meme start is updated in 'apply_meme' method if 'inline' memes added
            self.full_clip = apply_memes(self.full_clip, self.memes)
            print_completed('All memes applied correctly')

        return self.full_clip

    def __apply_sounds(self):
        """
        This method will try to get the requested sounds (as shortcodes) from
        our sounds Youtube account and, if existing, download them and add the
        sound to the audioclip.
        """
        # 1. Process, download and ignore unavailable sounds
        if len(self.sounds) > 0:
            index = 0
            while index < len(self.sounds):
                sound: segments.building.objects.sound.Sound = self.sounds[index]
                audio_filename = sound.download()
                if not audio_filename:
                    # Remove any sound that was not found, we will ignore it
                    print_error('Sound "' + sound.keywords + '" not found, ignoring it')
                    del self.sounds[index]
                else:
                    index += 1

        # Add all found sounds to our 'self.audio_clip'
        if len(self.sounds) > 0:
            self.full_clip = self.full_clip.set_audio(apply_sounds(self.full_clip.audio, self.sounds))

        return self.full_clip
    
    def __apply_stickers(self):
        if len(self.stickers) > 0:
            index = 0
            while index < len(self.stickers):
                sticker: segments.building.objects.sticker.Sticker = self.stickers[index]
                print('( ( ( ) ) )  Downloading sticker "' + sticker.keywords + '"')
                video_filename = sticker.download()
                if not video_filename:
                    # Remove any sticker that was not found, we will ignore it
                    print_error('Sticker "' + sticker.keywords + '" not found, ignoring it')
                    del self.stickers[index]
                else:
                    index += 1

        # Add all found stickers to our 'self.full_clip'
        if len(self.stickers) > 0:
            print_in_progress('Applying ' + str(len(self.stickers)) + ' stickers')
            self.full_clip = apply_stickers(self.full_clip, self.stickers)
            print_completed('All stickers applied correctly')

        return self.full_clip

    def __apply_images(self):
        if len(self.images) > 0:
            index = 0
            while index < len(self.images):
                image: segments.building.objects.image.Image = self.images[index]
                video_filename = image.download()
                if not video_filename:
                    # Remove any image that was not found, we will ignore it
                    print_error('Image "' + image.keywords + '" not found, ignoring it')
                    del self.images[index]
                else:
                    index += 1

        # Add all found images to our 'self.full_clip'
        if len(self.images) > 0:
            print_in_progress('Applying ' + str(len(self.images)) + ' images')
            self.full_clip = apply_images(self.full_clip, self.images)
            print_completed('All images applied correctly')

        return self.full_clip
    
    def __apply_green_screens(self):
        if len(self.green_screens) > 0:
            index = 0
            while index < len(self.green_screens):
                green_screen: segments.building.objects.green_screen.GreenScreen = self.green_screens[index]
                video_filename = green_screen.download()
                if not video_filename:
                    # Remove any sound that was not found, we will ignore it
                    print_error('Green screen "' + green_screen.keywords + '" not found, ignoring it')
                    del self.green_screens[index]
                else:
                    index += 1

        # Add all found green screens to our 'self.full_clip'
        if len(self.green_screens) > 0:
            print_in_progress('Applying ' + str(len(self.green_screens)) + ' green screens')
            self.full_clip = apply_green_screens(self.full_clip, self.green_screens)
            print_completed('All green screens applied correctly')

        return self.full_clip
    
    def __fix_audio_glitch(self):
        """
        This method was built to try to fix the audio glitch that always come back when
        using moviepy. I'm trying to remove the last audio "frames" to avoid that 
        glitch. This is not nice, but I need to do something with that...

        I'm detecting the silences in the audio to ensure that the end has a silence, so
        I can remove a part of the end without removing important audio part.
        """
        audio = self.full_clip.audio
        # from yta_multimedia.sound.silences import detect_silences_in_audio_file
        # silences = detect_silences(self.audio_filename)
        # if len(silences) > 0 and (silences[len(silences) - 1][1] + 0.2) > self.audio_clip.duration:
        #     # If silence at the end of the audio, remove a little to avoid glitches
        #     FRAMES = 5    # 5 frames is for my testing narrate, don't calibrated for external
        #     audio = audio.subclip(0, self.audio_clip.duration - ((1 / 60) * FRAMES))
        audio = audio.subclip(0, -0.12)

        self.full_clip = self.full_clip.set_audio(audio)

        return self.full_clip
    
    def __get_fullclip(self):
        if not self.full_clip and self.audio_clip and self.video_clip:
            self.full_clip = self.video_clip.set_audio(self.audio_clip)

        return self.full_clip
    
    def write_fullclip(self, output_filename):
        """
        Writes the segment fullclip to t he 'output_filename'.
        """
        if self.full_clip:
            print_in_progress('Writing full clip as "' + output_filename + '"')
            self.full_clip.write_videofile(output_filename)
            self.full_filename = output_filename
            print_completed('Output file wrote successfully')

        return output_filename


    """
            [   M I D - T I M E     P R O C E S S I N G ]
    """
    def __extract_effects_from_shortcodes(self):
        """
        Detects our shortcodes, that should have been loaded previously, and extracts
        the 'effect' shortcodes (if existing), checking if valid and adding to our
        effects list to be (later) processed as well as script-written effects.
        """
        # We could have shortcodes that are effects. We will process those shortcodes
        # and add them to our effects list.

        # We only accept effect shortcodes if there is a transcription that we
        # need to adjust shortcodes timing
        if self.transcription:
            if self.shortcodes and (len(self.shortcodes) > 0):
                for shortcode in self.shortcodes:
                    try:
                        keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
                        meme = segments.building.objects.meme.Meme(keywords, start, duration, origin, mode)
                        print_in_progress('Adding "' + meme.keywords + '" meme')
                        self.memes.append(meme)
                    except Exception as e:
                        print(e)
                        print_error('Failed instantiating meme ' + keywords)
                        continue

        return self.effects
    
    def __parse_enhancement_type_fields(self, shortcode):
        """
        This method is only for internal use and has been created to allow
        reusing this method of segment enhancement object fields extraction.
        """
        word_index = int(shortcode['previous_word_index'])
        word = self.transcription[word_index]

        print(shortcode)

        keywords = shortcode[EnhancementField.KEYWORDS.value]
        start = shortcode[EnhancementField.START.value]
        duration = shortcode[EnhancementField.DURATION.value]
        origin = shortcode[EnhancementField.ORIGIN.value]
        mode = shortcode[EnhancementField.MODE.value]

        # start
        if start == Start.START_OF_CURRENT_WORD.value:
            start = word['start']
        elif start == Start.END_OF_CURRENT_WORD.value:
            # The end of the segment but also start at 'end'? Not good
            # TODO: Special case
            start = word['end']
        elif start == Start.BEFORE_NEXT_WORD.value:
            if (word_index + 1) < len(self.transcription):
                # Between the word and the next one, in the silence gap in between
                start = (self.transcription[word_index + 1]['end'] + self.transcription[word_index + 1]['start']) / 2
            else:
                # The end of the segment but also start at 'end'? Not good
                # TODO: Special case
                if mode == Mode.INLINE.value:
                    start = self.full_clip.duration
                else:
                    start = word['end']

        # duration
        if duration == Duration.END_OF_CURRENT_WORD.value:
            duration = word['end'] - start
        elif duration == Duration.FILE_DURATION.value:
            if mode == Mode.INLINE.value:
                duration = Constants.FILE_DURATION.value
            else:
                # This is the maximum as it will be overlayed
                duration = self.full_clip.duration - start
        elif duration.startswith(Duration.END_OF_SUBSEQUENT_WORD.value):
            aux = duration.split('_')
            subsequent_word_index = int(aux[len(aux) - 1])

            if (word_index + subsequent_word_index) < (len(self.transcription) - 1):
                duration = self.transcription[word_index + subsequent_word_index]['end'] - start
            else:
                # TODO: Special case
                # Asking for the end of the segment, so lets use the segment end
                duration = self.full_clip.duration - start
        else:
            # By now, only float value
            duration = float(duration)

        # Special cases:
        # - End of segment
        # if word_index == len(self.transcription) - 1
        #   if inline => 

        return keywords, start, duration, mode, origin

    def __extract_memes_from_shortcodes(self):
        # We only accept these shortcodes if there is the text is narrated
        if self.transcription:
            if self.shortcodes and (len(self.shortcodes) > 0):
                for shortcode in self.shortcodes:
                    # Any shortcode has 'shortcode' and 'previous_word_index'
                    # green screen shortcode also should have 'keywords' and 'duration'
                    if shortcode['shortcode'] == 'meme':
                        # Options:
                        #   Inline meme with no duration
                        #   Inline meme with duration as end_of_word:X (non-sense, I think)
                        #   Inline meme with duration as 3
                        #   Inline meme with duration as video_duration
                        #
                        #   Overlay meme with no duration
                        #   Overlay meme with duration as end_of_word:X
                        #   Overlay meme with duration as 3
                        #   Overlay meme with duration as video_duration (non-sense, I think)
                        try:
                            keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
                            meme = segments.building.objects.meme.Meme(keywords, start, duration, origin, mode)
                            print_in_progress('Adding "' + meme.keywords + '" meme')
                            self.memes.append(meme)
                        except Exception as e:
                            print(e)
                            print_error('Failed instantiating meme ' + keywords)
                            continue
                    
        return self.memes
    
    def __extract_stickers_from_shortcodes(self):
        # We only accept these shortcodes if there is the text is narrated
        if self.transcription:
            if self.shortcodes and (len(self.shortcodes) > 0):
                for shortcode in self.shortcodes:
                    # Any shortcode has 'shortcode' and 'previous_word_index'
                    # green screen shortcode also should have 'keywords' and 'duration'
                    if shortcode['shortcode'] == 'sticker':
                        try:
                            keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
                            sticker = segments.building.objects.sticker.Sticker(keywords, start, duration, origin, mode)
                            print_in_progress('Adding "' + sticker.keywords + '" sticker')
                            self.stickers.append(sticker)
                        except Exception as e:
                            print(e)
                            print_error('Failed instantiating sticker ' + keywords)
                            continue
                    
        return self.stickers
    
    def __extract_images_from_shortcodes(self):
        # We only accept these shortcodes if there is the text is narrated
        if self.transcription:
            if self.shortcodes and (len(self.shortcodes) > 0):
                for shortcode in self.shortcodes:
                    # Any shortcode has 'shortcode' and 'previous_word_index'
                    # green screen shortcode also should have 'keywords' and 'duration'
                    if shortcode['shortcode'] == 'image':
                        try:
                            keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
                            sticker = segments.building.objects.image.Image(keywords, start, duration, origin, mode)
                            print_in_progress('Adding "' + sticker.keywords + '" sticker')
                            self.stickers.append(sticker)
                        except Exception as e:
                            print(e)
                            print_error('Failed instantiating image ' + keywords)
                            continue
                    
        return self.images

    def __extract_green_screens_from_shortcodes(self):
        # We only accept these shortcodes if there is the text is narrated
        if self.transcription:
            if self.shortcodes and (len(self.shortcodes) > 0):
                for shortcode in self.shortcodes:
                    # Any shortcode has 'shortcode' and 'previous_word_index'
                    # green screen shortcode also should have 'keywords' and 'duration'
                    if shortcode['shortcode'] == 'green_meme':
                        try:
                            keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
                            sticker = segments.building.objects.sticker.Sticker(keywords, start, duration, origin, mode)
                            print_in_progress('Adding "' + sticker.keywords + '" sticker')
                            self.stickers.append(sticker)
                        except Exception as e:
                            print(e)
                            print_error('Failed instantiating sticker ' + keywords)
                            continue
                    
        return self.green_screens
    
    def __extract_from_shortcodes(self, type: EnhancementType):
        objects = []
        if self.transcription:
            if self.shortcodes and (len(self.shortcodes) > 0):
                for shortcode in self.shortcodes:
                    # Any shortcode has 'shortcode' and 'previous_word_index'
                    # sound shortcode also should have 'keywords' and 'duration'
                    if shortcode['shortcode'] == type.value:
                        try:
                            keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
                            # TODO: Do this dynamically calling object
                            if type == EnhancementType.GREEN_SCREEN:
                                object = segments.building.objects.green_screen.GreenScreen(keywords, start, duration, origin, mode)
                            elif type == EnhancementType.MEME:
                                object = segments.building.objects.meme.Meme(keywords, start, duration, origin, mode)
                            elif type == EnhancementType.SOUND:
                                object = segments.building.objects.sound.Sound(keywords, start, duration, origin, mode)
                            elif type == EnhancementType.IMAGE:
                                object = segments.building.objects.image.Image(keywords, start, duration, origin, mode)
                            elif type == EnhancementType.STICKER:
                                object = segments.building.objects.sticker.Sticker(keywords, start, duration, origin, mode)
                            elif type == EnhancementType.EFFECT:
                                object = segments.building.objects.effect.Effect(keywords, start, duration, origin, mode, {})

                            print_in_progress('Adding "' + object.keywords + '" ' + type.value + '"')
                            objects.append(object)
                        except Exception as e:
                            print(e)
                            print_error('Failed instantiating ' + type.value + ' ' + keywords)
                            continue

        return objects
    
    def __extract_sounds_from_shortcodes(self):
        # We only accept these shortcodes if there is the text is narrated
        if self.transcription:
            if self.shortcodes and (len(self.shortcodes) > 0):
                for shortcode in self.shortcodes:
                    # Any shortcode has 'shortcode' and 'previous_word_index'
                    # sound shortcode also should have 'keywords' and 'duration'
                    if shortcode['shortcode'] == 'sound':
                        try:
                            keywords, start, duration, mode, origin = self.__parse_enhancement_type_fields(shortcode)
                            sound = segments.building.objects.sound.Sound(keywords, start, duration, origin, mode)
                            print_in_progress('Adding "' + sound.keywords + '" sound')
                            self.sounds.append(sound)
                        except Exception as e:
                            print(e)
                            print_error('Failed instantiating sound ' + keywords)
                            continue

        return self.sounds

    """
            [   M I N O R     C H E C K S  ]
    """
    def __has_narration(self):
        """
        Returns true if this segment has a narration (by file or by voice generation).
        """
        return self.audio_narration_filename or (self.text and self.voice)

    """
            [   V A L I D A T I O N  ]
    """
    def __check_structure_is_valid(self, json):
        # This will raise an Exception if not valid
        self.segment_validator.validate(json)

    """
            [   O T H E R S   ]
    """

    def __insert_automated_shortcodes(self):
        """
        Appends the automated shortcodes (banning, enhancement, etc.) to the transcripted
        text to enhanced the video.
        """
        from utils.narration_script.enhancer import get_shortcodes_by_word_index

        # 1. Apply enhancement words (including censorship)
        shortcodes_by_word_index = get_shortcodes_by_word_index(self.transcription)
        print(self.transcription_text)
        text_as_words = self.transcription_text.split(' ')
        for key in shortcodes_by_word_index:
            text_as_words[int(key)] += ' ' + shortcodes_by_word_index[key]
        self.transcription_text = ' '.join(text_as_words)
        print(self.transcription_text)

        # 2. Check double or triple (or more) consecutive blank spaces and remove again
        print_in_progress('Fixing excesive blank spaces')
        self.transcription_text = self.__fix_excesive_blank_spaces(self.transcription_text)
        print_completed('Excesive blank spaces fixed')

        print(self.transcription_text)

        return self.transcription_text

    def __check_script_text(self):
        """
        Checks if the existing text is well written (shortcodes can be processed well),
        applies a censorship sound to banned words and enhaces words to enhance  with 
        some specific strategies (if active).
        """
        if self.__has_narration():
            # 1. Check double or triple (or more) consecutive blank spaces and remove
            print_in_progress('Fixing excesive blank spaces')
            self.text = self.__fix_excesive_blank_spaces(self.text)
            print_completed('Excesive blank spaces fixed')

            """
            # No shortcodes available in text by now

            # 2. Check shortcodes are processable
            print_in_progress('Fixing shortcodes')
            self.text = self.__fix_text_shortcodes()
            print_completed('Shortcodes fixed')

            # 3. Censor bad words (with censorship sound)
            if DO_BAN_WORDS:
                print_in_progress('Processing banned words')
                self.text = self.__process_banned_words()
                print_completed('Banned words processed')

            # 4. Enhance content by adding shortcodes next to words in our dictionary
            if DO_ENHANCE_WORDS:
                print_in_progress('Processing enhanced words')
                self.text = self.__process_enhanced_words()
                print_completed('Enhanced words processed')

            # 5. Check double or triple (or more) consecutive blank spaces and remove again
            print_in_progress('Fixing excesive blank spaces')
            self.text = self.__fix_excesive_blank_spaces()
            print_completed('Excesive blank spaces fixed')

            print('@@ == >   Text that will be processed...')
            print(self.text)
            """

        return self.text
        
    # TODO: Import this from 'yta-general-utils' when available
    def __fix_excesive_blank_spaces(self, text):
        """
        Removed blank spaces longer than 1 from the provided 'text' and returns it clean.
        """
        # TODO: Ok, why am I using not the 'repl' param in re.search?
        # I'm applying it in the new method below, please check if
        # valid to avoid the while, thank you
        filtered = re.search('[ ]{2,}', text)
        while filtered:
            index_to_replace = filtered.end() - 1
            s = list(text)
            s[index_to_replace] = ''
            text = ''.join(s)
            filtered = re.search('[ ]{2,}', text)

        return text
    
    # TODO: Import this from 'yta-general-utils' when available
    def __fix_unseparated_periods(self, text):
        """
        This methods fixes the provided 'text' by applying a space
        after any period without it.
        """
        # Thank you: https://stackoverflow.com/a/70394076
        return re.sub(r'\.(?!(?<=\d\.)\d) ?', '. ', text)

    def __fix_text_shortcodes(self):
        """
        Checks the segment text and fixes the shortcodes that won't be processable.
        This means those shortcodes that end with ']x' when 'x' is not a blank
        space.
        """
        if self.text:
            filtered = re.search('][^ ]', self.text)
            while filtered:
                index_to_replace = filtered.end() - 1
                s = list(self.text)
                s[index_to_replace] = '' # I will delete that 'no white space char', sorry
                self.text = ''.join(s)
                filtered = re.search('][^ ]', self.text)

        return self.text

    def __check_and_format_effects(self, json):
        """
        This method checks if the provided effects are valid and also transform those
        json effects into 'Effect' objects that are stored in self.effects to process
        them better lately.

        This method is for the effects that comes in the script, not as shortcodes. 
        The ones in shortcodes will be processed later.
        """
        self.effects = []
        if 'effects' in json and (len(json['effects']) > 0):
            object_effects = []
            for effect in json['effects']:
                print_in_progress('Adding "' + effect['effect'] + '" effect')
                # TODO: Implement 'sound' parameter
                #object_effects.append(segments.building.objects.effect.Effect(effect['effect'], effect.get('start'), effect.get('end'), effect.get('sound', True), effect.get('parameters', {})))
                # TODO: Careful with 'start' and 'end'
                from segments.building.objects.enums import Origin, Mode
                object_effects.append(segments.building.objects.effect.Effect(effect['effect'], effect.get('start'), effect.get('end'), Origin.DEFAULT.value, Mode.DEFAULT.value, effect.get('parameters', {})))

            self.effects = object_effects

        return self.effects