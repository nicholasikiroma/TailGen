# TailGen

TailGen is a command-line interface (CLI) tool designed to simplify the process of generating Flask or FastAPI projects with Tailwind CSS integration. With TailGen, you can quickly set up a new web application project with the necessary files and directory structures, saving you time and effort in the initial setup phase.

## Features

- **Virtual Environment Management**: Automatically create a virtual environment for your project and downloads Python dependencies within the `venv` folder, ensuring isolated dependencies.
  
- **Template Generation**: Generates Flask or FastAPI project templates with Tailwind CSS integration, including directory structures and starter code.

- **Cross-Platform Compatibility**: Works seamlessly on both Windows and Unix-like systems, providing a consistent experience for all users.

- **Git initialization**

## Prerequisites

Before using TailGen, ensure you have the following installed on your system:

- Python 3
- Node.js (for Tailwind CSS integration)

## Installation

You can install TailGen using pip:

```bash
pip install tailgen
```

## Usage

To use TailGen, follow these steps:

1. Navigate to your project directory or specify the path to it.

2. Run the following command to generate the project templates:

   ```bash
   tailgen init
   ```

3. Run the following commands to see the options available for the `init` command:

```bash
tailgen init --help
```

## Contributing

Contributions to TailGen are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
