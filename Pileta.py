import datetime

import PySimpleGUI as sg
import pickle

#https://github.com/PySimpleGUI/PySimpleGUI/issues/362 hacer funcion
# para crear los layouts de forma individual y asignarlo cada vez que lo vaya a usar


class Alumnos:

    def __init__(self):
        try:
            sg.Popup("Cargando base de datos...")
            with open("alumnos.pkl", "rb") as alumnos:
                self.alumnos = pickle.load(alumnos)
                sg.Popup("Base de datos de alumnos cargada")
        except FileNotFoundError:
            sg.Popup("Archivo no encontrado :(")
            self.alumnos = {}
        try:
            with open("horarios.pkl", "rb") as horarios_read:
                self._horarios = pickle.load(horarios_read)
                sg.Popup("Base de datos de horarios cargada")
        except FileNotFoundError:
            self._horarios = {"Martes": {"17:30": {"Menores": [{}, 0], "Mayores": [{}, 0]},
                                         "18:30": {"Menores": [{}, 0], "Mayores": [{}, 0]},
                                         "19:30": {"Menores": [{}, 0], "Mayores": [{}, 0]}
                                         },
                              "Jueves": {"17:30": {"Menores": [{}, 0], "Mayores": [{}, 0]},
                                         "18:30": {"Menores": [{}, 0], "Mayores": [{}, 0]},
                                         "19:30": {"Menores": [{}, 0], "Mayores": [{}, 0]}
                                         },
                              "Viernes": {"17:30": {"Menores": [{}, 0], "Mayores": [{}, 0]},
                                          "18:30": {"Menores": [{}, 0], "Mayores": [{}, 0]},
                                          "19:30": {"Menores": [{}, 0], "Mayores": [{}, 0]}
                                          }}
        self.dia = None
        self.hora = None

    def guardar(self):
        with open("alumnos.pkl", "wb") as alumnos:
            pickle.dump(self.alumnos, alumnos)
        with open("horarios.pkl", "wb") as horarios:
            pickle.dump(self._horarios, horarios)
        sg.Popup("Guardado correctamente")

    def agregar_alumno(self, nombre, apellido, dni, edad, dias):
        fecha = datetime.date.today()
        self.alumnos[f"{str(dni)}"] = [f"{nombre + ' ' + apellido}",
                                       {"Fecha de inscripcion": f"{fecha}",
                                          "Fecha de pago": None,
                                          "Deuda": f"${0}",
                                          "Clases mensuales": dias * 4,
                                          "Edad": edad,
                                          "Dias/Horarios": None}]

    def agregar_a_horario(self, dni):
        edad = self.alumnos[f"{str(dni)}"][1]["Edad"]
        nombre_completo = self.alumnos[f"{str(dni)}"][0]
        try:
            if (str(dni) in self._horarios[self.dia][self.hora]["Mayores"][0]) or \
                    (str(dni) in self._horarios[self.dia][self.hora]["Menores"][0]):

                sg.Popup(f"Error: El alumno {nombre_completo} "
                        f"ya se encuentra inscripto el dia {self.dia} en el horario {self.hora}")

            else:
                if (edad <= 12 and self._horarios[self.dia][self.hora]["Menores"][1] > 10) \
                        or (edad > 12 and self._horarios[self.dia][self.hora]["Mayores"][1] > 25):
                    print(f"Error: El dia {self.dia, self.hora}, no esta disponible")

                else:
                    if edad > 12:
                        self._horarios[self.dia][self.hora]["Mayores"][0][f"{dni}"] = f"{nombre_completo}"
                        self._horarios[self.dia][self.hora]["Mayores"][1] += 1
                        sg.Popup(f"Alumno {nombre_completo} agregado al dia {self.dia, self.hora}")

                    else:
                        self._horarios[self.dia][self.hora]["Menores"][0][f"{dni}"] = f"{nombre_completo}"
                        self._horarios[self.dia][self.hora]["Menores"][1] += 1
                        sg.Popup(f"Alumno {nombre_completo} agregado al dia {self.dia, self.hora}")
        except KeyError:
            sg.Popup("Alumno no encontrado, por favor verifique los datos.")

    def modificar_horario(self, dni):
        pass

    def horarios_de_alumno(self, dni):
        horarios_alumno = []
        for dia in self._horarios:
            for horario in self._horarios[dia]:
                if dni in self._horarios[dia][horario]["Menores"][0] or dni in self._horarios[dia][horario]["Mayores"][0]:
                    horarios_alumno.append([dia, horario])
        self.alumnos[f"{str(dni)}"][1]["Dias/Horarios"] = horarios_alumno

    def agregar_deuda(self, dias, dni):

        if dias == 1:
            self.alumnos[f"{str(dni)}"][1]["Deuda"] = 3000
        elif dias == 2:
            self.alumnos[f"{str(dni)}"][1]["Deuda"] = 3600
        elif dias == 3:
            self.alumnos[f"{str(dni)}"][1]["Deuda"] = 4200
        self.horarios_de_alumno(dni)

    def agregar_pago(self, dni, monto):
        try:
            if monto >= self.alumnos[f"{str(dni)}"][1]["Deuda"]:
                sg.Popup(f"El vuelto es de ${(int(self.alumnos[f'{str(dni)}'][1]['Deuda']) - monto)*-1}")
                self.alumnos[f"{str(dni)}"][1]["Deuda"] = 0

            else:
                self.alumnos[f"{str(dni)}"][1]["Deuda"] = int(self.alumnos[f"{str(dni)}"][1]["Deuda"]) - monto
            self.alumnos[f"{str(dni)}"][1]["Fecha de pago"] = f"{datetime.date.today()}"
        except (KeyError, ValueError):
            if KeyError:
                sg.Popup("Error! El alumno no esta en la base de datos")
            elif ValueError:
                sg.Popup("Error! El valor ingresado debe ser numerico")

    def eliminar_alumno(self, dni):

        if str(dni) not in self.alumnos:
            sg.Popup("Alumno no encontrado")
        else:
            for dia in self._horarios:
                for horario in self._horarios[dia]:
                    if dni in self._horarios[dia][horario]["Menores"][0]:
                        self._horarios[dia][horario]["Menores"][0].pop(dni)
                        self._horarios[dia][horario]["Menores"][1] -= 1
                    elif dni in self._horarios[dia][horario]["Mayores"][0]:
                        self._horarios[dia][horario]["Mayores"][0].pop(dni)
                        self._horarios[dia][horario]["Mayores"][1] -= 1

            sg.Popup(f"Alumno {self.alumnos[str(dni)][0]} eliminado")
            self.alumnos.pop(str(dni))

    def mostrar_alumnos(self):
        sg.Popup(self.alumnos)

    def mostrar_horarios(self):
        horarios = []
        for dia in self._horarios:
            horarios.append(dia)
            for horario in self._horarios[dia]:
                horarios.append(f"{horario, self._horarios[dia][horario]}")
        return horarios

    def mostrar_deuda(self, dni):
        try:
            sg.Popup(f"La deuda de {self.alumnos[str(dni)][0]} es de ${self.alumnos[str(dni)][1]['Deuda']}")
        except KeyError:
            sg.Popup("Alumno no encontrado, por favor verifique los datos.")


class Interfaz:
    sg.theme("SystemDefaultForReal")

    def __init__(self):
        self.tamano_boton_main = (13, 3)
        self.tamano_boton_hr = (5, 2)

    """
    MENU
    """
    def menu(self):

        while True:
            main = self.main_menu_interfaz()
            event, values = main.read()
            if event == sg.WIN_CLOSED or event == "-cancel-":
                agenda.guardar()
                main.close()
                break
            elif event == "-0-":
                main.close()
                self.agregar_alumno()

            elif event == "-1-":
                main.close()
                self.registrar_pagos()

            elif event == "-2-":
                main.close()
                self.eliminar_alumno()

            elif event == "-3-":
                main.close()
                self.mostrar_deuda()

            elif event == "-4-":
                main.close()
                self.mostrar_horarios()

            elif event == "-5-":
                agenda.mostrar_alumnos()

            elif event == "-save-":
                agenda.guardar()

    """
    INTERFACES
    """

    # main

    def main_menu_interfaz(self):
        layout = [[sg.Button("Agregar alumnos", key="-0-", size=self.tamano_boton_main),
                   sg.Text("   "),
                   sg.Button("Registrar Pagos", key="-1-", size=self.tamano_boton_main),
                   sg.Text("   "),
                   sg.Button("Eliminar Alumnos", key="-2-", size=self.tamano_boton_main)],

                  [sg.Button("Mostrar Deuda de Alumno", key="-3-", size=self.tamano_boton_main),
                   sg.Text("   "),
                   sg.Button("Mostrar Horarios", key="-4-", size=self.tamano_boton_main),
                   sg.Text("   "),
                   sg.Button("Mostrar Alumnos", key="-5-", size=self.tamano_boton_main)],

                  [sg.Button("Ok"),
                   sg.Button("Cerrar", key="-cancel-"),
                   sg.Button("Guardar", key="-save-")]]

        return sg.Window("Natacion", layout, margins=(100, 100))

    # otras

    def crear_pagos_interfaz(self):
        registrar_pago_interfaz = [[sg.Text("Introduzca el monto: "), sg.Input()],
                                        [sg.Text("Introduzca el dni: "), sg.Input()],
                                        [sg.Button('Ok'), sg.Button('Cancel', key="-cancel-")]]
        return sg.Window("Registrar Pago", registrar_pago_interfaz, margins=(100, 100))

    def agregar_alumnos_interfaz(self):
        agregar_alumno_interfaz = [[sg.Text("Introduza el nombre: "), sg.Input()],
                                   [sg.Text("Introduza el apellido: "), sg.Input()],
                                   [sg.Text("Introduza el dni: "), sg.Input()],
                                   [sg.Text("Introduza la edad: "), sg.Input()],
                                   [sg.Text("Introduza la cantidad de dias: "), sg.Input()],
                                   [sg.Button('Ok'), sg.Button('Cancel', key="-cancel-")]]
        return sg.Window("Agregar alumno", agregar_alumno_interfaz, margins=(105, 105))

    def eliminar_alumnos_interfaz(self):
        eliminar_alumno_interfaz = [[sg.Text("Introduzca el dni: "), sg.Input()],
                                    [sg.Button('Ok', key='-ok-'), sg.Button('Cancel', key="-cancel-")]]
        return sg.Window("Eliminar alumnos", eliminar_alumno_interfaz, margins=(100, 100))

    def eliminar_confirm_interfaz(self, dni):
        try:
            eliminar_2 = [[sg.Text(f"Seguro que quiere eliminar a {agenda.alumnos[dni][0]}", key="-alumno-")],
                          [sg.Button("OK", key="-ok-"), sg.Button("CANCELAR", key="-cancel-")]]
            return sg.Window("Eliminar alumnos", eliminar_2, margins=(100, 100))
        except KeyError:
            sg.PopupScrolled("Error! Por favor verifique los datos")
            return "Error"

    def asignar_horarios_interfaz(self):
        elegir_horario_interfaz = [[sg.Text("Martes: ")],
                                   [sg.Button("17:30", key="-0-", size=self.tamano_boton_hr),
                                    sg.Button("18:30", key="-1-", size=self.tamano_boton_hr),
                                    sg.Button("19:30", key="-2-", size=self.tamano_boton_hr)],
                                   [sg.Text("Jueves: ")],
                                   [sg.Button("17:30", key="-3-", size=self.tamano_boton_hr),
                                    sg.Button("18:30", key="-4-", size=self.tamano_boton_hr),
                                    sg.Button("19:30", key="-5-", size=self.tamano_boton_hr)],
                                   [sg.Text("Viernes: ")],
                                   [sg.Button("17:30", key="-6-", size=self.tamano_boton_hr),
                                    sg.Button("18:30", key="-7-", size=self.tamano_boton_hr),
                                    sg.Button("19:30", key="-8-", size=self.tamano_boton_hr)],
                                   [sg.Button('Ok'), sg.Button('Cancel', key='-cancel-')]]
        return sg.Window("Seleccionar horarios", elegir_horario_interfaz, margins=(120, 120))

    def mostrar_horarios_interfaz(self):

        interfaz = [[sg.Text(agenda.mostrar_horarios()[0])],
                    [sg.Text(agenda.mostrar_horarios()[1])],
                    [sg.Text(agenda.mostrar_horarios()[2])],
                    [sg.Text(agenda.mostrar_horarios()[3])],

                    [sg.Text(agenda.mostrar_horarios()[4])],
                    [sg.Text(agenda.mostrar_horarios()[5])],
                    [sg.Text(agenda.mostrar_horarios()[6])],
                    [sg.Text(agenda.mostrar_horarios()[7])],

                    [sg.Text(agenda.mostrar_horarios()[8])],
                    [sg.Text(agenda.mostrar_horarios()[9])],
                    [sg.Text(agenda.mostrar_horarios()[10])],
                    [sg.Text(agenda.mostrar_horarios()[11])],
                    [sg.Text("")],
                    [sg.Button("OK", key="-ok-"), sg.Button("CANCELAR", key="-cancel-")]]
        return sg.Window("Mostrar Horarios", interfaz, margins=(100, 100))

    def mostrar_deuda_interfaz(self):
        layout = [[sg.Text("Introduzca el dni: "), sg.Input()],
                  [sg.Button('Ok', key='-ok-'), sg.Button('Cancel', key="-cancel-")]]
        return sg.Window("Mostrar Deuda", layout, margins=(100, 100))

    """
    METODOS INTERFAZ
    """
    def mostrar_horarios(self):
        interfaz = self.mostrar_horarios_interfaz()
        event, values = interfaz.read()
        if event in ["-ok-", "-cancel-"]:
            interfaz.close()
            self.menu()

    def mostrar_deuda(self):
        interfaz = self.mostrar_deuda_interfaz()
        event, values = interfaz.read()
        agenda.mostrar_deuda(values[0])

    def eliminar_alumno(self):

        borrar = self.eliminar_alumnos_interfaz()

        event, dni = borrar.read()
        if event == sg.WIN_CLOSED or event == "-cancel-":
            borrar.close()
            self.menu()
        else:
            confirm = self.eliminar_confirm_interfaz(dni[0])
            if confirm == "Error":
                borrar.close()
                self.menu()

            else:
                event, values = confirm.read()
                if event == "-ok-":
                    agenda.eliminar_alumno(dni[0])
                    confirm.close()
                    borrar.close()
                else:
                    borrar.close()
                    confirm.close()
                    sg.Popup("Operacion cancelada")

    def registrar_pagos(self):
        pagos = self.crear_pagos_interfaz()
        event, values = pagos.read()
        try:
            if event == sg.WIN_CLOSED or event == "-cancel-":
                pagos.close()
                self.menu()
            else:
                agenda.agregar_pago(values[1], int(values[0]))
                sg.Popup([["Pago registrado"],
                          [f"Alumno: {agenda.alumnos[values[1]][0]}"],
                          [f"Deuda: {agenda.alumnos[values[1]][1]['Deuda']}"]])
                pagos.close()
                self.menu()
        except (KeyError, ValueError):
            pagos.close()
            if ValueError:
                sg.Popup("Parametro Incorrecto")

    def agregar_alumno(self):
        alumnos_ventana = self.agregar_alumnos_interfaz()
        event, value = alumnos_ventana.read()
        if event == sg.WIN_CLOSED or event == "-cancel-":
            alumnos_ventana.close()
            self.menu()
        else:
            agenda.agregar_alumno(value[0], value[1], value[2], int(value[3]), int(value[4]))
            alumnos_ventana.close()
            self.agregar_a_horario(value[2], int(value[4]))

    def agregar_a_horario(self, dni, dias):
        horarios = self.asignar_horarios_interfaz()
        event, value = horarios.read()
        inscripciones = 0

        while inscripciones < dias:

            if event == sg.WIN_CLOSED or event == "-cancel-":
                horarios.close()
                self.menu()
                break
            elif event in ['-0-', '-1-', '-2-']:
                agenda.dia = "Martes"
                if event == '-0-':
                    agenda.hora = "17:30"
                elif event == '-1-':
                    agenda.hora = "18:30"
                elif event == '-2-':
                    agenda.hora = "19:30"
            elif event in ['-3-', '-4-', '-5-']:
                agenda.dia = "Jueves"
                if event == '-3-':
                    agenda.hora = "17:30"
                elif event == '-4-':
                    agenda.hora = "18:30"
                elif event == '-5-':
                    agenda.hora = "19:30"
            elif event in ['-6-', '-7-', '-8-']:
                agenda.dia = "Viernes"
                if event == '-6-':
                    agenda.hora = "17:30"
                elif event == '-7-':
                    agenda.hora = "18:30"
                elif event == '-8-':
                    agenda.hora = "19:30"
            inscripciones += 1
            agenda.agregar_a_horario(dni)
            event, value = horarios.read()

        horarios.close()
        agenda.agregar_deuda(dias, dni)
        sg.Popup(["Horarios agregados correctamente"],
                 [agenda.alumnos[dni][0]],
                 [agenda.alumnos[dni][1]["Dias/Horarios"]])


if __name__ == "__main__":
    agenda = Alumnos()
    interfaz = Interfaz()
    interfaz.menu()
