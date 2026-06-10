from servicios import CooperativaService

resultados = {"aprobadas": 0, "fallidas": 0}


def encabezado_prueba(numero, descripcion):
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print(f"║  PRUEBA {numero}  —  {descripcion:<48}║")
    print("╚" + "═" * 58 + "╝")


def verificacion(descripcion, condicion):
    """True → APROBADO | False → FALLIDO"""
    estado = "✅ APROBADO" if condicion else "❌ FALLIDO"
    print(f"     {estado}  ›  {descripcion}")
    resultados["aprobadas" if condicion else "fallidas"] += 1
    return condicion


def paso(num, texto):
    print(f"\n  Paso {num}: {texto}")
    print("  " + "─" * 50)


# ══════════════════════════════════════════════════════════════
#  PRUEBA 1 — Flujo completo y descuento de stock
# ══════════════════════════════════════════════════════════════

def prueba_1():
    encabezado_prueba(1, "Flujo completo y descuento de stock")
    print("""
  Descripción:
    Registrar un asociado, crear una finca a su nombre,
    registrar una cosecha de 500 kg, realizar una venta de
    200 kg y verificar que el saldo quede en 300 kg.

  Datos de entrada:
    ┌──────────────────────────────────────────────────┐
    │ Asociado │ ID: A001  │ Pedro Ospina              │
    │ Finca    │ Cód: F001 │ La Esperanza, Salento     │
    │ Cosecha  │ Núm: C001 │ 500 kg │ Caturra │ 2024-A │
    │ Venta    │ Núm: V001 │ 200 kg │ $3.500/kg         │
    └──────────────────────────────────────────────────┘

  Resultado esperado:
    Stock cosecha C001 tras la venta = 300 kg
    Total de la venta V001           = $700.000
""")

    s = CooperativaService()

    paso(1, "Registrar asociado Pedro Ospina (ID: A001)")
    s.crear_asociado("A001", "Pedro Ospina", "3001112233", 15)
    verificacion("Asociado A001 existe en el sistema",
                 "A001" in s._asociados)
    verificacion("Estado inicial del asociado es 'activo'",
                 s._asociados["A001"].estado == "activo")

    paso(2, "Registrar finca 'La Esperanza' (F001) para A001")
    s.crear_finca("F001", "La Esperanza", "Salento",
                  "El Roble", 7.5, ["Caturra", "Castillo"], "A001")
    verificacion("Finca F001 creada y vinculada al asociado A001",
                 "F001" in s._fincas and s._fincas["F001"].id_asociado == "A001")
    verificacion("Contador numero_fincas del asociado A001 = 1",
                 s._asociados["A001"].numero_fincas == 1)

    paso(3, "Registrar cosecha C001: 500 kg de Caturra, temporada 2024-A")
    s.registrar_cosecha("C001", "F001", "2024-A", "Caturra", 500.0, "2024-10-10")
    verificacion("Cosecha C001 existe en el sistema",
                 "C001" in s._cosechas)
    verificacion("Stock inicial de C001 = 500 kg",
                 s._cosechas["C001"].cantidad_kg == 500.0)

    paso(4, "Registrar venta V001: 200 kg a Tostadores del Sur a $3.500/kg")
    v = s.registrar_venta("V001", "C001", "Tostadores del Sur",
                          "2024-11-05", 200.0, 3500.0)
    stock = s._cosechas["C001"].cantidad_kg
    verificacion(f"Stock de C001 después de la venta = 300 kg  (obtenido: {stock})",
                 stock == 300.0)
    verificacion(f"Total V001 = $700.000  (obtenido: ${v.total:,.0f})",
                 v.total == 700_000.0)

    paso(5, "Intentar vender 400 kg (solo hay 300) → debe bloquearse")
    bloqueado = False
    try:
        s.registrar_venta("V002", "C001", "X", "2024-11-10", 400.0, 3500.0)
    except ValueError as e:
        bloqueado = True
        print(f"     ⛔ Bloqueado: {e}")
    verificacion("Venta con stock insuficiente fue rechazada", bloqueado)
    verificacion("Stock de C001 NO cambió (sigue en 300 kg)",
                 s._cosechas["C001"].cantidad_kg == 300.0)


# ══════════════════════════════════════════════════════════════
#  PRUEBA 2 — Restricciones de eliminación en cascada
# ══════════════════════════════════════════════════════════════

def prueba_2():
    encabezado_prueba(2, "Restricciones de eliminación en cascada")
    print("""
  Descripción:
    Intentar eliminar asociado con fincas     → bloqueado
    Intentar eliminar finca con cosechas      → bloqueado
    Eliminar cosecha → finca → asociado       → permitido en ese orden

  Datos de entrada:
    ┌──────────────────────────────────────────────────┐
    │ Asociado │ ID: B001  │ Luz Marina García         │
    │ Finca    │ Cód: G001 │ vinculada a B001          │
    │ Cosecha  │ Núm: H001 │ vinculada a G001          │
    └──────────────────────────────────────────────────┘

  Resultado esperado:
    Eliminar asociado con finca    → ❌ bloqueado
    Eliminar finca con cosecha     → ❌ bloqueado
    Eliminar cosecha (sin ventas)  → ✅ permitido
    Eliminar finca (sin cosechas)  → ✅ permitido
    Eliminar asociado (sin fincas) → ✅ permitido
""")

    s = CooperativaService()
    print("  [Setup] Creando datos de prueba...")
    s.crear_asociado("B001", "Luz Marina García", "3157778899", 10)
    s.crear_finca("G001", "Villa Café", "Manizales", "La Palma",
                  4.0, ["Colombia"], "B001")
    s.registrar_cosecha("H001", "G001", "2024-B", "Colombia", 300.0, "2024-11-20")
    print()

    paso(1, "Intentar eliminar asociado B001 (tiene finca G001)")
    bloq1 = False
    try:
        s.eliminar_asociado("B001")
    except PermissionError as e:
        bloq1 = True
        print(f"     ⛔ Bloqueado: {e}")
    verificacion("Eliminación de asociado con fincas fue bloqueada", bloq1)
    verificacion("Asociado B001 sigue en el sistema", "B001" in s._asociados)

    paso(2, "Intentar eliminar finca G001 (tiene cosecha H001)")
    bloq2 = False
    try:
        s.eliminar_finca("G001")
    except PermissionError as e:
        bloq2 = True
        print(f"     ⛔ Bloqueado: {e}")
    verificacion("Eliminación de finca con cosechas fue bloqueada", bloq2)
    verificacion("Finca G001 sigue en el sistema", "G001" in s._fincas)

    paso(3, "Eliminar cosecha H001 (sin ventas vinculadas)")
    ok3 = False
    try:
        s.eliminar_cosecha("H001")
        ok3 = True
    except Exception as e:
        print(f"     Error: {e}")
    verificacion("Cosecha H001 eliminada correctamente", ok3)
    verificacion("H001 ya no está en el sistema", "H001" not in s._cosechas)

    paso(4, "Eliminar finca G001 (ya sin cosechas)")
    ok4 = False
    try:
        s.eliminar_finca("G001")
        ok4 = True
    except Exception as e:
        print(f"     Error: {e}")
    verificacion("Finca G001 eliminada correctamente", ok4)
    verificacion("G001 ya no está en el sistema", "G001" not in s._fincas)
    verificacion("Contador numero_fincas de B001 = 0",
                 s._asociados["B001"].numero_fincas == 0)

    paso(5, "Eliminar asociado B001 (ya sin fincas)")
    ok5 = False
    try:
        s.eliminar_asociado("B001")
        ok5 = True
    except Exception as e:
        print(f"     Error: {e}")
    verificacion("Asociado B001 eliminado correctamente", ok5)
    verificacion("B001 ya no está en el sistema", "B001" not in s._asociados)


# ══════════════════════════════════════════════════════════════
#  RUNNER
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "█" * 60)
    print("   PRUEBAS FUNCIONALES  —  CAFÉ DE ALTURA")
    print("   Taller de Desarrollo de Software")
    print("█" * 60)

    prueba_1()
    prueba_2()

    total = resultados["aprobadas"] + resultados["fallidas"]
    print("\n\n" + "═" * 60)
    print("  RESUMEN DE RESULTADOS")
    print("═" * 60)
    print(f"  Verificaciones aprobadas : {resultados['aprobadas']}/{total}")
    print(f"  Verificaciones fallidas  : {resultados['fallidas']}/{total}")
    estado = ("✅ TODAS LAS PRUEBAS PASARON" if resultados["fallidas"] == 0
              else "❌ HAY PRUEBAS FALLIDAS — revisar")
    print(f"\n  Estado final: {estado}")
    print("═" * 60)