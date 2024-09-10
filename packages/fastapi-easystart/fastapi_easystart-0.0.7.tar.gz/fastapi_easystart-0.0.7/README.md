# FastAPI EasyStart

FastAPI EasyStart is a streamlined library designed to help developers quickly set up and configure a FastAPI project with essential components. It simplifies the process of creating APIs by providing ready-to-use templates and configurations for common tasks such as authentication, database integration, and CORS settings.


## Features

- 🚀 Quick Start Templates: Get started with FastAPI in seconds using predefined project structures and configurations.
- 🔧 Environment Management: Easily manage environment variables and settings.
- 🌍 CORS Configuration: Simplify CORS setup with built-in configurations.
- 📦 Modular Components: Use only what you need with modular and customizable components.
- 💡 Custom Exception Classes: Enhance error handling with predefined, customizable exception classes tailored for FastAPI.
- 🔐 Authentication: Easily integrate JWT-based authentication. (Coming Soon)
- 💾 Database Support: Seamless integration with popular databases like SQLite, PostgreSQL, and MongoDB. (Coming Soon)

## Installation

You can install the fastapi-easystart package using either pip or pipenv:

```bash
pip install fastapi-easystart
```

## Quickstart

### 1. Initialize a New FastAPI Project
Begin by creating a new FastAPI project with the default settings and configurations. Run the following command:
```bash
python -m  fastapi_easystart.main init
```
This command will generate the basic project structure, including directories and initial files, based on the easy start template.

### 2. Configure the main.py File
After initializing your project, configure the main.py file to set up the FastAPI application. If you want to either override or merge the existing main.py file with a new configuration, use the following command:
```bash
python -m fastapi_easystart.main config-main
```

### 3. Running the Development Server
Once the project is set up, you can start the development server:
```bash
uvicorn main:app --reload
```

Alternatively, you can use the FastAPI CLI command:

```bash
fastapi dev main.py
```

## Documentation

For full documentation, visit the FastAPI EasyStart Documentation (Coming Soon).

[//]: # (## Contributing)

[//]: # ()
[//]: # (Contributions are welcome! Please see the CONTRIBUTING.md file for more information on how to get involved.)


## License

This project is licensed under a modified MIT License - see the [LICENSE](LICENSE) file for details.

---

This version organizes the information clearly, ensures that placeholders for future content are marked, and maintains a professional tone throughout. Adjust the documentation and URLs when they are available.















