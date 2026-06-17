from modelos import Asociado, Finca, Cosecha, Venta
from typing import List, Optional
from persistencia import guardar, cargar

class CooperativaService:

    def __init__(self):
        self._asociados = {}
        self._fincas    = {}
        self._cosechas  = {}
        self._ventas    = {}
        cargar(self)


    # ══════════════════════════════════════════════════════
    #  SECCIÓN A — CRUD ASOCIADOS
    # ══════════════════════════════════════════════════════

    # ── A1. CREATE ──────────────────────────────────────
    def crear_asociado(self, identificacion: str, nombre: str,
                       telefono: str, años_caficultor: int) -> Asociado:
        """Registra un nuevo asociado. Lanza ValueError si el ID ya existe."""
        if identificacion in self._asociados:
            raise ValueError(f"Ya existe un asociado con ID '{identificacion}'.")

        asociado = Asociado(identificacion, nombre, telefono, años_caficultor)
        self._asociados[identificacion] = asociado
        guardar(self)
        return asociado

    # ── A2. READ ────────────────────────────────────────
    def listar_asociados(self, estado: Optional[str] = None) -> List[Asociado]:
        """Lista todos los asociados. Filtra por estado si se indica."""
        todos = list(self._asociados.values())
        if estado:
            return [a for a in todos if a.estado == estado]
        return todos

    def buscar_asociado(self, identificacion: str) -> Asociado:
        """Busca por ID. Lanza KeyError si no existe."""
        if identificacion not in self._asociados:
            raise KeyError(f"Asociado '{identificacion}' no encontrado.")
        return self._asociados[identificacion]

    # ── A3. UPDATE ──────────────────────────────────────
    def actualizar_asociado(self, identificacion: str, **campos) -> Asociado:
        """
        Actualiza campos del asociado.
        Campos permitidos: nombre, telefono, anos_caficultor, estado.
        Uso: actualizar_asociado("A001", nombre="Nuevo nombre")
        """
        asociado  = self.buscar_asociado(identificacion)
        permitidos = {"nombre", "telefono", "anos_caficultor", "estado"}

        for campo, valor in campos.items():
            if campo not in permitidos:
                raise ValueError(f"No se puede modificar el campo '{campo}'.")
            setattr(asociado, campo, valor)
        guardar(self)
        return asociado

    # ── A4. DELETE ──────────────────────────────────────
    def eliminar_asociado(self, identificacion: str) -> str:
        """
        Elimina un asociado SOLO si no tiene fincas.
        Regla: un asociado con fincas no puede borrarse.
        """
        self.buscar_asociado(identificacion)

        fincas_propias = [f for f in self._fincas.values()
                          if f.id_asociado == identificacion]
        if fincas_propias:
            raise PermissionError(
                f"No se puede eliminar: el asociado tiene "
                f"{len(fincas_propias)} finca(s). Elimine primero las fincas.")

        nombre = self._asociados[identificacion].nombre
        del self._asociados[identificacion]
        guardar(self)
        return nombre

    # ══════════════════════════════════════════════════════
    #  SECCIÓN B — CRUD FINCAS
    # ══════════════════════════════════════════════════════

    # ── B1. CREATE ──────────────────────────────────────
    def crear_finca(self, codigo: str, nombre: str, municipio: str,
                    vereda: str, area_hectareas: float,
                    variedades: List[str], id_asociado: str) -> Finca:
        """Registra una finca vinculada a un asociado existente."""
        if codigo in self._fincas:
            raise ValueError(f"Ya existe una finca con código '{codigo}'.")

        asociado = self.buscar_asociado(id_asociado)   # valida que exista

        finca = Finca(codigo, nombre, municipio, vereda,
                      area_hectareas, variedades, id_asociado)
        self._fincas[codigo] = finca
        asociado.numero_fincas += 1   # actualizar contador
        guardar(self)
        return finca

    # ── B2. READ ────────────────────────────────────────
    def listar_fincas(self, id_asociado: Optional[str] = None) -> List[Finca]:
        todas = list(self._fincas.values())
        if id_asociado:
            return [f for f in todas if f.id_asociado == id_asociado]
        return todas

    def buscar_finca(self, codigo: str) -> Finca:
        if codigo not in self._fincas:
            raise KeyError(f"Finca '{codigo}' no encontrada.")
        return self._fincas[codigo]

    # ── B3. UPDATE ──────────────────────────────────────
    def actualizar_finca(self, codigo: str, **campos) -> Finca:
        """Campos permitidos: nombre, municipio, vereda, area_hectareas, variedades."""
        finca      = self.buscar_finca(codigo)
        permitidos = {"nombre", "municipio", "vereda", "area_hectareas", "variedades"}
        for campo, valor in campos.items():
            if campo not in permitidos:
                raise ValueError(f"Campo '{campo}' no editable en Finca.")
            setattr(finca, campo, valor)
        guardar(self)
        return finca

    # ── B4. DELETE ──────────────────────────────────────
    def eliminar_finca(self, codigo: str) -> str:
        """Elimina una finca SOLO si no tiene cosechas. Descuenta contador del asociado."""
        finca = self.buscar_finca(codigo)

        cosechas_propias = [c for c in self._cosechas.values()
                            if c.codigo_finca == codigo]
        if cosechas_propias:
            raise PermissionError(
                f"No se puede eliminar: la finca tiene "
                f"{len(cosechas_propias)} cosecha(s). Elimine primero las cosechas.")

        if finca.id_asociado in self._asociados:
            self._asociados[finca.id_asociado].numero_fincas -= 1

        del self._fincas[codigo]
        guardar(self)
        return finca.nombre


    # ══════════════════════════════════════════════════════
    #  SECCIÓN C — CRUD COSECHAS
    # ══════════════════════════════════════════════════════

    # ── C1. CREATE ──────────────────────────────────────
    def registrar_cosecha(self, numero: str, codigo_finca: str,
                          temporada: str, variedad_cafe: str,
                          cantidad_kg: float, fecha_recoleccion: str) -> Cosecha:
        """Registra una cosecha en una finca existente."""
        if numero in self._cosechas:
            raise ValueError(f"Ya existe una cosecha número '{numero}'.")
        self.buscar_finca(codigo_finca)   # valida que la finca exista

        cosecha = Cosecha(numero, codigo_finca, temporada,
                          variedad_cafe, cantidad_kg, fecha_recoleccion)
        self._cosechas[numero] = cosecha
        guardar(self)
        return cosecha

    # ── C2. READ ────────────────────────────────────────
    def listar_cosechas(self, codigo_finca: Optional[str] = None) -> List[Cosecha]:
        todas = list(self._cosechas.values())
        if codigo_finca:
            return [c for c in todas if c.codigo_finca == codigo_finca]
        return todas

    def buscar_cosecha(self, numero: str) -> Cosecha:
        if numero not in self._cosechas:
            raise KeyError(f"Cosecha '{numero}' no encontrada.")
        return self._cosechas[numero]

    # ── C3. UPDATE ──────────────────────────────────────
    def actualizar_cosecha(self, numero: str, **campos) -> Cosecha:
        """Campos: temporada, variedad_cafe, cantidad_kg, fecha_recoleccion, estado."""
        cosecha    = self.buscar_cosecha(numero)
        permitidos = {"temporada", "variedad_cafe", "cantidad_kg",
                      "fecha_recoleccion", "estado"}
        for campo, valor in campos.items():
            if campo not in permitidos:
                raise ValueError(f"Campo '{campo}' no editable en Cosecha.")
            setattr(cosecha, campo, valor)
        guardar(self)
        return cosecha

    # ── C4. DELETE ──────────────────────────────────────
    def eliminar_cosecha(self, numero: str) -> str:
        """Elimina una cosecha solo si no tiene ventas asociadas."""
        cosecha = self.buscar_cosecha(numero)

        ventas_propias = [v for v in self._ventas.values()
                          if v.numero_cosecha == numero]
        if ventas_propias:
            raise PermissionError(
                f"No se puede eliminar: la cosecha tiene "
                f"{len(ventas_propias)} venta(s) registrada(s).")

        del self._cosechas[numero]
        guardar(self)
        return cosecha.numero


    # ══════════════════════════════════════════════════════
    #  SECCIÓN D — CRUD VENTAS
    # ══════════════════════════════════════════════════════

    # ── D1. CREATE ──────────────────────────────────────
    def registrar_venta(self, numero_venta: str, numero_cosecha: str,
                        comprador: str, fecha: str,
                        cantidad_kg: float, precio_por_kg: float) -> Venta:
        """
        Registra una venta y DESCUENTA el stock de la cosecha.
        Si cantidad_kg > stock disponible → lanza ValueError.
        """
        if numero_venta in self._ventas:
            raise ValueError(f"Ya existe la venta '{numero_venta}'.")

        cosecha = self.buscar_cosecha(numero_cosecha)

        if cantidad_kg <= 0:
            raise ValueError("La cantidad a vender debe ser mayor a 0.")
        if cantidad_kg > cosecha.cantidad_kg:
            raise ValueError(
                f"Stock insuficiente. "
                f"Disponible: {cosecha.cantidad_kg} kg | "
                f"Solicitado: {cantidad_kg} kg.")

        venta = Venta(numero_venta, numero_cosecha, comprador,
                      fecha, cantidad_kg, precio_por_kg)
        self._ventas[numero_venta] = venta

        cosecha.cantidad_kg = round(cosecha.cantidad_kg - cantidad_kg, 2)  # descontar
        guardar(self)
        return venta

    # ── D2. READ ────────────────────────────────────────
    def listar_ventas(self, numero_cosecha: Optional[str] = None) -> List[Venta]:
        todas = list(self._ventas.values())
        if numero_cosecha:
            return [v for v in todas if v.numero_cosecha == numero_cosecha]
        return todas

    # ── D3. UPDATE ──────────────────────────────────────
    def actualizar_venta(self, numero_venta: str, **campos) -> Venta:
        """Solo se editan comprador y fecha (kg y precio afectan el stock)."""
        if numero_venta not in self._ventas:
            raise KeyError(f"Venta '{numero_venta}' no encontrada.")
        venta      = self._ventas[numero_venta]
        permitidos = {"comprador", "fecha"}
        for campo, valor in campos.items():
            if campo not in permitidos:
                raise ValueError(f"Campo '{campo}' no editable directamente.")
            setattr(venta, campo, valor)
        guardar(self)
        return venta

    # ── D4. DELETE ──────────────────────────────────────
    def eliminar_venta(self, numero_venta: str) -> str:
        """Cancela una venta y DEVUELVE los kg al stock de la cosecha."""
        if numero_venta not in self._ventas:
            raise KeyError(f"Venta '{numero_venta}' no encontrada.")
        venta = self._ventas.pop(numero_venta)

        if venta.numero_cosecha in self._cosechas:
            self._cosechas[venta.numero_cosecha].cantidad_kg += venta.cantidad_kg
        guardar(self)
        return numero_venta