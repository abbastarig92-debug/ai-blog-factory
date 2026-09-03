"""
النواة المشتركة لكل الوكلاء: عميل LLM، تحميل الإعدادات، الحالة، السجلّات.
يدعم Anthropic (افتراضي) و OpenAI كبديل — يختار حسب المفاتيح المتاحة.
"""
from __future__ import annotations
import os, json, re, time, logging, pathlib, datetime as dt
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / "state"
CONTENT = ROOT / "site" / "src" / "content" / "blog"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-18s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)


def log(name: str) -> logging.Logger:
    return logging.getLogger(name)


# ---------------------------------------------------------------- config
def cfg(name: str) -> dict:
    with open(ROOT / "config" / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


SITE = cfg("site")
NICHE = cfg("niche")


# ---------------------------------------------------------------- state
def load_state(name: str, default: Any) -> Any:
    p = STATE / f"{name}.json"
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8") or "null") or default


def save_state(name: str, data: Any) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / f"{name}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def today() -> str:
    return dt.date.today().isoformat()


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", s)[:70].strip("-")


# ---------------------------------------------------------------- LLM
class LLM:
    """غلاف موحّد فوق Anthropic / OpenAI مع إعادة المحاولة وتحليل JSON."""

    def __init__(self, model: str | None = None):
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        if self.anthropic_key:
            self.provider = "anthropic"
        elif self.openai_key:
            self.provider = "openai"
        elif self.gemini_key:
            self.provider = "gemini"
        else:
            self.provider = "none"
        defaults = {"anthropic": "claude-sonnet-4-5", "openai": "gpt-4o-mini",
                    "gemini": "gemini-2.5-flash", "none": ""}
        self.model = model or os.getenv("LLM_MODEL") or defaults[self.provider]
        self.log = log("llm")

    def available(self) -> bool:
        return self.provider != "none"

    def chat(self, system: str, user: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        if self.provider == "none":
            raise RuntimeError(
                "لا يوجد مفتاح API. ضع ANTHROPIC_API_KEY أو OPENAI_API_KEY أو "
                "GEMINI_API_KEY (مجاني) في متغيرات البيئة."
            )
        last = None
        for attempt in range(4):
            try:
                if self.provider == "anthropic":
                    return self._anthropic(system, user, max_tokens, temperature)
                if self.provider == "gemini":
                    return self._gemini(system, user, max_tokens, temperature)
                return self._openai(system, user, max_tokens, temperature)
            except Exception as e:  # noqa: BLE001
                last = e
                wait = 2 ** attempt * 3
                self.log.warning("محاولة %s فشلت (%s) — إعادة بعد %ss", attempt + 1, e, wait)
                time.sleep(wait)
        raise RuntimeError(f"فشل نداء النموذج بعد 4 محاولات: {last}")

    def _anthropic(self, system, user, max_tokens, temperature):
        import anthropic

        c = anthropic.Anthropic(api_key=self.anthropic_key)
        r = c.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(b.text for b in r.content if b.type == "text")

    def _openai(self, system, user, max_tokens, temperature):
        from openai import OpenAI

        c = OpenAI(api_key=self.openai_key)
        r = c.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return r.choices[0].message.content or ""

    def _gemini(self, system, user, max_tokens, temperature):
        """واجهة REST مباشرة — بلا مكتبات إضافية. الطبقة المجانية تكفي 2-3 مقالات يومياً."""
        import json as _json, urllib.request
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{self.model}:generateContent?key={self.gemini_key}")
        body = _json.dumps({
            "system_instruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": temperature,
                                 "maxOutputTokens": max_tokens},
        }).encode()
        req = urllib.request.Request(url, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            data = _json.load(r)
        cands = data.get("candidates") or []
        if not cands:
            raise RuntimeError(f"لا استجابة من Gemini: {str(data)[:300]}")
        parts = cands[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
        if not text.strip():
            raise RuntimeError(f"استجابة فارغة من Gemini ({cands[0].get('finishReason')})")
        return text

    def json(self, system: str, user: str, max_tokens: int = 4000, temperature: float = 0.4) -> Any:
        raw = self.chat(
            system + "\n\nReturn ONLY valid JSON. No markdown fences, no commentary.",
            user,
            max_tokens,
            temperature,
        )
        return parse_json(raw)


def parse_json(raw: str) -> Any:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.S)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"(\[.*\]|\{.*\})", raw, re.S)
        if not m:
            raise
        return json.loads(m.group(1))


# ---------------------------------------------------------------- markdown
def write_post(front: dict, body: str) -> pathlib.Path:
    CONTENT.mkdir(parents=True, exist_ok=True)
    path = CONTENT / f"{front['slug']}.md"
    fm = yaml.safe_dump(front, allow_unicode=True, sort_keys=False).strip()
    path.write_text(f"---\n{fm}\n---\n\n{body.strip()}\n", encoding="utf-8")
    return path


def read_posts() -> list[dict]:
    """يقرأ كل المقالات المنشورة مع الـ frontmatter."""
    out = []
    if not CONTENT.exists():
        return out
    for p in sorted(CONTENT.glob("*.md")):
        txt = p.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
        if not m:
            continue
        try:
            front = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        out.append({"path": p, "front": front, "body": m.group(2)})
    return out
