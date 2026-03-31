# AI Slop Patterns

Reference catalog for the code-scanner-agent. These are common AI-generated code patterns that degrade codebase quality.

## Comments to Remove

- Obvious/redundant comments explaining what code clearly does
- Comments that don't match the commenting style elsewhere in the file
- Section divider comments when not used elsewhere
- `// TODO` or `// FIXME` comments added by the AI with no actionable context
- Comments restating the function signature or variable name

## Defensive Code to Remove

- Try/catch blocks around code that doesn't throw
- Null/undefined checks when callers guarantee valid input
- Type guards that duplicate earlier validation
- Fallback values for parameters that are always provided
- Redundant `if (!x) return` guards when `x` is guaranteed by the caller
- Empty catch blocks that silently swallow errors

## Type Issues to Fix

- Casts to `any` that bypass TypeScript's type system
- Type assertions (`as Type`) that hide real type mismatches
- Overly broad generic types when specific types exist
- `unknown` used as a lazy escape hatch instead of proper typing
- Redundant type annotations on variables where inference is sufficient

## Structural Patterns to Flag

- Unnecessary abstraction layers (wrapper functions that just call another function)
- Single-use utility functions that obscure inline logic
- Over-engineered error handling for internal code paths
- Feature flags or backwards-compatibility shims for code that was just written
- Premature abstractions (interfaces/classes for one implementation)
- Re-exported types or renamed `_unused` variables instead of deletion
