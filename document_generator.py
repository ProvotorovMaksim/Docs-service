from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jinja2 import Environment, StrictUndefined
from weasyprint import HTML

DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>{{ document_title or 'Документ' }}</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 40px;
        color: #1f2937;
        line-height: 1.5;
      }
      h1, h2 {
        color: #111827;
      }
      .meta {
        margin-bottom: 20px;
        color: #374151;
      }
      .section {
        margin-top: 24px;
      }
      .label {
        font-weight: bold;
      }
    </style>
  </head>
  <body>
    <h1>{{ document_title or 'Документ' }}</h1>
    <div class="meta">
      <div><span class="label">Номер:</span> {{ document_number or '—' }}</div>
      <div><span class="label">Дата:</span> {{ document_date or '—' }}</div>
    </div>

    <div class="section">
      <h2>Контрагент</h2>
      <p><span class="label">Компания:</span> {{ company_name or '—' }}</p>
      <p><span class="label">Контакт:</span> {{ contact_name or '—' }}</p>
      <p><span class="label">Email:</span> {{ email or '—' }}</p>
    </div>

    <div class="section">
      <h2>Содержание</h2>
      <p>{{ content or 'Содержимое документа отсутствует.' }}</p>
    </div>
  </body>
</html>
"""


def _parse_payload(value: Any) -> dict[str, Any]:
    if value is None:
        raise ValueError("Пустое значение для генерации документа")

    if isinstance(value, dict):
        return value

    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("Пустая строка для генерации документа")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return {"template": text, "context": {}}

        if isinstance(parsed, dict):
            return parsed

        return {"value": parsed}

    return {"value": value}


def _resolve_template(payload: dict[str, Any]) -> str:
    for key in ("template", "html_template", "document_template"):
        template_source = payload.get(key)
        if template_source:
            return str(template_source)
    return DEFAULT_TEMPLATE


def _resolve_context(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}

    for key in ("context", "data", "values"):
        value = payload.get(key)
        if isinstance(value, dict):
            return value

    context = {
        key: value
        for key, value in payload.items()
        if key not in {"template", "html_template", "document_template", "document_name", "output_dir"}
    }
    return context


def generate_docs(value: Any) -> str:
    """
    Генерирует PDF документ по шаблону с подстановкой плейсхолдеров.

    Ожидается JSON-строка или словарь вида:
    {
        "document_name": "contract",
        "template": "<h1>{{ company_name }}</h1>",
        "context": {
            "company_name": "ООО Ромашка",
            "document_title": "Договор",
            "content": "Текст документа"
        }
    }

    Возвращает путь к созданному PDF-файлу.
    """
    payload = _parse_payload(value)
    template_source = _resolve_template(payload)
    context = _resolve_context(payload)
    document_name = str(payload.get("document_name") or payload.get("name") or "document")
    output_dir = Path(str(payload.get("output_dir") or "generated_documents"))
    output_dir.mkdir(parents=True, exist_ok=True)

    rendered_html = Environment(undefined=StrictUndefined).from_string(template_source).render(**context)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    pdf_path = output_dir / f"{document_name}_{timestamp}.pdf"

    HTML(string=rendered_html).write_pdf(str(pdf_path))
    return str(pdf_path)


if __name__ == "__main__":
    sample_payload = {
        "document_name": "contract",
        "context": {
            "document_title": "Договор на оказание услуг",
            "document_number": "№ 001/2026",
            "document_date": "25.08.2026",
            "company_name": "ООО Тестовая Компания",
            "contact_name": "Иван Иванов",
            "email": "ivan@example.com",
            "content": "Настоящий документ подтверждает выполнение обязательств по оказанию услуг.",
        },
    }
    result_path = generate_docs(sample_payload)
    print(f"PDF generated: {result_path}")