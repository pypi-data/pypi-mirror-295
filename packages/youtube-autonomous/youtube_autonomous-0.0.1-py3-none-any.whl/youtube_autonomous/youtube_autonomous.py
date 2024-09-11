from yta_general_utils.tmp_processor import clean_tmp_folder
from yta_general_utils.file_processor import get_project_abspath, create_file_abspath

class YoutubeAutonomous:
    def __init__(self, segments_abspath: str):
        """
        Initializes the object by creating the segments files folder
        in the provided 'segments_abspath' if it doesn't exist. This
        parameter, if not provided, will make the folder be created
        in the current project main folder with 'segments_files' 
        folder name.
        """
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
    