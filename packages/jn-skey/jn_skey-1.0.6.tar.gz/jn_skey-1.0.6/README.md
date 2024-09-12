
# jn-skey

**jn-skey** is a Python command-line tool that allows you to quickly insert the current date and time into any text field by using a customizable keyboard shortcut. This tool is particularly useful for those who need to timestamp entries frequently.

## Features

- Insert the current date and time in the format `YYYY-MM-DD hh:mm:ss`.
- Configurable keyboard shortcut for triggering the insertion.
- Lightweight and easy to use.

## Installation

You can install **jn-skey** via `pip`. To do so, run:

```bash
pip install jn-skey
```

## Usage

After installation, you can run the `jn-skey` command from your terminal. Once running, the tool listens for a specific keyboard shortcut to insert the current date and time.

### Default Keyboard Shortcut

The default keyboard shortcut is:

```
SHIFT + ALT + *
```

When this combination is pressed, the current date and time in the format `YYYY-MM-DD hh:mm:ss` will be typed out at the cursor's position.

### Running the Command

To start the tool, simply open a terminal and run:

```bash
jn-skey
```

The tool will output a message indicating that it is listening for the keyboard shortcut.

### Example

```text
SHORTCUT KEY FOR YYYY-MM-DD hh:mm:ss IS SHIFT + ALT + * (main keyboard)
```

Pressing `SHIFT + ALT + *` will then type something like:

```text
2024-09-06 12:45:30
```

## Requirements

- Python 3.6 or higher
- pynput library (automatically installed with the package)

## Contributing

Contributions are welcome! If you'd like to improve this package, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact me at `your.email@example.com`.

## Acknowledgments

- [pynput](https://pypi.org/project/pynput/) - Used for keyboard event handling.
