# Historial de Versiones

## [Versión 0.0.1] - 2025-03-01
- Primera versión del sistema.
### Añadido
- Métodos CRUD básicos para manejar usuarios.
- Lógica de autenticación en obtención de usuario a partir de login.

### Observaciones
- Esta es la primera versión desplegada sin testing de funcionamiento, las pruebas se realizaron
en un ámbito sencillo y básico sin documentación alguna. Se llevó a cabo de esta manera por la
necesidad de tener un pie de inicio del cual partir en cuanto al sistema. En posteriores versiones
se mejorará la aplicación de buenas prácticas en el código y testing unitario documentado para
asegurar una integridad más robusta del sistema.

## [Versión 0.1.0] - 2025-03-22
### Añadido
- Autorización mediante JWT en métodos que modifiquen datos de un usuario registrado.
    - Autorización al intentar obtener los datos del usuario a través de login (Como lo hacía la anterior
    versión)
    - Necesidad de autorización al intentar modificar datos del usuario.
    - Necesidad de autorización al intentar eliminar el usuario.

### Cambiado
- Cambios mínimos en servicios de base de datos
    - Implementación de inyección de dependencias con la conexión de la base de datos, logrando así un 
    desacoplamiento tanto con la librería utilizada para la conexión.
    - Implementación de patrón adaptador en las conexiones a base de datos, dando robustez y una menor
    dependencia del sistema a un único tipo de conexión con base de datos.

### Corregido
- Testing de funcionalidad faltantes

## [Versión 0.2.0] - 2025-04-06
### Añadido
- Implementación de recuperación de contraseña mediante email.
    - Implementación de un nuevo método para obtener el usuario a partir de su email.
    - Implementación de un nuevo método para enviar un email al usuario con un token de recuperación
    de contraseña.
    - Implementación de un nuevo método para cambiar la contraseña del usuario a partir del token enviado luego de validar el código de recuperación.

## [Versión 0.2.1] - 2025-04-07
### Corregido
- Error en la carga de .env

## [Versión 0.2.2] - 2025-04-07
### Corregido
- Error en la llamada del endpoint de obtención de usuario a partir del token. (/user/me).

## [Versión 0.2.3] - 2025-04-08
### Corregido
- Corrección en implementacion de singleton en clase EnvManager