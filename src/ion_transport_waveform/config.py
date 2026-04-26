from dataclasses import dataclass

AMU = 1.66053906660e-27
ELEMENTARY_CHARGE = 1.602176634e-19

@dataclass(frozen=True)
class IonSpecies:
    name: str = "Ca+"
    mass_amu: float = 40.0
    charge_e: float = 1.0

    @property
    def mass_kg(self) -> float:
        return self.mass_amu * AMU

    @property
    def charge_c(self) -> float:
        return self.charge_e * ELEMENTARY_CHARGE

@dataclass(frozen=True)
class TrapConfig:
    electrode_pitch_m: float = 80e-6
    basis_width_m: float = 90e-6
    omega_rad_s: float = 2.0 * 3.141592653589793 * 1.0e6
    voltage_limit_v: float = 10.0
    dt_s: float = 2e-8
