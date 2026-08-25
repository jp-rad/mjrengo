# report-generator-1

A Python-based report generation toolkit supporting ODT and DOCX templates, with FastAPI integration and Docker compatibility.  
Includes support for Relatorio, a templating library capable of generating various document formats such as ODT, ODS, PNG, SVG, and more.

---

## Installation

### Install from Remote Repository

To install the latest version directly from GitHub, run:

```bash
pip3 install --upgrade git+https://github.com/jp-one/report-generator-1.git
```

### Local Installation (Development)

If you want to install from your local source (for development or testing):

```bash
pip3 uninstall -y rptgen1          # Remove any previous installation
cd code                            # Enter the source directory
python3 -m build                   # Build the package
pip3 install --upgrade .           # Install the built package
```
> **Note:** If you are using Docker, make sure you run these commands inside the `/home/vscode/dev/code` directory.

---

## Running Unit Tests

Unit tests are written using `pytest`. To execute all tests and save results:

```bash
cd code/tests
pytest
```

- Test results and logs are saved in the `tests/result` directory.
- You can customize test runs with additional pytest options, e.g. `pytest -v` for verbose output.

---

## FastAPI Report Engine Example

A sample FastAPI server is provided to demonstrate report generation via API.

To start the example server:

```bash
cd code/example/fastapi-report-engine
python3 main.py
```

Once running, you can access the interactive API documentation at:

- [http://localhost/docs](http://localhost/docs)
- [http://localhost:8002/docs](http://localhost:8002/docs)

Use these endpoints to test report generation and explore available API features.

---

## Project Structure

- `code/src/rptgen1/` — Main source code and package files
- `code/tests/` — Unit tests and test data
- `code/example/fastapi-report-engine/` — FastAPI example server

---

## Dependencies

This project relies on the following open-source libraries:

- [python-odt-template](https://github.com/Tobi-De/python-odt-template) — ODT template rendering
- [python-docx-template](https://github.com/elapouya/python-docx-template) — DOCX template rendering
- [relatorio](https://pypi.org/project/relatorio/) — templating engine for generating documents
- [unoserver](https://github.com/unoconv/unoserver) — LibreOffice server for document conversion
- [unoserver-docker](https://github.com/unoconv/unoserver-docker) — Dockerized unoserver for container environments

---

## Contributing

Contributions are welcome! Please submit issues or pull requests via GitHub.

---

## License

See the `LICENSE` file for details.

---

## Acknowledgements

Thanks to the open-source community for their
