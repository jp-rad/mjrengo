import datetime
from fastapi.testclient import TestClient
import json
from pathlib import Path
import pytest
import urllib
import urllib.parse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app


@pytest.fixture
def currnet_datetime():
    td = datetime.timedelta(hours=9)
    tz = datetime.timezone(td, "JST")
    dt = datetime.datetime.now(tz)
    return str(dt)


@pytest.fixture
def current_dir_path():
    return Path(__file__).parent


@pytest.fixture
def results_dir_path(current_dir_path: Path):
    path = current_dir_path.joinpath("../../../results")
    path.mkdir(exist_ok=True)
    return path


@pytest.fixture
def odt_dir_path(current_dir_path: Path):
    return current_dir_path.joinpath("samples/odt")


@pytest.fixture
def simple_template_odt_file_reader(odt_dir_path: Path):
    file_path = odt_dir_path.joinpath("simple_template.odt")
    return open(file_path, "rb")


@pytest.fixture
def readme_md_file_text(odt_dir_path: Path):
    file_path = odt_dir_path.joinpath("README.md")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def template_odt_file_reader(odt_dir_path: Path):
    file_path = odt_dir_path.joinpath("template.odt")
    return open(file_path, "rb")


@pytest.fixture
def writer_png_file_reader(odt_dir_path: Path):
    file_path = odt_dir_path.joinpath("writer.png")
    return open(file_path, "rb")


@pytest.fixture
def context_odt(
    currnet_datetime,
    readme_md_file_text,
):
    return {
        "document": {
            "datetime": currnet_datetime,
            "md_sample": readme_md_file_text,
        },
        "countries": [
            {
                "country": "United States",
                "capital": "Washington",
                "cities": ["miami", "new york", "california", "texas", "atlanta"],
            },
            {"country": "England", "capital": "London", "cities": ["gales"]},
            {
                "country": "Japan",
                "capital": "Tokio",
                "cities": ["hiroshima", "nagazaki"],
            },
            {
                "country": "Nicaragua",
                "capital": "Managua",
                "cities": ["leon", "granada", "masaya"],
            },
            {"country": "Argentina", "capital": "Buenos aires"},
            {"country": "Chile", "capital": "Santiago"},
            {
                "country": "Mexico",
                "capital": "MExico City",
                "cities": ["puebla", "cancun"],
            },
        ],
    }


@pytest.fixture
def docx_dir_path(current_dir_path: Path):
    return current_dir_path.joinpath("samples/docx")


@pytest.fixture
def order_tpl_docx_file_path(docx_dir_path: Path):
    return docx_dir_path.joinpath("order_tpl.docx")


@pytest.fixture
def order_tpl_docx_file_reader(docx_dir_path: Path):
    file_path = docx_dir_path.joinpath("order_tpl.docx")
    return open(file_path, "rb")


@pytest.fixture
def replace_picture_tpl_docx_file_reader(docx_dir_path: Path):
    file_path = docx_dir_path.joinpath("replace_picture_tpl.docx")
    return open(file_path, "rb")


@pytest.fixture
def python_png_file_reader(docx_dir_path: Path):
    file_path = docx_dir_path.joinpath("python.png")
    return open(file_path, "rb")


@pytest.fixture
def context_docx():
    return {
        "customer_name": "Eric",
        "items": [
            {"desc": "Python interpreters", "qty": 2, "price": "FREE"},
            {"desc": "Django projects", "qty": 5403, "price": "FREE"},
            {"desc": "Guido", "qty": 1, "price": "100,000,000.00"},
        ],
        "in_europe": True,
        "is_paid": False,
        "company_name": "The World Wide company",
        "total_price": "100,000,000.00",
    }


@pytest.fixture
def relatorio_dir_path(current_dir_path: Path):
    return current_dir_path.joinpath("samples/relatorio")


@pytest.fixture
def pie_chart_png_cha_file_reader(relatorio_dir_path: Path):
    file_path = relatorio_dir_path.joinpath("pie_chart.png.cha")
    return open(file_path, "rb")


@pytest.fixture
def vbar_chart_svg_cha_file_reader(relatorio_dir_path: Path):
    file_path = relatorio_dir_path.joinpath("vbar_chart.svg.cha")
    return open(file_path, "rb")


@pytest.fixture
def basic_tex_file_reader(relatorio_dir_path: Path):
    file_path = relatorio_dir_path.joinpath("basic.tex")
    return open(file_path, "rb")


@pytest.fixture
def context_relatorio():
    return {
        "customer": {
            "name": "John Bonham",
            "address": {"street": "Smirnov street", "zip": 1000, "city": "Montreux"},
        },
        "lines": [
            {
                "item": {"name": "Vodka 70cl", "reference": "VDKA-001", "price": 10.34},
                "quantity": 7,
                "amount": 7 * 10.34,
            },
            {
                "item": {
                    "name": "Cognac 70cl",
                    "reference": "CGNC-067",
                    "price": 13.46,
                },
                "quantity": 12,
                "amount": 12 * 13.46,
            },
            {
                "item": {
                    "name": "Sparkling water 25cl",
                    "reference": "WATR-007",
                    "price": 4,
                },
                "quantity": 1,
                "amount": 4,
            },
            {
                "item": {
                    "name": "Good customer",
                    "reference": "BONM-001",
                    "price": -20,
                },
                "quantity": 1,
                "amount": -20,
            },
        ],
        "id": "MZY-20080703",
        "status": "late",
    }


client = TestClient(app)


def extract_filename_from_response(response):
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition:
        if "filename*=utf-8''" in content_disposition:
            filename = content_disposition.split("filename*=utf-8''")[-1]
            filename = urllib.parse.unquote(filename)
            return filename
        elif "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"')
            return filename
        else:
            return None
    else:
        return None


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_simple_template_odt(
    convert_to_pdf: bool,
    results_dir_path: Path,
    simple_template_odt_file_reader,
    context_odt,
):
    request_data = {
        "context": context_odt,
        "file_basename": "komainu_odt_simple_template_{{document.datetime}}",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = {
        "request": (None, json.dumps(request_data), "application/json"),
        "template": (
            "simple_template.odt",
            simple_template_odt_file_reader,
            "application/vnd.oasis.opendocument.text",
        ),
    }

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"application/vnd.oasis.opendocument.text" in response.content

    result_filename = extract_filename_from_response(response)
    with open(results_dir_path.joinpath(result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_template_odt(
    convert_to_pdf: bool,
    results_dir_path: Path,
    template_odt_file_reader,
    writer_png_file_reader,
    simple_template_odt_file_reader,
):
    context = {"image": "writer.png"}

    request_data = {
        "context": context,
        "file_basename": "komainu_odt_template",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = [
        ("request", (None, json.dumps(request_data), "application/json")),
        (
            "template",
            (
                "template.odt",
                template_odt_file_reader,
                "application/vnd.oasis.opendocument.text",
            ),
        ),
        ("medias", ("writer.png", writer_png_file_reader, "image/png")),
        (
            "medias",
            (
                "simple_template.odt",
                simple_template_odt_file_reader,
                "application/vnd.oasis.opendocument.text",
            ),
        ),
    ]

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"application/vnd.oasis.opendocument.text" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_odt_template.pdf"
    else:
        assert result_filename == "komainu_odt_template.odt"
    with open(results_dir_path.joinpath(result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_order_tpl_docx(
    convert_to_pdf: bool,
    results_dir_path: Path,
    order_tpl_docx_file_reader,
    context_docx,
):
    request_data = {
        "context": context_docx,
        "file_basename": "komainu_docx_order_{{customer_name}}",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = [
        ("request", (None, json.dumps(request_data), "application/json")),
        (
            "template",
            (
                "order_tpl.docx",
                order_tpl_docx_file_reader,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        ),
    ]

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"word/document.xml" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_docx_order_Eric.pdf"
    else:
        assert result_filename == "komainu_docx_order_Eric.docx"
    with open(results_dir_path.joinpath(result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_replace_picture_tpl_docx(
    convert_to_pdf: bool,
    results_dir_path: Path,
    replace_picture_tpl_docx_file_reader,
    python_png_file_reader,
):
    context = {"name": "python"}

    request_data = {
        "context": context,
        "file_basename": "komainu_docx_replace_picture_{{name}}",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = {
        "request": (None, json.dumps(request_data), "application/json"),
        "template": (
            "replace_picture_tpl.docx",
            replace_picture_tpl_docx_file_reader,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        # image tag: python_logo.png
        "medias": ("python_logo.png", python_png_file_reader, "image/png"),
    }

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"word/document.xml" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_docx_replace_picture_python.pdf"
    else:
        assert result_filename == "komainu_docx_replace_picture_python.docx"
    with open(results_dir_path.joinpath(result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_pie_chart_png_cha(
    convert_to_pdf: bool,
    results_dir_path: Path,
    pie_chart_png_cha_file_reader,
    context_relatorio,
):
    request_data = {
        "context": context_relatorio,
        "file_basename": "komainu_pie",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = {
        "request": (None, json.dumps(request_data), "application/json"),
        "template": (
            "pie_chart.png.cha",
            pie_chart_png_cha_file_reader,
            "application/octet-stream",
        ),
    }

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"PNG" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_pie.pdf"
    else:
        assert result_filename == "komainu_pie.png"
    with open(results_dir_path.joinpath(result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_vbar_chart_svg_cha(
    convert_to_pdf: bool,
    results_dir_path: Path,
    vbar_chart_svg_cha_file_reader,
    context_relatorio,
):
    request_data = {
        "context": context_relatorio,
        "file_basename": "komainu_vbar",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = {
        "request": (None, json.dumps(request_data), "application/json"),
        "template": (
            "vbar_chart.svg.cha",
            vbar_chart_svg_cha_file_reader,
            "application/octet-stream",
        ),
    }

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"<svg xmlns=" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_vbar.pdf"
    else:
        assert result_filename == "komainu_vbar.svg"
    with open(results_dir_path.joinpath(result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False])
def test_komainu_post_basic_tex(
    convert_to_pdf: bool,
    results_dir_path: Path,
    basic_tex_file_reader,
    context_relatorio,
):
    request_data = {
        "context": context_relatorio,
        "file_basename": "komainu_basic_tex",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = {
        "request": (None, json.dumps(request_data), "application/json"),
        "template": (
            "basic.tex",
            basic_tex_file_reader,
            "application/octet-stream",
        ),
    }

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"%PDF" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_basic_tex.pdf"
    else:
        assert result_filename == "komainu_basic_tex.pdf"
    with open(results_dir_path.joinpath(result_filename), "wb") as f:
        f.write(response.content)
