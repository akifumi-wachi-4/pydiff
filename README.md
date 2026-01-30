# Python Diff Tool 📝

A modern, web-based text difference comparison tool built with Python and FastAPI. This tool allows you to compare two texts side by side and visualize their differences with syntax highlighting.

This repository is based on [meso-cacase/difff](https://github.com/meso-cacase/difff), a Perl-based text difference tool. This Python implementation provides the same functionality with a modern web framework.

## Installation & Setup 🚀

### Prerequisites
- Python 3.12 or higher
- uv

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd difff-python
   ```

2. **Install dependencies using UV (recommended)**
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   uv run python main.py
   ```

4. **Open your browser**
   Navigate to `http://127.0.0.1:8000` to use the diff tool

## Usage 💻

1. **Enter Text**: Paste or type your text in the left and right text areas
2. **Compare**: Click the "🔍 Compare" button to generate the difference analysis
3. **View Results**: The differences will be highlighted in a table format below
4. **Statistics**: View detailed statistics about character counts, spaces, line breaks, and words
5. **Customize**: Use the color theme selector to change the highlighting colors

## Dependencies 📦

- `fastapi>=0.128.0` - Modern web framework
- `jinja2>=3.1.6` - Template engine
- `python-multipart>=0.0.21` - Form data handling
- `uvicorn>=0.40.0` - ASGI server
- `ruff>=0.14.13` - Code linting and formatting

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This application is based on [difff](https://github.com/meso-cacase/difff), which is licensed under the 2-Clause BSD License.

## Support 💬

If you encounter any issues or have suggestions for improvements, please open an issue on GitHub.
