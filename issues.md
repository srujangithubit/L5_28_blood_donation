# Static Code Analysis Issues

The line numbers below refer to the original `blood_donation.py` scanned before fixes. Line numbers may change after editing.

| Issue | Type / Severity | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command built from phone numbers | Security — High (Bandit B605) | 63–65; reported at 65 | `os.system()` invokes a shell with values joined into a command string, creating a command-injection risk. | Remove the unused SMS stub rather than invoking a shell command. A real notification feature should use a supported SMS-provider API and validated recipients. |
| Insecure temporary filename | Security — Medium (Bandit B306) | 58–60; reported at 60 | `tempfile.mktemp()` returns a name without securely creating and reserving the file. | Use `tempfile.NamedTemporaryFile()` with `delete=False` when a persistent path is required. |
| Mutable default list | Correctness / maintainability — Medium (Pylint W0102) | 17 | `notes=[]` is created once and can be shared across calls, causing notes to persist unexpectedly. | Use `notes=None` and create a new list inside the function. |
| Broad exception handler | Reliability — Medium (Pylint W0718) | 42–46; reported at 45 | `except Exception` hides unexpected errors and makes failures look like a valid zero-stock result. | Validate the patient group before summing; return zero explicitly for an unknown group to preserve the demo's existing behavior. |
| Assertion used for input validation | Security / correctness — Low (Bandit B101) | 17–18; reported at 18 | Assertions can be removed when Python runs with optimization, so they should not validate ordinary user input. | Replace the assertion with an explicit check and raise `ValueError` for an unknown donor blood group. |
| Hard-coded password | Security — Low (Bandit B105) | 5 | `OFFICER_PASSWORD` stores a password-like value directly in source code, although the demo does not use it. | Remove the unused constant. Real authentication should use a proper authentication flow and secure secret configuration. |
| Missing module/function docstrings and naming conventions | Maintainability / style (Pylint C0114, C0116, C0103) | 1, 17, 27, 33, 42, 49, 53, 58, 63, 68 | The module and functions lack documentation, and names such as `registerDonor` do not follow Python's `snake_case` convention. | Add concise docstrings and rename functions and parameters to `snake_case`, updating their call sites. |
| Flake8 style violations | Style (Flake8 E501, E303, E261, E225) | 7, 58, 80, 81 | The file contains an overlong line, too many blank lines, an improperly spaced inline comment, and missing whitespace around an operator. | Wrap long lines, remove excess blank lines, and apply standard spacing. |
