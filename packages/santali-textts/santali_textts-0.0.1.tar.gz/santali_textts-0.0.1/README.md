# Text-to-Speech Program

## Overview

This is a simple Text-to-Speech (TTS) program developed in Python. Currently, it has been trained on a limited set of words, and it's designed to convert text input into speech output.

## Features

- Converts text to speech using a basic trained model.
- Limited vocabulary at present; additional training is required for broader language support.

## Requirements

Python 3.8 is required for this package.

## Installation

```
pip install santali_textts
```

## Usage

1. **Train the Model (Optional):**

   Custom Vocabulary: Currently trained with a limited set of words, including: ᱟᱵᱩ, ᱵᱟᱝ, ᱫᱚᱱ, ᱫᱟᱨ, ᱦᱟᱨᱩᱵ, ᱦᱮᱡᱳ, ᱦᱮᱱᱤ, ᱡᱟᱯᱮᱰ, ᱡᱚᱢ, ᱡᱳᱛᱳ, ᱠᱳᱢ, ᱞᱟᱱᱟ, ᱢᱟᱨᱟᱱᱜ, ᱢᱩᱪᱟ.

2. **Run the Program:**

    ```bash
    from santali_textts import santali_audio

    text = "ᱟᱵᱩ ᱵᱟᱝ ᱫᱚᱱ ᱫᱟᱨ ᱦᱟᱨᱩᱵ ᱦᱮᱡᱳ ᱦᱮᱱᱫᱤ ᱡᱟᱯᱮᱰ ᱡᱚᱢ ᱡᱳᱛᱳ ᱠᱳᱢ ᱞᱟᱱᱫᱟ ᱢᱟᱨᱟᱱᱜ ᱢᱩᱪᱟ"
    output_filename = "output_audio.wav"
    santali_audio(text, output_filename)

    ```

3. **Play the Output:**

   The output will be saved as an audio file in the specified output directory. You can play it using any standard audio player.

## Contributing

Feel free to contribute to the project by submitting pull requests or opening issues. If you have suggestions for improvements or additional features, your input is welcome!




