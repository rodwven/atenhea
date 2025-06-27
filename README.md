# Sistema de Notas

Este proyecto incluye un script simple de linea de comandos para gestionar notas con estados.

## Uso

```
python notes.py add "texto de la nota" --status pendiente --shared usuario1,usuario2
python notes.py list
python notes.py status <id> resuelto
python notes.py share <id> otro_usuario
```

Los estados disponibles son `pendiente`, `resuelto`, `listo` y `cerrado`.

Las notas se almacenan en `notes.json` en el mismo directorio.
