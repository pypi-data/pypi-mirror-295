# Wav2Lip Package

Wav2Lip is a Python package that simplifies the setup and execution of the [Wav2Lip](https://github.com/anothermartz/Easy-Wav2Lip) model, a deep learning tool for lip synchronization with enhanced quality options.

```
wav2lip_project/
├── wav2lip/
│   ├── __init__.py
│   └── wav2lip.py  # Refactored class-based script with the correct name
├── pyproject.toml  # Poetry configuration file
├── README.md  # Project description and usage instructions
├── LICENSE  # License file (e.g., MIT License)
├── tests/
│   └── test_wav2lip.py  # Unit tests for the package
├── dist/  # Will contain build files after 'poetry build'
├── .gitignore  # Files to ignore in version control (optional)
└── setup.cfg  # Optional: You can include a setup.cfg for backward compatibility
```

## Features

 setup for Google Colab environments.
- Supports multiple quality settings (Fast, Improved, Enhanced).
- Integrated with GFPGAN for face upscaling.
- Easy configuration through INI files for customizable options.

## Installation

To install the Wav2Lip package, you can use [Poetry](https://python-poetry.org/) to manage dependencies.

```bash
pip install wav2lip
```

## Usage

Here's an example of how to use the `Wav2Lip` package:

```python
from wav2lip.wav2lip import Wav2Lip

# Initialize Wav2Lip
wav2lip = Wav2Lip()

# Setup environment (ensure that you have GPU enabled)
wav2lip.setup()

# Run the model with video and audio input
wav2lip.run(video_file="/content/your_video.mp4", vocal_file="/content/your_audio.wav")
```

### Options

You can specify different options for the model, such as:

- **Quality**: `"Fast"`, `"Improved"`, or `"Enhanced"`.
- **Output Height**: `"half resolution"`, `"full resolution"`, or `"480"`.
- **Padding and Mask**: Customize mouth tracking, padding, and mask settings.

## Contributing

Feel free to open issues or contribute by submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
