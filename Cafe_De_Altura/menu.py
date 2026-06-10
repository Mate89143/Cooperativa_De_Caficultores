from servicios import CooperativaService

# ── Helpers de presentación ───────────────────────────────────

def titulo(t):
    print("\n" + "="*55)
    print("  " + t)
    print("="*55)

def ok(m): print("  OK: " + m)
def err(m): print("  ERROR: " + m)
def info(m): print("  INFO: " + m)

def mostrar_lista(items, vacio="No hay registros."):
    if not items:
        info(vacio)
    else:
        for i in items:
            print(i)

def pedir(campo, tipo=str):
    while True:
        try:
            return tipo(input("  " + campo + ": ").strip())
        except:
            err("Valor inválido para '" + campo + "', intente de nuevo.")


# ══════════════════════════════════════════════════════════════
#  SUBMENÚ: ASOCIADOS
# ══════════════════════════════════════════════════════════════

def menu_asociados(s: CooperativaService):
    while True:
        titulo("ASOCIADOS")
        print("  1. Registrar nuevo asociado")
        print("  2. Listar asociados")
        print("  3. Buscar asociado por ID")
        print("  4. Actualizar datos de asociado")
        print("  5. Eliminar asociado")
        print("  0. ← Volver")
        op = input("\n  Opción: ").strip()

        if op == "1":
            titulo("Registrar Asociado")
            try:
                a = s.crear_asociado(
                    pedir("Identificación"),
                    pedir("Nombre completo"),
                    pedir("Teléfono"),
                    pedir("Años como caficultor", int)
                )
                ok(f"Asociado '{a.nombre}' registrado.")
            except ValueError as e:
                err(e)

        elif op == "2":
            titulo("Listar Asociados")
            filtro = input("  Filtrar por estado (activo/inactivo) "
                           "o Enter para todos: ").strip()
            mostrar_lista(s.listar_asociados(filtro or None))

        elif op == "3":
            titulo("Buscar Asociado")
            try:
                print(s.buscar_asociado(pedir("ID del asociado")))
            except KeyError as e:
                err(e)

        elif op == "4":
            titulo("Actualizar Asociado")
            print("  Campos: nombre | telefono | anos_caficultor | estado")
            try:
                idd   = pedir("ID del asociado")
                campo = pedir("Campo a modificar")
                valor = pedir("Nuevo valor")
                if campo == "anos_caficultor":
                    valor = int(valor)
                a = s.actualizar_asociado(idd, **{campo: valor})
                ok("Asociado actualizado.")
                print(a)
            except (KeyError, ValueError) as e:
                err(e)

        elif op == "5":
            titulo("Eliminar Asociado")
            try:
                nombre = s.eliminar_asociado(pedir("ID del asociado a eliminar"))
                ok(f"Asociado '{nombre}' eliminado.")
            except (KeyError, PermissionError) as e:
                err(e)

        elif op == "0":
            break
        else:
            err("Opción no válida.")


# ══════════════════════════════════════════════════════════════
#  SUBMENÚ: FINCAS
# ══════════════════════════════════════════════════════════════

def menu_fincas(s: CooperativaService):
    while True:
        titulo("FINCAS")
        print("  1. Registrar finca")
        print("  2. Listar fincas")
        print("  3. Actualizar finca")
        print("  4. Eliminar finca")
        print("  0. ← Volver")
        op = input("\n  Opción: ").strip()

        if op == "1":
            titulo("Registrar Finca")
            try:
                vars_raw   = pedir("Variedades de café (separadas por coma)")
                variedades = [v.strip() for v in vars_raw.split(",")]
                f = s.crear_finca(
                    pedir("Código de finca"),
                    pedir("Nombre de finca"),
                    pedir("Municipio"),
                    pedir("Vereda"),
                    pedir("Área en hectáreas", float),
                    variedades,
                    pedir("ID del asociado propietario")
                )
                ok(f"Finca '{f.nombre}' registrada.")
            except (ValueError, KeyError) as e:
                err(e)

        elif op == "2":
            titulo("Listar Fincas")
            idasoc = input("  Filtrar por ID asociado o Enter para todas: ").strip()
            mostrar_lista(s.listar_fincas(idasoc or None))

        elif op == "3":
            titulo("Actualizar Finca")
            print("  Campos: nombre | municipio | vereda | area_hectareas | variedades")
            try:
                cod   = pedir("Código de la finca")
                campo = pedir("Campo a modificar")
                valor = pedir("Nuevo valor")
                if campo == "area_hectareas":
                    valor = float(valor)
                elif campo == "variedades":
                    valor = [v.strip() for v in valor.split(",")]
                s.actualizar_finca(cod, **{campo: valor})
                ok("Finca actualizada.")
            except (KeyError, ValueError) as e:
                err(e)

        elif op == "4":
            titulo("Eliminar Finca")
            try:
                nombre = s.eliminar_finca(pedir("Código de la finca"))
                ok(f"Finca '{nombre}' eliminada.")
            except (KeyError, PermissionError) as e:
                err(e)

        elif op == "0":
            break
        else:
            err("Opción no válida.")


# ══════════════════════════════════════════════════════════════
#  SUBMENÚ: COSECHAS
# ══════════════════════════════════════════════════════════════

def menu_cosechas(s: CooperativaService):
    while True:
        titulo("COSECHAS")
        print("  1. Registrar cosecha")
        print("  2. Listar cosechas")
        print("  3. Actualizar cosecha")
        print("  4. Eliminar cosecha")
        print("  0. ← Volver")
        op = input("\n  Opción: ").strip()

        if op == "1":
            titulo("Registrar Cosecha")
            try:
                c = s.registrar_cosecha(
                    pedir("Número de cosecha"),
                    pedir("Código de finca"),
                    pedir("Temporada (ej. 2024-A)"),
                    pedir("Variedad de café"),
                    pedir("Cantidad producida (kg)", float),
                    pedir("Fecha de recolección (YYYY-MM-DD)")
                )
                ok(f"Cosecha #{c.numero} registrada con {c.cantidad_kg} kg.")
            except (ValueError, KeyError) as e:
                err(e)

        elif op == "2":
            titulo("Listar Cosechas")
            finca = input("  Filtrar por código de finca o Enter para todas: ").strip()
            mostrar_lista(s.listar_cosechas(finca or None))

        elif op == "3":
            titulo("Actualizar Cosecha")
            print("  Campos: temporada | variedad_cafe | cantidad_kg | "
                  "fecha_recoleccion | estado")
            try:
                num   = pedir("Número de cosecha")
                campo = pedir("Campo a modificar")
                valor = pedir("Nuevo valor")
                if campo == "cantidad_kg":
                    valor = float(valor)
                s.actualizar_cosecha(num, **{campo: valor})
                ok("Cosecha actualizada.")
            except (KeyError, ValueError) as e:
                err(e)

        elif op == "4":
            titulo("Eliminar Cosecha")
            try:
                num = pedir("Número de cosecha")
                s.eliminar_cosecha(num)
                ok(f"Cosecha '{num}' eliminada.")
            except (KeyError, PermissionError) as e:
                err(e)

        elif op == "0":
            break
        else:
            err("Opción no válida.")


# ══════════════════════════════════════════════════════════════
#  SUBMENÚ: VENTAS
# ══════════════════════════════════════════════════════════════

def menu_ventas(s: CooperativaService):
    while True:
        titulo("VENTAS")
        print("  1. Registrar venta")
        print("  2. Listar ventas")
        print("  3. Actualizar venta")
        print("  4. Cancelar venta")
        print("  0. ← Volver")
        op = input("\n  Opción: ").strip()

        if op == "1":
            titulo("Registrar Venta")
            try:
                v = s.registrar_venta(
                    pedir("Número de venta"),
                    pedir("Número de cosecha"),
                    pedir("Nombre del comprador"),
                    pedir("Fecha (YYYY-MM-DD)"),
                    pedir("Cantidad a vender (kg)", float),
                    pedir("Precio por kg ($)", float)
                )
                ok(f"Venta registrada. Total: ${v.total:,.0f}")
                cosecha = s.buscar_cosecha(v.numero_cosecha)
                info(f"Stock restante en cosecha {v.numero_cosecha}: "
                     f"{cosecha.cantidad_kg} kg")
            except (ValueError, KeyError) as e:
                err(e)

        elif op == "2":
            titulo("Listar Ventas")
            numc  = input("  Filtrar por cosecha o Enter para todas: ").strip()
            lista = s.listar_ventas(numc or None)
            mostrar_lista(lista)
            if lista:
                print(f"\n  Total acumulado: ${sum(v.total for v in lista):,.0f}")

        elif op == "3":
            titulo("Actualizar Venta")
            print("  Campos editables: comprador | fecha")
            try:
                num   = pedir("Número de venta")
                campo = pedir("Campo a modificar")
                valor = pedir("Nuevo valor")
                s.actualizar_venta(num, **{campo: valor})
                ok("Venta actualizada.")
            except (KeyError, ValueError) as e:
                err(e)

        elif op == "4":
            titulo("Cancelar Venta")
            try:
                num = pedir("Número de venta a cancelar")
                s.eliminar_venta(num)
                ok(f"Venta '{num}' cancelada. Stock devuelto a la cosecha.")
            except KeyError as e:
                err(e)

        elif op == "0":
            break
        else:
            err("Opción no válida.")


# ══════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════

def main():
    s = CooperativaService()   # una sola instancia para toda la sesión

    while True:
        titulo("COOPERATIVA DE CAFICULTORES — CAFÉ DE ALTURA")
        print("  1. Asociados")
        print("  2. Fincas")
        print("  3. Cosechas")
        print("  4. Ventas")
        print("  0. Salir")
        op = input("\n  Opción: ").strip()

        if   op == "1": menu_asociados(s)
        elif op == "2": menu_fincas(s)
        elif op == "3": menu_cosechas(s)
        elif op == "4": menu_ventas(s)
        elif op == "0":
            print("\n  ¡Hasta pronto! ☕\n")
            break
        else:
            err("Opción no válida.")


if __name__ == "__main__":
    main()