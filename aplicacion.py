import json

class Persona:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

class Comprador(Persona):
    def __init__(self, nombre, email):
        super().__init__(nombre, email)

class Organizador(Persona):
    def __init__(self, nombre, email):
        super().__init__(nombre, email)

class Evento:
    def __init__(self, nombre, fecha, precio_base):
        self.nombre = nombre
        self.fecha = fecha
        self.precio_base = precio_base

    def mostrar_detalle(self):
        raise NotImplementedError("Este método debe ser implementado en las clases derivadas.")

class EventoParrillada(Evento):
    def __init__(self, nombre, fecha, precio_base, tipo_silla):
        super().__init__(nombre, fecha, precio_base)
        self.tipo_silla = tipo_silla

    def mostrar_detalle(self):
        return f"Evento de parrillada '{self.nombre}', Fecha: {self.fecha}, Tipo de silla: {self.tipo_silla}. Precio base: ${self.precio_base}"

class EventoVIP(Evento):
    def __init__(self, nombre, fecha, precio_base, zonavip):
        super().__init__(nombre, fecha, precio_base)
        self.zonavip = zonavip

    def mostrar_detalle(self):
        return f"Evento VIP '{self.nombre}' el {self.fecha}. Precio base: ${self.precio_base}. Lugar VIP: {', '.join(self.zonavip)}"

class Venta:
    def __init__(self, comprador, evento, cantidad):
        self.comprador = comprador
        self.evento = evento
        self.cantidad = cantidad

    def calcular_total(self):
        total_sin_descuento = self.evento.precio_base * self.cantidad
        
        # Aplicar descuento si la cantidad de tickets es mayor o igual a 5
        if self.cantidad >= 5:
            descuento = total_sin_descuento * 0.1  # Supongamos un descuento del 10%
            total_con_descuento = total_sin_descuento - descuento
            return total_con_descuento
        else:
            return total_sin_descuento

class GestorVentas:
    def __init__(self):
        self.ventas = []

    def agregar_venta(self, venta):
        self.ventas.append(venta)

    def generar_reporte_evento(self, evento):
        total_ventas_evento = sum(venta.cantidad for venta in self.ventas if venta.evento == evento)
        return f"Total ventas para el evento '{evento.nombre}': {total_ventas_evento}"

    def generar_reporte_total(self):
        total_ventas = sum(venta.cantidad for venta in self.ventas)
        return f"Total ventas: {total_ventas}"

    def guardar_ventas_json(self, filename):
        ventas_data = []
        for venta in self.ventas:
            venta_data = {
                'comprador': venta.comprador.nombre,
                'evento': venta.evento.nombre,
                'cantidad': venta.cantidad
            }
            ventas_data.append(venta_data)
        
        with open(filename, 'w') as file:
            json.dump(ventas_data, file)

    def cargar_ventas_json(self, filename):
        try:
            with open(filename, 'r') as file:
                ventas_data = json.load(file)
                for venta_data in ventas_data:
                    comprador = Comprador(venta_data['comprador'], "")
                    evento = Evento(venta_data['evento'], "", 0)  # Necesitas cargar el evento desde algún lugar
                    venta = Venta(comprador, evento, venta_data['cantidad'])
                    self.agregar_venta(venta)
        except FileNotFoundError:
            raise FileNotFoundError("El archivo de ventas no existe.")
        except json.JSONDecodeError:
            raise ValueError("El archivo de ventas tiene un formato JSON inválido.")

def mostrar_menu():
    print("1. Agregar venta")
    print("2. Generar reporte por evento")
    print("3. Generar reporte total")
    print("4. Guardar ventas en archivo JSON")
    print("5. Cargar ventas desde archivo JSON")
    print("6. Salir")

def main():
    gestor_ventas = GestorVentas()

    evento_parrillada = EventoParrillada("Parrillada en el parque", "2024-04-01", 20, "Parque Central")
    evento_vip = EventoVIP("VIP BBQ Night", "2024-04-02", 50, ["Asientos reservados", "Catering exclusivo"])

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre_comprador = input("Nombre del comprador: ")
            email_comprador = input("Email del comprador: ")
            comprador = Comprador(nombre_comprador, email_comprador)

            print("Eventos disponibles:")
            print("1. Parrillada en el parque")
            print("2. VIP BBQ Night")
            evento_opcion = input("Seleccione un evento: ")

            cantidad = int(input("Cantidad de tickets: "))

            if evento_opcion == "1":
                venta = Venta(comprador, evento_parrillada, cantidad)
                gestor_ventas.agregar_venta(venta)
                print("Venta agregada con éxito.")
            elif evento_opcion == "2":
                venta = Venta(comprador, evento_vip, cantidad)
                gestor_ventas.agregar_venta(venta)
                print("Venta agregada con éxito.")
            else:
                print("Opción inválida.")

        elif opcion == "2":
            print("Eventos disponibles:")
            print("1. Parrillada en el parque")
            print("2. VIP BBQ Night")
            evento_opcion = input("Seleccione un evento para generar reporte: ")

            if evento_opcion == "1":
                print(gestor_ventas.generar_reporte_evento(evento_parrillada))
            elif evento_opcion == "2":
                print(gestor_ventas.generar_reporte_evento(evento_vip))
            else:
                print("Opción inválida.")

        elif opcion == "3":
            print(gestor_ventas.generar_reporte_total())

        elif opcion == "4":
            filename = input("Ingrese el nombre del archivo JSON para guardar las ventas: ")
            gestor_ventas.guardar_ventas_json(filename)
            print("Ventas guardadas en el archivo JSON.")

        elif opcion == "5":
            filename = input("Ingrese el nombre del archivo JSON para cargar las ventas: ")
            gestor_ventas.cargar_ventas_json(filename)
            print("Ventas cargadas desde el archivo JSON.")

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
