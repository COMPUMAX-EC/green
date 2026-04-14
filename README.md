# Registro de actividad automatizada

Este repositorio existe para **documentar de forma pública** las ejecuciones de un workflow en GitHub Actions. Cada commit que ves aquí **corresponde a una ejecución real** que puedes abrir en la pestaña *Actions* y revisar logs, artefactos y el diff exacto.

## Qué hace el proyecto

1. **Una vez al día** (hora UTC configurable) se ejecuta el workflow.
2. Al inicio de cada **semana ISO** se eligen **al azar cinco días** (lunes a domingo, en UTC).
3. Solo si “hoy” es uno de esos cinco días, se añade una fila a `data/activity-log.md` y se guarda el calendario en `data/schedules/`.
4. El contenido del commit es **solo** ese registro y los metadatos de la semana: trazabilidad, no código de producto.

Así las contribuciones en GitHub reflejan **automatización y disciplina de CI**, no trabajo de desarrollo en otro sentido. Para portafolios o CV, lo razonable es enlazar también repos donde sí hay código, issues y revisiones.

## Puesta en marcha

1. Crea un repositorio vacío en GitHub y sube estos archivos.
2. En **Settings → Actions → General**, deja permitidos los workflows (por defecto suele estar bien).
3. Comprueba que la rama por defecto se llama `main` (o cambia el workflow si usas otra).
4. Opcional: ajusta la hora del cron en `.github/workflows/scheduled-activity.yml`.
5. Para que los commits **cuenten en tu gráfico personal** de GitHub, en el repo ve a **Settings → Secrets and variables → Actions** y crea:
   - `ACTIVITY_GIT_NAME` (por ejemplo tu nombre o `@tuusuario`)
   - `ACTIVITY_GIT_EMAIL` (el correo verificado de tu cuenta; suele ser el de *noreply* de GitHub en **Settings → Emails**)

   Si no los defines, el autor será `github-actions[bot]` y el gráfico de contribuciones de tu perfil puede no reflejar esos commits aunque el historial del repo sí quede registrado.

## Archivos importantes

| Ruta | Descripción |
| --- | --- |
| `.github/workflows/scheduled-activity.yml` | Programación y job que actualiza el registro |
| `scripts/update_activity.py` | Lógica de “cinco días aleatorios por semana” y escritura del log |
| `data/activity-log.md` | Historial legible de ejecuciones |
| `data/schedules/*.json` | Plan semanal generado (qué días tocaron) |

## Licencia

MIT — úsalo como plantilla si te sirve.
