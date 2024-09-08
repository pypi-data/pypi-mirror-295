import os
import sys
import time
import torch
import warnings
import configparser
from google.colab import drive
from wyn_wav2lip.easy_functions import format_time, autoplay_video

class Wav2Lip:
    def __init__(self, version: str = 'v8.3'):
        self.version = version
        self.working_directory = None
        self.start_time = None

    def setup(self):
        """Perform the setup for Wav2Lip."""
        self._check_installation()
        self._check_gpu()
        self._mount_google_drive()
        self._start_timer()
        self._clone_git_repo()
        self._install_dependencies()
        print("Setup complete, ready to run the model.")

    def _check_installation(self):
        """Check if Wav2Lip is already installed."""
        if os.path.exists('installed.txt'):
            with open('last_file.txt', 'r') as file:
                last_file = file.readline()
            if last_file == self.version:
                sys.exit(f'Wav2Lip {self.version} has already been run on this instance!')

    def _check_gpu(self):
        """Ensure GPU is available."""
        print('Checking for GPU...')
        if not torch.cuda.is_available():
            sys.exit('No GPU in runtime. Please go to the "Runtime" menu, "Change runtime type" and select "GPU".')

    def _mount_google_drive(self):
        """Mount Google Drive for file access."""
        print('Requesting Google Drive access...')
        try:
            drive.mount('/content/drive')
        except:
            print("Google Drive not linked")

    def _start_timer(self):
        """Start a timer to measure setup time."""
        self.start_time = time.time()

    def _clone_git_repo(self):
        """Clone the Wav2Lip repository."""
        giturl = 'https://github.com/anothermartz/Easy-Wav2Lip.git'
        os.system(f'git clone -b {self.version} {giturl}')
        os.chdir('Easy-Wav2Lip')
        self.working_directory = os.getcwd()
        os.makedirs('face_alignment', exist_ok=True)
        os.makedirs('temp', exist_ok=True)

    def _install_dependencies(self):
        """Install necessary dependencies."""
        print('Installing batch_face...')
        warnings.filterwarnings("ignore", category=UserWarning, module='torchvision.transforms.functional_tensor')
        os.system('pip install batch_face --quiet')
        os.system('pip install basicsr==1.4.2 --quiet')
        print('Fixing basicsr degradations.py...')
        os.system('cp /content/Easy-Wav2Lip/degradations.py /usr/local/lib/python3.10/dist-packages/basicsr/data/degradations.py')
        print('Installing gfpgan...')
        os.system('pip install gfpgan --quiet')
        os.system('python install.py')

    def finish_setup(self):
        """Finish the setup and display elapsed time."""
        elapsed_time = time.time() - self.start_time
        print(f"Execution time: {format_time(elapsed_time)}")

    def run(self, video_file: str, vocal_file: str = "", quality: str = "Enhanced",
            output_height: str = "full resolution", use_previous_tracking_data: bool = True,
            wav2lip_version: str = "Wav2Lip", nosmooth: bool = True, U: int = 0, D: int = 10, L: int = 0, R: int = 0,
            size: float = 1.5, feathering: int = 1, mouth_tracking: bool = False, debug_mask: bool = False,
            batch_process: bool = False, output_suffix: str = "_Wav2Lip", include_settings_in_suffix: bool = False,
            preview_input: bool = False, preview_settings: bool = False, frame_to_preview: int = 100):
        """Run the Wav2Lip model."""
        if not os.path.exists('installed.txt'):
            sys.exit('Setup has not been completed! Please run the setup first.')

        # Prepare options
        options = {
            'video_file': video_file,
            'vocal_file': vocal_file,
            'quality': quality,
            'output_height': output_height,
            'wav2lip_version': wav2lip_version,
            'use_previous_tracking_data': use_previous_tracking_data,
            'nosmooth': nosmooth
        }

        padding = {'U': U, 'D': D, 'L': L, 'R': R}

        mask = {
            'size': size,
            'feathering': feathering,
            'mouth_tracking': mouth_tracking,
            'debug_mask': debug_mask
        }

        other = {
            'batch_process': batch_process,
            'output_suffix': output_suffix,
            'include_settings_in_suffix': include_settings_in_suffix,
            'preview_input': preview_input,
            'preview_settings': preview_settings,
            'frame_to_preview': frame_to_preview
        }

        # Write configuration to file
        config = configparser.ConfigParser()
        config['OPTIONS'] = options
        config['PADDING'] = padding
        config['MASK'] = mask
        config['OTHER'] = other

        with open('config.ini', 'w') as config_file:
            config.write(config_file)

        # Run the model
        os.system('python run.py')

        # Display the result
        if preview_settings:
            preview_image = os.path.join('temp', 'preview.jpg')
            if os.path.isfile(preview_image):
                from IPython.display import Image
                display(Image(preview_image))
        else:
            output_video = os.path.join('temp', 'output.mp4')
            if os.path.isfile(output_video):
                print(f"Loading video preview...")
                autoplay_video(output_video)
