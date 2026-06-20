# MCU Software Requirements Specification

## 1. Document Information

| Attribute | Value |
|---|---|
| Document ID | MCU_SWRS |
| Module | MCU |
| AUTOSAR Release | 4.4.x |
| Target MCU | STM32F407xx |
| Demo Board | STM32F407 Discovery |
| Version | 0.1.0 |

## 2. Functional Requirements

### MCU_REQ_001: Low Power Mode Configuration

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12421 |
| Origin | AR |
| Category | Configuration and Initialization |
| Applicability | Applicable |
| Dependencies | [SRS_Mcu_12268] MCU Power Management Control |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall allow configuration of hardware-supported low power modes required by the application.

**Rationale**

To reduce MCU power consumption based on application needs.

**Notes**

TBD

---

### MCU_REQ_002: The MCU Driver shall allow the static configuration of RAM segments that are initialized during start-up

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12350 |
| Origin | AR |
| Category | Configuration and Initialization |
| Applicability | Applicable |
| Dependencies | [SRS_Mcu_12331] RAM Initialization |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall support static configuration of the RAM segments initialized during start-up.

**Rationale**

To select which RAM segments are initialized and which retain their contents.

**Notes**

TBD

---

### MCU_REQ_003: The MCU Driver shall provide a service to initialize the contents of configured RAM sections

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12331 |
| Origin | AR |
| Category | Configuration and Initialization |
| Applicability | Applicable |
| Dependencies | [SRS_Mcu_12350] Configuration of RAM segments |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall initialize configured RAM sections without modifying unconfigured sections.

**Rationale**

To provide defined RAM contents after ECU start-up.

**Notes**

TBD

---

### MCU_REQ_004: The MCU driver shall provide a service to query the lock status of all PLLs in the micro controller individually

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12392 |
| Origin | AR |
| Category | Configuration and Initialization |
| Applicability | Applicable |
| Dependencies | [SRS_Mcu_12208] Initialization of the MCU clock |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall report each PLL as locked, unlocked, or unsupported.

**Rationale**

TBD

**Notes**

TBD

---

### MCU_REQ_005: The MCU Driver shall provide a service for activating the PLL clock distribution to the whole MCU

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12336 |
| Origin | AR |
| Category | Configuration and Initialization |
| Applicability | Applicable |
| Dependencies | [SRS_Mcu_12208], [SRS_Mcu_12392] |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall activate each supported PLL clock distribution only after that PLL is locked.

**Rationale**

Some microcontrollers contain multiple PLLs.

**Notes**

TBD

---

### MCU_REQ_006: The MCU Driver shall configure the clock safety features

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12207 |
| Origin | AR |
| Category | Configuration and Initialization |
| Applicability | Applicable |
| Dependencies | [SRS_Mcu_12208] |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall configure supported clock safety features, including crystal-loss handling and error notification controls.

**Rationale**

To support recovery or safe shutdown when the crystal clock is lost.

**Notes**

TBD

---

### MCU_REQ_007: The MCU Driver shall provide a service to initialize the clock system of the MCU

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12208 |
| Origin | AR |
| Category | Configuration and Initialization |
| Applicability | Applicable |
| Dependencies | [SRS_Mcu_12392] Provide lock status of PLL |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall initialize PLL factors, start the selected PLL lock process, and configure MCU-wide clock options without requiring a wait for PLL lock.

**Rationale**

TBD

**Notes**

TBD

---

### MCU_REQ_008: The MCU Driver shall provide a service for querying the standardized reset reason

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12000 |
| Origin | AR |
| Category | Normal Operation |
| Applicability | Applicable |
| Dependencies | None |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall report a supported standardized reset reason, using Power On Reset as the default.

**Rationale**

Different reset reasons can require different initialization actions.

**Notes**

Hardware need not distinguish every standardized reset reason.

---

### MCU_REQ_009: The MCU driver shall provide a service that allows to query the raw reset status

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12215 |
| Origin | AR |
| Category | Normal Operation |
| Applicability | Applicable |
| Dependencies | None |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall return the complete raw, microcontroller-specific reset information.

**Rationale**

To store reset information in diagnostic error memory after ECU start-up.

**Notes**

Return zero when the microcontroller has no reset status register.

---

### MCU_REQ_010: The MCU driver shall provide a reset trigger function

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12277 |
| Origin | AR |
| Category | Normal Operation |
| Applicability | Applicable |
| Dependencies | None |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall provide a configured hardware reset trigger when software-triggered reset is supported.

**Rationale**

To force controlled MCU reinitialization after unknown software states are detected.

**Notes**

The function shall not be used when the microcontroller cannot trigger a reset by software.

---

### MCU_REQ_011: The MCU Driver shall provide a service for querying the RAM status

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_13701 |
| Origin | AR |
| Category | Normal Operation |
| Applicability | Applicable |
| Dependencies | None |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall report RAM as valid or invalid when supported; otherwise, the function shall be disabled.

**Rationale**

Different RAM states can require different initialization actions.

**Notes**

RAM invalid is the default state when multiple states cannot be distinguished.

---

### MCU_REQ_012: The MCU driver shall provide a notification of failure of the clock source

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12394 |
| Origin | AR |
| Category | Fault operation |
| Applicability | Applicable |
| Dependencies | None |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall notify detectable clock-source failures outside the start-up phase.

**Rationale**

To allow an appropriate recovery action after a clock fault is detected.

**Notes**

TBD

---

### MCU_REQ_013: The MCU driver shall provide a service to activate MCU power saving modes of the µC

| Attribute | Value |
|---|---|
| Source | AUTOSAR_SRS_MCUDriver |
| Source ID | SRS_Mcu_12268 |
| Origin | AR |
| Category | Shutdown operation |
| Applicability | Applicable |
| Dependencies | [SRS_Mcu_12421] Low Power Mode Configuration |
| Architecture | TBD |
| Detailed Design | TBD |
| Status | Draft |

**Requirement**

The MCU Driver shall provide a service that activates MCU power-saving modes.

**Rationale**

TBD

**Notes**

Low power modes are not required on every microcontroller device.

---
