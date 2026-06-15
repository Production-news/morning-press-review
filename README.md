# 🌏 Morning Press Review Agent

Автоматический утренний дайджест новостей из Китая, Индии и MENA.
Отправляется каждый день в **8:00 по времени Алматы**.

## Категории новостей
- 🔬 Технологии и инновации
- 🎭 Культура, спорт, светская жизнь

---

## Настройка (один раз)

### 1. Получи Gmail App Password
> Обычный пароль Gmail не подойдёт — нужен специальный "пароль приложения".

1. Перейди на [myaccount.google.com/security](https://myaccount.google.com/security)
2. Включи **двухэтапную аутентификацию** (если не включена)
3. Найди раздел **"Пароли приложений"** (App Passwords)
4. Создай новый → выбери "Другое" → назови "Morning Digest"
5. Скопируй 16-значный пароль (он показывается только один раз!)

### 2. Добавь секреты в GitHub

В репозитории: **Settings → Secrets and variables → Actions → New repository secret**

Добавь 4 секрета:

| Название | Значение |
|----------|----------|
| `ANTHROPIC_API_KEY` | Твой ключ с console.anthropic.com |
| `GMAIL_USER` | Твой Gmail адрес (example@gmail.com) |
| `GMAIL_APP_PASSWORD` | 16-значный пароль из шага 1 |
| `RECIPIENT_EMAIL` | Email куда слать дайджест |

### 3. Загрузи файлы в репозиторий

Загрузи в корень репозитория:
- `agent.py`
- `.github/workflows/daily-digest.yml`

### 4. Протестируй вручную

В репозитории: **Actions → Morning Press Review → Run workflow**

Если письмо пришло — всё работает! Дальше агент будет запускаться сам каждое утро в 8:00.

---

## Файлы

```
morning-press-review/
├── agent.py                          # Основной скрипт агента
├── .github/
│   └── workflows/
│       └── daily-digest.yml          # Расписание запуска
└── README.md
```
