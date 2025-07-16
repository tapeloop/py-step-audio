# Py-Step-Audio

[![PyPI - Version](https://img.shields.io/pypi/v/py-step-audio.svg)](https://pypi.org/project/py-step-audio)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/py-step-audio.svg)](https://pypi.org/project/py-step-audio)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## About

`py-step-audio` is a Python package designed to facilitate the creation of audio files that can be used in step sequencers. It provides a simple interface for generating audio files with various parameters, making it easy to create custom sounds for music production.

## Features
- Generate audio files for step sequencers
- Create wrapped sequncers around single samples

## Usage

To use `py-step-audio`, you can import it in your Python script and call the `sample` function to generate an audio file. Here's a basic example:

```python py-step-audio sample.wav```

This will startup a step sequencer with a single sample and generate an audio file named `sample.wav` in the current directory.

## Installation

```console
pip install py-step-audio
```

## License

`py-step-audio` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
