# Example - FastAPI Report Engine

```bash
cd code/example/fastapi-report-engine
python main.py
```

http://localhost/docs or http://localhost:8002/docs

samples:
- `./code/example/fastapi-report-engine/tests/samples/odt`
- `./code/example/fastapi-report-engine/tests/samples/docx`
- `./code/example/fastapi-report-engine/tests/samples/relatorio`

## odt - simple_template.odt

- template: `simple_template.odt`
- medias: (unckecked: `Send empty value`)
- request:

```json

{
    "context": {
        "document": {
            "datetime": "2025/01/23 12:34",
            "md_sample": "# This is an H1\n## This is an H2\nMarkdown is a lightweight markup language."
        },
        "countries": [
            {
                "country": "United States",
                "capital": "Washington",
                "cities": ["miami", "new york", "california", "texas", "atlanta"]
            },
            {"country": "England", "capital": "London", "cities": ["gales"]},
            {"country": "Japan", "capital": "Tokio", "cities": ["hiroshima", "nagazaki"]},
            {
                "country": "Nicaragua",
                "capital": "Managua",
                "cities": ["leon", "granada", "masaya"]
            },
            {"country": "Argentina", "capital": "Buenos aires"},
            {"country": "Chile", "capital": "Santiago"},
            {"country": "Mexico", "capital": "MExico City", "cities": ["puebla", "cancun"]}
        ]
    },
    "file_basename": "renderd_{{document.datetime}}",
    "convert_to_pdf": true,
    "pdf_filter_options": {
        "Watermark": "draft",
        "SelectPdfVersion": "3"
    }
}

```

## odt - template.odt

- template: `template.odt`
- medias: `writer.png`
- request:

```json

{
    "context": {
        "image":"writer.png"
    },
    "file_basename": "rendered_{{image}}",
    "convert_to_pdf": true,
    "pdf_filter_options": {}
}

```

## docx - order_tpl.docx

- template: `order_tpl.docx`
- medias: (unckecked: `Send empty value`)
- request:

```json

{
    "context": {
        "customer_name": "Eric",
        "items": [
            {"desc": "Python interpreters", "qty": 2, "price": "FREE"},
            {"desc": "Django projects", "qty": 5403, "price": "FREE"},
            {"desc": "Guido", "qty": 1, "price": "100,000,000.00"}
        ],
        "in_europe": true,
        "is_paid": false,
        "company_name": "The World Wide company",
        "total_price": "100,000,000.00"
    },
    "file_basename": "rendered_{{customer_name}}",
    "convert_to_pdf": true,
    "pdf_filter_options": {"TiledWatermark": "draft"}
}

```

## docx - replace_picture_tpl.docx

- template: `replace_picture_tpl.docx`
- medias: `python_logo.png`
- request:

```json

{
    "context": {
        "name":"python"
    },
    "file_basename": "rendered_{{name}}",
    "convert_to_pdf": true,
    "pdf_filter_options": {}
}

```

## relatorio - basic.tex, pie_chart.png.cha, vbar_chart.svg.cha

- template: `basic.tex` or `pie_chart.png.cha` or `vbar_chart.svg.cha`
- medias: (unckecked: `Send empty value`)
- request:

```json

{
    "context": {
        "customer": {
            "name": "John Bonham",
            "address": {"street": "Smirnov street", "zip": 1000, "city": "Montreux"}
        },
        "lines": [
            {
                "item": {"name": "Vodka 70cl", "reference": "VDKA-001", "price": 10.34},
                "quantity": 7,
                "amount": 72.38
            },
            {
                "item": {
                    "name": "Cognac 70cl",
                    "reference": "CGNC-067",
                    "price": 13.46
                },
                "quantity": 12,
                "amount": 161.52
            },
            {
                "item": {
                    "name": "Sparkling water 25cl",
                    "reference": "WATR-007",
                    "price": 4
                },
                "quantity": 1,
                "amount": 4
            },
            {
                "item": {
                    "name": "Good customer",
                    "reference": "BONM-001",
                    "price": -20
                },
                "quantity": 1,
                "amount": -20
            }
        ],
        "id": "MZY-20080703",
        "status": "late"
    },
    "file_basename": "relatorio_{{customer.name}}",
    "convert_to_pdf": false,
    "pdf_filter_options": {}
}

```
