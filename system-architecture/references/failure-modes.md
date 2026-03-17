# Failure Mode Criticality

Classify each failure scenario identified during architecture validation.

| Criticality | Definition | Required Handling |
|-------------|-----------|-------------------|
| **CRITICAL** | Data loss, security breach, payment error | Explicit error handling, monitoring alert, automated test |
| **HIGH** | Feature broken, user blocked | Error recovery path, manual fallback documented |
| **MEDIUM** | Degraded experience, slow response | Graceful degradation, retry logic |
| **LOW** | Cosmetic, non-blocking | Log for next cycle |

For each API endpoint and data flow, ask: "What happens when this fails?" Then classify the answer.
