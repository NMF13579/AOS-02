# Fictional Example — Documentation Cleanup Request

```yaml
execution_authorized: false
mutating_executor: DISABLED
fictional: true
```

## Сценарий

Идея: привести в порядок одну страницу документации. Risk задаёт низкий профиль. Scope разрешает только `docs/guide.md`; `src/`, `.github/` и любые credentials остаются вне scope.

Владелец может скомпилировать черновик Task Brief и технически проверить records. Даже при `validation: PASS`:

```yaml
approval_granted: false
execution_authorized: false
```

`preview-execution` может показать предполагаемую операцию, но `execute-scoped` остаётся blocked. Для реального изменения нужен отдельный Human Decision и будущий trusted executor, которого в rebuild v1 нет.
