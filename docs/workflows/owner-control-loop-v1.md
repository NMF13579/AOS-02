# Owner Control Loop v1

```yaml
execution_authorized: false
mutating_executor: DISABLED
```

## Что делает владелец

1. Собирает `Idea`, `Risk` и `Scope` как v2 YAML records.
2. Запускает `compile-task`; результат — только черновик Task Brief.
3. Добавляет проверяемые Evidence records и запускает `validate`.
4. Читает JSON-результат: `PASS` означает техническую корректность, а не одобрение.
5. Для execution-related request может посмотреть `preview-execution`; readiness остаётся blocked.

## Что система не делает

- не подтверждает, что решение принял человек;
- не меняет файлы через control API;
- не делает commit, push, merge или release;
- не считает `UNKNOWN` или `NOT_RUN` успешным результатом.

Если результат требует human review, остановитесь и примите решение вне локального YAML.
