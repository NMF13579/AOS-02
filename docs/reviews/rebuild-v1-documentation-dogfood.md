# Documentation-Only Dogfood — Rebuild v1

```yaml
kind: documentation-only
execution_authorized: false
mutating_executor: DISABLED
```

## Реальная задача

Проверить, может ли владелец без знания внутреннего Python-кода найти: установку, validated control loop, пример и границу полномочий.

## Выполнить

1. Открыть корневой `README.md`.
2. Перейти в `Validated Control Loop v1`.
3. Сверить, что normal package installation описана явно.
4. Прочитать fictional example и подтвердить, что она не выдаёт execution authority.
5. Заполнить human-review checklist.

## Критерий

Документация должна однозначно говорить: технический PASS не является approval; mutation, Git writes и trusted human authority отсутствуют.
