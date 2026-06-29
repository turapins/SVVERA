# SVVERA
**AI Creative Production System — Vocal Image**
> S = Script · V = Video · V = Voice · E = Edit · R = Resolve · A = Analysis

---

## Что это

SVVERA — мульти-агентная система для производства performance video ads для Vocal Image.

Оркестратор: **Claude Code** (главный мозг).
База: **OpenMontage** (pipeline engine).
Все решения логируются. Каждый этап требует апрува от Ivan.

---

## Стек

| Роль | Инструмент |
|------|-----------|
| Оркестратор | Claude Code |
| Video + Photo генерация | Higgsfield |
| Voice (основной) | ElevenLabs (Andy / Peter / Arya) |
| Voice (альтернатива) | Higgsfield Voice |
| Анализ роликов | Gemini Vision |
| Аватары / презентеры | HeyGen |
| Монтаж простой | Remotion + FFmpeg |
| Монтаж сложный | DaVinci Resolve (davinci-resolve-mcp) |
| Скрипты + визуал брифы | Google Docs + Figma |
| Документация + таски | ClickUp (автоматически) |
| Хранилище креативов | Google Drive |
| Конкурентный анализ | Tryatria (pending admin) |
| Версионирование | GitHub (turapins/SVVERA) |

---

## Агенты SVVERA

### S — Script Agent
- Читает контекст из Google Drive (скрипты-победители, брифы, аватары)
- Генерирует скрипт по шаблону Vocal Image
- Структура: **Hook → Value → Proof → CTA**
- Выдаёт: скрипт + scene plan + промпты для каждой сцены
- Апрув от Ivan перед переходом к следующему агенту

### V — Video Agent
- Получает scene plan + промпты от Script Agent
- Генерирует клипы через Higgsfield
- **Reference image control**: один reference скейлится на все кадры (фото + видео)
- Никакой случайной генерации — всё через reference
- Поддерживает character consistency между сценами

### V — Voice Agent
- Получает скрипт от Script Agent
- Основной провайдер: ElevenLabs (Andy / Peter / Arya)
- Альтернатива: Higgsfield Voice
- Выбор провайдера задаётся в конфиге задачи

### E — Edit Agent
- Собирает клипы + голос + субтитры
- Простые проекты: Remotion + FFmpeg
- Сложные проекты: передаёт в Resolve Agent
- Форматы: 9:16 (Reels/TikTok), 1:1, 16:9
- Word-level субтитры из коробки

### R — Resolve Agent
- Финальный polish в DaVinci Resolve Studio
- Через `davinci-resolve-mcp`
- Цветокоррекция, аудио микс, финальный рендер
- Используется для сложных проектов (шоуменсеты, подкасты)

### A — Analysis Agent
- Анализирует готовые ролики через Gemini Vision
- Анализирует ролики конкурентов (через Tryatria когда будет доступ)
- Выдаёт: hook rate оценку, структуру, сильные/слабые места
- Обучает Script Agent на winners

---

## Типы контента

| Тип | Формат | Кампания |
|-----|--------|----------|
| UGC ad | 9:16, 15–60 сек | Web funnel + App installs |
| Подкаст (2 персонажа) | 9:16, 30–90 сек | Web funnel |
| Шоуменсет | 9:16 / 16:9 | Web funnel |
| Стикеры | PNG/WEBP | App installs |
| Статика | 1:1 / 9:16 | Web funnel + App installs |

**Web funnel** — контент для привлечения на сайт, более длинный, образовательный
**App installs** — короткий, прямой, action-oriented

---

## Структура репозитория

```
SVVERA/ (= ~/OpenMontage на локальной машине)
│
├── SVVERA.md              ← этот файл (главный документ)
├── CLAUDE.md              ← инструкции для агента Claude Code
├── .env.example           ← шаблон ключей (без значений)
├── .gitignore             ← исключает .env и media файлы
│
├── skills/
│   ├── vocal-image/       ← Vocal Image скиллы для агента
│   │   ├── playbook.md    ← правила creative production
│   │   ├── avatars.md     ← Andy, Peter, Arya — профили
│   │   └── criteria.md    ← что такое хороший ролик
│   ├── core/              ← OpenMontage core skills
│   └── pipelines/         ← pipeline skills
│
├── context/               ← знания системы
│   ├── brand/             ← персонажи, reference sheets
│   ├── scripts/           ← winners и losers с метриками
│   └── playbook.md        ← правила Vocal Image creative
│
├── agents/                ← конфиги агентов SVVERA
│
├── pipeline_defs/         ← OpenMontage pipeline manifests
│
├── output/                ← готовые ролики (не в git)
└── work/                  ← рабочие файлы (не в git)
```

---

## Ключи (.env)

```bash
# Video + Photo + Voice (основной)
HIGGSFIELD_API_KEY=

# Voice (основной)
ELEVENLABS_API_KEY=

# Analysis (анализ роликов через Vision)
GEMINI_API_KEY=

# Аватары
HEYGEN_API_KEY=

# Stock media (бесплатно)
PEXELS_API_KEY=
PIXABAY_API_KEY=

# Google Drive
GOOGLE_DRIVE_ROOT_ID=1JjZYiyYSSDliLKDITCCH6-1E1ehSXCzp
GOOGLE_DRIVE_ARCHIVE_ID=1zeTJs-UpzHp_a6myXAFHs8G2CP5zPpos

# ClickUp
CLICKUP_API_KEY=
CLICKUP_LIST_ID=        # Performance Sets board
```

---

## ClickUp автоматизация

Каждый завершённый проект автоматически создаёт таск в ClickUp:
- Название: `[ID] НАЗВАНИЕ_РОЛИКА`
- Ссылка на Google Doc (скрипт)
- Ссылка на Google Drive (готовый ролик)
- Теги: формат, кампания, персонаж, статус
- Упоминание пользователей по роли

---

## Правила системы

1. **Никакой случайной генерации** — всё через reference image control (Higgsfield)
2. **Апрув на каждом этапе** — Ivan апрувит перед переходом
3. **Контекст из Drive** — агент всегда читает winners перед генерацией
4. **Логирование решений** — каждый выбор провайдера и стиля записывается
5. **Простое → Remotion/FFmpeg, Сложное → Resolve**
6. **Форматы** — 9:16 default для всех ads; 16:9 только для шоуменсетов и YouTube

---

## Статус компонентов

| Компонент | Статус |
|-----------|--------|
| OpenMontage | ✅ установлен и настроен |
| HyperFrames | ✅ v0.7.18 |
| Remotion | ✅ установлен |
| FFmpeg | ✅ v8.1 |
| ElevenLabs | ✅ ключ есть |
| Pexels | ✅ ключ есть |
| Pixabay | ✅ ключ есть |
| Higgsfield | ✅ ключ есть |
| Gemini | ✅ ключ есть (GOOGLE_API_KEY) |
| HeyGen | ✅ ключ есть |
| davinci-resolve-mcp | 🔧 нужно установить |
| Google Drive | 🔧 нужна настройка |
| ClickUp | 🔧 нужна настройка |
| Tryatria | ⏳ pending admin access |
| Figma | ⏳ фаза 3 |

---

## Фазы реализации

**Фаза 1 (сейчас)** — основа работает
- ✅ OpenMontage + HyperFrames + Remotion
- ✅ ElevenLabs + Pexels
- 🎯 Добавить Vocal Image skills (playbook, avatars, criteria)
- 🎯 Первый UGC ad через pipeline

**Фаза 2** — полный production цикл
- Higgsfield video generation + reference image control
- Gemini analysis agent
- Google Drive интеграция

**Фаза 3** — автоматизация
- ClickUp auto-tasks
- DaVinci Resolve MCP
- Figma visual briefs

**Фаза 4** — аналитика и рост
- Tryatria competitor analysis
- Meta Ads performance feedback loop
- Script Agent обучается на winners

---

*Последнее обновление: июнь 2026*
*Версия: 0.2 — Active Build*
