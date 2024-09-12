# Spangled's Download Manager

**Spangled's Download Manager (SDLM)** is a lightweight command-line tool for downloading files from `fuckingfast.co`. It supports both manual URL input and batch downloads from a file, providing a simple yet effective solution for your downloading needs.

## Features

- **Simple Command-Line Interface:** Easy to use with a single `sdlm` command.
- **Automatic Folder Creation:** Automatically creates a `downloads` folder for your files.
- **Two Input Modes:**
  - **Manual Input:** Type URLs directly into the command line.
  - **Reading from File:** Read URLs from a `downloads.txt` file for downloading batches of files.
- **Progress Bar:** Displays a progress bar for each download to track its completion.

## Installation

To install SDLM, you'll need Python and pip (Python's package installer). If you have Python installed, pip is typically included.

Run the following command to install SDLM:

```shell
pip install sdlm
```

# Spangled's Download Manager

**Spangled's Download Manager (SDLM)** is a lightweight command-line tool for downloading files from `fuckingfast.co`. It supports both manual URL input and batch downloads from a file, providing a simple yet effective solution for your downloading needs.

## Features

- **Simple Command-Line Interface:** Easy to use with a single `sdlm` command.
- **Automatic Folder Creation:** Automatically creates a `downloads` folder for your files.
- **Two Input Modes:**
  - **Manual Input:** Type URLs directly into the command line.
  - **Read from File:** Read URLs from a `downloads.txt` file for batch downloading.
- **Progress Bar:** Displays a progress bar for each download to track its completion.

## Installation

To install SDLM, you'll need Python and pip (Python's package installer). If you have Python installed, pip is typically included.

Run the following command to install SDLM:

```shell
pip install sdlm
```

# Usage

After installing, you can start using SDLM by simply typing sdlm in your terminal:

```shell
sdlm
```
Download Modes

    Manual Input Mode:
        When prompted, type input and press Enter.
        You will be prompted to enter URLs one by one.
        Press Enter without typing a URL to stop inputting and start downloading.

    Read from File Mode:
        When prompted, type read and press Enter.
        SDLM will read URLs from a downloads.txt file located in the same directory.
        Make sure your downloads.txt file contains one URL per line.

Example downloads.txt File:
```shell
https://fuckingfast.co/file1
https://fuckingfast.co/file2
https://fuckingfast.co/file3
```

Notes

    The tool currently only supports links from fuckingfast.co.
    Ensure you have a stable internet connection for uninterrupted downloads.
    SDLM will automatically append .zip to the extension of every file it downloads.

Why Use SDLM?

While there are many alternatives out there, SDLM offers a straightforward, no-frills approach to downloading files. It’s perfect for those who prefer simplicity and a minimalist command-line experience.

# Contributing

Feel free to fork this repository and submit pull requests. Any contributions, improvements, or suggestions are welcome!

# License

This project is licensed under the GPL-3.0 License.
