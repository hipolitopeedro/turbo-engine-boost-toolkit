#!/usr/bin/env python3
"""
turbo_sizing_calculator.py
EN: Calculates turbocharger compressor Pressure Ratio (PR), Mass Air Flow (lb/min),
    effective dynamic compression ratio under boost, and required fuel injector size
    (cc/min and lb/hr) for Gasoline or Ethanol (E100/E85).
PT: Calcula Pressure Ratio (PR) do compressor, vazão mássica de ar (lb/min),
    taxa de compressão efetiva sob pressão e vazão necessária de bicos injetores
    (cc/min e lb/h) para Gasolina ou Etanol.
"""

import argparse

ATM_BAR = 1.01325
BAR_TO_PSI = 14.5038


def calculate_turbo_setup(
    displacement_l: float,
    cylinders: int,
    max_rpm: int,
    boost_bar: float,
    volumetric_efficiency: float,
    intake_temp_c: float,
    static_cr: float,
    fuel_type: str,
) -> None:
    boost_psi = boost_bar * BAR_TO_PSI
    atm_psi = ATM_BAR * BAR_TO_PSI

    # Compressor Pressure Ratio (Absolute Outlet / Absolute Inlet)
    pressure_ratio = (atm_psi + boost_psi) / atm_psi

    # Engine displacement in cubic inches (1L = 61.0237 CID)
    cid = displacement_l * 61.0237
    intake_temp_r = (intake_temp_c * 9.0 / 5.0) + 491.67  # Rankine
    manifold_abs_psi = atm_psi + boost_psi

    # Ideal Gas Law Mass Air Flow (lb/min)
    # MAF = (MAP * CID * RPM * VE) / (2 * 1728 * R * T_R) where R for air = 53.35 ft*lbf/(lb*R)
    airflow_cfm = (cid * max_rpm * volumetric_efficiency) / 3456.0
    air_density_lb_ft3 = (manifold_abs_psi * 144.0) / (53.35 * intake_temp_r)
    mass_airflow_lb_min = airflow_cfm * air_density_lb_ft3
    mass_airflow_kg_h = mass_airflow_lb_min * 27.2155

    # Estimated flywheel HP (approx 10.2 HP per lb/min on modern turbo setups)
    estimated_hp = mass_airflow_lb_min * (10.6 if fuel_type == "ethanol" else 10.0)

    # Effective Compression Ratio under boost
    effective_cr = static_cr * pressure_ratio

    # BSFC (Brake Specific Fuel Consumption) in lb/(HP*hr)
    bsfc = 0.64 if fuel_type == "ethanol" else 0.47
    max_duty_cycle = 0.80  # Safe 80% max Injector Duty Cycle (IDC)

    injector_lb_hr = (estimated_hp * bsfc) / (cylinders * max_duty_cycle)
    injector_cc_min = injector_lb_hr * 10.5

    print("==========================================================================")
    print("  TURBOCHARGED ENGINE & FUEL SYSTEM SIZING CALCULATOR")
    print("==========================================================================")
    print(f"  Engine Setup       : {displacement_l:.1f}L ({cylinders} cyl) | Redline: {max_rpm} RPM | Static CR: {static_cr}:1")
    print(f"  Target Boost       : {boost_bar:.2f} bar ({boost_psi:.1f} psi) | Pressure Ratio (PR): {pressure_ratio:.2f}")
    print(f"  Effective Boost CR : {effective_cr:.2f}:1")
    print("--------------------------------------------------------------------------")
    print(f"  Mass Air Flow      : {mass_airflow_lb_min:.1f} lb/min ({mass_airflow_kg_h:.1f} kg/h)")
    print(f"  Estimated Output   : ~{int(estimated_hp)} HP (Crank) on {fuel_type.upper()}")
    print(
        f"  Min Injector Size  : {int(injector_cc_min)} cc/min ({injector_lb_hr:.1f} lb/hr) per cylinder @ 80% IDC"
    )
    print("==========================================================================")


def main() -> None:
    parser = argparse.ArgumentParser(description="Turbocharger Airflow & Fuel Injector Calculator")
    parser.add_argument("--displacement-l", type=float, default=2.0, help="Engine displacement in Liters")
    parser.add_argument("--cylinders", type=int, default=4, help="Number of cylinders")
    parser.add_argument("--max-rpm", type=int, default=6800, help="Peak power RPM")
    parser.add_argument("--boost-bar", type=float, default=1.2, help="Target gauge boost pressure in bar")
    parser.add_argument("--ve", type=float, default=0.92, help="Volumetric efficiency (0.0 - 1.1)")
    parser.add_argument("--iat-c", type=float, default=42.0, help="Manifold Intake Air Temp in Celsius")
    parser.add_argument("--static-cr", type=float, default=9.5, help="Static mechanical compression ratio")
    parser.add_argument(
        "--fuel",
        choices=["gasoline", "ethanol"],
        default="ethanol",
        help="Fuel type (gasoline or ethanol)",
    )
    args = parser.parse_args()

    calculate_turbo_setup(
        displacement_l=args.displacement_l,
        cylinders=args.cylinders,
        max_rpm=args.max_rpm,
        boost_bar=args.boost_bar,
        volumetric_efficiency=args.ve,
        intake_temp_c=args.iat_c,
        static_cr=args.static_cr,
        fuel_type=args.fuel,
    )


if __name__ == "__main__":
    main()
