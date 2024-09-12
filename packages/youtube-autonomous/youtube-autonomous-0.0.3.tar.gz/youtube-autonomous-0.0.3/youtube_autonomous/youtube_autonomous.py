from yta_general_utils.tmp_processor import clean_tmp_folder
from yta_general_utils.file_processor import get_project_abspath, create_file_abspath, read_json_from_file
from yta_general_utils.logger import print_completed
from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.segments.validation.segment_validator import SegmentValidator

class YoutubeAutonomous:
    __database_handler: DatabaseHandler = None
    """
    Object to interact with the database and get and create projects.
    """
    __segment_validator: SegmentValidator = None
    """
    Object to validate the segments we want to use to build a project.
    """

    def __init__(self, segments_abspath: str):
        """
        Initializes the object by creating the segments files folder
        in the provided 'segments_abspath' if it doesn't exist. This
        parameter, if not provided, will make the folder be created
        in the current project main folder with 'segments_files' 
        folder name.
        """
        self.__database_handler = DatabaseHandler()
        self.__segment_validator = SegmentValidator()

        if not segments_abspath:
            segments_abspath = get_project_abspath() + 'segments_files'
        
        # TODO: Do some checkings about the provided abspath
        self.segments_abspath = segments_abspath
        # We force to create the folder if it doesn't exist
        create_file_abspath(self.segments_abspath + 'toforce')

    def purge(self, do_remove_segments_files = False):
        """
        Cleans the temporary folder removing all previous generated 
        temporary files, and also the segment files if the
        'do_remove_segments_files' parameter is set to True.
        """
        clean_tmp_folder()
        if do_remove_segments_files:
            # TODO: Remove all files in self.segments_abspath folder
            pass

    def check_config(self):
        # TODO: Check that he config is ok
        pass

    

    def insert_project_in_database_from_file(self, filename: str):
        """
        Reads the provided project content 'filename' and creates a new 
        project in the database if the provided 'filename' contains a new
        project and is valid. If the information belongs to an already
        registered project, it will raise an exception.

        This method returns the new stored project mongo ObjectId if 
        successfully stored, or raises an Exception if anything went wrong.
        """
        if not filename:
            raise Exception('We need a project content "filename" to create a new project.')

        json_data = read_json_from_file(filename)

        # If a project with the same content exists, it is the same project
        db_project = self.__database_handler.get_database_project_from_json(json_data)
        if db_project:
            raise Exception('There is an existing project in the database with the same content.')

        # We validate each segment to be able to store the project
        for segment in json_data['segments']:
            self.__segment_validator.validate(segment)

        db_project = self.__database_handler.insert_project(json_data)

        print_completed('Project created in database with ObjectId = "' + str(db_project['_id']) + '"')

        return str(db_project['_id'])

    