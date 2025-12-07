"""
匯出 OpenAPI JSON 到 tests/e2e/__fixtures__/openapi.json
用於 E2E Agent 的契約對齊。
執行方式：python tests/e2e/export_openapi.py
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from main import app  # type: ignore
except Exception as e:
    raise SystemExit(f"❌ 無法匯入 main.app，請確認後端可被匯入：{e}")


def main():
    output_path = Path(__file__).parent / "__fixtures__" / "openapi.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    schema = app.openapi()
    output_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ OpenAPI 已匯出到 {output_path}")


if __name__ == "__main__":
    main()
