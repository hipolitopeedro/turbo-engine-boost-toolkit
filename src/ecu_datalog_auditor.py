#!/usr/bin/env python3
"""
ecu_datalog_auditor.py
EN: Parses standalone ECU datalogs (CSV) from a turbocharged engine WOT pull and flags
    dangerous operating conditions: Lean Lambda under boost, Injector Duty Cycle (IDC)
    saturation, Intercooler Heat Soak (high IAT), and Overboost.
PT: Analisa datalogs CSV de injeção programável em motores turbo e alerta sobre condições
    de risco: mistura pobre sob pressão, saturação de bicos (IDC), temperatura de admissão
    elevada (IAT) e overboost.
"""

import argparse
import csv
from typing import List


def audit_datalog(csv_path: str, max_boost_bar: float, max_idc_pct: float, max_iat_c: float) -> None:
    alerts: List[str] = []
    peak_boost = 0.0
    peak_rpm = 0
    peak_idc = 0.0

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t_sec = float(row["time_s"])
            rpm = int(row["rpm"])
            map_bar = float(row["map_gauge_bar"])
            tps = float(row["tps_pct"])
            measured_lambda = float(row["lambda_measured"])
            target_lambda = float(row["lambda_target"])
            iat_c = float(row["iat_c"])
            idc_pct = float(row["idc_pct"])

            peak_boost = max(peak_boost, map_bar)
            peak_rpm = max(peak_rpm, rpm)
            peak_idc = max(peak_idc, idc_pct)

            # Only audit active WOT boost regions
            if tps >= 90.0 and map_bar >= 0.4:
                # 1. Lean mixture check under boost
                if measured_lambda - target_lambda >= 0.04:
                    alerts.append(
                        f"[{t_sec:>5.2f}s @ {rpm} RPM] LEAN UNDER BOOST: "
                        f"Boost={map_bar:.2f} bar | Measured Lambda={measured_lambda:.2f} (Target={target_lambda:.2f})"
                    )

                # 2. Overboost check
                if map_bar > max_boost_bar:
                    alerts.append(
                        f"[{t_sec:>5.2f}s @ {rpm} RPM] OVERBOOST DETECTED: "
                        f"Boost={map_bar:.2f} bar exceeds limit ({max_boost_bar:.2f} bar)"
                    )

                # 3. Injector Duty Cycle saturation check
                if idc_pct > max_idc_pct:
                    alerts.append(
                        f"[{t_sec:>5.2f}s @ {rpm} RPM] HIGH INJECTOR DUTY CYCLE: "
                        f"IDC={idc_pct:.1f}% (Safe limit: {max_idc_pct:.1f}%)"
                    )

                # 4. High Intake Air Temperature (Intercooler Heat Soak)
                if iat_c > max_iat_c:
                    alerts.append(
                        f"[{t_sec:>5.2f}s @ {rpm} RPM] HIGH INTAKE TEMP (HEAT SOAK): "
                        f"IAT={iat_c:.1f} C (Limit: {max_iat_c:.1f} C)"
                    )

    print("==========================================================================")
    print("  STANDALONE ECU WOT DATALOG SAFETY AUDITOR")
    print("==========================================================================")
    print(f"  Peak RPM   : {peak_rpm} RPM")
    print(f"  Peak Boost : {peak_boost:.2f} bar ({peak_boost * 14.5038:.1f} psi)")
    print(f"  Peak IDC   : {peak_idc:.1f}%")
    print("--------------------------------------------------------------------------")

    if not alerts:
        print("  [STATUS: SAFE] All WOT parameters remained within target safety thresholds.")
    else:
        print(f"  [STATUS: {len(alerts)} WARNING(S) DETECTED DURING PULL]")
        for a in alerts:
            print(f"    ! {a}")
    print("==========================================================================")


def main() -> None:
    parser = argparse.ArgumentParser(description="Standalone ECU Turbo Datalog Safety Auditor")
    parser.add_argument("--log", default="data/sample_wot_pull_datalog.csv", help="Path to ECU datalog CSV")
    parser.add_argument("--max-boost-bar", type=float, default=1.25, help="Max safe boost pressure (bar)")
    parser.add_argument("--max-idc-pct", type=float, default=85.0, help="Max safe Injector Duty Cycle (%)")
    parser.add_argument("--max-iat-c", type=float, default=60.0, help="Max safe Intake Air Temp (C)")
    args = parser.parse_args()

    audit_datalog(args.log, args.max_boost_bar, args.max_idc_pct, args.max_iat_c)


if __name__ == "__main__":
    main()
