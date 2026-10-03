[English](../../security.md) · [العربية](../ar/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Tiếng Việt](../vi/security.md) · [中文（简体）](../zh-Hans/security.md) · [中文（繁體）](../zh-Hant/security.md) · [Deutsch](../de/security.md) · [Русский](../ru/security.md)

[← Volver al inicio en español](../../../i18n/README.es.md)

# Seguridad

## Autorización y límites

Use el puente sólo con un equipo y cuenta UU autorizados. Todo se ejecuta como el usuario Unix conectado en un prefijo Wine dedicado. Xvfb emplea Xauthority sin TCP; las tuberías pertenecen al wineserver del prefijo. Los auxiliares nativos X11 y de terminal usan puertos IPv4 loopback efímeros y tokens nuevos de 256 bits. Los directorios son `0700`, el archivo de entrega del terminal `0600`, con un máximo de cuatro shells.

El VNC del gestor no tiene contraseña propia, pero sólo escucha en loopback y exporta una ventana UU, no el root privado. El relay opcional para Mac usa VNC autenticado a través de SSH. FreeRDP sólo conecta con `127.0.0.1` y comprueba la huella TLS. El listener LAN de GNOME depende de su configuración: proteja el equipo con firewall y contraseña independiente.

## Credenciales y datos

`secret-tool` guarda la contraseña en el keyring de inicio; FreeRDP la recibe por stdin. VNC clásico usa los primeros ocho bytes, con archivo `0600`. El arranque desatendido cifra la contraseña adicional del keyring mediante TPM2/systemd-creds, descifrando sólo en el directorio runtime protegido. El autologin GDM abre el acceso físico después del arranque; TPM no protege frente a procesos del usuario ya conectado y LUKS sigue requiriendo interacción.

Los logs de entrada sólo contienen cantidades, tipos, flags, ruta, resultado y error; nunca caracteres, coordenadas o portapapeles. El terminal no registra órdenes ni salida. El texto semántico tiene un límite de 2.048 registros y queda en el portapapeles tras pegar. No publique tokens, registro, prefijos, logs sin filtrar ni capturas privadas.

## Binarios y mantenimiento

El parcheador sólo acepta un manifiesto `approved` con hash completo, tamaño, firmas únicas y sustituciones de igual longitud. Conserva originales `.uu-original`. El manifiesto 4.42 no autoriza otras versiones. Los borradores requieren revisión semántica independiente; reutilizar el relay requiere coincidencia de fuente, recipe, profile, pins y provenance.

Los instaladores desconocidos se extraen primero sin ejecutarlos. `--sandbox-install` es explícito y usa un staging Bubblewrap/systemd sin red. Wine no es una barrera fuerte entre procesos del mismo usuario. La reparación no aprueba su propio resultado: promover requiere hashes exactos, acceptance comprometida, pruebas reales de controlador/login y al menos 270 segundos estables. La transacción copia todo el prefijo y lo restaura al fallar, sin modificar XRDP.

[Compilación](source-build.md) · [Actualizaciones](automatic-updates.md)

## Comandos y valores técnicos

```text
~/.local/share/wineprefixes/uu-remote
~/.config/uu-remote-bridge/environment
CLIPBOARD / PRIMARY
KEYEVENTF_UNICODE / cliprdr
```

## Código fuente y temas relacionados

- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [patches/freerdp-sdl-product.json](../../../patches/freerdp-sdl-product.json)

Los detalles técnicos están disponibles en inglés y chino simplificado:

- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
