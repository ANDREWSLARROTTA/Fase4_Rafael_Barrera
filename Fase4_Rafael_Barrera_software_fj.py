# =========================================================
# SISTEMA INTEGRAL SOFTWARE FJ
# FASE 4 - PROGRAMACIÓN
# RAFAEL ANDRES BARRERA LARROTTA
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# =========================================================

# =========================================================
# IMPORTACIONES
# =========================================================

from abc import ABC, abstractmethod
from datetime import datetime


# =========================================================
# SISTEMA DE LOGS
# =========================================================

def registrar_log(mensaje):

    with open("logs.txt", "a", encoding="utf-8") as archivo:

        archivo.write(f"{datetime.now()} --> {mensaje}\n")


# =========================================================
# EXCEPCIONES PERSONALIZADAS
# =========================================================

class ErrorCliente(Exception):
    """Excepción para errores relacionados con clientes"""
    pass


class ErrorServicio(Exception):
    """Excepción para errores relacionados con servicios"""
    pass


class ErrorReserva(Exception):
    """Excepción para errores relacionados con reservas"""
    pass


# =========================================================
# CLASE ABSTRACTA PRINCIPAL
# =========================================================

class EntidadSistema(ABC):

    @abstractmethod
    def mostrar_detalles(self):
        pass


# =========================================================
# CLASE CLIENTE
# =========================================================

class Cliente(EntidadSistema):

    def __init__(self, identificacion, nombre, correo):

        try:

            if not str(identificacion).isdigit():
                raise ErrorCliente("La identificación debe contener números")

            if len(nombre.strip()) < 3:
                raise ErrorCliente("El nombre debe tener mínimo 3 caracteres")

            if "@" not in correo or "." not in correo:
                raise ErrorCliente("Correo electrónico inválido")

            self.__identificacion = identificacion
            self.__nombre = nombre
            self.__correo = correo

            registrar_log(f"Cliente creado correctamente: {nombre}")

        except ErrorCliente as error:

            registrar_log(f"Error al registrar cliente: {error}")
            raise

    def obtener_nombre(self):
        return self.__nombre

    def obtener_correo(self):
        return self.__correo

    def mostrar_detalles(self):

        return (
            f"Cliente -> ID: {self.__identificacion} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo}"
        )


# =========================================================
# CLASE ABSTRACTA SERVICIO
# =========================================================

class Servicio(ABC):

    def __init__(self, nombre_servicio, tarifa_base):

        if tarifa_base <= 0:
            raise ErrorServicio("La tarifa debe ser mayor que cero")

        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion_servicio(self):
        pass


# =========================================================
# SERVICIO 1 - RESERVA DE SALAS
# =========================================================

class ReservaSala(Servicio):

    def __init__(self, nombre_servicio, tarifa_base, capacidad):

        super().__init__(nombre_servicio, tarifa_base)
        self.capacidad = capacidad

    def calcular_costo(self):

        impuesto = self.tarifa_base * 0.19
        return self.tarifa_base + impuesto

    def descripcion_servicio(self):

        return (
            f"Reserva de Sala -> "
            f"{self.nombre_servicio} | "
            f"Capacidad: {self.capacidad}"
        )


# =========================================================
# SERVICIO 2 - ALQUILER DE EQUIPOS
# =========================================================

class AlquilerEquipo(Servicio):

    def __init__(self, nombre_servicio, tarifa_base, garantia):

        super().__init__(nombre_servicio, tarifa_base)
        self.garantia = garantia

    def calcular_costo(self):

        return self.tarifa_base + self.garantia

    def descripcion_servicio(self):

        return (
            f"Alquiler de Equipo -> "
            f"{self.nombre_servicio} | "
            f"Garantía: {self.garantia}"
        )


# =========================================================
# SERVICIO 3 - ASESORÍAS ESPECIALIZADAS
# =========================================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, nombre_servicio, tarifa_base, nivel):

        super().__init__(nombre_servicio, tarifa_base)
        self.nivel = nivel

    def calcular_costo(self):

        incremento = self.tarifa_base * 0.25
        return self.tarifa_base + incremento

    def descripcion_servicio(self):

        return (
            f"Asesoría Especializada -> "
            f"{self.nombre_servicio} | "
            f"Nivel: {self.nivel}"
        )


# =========================================================
# CLASE RESERVA
# =========================================================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        try:

            if horas <= 0:
                raise ErrorReserva("La duración de la reserva debe ser válida")

            self.cliente = cliente
            self.servicio = servicio
            self.horas = horas
            self.estado = "Pendiente"

            registrar_log("Reserva creada correctamente")

        except ErrorReserva as error:

            registrar_log(f"Error creando reserva: {error}")
            raise

    def confirmar_reserva(self):

        try:

            self.estado = "Confirmada"
            registrar_log("Reserva confirmada")

        except Exception as error:

            raise ErrorReserva(
                "No fue posible confirmar la reserva"
            ) from error

    def cancelar_reserva(self):

        self.estado = "Cancelada"
        registrar_log("Reserva cancelada")

    def calcular_total(self):

        try:

            costo = self.servicio.calcular_costo()
            total = costo * self.horas

        except Exception as error:

            raise ErrorReserva(
                "Error calculando el valor de la reserva"
            ) from error

        else:

            registrar_log(f"Pago calculado correctamente: {total}")
            return total

        finally:

            registrar_log("Proceso de cálculo finalizado")

    def mostrar_resumen(self):

        return (
            f"\nCliente: {self.cliente.obtener_nombre()}\n"
            f"Servicio: {self.servicio.nombre_servicio}\n"
            f"Horas: {self.horas}\n"
            f"Estado: {self.estado}"
        )


# =========================================================
# SIMULACIONES DEL SISTEMA
# =========================================================

print("\n==============================================")
print("INICIO DE SIMULACIONES DEL SISTEMA SOFTWARE FJ")
print("==============================================\n")


# ---------------------------------------------------------
# SIMULACIÓN 1 - CLIENTE VÁLIDO
# ---------------------------------------------------------

try:

    cliente1 = Cliente(
        "1001",
        "Carlos Ramirez",
        "carlos@gmail.com"
    )

    print(cliente1.mostrar_detalles())

except ErrorCliente as error:

    print("Error:", error)


# ---------------------------------------------------------
# SIMULACIÓN 2 - CLIENTE CON NOMBRE INVÁLIDO
# ---------------------------------------------------------

try:

    cliente2 = Cliente(
        "1002",
        "Al",
        "al@gmail.com"
    )

except ErrorCliente as error:

    print("Error detectado:", error)


# ---------------------------------------------------------
# SIMULACIÓN 3 - CLIENTE CON CORREO INVÁLIDO
# ---------------------------------------------------------

try:

    cliente3 = Cliente(
        "1003",
        "Andrea Torres",
        "correo_invalido"
    )

except ErrorCliente as error:

    print("Error detectado:", error)


# ---------------------------------------------------------
# SIMULACIÓN 4 - SERVICIO VÁLIDO
# ---------------------------------------------------------

try:

    servicio1 = ReservaSala(
        "Sala Empresarial",
        120000,
        20
    )

    print(servicio1.descripcion_servicio())

except ErrorServicio as error:

    print("Error:", error)


# ---------------------------------------------------------
# SIMULACIÓN 5 - SERVICIO CON PRECIO INVÁLIDO
# ---------------------------------------------------------

try:

    servicio2 = AlquilerEquipo(
        "Video Beam",
        -50000,
        10000
    )

except ErrorServicio as error:

    print("Error detectado:", error)


# ---------------------------------------------------------
# SIMULACIÓN 6 - ASESORÍA VÁLIDA
# ---------------------------------------------------------

try:

    servicio3 = AsesoriaEspecializada(
        "Consultoría TI",
        250000,
        "Avanzado"
    )

    print(servicio3.descripcion_servicio())

except ErrorServicio as error:

    print("Error:", error)


# ---------------------------------------------------------
# SIMULACIÓN 7 - RESERVA EXITOSA
# ---------------------------------------------------------

try:

    reserva1 = Reserva(
        cliente1,
        servicio1,
        3
    )

    reserva1.confirmar_reserva()

    print(reserva1.mostrar_resumen())

    total = reserva1.calcular_total()

    print(f"Valor total: ${total}")

except ErrorReserva as error:

    print("Error:", error)


# ---------------------------------------------------------
# SIMULACIÓN 8 - RESERVA INVÁLIDA
# ---------------------------------------------------------

try:

    reserva2 = Reserva(
        cliente1,
        servicio1,
        -4
    )

except ErrorReserva as error:

    print("Error detectado:", error)


# ---------------------------------------------------------
# SIMULACIÓN 9 - CANCELACIÓN DE RESERVA
# ---------------------------------------------------------

try:

    reserva3 = Reserva(
        cliente1,
        servicio3,
        2
    )

    reserva3.cancelar_reserva()

    print(reserva3.mostrar_resumen())

except ErrorReserva as error:

    print("Error:", error)


# ---------------------------------------------------------
# SIMULACIÓN 10 - ERROR DE CONVERSIÓN
# ---------------------------------------------------------

try:

    numero = int("texto")

except ValueError as error:

    registrar_log(f"Error de conversión: {error}")

    print("Error detectado en conversión:", error)


# ---------------------------------------------------------
# SIMULACIÓN 11 - ENCADENAMIENTO DE EXCEPCIONES
# ---------------------------------------------------------

try:

    try:

        valor = int("abc")

    except ValueError as error_original:

        raise ErrorCliente(
            "La conversión del dato del cliente falló"
        ) from error_original

except ErrorCliente as error:

    registrar_log(f"Excepción encadenada: {error}")

    print("Error encadenado detectado:", error)


# ---------------------------------------------------------
# SIMULACIÓN 12 - PROCESO FINAL
# ---------------------------------------------------------

try:

    print("\nSistema ejecutado correctamente")
    registrar_log("Sistema ejecutado sin interrupciones")

except Exception as error:

    print("Error inesperado:", error)

finally:

    print("\n==============================================")
    print("FIN DE SIMULACIONES DEL SISTEMA")
    print("==============================================")