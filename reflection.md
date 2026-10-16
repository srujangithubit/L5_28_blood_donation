# Lab 5: Static Code Analysis — Reflection

**Note:** The uploaded handout describes reflection questions but does not contain the four questions themselves. The responses below are drafted from the objective and learning outcomes printed in the handout. If your instructor provided a separate page with the exact questions, use those prompts to check whether any answer needs to be reworded.

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without running the program to identify potential defects, insecure patterns, and style violations. In this lab, it helped identify problems that were not obvious from the program's normal demonstration output, such as the mutable default list, broad exception handling, unsafe temporary-file creation, and shell command construction. It is useful because these issues can be identified early, before the code is deployed or used with real data.

## 2. What did Pylint, Bandit, and Flake8 identify?

Pylint reported maintainability and code-quality issues, including missing module and function docstrings, names that did not follow `snake_case`, a mutable default argument, and catching the overly broad `Exception` class. Bandit identified security-related patterns: a hard-coded password-like constant, use of `assert` for validation, `tempfile.mktemp()`, and calling `os.system()` with a command assembled from supplied values. Flake8 found style violations related to line length, extra blank lines, inline-comment spacing, and missing whitespace around an operator. Each tool focused on a different part of code quality.

## 3. Which issues were most important, and how were they addressed?

The highest-priority finding was the Bandit B605 warning for starting a shell process. Joining phone-list values into a shell command can allow command injection, so the unused SMS helper was removed rather than keeping an unsafe command. The insecure `tempfile.mktemp()` call was replaced with `NamedTemporaryFile()`. The mutable default `notes=[]` was changed to `notes=None` with initialization inside the function. Broad exception handling was removed from the stock lookup, and ordinary input validation now uses an explicit check instead of `assert`. The unused hard-coded password constant was removed. Function names and documentation were improved, and formatting was corrected.

## 4. What did this lab teach about maintainability and verification?

The lab showed that clean output from a demonstration does not prove that a program is secure or well-maintained. Static analysis finds suspicious patterns, but its reports still need to be interpreted in context and the fixes must preserve the intended behavior. After editing, the program should be run again and checked with all three tools. Regression checks are also important: the blood-stock output should remain consistent, valid blood groups should use the correct red-blood-cell compatibility mapping, and invalid inputs should be handled deliberately. Static analysis complements testing; it does not replace functional tests or real-world security review.
