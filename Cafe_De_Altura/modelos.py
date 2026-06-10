from dataclasses import dataclass, field
from typing import List


# ──────────────────────────────────────────────
#  ENTIDAD 1: ASOCIADO
# ──────────────────────────────────────────────
@dataclass
class Asociado:
    identificacion: str      # Cédula o NIT — clave única
    nombre: str
    telefono: str
    anos_caficultor: int
    numero_fincas: int = 0   # Se actualiza al crear/borrar fincas
    estado: str = "activo"   # "activo" / "inactivo"

    def __str__(self):
        return (f"  ID: {self.identificacion:<12} | Nombre: {self.nombre:<20} "
                f"| Tel: {self.telefono:<12} | Exp: {self.anos_caficultor} años "
                f"| Fincas: {self.numero_fincas} | Estado: {self.estado}")


# ──────────────────────────────────────────────
#  ENTIDAD 2: FINCA
# ──────────────────────────────────────────────
@dataclass
class Finca:
    codigo: str
    nombre: str
    municipio: str
    vereda: str
    area_hectareas: float
    variedades: List[str]    
    id_asociado: str         

    def __str__(self):
        return (f"  Cód: {self.codigo:<8} | Nombre: {self.nombre:<18} "
                f"| {self.vereda}, {self.municipio} "
                f"| {self.area_hectareas} ha "
                f"| Variedades: {', '.join(self.variedades)} "
                f"| Propietario: {self.id_asociado}")


# ──────────────────────────────────────────────
#  ENTIDAD 3: COSECHA
# ──────────────────────────────────────────────
@dataclass
class Cosecha:
    numero: str
    codigo_finca: str        
    temporada: str           
    variedad_cafe: str
    cantidad_kg: float       # Stock disponible
    fecha_recoleccion: str   # Formato YYYY-MM-DD
    estado: str = "en proceso"
    # Estados: "en proceso" / "recolectada" / "en beneficio" / "terminada"

    def __str__(self):
        return (f"  Núm: {self.numero:<8} | Finca: {self.codigo_finca:<8} "
                f"| Temporada: {self.temporada} | Variedad: {self.variedad_cafe:<12} "
                f"| Stock: {self.cantidad_kg} kg | Fecha: {self.fecha_recoleccion} "
                f"| Estado: {self.estado}")


# ──────────────────────────────────────────────
#  ENTIDAD 4: VENTA
# ──────────────────────────────────────────────
@dataclass
class Venta:
    numero_venta: str
    numero_cosecha: str      
    comprador: str
    fecha: str               # Formato YYYY-MM-DD
    cantidad_kg: float
    precio_por_kg: float

    @property
    def total(self) -> float:
        return round(self.cantidad_kg * self.precio_por_kg, 2)

    def __str__(self):
        return (f"  Venta: {self.numero_venta:<8} | Cosecha: {self.numero_cosecha:<8} "
                f"| Comprador: {self.comprador:<20} | Fecha: {self.fecha} "
                f"| {self.cantidad_kg} kg × ${self.precio_por_kg:,.0f} "
                f"= TOTAL: ${self.total:,.0f}")