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
| Status | Draft |

## 2. Software Requirements

### MCU_SWRS_001: Software-Triggered Hardware Reset

**Type**

Functional

**Requirement**

The MCU Driver shall provide a service that triggers a hardware reset through software.

**Verification Criteria**

Given an authorized caller and an initialized MCU Driver, when the caller invokes the reset service, then the MCU shall undergo a hardware reset.

**Rationale**

To force controlled MCU reinitialization after an unknown software state is detected.

**Notes / Deviations**

Only an authorized user shall be able to call the reset service.

---

### MCU_SWRS_002: Get Last Reset Reason

**Type**

Functional

**Requirement**

The MCU Driver shall provide a service that returns the reason for the last reset when the hardware supports reset-reason detection.

**Verification Criteria**

Given the hardware supports reset-reason detection and a known reset has occurred, when the reset-reason service is called, then it shall return the reason corresponding to that reset.

**Rationale**

Different reset reasons can require different application actions after MCU reinitialization.

**Notes / Deviations**

An ECU can have several reset sources. The hardware is not required to distinguish every reset reason.

---

### MCU_SWRS_003: Enable and Configure the MCU Clock

**Type**

Functional

**Requirement**

The MCU Driver shall provide a service that enables and configures the MCU clock, including the CPU clock, peripheral clocks, prescalers, and multipliers.

**Verification Criteria**

Given a valid clock configuration, when the clock service is invoked, then the configured CPU clock, peripheral clocks, prescalers, and multipliers shall become active.

**Rationale**

TBD

**Notes / Deviations**

All available peripheral clocks shall be exposed to other BSW modules through the McuClockReferencePoint container.

---

### MCU_SWRS_004: Activate an MCU Reduced-Power Mode

**Type**

Functional

**Requirement**

The MCU Driver shall provide a service that activates a configured reduced-power mode available in the MCU hardware.

**Verification Criteria**

Given a configured reduced-power mode supported by the MCU hardware, when the mode service is invoked for that mode, then the MCU shall enter the requested reduced-power mode.

**Rationale**

TBD

**Notes / Deviations**

Some MCU mode configurations may permit wake-up only by hardware reset.

---

### MCU_SWRS_005: Configure MCU-Dependent Power Modes

**Type**

Configuration

**Requirement**

The MCU Driver configuration set shall define the MCU-dependent number and configuration of supported MCU modes.

**Verification Criteria**

Given the power modes available in the target MCU hardware, when the MCU Driver configuration set is inspected, then the configured mode count and each mode definition shall conform to the target MCU's supported modes.

**Rationale**

To expose the hardware-supported low-power modes required by the application.

**Notes / Deviations**

Activating a reduced-power mode may affect the PLL, internal oscillator, CPU clock, peripheral clocks, and power supplies. The upper layer is responsible for restoring normal operation or switching off the MCU power supply as applicable.

---

### MCU_SWRS_006: Detect Development Errors

**Type**

Error Handling

**Requirement**

Depending on the MCU Driver build version, the MCU Driver shall detect API calls with invalid parameters and the specified initialization or state errors using the corresponding error codes:

| Related error code | Value |
|---|---|
| `MCU_E_PARAM_CONFIG` | `0x0A` |
| `MCU_E_PARAM_CLOCK` | `0x0B` |
| `MCU_E_PARAM_MODE` | `0x0C` |
| `MCU_E_PARAM_RAMSECTION` | `0x0D` |
| `MCU_E_PLL_NOT_LOCKED` | `0x0E` |
| `MCU_E_UNINIT` | `0x0F` |
| `MCU_E_PARAM_POINTER` | `0x10` |
| `MCU_E_INIT_FAILED` | `0x11` |

**Verification Criteria**

Given a build version in which development error detection is enabled, when each specified invalid parameter, initialization, or MCU state condition is exercised, then the MCU Driver shall detect the condition using its corresponding error code and value.

**Rationale**

To provide standardized naming and classification of development errors.

**Notes / Deviations**

Applicability is TBD because the project build version and its development error detection setting are not specified. No MCU MRS requirement maps SRS_BSW_00327 or SRS_BSW_00337 to an internal upstream ID.

---

### MCU_SWRS_007: Report Clock Source Failure

**Type**

Error Handling

**Requirement**

When clock failure notification is enabled and a clock source failure occurs, the MCU Driver shall report `MCU_E_CLOCK_FAILURE` to DEM.

| Related error code | Value |
|---|---|
| `MCU_E_CLOCK_FAILURE` | Assigned by DEM |

**Verification Criteria**

Given clock failure notification is enabled, when a clock source failure occurs, then the MCU Driver shall report `MCU_E_CLOCK_FAILURE` using the DEM-assigned event value.

**Rationale**

To allow an appropriate recovery action after a clock fault is detected.

**Notes / Deviations**

This requirement applies only when clock failure notification is enabled in the MCU configuration set.

---

### MCU_SWRS_008: Detect MCU Clock Failure

**Type**

Error Handling

**Requirement**

The fail criterion for `MCU_E_CLOCK_FAILURE` shall be the occurrence of a clock source failure.

| Related error code | Value |
|---|---|
| `MCU_E_CLOCK_FAILURE` | Assigned by DEM |

**Verification Criteria**

Given clock failure notification is enabled, when a clock source failure occurs, then the `MCU_E_CLOCK_FAILURE` monitor shall evaluate the event as failed.

**Rationale**

To define the condition that identifies an active clock source failure.

**Notes / Deviations**

The fail criterion is active only when clock failure notification is enabled in the MCU configuration set.

---

### MCU_SWRS_009: Detect Recovery from MCU Clock Failure

**Type**

Error Handling

**Requirement**

The pass criterion for `MCU_E_CLOCK_FAILURE` shall be the absence of a clock source failure.

| Related error code | Value |
|---|---|
| `MCU_E_CLOCK_FAILURE` | Assigned by DEM |

**Verification Criteria**

Given clock failure notification is enabled, when no clock source failure is present, then the `MCU_E_CLOCK_FAILURE` monitor shall evaluate the event as passed.

**Rationale**

To define the condition that identifies recovery from a clock source failure.

**Notes / Deviations**

The pass criterion is active only when clock failure notification is enabled in the MCU configuration set.

---

### MCU_SWRS_010: Report Production Errors Through AUTOSAR DEM Callbacks

**Type**

Error Handling

**Requirement**

The MCU Driver shall follow the standardized AUTOSAR production-error reporting concept using callback routines specified by the Diagnostic Event Manager (DEM).

**Verification Criteria**

Given a configured and detectable MCU production error, when the error occurs, then the MCU Driver shall notify the error through the standardized DEM callback mechanism.

**Rationale**

TBD

**Notes / Deviations**

The source block does not specify a related error code or value.

---

### MCU_SWRS_011: Exclude Production Errors from Function Return Values

**Type**

Error Handling

**Requirement**

The MCU Driver shall not use a production error as the return value of a called function.

**Verification Criteria**

Given an MCU Driver function is called and a production error occurs during that call, when the function returns, then its return value shall not encode or report the production error.

**Rationale**

TBD

**Notes / Deviations**

The source block does not specify a related error code or value.

---

## 3. Traceability Matrix

| SWRS ID | SWS Source ID | Upstream | Category | Type | Applicability | Dependencies | Architecture | Detailed Design | Test IDs | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| MCU_SWRS_001 | SWS_Mcu_00055 | [MCU_MRS_010] | Reset | Functional | Applicable | None | TBD | TBD | TBD | Draft |
| MCU_SWRS_002 | SWS_Mcu_00052 | [MCU_MRS_008] | Reset | Functional | Applicable | None | TBD | TBD | TBD | Draft |
| MCU_SWRS_003 | SWS_Mcu_00248 | [MCU_MRS_007] | Clock | Functional | Applicable | [MCU_MRS_004] | TBD | TBD | TBD | Draft |
| MCU_SWRS_004 | SWS_Mcu_00164 | [MCU_MRS_013] | MCU Mode service | Functional | Applicable | [MCU_MRS_001] | TBD | TBD | TBD | Draft |
| MCU_SWRS_005 | SWS_Mcu_00165 | [MCU_MRS_001] | MCU Mode service | Configuration | Applicable | [MCU_MRS_013] | TBD | TBD | TBD | Draft |
| MCU_SWRS_006 | SWS_Mcu_00012 | N/A | Development Errors | Error Handling | TBD | None | TBD | TBD | TBD | Draft |
| MCU_SWRS_007 | SWS_Mcu_00053 | [MCU_MRS_012] | Extended Production Errors (for Release 4.1.1) | Error Handling | Applicable | Clock failure notification enabled | TBD | TBD | TBD | Draft |
| MCU_SWRS_008 | SWS_Mcu_00257 | [MCU_MRS_012], [MCU_SWRS_007] | MCU_E_CLOCK_FAILURE | Error Handling | Applicable | Clock failure notification enabled | TBD | TBD | TBD | Draft |
| MCU_SWRS_009 | SWS_Mcu_00258 | [MCU_MRS_012], [MCU_SWRS_007] | MCU_E_CLOCK_FAILURE | Error Handling | Applicable | Clock failure notification enabled | TBD | TBD | TBD | Draft |
| MCU_SWRS_010 | SWS_Mcu_00051 | [MCU_MRS_012] | Error notification | Error Handling | Applicable | DEM | TBD | TBD | TBD | Draft |
| MCU_SWRS_011 | SWS_Mcu_00226 | [MCU_MRS_012], [MCU_SWRS_010] | Error notification | Error Handling | Applicable | None | TBD | TBD | TBD | Draft |

## 4. Traceability Rules

- Each SWRS requirement shall have one unique `MCU_SWRS_nnn` identifier.
- `SWS Source ID` shall reference the originating AUTOSAR SWS requirement.
- `Upstream` shall reference the MRS, SWRS, or other requirement(s) from which the SWRS is derived. Use `N/A` only with a documented rationale in `Notes / Deviations`.
- `Type`, `Applicability`, dependencies, downstream links, and status shall be maintained only in the Traceability Matrix to avoid duplication.
- Explain `Partial`, `Not Applicable`, or `TBD` applicability in `Notes / Deviations`.
- `Architecture`, `Detailed Design`, and `Test IDs` may remain `TBD` until those artifacts are created.
- Split a source requirement only when its behaviors have different applicability, design allocation, or verification criteria.
- Do not duplicate the SWS text without refinement; capture project-specific behavior, constraints, and applicability.
