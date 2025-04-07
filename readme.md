# User Manager

Como desarrolladores, muchas veces nos encontramos con la necesidad de agregar a nuestros proyectos alguna implementación capaz de gestionar usuarios, por ejemplo, registrarlos, modificarlos, actualizarlos y también eliminarlos. Aunque al principio esta tarea pueda parecer sencilla, a medida que el proyecto avanza es común que esta implementación se vuelva compleja y poco estructurada. En esos casos, solemos desviarnos de nuestro proyecto principal para poder mejorar y aplicar las mejores prácticas a ese subproyecto de gestión de usuarios, lo que resulta en una pérdida de tiempo valioso para nosotros.

La reflexión anterior fue el punto de apoyo que me llevó a crear esta API, la cual cumple con las características esenciales que, a mi parecer, debe tener, mínimamente, todo sistema de gestión de usuarios: gestión del ciclo de vida del usuario, seguridad mediante autenticación y autorización, escalabilidad y simplicidad de uso.

---

## Descripción

User Manager es una API para gestionar usuarios. Permite crear, editar, eliminar y listar usuarios de manera eficiente y segura.

---

## Accesos rápidos
- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación y configuración del backend](#instalación-y-configuración-del-backend)
- [Consumo de API](#consumo-de-api)
- [Endpoints](#endpoints)
- [Configuración de base de datos](#configuracion-de-base-de-datos)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Características

- Crear nuevos usuarios.
- Editar información de usuarios existentes.
- Eliminar usuarios.
- Listar todos los usuarios.
- Autenticación y autorización mediante JWT (JSON Web Token).
- Recuperación de contraseña mediante correo electrónico.

---

## Tecnologías
- **Lenguaje de programación:** Python
- **Framework web:** FastAPI
- **Base de datos:** SQLite (por defecto)
- **Autenticación y autorización:** JSON Web Token (JWT) y Oauth2
- **Gestión de dependencias:** pip
- **Pruebas:** pytest
- **Control de versiones:** Git
- **Documentación de API:** OpenAPI (generada por FastAPI)


## Instalación y configuración del backend

### Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/josemoyano04/user-manager.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd user-manager
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

---

### Configuración

Para iniciar la aplicación, es necesario seguir a detalle los siguientes pasos para evitar errores:

1. Dentro del directorio raíz, crea un archivo `.env` vacío:
    ```bash
    # Windows:
    type NUL > .env

    # Unix:
    touch .env
    ```

    > **⚠️ ADVERTENCIA:** Ten cuidado en este punto y verifica que no exista un archivo llamado `.env` en la carpeta donde se ejecuta el comando, ya que al hacerlo se sobreescribirá el nuevo archivo vacío sobre el anterior.

---

2. Dentro del archivo `.env` es necesario que agregues las siguientes variables:

    ```python
    # Constantes de configuración de la base de datos
    PRODUCTION_DATABASE_URL = example_url
    PRODUCTION_DATABASE_AUTH_TOKEN = example_token

    # Constantes de configuración del JSON Web Token
    JWT_SECRET_KEY = 6403a23f63970faa4649f44a9ad4fdbe06db3c00f5c7cb9b3773ee481c60a47d
    JWT_ALGORITHM = HS256
    JWT_EXPIRE_MINUTES = 120
    ```

    > **NOTA:** Se recomienda ejecutar el comando `openssl rand -hex 32` en bash para obtener un hexadecimal aleatorio de 32 bits y almacenarlo en la variable `JWT_SECRET_KEY`.

    ```bash
    openssl rand -hex 32

    # Output:
    6403a23f63970faa4649f44a9ad4fdbe06db3c00f5c7cb9b3773ee481c60a47d
    ```

---

> **‼️ IMPORTANTE:** Por defecto, el sistema está configurado para conectarse a una base de datos SQLite desplegada. Si te interesa implementar un tipo de base de datos distinto, desplázate hacia la sección de `CONFIGURACIÓN DE BASE DE DATOS`.

---

3. Ejecuta los tests desde el directorio raíz para verificar que todo funciona correctamente:
    ```bash
    python -m pytest . -v
    ```

---

4. Inicia la aplicación en local con:
    ```bash
    python -m fastapi dev main.py
    ```

---

## Consumo de API
Documentación generada por FastAPI usando OpenAPI: [Documentación](https://user-manager-mi2a.onrender.com/docs)

>**NOTA:** Si realiza modificaciones, puede ver la documentación actualizada en tiempo real ejecutando la aplicación con `python -m fastapi dev main.py` y accediendo a la ruta [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints

### Agregar un usuario:
**Endpoint**: /user/register

**Descripción**: Este endpoint permite registrar un nuevo usuario en el sistema. Se debe enviar un JSON con los datos del usuario a registrar.

**Método**: POST

**Autenticación**: No requiere autenticación.

**Elementos del body**:
* <strong> user[objet]: </strong> Objeto que contiene los datos del usuario a registrar. Este campo es obligatorio y debe contener los siguientes campos:
    * <strong> full_name[str]: </strong> Nombre completo del usuario.
    * <strong> username[str]: </strong> Nombre de usuario. Este campo es único y no puede repetirse entre usuarios.
    * <strong> email[str]: </strong> Correo electrónico del usuario. Este campo es único y no puede repetirse entre usuarios.
    * <strong> password[str]: </strong> Contraseña del usuario.

**Ejemplo de uso con javascript**:
```javascript
//Javascript
//Modificar con URL de la API desplegada para uso en producción
const API_URL = "http://127.0.0.1:8000";
const ENDPOINT = "/user/register";
fetch(`${API_URL}${ENDPOINT}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        user: {
            full_name: "example",
            username: "example",
            email: "user@example.com",
            password: "example"
        }
    })
})
.then(response => response.json())
.then(data => {
    console.log('Success:', data);
})
.catch((error) => {
    console.error('Error:', error);
});

```

**Respuesta OK**:
```json
{
  "status": "success",
  "data": {
    "user": {
      "full_name": "example",
      "username": "example",
      "email": "example@example.com"
    }
  },
  "message": "Usuario registrado correctamente."
}
```

**Descripcion de codigos de error:**
- **409 - Conflict**: El usuario que intenta agregar tiene el username o email ya registrado para otro usuario.
- **500 - Internal Server Error**: Error del lado del servidor. Crear un issue reportando el error para solucionarlo lo más pronto posible.

### Inicio de sesión de usuario (Obtención de JSON Web Token):
**Endpoint**: /login

**Descripción**: Este endpoint permite iniciar sesión y obtener un token JWT para autenticar al usuario en futuras solicitudes.

**Método**: POST

**Autenticación**: No requiere autenticación.

**Content-type**: application/x-www-form-urlencoded

**Elementos del formulario**:
* <strong>username[str]: </strong> Nombre de usuario.
* <strong>password[str]: </strong> Contraseña de usuario.

**Ejemplo de uso con javascript**:

```javascript
//Javascript
//Modificar con URL de la API desplegada para uso en producción
const API_URL = "http://127.0.0.1:8000"
const ENDPOINT = "/login"

let data = new URLSearchParams()
let username = "example"
let password = "example"
data.append("username", username);
data.append("password", password);

fetch(`${API_URL}${ENDPOINT}`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: data.toString()
    })
.then(response => response.json())
.then(data => {
    console.log('Success:', data);
    const TOKEN = data.access_token // <-- JWT 
})
.catch((error) => {
    console.error('Error:', error);
});

```

**Respuesta OK**:
```json
{
  "status": "success",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJleGFtcGxlIiwiZXhwIjoxNzQyODY0OTk1fQ.db3VJJtciotJmgEE4f6jUDzCzolgLJ9ng_2X-DwI0FQ",
  "token_type": "Bearer"
}
```

**Descripción de códigos de error**:
- **401 - Unauthorized**: El username o password son incorrectos.
- **500 - Internal Server Error**: Error del lado del servidor. Crear un issue reportando el error para solucionarlo lo más pronto posible.

### Recuperar datos del usuario:

**Endpoint**: /user/me

**Descripción**: Este endpoint permite recuperar los datos del usuario autenticado. Se debe enviar el token JWT en la cabecera de la solicitud.

**Método**: GET

**Autenticación**: Bearer Token

**Content-type**: application/json 

**Ejemplo de uso con javascript**:

```javascript
//Javascript
//Modificar con URL de la API desplegada para uso en producción
const API_URL = "http://127.0.0.1:8000";
const ENDPOINT = "/user/me";

fetch(`${API_URL}${ENDPOINT}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${TOKEN}` // <-- JWT obtenido en el login
    }
})
.then(response => response.json())
.then(data => {
    console.log('User Data:', data);
})
.catch((error) => {
    console.error('Error:', error);
});
```

**Respuesta OK**:
```json
{
  "status": "success",
  "data": {
    "full_name": "example",
    "username": "example",
    "email": "example@example.com",
    "password": "$2b$12$XhjpCAjMyPqAn1.fs1KygexbqxjutGpzw9eA313cjXx5zkimQtC2K"
  }
}
```

**Descripción de códigos de error**:
- **400 - Bad Request**: Token inválido por formato incorrecto o por expiración.
- **401 - Unauthorized**: El token proporcionado tiene un formato incorrecto o está expirado.
- **404 - Not Found**: El username no se encontró en la base de datos.
- **500 - Internal Server Error**: Error del lado del servidor. Crear un issue reportando el error para solucionarlo lo más pronto posible.


### Modificar datos del usuario:
**Endpoint**: /user/update

**Descripción**: Este endpoint permite modificar los datos del usuario autenticado. Se debe enviar el token JWT en la cabecera de la solicitud.

**Método**: PUT

**Autenticación**: Bearer Token

**Content-type**: application/json

**Elementos del body**:
* <strong> updated_user[object]: </strong> Objeto que contiene los nuevos datos del usuario, los datos que no quieran modificarse, deben colocarse igual a los actuales. Este campo es obligatorio y debe contener los siguientes campos:
    * <strong> full_name[str]: </strong> Nombre completo del usuario.
    * <strong> username[str]: </strong> Nombre de usuario. Este campo es único y no puede repetirse entre usuarios.
    * <strong> email[str]: </strong> Correo electrónico del usuario. Este campo es único y no puede repetirse entre usuarios.
    * <strong> password[str]: </strong> Contraseña del usuario.

**Ejemplo de uso con javascript**:
```javascript
//Javascript
//Modificar con URL de la API desplegada para uso en producción
const API_URL = "http://127.0.0.1:8000";
const ENDPOINT = "/user/update";

fetch(`${API_URL}${ENDPOINT}`, {
    method: "PUT",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${TOKEN}` // <-- JWT obtenido en el login
    },
    body: JSON.stringify({
        username: "example" // <-- Username previo a actualizar
        updated_user: {
            //Nuevos datos
            full_name: "new_example",
            username: "new_example",
            email: "new_user@example.com",
            password: "new_example"
        }
    })
})
.then(response => response.json())
.then(data => {
    console.log('User Updated:', data);
})
.catch((error) => {
    console.error('Error:', error);
});
```

**Respuesta OK**:
```json
{
  "status": "success",
  "message": "Usuario actualizado con éxito."
}
```

**Descripción de códigos de error**:
- **401 - Unauthorized**: El token proporcionado tiene un formato incorrecto o está expirado.
- **409 - Conflict**: El usuario que intenta agregar tiene el username o email ya registrado para otro usuario.
- **500 - Internal Server Error**: Error del lado del servidor. Crear un issue reportando el error para solucionarlo lo más pronto posible.

### Eliminar usuario: 
**Endpoint**: /user/delete

**Descripción**: Este endpoint permite eliminar el usuario autenticado. Se debe enviar el token JWT en la cabecera de la solicitud.

**Método**: DELETE

**Autenticación**: Bearer Token

**Content-type**: application/json

**Ejemplo de uso con javascript**:
```javascript
//Javascript
//Modificar con URL de la API desplegada para uso en producción
const API_URL = "http://127.0.0.1:8000";
const ENDPOINT = "/user/delete";

fetch(`${API_URL}${ENDPOINT}`, {
    method: "DELETE",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${TOKEN}` // <-- JWT obtenido en el login
    }  
})
.then(response => response.json())
.then(data => {
    console.log('User Deleted:', data);
})
.catch((error) => {
    console.error('Error:', error);
});
```

**Response OK:**
```json
{
  "status": "success",
  "data": "example",
  "message": "Usuario 'example' eliminado con éxito."
}
```

**Descripción de códigos de error**:
- **401 - Unauthorized**: El token proporcionado tiene un formato incorrecto o está expirado.
- **409 - Conflict**: El usuario que intenta agregar tiene el username o email ya registrado para otro usuario.
- **500 - Internal Server Error**: Error del lado del servidor. Crear un issue reportando el error para solucionarlo lo más pronto posible.

---

### Enviar email para recuperar contraseña: 
**Endpoint**: /recovery-password/request

**Descripción**: Este endpoint permite enviar un correo electrónico al usuario para restablecer su contraseña.

**Método**: POST

**Autenticación**: No requiere autenticación.

**Content-type**: application/json

**Elementos del body**:
* <strong> receiver_email[str]: </strong> Correo electrónico del usuario que solicita el cambio de contraseña.

* <strong> sender_email[str]: </strong> Correo electrónico del remitente. Este correo debe ser el mismo que se utiliza para enviar el correo de recuperación de contraseña.

* <strong> password_email[str]:</strong> Contraseña del correo electrónico del remitente. Este correo debe ser el mismo que se utiliza para enviar el correo de recuperación de contraseña.
    > **NOTA:** Se recomienda generar una contraseña de aplicación para tu correo electrónico. Si usas Gmail, puedes seguir [esta guía](https://support.google.com/mail/answer/185833?hl=es) para crear una contraseña de aplicación.  Si usas otro proveedor de correo electrónico, consulta la documentación de tu proveedor para obtener información sobre cómo generar una contraseña de aplicación.

* <strong> email_template_html[str]:</strong> Plantilla HTML del correo electrónico que se enviará al usuario para la recuperación de contraseña. Esta plantilla debe contener un enlace para que el usuario pueda restablecer su contraseña. IMPORTANTE: Para que la plantilla funcione, es necesario tener las sigueintes etiqueta:

    * <strong> < strong id="username-to-recovering-password"> AQUI IRA EL NOMBRE DE USAURIO < strong > </strong> 
    <br>
    <br>
    * <strong> < div id="password-recovery-code" > AQUI IRA EL CODIGO< /div > </strong> 
    <br>
    <br>
    >**IMPORTANTE**: Es de suma importancia respetar esas etiquetas en el template para que al recibirlo, el backend pueda reemplazar el nombre de usuario y el código de recuperación por los correspondientes al usuario que lo solicita. 
    <br>
    <br>

    Si quiere usar la plantilla por defecto, enviar null en ese campo

* <strong> custom_code[str]: </strong> Código personalizado que se puede incluir en el correo electrónico. Este código puede ser utilizado para personalizar el mensaje o para incluir información adicional. Se recomienda dejar la variable en null para que el backend genere un código aleatorio y único para cada usuario. Este código se enviará al correo electrónico del usuario y se utilizará para verificar la identidad del usuario al restablecer su contraseña.


**Ejemplo de uso con javascript**:
```javascript
//Javascript
//Modificar con URL de la API desplegada para uso en producción
const API_URL = "http://127.0.0.1:8000";
const ENDPOINT = "/recovery-password/request";

fetch(`${API_URL}${ENDPOINT}`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    }
    body: JSON.stringify({
        {
        receiver_email: "user@example.com",
        sender_email: "adminEmail@example.com",
        password_email: "passwordEmail",
        email_template_html: "<html in string>" //o null,
        custom_code: "custom code" //o null 
        }
    })
})
.then(response => response.json())
.then(data => {
    console.log('Data:', data);
})
.catch((error) => {
    console.error('Error:', error);
});
```

**Respuesta OK****:
```json
{
  "status": "success",
  "message": "Código de recuperación enviado correctamente."
}
```

**Descripción de códigos de error**:
- **404 - Not Found**: El email no fue encontrado en la base de datos
- **500 - Internal Server Error**: Error del lado del servidor. Crear un issue reportando el error para solucionarlo lo más pronto posible.


###Recuperar contraseña: /user/recovery

### Verificar código de recuperación:
**Endpoint**: [/recovery-password/verify-code]()

**Descripción**: Este endpoint permite verificar el código de recuperación enviado al correo electrónico del usuario.

**Método**: POST

**Autenticación**: No requiere autenticación.

**Content-type**: application/json

**Elementos del body**:
* <strong> code[str]: </strong> Código de recuperación enviado al correo electrónico del usuario. Este campo es obligatorio.
* <strong> user-email[str]: </strong> Correo electrónico del usuario. Este campo es obligatorio y debe coincidir con el email a donde se envio el código de recuperación.

**Ejemplo de uso con javascript**:
```javascript
//Javascript
//Modificar con URL de la API desplegada para uso en producción
const API_URL = "http://127.0.0.1:8000";
const ENDPOINT = "/recovery-password/verify-code";

fetch(`${API_URL}${ENDPOINT}`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    }
    body: JSON.stringify({
        code: "12345", // Código de ejemplo.
        user_email: "example@example.com" 
    })
})
.then(response => response.json())
.then(data => {
    console.log('Data:', data);
})
.catch((error) => {
    console.error('Error:', error);
});
```

**Respuesta OK**:
```json
{
  "status": "success",
  "message": "Código de recuperación verificado correctamente.",
  "token": "EXAMPLE_TOKEN_abcdefghijklmnopqrstuvwxyz"
}
```
**Descripción de códigos de error**:
* **400 - Bad Request**: El código de recuperación no es válido o ha expirado.
* **404 - Not Found**: El email no fue encontrado en la base de datos.
* **500 - Internal Server Error**: Error del lado del servidor. Crear un issue reportando el error para solucionarlo lo más pronto posible.

### Cambiar contraseña:
**Endpoint**: [/recovery-password/reset]()

**Descripción**: Este endpoint permite cambiar la contraseña del usuario. Se debe enviar el token JWT en la cabecera de la solicitud.

**Método**: POST

**Autenticación**: Bearer Token

**Content-type**: application/json

**Elementos del body**:
* <strong> email[str]: </strong> Correo electrónico del usuario. Este campo es obligatorio y debe coincidir con el email a donde se envio el código de recuperación.
* <strong> new_password[str]: </strong> Nueva contraseña del usuario. Este campo es obligatorio y debe cumplir con los requisitos de seguridad establecidos en el sistema.

**Ejemplo de uso con javascript**:
```javascript
//Javascript
//Modificar con URL de la API desplegada para uso en producción
const API_URL = "http://127.0.0.1:8000";
const ENDPOINT = "/recovery-password/reset";

fetch(`${API_URL}${ENDPOINT}`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${TOKEN}` // <-- JWT obtenido desde el endpoint /recovery-password/verify-code
    }
    body: JSON.stringify({
        email: "example@example.com",
        new_password: "new_password"
    })
})
.then(response => response.json())
.then(data => {
    console.log('Data:', data);
})
.catch((error) => {
    console.error('Error:', error);
});
```

**Respuesta OK**:
```json
{
  "status": "success",
  "message": "Contraseña cambiada correctamente."
}
```

**Descripción de códigos de error**:
* **401 - Unauthorized**: El token proporcionado tiene un formato incorrecto o está expirado.
* **500 - Internal Server Error**: Error del lado del servidor. Crear un issue reportando el error para solucionarlo lo más pronto posible.


## Configuracion de base de datos

La estructura de este proyecto es escalable para agregar nuevas conexiones a distintos tipos de bases de datos si no se desea mantener únicamente una conexión con `sqlite`. Todo esto es posible gracias a la aplicación del patrón de diseño "Adapter". Implementar esta funcionalidad es relativamente sencillo. A continuación, se detallan algunos puntos generales como guía para agregar dichas modificaciones:

---

### Guía para la Implementación

1. Observando la distribución de directorios, se puede notar que hay una carpeta `adapters` dentro del directorio raíz del proyecto. Dentro de la carpeta mencionada se encuentra la clase abstracta `DatabaseConnection`, utilizada como interfaz para definir las conexiones a la base de datos. Esta clase incluye tres métodos abstractos que cada nueva subclase debe implementar.

<p align="center">
    <img src="src/images/adapter_folder.png" alt="Descripción de la imagen">
</p>

2. Dentro de `adapters`, crea un nuevo fichero con un nombre descriptivo para mantener una estructura limpia.
<p align="center">
    <img src="src/images/adapter_folder_new_file.png" alt="Descripción de la imagen">
</p>


3. En el nuevo fichero, es necesario crear una clase que herede de `DatabaseConnection` e implemente los métodos abstractos, por ejemplo:
    ```python
    from adapters.database_connection import DatabaseConnection
    import mysql.connector
    from mysql.connector import MySQLConnection, Error
    from errors.database_errors import DatabaseConnectionError, DatabaseQueryError

    class AdapterDBConnMySQLClient(DatabaseConnection):
        __instance = None

        def __new__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = super().__new__(cls)
            return cls.__instance
        
        def __init__(self, host: str, user: str, password: str, database: str):
            if not hasattr(self, "__initialized"):
                self.__initialized = True
                self.host = host
                self.user = user
                self.password = password
                self.database = database
                self.current_client: MySQLConnection = None
                
        def connect(self) -> None:
            if self.current_client is None:
                try:
                    self.current_client = mysql.connector.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=self.database
                    )
                except Error as error:
                    raise DatabaseConnectionError(str(error))
            
        def execute(self, query: str, params: list = []) -> list[tuple]:
            if self.current_client is None:
                raise DatabaseConnectionError("La conexión a la base de datos está cerrada.")
            
            try:
                cursor = self.current_client.cursor()
                cursor.execute(query, params)
                if query.strip().lower().startswith("select"):
                    results = cursor.fetchall()
                    return results
                else:
                    self.current_client.commit()
                    return cursor.rowcount
            except Error as error:
                raise DatabaseQueryError(str(error))
            finally:
                cursor.close()
            
        def close(self) -> None:
            if self.current_client is not None:
                self.current_client.close()
                self.current_client = None

    ```

4. Una vez creada la clase, se recomienda escribir pruebas correspondientes para validar que no haya fallos en la nueva implementación.

5. En el directorio raíz existe otra carpeta llamada `connections`, donde se encuentra un fichero con un método que construye y retorna la conexión a la base de datos correspondiente.

6. Dentro del fichero mencionado en el punto 5, crea una nueva función que siga la premisa de mantener dicho fichero como el responsable de contener funciones encargadas de construir y retornar conexiones a bases de datos. Puedes usar como guía la función `db_conn_libsql_client`, ubicada dentro del fichero, por ejemplo:
    ```python
    from utils.env_loader import EnvManager
    from adapters.adapter_db_conn_mysql import AdapterDBConnMySQLClient

    def db_conn_mysql_client() -> AdapterDBConnMySQLClient:
        ENV = EnvManager()

        HOST = ENV.get("MYSQL_HOST")
        USER = ENV.get("MYSQL_USER")
        PASSWORD = ENV.get("MYSQL_PASSWORD")
        DATABASE = ENV.get("MYSQL_DATABASE")

        DB_CONN = AdapterDBConnMySQLClient(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        return DB_CONN

    ```
>**NOTA** Asegurarse de agregar las correspondientes variables de entornos en el fichero `.env` para evitar errores.


7. Una vez creada la función, dirígete a cada router dentro del directorio `routers` y modifica la constante `DB_CONN` para que almacene la conexión retornada por la nueva función creada.

``` python
from fastapi import APIRouter, Depends
from controllers import auth_controller as at
from connections.db_connection import db_conn_mysql_client
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

#DATABASE CONNECTION CONSTANTS
DB_CONN = db_conn_mysql_client() # <-- Nueva funcion

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl= "/login")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res = await at.login_for_access_token_controller(db_conn= DB_CONN, 
                                                     form_data= form_data)
    return res

#Continuar la modificacion en el resto de routers
```

---

Con esta guía, podrás mantener una estructura escalable y flexible que facilite la integración de múltiples tipos de bases de datos en el proyecto.

---


## Contribuir

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`) usa `feature` en el pie de la rama para nuevas implementacions y `fix` para corrección de errores.
3. Realiza tus cambios y haz un commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Esto significa que puedes usar, modificar y distribuir este software de forma libre, siempre que cumplas con los términos de la Licencia MIT. 

**Nota:** El uso de este proyecto queda completamente bajo la responsabilidad del usuario. El autor no se hace responsable por cualquier resultado, mal uso o daño causado por el uso de este software. Consulta el archivo [LICENSE](LICENCE.md) para más detalles.
