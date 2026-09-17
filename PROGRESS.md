# SDE-1 Learning Progress

## Tracking Format
- **Status**: Not Started | In Progress | Notes Generated | Review Complete
- **Last Updated**: timestamp

## MODULE 1 — JavaScript

### Unit 1.1 — The Execution Model
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.1.1 | How JS runs: parsing, creation/execution, hoisting | Notes Generated | 01-01-the-execution-model-part1.md |
| 1.1.2 | var vs let vs const, TDZ | Notes Generated | 01-01-the-execution-model-part1.md |
| 1.1.3 | Call stack, stack trace, stack overflow | In Progress | - |
| 1.1.4 | Lexical scope and scope chain | Not Started | - |
| 1.1.5 | Closures: what's retained, loop puzzle, real uses | Not Started | - |
| 1.1.6 | Closures and memory leaks | Not Started | - |
| 1.1.7 | IIFEs and module pattern | Not Started | - |

### Unit 1.2 — Types and Coercion
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.2.1 | 7 primitives + object, typeof lies | Not Started | - |
| 1.2.2 | Value vs reference semantics | Not Started | - |
| 1.2.3 | Abstract vs strict equality | Not Started | - |
| 1.2.4 | Truthy/falsy values | Not Started | - |
| 1.2.5 | null vs undefined, ?? vs || | Not Started | - |
| 1.2.6 | NaN, Object.is, floating-point, BigInt | Not Started | - |
| 1.2.7 | Shallow vs deep copy | Not Started | - |

### Unit 1.3 — Functions and this
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.3.1 | Functions as first-class values, HOFs | Not Started | - |
| 1.3.2 | Four binding rules for this | Not Started | - |
| 1.3.3 | Arrow functions | Not Started | - |
| 1.3.4 | call, apply, bind + myBind impl | Not Started | - |
| 1.3.5 | Parameters: defaults, rest, spread, destructuring | Not Started | - |
| 1.3.6 | Currying and partial application | Not Started | - |
| 1.3.7 | Pure functions, side effects, referential transparency | Not Started | - |

### Unit 1.4 — Objects and Prototypes
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.4.1 | Object creation patterns | Not Started | - |
| 1.4.2 | Property descriptors, Object.freeze | Not Started | - |
| 1.4.3 | Getters, setters, computed keys | Not Started | - |
| 1.4.4 | Prototype chain | Not Started | - |
| 1.4.5 | Constructor functions, new operator | Not Started | - |
| 1.4.6 | class syntax as sugar | Not Started | - |
| 1.4.7 | Prototypal vs classical inheritance | Not Started | - |
| 1.4.8 | Object iteration methods | Not Started | - |

### Unit 1.5 — Arrays and Data Transformation
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.5.1 | Array creation, Array.from/of | Not Started | - |
| 1.5.2 | map, filter, reduce (implement all 3) | Not Started | - |
| 1.5.3 | reduce in depth | Not Started | - |
| 1.5.4 | find, findIndex, some, every, includes | Not Started | - |
| 1.5.5 | sort: comparator, stability, multi-key | Not Started | - |
| 1.5.6 | Mutating vs non-mutating methods | Not Started | - |
| 1.5.7 | Set and Map, WeakMap/WeakSet | Not Started | - |
| 1.5.8 | Immutable update patterns for nested state | Not Started | - |

### Unit 1.6 — Asynchronous JavaScript
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.6.1 | Why async: single-threaded, blocking | Not Started | - |
| 1.6.2 | Event loop: call stack, Web APIs, task/microtask | Not Started | - |
| 1.6.3 | Microtask vs macrotask starvation | Not Started | - |
| 1.6.4 | Callbacks, callback hell, inversion of control | Not Started | - |
| 1.6.5 | Promises: states, then/catch/finally, chaining | Not Started | - |
| 1.6.6 | Error propagation through chains | Not Started | - |
| 1.6.7 | Promise.all / allSettled / race / any | Not Started | - |
| 1.6.8 | async/await, sequential vs parallel | Not Started | - |
| 1.6.9 | try/catch, error patterns, async iterators | Not Started | - |
| 1.6.10 | AbortController, request cancellation | Not Started | - |
| 1.6.11 | Timers: setTimeout/setInterval | Not Started | - |
| 1.6.12 | Debounce and throttle (implement both) | Not Started | - |

### Unit 1.7 — Modules and Tooling
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.7.1 | Why modules exist | Not Started | - |
| 1.7.2 | ESM: import/export, live bindings | Not Started | - |
| 1.7.3 | CommonJS vs ESM | Not Started | - |
| 1.7.4 | Dynamic import, code splitting | Not Started | - |
| 1.7.5 | What a bundler does | Not Started | - |
| 1.7.6 | Transpilation vs polyfilling | Not Started | - |
| 1.7.7 | Tree shaking, side effects | Not Started | - |
| 1.7.8 | package.json full | Not Started | - |

### Unit 1.8 — Browser, DOM and Networking
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.8.1 | Critical rendering path | Not Started | - |
| 1.8.2 | DOM selection, layout thrashing | Not Started | - |
| 1.8.3 | Reflow vs repaint | Not Started | - |
| 1.8.4 | Event model: capturing, target, bubbling | Not Started | - |
| 1.8.5 | Event delegation | Not Started | - |
| 1.8.6 | fetch: request/response, error handling | Not Started | - |
| 1.8.7 | CORS | Not Started | - |
| 1.8.8 | Storage: localStorage, cookies, IndexedDB | Not Started | - |
| 1.8.9 | Script loading: defer vs async | Not Started | - |
| 1.8.10 | Observers: IntersectionObserver, ResizeObserver | Not Started | - |
| 1.8.11 | Web Workers | Not Started | - |

### Unit 1.9 — Modern Syntax and Advanced Corners
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.9.1 | Destructuring: nested, renamed, defaults | Not Started | - |
| 1.9.2 | Optional chaining, nullish coalescing | Not Started | - |
| 1.9.3 | Template literals and tagged templates | Not Started | - |
| 1.9.4 | Symbols and well-known symbols | Not Started | - |
| 1.9.5 | Iterators and generators | Not Started | - |
| 1.9.6 | Proxy and Reflect | Not Started | - |
| 1.9.7 | Error handling: custom errors, cause | Not Started | - |
| 1.9.8 | Strict mode | Not Started | - |

### Unit 1.10 — TypeScript
| Atom | Topic | Status | Notes File |
|------|-------|--------|------------|
| 1.10.1 | Why types, structural vs nominal | Not Started | - |
| 1.10.2 | Primitives, arrays, tuples, any/unknown/never | Not Started | - |
| 1.10.3 | Interfaces vs type aliases | Not Started | - |
| 1.10.4 | Union, intersection, literal, discriminated unions | Not Started | - |
| 1.10.5 | Narrowing | Not Started | - |
| 1.10.6 | Generics: functions, interfaces, constraints | Not Started | - |
| 1.10.7 | Utility types | Not Started | - |
| 1.10.8 | Typing React | Not Started | - |
| 1.10.9 | tsconfig essentials | Not Started | - |
| 1.10.10 | Declaration files, Zod | Not Started | - |

---
*Remaining modules (2-17) will be added as we progress*
