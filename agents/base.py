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
                    "gemini": "gemini-3.8-flash", "none": ""}
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
                if attempt == 3:
                    self.log.error("محاولة %s فشلت نهائياً: %s", attempt + 1, e)
                    break
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

    # ---- Gemini: REST مباشر، بلا مكتبات إضافية -------------------------
    GEMINI_API = "https://generativelanguage.googleapis.com/v1beta"

    def _gemini_request(self, path: str, body: dict | None = None) -> dict:
        """نداء REST مع إظهار نص الخطأ الحقيقي من Google بدل رسالة HTTP مبهمة."""
        import json as _json, urllib.request, urllib.error
        sep = "&" if "?" in path else "?"
        url = f"{self.GEMINI_API}/{path}{sep}key={self.gemini_key}"
        data = _json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"} if data else {},
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return _json.load(r)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:600]
            raise RuntimeError(f"Gemini HTTP {e.code} على {path} — {detail}") from None

    def _gemini_models(self) -> list[str]:
        """أسماء الموديلات المتاحة فعلياً لهذا المفتاح والتي تدعم generateContent."""
        data = self._gemini_request("models?pageSize=200")
        out = []
        for m in data.get("models", []):
            if "generateContent" in (m.get("supportedGenerationMethods") or []):
                out.append(m["name"].split("/", 1)[-1])
        return out

    @staticmethod
    def _gemini_rank(name: str) -> tuple:
        """يفضّل موديلات flash العامة، ويؤخّر المتخصصة وخفيفة الجودة."""
        bad = any(x in name for x in ("vision", "embedding", "aqa", "image", "tts", "live"))
        return (bad, "flash" not in name, "lite" in name, name)

    def _gemini_resolve_model(self) -> str:
        """يتأكد أن الموديل المطلوب موجود، ويجهّز قائمة بدائل حية مرتّبة."""
        if getattr(self, "_gemini_model_ok", False):
            return self.model
        available = sorted(self._gemini_models(), key=self._gemini_rank)
        if not available:
            raise RuntimeError("لا يوجد أي موديل يدعم generateContent لهذا المفتاح")
        if self.model not in available:
            self.log.warning("الموديل «%s» غير متاح — التحويل إلى «%s»", self.model, available[0])
            self.model = available[0]
        # البدائل: الموديل المختار أولاً، ثم البقية بالترتيب
        self._gemini_alts = [self.model] + [m for m in available if m != self.model]
        self._gemini_model_ok = True
        return self.model

    @staticmethod
    def _gemini_busy(err: Exception) -> bool:
        """هل الخطأ ازدحام مؤقت أو تجاوز حصة؟ عندها البديل أجدى من إعادة المحاولة."""
        t = str(err)
        return ("HTTP 503" in t or "HTTP 429" in t
                or "UNAVAILABLE" in t or "RESOURCE_EXHAUSTED" in t)

    def _gemini_generate(self, model, system, user, max_tokens, temperature):
        # موديلات الجيل الثالث «تفكّر» قبل الإجابة، وتفكيرها يُخصم من سقف المخرجات،
        # فنعطيها هامشاً كافياً حتى لا يعود الرد فارغاً بسبب MAX_TOKENS.
        budget = max(int(max_tokens) * 4, 8192)
        body = {
            "system_instruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": temperature,
                                 "maxOutputTokens": budget},
        }
        data = self._gemini_request(f"models/{model}:generateContent", body)
        cands = data.get("candidates") or []
        if not cands:
            fb = data.get("promptFeedback")
            raise RuntimeError(f"لا استجابة من Gemini (promptFeedback={fb}) {str(data)[:300]}")
        parts = cands[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts if "text" in p)
        if not text.strip():
            raise RuntimeError(
                f"استجابة فارغة من Gemini (finishReason={cands[0].get('finishReason')}, "
                f"usage={data.get('usageMetadata')})"
            )
        return text

    def _gemini(self, system, user, max_tokens, temperature):
        """ينادي الموديل، وعند الازدحام (503) أو تجاوز الحصة (429) ينتقل فوراً
        إلى البديل التالي بدل إعادة المحاولة على موديل مشغول."""
        self._gemini_resolve_model()
        last = None
        for model in list(self._gemini_alts)[:4]:
            try:
                text = self._gemini_generate(model, system, user, max_tokens, temperature)
            except RuntimeError as e:
                if not self._gemini_busy(e):
                    raise
                last = e
                self.log.warning("الموديل «%s» مزدحم — تجربة البديل التالي", model)
                continue
            if model != self.model:
                self.log.warning("تم التثبيت على الموديل البديل «%s»", model)
                self.model = model
                # اجعل الناجح أول القائمة للنداءات التالية
                self._gemini_alts = [model] + [m for m in self._gemini_alts if m != model]
            return text
        raise RuntimeError(f"كل موديلات Gemini المتاحة مزدحمة الآن — آخر خطأ: {last}")

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

