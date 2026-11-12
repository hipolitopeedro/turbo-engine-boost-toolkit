# Turbocharged Engine Sizing & ECU Datalog Safety Toolkit

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Motorsport](https://img.shields.io/badge/Automotive-Turbo_%26_ECU_Tuning-D9230F?style=for-the-badge)

> **English:** Automotive engineering hobby project focused on **Turbocharged Engines & Standalone ECU Telemetry (FuelTech / MegaSquirt / Haltech style logs)**. Includes a turbocharger mass airflow & fuel injector sizing calculator (Gasoline vs. Ethanol E100) and an automated ECU datalog safety auditor that detects lean AFR/Lambda under boost, injector duty cycle saturation, heat soak, and overboost events.
>
> **Português:** Projeto pessoal de engenharia automotiva focado em **Motores Turbo e Telemetria de Injeções Programáveis (estilo FuelTech / MegaSquirt / Haltech)**. Inclui uma calculadora de dimensionamento de turbina e bicos injetores (Gasolina vs. Etanol E100) e um auditor automatizado de datalogs que detecta mistura pobre sob pressão, saturação de duty cycle de bicos (IDC), *heat soak* de intercooler e *overboost*.

---

## Included Tools / Ferramentas Inclusas

| File | Description (EN) | Descrição (PT-BR) |
| :--- | :--- | :--- |
| [`src/turbo_sizing_calculator.py`](src/turbo_sizing_calculator.py) | Computes compressor Pressure Ratio ($PR$), engine Mass Air Flow (`lb/min` and `kg/h`), estimated brake horsepower, dynamic boost compression ratio, and minimum required fuel injector flow (`cc/min` & `lb/hr`) for Pump Gas or Ethanol. | Calcula Taxa de Pressão do compressor ($PR$), fluxo de ar em massa (`lb/min` e `kg/h`), potência estimada, taxa de compressão dinâmica sob pressão e vazão mínima de bicos injetores (`cc/min` e `lb/h`) para Gasolina ou Etanol. |
| [`src/ecu_datalog_auditor.py`](src/ecu_datalog_auditor.py) | Analyzes Wide Open Throttle (WOT) ECU CSV datalogs (`RPM`, `MAP_bar`, `TPS_pct`, `Lambda`, `Target_Lambda`, `IAT_C`, `CLT_C`, `Ign_Deg`, `IDC_pct`) and flags dangerous tuning conditions before engine damage occurs. | Analisa datalogs CSV de puxadas WOT e alerta automaticamente sobre condições críticas (mistura pobre sob pressão, bico travado acima de 85% de IDC, temperatura de admissão alta e *overboost*). |
| [`data/sample_wot_pull_datalog.csv`](data/sample_wot_pull_datalog.csv) | Sample 3rd-gear WOT dyno pull datalog (2,500 to 7,000 RPM @ 1.2 bar boost) for analysis. | Datalog de exemplo de uma puxada em 3ª marcha (2.500 a 7.000 RPM com 1.2 bar de pressão). |

---

## Quick Start / Como Executar

### 1. Turbocharger Airflow & Fuel Injector Calculator
```bash
# Example: 2.0L 4-cylinder engine running 1.2 bar (17.4 psi) of boost on Ethanol (E100) at 6800 RPM
python src/turbo_sizing_calculator.py \
    --displacement-l 2.0 \
    --cylinders 4 \
    --max-rpm 6800 \
    --boost-bar 1.2 \
    --static-cr 9.5 \
    --fuel ethanol
```

### 2. Standalone ECU Datalog Safety Auditor
```bash
python src/ecu_datalog_auditor.py --log data/sample_wot_pull_datalog.csv --max-boost-bar 1.25
```
