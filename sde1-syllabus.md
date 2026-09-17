# The SDE-1 Syllabus
### A tier-3 gap-closing curriculum for .NET + React engineers

**How to read this document.** Every module has three layers:

- **MODULE** — the big area (e.g. JavaScript)
- **UNIT** — a coherent chunk you'd study over a few days (e.g. The Execution Model)
- **ATOM** — one sitting, 1–3 hours, one idea, one thing you can now explain or build

Each module opens with **Why this exists** — the actual failure mode in production or in an interview that this knowledge prevents. If you can't articulate the why, you'll forget the what.

---

## PART 0 — Turning Learning Into Knowledge

This is the part most roadmaps skip, and it's the reason people finish 200-hour courses and remember nothing. Read this before anything else.

### 0.1 The four states of knowing

1. **Recognised** — "I've seen that word." Useless.
2. **Recalled** — you can define it from memory. Passes a quiz, fails an interview.
3. **Explained** — you can teach it to someone else including *why it works that way*. Passes an interview.
4. **Applied** — you reach for it unprompted while solving something new. This is engineering.

Every atom in this document should end at state 3 minimum. The build projects push you to 4.

### 0.2 The loop that actually works

For each atom:

1. **Predict first.** Before reading, write one sentence guessing what it is. Being wrong is what makes it stick.
2. **Learn actively.** No passive video watching. Pause, type the code yourself, break it deliberately.
3. **Produce something.** A code snippet you wrote, a diagram you drew, or 5 lines in your own words. If nothing was produced, it didn't happen.
4. **Explain it out loud** in under 90 seconds, as if to a junior. Record it on your phone occasionally. Where you stumble is where you don't understand.
5. **Schedule the recall.** Add a question to your review deck. Answer it at day 1, day 7, day 30.

### 0.3 Your two artifacts

**The notebook.** One markdown repo, one file per unit. Structure each file:

```
# Unit name
## The problem this solves
## The mental model (one paragraph, no jargon)
## The details
## The gotchas / things that bit me
## Interview-shaped questions I can now answer
```

Write this *after* studying, from memory, then correct it. Writing from memory is the study session; writing while copying is not.

**The review deck.** Anki, or a simple spreadsheet with a date column. Questions must be *why*-shaped, not *what*-shaped:

- Bad: "What is a closure?"
- Good: "Why does a `for (var i...)` loop with `setTimeout` print the same number every time, and what exactly changes with `let`?"

### 0.4 Ratios that keep you honest

- **60% building, 40% consuming.** If the ratio inverts for two weeks straight, you're in tutorial hell.
- **One project per module.** Not a tutorial clone — something you specified yourself, however small.
- **Every module ends with a written "proof"** — the build, plus the section in the notebook, plus 10 review cards.

### 0.5 The tier-3 gap, specifically

The gap is rarely syntax. It's these four things, and this syllabus attacks each one deliberately:

1. **No mental model of the machine.** You know `async/await` but not what a thread is, what a context switch costs, or why a blocking call in a request handler destroys throughput. → *Fixed by the OS, Networks and Concurrency modules.*
2. **No exposure to scale.** Your college project had 1 user and 50 rows. You've never seen an N+1 query, a missing index, or a cache stampede. → *Fixed by Databases and HLD.*
3. **No design vocabulary.** You can make it work but can't defend a class structure or name a trade-off. → *Fixed by LLD.*
4. **No "why" behind tooling.** You use React and EF Core as magic boxes, so you can't debug them when they behave unexpectedly. → *Fixed by the "how it works underneath" atoms in every module.*

### 0.6 Sequencing and realistic timeline

Assume 2–3 focused hours on weekdays, 5–6 on weekends. That is roughly **12–14 months** to get through this properly. Do not run modules in parallel beyond the pairing shown — depth beats breadth here.

| Phase | Months | Modules | Why this order |
|---|---|---|---|
| **1. Language foundations** | 1–2 | JavaScript, C# + OOP, Engineering Hygiene | You cannot learn a framework before its language. Every later module assumes you can read and write both. |
| **2. Problem solving** | 3–4 | DSA in C# | Slots here because it needs C# fluency in front of it, and because the reasoning-about-cost habit it builds pays off in every module after. |
| **3. Build things** | 5–6 | CSS/SCSS, React, ASP.NET Core, Databases | This is your employable core. Ship a real full-stack app at the end. |
| **4. The machine underneath** | 7–9 | Operating Systems, Networks, Terminal/Containers/Cloud, Security, Multithreading | Now you have concrete experiences to attach these abstractions to. Learning OS before you've written a web server is memorisation; learning it after is comprehension. |
| **5. Design** | 10–12 | LLD, Machine Coding, HLD basics | Design only means something once you've felt the pain of bad design. |
| **6. Frontier** | 13 | Agentic AI, plus interview consolidation | Highest-leverage differentiator, lowest foundational dependency — so it goes last. |

---

## PART 1 — FOUNDATIONS

---

# MODULE 1 — JavaScript

> **Why this exists.** React is a library, not a language. Almost every "React bug" is actually a JavaScript misunderstanding — stale closures, reference equality, `this` binding, unhandled promise rejection. Engineers who learn React without learning JavaScript hit a ceiling in about eight months and can never debug anything the tutorial didn't cover. Also: JS is the most-interviewed frontend topic and the one where tier-3 candidates are most obviously exposed.

### Unit 1.1 — The Execution Model

*Why: this single unit explains "why is this `undefined`", stale state in React, and half of all interview trick questions.*

- **Atom 1.1.1** — How JS runs: parsing, the two-phase creation/execution of an execution context, and why hoisting exists as a consequence.
- **Atom 1.1.2** — `var` vs `let` vs `const`: function scope vs block scope, the Temporal Dead Zone, and why `const` doesn't mean immutable.
- **Atom 1.1.3** — The call stack. Trace a nested function call by hand. Read a stack trace properly. Cause and recognise a stack overflow.
- **Atom 1.1.4** — Lexical scope and the scope chain. Why scope is decided at *write* time, not call time.
- **Atom 1.1.5** — **Closures.** What is actually retained in memory, the classic loop-with-`setTimeout` puzzle, and three real uses: private state, function factories, memoisation.
- **Atom 1.1.6** — Closures and memory leaks: when a closure keeps a large object alive longer than you intended.
- **Atom 1.1.7** — IIFEs and the module pattern; why they mattered pre-ESM and where you still see them.

**Proof:** implement `once(fn)`, `memoize(fn)`, and a counter factory with truly private state — no classes, no external variables.

### Unit 1.2 — Types and Coercion

*Why: `==` bugs, `NaN` propagation, and the "why did my object comparison fail" class of bugs.*

- **Atom 1.2.1** — The 7 primitives + object. `typeof` and its famous lies (`typeof null`, `typeof function`).
- **Atom 1.2.2** — Value vs reference semantics. Assignment, function arguments, and why mutating a prop breaks React.
- **Atom 1.2.3** — Abstract vs strict equality. Read the coercion table once, then commit to `===` forever and know *why*.
- **Atom 1.2.4** — Truthy/falsy: the exact list of 8 falsy values. Why `if (count)` is a bug when `count` can be 0.
- **Atom 1.2.5** — `null` vs `undefined` — the intent difference. `??` vs `||` and when the distinction bites.
- **Atom 1.2.6** — `NaN`, `Object.is`, `-0`, floating-point (`0.1 + 0.2`), `Number.EPSILON`, `BigInt`.
- **Atom 1.2.7** — Shallow vs deep copy: spread, `Object.assign`, `structuredClone`, and hand-writing a `deepClone` with cycle handling.

**Proof:** write your own `deepEqual(a, b)` handling arrays, objects, dates, `NaN`, and nested cycles.

### Unit 1.3 — Functions and `this`

*Why: `this` is the #1 source of confusion for developers coming from C#-style languages, where `this` is static.*

- **Atom 1.3.1** — Functions as first-class values: passing, returning, storing. Higher-order functions.
- **Atom 1.3.2** — The four binding rules for `this`: default, implicit, explicit, `new`. Determine `this` for any call site in 10 seconds.
- **Atom 1.3.3** — Arrow functions: lexical `this`, no `arguments`, not constructible. When an arrow function is *wrong*.
- **Atom 1.3.4** — `call`, `apply`, `bind`. Then implement `Function.prototype.myBind` yourself.
- **Atom 1.3.5** — Parameters: defaults, rest, spread, destructuring with defaults, `arguments` vs rest.
- **Atom 1.3.6** — Currying and partial application. Implement `curry(fn)` supporting `f(1)(2)(3)` and `f(1,2)(3)`.
- **Atom 1.3.7** — Pure functions, side effects, referential transparency. Why this matters for React rendering.

### Unit 1.4 — Objects and Prototypes

*Why: JS's inheritance is fundamentally different from C#'s. Understanding this is what separates "I use classes" from "I understand the object model."*

- **Atom 1.4.1** — Object creation: literals, `new`, `Object.create`, factory functions.
- **Atom 1.4.2** — Property descriptors: `writable`, `enumerable`, `configurable`. `Object.freeze` and its shallowness.
- **Atom 1.4.3** — Getters, setters, computed keys, shorthand.
- **Atom 1.4.4** — **The prototype chain.** `[[Prototype]]` vs `.prototype`, lookup resolution, `Object.getPrototypeOf`.
- **Atom 1.4.5** — Constructor functions and what `new` actually does (all four steps).
- **Atom 1.4.6** — `class` syntax as sugar: `extends`, `super`, static members, private `#fields`, `instanceof`.
- **Atom 1.4.7** — Prototypal vs classical inheritance — articulate the difference to someone who only knows C#.
- **Atom 1.4.8** — `Object.keys/values/entries`, `for...in` vs `for...of`, `hasOwnProperty` and why you should use `Object.hasOwn`.

**Proof:** implement `myNew(Constructor, ...args)` and a working `Object.create` polyfill.

### Unit 1.5 — Arrays and Data Transformation

*Why: 80% of frontend work is reshaping data. Fluency here is the difference between 5 lines and 40.*

- **Atom 1.5.1** — Array creation, holes, `Array.from`, `Array.of`, array-likes vs true arrays.
- **Atom 1.5.2** — `map`, `filter`, `reduce` — and implement all three as polyfills.
- **Atom 1.5.3** — `reduce` in depth: grouping, flattening, building lookups, and composing functions with it.
- **Atom 1.5.4** — `find`, `findIndex`, `some`, `every`, `includes`, `indexOf` and the `NaN` gotcha.
- **Atom 1.5.5** — `sort`: the comparator contract, why default sort is lexicographic, stability, sorting objects by multiple keys.
- **Atom 1.5.6** — Mutating vs non-mutating methods. `splice` vs `slice`. The new immutable methods (`toSorted`, `toReversed`, `with`).
- **Atom 1.5.7** — `Set` and `Map`: when they beat objects and arrays, iteration order, `WeakMap`/`WeakSet` and their GC role.
- **Atom 1.5.8** — Immutable update patterns for nested state — the exact skill React demands.

**Proof:** given a flat array of records, produce a nested tree, a grouped summary, and a sorted-paginated slice — no libraries.

### Unit 1.6 — Asynchronous JavaScript

*Why: this is the highest-value unit in the entire frontend track. It's the most common interview topic and the source of the most subtle bugs.*

- **Atom 1.6.1** — Why async exists: JS is single-threaded, the browser is not. Blocking the main thread = frozen UI.
- **Atom 1.6.2** — **The event loop**: call stack, Web APIs, task (macrotask) queue, microtask queue. Hand-trace the output order of mixed `setTimeout`/`Promise`/sync code.
- **Atom 1.6.3** — Microtask vs macrotask starvation; `queueMicrotask`; where `requestAnimationFrame` sits.
- **Atom 1.6.4** — Callbacks, callback hell, inversion of control — the problem Promises were invented to fix.
- **Atom 1.6.5** — Promises: the three states, `then`/`catch`/`finally`, the chaining contract, how return values flow.
- **Atom 1.6.6** — Error propagation through a chain. Unhandled rejections. Why a missing `return` silently breaks a chain.
- **Atom 1.6.7** — `Promise.all` / `allSettled` / `race` / `any` — and *when each is the right choice*.
- **Atom 1.6.8** — `async`/`await` as syntax over promises. Sequential vs parallel `await` — the most common real performance bug.
- **Atom 1.6.9** — `try/catch` with await, error handling patterns, `for await...of`, async iterators and generators.
- **Atom 1.6.10** — `AbortController`, request cancellation, and cleaning up on unmount.
- **Atom 1.6.11** — Timers: `setTimeout`/`setInterval` accuracy, drift, clearing. Implement `sleep`.
- **Atom 1.6.12** — **Debounce and throttle** — implement both from scratch, know the exact behavioural difference, and name a real use case for each.

**Proof:** implement `Promise` from scratch (states, `then`, chaining), plus `promiseAll`, `promiseRace`, `retryWithBackoff`, and a `promisePool` with concurrency limit.

### Unit 1.7 — Modules and Tooling

*Why: you'll debug build errors weekly. Not knowing what a bundler does makes those errors unsolvable.*

- **Atom 1.7.1** — Why modules exist: the global-namespace problem they replaced.
- **Atom 1.7.2** — ESM: `import`/`export`, named vs default, live bindings, static analysability.
- **Atom 1.7.3** — CommonJS vs ESM: `require` vs `import`, sync vs async, and the interop pain in Node.
- **Atom 1.7.4** — Dynamic `import()` and code splitting.
- **Atom 1.7.5** — What a bundler actually does: dependency graph, transformation, output. Vite vs Webpack conceptually; dev server vs production build.
- **Atom 1.7.6** — Transpilation vs polyfilling. What Babel does. Browser targets.
- **Atom 1.7.7** — Tree shaking, side effects, and why your bundle is 3MB.
- **Atom 1.7.8** — `package.json` in full: dependencies vs devDependencies vs peer, semver ranges, lockfiles and why you commit them, `npm ci` vs `npm install`.

### Unit 1.8 — Browser, DOM and Networking

*Why: React abstracts the DOM but doesn't eliminate it. Every machine-coding round needs event handling; every real app hits CORS.*

- **Atom 1.8.1** — The critical rendering path: HTML → DOM → CSSOM → render tree → layout → paint → composite.
- **Atom 1.8.2** — DOM selection and manipulation; `createElement`, fragments, and why layout thrashing is slow.
- **Atom 1.8.3** — Reflow vs repaint. Which operations trigger which. Batching reads and writes.
- **Atom 1.8.4** — The event model: capturing, target, bubbling. `stopPropagation` vs `preventDefault`.
- **Atom 1.8.5** — **Event delegation** — the pattern behind every efficient list handler.
- **Atom 1.8.6** — `fetch`: request/response, headers, methods, JSON, error handling (and why a 404 doesn't reject).
- **Atom 1.8.7** — **CORS**: same-origin policy, preflight requests, `Access-Control-Allow-*`, credentials. Why "just disable CORS" is not an answer.
- **Atom 1.8.8** — Storage: `localStorage`, `sessionStorage`, cookies (`HttpOnly`, `Secure`, `SameSite`), IndexedDB. Which to use for auth tokens and why.
- **Atom 1.8.9** — Script loading: `defer` vs `async`, placement, render blocking.
- **Atom 1.8.10** — Observers: `IntersectionObserver` (infinite scroll, lazy loading), `ResizeObserver`, `MutationObserver`.
- **Atom 1.8.11** — Web Workers: true parallelism in the browser, the messaging boundary, when it's worth it.

### Unit 1.9 — Modern Syntax and Advanced Corners

- **Atom 1.9.1** — Destructuring: nested, renamed, defaults, in parameters.
- **Atom 1.9.2** — Optional chaining `?.`, nullish coalescing `??`, logical assignment operators.
- **Atom 1.9.3** — Template literals and tagged templates.
- **Atom 1.9.4** — Symbols and well-known symbols (`Symbol.iterator`, `Symbol.asyncIterator`).
- **Atom 1.9.5** — Iterators and generators: the protocol, `yield`, lazy sequences, infinite sequences.
- **Atom 1.9.6** — `Proxy` and `Reflect` — the mechanism behind reactive frameworks like Vue and MobX.
- **Atom 1.9.7** — Error handling: custom `Error` subclasses, `cause`, error boundaries at the app level.
- **Atom 1.9.8** — Strict mode; what it changes and why it's on by default in modules.

### Unit 1.10 — TypeScript (non-negotiable addition)

*Why: you're a C# developer. TypeScript is how you bring that type safety to the frontend, and it's now the industry default — a JS-only frontend developer is at a real disadvantage.*

- **Atom 1.10.1** — Why types: errors at compile time vs 2am. Structural vs nominal typing (the key mental shift from C#).
- **Atom 1.10.2** — Primitives, arrays, tuples, `any` vs `unknown` vs `never`.
- **Atom 1.10.3** — Interfaces vs type aliases; when each is idiomatic.
- **Atom 1.10.4** — Union and intersection types; literal types; discriminated unions and exhaustive `switch`.
- **Atom 1.10.5** — Narrowing: `typeof`, `in`, `instanceof`, type predicates (`x is Foo`).
- **Atom 1.10.6** — Generics: functions, interfaces, constraints, defaults. Compare directly to C# generics.
- **Atom 1.10.7** — Utility types: `Partial`, `Pick`, `Omit`, `Record`, `Required`, `Readonly`, `ReturnType`.
- **Atom 1.10.8** — Typing React: props, children, events, hooks, generic components.
- **Atom 1.10.9** — `tsconfig` essentials: `strict`, `noUncheckedIndexedAccess`, module resolution.
- **Atom 1.10.10** — Declaration files, `unknown` at API boundaries, runtime validation with Zod.

### 📦 MODULE 1 PROOF OF LEARNING

Build a **vanilla JS + TypeScript single-page app** — no framework. A movie search with debounced input, cancellable in-flight requests, infinite scroll via `IntersectionObserver`, a favourites list persisted to `localStorage`, and a custom event-delegated list. Then write your own tiny `Promise` implementation and 20 polyfills in a repo.

---

# MODULE 2 — CSS and SCSS

> **Why this exists.** Backend-leaning developers treat CSS as guesswork — they add properties until it looks right. That's not a skill gap in syntax, it's a missing mental model of the layout algorithms. Two afternoons on the box model, stacking contexts and flex/grid algorithms permanently ends the guessing.

### Unit 2.1 — CSS Fundamentals (do this before touching SCSS)

- **Atom 2.1.1** — The cascade: origin, importance, specificity, source order. Calculate specificity by hand. Why `!important` is a symptom.
- **Atom 2.1.2** — Inheritance, `inherit`/`initial`/`unset`/`revert`.
- **Atom 2.1.3** — The box model: content, padding, border, margin. `box-sizing: border-box` and why everyone sets it globally.
- **Atom 2.1.4** — Margin collapsing — the rules, and why your spacing "disappeared".
- **Atom 2.1.5** — `display`: block, inline, inline-block, none, and the flow model.
- **Atom 2.1.6** — Positioning: static, relative, absolute, fixed, sticky. What "containing block" means for each.
- **Atom 2.1.7** — **Stacking contexts and `z-index`** — why your `z-index: 9999` doesn't work.
- **Atom 2.1.8** — **Flexbox**: main/cross axis, `flex-grow`/`shrink`/`basis`, alignment, `flex-wrap`. The `flex: 1` shorthand explained.
- **Atom 2.1.9** — **Grid**: template rows/columns, `fr`, `repeat`, `minmax`, `auto-fit`/`auto-fill`, areas, gap. When grid beats flex.
- **Atom 2.1.10** — Units: px, rem, em, %, vh/vw/dvh, ch. When each is correct.
- **Atom 2.1.11** — Responsive design: mobile-first, media queries, container queries, fluid typography with `clamp()`.
- **Atom 2.1.12** — Custom properties (CSS variables), scoping, and runtime theming (dark mode).
- **Atom 2.1.13** — Transitions, transforms, keyframe animations. Which properties are GPU-cheap (`transform`/`opacity`) and why.
- **Atom 2.1.14** — Pseudo-classes and pseudo-elements; `:has()`, `:is()`, `:where()`.
- **Atom 2.1.15** — Overflow, scroll containers, `aspect-ratio`, `object-fit`.
- **Atom 2.1.16** — Accessibility basics: semantic HTML, focus states, contrast, `aria-*` where semantics fall short, keyboard navigation.

### Unit 2.2 — SCSS

*Why: SCSS exists to solve CSS-at-scale problems — repetition, no variables (historically), no composition, one giant file.*

- **Atom 2.2.1** — Why a preprocessor; the compile step; SCSS vs Sass syntax.
- **Atom 2.2.2** — Variables, and when to prefer a CSS custom property instead (runtime vs compile time).
- **Atom 2.2.3** — Nesting, the `&` parent selector, and the discipline of never nesting past 3 levels.
- **Atom 2.2.4** — Partials and `@use` / `@forward` (and why `@import` is deprecated). Namespacing.
- **Atom 2.2.5** — Mixins with `@include`, arguments, defaults, `@content` blocks.
- **Atom 2.2.6** — Functions vs mixins — the real difference. Built-in modules: `math`, `color`, `map`, `string`.
- **Atom 2.2.7** — `@extend` and placeholder selectors — and why `@extend` is usually a trap.
- **Atom 2.2.8** — Maps: design tokens, theme objects, `map.get`.
- **Atom 2.2.9** — Control flow: `@if`, `@each`, `@for`. Generating utility classes.
- **Atom 2.2.10** — Architecture: 7-1 pattern, BEM naming, component-scoped styles, and where CSS Modules / Tailwind fit as alternatives.

### 📦 MODULE 2 PROOF OF LEARNING

Rebuild a real product page (pick a site you like) pixel-close, responsive from 320px to 1920px, using a SCSS token system, dark mode via custom properties, and zero layout hacks. No CSS framework.

---

# MODULE 3 — C# and Object-Oriented Programming

> **Why this exists.** C# is your primary language — depth here compounds into ASP.NET Core, DSA, LLD and concurrency. Most candidates know C# syntax but not the runtime: value vs reference semantics, boxing, closures over loop variables, `IEnumerable` deferred execution, and what `async` actually compiles to. Those are exactly what senior interviewers probe.

### Unit 3.1 — The Type System and Memory

- **Atom 3.1.1** — The CLR, IL, JIT, assemblies, and what "managed code" means.
- **Atom 3.1.2** — Value types vs reference types; stack vs heap (and why "value types live on the stack" is an oversimplification).
- **Atom 3.1.3** — Boxing and unboxing: the hidden allocation, and where it silently hurts performance.
- **Atom 3.1.4** — `struct` vs `class` — the actual decision criteria. `readonly struct`, `ref struct`.
- **Atom 3.1.5** — Nullable value types vs **nullable reference types**; `?`, `!`, and why NRT is a design tool, not a warning to suppress.
- **Atom 3.1.6** — Default values, `default`, and the null-object pattern.
- **Atom 3.1.7** — Equality: `==` vs `Equals` vs `ReferenceEquals`; overriding `Equals` and `GetHashCode` together and why they must agree.
- **Atom 3.1.8** — `string` immutability, interning, `StringBuilder`, `Span<char>`, and why string concat in a loop is a real bug.
- **Atom 3.1.9** — Garbage collection: generations 0/1/2, LOH, roots, when collection happens. Finalizers vs `IDisposable`.
- **Atom 3.1.10** — `IDisposable`, `using` statements and declarations, `IAsyncDisposable`, and the dispose pattern.

### Unit 3.2 — Object-Oriented Programming, Properly

*Why: everyone can recite the four pillars. Very few can justify a design decision. This unit targets the second skill.*

- **Atom 3.2.1** — **Encapsulation**: not "make fields private" but "protect invariants". Access modifiers including `internal` and `protected internal`.
- **Atom 3.2.2** — **Abstraction**: modelling the relevant, hiding the rest. Abstract classes, abstract members.
- **Atom 3.2.3** — **Inheritance**: `base`, constructor chaining, `sealed`. The fragile base class problem.
- **Atom 3.2.4** — **Polymorphism**: `virtual`/`override`/`new`, runtime dispatch, method hiding vs overriding. Compile-time (overloading) vs runtime polymorphism.
- **Atom 3.2.5** — **Interfaces**: contracts, multiple implementation, explicit implementation, default interface methods.
- **Atom 3.2.6** — **Interface vs abstract class** — decide correctly and defend it. ("is-a" vs "can-do", state vs contract.)
- **Atom 3.2.7** — **Composition over inheritance** — refactor an inheritance hierarchy into composition and articulate what improved.
- **Atom 3.2.8** — Coupling and cohesion — measure them in your own code.
- **Atom 3.2.9** — **SOLID part 1**: Single Responsibility and Open/Closed, with a before/after refactor for each.
- **Atom 3.2.10** — **SOLID part 2**: Liskov Substitution (the square/rectangle problem), Interface Segregation, Dependency Inversion.
- **Atom 3.2.11** — Dependency Inversion vs Dependency Injection vs IoC container — three different things people conflate.

### Unit 3.3 — Generics and Collections

- **Atom 3.3.1** — Why generics: type safety plus no boxing. Compare to pre-generics `ArrayList`.
- **Atom 3.3.2** — Generic classes, methods, constraints (`where T : class, new(), IComparable<T>`).
- **Atom 3.3.3** — Covariance and contravariance (`out`/`in`) — why `IEnumerable<Derived>` works where `List<Derived>` doesn't.
- **Atom 3.3.4** — The collection interface hierarchy: `IEnumerable` → `ICollection` → `IList`, plus `IReadOnlyList`. Which to expose from an API.
- **Atom 3.3.5** — `List<T>` internals: backing array, capacity doubling, amortised O(1) add.
- **Atom 3.3.6** — `Dictionary<K,V>` internals: buckets, hashing, collisions, why a mutable key is a bug.
- **Atom 3.3.7** — `HashSet<T>`, `SortedDictionary`, `SortedSet`, `SortedList` — the complexity trade-offs.
- **Atom 3.3.8** — `Queue<T>`, `Stack<T>`, `LinkedList<T>`, `PriorityQueue<TElement,TPriority>`.
- **Atom 3.3.9** — Arrays, multidimensional vs jagged, `Span<T>` and `Memory<T>` for allocation-free slicing.
- **Atom 3.3.10** — Choosing a collection: a decision table you write yourself, by operation complexity.

### Unit 3.4 — Delegates, Lambdas and LINQ

- **Atom 3.4.1** — Delegates as type-safe function pointers; multicast delegates.
- **Atom 3.4.2** — `Func`, `Action`, `Predicate`; lambdas; closures in C# (and the captured-loop-variable gotcha).
- **Atom 3.4.3** — Events: the `event` keyword, publisher/subscriber, why events over raw delegates, and unsubscribing to avoid leaks.
- **Atom 3.4.4** — `IEnumerable<T>`, `IEnumerator<T>`, and `yield return` — write a custom iterator.
- **Atom 3.4.5** — **Deferred (lazy) execution** — the single most misunderstood LINQ behaviour. Multiple enumeration bugs.
- **Atom 3.4.6** — LINQ operators: filtering, projection, ordering, grouping, joining, aggregation, set operations, partitioning.
- **Atom 3.4.7** — Query syntax vs method syntax.
- **Atom 3.4.8** — **`IEnumerable` vs `IQueryable`** — expression trees, and why calling `.ToList()` too early destroys your SQL.
- **Atom 3.4.9** — Expression trees conceptually: code as data, and how EF Core turns your lambda into SQL.
- **Atom 3.4.10** — LINQ performance: allocations, `ToList` vs `ToArray`, when a plain loop is right.

### Unit 3.5 — Modern C# Language Features

- **Atom 3.5.1** — Properties: auto, computed, `init`, expression-bodied, required members.
- **Atom 3.5.2** — `record` and `record struct`: value equality, `with` expressions, when to use over class.
- **Atom 3.5.3** — Pattern matching: type, constant, relational, logical, property, positional, list patterns.
- **Atom 3.5.4** — `switch` expressions and exhaustiveness.
- **Atom 3.5.5** — Tuples and deconstruction.
- **Atom 3.5.6** — Extension methods — how they work, and their limits.
- **Atom 3.5.7** — Indexers, operator overloading, implicit/explicit conversion operators.
- **Atom 3.5.8** — Nested, partial, static and anonymous types.
- **Atom 3.5.9** — Attributes and reflection: reading metadata at runtime, and the performance cost.
- **Atom 3.5.10** — Source generators, conceptually — compile-time code generation and why it's replacing reflection.

### Unit 3.6 — Exceptions and Defensive Code

- **Atom 3.6.1** — Exception hierarchy; `try`/`catch`/`finally` semantics; the cost of throwing.
- **Atom 3.6.2** — `throw` vs `throw ex` — stack trace preservation.
- **Atom 3.6.3** — Custom exceptions; when a custom type earns its keep.
- **Atom 3.6.4** — Exception filters (`when`), `ExceptionDispatchInfo`.
- **Atom 3.6.5** — Exceptions vs result types; when not to use exceptions for control flow.
- **Atom 3.6.6** — Guard clauses, `ArgumentNullException.ThrowIfNull`, fail-fast, validating at boundaries.

### 📦 MODULE 3 PROOF OF LEARNING

Build a **console-based library management system** with no framework: proper domain model, interfaces, DI by hand (no container), file persistence, custom exceptions, LINQ-based queries, and unit tests. Then write a second version that deliberately violates SOLID and document exactly what breaks when requirements change.

---

# MODULE 4 — Engineering Hygiene (the invisible syllabus)

> **Why this exists.** These are never taught in a tier-3 curriculum and are assumed on day one of the job. Not knowing them makes you look junior regardless of your algorithm skills. Budget 2 weeks, then keep using them forever. (The terminal, Docker and cloud live in Module 12 — they need the OS grounding from Module 10 first.)

### Unit 4.1 — Git and Version Control

- **Atom 4.1.1** — The object model: blobs, trees, commits, refs. Git as a DAG, not a folder of versions.
- **Atom 4.1.2** — The three areas: working directory, staging, repository. `add`/`commit`/`status`/`diff`.
- **Atom 4.1.3** — Branching and merging; fast-forward vs three-way merge; resolving conflicts by hand.
- **Atom 4.1.4** — `rebase` vs `merge`; interactive rebase; the golden rule about rewriting public history.
- **Atom 4.1.5** — `reset` (soft/mixed/hard) vs `revert` vs `restore` — know which destroys work.
- **Atom 4.1.6** — `stash`, `cherry-pick`, `reflog` (your undo button), `bisect` (finding the breaking commit).
- **Atom 4.1.7** — Remotes, `fetch` vs `pull`, tracking branches, force-with-lease.
- **Atom 4.1.8** — Workflow: trunk-based vs GitFlow, PR etiquette, atomic commits, conventional commit messages.

### Unit 4.2 — Testing

- **Atom 4.2.1** — Why tests: the real payoff is refactoring confidence, not bug-catching.
- **Atom 4.2.2** — The test pyramid: unit, integration, e2e — cost and value of each.
- **Atom 4.2.3** — Arrange-Act-Assert; one behaviour per test; naming tests as specifications.
- **Atom 4.2.4** — xUnit: facts, theories, fixtures, lifetime.
- **Atom 4.2.5** — Test doubles: dummy, stub, spy, mock, fake. Moq/NSubstitute basics.
- **Atom 4.2.6** — Mocking pitfalls: over-mocking, testing implementation instead of behaviour.
- **Atom 4.2.7** — Testable design: why DI and interfaces exist partly for this.
- **Atom 4.2.8** — Coverage as a signal not a target; mutation testing conceptually.
- **Atom 4.2.9** — TDD: red-green-refactor. Do one full kata this way even if you never adopt it.
- **Atom 4.2.10** — Frontend testing: React Testing Library philosophy (test what the user sees), `userEvent`, MSW for API mocking, Playwright for e2e.

### Unit 4.3 — Code Quality

- **Atom 4.3.1** — Naming: the single highest-leverage readability skill.
- **Atom 4.3.2** — Function size, single level of abstraction, early returns over nesting.
- **Atom 4.3.3** — Comments: when they're a code smell vs when they're essential (the *why*, not the *what*).
- **Atom 4.3.4** — Code smells catalogue: long method, large class, feature envy, primitive obsession, shotgun surgery, data clumps.
- **Atom 4.3.5** — Refactoring moves: extract method, extract class, replace conditional with polymorphism, introduce parameter object.
- **Atom 4.3.6** — Reading code you didn't write — a trainable skill. Clone a mid-size OSS repo and trace one feature end to end.
- **Atom 4.3.7** — Code review: giving and receiving. What to look for beyond style.

---

# MODULE 5 — Data Structures and Algorithms in C#

> **Why this exists.** Two separate reasons, and conflating them is why people study DSA badly. **Reason one:** it is the filter for every product-company interview, and for a tier-3 candidate it is the most meritocratic filter available — nobody can tell where you studied from a clean O(n log n) solution. **Reason two, the one that actually matters long term:** it trains you to reason about cost. Engineers who've internalised complexity analysis instinctively notice the nested loop over a 10,000-item list, the O(n) lookup inside a loop, the accidental quadratic. That instinct is DSA's real product.

**How to run this module:** two focused months, then a maintenance habit. Work through the units in order, since each pattern builds on the last. Target ~350–400 problems total, but *quality over count*. Rules: attempt for 25–30 minutes before looking; after solving, always read two better solutions; re-solve anything you needed a hint for after 7 days; maintain a "patterns learned" file, not a "problems solved" count.

**After this module ends**, drop to 3–4 problems a week for the rest of the plan. Not because you need more coverage, but because pattern recall decays fast and rebuilding it a week before interviews doesn't work. Rotate through your "needed a hint" list rather than grinding new problems.

### Unit 5.1 — Foundations of Analysis

- **Atom 5.1.1** — Why complexity analysis: comparing algorithms independent of machine.
- **Atom 5.1.2** — Big-O, Big-Ω, Big-Θ; worst/average/best case; why we default to worst case.
- **Atom 5.1.3** — Deriving time complexity from loops, nested loops, sequential blocks.
- **Atom 5.1.4** — Space complexity, including recursion stack space (the one people forget).
- **Atom 5.1.5** — Amortised analysis: why `List.Add` is O(1) despite the resize.
- **Atom 5.1.6** — Recurrence relations and the Master Theorem for divide-and-conquer.
- **Atom 5.1.7** — The complexity hierarchy and what's tractable at n = 10, 10³, 10⁶, 10⁹ — how to infer the expected solution from constraints.

### Unit 5.2 — C# for Competitive/Interview Coding

*Why: don't lose an interview to unfamiliarity with your own standard library.*

- **Atom 5.2.1** — Fast I/O; `Console` reading patterns.
- **Atom 5.2.2** — `List<T>`, `Dictionary<K,V>`, `HashSet<T>` — the workhorses, with their exact complexities.
- **Atom 5.2.3** — `SortedDictionary`, `SortedSet`, `PriorityQueue<T,TP>` — the ones that turn hard problems easy.
- **Atom 5.2.4** — `Queue`, `Stack`, `LinkedList`, `Array.Sort` with custom `Comparer`/`Comparison`.
- **Atom 5.2.5** — `StringBuilder`, `string.Split`, `Span<T>` for parsing; char arithmetic.
- **Atom 5.2.6** — `Tuple`/`ValueTuple` as lightweight compound keys and return values.
- **Atom 5.2.7** — LINQ in interviews: when it clarifies vs when it hides complexity.

### Unit 5.3 — Arrays and Strings

- **Atom 5.3.1** — Array traversal patterns; in-place modification; the two-pass idea.
- **Atom 5.3.2** — **Two pointers**: opposite ends (pair sum, container with most water, reverse), and same-direction (remove duplicates, move zeroes).
- **Atom 5.3.3** — **Sliding window, fixed size**: max sum subarray of size k.
- **Atom 5.3.4** — **Sliding window, variable size**: longest substring without repeats, minimum window substring. The expand/contract invariant.
- **Atom 5.3.5** — **Prefix sums** and difference arrays; 2D prefix sums; subarray sum equals k (prefix + hashmap).
- **Atom 5.3.6** — Kadane's algorithm and the maximum subarray family.
- **Atom 5.3.7** — Matrix problems: spiral, rotate in place, set zeroes, transpose.
- **Atom 5.3.8** — Cyclic sort and the "numbers 1..n" family (find missing, find duplicate).
- **Atom 5.3.9** — String manipulation: palindromes, anagrams, frequency maps, expand-around-centre.
- **Atom 5.3.10** — String matching: naive, and KMP with the LPS array (understand it once).

### Unit 5.4 — Hashing

- **Atom 5.4.1** — Hash function properties, collisions, chaining vs open addressing, load factor.
- **Atom 5.4.2** — Trading space for time — the core hashing insight. Two Sum as the canonical example.
- **Atom 5.4.3** — Frequency counting, grouping (anagrams), and hashing a canonical form.
- **Atom 5.4.4** — Hashing for O(1) membership: longest consecutive sequence.
- **Atom 5.4.5** — Designing composite keys; custom `GetHashCode` for tuples/structs.

### Unit 5.5 — Sorting and Searching

- **Atom 5.5.1** — Bubble/selection/insertion — implement once, understand stability and adaptivity.
- **Atom 5.5.2** — Merge sort: divide and conquer, stability, external sorting, counting inversions.
- **Atom 5.5.3** — Quick sort: partition schemes, pivot choice, worst case, Quickselect for k-th largest.
- **Atom 5.5.4** — Heap sort; counting sort, radix sort, bucket sort and their non-comparison constraints.
- **Atom 5.5.5** — Why comparison sorts are Ω(n log n).
- **Atom 5.5.6** — **Binary search**: the exact loop invariant, `low + (high-low)/2`, and writing it bug-free every time.
- **Atom 5.5.7** — Binary search variants: first/last occurrence, lower/upper bound, search in rotated array, find peak.
- **Atom 5.5.8** — **Binary search on the answer** — the pattern that unlocks a whole class of "minimise the maximum" problems (Koko eating bananas, split array, ship packages).
- **Atom 5.5.9** — Sorting as a preprocessing step: intervals, meeting rooms, custom comparators.

### Unit 5.6 — Recursion and Backtracking

- **Atom 5.6.1** — The recursion mental model: base case, recursive case, trusting the recursion. Draw the recursion tree.
- **Atom 5.6.2** — The call stack during recursion; converting recursion to iteration; tail recursion.
- **Atom 5.6.3** — Subsets/power set — both the include/exclude tree and the bitmask method.
- **Atom 5.6.4** — Permutations, combinations, combination sum; handling duplicates.
- **Atom 5.6.5** — **The backtracking template**: choose → explore → un-choose. N-Queens, Sudoku, rat in a maze.
- **Atom 5.6.6** — Pruning: how to recognise and cut dead branches.
- **Atom 5.6.7** — Word search / grid backtracking with visited state.

### Unit 5.7 — Linked Lists

- **Atom 5.7.1** — Singly, doubly, circular; array vs linked list trade-offs (cache locality is the real answer).
- **Atom 5.7.2** — Traversal, insertion, deletion; the dummy-head trick that removes half your edge cases.
- **Atom 5.7.3** — Reversal: iterative and recursive; reverse in k-groups.
- **Atom 5.7.4** — **Fast and slow pointers**: middle node, cycle detection (Floyd's), cycle start, palindrome check.
- **Atom 5.7.5** — Merging sorted lists; merge k lists with a heap.
- **Atom 5.7.6** — Copy list with random pointer; flatten a multilevel list.
- **Atom 5.7.7** — **LRU cache** with hashmap + doubly linked list — do this one until it's automatic.

### Unit 5.8 — Stacks and Queues

- **Atom 5.8.1** — Stack ADT, LIFO, applications: undo, call stack, expression evaluation.
- **Atom 5.8.2** — Balanced parentheses; infix/postfix/prefix conversion and evaluation.
- **Atom 5.8.3** — **Monotonic stack**: next greater element, daily temperatures, largest rectangle in histogram, trapping rain water.
- **Atom 5.8.4** — Min stack in O(1); stack using queues and vice versa.
- **Atom 5.8.5** — Queue ADT, circular queue, deque.
- **Atom 5.8.6** — **Monotonic deque**: sliding window maximum.

### Unit 5.9 — Trees

- **Atom 5.9.1** — Terminology: height, depth, balanced, complete, full, perfect. Binary tree representation.
- **Atom 5.9.2** — DFS traversals: preorder, inorder, postorder — recursive and iterative. What each is *for*.
- **Atom 5.9.3** — BFS / level-order with a queue; level-by-level processing; zigzag; right side view.
- **Atom 5.9.4** — Height, diameter, balanced check, and the "return multiple values up the recursion" pattern.
- **Atom 5.9.5** — **Lowest common ancestor** — in a binary tree and in a BST.
- **Atom 5.9.6** — Path problems: root-to-leaf sums, max path sum, all paths.
- **Atom 5.9.7** — Tree construction from traversals; serialise and deserialise.
- **Atom 5.9.8** — **BST**: the invariant, search/insert/delete, why inorder gives sorted output, validating a BST.
- **Atom 5.9.9** — BST degradation to O(n) and why self-balancing exists: AVL rotations and Red-Black trees *conceptually* (you must know why, not implement).
- **Atom 5.9.10** — **Tries**: insert, search, prefix search, autocomplete, word dictionary with wildcards.
- **Atom 5.9.11** — Segment trees and Fenwick trees — range query + point update. Know when they apply.

### Unit 5.10 — Heaps and Priority Queues

- **Atom 5.10.1** — The heap property; array representation; sift up/down; build-heap in O(n).
- **Atom 5.10.2** — Implement a min-heap from scratch, then use C#'s `PriorityQueue`.
- **Atom 5.10.3** — **Top-K pattern**: k largest, k closest, top k frequent — and why a size-k heap beats sorting.
- **Atom 5.10.4** — **Two-heap pattern**: median from a data stream.
- **Atom 5.10.5** — K-way merge; task scheduler; meeting rooms II.

### Unit 5.11 — Graphs

*Why: graphs are the highest-frequency "hard" topic and the one most people skip. They're also everywhere in real systems — dependency resolution, routing, social features, deadlock detection.*

- **Atom 5.11.1** — Representations: adjacency list vs matrix vs edge list; directed/undirected; weighted; density trade-offs.
- **Atom 5.11.2** — **DFS** on graphs: recursive and iterative, visited sets, connected components.
- **Atom 5.11.3** — **BFS** on graphs: shortest path in unweighted graphs, level tracking.
- **Atom 5.11.4** — Grid-as-graph: number of islands, flood fill, rotting oranges, shortest path in a maze.
- **Atom 5.11.5** — **Multi-source BFS** — the trick that turns hard problems easy.
- **Atom 5.11.6** — Cycle detection: undirected (parent tracking) vs directed (recursion stack / colours).
- **Atom 5.11.7** — **Topological sort**: Kahn's algorithm and DFS-based. Course schedule. Real use: build systems, task dependencies.
- **Atom 5.11.8** — **Union-Find (DSU)**: union by rank, path compression, near-O(1). Connected components, redundant connection, accounts merge.
- **Atom 5.11.9** — **Dijkstra's**: with a priority queue, why it fails on negative weights.
- **Atom 5.11.10** — Bellman-Ford and Floyd-Warshall — when each is the right tool.
- **Atom 5.11.11** — Minimum spanning tree: Kruskal (with DSU) and Prim.
- **Atom 5.11.12** — Bipartite check / graph colouring; 0-1 BFS.

### Unit 5.12 — Dynamic Programming

*Why: DP is where most candidates stall. It isn't a bag of tricks; it's a single idea — overlapping subproblems + optimal substructure — applied through a repeatable process.*

- **Atom 5.12.1** — The DP recognition test: is there a choice at each step, and do subproblems repeat?
- **Atom 5.12.2** — The process: brute-force recursion → memoise → tabulate → space-optimise. Do this on Fibonacci once, fully.
- **Atom 5.12.3** — Defining state: what parameters uniquely identify a subproblem. This is the whole skill.
- **Atom 5.12.4** — **1D DP**: climbing stairs, house robber, min cost climbing, decode ways.
- **Atom 5.12.5** — **0/1 Knapsack** and its family: subset sum, equal partition, target sum, count subsets.
- **Atom 5.12.6** — **Unbounded knapsack**: coin change (min coins and count ways), rod cutting.
- **Atom 5.12.7** — **Grid DP**: unique paths, min path sum, with obstacles.
- **Atom 5.12.8** — **String DP**: longest common subsequence, edit distance, longest palindromic subsequence/substring, wildcard and regex matching.
- **Atom 5.12.9** — **Longest increasing subsequence**: O(n²) DP and the O(n log n) patience/binary-search version.
- **Atom 5.12.10** — DP on stocks: the full ladder (1 transaction → k transactions → cooldown → fee).
- **Atom 5.12.11** — Partition DP / MCM: matrix chain multiplication, burst balloons, palindrome partitioning.
- **Atom 5.12.12** — DP on trees; DP with bitmask (travelling salesman as the example).
- **Atom 5.12.13** — Reconstructing the solution, not just the optimal value.

### Unit 5.13 — Greedy, Intervals and Bit Manipulation

- **Atom 5.13.1** — Greedy: the exchange argument; how to *prove* greedy works, and recognising when it doesn't (and DP is needed).
- **Atom 5.13.2** — Classic greedy: activity selection, fractional knapsack, jump game, gas station, candy distribution.
- **Atom 5.13.3** — Interval problems: merge, insert, non-overlapping, meeting rooms — sorting by start vs end.
- **Atom 5.13.4** — Bit basics: AND, OR, XOR, NOT, shifts. Two's complement.
- **Atom 5.13.5** — Bit tricks: check/set/clear/toggle the i-th bit, `n & (n-1)`, count set bits, power of two.
- **Atom 5.13.6** — XOR properties: single number, missing number, two single numbers.
- **Atom 5.13.7** — Bitmasks for subsets and state compression.

### 📦 MODULE 5 PROOF OF LEARNING

Maintain a public repo: every solution in C#, with a comment header stating the pattern, the complexity, and the key insight in one sentence. Additionally implement from scratch, no library: dynamic array, linked list, hash map, min-heap, BST, trie, graph with BFS/DFS/Dijkstra, and LRU cache.

---

## PART 2 — BUILDING REAL SOFTWARE

---

# MODULE 6 — React

> **Why this exists.** React's value proposition is one idea: *UI as a function of state*. Manual DOM manipulation forces you to describe transitions ("when this changes, update those five elements"), which grows quadratically in complexity and is where bugs live. React lets you describe destinations instead. Every React feature — reconciliation, hooks, keys, memoisation — is a consequence of making that idea fast enough to be practical. Learn it in that order and React stops being magic.

### Unit 6.1 — The Mental Model

- **Atom 6.1.1** — The problem React solves: imperative DOM updates vs declarative rendering. Build a small counter in vanilla JS and in React; compare what you had to think about.
- **Atom 6.1.2** — Components as functions of props → UI. Composition over configuration.
- **Atom 6.1.3** — JSX: what it compiles to (`React.createElement`), expressions vs statements, conditional and list rendering.
- **Atom 6.1.4** — The **element tree vs the DOM**; what "virtual DOM" actually means and the common misconception that it's "faster than the DOM".
- **Atom 6.1.5** — **Render vs commit** — the two phases. Rendering does not mean touching the DOM.
- **Atom 6.1.6** — Reconciliation: how React diffs, the element-type heuristic, and **why `key` matters** (use index as key, break it, watch state attach to the wrong row).
- **Atom 6.1.7** — Purity of render; why side effects in render are forbidden; what StrictMode's double render is testing.

### Unit 6.2 — State

- **Atom 6.2.1** — `useState`: what a "hook" is, why hooks are called unconditionally at the top level, and how React tracks them by call order.
- **Atom 6.2.2** — State is a snapshot. Why `setCount(count+1)` three times adds one, and the updater form that fixes it.
- **Atom 6.2.3** — Batching, `flushSync`, and automatic batching in React 18+.
- **Atom 6.2.4** — **Immutability**: why mutating state doesn't re-render; updating nested objects and arrays correctly.
- **Atom 6.2.5** — Choosing state structure: avoid redundant state, avoid duplicated state, group related state, keep it flat.
- **Atom 6.2.6** — **Derived state** — compute during render instead of storing. The single most common React mistake.
- **Atom 6.2.7** — Lifting state up; the single source of truth.
- **Atom 6.2.8** — Controlled vs uncontrolled components; when to reset state with a `key`.
- **Atom 6.2.9** — `useReducer`: when state transitions get complex; reducer as a pure function; action design.

### Unit 6.3 — Effects and the Outside World

*Why: `useEffect` is the most overused hook in existence. This unit is as much about not using it as using it.*

- **Atom 6.3.1** — What an effect is *for*: synchronising with external systems (network, DOM APIs, subscriptions, timers).
- **Atom 6.3.2** — **When you don't need an effect**: transforming data for rendering, handling user events, resetting state on prop change.
- **Atom 6.3.3** — The dependency array: how React compares deps (`Object.is`), why object/function deps re-run every render.
- **Atom 6.3.4** — **Cleanup functions**: subscriptions, timers, aborting fetches. Why StrictMode runs setup→cleanup→setup in dev.
- **Atom 6.3.5** — The effect lifecycle framed as "synchronise and desynchronise", not "mount and unmount".
- **Atom 6.3.6** — Stale closures in effects and callbacks — the top React bug once you're past beginner.
- **Atom 6.3.7** — `useLayoutEffect` vs `useEffect` — timing relative to paint, and the rare cases it's needed.
- **Atom 6.3.8** — Race conditions in data fetching, and the `ignore` flag / `AbortController` fixes.

### Unit 6.4 — Refs, Context and Escape Hatches

- **Atom 6.4.1** — `useRef` for mutable values that don't trigger re-render; refs vs state.
- **Atom 6.4.2** — DOM refs: focus, scroll, measure, integrating a non-React library.
- **Atom 6.4.3** — Forwarding refs and the ref-as-prop change in React 19; `useImperativeHandle`.
- **Atom 6.4.4** — Prop drilling: when it's fine and when it isn't.
- **Atom 6.4.5** — **Context**: creating, providing, consuming; the re-render cost; splitting contexts by update frequency.
- **Atom 6.4.6** — Context + reducer as a lightweight state management combo.
- **Atom 6.4.7** — Portals: modals, tooltips, escaping overflow and stacking contexts.
- **Atom 6.4.8** — **Error boundaries**: what they catch and what they don't (events, async, SSR).

### Unit 6.5 — Custom Hooks

- **Atom 6.5.1** — Extracting stateful logic; the naming convention and why it's more than convention (linting, rules of hooks).
- **Atom 6.5.2** — The Rules of Hooks and the reason behind them (call-order indexing).
- **Atom 6.5.3** — Build a personal hook library: `useDebounce`, `useLocalStorage`, `useFetch`, `usePrevious`, `useOnClickOutside`, `useMediaQuery`, `useIntersectionObserver`, `useToggle`.
- **Atom 6.5.4** — Hooks that return stable references; when to `useCallback` inside a hook.

### Unit 6.6 — Performance

- **Atom 6.6.1** — Measure first: React DevTools Profiler, flame graphs, "why did this render".
- **Atom 6.6.2** — Why re-renders happen, and why a re-render is usually *not* the problem.
- **Atom 6.6.3** — `React.memo`, and why it fails when you pass inline objects/functions.
- **Atom 6.6.4** — `useMemo` and `useCallback`: what they cost, when they pay off, and why applying them everywhere makes things slower.
- **Atom 6.6.5** — Moving state down / lifting content up — structural fixes that beat memoisation.
- **Atom 6.6.6** — **List virtualisation** for large lists; the concept, then a library.
- **Atom 6.6.7** — Code splitting: `React.lazy`, `Suspense`, route-level splitting, bundle analysis.
- **Atom 6.6.8** — Concurrent features: `useTransition`, `useDeferredValue`, and the problem they solve (keeping input responsive during expensive renders).
- **Atom 6.6.9** — Core Web Vitals: LCP, CLS, INP — what they measure and the common fixes.
- **Atom 6.6.10** — The React Compiler, conceptually — what automatic memoisation changes.

### Unit 6.7 — Forms, Data and Routing

- **Atom 6.7.1** — Controlled inputs, multi-field forms, validation timing (blur vs submit vs change).
- **Atom 6.7.2** — React Hook Form: uncontrolled-by-default philosophy and why it's fast. Schema validation with Zod.
- **Atom 6.7.3** — Data fetching states: loading, error, empty, success — the four states every UI must handle.
- **Atom 6.7.4** — Why server state ≠ client state: caching, staleness, refetching, deduplication.
- **Atom 6.7.5** — TanStack Query: queries, mutations, cache keys, invalidation, optimistic updates.
- **Atom 6.7.6** — Routing: routes, nested routes, params, query strings, programmatic navigation, protected routes, lazy routes.
- **Atom 6.7.7** — Client-side state managers compared: Context, Zustand, Redux Toolkit — the actual decision criteria.
- **Atom 6.7.8** — Redux fundamentals since you'll meet it: store, actions, reducers, immutability, middleware, RTK Query. Understand the flow even if you don't choose it.

### Unit 6.8 — Rendering Strategies and Beyond

- **Atom 6.8.1** — CSR vs SSR vs SSG vs ISR — the trade-offs in TTFB, SEO, and complexity.
- **Atom 6.8.2** — Hydration, and what a hydration mismatch is.
- **Atom 6.8.3** — React Server Components conceptually: what runs where, the client boundary.
- **Atom 6.8.4** — Next.js App Router at an orientation level: file-based routing, server actions, data fetching.
- **Atom 6.8.5** — Component patterns: compound components, render props, HOCs, headless components. Recognise them in libraries you use.
- **Atom 6.8.6** — Styling in React: CSS Modules, SCSS modules, CSS-in-JS, Tailwind — trade-offs.
- **Atom 6.8.7** — Accessibility in React: labels, roles, focus management in modals, announcing dynamic content.

### 📦 MODULE 6 PROOF OF LEARNING

Build a **non-trivial React + TypeScript app** — e.g. an expense tracker or issue tracker with auth, filtering, sorting, pagination, optimistic updates, offline-tolerant caching, dark mode, and full keyboard accessibility. Then write a post explaining three performance problems you found with the Profiler and how you fixed them.

---

# MODULE 7 — Machine Coding

> **Why this exists.** This is a distinct interview round from DSA and from system design, and it's the one that most closely resembles the job. You get 60–120 minutes to build a working, extensible feature. It is graded on: working software first, clean component decomposition, sensible state modelling, edge-case handling, and whether your code could absorb a new requirement without a rewrite. Most people fail it not from lack of knowledge but from lack of *process* — they start coding before they've modelled the state.

### Unit 7.1 — The Process

- **Atom 7.1.1** — Requirement clarification: ask about scale, persistence, edge cases, and what's explicitly out of scope. Write the list down and confirm it.
- **Atom 7.1.2** — Prioritisation: agree on core vs bonus features *before* coding. Never start with the hard bonus.
- **Atom 7.1.3** — **State modelling first**: what is the minimum state, where does it live, what is derived? Sketch it before writing JSX.
- **Atom 7.1.4** — Component decomposition: identify boundaries by responsibility and by what re-renders together.
- **Atom 7.1.5** — Folder and file structure that signals seniority; separating logic (hooks) from presentation.
- **Atom 7.1.6** — Working software at every checkpoint — commit-sized increments, never a half-broken app at time-up.
- **Atom 7.1.7** — Edge cases as a checklist: empty, loading, error, single item, very many items, long text, rapid clicks, unmount mid-request.
- **Atom 7.1.8** — Narrating your reasoning while coding; how to handle being stuck out loud.
- **Atom 7.1.9** — The last 10 minutes: cleanup, a short README, and stating what you'd do with more time.

### Unit 7.2 — Core Problem Set (build each in under 90 minutes)

*Group A — state and events:* counter with custom step, todo list with filters and persistence, star rating with hover states, accordion (single and multi-open), tabs with lazy content, toggle/switch, progress bar, stepper form wizard.

*Group B — async and performance:* **typeahead/autocomplete** with debounce, caching, keyboard navigation and request cancellation; **infinite scroll** with `IntersectionObserver`; pagination with page-size control; polling with backoff; file upload with progress.

*Group C — composition and recursion:* **nested comments** with reply/collapse; **file explorer tree** with expand/collapse and add/delete; multi-level dropdown menu; JSON viewer.

*Group D — UI systems:* **toast/notification system** with a queue, auto-dismiss and imperative API; modal system with focus trap and portals; **carousel** with autoplay and touch; tooltip with positioning; virtualised list built by hand.

*Group E — interaction-heavy:* **drag-and-drop kanban board**; sortable list; calendar/date picker; **OTP input** with paste and auto-advance; image gallery with lightbox.

*Group F — logic puzzles as UI:* tic-tac-toe with win detection and undo; snake; connect four; memory match; **Excel-like grid** with formula cells; whack-a-mole; typing speed test; poll widget with live results.

### Unit 7.3 — Backend Machine Coding (C#)

*Why: many .NET roles run this round as an API or console problem instead of a UI one.*

- **Atom 7.3.1** — In-memory **rate limiter** (fixed window, sliding window, token bucket) with an extensible strategy.
- **Atom 7.3.2** — **LRU / LFU cache** with generics, TTL and thread safety.
- **Atom 7.3.3** — A **logging framework**: levels, multiple sinks, async writes, configuration.
- **Atom 7.3.4** — **Task scheduler** with priorities, retries and cancellation.
- **Atom 7.3.5** — Simple in-memory key-value store with expiry and a command interface.
- **Atom 7.3.6** — CSV/JSON parser or a small expression evaluator.
- **Atom 7.3.7** — CRUD API with validation, pagination, filtering, and proper status codes — under time pressure.

### 📦 MODULE 7 PROOF OF LEARNING

25 problems, each timed, each in its own repo folder with a README stating the requirements you assumed, your state model, and what you'd extend. Re-do your five worst after a month.

---

# MODULE 8 — ASP.NET Core

> **Why this exists.** This is where your employability concentrates. The framework is not the point — the point is understanding the shape of a web request: what happens between a byte arriving on a socket and a JSON response leaving. Developers who only know "put `[HttpGet]` on a method" cannot debug a DI lifetime bug, a middleware ordering issue, or a connection-pool exhaustion, which are the actual production incidents.

### Unit 8.1 — Foundations and the Request Pipeline

- **Atom 8.1.1** — What a web framework does; .NET hosting model; Kestrel and reverse proxies (why nginx/IIS sits in front).
- **Atom 8.1.2** — `Program.cs`: the builder, service registration, the app pipeline, and the two distinct phases.
- **Atom 8.1.3** — The `HttpContext`: request, response, features, items, and its per-request lifetime.
- **Atom 8.1.4** — **Middleware**: the pipeline as nested delegates. `Use`, `Run`, `Map`. Write one from scratch.
- **Atom 8.1.5** — **Middleware ordering** — why auth-before-authz, why exception handling goes first, why static files go early. Break the order deliberately and observe.
- **Atom 8.1.6** — Minimal APIs vs MVC controllers — when each is appropriate.
- **Atom 8.1.7** — Endpoint routing: route templates, constraints, parameters, route groups.
- **Atom 8.1.8** — The full request lifecycle, drawn on one page from socket to response.

### Unit 8.2 — Dependency Injection and Configuration

- **Atom 8.2.1** — Why DI: testability, swappability, and inverting the dependency direction. Manual DI vs a container.
- **Atom 8.2.2** — **Service lifetimes**: singleton, scoped, transient — and what "scope" means in a web request.
- **Atom 8.2.3** — **Captive dependency** — injecting a scoped service into a singleton, why it's a bug, and how to detect it.
- **Atom 8.2.4** — Registering implementations, multiple implementations, factory registration, keyed services.
- **Atom 8.2.5** — `IServiceScopeFactory` for background work.
- **Atom 8.2.6** — Configuration providers and precedence: appsettings, environment-specific files, environment variables, command line, user secrets, Key Vault.
- **Atom 8.2.7** — The **options pattern**: `IOptions`, `IOptionsSnapshot`, `IOptionsMonitor` — the difference and when each matters.
- **Atom 8.2.8** — Environments, feature flags, and never committing secrets.

### Unit 8.3 — Building APIs

- **Atom 8.3.1** — REST properly: resources, nouns not verbs, correct verb semantics, idempotency, statelessness. Richardson maturity model.
- **Atom 8.3.2** — Status codes that actually mean something: 200/201/204/400/401/403/404/409/422/429/500.
- **Atom 8.3.3** — Model binding: from route, query, body, header, form. Custom binders.
- **Atom 8.3.4** — Validation: data annotations, FluentValidation, validating at the boundary, returning consistent error shapes.
- **Atom 8.3.5** — DTOs vs domain entities — why you never expose your EF entity directly. Mapping (manual vs AutoMapper vs Mapperly).
- **Atom 8.3.6** — Filters: action, result, exception, authorisation — and filters vs middleware.
- **Atom 8.3.7** — **Global exception handling** and `ProblemDetails` (RFC 7807). Never leak stack traces.
- **Atom 8.3.8** — API versioning strategies: URL, header, query. Deprecation.
- **Atom 8.3.9** — Pagination, filtering, sorting and searching as a reusable query contract.
- **Atom 8.3.10** — OpenAPI/Swagger; documenting responses; generating clients.
- **Atom 8.3.11** — Content negotiation, JSON serialisation options, `System.Text.Json` behaviour, custom converters.
- **Atom 8.3.12** — CORS configuration on the server side (now connect it to Atom 1.8.7).
- **Atom 8.3.13** — File upload/download, streaming large responses, `IAsyncEnumerable` endpoints.

### Unit 8.4 — Entity Framework Core and Data Access

*Why: the ORM is where most .NET performance disasters originate, because it's easy to write code that looks fine and generates catastrophic SQL.*

- **Atom 8.4.1** — What an ORM does and its costs; EF Core vs Dapper vs raw ADO.NET, and when each is right.
- **Atom 8.4.2** — `DbContext`: unit of work + repository, its scoped lifetime, and why it's not thread-safe.
- **Atom 8.4.3** — Modelling: conventions, data annotations, Fluent API; one-to-many, many-to-many, one-to-one; owned types.
- **Atom 8.4.4** — **Migrations**: creating, applying, reverting, and the discipline of reviewing generated SQL. Migrations in a team and in production.
- **Atom 8.4.5** — **Change tracking**: how EF knows what changed, `AsNoTracking` and when to use it, identity resolution.
- **Atom 8.4.6** — Loading strategies: eager (`Include`), explicit, lazy — and why lazy loading is usually a trap.
- **Atom 8.4.7** — **The N+1 problem** — reproduce it, see it in the SQL log, fix it. Non-negotiable.
- **Atom 8.4.8** — `IQueryable` composition, client vs server evaluation, and what forces a query to execute.
- **Atom 8.4.9** — Projections to DTOs with `Select` — the biggest easy performance win.
- **Atom 8.4.10** — Split queries, compiled queries, batching, bulk operations (`ExecuteUpdate`/`ExecuteDelete`).
- **Atom 8.4.11** — Transactions and `SaveChanges` semantics; ambient transactions across contexts.
- **Atom 8.4.12** — **Concurrency**: optimistic (`RowVersion`) vs pessimistic; handling `DbUpdateConcurrencyException`.
- **Atom 8.4.13** — Raw SQL, stored procedures, and parameterisation (this is also SQL injection prevention).
- **Atom 8.4.14** — Connection pooling and resiliency: retry on transient failure, timeouts, pool exhaustion symptoms.
- **Atom 8.4.15** — Repository and specification patterns — the arguments for and against layering over EF.

### Unit 8.5 — Authentication and Authorisation

- **Atom 8.5.1** — AuthN vs AuthZ — precise distinction.
- **Atom 8.5.2** — Cookie auth vs token auth; where each fits (server-rendered vs SPA vs mobile).
- **Atom 8.5.3** — **JWT**: structure (header/payload/signature), signing vs encryption, validation steps, expiry. Decode one by hand.
- **Atom 8.5.4** — Refresh tokens, rotation, revocation, and why a JWT can't be "logged out" without extra machinery.
- **Atom 8.5.5** — Where to store tokens in a browser — `HttpOnly` cookie vs localStorage, and the XSS/CSRF trade-off.
- **Atom 8.5.6** — ASP.NET Core Identity: users, roles, password hashing, lockout, email confirmation, 2FA.
- **Atom 8.5.7** — Claims-based authorisation; roles vs claims vs policies; custom requirements and handlers.
- **Atom 8.5.8** — Resource-based authorisation ("can *this* user edit *this* record").
- **Atom 8.5.9** — OAuth 2.0 and OpenID Connect flows; external providers; what an identity provider does.
- **Atom 8.5.10** — API keys, HMAC signing, and machine-to-machine auth.

### Unit 8.6 — Cross-Cutting Concerns

- **Atom 8.6.1** — Logging: `ILogger<T>`, log levels, **structured logging** with Serilog, correlation IDs across requests.
- **Atom 8.6.2** — What to log and what never to log (PII, secrets, tokens).
- **Atom 8.6.3** — Caching: `IMemoryCache`, `IDistributedCache`, Redis, `HybridCache`. Cache-aside pattern. Key design, TTLs, invalidation, stampede protection.
- **Atom 8.6.4** — Response caching, ETags, conditional requests, output caching.
- **Atom 8.6.5** — Background work: `IHostedService`, `BackgroundService`, `PeriodicTimer`, `System.Threading.Channels` for in-process queues.
- **Atom 8.6.6** — When you need a real queue instead (durability, retries, multiple instances) — Hangfire, RabbitMQ, Azure Service Bus.
- **Atom 8.6.7** — `HttpClientFactory`: socket exhaustion, named/typed clients, Polly for retry, timeout, circuit breaker.
- **Atom 8.6.8** — Rate limiting middleware; the built-in limiter algorithms.
- **Atom 8.6.9** — Health checks, readiness vs liveness, and graceful shutdown.
- **Atom 8.6.10** — Observability: metrics, distributed tracing, OpenTelemetry, and the three pillars.
- **Atom 8.6.11** — Real-time: SignalR — hubs, connections, groups, scaling with a backplane. When to use it vs SSE vs polling.

### Unit 8.7 — Architecture and Testing

- **Atom 8.7.1** — Layered architecture; separation of concerns across API / Application / Domain / Infrastructure.
- **Atom 8.7.2** — Clean/Onion architecture and the dependency rule; when the ceremony is worth it and when it's over-engineering.
- **Atom 8.7.3** — CQRS at the application level; MediatR and the case for and against it.
- **Atom 8.7.4** — Domain modelling basics: entities, value objects, aggregates, invariants. Anemic vs rich domain models.
- **Atom 8.7.5** — Unit testing services with mocked dependencies.
- **Atom 8.7.6** — **Integration testing** with `WebApplicationFactory` and Testcontainers against a real database.
- **Atom 8.7.7** — Deployment: publishing, Docker for .NET, environment configuration, health probes, zero-downtime deploys.
- **Atom 8.7.8** — Performance: async all the way down, avoiding sync-over-async, benchmarking with BenchmarkDotNet, profiling a slow endpoint.

### 📦 MODULE 8 PROOF OF LEARNING

Build and **deploy** a production-shaped API: JWT auth with refresh tokens, role and policy authorisation, EF Core with reviewed migrations, Redis caching, structured logging with correlation IDs, global exception handling, rate limiting, background job processing, health checks, integration tests against Testcontainers, Dockerised, running behind a real domain with HTTPS. Then load-test it and write down where it broke first.

---

# MODULE 9 — Databases

> **Why this exists.** The database is almost always the bottleneck and almost always the source of the outage. It's also the fastest place to look competent or incompetent: a candidate who can explain why a composite index on `(status, created_at)` helps one query and not another is instantly credible. Most tier-3 graduates have written SELECTs but have never seen an execution plan, never chosen an isolation level deliberately, and never designed a schema for anything beyond a college project.

### Unit 9.1 — Relational Modelling

- **Atom 9.1.1** — The relational model: relations, tuples, attributes, domains. Why it won.
- **Atom 9.1.2** — Keys: primary, candidate, composite, foreign, surrogate vs natural. GUID vs int as PK (and the index fragmentation issue).
- **Atom 9.1.3** — ER modelling: entities, relationships, cardinality, converting an ERD to tables.
- **Atom 9.1.4** — **Normalisation**: 1NF, 2NF, 3NF, BCNF — with a genuinely messy table you normalise yourself.
- **Atom 9.1.5** — **Denormalisation** — when duplication is the right answer, and the consistency cost you accept.
- **Atom 9.1.6** — Constraints: NOT NULL, UNIQUE, CHECK, DEFAULT, FK actions (cascade/restrict/set null). Enforcing invariants in the DB vs the app.
- **Atom 9.1.7** — Data types and why they matter: sizing, `varchar` vs `nvarchar`, decimal vs float for money, dates and time zones (store UTC).
- **Atom 9.1.8** — Soft delete, audit columns, temporal/history tables.
- **Atom 9.1.9** — Modelling hierarchies (adjacency list, path enumeration, closure table) and many-to-many with payload.

### Unit 9.2 — SQL

- **Atom 9.2.1** — DDL, DML, DCL, TCL. `SELECT` logical processing order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY) — this explains most SQL confusion.
- **Atom 9.2.2** — Filtering: predicates, `IN`, `BETWEEN`, `LIKE`, and **three-valued logic with NULL**.
- **Atom 9.2.3** — **Joins**: inner, left, right, full, cross, self-join. Draw what each returns. Join vs subquery.
- **Atom 9.2.4** — Aggregation: `GROUP BY`, aggregate functions, `HAVING` vs `WHERE`, `COUNT(*)` vs `COUNT(col)`.
- **Atom 9.2.5** — Subqueries: scalar, correlated, `EXISTS` vs `IN` vs `JOIN` and their performance differences.
- **Atom 9.2.6** — **CTEs** and recursive CTEs (org charts, hierarchies).
- **Atom 9.2.7** — **Window functions**: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`/`LEAD`, running totals, `PARTITION BY`. The tool that replaces a dozen self-joins.
- **Atom 9.2.8** — Set operations: `UNION` vs `UNION ALL`, `INTERSECT`, `EXCEPT`.
- **Atom 9.2.9** — `INSERT`/`UPDATE`/`DELETE`, upserts (`MERGE`), bulk operations, `OUTPUT`.
- **Atom 9.2.10** — Views, indexed/materialised views, stored procedures, functions, triggers — and the case against heavy trigger use.
- **Atom 9.2.11** — Interview SQL: nth highest salary, duplicates, gaps and islands, top-N per group, pivoting.

### Unit 9.3 — Indexing and Performance

*Why: this unit alone will make you visibly better than most SDE-1 candidates.*

- **Atom 9.3.1** — How a table is stored: pages, heaps, row layout.
- **Atom 9.3.2** — **B-tree indexes**: structure, why lookup is O(log n), why they're the default. B-tree vs hash index.
- **Atom 9.3.3** — Clustered vs non-clustered indexes; the physical ordering consequence; one clustered index per table.
- **Atom 9.3.4** — **Composite indexes and column order** — the leftmost-prefix rule. Why `(a,b)` serves a query on `a` but not on `b`.
- **Atom 9.3.5** — **Covering indexes** and included columns; eliminating key lookups.
- **Atom 9.3.6** — Selectivity and cardinality; why an index on a boolean column is usually useless.
- **Atom 9.3.7** — **When indexes hurt**: write amplification, storage, maintenance. Over-indexing is a real problem.
- **Atom 9.3.8** — **Reading an execution plan**: table scan vs index seek vs index scan, nested loop vs hash vs merge join, estimated vs actual rows.
- **Atom 9.3.9** — SARGability — why `WHERE YEAR(date) = 2024` kills your index and how to rewrite it.
- **Atom 9.3.10** — Statistics, parameter sniffing, plan caching.
- **Atom 9.3.11** — Query tuning workflow: find the slow query, read the plan, fix the biggest operator, re-measure.
- **Atom 9.3.12** — Full-text search basics and when you need a real search engine instead.

### Unit 9.4 — Transactions and Concurrency

- **Atom 9.4.1** — **ACID** — define each property with a concrete failure it prevents.
- **Atom 9.4.2** — The concurrency anomalies: dirty read, non-repeatable read, phantom read, lost update. Reproduce each in two SQL sessions.
- **Atom 9.4.3** — **Isolation levels**: read uncommitted, read committed, repeatable read, serializable, snapshot. Which anomaly each prevents and what it costs.
- **Atom 9.4.4** — Locking: shared vs exclusive, row/page/table granularity, lock escalation.
- **Atom 9.4.5** — **Deadlocks**: how they form, deadlock graphs, prevention by consistent lock ordering, retry logic.
- **Atom 9.4.6** — MVCC — how snapshot isolation avoids readers blocking writers.
- **Atom 9.4.7** — Optimistic vs pessimistic concurrency control at the application level.
- **Atom 9.4.8** — Long-running transactions and why they're an outage waiting to happen.

### Unit 9.5 — NoSQL and Polyglot Persistence

- **Atom 9.5.1** — Why NoSQL appeared: the specific relational limitations at scale.
- **Atom 9.5.2** — The four families: key-value, document, wide-column, graph — with a real use case for each.
- **Atom 9.5.3** — Document databases (MongoDB/Cosmos): schema design by access pattern, embedding vs referencing, aggregation pipeline.
- **Atom 9.5.4** — **Redis** in depth: data types (string, hash, list, set, sorted set, stream), TTL, persistence (RDB/AOF), pub/sub, atomic operations, distributed locks and their caveats.
- **Atom 9.5.5** — Wide-column (Cassandra) and the "design the table per query" mindset.
- **Atom 9.5.6** — Graph databases and when relationship traversal beats joins.
- **Atom 9.5.7** — Time-series and search (Elasticsearch) as specialised stores.
- **Atom 9.5.8** — **SQL vs NoSQL decision framework** — answer it with trade-offs, never with "NoSQL is faster".

### Unit 9.6 — Operating a Database

- **Atom 9.6.1** — Replication: leader-follower, sync vs async, replication lag and the read-your-own-writes problem.
- **Atom 9.6.2** — Read replicas and routing reads vs writes.
- **Atom 9.6.3** — **Partitioning and sharding**: horizontal vs vertical, shard key selection, hotspots, cross-shard queries and joins.
- **Atom 9.6.4** — Connection pooling: pool sizing, exhaustion, and why it's often the real cause of "the database is slow".
- **Atom 9.6.5** — Backups, point-in-time recovery, RPO and RTO.
- **Atom 9.6.6** — **Zero-downtime schema migrations**: expand-contract, adding a column safely, backfilling large tables.
- **Atom 9.6.7** — Monitoring: slow query logs, wait stats, connection counts, replication lag.
- **Atom 9.6.8** — Cost of a query at scale: rows examined vs rows returned as a mental metric.

### 📦 MODULE 9 PROOF OF LEARNING

Take a 1-million-row synthetic dataset. Write 10 realistic queries, measure them, add indexes deliberately, and document before/after execution plans and timings for each. Separately, design a schema for a booking system with a real concurrency constraint (no double-booking) and implement it correctly under load.

---

## PART 3 — THE MACHINE UNDERNEATH

*You are studying these **after** building real software on purpose. Learning virtual memory before you've profiled a slow API is memorisation. Learning it after you've watched a process get OOM-killed is comprehension.*

---

# MODULE 10 — Operating Systems

> **Why this exists.** Every performance question you'll ever be asked reduces to an OS concept. Why is your API slow under load? Thread pool starvation. Why did the container die? OOM killer. Why does async help at all? Because blocking a thread parks an expensive OS resource while a socket sits idle. Without OS grounding, `async/await` is a magic word; with it, you can reason about throughput from first principles. This is also the single biggest visible gap between tier-1 and tier-3 candidates in interviews.

### Unit 10.1 — What an OS Is

- **Atom 10.1.1** — The OS as resource manager and abstraction layer; kernel space vs user space.
- **Atom 10.1.2** — **System calls** — the boundary crossing, and why it's expensive.
- **Atom 10.1.3** — Interrupts, traps, and the CPU's privilege rings.
- **Atom 10.1.4** — Monolithic vs microkernel; where Linux and Windows sit.
- **Atom 10.1.5** — Boot sequence at a high level; init/systemd.

### Unit 10.2 — Processes and Threads

- **Atom 10.2.1** — What a process is: address space, PCB, states (new/ready/running/waiting/terminated).
- **Atom 10.2.2** — Process memory layout: text, data, heap, stack. Where your variables actually live.
- **Atom 10.2.3** — **Process vs thread** — the precise distinction (address space sharing). What threads share and what they don't.
- **Atom 10.2.4** — **Context switching**: what gets saved and restored, and why it costs microseconds you can't afford at scale.
- **Atom 10.2.5** — Process creation: `fork`/`exec`, parent-child, zombies and orphans.
- **Atom 10.2.6** — User-level vs kernel-level threads; the M:N model. Where .NET threads sit.
- **Atom 10.2.7** — **Thread pools** — why creating a thread per request doesn't scale, and how .NET's pool grows.

### Unit 10.3 — CPU Scheduling

- **Atom 10.3.1** — Why scheduling exists; the goals in tension (throughput, latency, fairness, starvation avoidance).
- **Atom 10.3.2** — Preemptive vs non-preemptive; the time quantum.
- **Atom 10.3.3** — Algorithms: FCFS, SJF, SRTF, priority, **Round Robin**, multilevel feedback queue. Compute average waiting/turnaround time for each by hand.
- **Atom 10.3.4** — Priority inversion and priority inheritance.
- **Atom 10.3.5** — CPU-bound vs I/O-bound workloads — the classification that drives every concurrency decision you'll make.
- **Atom 10.3.6** — Multicore scheduling, affinity, load balancing across cores.

### Unit 10.4 — Memory Management

- **Atom 10.4.1** — Physical vs logical addresses; the MMU and address translation.
- **Atom 10.4.2** — Contiguous allocation, external and internal fragmentation.
- **Atom 10.4.3** — **Paging**: pages, frames, the page table, multi-level page tables.
- **Atom 10.4.4** — The **TLB** — why it exists, hits vs misses, and its link to cache-friendly code.
- **Atom 10.4.5** — Segmentation and segmented paging.
- **Atom 10.4.6** — **Virtual memory and demand paging** — why every process thinks it owns all the memory.
- **Atom 10.4.7** — Page faults: minor vs major; the cost of a major fault relative to a memory access.
- **Atom 10.4.8** — Page replacement: FIFO, LRU, optimal, clock. Belady's anomaly. *(Note the direct link to Atom 5.7.7 — LRU cache.)*
- **Atom 10.4.9** — **Thrashing**, the working set model, and what it looks like in production monitoring.
- **Atom 10.4.10** — Memory-mapped files; copy-on-write.
- **Atom 10.4.11** — The memory hierarchy: registers → L1/L2/L3 → RAM → disk, with the actual latency numbers. **Cache lines and locality of reference** — why array traversal beats linked-list traversal despite equal Big-O.
- **Atom 10.4.12** — Stack vs heap allocation cost; connect back to C# value/reference types and GC.

### Unit 10.5 — Concurrency Primitives (OS view)

- **Atom 10.5.1** — Race conditions and the **critical section problem**; the three requirements (mutual exclusion, progress, bounded waiting).
- **Atom 10.5.2** — Atomicity, test-and-set, compare-and-swap at the hardware level.
- **Atom 10.5.3** — **Mutex vs semaphore vs binary semaphore** — the real difference (ownership).
- **Atom 10.5.4** — Condition variables and monitors.
- **Atom 10.5.5** — Classic problems: producer-consumer, readers-writers, dining philosophers. Implement each.
- **Atom 10.5.6** — **Deadlock**: the four Coffman conditions; prevention, avoidance (banker's algorithm), detection, recovery.
- **Atom 10.5.7** — Livelock and starvation, and how they differ from deadlock.
- **Atom 10.5.8** — Spinlocks vs blocking locks — when burning CPU is cheaper than a context switch.

### Unit 10.6 — I/O, Files and Linux in Practice

- **Atom 10.6.1** — File systems: inodes, directories, hard vs soft links, journaling.
- **Atom 10.6.2** — Disk I/O: seek time, rotational latency, SSD vs HDD access patterns, sequential vs random I/O.
- **Atom 10.6.3** — Buffering, caching, the page cache, `fsync` and durability.
- **Atom 10.6.4** — **Blocking vs non-blocking I/O; synchronous vs asynchronous I/O.** The four combinations.
- **Atom 10.6.5** — **I/O multiplexing**: `select`, `poll`, `epoll`/`kqueue`/IOCP — the mechanism that makes async servers possible. Trace how this underlies Kestrel and Node.
- **Atom 10.6.6** — The C10K problem and why thread-per-connection died.
- **Atom 10.6.7** — Linux in practice: `ps`, `top`/`htop`, `free`, `df`, `lsof`, `strace`, `dmesg`, `journalctl`. Diagnose a "high CPU" and a "high memory" incident.
- **Atom 10.6.8** — Signals, `SIGTERM` vs `SIGKILL`, and graceful shutdown in a containerised app.
- **Atom 10.6.9** — Containers as OS features: namespaces (PID, network, mount) and cgroups (CPU, memory limits). Why the OOM killer targets your container.

### 📦 MODULE 10 PROOF OF LEARNING

Write a small multi-threaded producer-consumer in C# with a bounded buffer using only `Monitor`. Then: deliberately create a deadlock and diagnose it with a debugger; write a program that thrashes and observe page faults; and benchmark row-major vs column-major 2D array traversal to see cache locality in real numbers.

---

# MODULE 11 — Computer Networks

> **Why this exists.** You are building distributed systems whether you call them that or not — a browser, an API, and a database are three machines talking. Networking is what turns "the API is slow sometimes" into a debuggable question. It also owns the single most common interview question in existence: *what happens when you type a URL into a browser?* That question is a rite of passage precisely because a complete answer touches DNS, TCP, TLS, HTTP, load balancing, and rendering.

### Unit 11.1 — Models and Layering

- **Atom 11.1.1** — Why layering: separation of concerns across a network stack.
- **Atom 11.1.2** — The OSI 7 layers and the TCP/IP 4-layer model; the mapping between them.
- **Atom 11.1.3** — Encapsulation: how a payload gains headers on the way down and sheds them on the way up.
- **Atom 11.1.4** — Where each thing you use lives: HTTP (7), TLS (~6/7), TCP/UDP (4), IP (3), Ethernet (2).

### Unit 11.2 — The Lower Layers

- **Atom 11.2.1** — Physical layer: bandwidth vs latency vs throughput — three things people conflate.
- **Atom 11.2.2** — Data link layer: MAC addresses, frames, switches, ARP.
- **Atom 11.2.3** — **IP addressing**: IPv4 structure, classes, private ranges, IPv6 basics.
- **Atom 11.2.4** — **Subnetting and CIDR** — compute network/broadcast/usable range by hand. You need this for cloud VPCs.
- **Atom 11.2.5** — Routing: routing tables, default gateway, static vs dynamic, hop-by-hop forwarding.
- **Atom 11.2.6** — **NAT** and why your laptop's IP isn't what the server sees.
- **Atom 11.2.7** — ICMP, `ping`, `traceroute` — and how to read their output.

### Unit 11.3 — Transport Layer

- **Atom 11.3.1** — Ports, sockets, and the 4-tuple that identifies a connection.
- **Atom 11.3.2** — **TCP**: connection-oriented, reliable, ordered. The guarantees it makes.
- **Atom 11.3.3** — The **three-way handshake** and the four-way teardown; TIME_WAIT and why it exhausts ports.
- **Atom 11.3.4** — Sequence numbers, ACKs, retransmission, and the retransmission timeout.
- **Atom 11.3.5** — Flow control and the sliding window; the receive buffer.
- **Atom 11.3.6** — Congestion control: slow start, congestion avoidance, fast retransmit. Why a new connection starts slow — and why connection reuse matters so much.
- **Atom 11.3.7** — **UDP**: what you give up and what you gain. When it's correct (DNS, video, gaming, QUIC).
- **Atom 11.3.8** — Head-of-line blocking at the TCP level.
- **Atom 11.3.9** — Socket states; reading `netstat`/`ss` output during an incident.

### Unit 11.4 — Application Layer

- **Atom 11.4.1** — **DNS**: the hierarchy (root → TLD → authoritative), recursive resolution, record types (A, AAAA, CNAME, MX, TXT, NS), TTL and caching. Trace a lookup with `dig`.
- **Atom 11.4.2** — DNS-based load balancing, GeoDNS, and DNS propagation delays.
- **Atom 11.4.3** — **HTTP/1.1**: request/response anatomy, methods and their semantics, safe vs idempotent.
- **Atom 11.4.4** — Status code families and the ones that carry real meaning (301 vs 302, 401 vs 403, 409, 429).
- **Atom 11.4.5** — Headers that matter: `Content-Type`, `Accept`, `Authorization`, `Cache-Control`, `ETag`, `Cookie`, `Origin`, `X-Forwarded-For`.
- **Atom 11.4.6** — Persistent connections, keep-alive, pipelining and its failure.
- **Atom 11.4.7** — **HTTP caching**: `Cache-Control` directives, `ETag`/`If-None-Match`, `Last-Modified`, revalidation, and the difference between browser, CDN and proxy caches.
- **Atom 11.4.8** — **HTTP/2**: binary framing, multiplexing, header compression, server push. Which HTTP/1.1 workarounds it made obsolete.
- **Atom 11.4.9** — **HTTP/3 and QUIC**: UDP-based, why it fixes transport-level head-of-line blocking.
- **Atom 11.4.10** — Cookies and sessions: attributes (`HttpOnly`, `Secure`, `SameSite`, `Domain`, `Path`), and the stateless-protocol problem they solve.
- **Atom 11.4.11** — **CORS from the network view** — the preflight `OPTIONS` request on the wire. Watch one in DevTools.
- **Atom 11.4.12** — Real-time options compared: polling, long polling, **SSE**, **WebSockets** (upgrade handshake, framing), WebRTC. Pick correctly for a given requirement.
- **Atom 11.4.13** — REST vs GraphQL vs gRPC: transport, schema, and trade-offs.

### Unit 11.5 — Network Infrastructure

- **Atom 11.5.1** — Forward proxy vs **reverse proxy**; what nginx actually does in front of your app.
- **Atom 11.5.2** — **Load balancers**: L4 vs L7; algorithms (round robin, least connections, IP hash, weighted); health checks; sticky sessions and why they're a smell.
- **Atom 11.5.3** — **CDNs**: edge caching, origin pull, cache invalidation, and what belongs on a CDN.
- **Atom 11.5.4** — API gateways: routing, auth, rate limiting, aggregation.
- **Atom 11.5.5** — Firewalls, security groups, VPCs, public vs private subnets.
- **Atom 11.5.6** — Debugging tools: browser DevTools network tab in depth, `curl -v`, Postman, Wireshark basics, `tcpdump`.

### 📦 MODULE 11 PROOF OF LEARNING

Write the **complete "what happens when you type a URL"** answer — 2,000+ words, covering DNS resolution with caching layers, TCP handshake, TLS handshake, HTTP request, server processing, response, and browser rendering. Then verify each claim with `dig`, `curl -v`, and Wireshark. This one document is worth a dozen interview answers.

---

# MODULE 12 — The Terminal, Containers and the Cloud

> **Why this exists.** Your code does not run on your laptop. It runs on a Linux box you reach through SSH, inside a container you built, on hardware you rent, reached through a network you configured. Every deployment, every 2am incident, and every "but it works locally" happens in this layer — and it is almost entirely absent from a tier-3 curriculum. It's also the cheapest gap to close: free tiers exist, and a candidate who has personally deployed, monitored and debugged something in the cloud is instantly more credible than one who has only ever pressed F5. This module sits after Operating Systems and Networks deliberately: containers *are* OS features, and cloud networking *is* subnetting. Learn those first and this module becomes obvious rather than magical.

### Unit 12.1 — The Terminal and Linux in Practice

*Why: the shell is the only interface a server has. It's also reproducible and scriptable in a way that clicking never is — a command you can paste into a runbook is worth ten screenshots.*

- **Atom 12.1.1** — Why the shell: reproducibility, scriptability, and remote access. Shell vs terminal vs console — the words people misuse.
- **Atom 12.1.2** — The Linux filesystem hierarchy: `/etc`, `/var`, `/usr`, `/tmp`, `/proc`, `/home`. Where logs, configs and binaries actually live.
- **Atom 12.1.3** — Navigation and file operations: `cd`, `ls -la`, `pwd`, `cp`, `mv`, `rm`, `mkdir`, `ln -s`. Absolute vs relative paths; globbing and wildcards.
- **Atom 12.1.4** — Finding things: `find` with predicates, `locate`, `which`, `tree`.
- **Atom 12.1.5** — Viewing files: `cat`, `less`, `head`, `tail`, and **`tail -f`** on a live log. Survival-level `vim` (open, edit, save, quit — the one that traps people).
- **Atom 12.1.6** — **Streams and redirection**: stdin/stdout/stderr, `>`, `>>`, `2>&1`, `/dev/null`, `tee`. Exit codes, `$?`, `&&` vs `||` vs `;`.
- **Atom 12.1.7** — **Pipes and composition** — the core Unix idea. Chaining small tools into a solution.
- **Atom 12.1.8** — Text processing: `grep` (with regex, `-r`, `-i`, `-v`, `-A/-B`), `cut`, `sort`, `uniq -c`, `wc`, `tr`, `xargs`.
- **Atom 12.1.9** — `sed` for substitution and `awk` for column work — the 20% of each you'll actually use.
- **Atom 12.1.10** — **`jq`** for JSON on the command line — indispensable when working with APIs.
- **Atom 12.1.11** — Permissions: the `rwx` model, numeric vs symbolic `chmod`, `chown`, `sudo`, and why `chmod 777` is never the fix.
- **Atom 12.1.12** — Processes from the shell: `ps aux`, `top`/`htop`, `kill` and signals, `jobs`, `fg`/`bg`, `&`, `nohup`. Managing services with `systemctl` and reading `journalctl`.
- **Atom 12.1.13** — Resource inspection: `df -h`, `du -sh`, `free -h`, `lsof`, `iostat`. Diagnosing "disk full" and "out of memory".
- **Atom 12.1.14** — Networking from the CLI: `curl` (verbose, headers, methods, auth), `wget`, `dig`, `ss`/`netstat`, `nc`, `traceroute`. Prove a connectivity problem rather than guessing.
- **Atom 12.1.15** — Environment: `env`, `export`, `PATH`, shell startup files (`.bashrc`/`.zshrc`), aliases, and why your script "can't find" a command.
- **Atom 12.1.16** — **SSH**: key pairs, `authorized_keys`, `~/.ssh/config`, agent forwarding, `scp`/`rsync`, and local/remote port forwarding (tunnelling to a database behind a firewall).
- **Atom 12.1.17** — **Shell scripting**: shebang, variables and quoting, `if`/`case`, loops, functions, arguments, and `set -euo pipefail` as the default safety line.
- **Atom 12.1.18** — `tmux` (or `screen`) for sessions that survive a dropped connection.
- **Atom 12.1.19** — Package management: `apt`/`yum`, installing the .NET SDK and Node on a fresh box, version managers.
- **Atom 12.1.20** — **The diagnostic drill**: SSH into a box you've never seen and answer — what's running, what's listening, what's eating CPU, what's filling the disk, where are the logs, and when did it last restart? Practise until it's routine.

### Unit 12.2 — Docker and Containers

*Why: containers solved environment drift, which was the single biggest source of deployment failure. But treating Docker as a magic box means you can't debug an image that won't start, and you'll ship 2GB images with secrets baked in.*

- **Atom 12.2.1** — The problem containers solve: dependency hell, environment drift, "works on my machine".
- **Atom 12.2.2** — **Containers vs VMs**: shared kernel vs full guest OS. The startup time and density difference.
- **Atom 12.2.3** — How containers actually work: **namespaces** (PID, network, mount, user) for isolation and **cgroups** for resource limits. *(Direct callback to Atom 10.6.9 — a container is a process with a restricted view, not a small VM.)*
- **Atom 12.2.4** — **Images vs containers**: an image is a template, a container is a running instance. Layers and the union filesystem.
- **Atom 12.2.5** — **The build cache**: how layer caching works, why instruction order determines build speed, and the classic `COPY . .` before `restore` mistake.
- **Atom 12.2.6** — Registries, repositories, tags and digests. Why `:latest` is a liability in production.
- **Atom 12.2.7** — Dockerfile instructions: `FROM`, `RUN`, `COPY` vs `ADD`, `WORKDIR`, `ENV`, `ARG`, `EXPOSE`, `USER`, and **`CMD` vs `ENTRYPOINT`** (the difference people get wrong).
- **Atom 12.2.8** — **Multi-stage builds for .NET**: SDK image to build, runtime image to run. Compare the resulting image sizes yourself.
- **Atom 12.2.9** — Base image choice: full vs slim vs alpine vs **chiselled/distroless**. The trade-off between size, debuggability and attack surface.
- **Atom 12.2.10** — `.dockerignore`, running as a **non-root user**, and keeping the image small on purpose.
- **Atom 12.2.11** — Running containers: `run` (with `-d`, `-p`, `-e`, `-v`), `exec`, `logs`, `ps`, `inspect`, `stop`/`rm`, restart policies.
- **Atom 12.2.12** — **The ephemeral filesystem** — anything written inside a container is gone on restart. Volumes vs bind mounts, and when each is right.
- **Atom 12.2.13** — Container networking: the default bridge, publishing ports, user-defined networks, and container-to-container DNS by service name.
- **Atom 12.2.14** — Configuration and secrets: environment variables, mounted files, and **why secrets must never be baked into an image** (they persist in the layer history even if a later layer deletes them).
- **Atom 12.2.15** — **Docker Compose**: define your whole local stack — API + SQL Server/Postgres + Redis — with `depends_on`, health checks and a shared network. This becomes your standard dev environment.
- **Atom 12.2.16** — Health checks, graceful shutdown, and handling `SIGTERM` properly in a .NET app so deploys don't drop requests.
- **Atom 12.2.17** — Resource limits: memory and CPU constraints, and what the OOM killer does to your container.
- **Atom 12.2.18** — Debugging: a container that exits immediately, a container that can't reach another, an image that's mysteriously huge. Use `logs`, `inspect`, `exec`, and `history`.
- **Atom 12.2.19** — Image security: vulnerability scanning (Trivy/Docker Scout), rebuilding for base image patches, pinning digests, minimising installed packages.
- **Atom 12.2.20** — **Kubernetes vocabulary** (recognition depth only, no deep dive): pod, ReplicaSet, Deployment, Service, Ingress, ConfigMap, Secret, namespace, liveness/readiness probes, resource requests vs limits, HPA. Enough to read a manifest and follow a conversation — that's the SDE-1 bar.

### Unit 12.3 — CI/CD

*Why: shipping is a skill. The gap between "my code works" and "my code is running in production, tested, versioned and rollback-able" is where a lot of juniors stall.*

- **Atom 12.3.1** — Why continuous integration: the integration pain it removes, and fast feedback as the real product.
- **Atom 12.3.2** — Pipeline anatomy: trigger → restore → build → test → scan → package → publish → deploy.
- **Atom 12.3.3** — **GitHub Actions**: workflows, jobs, steps, runners, triggers, matrix builds, dependency caching, secrets and variables. Write one for a .NET API end to end.
- **Atom 12.3.4** — The Azure DevOps Pipelines equivalent, since many .NET shops use it. YAML pipelines, stages, agent pools.
- **Atom 12.3.5** — Build artifacts, versioning, semantic versioning, and tagging container images with the commit SHA rather than `latest`.
- **Atom 12.3.6** — **Quality gates**: unit tests, integration tests, code coverage thresholds, linting/analyzers, dependency vulnerability scanning. Failing the build on purpose.
- **Atom 12.3.7** — Branch protection, required checks, and PR-based workflow.
- **Atom 12.3.8** — Continuous delivery vs continuous deployment; environments, promotion, manual approval gates.
- **Atom 12.3.9** — **Database migrations in a pipeline** — the genuinely hard part. Expand-contract, running migrations as a separate step, and never coupling a migration to a rollback-able deploy.
- **Atom 12.3.10** — Deployment strategies in practice: rolling, blue-green, canary; feature flags to decouple deploy from release; how to actually roll back.
- **Atom 12.3.11** — Secrets in pipelines: repository/environment secrets, and **OIDC federation to the cloud** instead of long-lived credentials.
- **Atom 12.3.12** — Pipeline hygiene: keeping builds fast, flaky test policy, and why a red main branch is an emergency.

### Unit 12.4 — Cloud Fundamentals (provider-agnostic)

*Why: learn the concepts before the console. Every provider has the same primitives under different brand names, and the concepts are what transfer between jobs.*

- **Atom 12.4.1** — What the cloud actually is: rented capacity behind an API. Why elasticity and opex-over-capex changed how software is built.
- **Atom 12.4.2** — Service models: IaaS, CaaS, PaaS, FaaS, SaaS — and the responsibility line moving in each. Pick the right level for a workload.
- **Atom 12.4.3** — **The shared responsibility model** — what the provider secures and what remains unambiguously yours.
- **Atom 12.4.4** — Regions, availability zones, and edge locations. Latency, data residency, and designing for AZ failure.
- **Atom 12.4.5** — **Compute**: VMs vs managed containers vs serverless functions. Cold starts, execution limits, and the real decision criteria.
- **Atom 12.4.6** — **Storage**: object/blob vs block vs file. Storage tiers, lifecycle policies, and what never belongs in a database.
- **Atom 12.4.7** — **Cloud networking**: VPC/VNet, subnets (this is Atom 11.2.4 applied), public vs private subnets, route tables, NAT gateways, security groups/NSGs, private endpoints. Why your database should have no public IP.
- **Atom 12.4.8** — **Identity and access**: IAM roles and policies, least privilege, and **managed identities / instance roles** — the pattern that removes credentials from your app entirely.
- **Atom 12.4.9** — Managed databases: why self-hosting is rarely worth it now. Backups, PITR, failover, read replicas, connection limits.
- **Atom 12.4.10** — Managed cache, queues and event streams as services.
- **Atom 12.4.11** — Secrets management services and rotation *(connects to Atom 13.6.1)*.
- **Atom 12.4.12** — **Observability in the cloud**: centralised logs, metrics, distributed traces, dashboards, and alert rules that page a human only for symptoms users feel.
- **Atom 12.4.13** — DNS, TLS certificate management, CDN and WAF as managed services.
- **Atom 12.4.14** — **Autoscaling**: horizontal scaling rules, scale-to-zero, and why your app must be stateless for any of it to work.
- **Atom 12.4.15** — **The cost model**: pay-per-use, the egress trap, reserved vs spot vs on-demand, tagging for cost attribution, and budget alerts. Cost is a design constraint, not an afterthought.
- **Atom 12.4.16** — The Well-Architected pillars: reliability, security, cost optimisation, operational excellence, performance efficiency — a checklist you can apply to any design.

### Unit 12.5 — Azure in Practice (with the AWS mapping)

*Why: as a .NET developer, Azure is where most of your job market sits — but the concepts are identical elsewhere, so learn one deeply and carry a mapping table for the other. Pick **one** to actually build in; knowing two shallowly is worth less than one properly.*

- **Atom 12.5.1** — The resource model: tenants, subscriptions, resource groups, and Azure Resource Manager. Naming and tagging conventions.
- **Atom 12.5.2** — **App Service**: deploying a .NET API, application settings, deployment slots and slot swapping for zero-downtime releases.
- **Atom 12.5.3** — **Azure Container Apps** (and AKS at a vocabulary level): running your container image with scaling rules and revisions.
- **Atom 12.5.4** — **Azure Functions**: triggers and bindings, consumption vs premium plans, and when serverless genuinely fits.
- **Atom 12.5.5** — **Azure SQL / PostgreSQL Flexible Server**: provisioning, firewall rules, connection strings, DTU/vCore sizing, automated backups.
- **Atom 12.5.6** — **Blob Storage**: containers, access tiers, SAS tokens for time-limited access, static site hosting.
- **Atom 12.5.7** — **Azure Cache for Redis** wired into your API's caching layer.
- **Atom 12.5.8** — Messaging: Storage Queues vs **Service Bus** (topics, subscriptions, dead-letter queues) vs Event Hubs. Choosing correctly.
- **Atom 12.5.9** — **Key Vault + Managed Identity** — the single most valuable pattern in this unit. Zero secrets in configuration, zero credentials in code.
- **Atom 12.5.10** — **Application Insights and Log Analytics**: instrumenting a .NET app, request/dependency/exception telemetry, live metrics, and querying with **KQL**.
- **Atom 12.5.11** — Front Door / Application Gateway / Azure CDN: routing, WAF, TLS termination, custom domains.
- **Atom 12.5.12** — Microsoft Entra ID for app authentication; app registrations, scopes, and connecting it back to Unit 13.4 (OAuth/OIDC).
- **Atom 12.5.13** — Azure Container Registry and pushing images from CI.
- **Atom 12.5.14** — **The AWS mapping table** — build this yourself as a study exercise:

  | Concept | Azure | AWS |
  |---|---|---|
  | Managed app hosting | App Service | Elastic Beanstalk / App Runner |
  | Managed containers | Container Apps / AKS | ECS Fargate / EKS |
  | Serverless functions | Azure Functions | Lambda |
  | Virtual machines | Virtual Machines | EC2 |
  | Object storage | Blob Storage | S3 |
  | Managed relational DB | Azure SQL / PG Flexible | RDS / Aurora |
  | Managed NoSQL | Cosmos DB | DynamoDB |
  | Managed cache | Cache for Redis | ElastiCache |
  | Queue / messaging | Service Bus / Storage Queues | SQS / SNS |
  | Event streaming | Event Hubs | Kinesis |
  | Secrets | Key Vault | Secrets Manager |
  | Identity for workloads | Managed Identity | IAM Roles |
  | Observability | App Insights / Log Analytics | CloudWatch / X-Ray |
  | CDN / edge | Front Door / CDN | CloudFront |
  | DNS | Azure DNS | Route 53 |
  | Private network | VNet | VPC |
  | Container registry | ACR | ECR |
  | IaC (native) | Bicep / ARM | CloudFormation |

### Unit 12.6 — Infrastructure as Code and Operating What You Ship

*Why: clicking through a portal isn't reproducible, reviewable, or recoverable. And building something is only half the job — the other half is running it.*

- **Atom 12.6.1** — Why IaC: reproducibility, peer review, drift detection, disaster recovery. Clicking in a console is an undocumented, unrepeatable change.
- **Atom 12.6.2** — Declarative vs imperative infrastructure. **Terraform** vs **Bicep/ARM** vs Pulumi — and why Bicep is the low-friction start for Azure.
- **Atom 12.6.3** — State files, `plan` vs `apply`, drift, and why state is the thing that will bite you.
- **Atom 12.6.4** — Modules, variables and per-environment parameterisation; dev/staging/prod parity.
- **Atom 12.6.5** — Wiring IaC into the pipeline: plan on PR, apply on merge, with approval gates.
- **Atom 12.6.6** — **Monitoring and alerting**: the RED method for services (rate, errors, duration), dashboards worth looking at, and alerting on user-visible symptoms rather than causes.
- **Atom 12.6.7** — On-call basics: runbooks, escalation, severity levels, and what "the pager went off" actually looks like.
- **Atom 12.6.8** — **Incident response**: detect, mitigate first (roll back beats root-cause under pressure), then investigate. Blameless post-mortems and writing one.
- **Atom 12.6.9** — Cost review as a habit: find the most expensive resource in your own account and justify it or delete it.
- **Atom 12.6.10** — The 12-Factor App — read it once, then audit your own application against all twelve.

### 📦 MODULE 12 PROOF OF LEARNING

**Deploy your Module 8 API to the cloud, properly.** The bar is:

- Containerised with a multi-stage build, non-root user, under 250MB, pushed to a registry
- Running on Container Apps or App Service, with a managed database and managed Redis
- **Zero secrets in configuration** — Key Vault plus managed identity
- Private networking: the database has no public endpoint
- Custom domain with TLS you configured
- Application Insights wired in, with one dashboard and one alert that actually fires
- A GitHub Actions pipeline that builds, tests, scans, and deploys on merge to main, using OIDC rather than a stored credential
- All infrastructure defined in **Bicep or Terraform**, committed to the repo
- A budget alert, and the whole thing running inside free/low tiers

Then: **break it deliberately** — kill the database connection, exhaust memory, deploy a bad build — and practise diagnosing each one from logs and metrics alone, without local access. Write up what you saw and how you found it. That write-up is worth more in an interview than the deployment itself.

---

# MODULE 13 — Security, Certificates and Cryptography

> **Why this exists.** Security is the domain where you cannot invent solutions and where a single mistake is unrecoverable — a leaked credential or an SQL injection is not a bug you patch quietly. It's also a strong seniority signal: an SDE-1 who asks "where is this token stored and what's the blast radius if it leaks?" is immediately treated differently. Practically: you will implement authentication in your first year, and doing it wrong is the default outcome without this module.

### Unit 13.1 — Foundations

- **Atom 13.1.1** — The CIA triad: confidentiality, integrity, availability. Classify any vulnerability into it.
- **Atom 13.1.2** — Threat modelling with STRIDE; attack surface; trust boundaries.
- **Atom 13.1.3** — Core principles: least privilege, defence in depth, fail securely, don't trust the client, secure by default.
- **Atom 13.1.4** — Kerckhoffs's principle — why "security through obscurity" and rolling your own crypto both fail.
- **Atom 13.1.5** — Authentication vs authorisation vs accounting.

### Unit 13.2 — Cryptography

- **Atom 13.2.1** — **Encoding vs hashing vs encryption** — three different things constantly confused. Base64 is not security.
- **Atom 13.2.2** — **Symmetric encryption**: AES, block vs stream ciphers, modes (ECB's famous failure, CBC, **GCM** and authenticated encryption), IVs and nonces.
- **Atom 13.2.3** — The key distribution problem — the exact reason asymmetric crypto exists.
- **Atom 13.2.4** — **Asymmetric encryption**: RSA and ECC, public/private key pairs, encrypt-with-public / decrypt-with-private.
- **Atom 13.2.5** — Why we use both: hybrid encryption (asymmetric to exchange a symmetric key) — the pattern behind TLS.
- **Atom 13.2.6** — **Diffie-Hellman key exchange**; ephemeral DH and **forward secrecy**.
- **Atom 13.2.7** — **Cryptographic hashing**: properties (deterministic, one-way, avalanche, collision-resistant), SHA-256, why MD5 and SHA-1 are dead.
- **Atom 13.2.8** — **Password hashing is different**: bcrypt, scrypt, Argon2, work factors, **salts** (and why per-user), peppers. Why SHA-256 is the wrong tool for passwords.
- **Atom 13.2.9** — HMAC: integrity plus authenticity with a shared secret. Webhook signature verification.
- **Atom 13.2.10** — **Digital signatures**: sign with private, verify with public. Non-repudiation.
- **Atom 13.2.11** — Randomness: CSPRNG vs `Random`; why a predictable token is a vulnerability.
- **Atom 13.2.12** — Encryption at rest vs in transit; envelope encryption; key rotation.

### Unit 13.3 — Certificates, PKI and TLS

- **Atom 13.3.1** — The trust problem: a public key alone proves nothing about identity.
- **Atom 13.3.2** — **X.509 certificates**: subject, issuer, validity, public key, extensions, SAN. Inspect a real one in your browser and with `openssl`.
- **Atom 13.3.3** — **Certificate Authorities and the chain of trust**: root → intermediate → leaf. The OS/browser trust store.
- **Atom 13.3.4** — Self-signed certificates: what they do and don't give you; the local dev story.
- **Atom 13.3.5** — CSRs, issuance, domain validation vs OV vs EV, Let's Encrypt and ACME.
- **Atom 13.3.6** — Revocation: CRL, OCSP, OCSP stapling, short-lived certs.
- **Atom 13.3.7** — **The TLS 1.3 handshake, step by step** — what's exchanged, when the session key is derived, what's encrypted from which point.
- **Atom 13.3.8** — What TLS actually guarantees (and what it doesn't — it says nothing about the server's honesty).
- **Atom 13.3.9** — Cipher suites, TLS versions, and why 1.0/1.1 are disabled.
- **Atom 13.3.10** — Certificate pinning, mTLS (mutual TLS) for service-to-service auth.
- **Atom 13.3.11** — Common failures: expired cert, hostname mismatch, incomplete chain, clock skew. Diagnose each.

### Unit 13.4 — Identity and Access

- **Atom 13.4.1** — Password policy reality: length over complexity, breach lists, no forced rotation.
- **Atom 13.4.2** — MFA: TOTP (how the 6-digit code is derived), WebAuthn/passkeys, SMS and why it's weak.
- **Atom 13.4.3** — **Sessions vs tokens** — the stateful/stateless trade-off, revocation, scaling.
- **Atom 13.4.4** — JWT security specifically: the `alg: none` attack, algorithm confusion, why you validate `iss`/`aud`/`exp`, and why JWTs shouldn't hold secrets (they're signed, not encrypted).
- **Atom 13.4.5** — **OAuth 2.0**: roles, the authorisation code flow **with PKCE**, why implicit flow is deprecated, client credentials, scopes.
- **Atom 13.4.6** — **OpenID Connect**: the identity layer over OAuth, ID tokens, userinfo. OAuth ≠ authentication.
- **Atom 13.4.7** — SSO, SAML, and federated identity at a conceptual level.
- **Atom 13.4.8** — Access control models: RBAC, ABAC, ReBAC. Designing permissions that survive requirement changes.
- **Atom 13.4.9** — Service-to-service auth: API keys, mTLS, workload identity.

### Unit 13.5 — Application Vulnerabilities (OWASP)

*Every atom here: understand it, then exploit it in your own deliberately vulnerable app, then fix it. Reading alone doesn't work for this unit.*

- **Atom 13.5.1** — **Injection**: SQL injection variants (classic, blind, second-order), NoSQL injection, command injection. Parameterised queries as the fix — and why escaping is not.
- **Atom 13.5.2** — **XSS**: stored, reflected, DOM-based. Output encoding by context, `dangerouslySetInnerHTML`, sanitisation libraries.
- **Atom 13.5.3** — **CSRF**: why it works, anti-forgery tokens, `SameSite` cookies, and why token-in-header auth is largely immune.
- **Atom 13.5.4** — **Broken access control / IDOR** — the most common real-world vulnerability. Always authorise on the server, per resource.
- **Atom 13.5.5** — **SSRF** and why it's devastating in cloud environments (metadata endpoints).
- **Atom 13.5.6** — Insecure deserialisation; XXE.
- **Atom 13.5.7** — Security misconfiguration: default credentials, verbose errors, open S3 buckets, exposed admin endpoints, directory listing.
- **Atom 13.5.8** — Sensitive data exposure: logging tokens, PII in URLs, unencrypted backups.
- **Atom 13.5.9** — Vulnerable dependencies: SCA scanning, `dotnet list package --vulnerable`, `npm audit`, supply chain risk.
- **Atom 13.5.10** — **Security headers**: CSP (and why it's the strongest XSS defence), HSTS, `X-Content-Type-Options`, `X-Frame-Options`/`frame-ancestors`, `Referrer-Policy`.
- **Atom 13.5.11** — Rate limiting, account lockout, and enumeration attacks (including timing-based user enumeration).
- **Atom 13.5.12** — File upload security: type validation, storage location, serving from a separate origin.
- **Atom 13.5.13** — Business logic flaws: race conditions in payments, negative quantities, replay attacks, idempotency as a defence.

### Unit 13.6 — Operational Security

- **Atom 13.6.1** — **Secrets management**: never in source, environment variables vs a vault, Azure Key Vault / AWS Secrets Manager, rotation.
- **Atom 13.6.2** — What to do when a secret leaks — the rotation-first response.
- **Atom 13.6.3** — Principle of least privilege in cloud IAM; role assumption; scoping database users.
- **Atom 13.6.4** — Audit logging and tamper-evidence.
- **Atom 13.6.5** — Data privacy basics: PII classification, GDPR concepts (consent, right to erasure, data minimisation), data residency.
- **Atom 13.6.6** — Incident response: contain, eradicate, recover, post-mortem.

### 📦 MODULE 13 PROOF OF LEARNING

Take your Module 8 API and (1) run **OWASP Juice Shop** and solve 20+ challenges hands-on; (2) build a deliberately vulnerable branch with SQLi, XSS, IDOR and a broken JWT check, exploit each yourself, then fix each and write up the before/after; (3) generate a certificate chain with `openssl` and serve your app over TLS you configured yourself.

---

## PART 4 — DESIGN

---

# MODULE 14 — Low-Level Design

> **Why this exists.** LLD is the interview round that most directly predicts day-to-day performance, because writing code that survives changing requirements *is* the job. The distinguishing skill isn't knowing 23 patterns by name — it's being able to say "I chose composition here because payment methods will grow, and inheritance would force me to modify existing classes." Patterns are vocabulary; the trade-off reasoning is the actual competence being tested.

### Unit 14.1 — Design Principles

- **Atom 14.1.1** — Why design at all: the cost of change over a system's lifetime.
- **Atom 14.1.2** — **SOLID revisited in depth** — one atom per principle, each with a real refactor you perform yourself (this is deliberate repetition of 3.2; now you have code worth refactoring).
- **Atom 14.1.3** — DRY — and its overuse; the wrong abstraction is more expensive than duplication.
- **Atom 14.1.4** — KISS, YAGNI, and recognising over-engineering in your own work.
- **Atom 14.1.5** — Law of Demeter; tell-don't-ask.
- **Atom 14.1.6** — **Composition over inheritance** with a full worked example.
- **Atom 14.1.7** — Program to an interface; designing for extension.
- **Atom 14.1.8** — Separation of concerns, cohesion and coupling as measurable qualities.
- **Atom 14.1.9** — Immutability as a design tool.

### Unit 14.2 — Modelling and Diagrams

- **Atom 14.2.1** — Requirement gathering: functional vs non-functional, in-scope vs out-of-scope.
- **Atom 14.2.2** — Identifying entities/nouns and behaviours/verbs from a problem statement.
- **Atom 14.2.3** — **UML class diagrams**: association, aggregation, composition, inheritance, dependency, multiplicity. Draw them fast and correctly.
- **Atom 14.2.4** — **Sequence diagrams** for a use case flow.
- **Atom 14.2.5** — State diagrams; activity diagrams.
- **Atom 14.2.6** — Value objects vs entities; enums vs polymorphism for varying behaviour.

### Unit 14.3 — Creational Patterns

*For each pattern: the problem it solves → the structure → a real-world example → the trade-off/downside → when NOT to use it.*

- **Atom 14.3.1** — **Singleton** — including thread-safe implementations in C# (`Lazy<T>`), why it's often an anti-pattern, and DI as the better answer.
- **Atom 14.3.2** — **Factory Method** and **Simple Factory**.
- **Atom 14.3.3** — **Abstract Factory** — families of related objects.
- **Atom 14.3.4** — **Builder** — complex construction, fluent APIs, immutable objects with many optional fields.
- **Atom 14.3.5** — **Prototype** — cloning, and its link to deep-copy semantics.
- **Atom 14.3.6** — Object pool — and its link to connection/thread pooling.

### Unit 14.4 — Structural Patterns

- **Atom 14.4.1** — **Adapter** — integrating an incompatible third-party interface.
- **Atom 14.4.2** — **Decorator** — adding behaviour without subclassing. (Note: this is exactly what ASP.NET middleware is.)
- **Atom 14.4.3** — **Facade** — simplifying a complex subsystem.
- **Atom 14.4.4** — **Proxy** — lazy loading, access control, caching, remote proxies.
- **Atom 14.4.5** — **Composite** — tree structures with uniform treatment (file systems, UI trees, nested comments).
- **Atom 14.4.6** — **Bridge** — separating abstraction from implementation.
- **Atom 14.4.7** — Flyweight — sharing to reduce memory.

### Unit 14.5 — Behavioural Patterns

- **Atom 14.5.1** — **Strategy** — the single most useful pattern in day-to-day work. Interchangeable algorithms.
- **Atom 14.5.2** — **Observer** — event notification; its relationship to C# events and pub/sub.
- **Atom 14.5.3** — **Command** — encapsulating requests; undo/redo; queuing.
- **Atom 14.5.4** — **State** — replacing sprawling conditionals with state objects. State machines.
- **Atom 14.5.5** — **Template Method** — algorithm skeleton with overridable steps.
- **Atom 14.5.6** — **Chain of Responsibility** — request pipelines, validation chains, middleware.
- **Atom 14.5.7** — **Iterator** — and its C# realisation via `IEnumerable`/`yield`.
- **Atom 14.5.8** — **Mediator** — reducing many-to-many coupling.
- **Atom 14.5.9** — Visitor, Memento, Interpreter — recognise them, know when they apply.
- **Atom 14.5.10** — Null Object, Specification, Repository, Unit of Work — patterns you'll meet in .NET codebases.

### Unit 14.6 — Code Smells and Refactoring

- **Atom 14.6.1** — Recognising the smell catalogue: long method, god class, primitive obsession, long parameter list, switch statements on type, feature envy, shotgun surgery, temporal coupling.
- **Atom 14.6.2** — Refactoring safely: tests first, small steps, never mix refactor with behaviour change.
- **Atom 14.6.3** — Replace conditional with polymorphism; replace magic number with constant; introduce parameter object; extract class.
- **Atom 14.6.4** — Pattern *over*use — when a strategy pattern for two cases is worse than an `if`.

### Unit 14.7 — LLD Problem Set

**The framework to apply to every problem, in order:**
1. Clarify requirements and explicitly state scope
2. Identify core entities and their attributes
3. Define relationships and cardinality
4. Extract interfaces and identify what varies
5. Apply patterns *only where variation justifies them*
6. Handle concurrency and edge cases
7. Walk through the main use case end to end
8. State what you'd change to support extension X

**Tier 1 — do these first:** Parking Lot · Vending Machine · ATM · Tic-Tac-Toe · Library Management · Snake and Ladder · Coffee Machine

**Tier 2 — the common interview set:** Elevator System · **Splitwise** · BookMyShow / movie ticket booking · **LRU Cache (design version)** · **Rate Limiter** · Logging Framework · Notification Service · Chess · Deck of Cards / Poker

**Tier 3 — harder:** Food Delivery (Swiggy/Zomato) · Ride Hailing (Uber) · Inventory Management · Hotel Booking · Online Auction · Stack Overflow · Calendar/Meeting Scheduler · Traffic Signal System · Distributed Job Scheduler · Payment Gateway

For each, produce: a class diagram, working C# code, and a written note on the patterns used and the trade-offs.

### 📦 MODULE 14 PROOF OF LEARNING

15 LLD problems fully implemented in C# with tests, each in a repo folder with its class diagram and a `TRADEOFFS.md`. For three of them, implement a *second* version after a new requirement is added, and document what your original design made easy or hard.

---

# MODULE 15 — Multithreading and Concurrency Patterns

> **Why this exists.** This is the highest-difficulty, highest-differentiation topic on this list. Concurrency bugs are non-deterministic — they don't reproduce, they don't appear in tests, and they surface in production under load. That makes *correct-by-design* the only viable strategy, which is why the patterns matter more than the primitives. For a .NET developer specifically: you use `async/await` daily, and most developers cannot explain what it does. Being one who can is a genuine step-change in perceived seniority.

### Unit 15.1 — Foundations

- **Atom 15.1.1** — Concurrency vs parallelism — the precise distinction, with an example of each.
- **Atom 15.1.2** — Why concurrency: latency hiding for I/O-bound work vs throughput for CPU-bound work. Two different problems, two different tools.
- **Atom 15.1.3** — Amdahl's law and the limits of parallelisation.
- **Atom 15.1.4** — The .NET threading model: `Thread`, the thread pool, and why you almost never create threads directly.
- **Atom 15.1.5** — Thread pool behaviour: injection rate, starvation, and how a blocked thread pool causes cascading latency.
- **Atom 15.1.6** — Foreground vs background threads; thread lifecycle.
- **Atom 15.1.7** — `Thread.Sleep` vs `Task.Delay` — and why the difference is more than syntax.

### Unit 15.2 — Shared State and Its Hazards

- **Atom 15.2.1** — **Race conditions** — write one, watch a counter lose increments, understand why `i++` isn't atomic.
- **Atom 15.2.2** — Atomicity, visibility, and ordering — the three separate guarantees you need.
- **Atom 15.2.3** — The **memory model**: compiler and CPU reordering, why a variable can be stale in another thread.
- **Atom 15.2.4** — `volatile`, `Volatile.Read/Write`, `Thread.MemoryBarrier` — what they actually guarantee.
- **Atom 15.2.5** — Torn reads/writes for non-atomic types.
- **Atom 15.2.6** — False sharing and cache line contention (connect to Atom 10.4.11).
- **Atom 15.2.7** — Why immutability sidesteps almost all of this — the most underrated concurrency technique.

### Unit 15.3 — Synchronisation Primitives in C#

- **Atom 15.3.1** — `lock` / `Monitor`: entry, exit, `Wait`/`Pulse`. What object to lock on and why never `lock(this)` or `lock("string")`.
- **Atom 15.3.2** — Lock granularity: coarse vs fine; lock contention; the cost of an uncontended vs contended lock.
- **Atom 15.3.3** — `Mutex` (cross-process), `Semaphore` and **`SemaphoreSlim`** (throttling concurrency — very commonly needed).
- **Atom 15.3.4** — `ReaderWriterLockSlim` — when read-heavy access justifies it.
- **Atom 15.3.5** — **`Interlocked`** — lock-free atomic operations, `CompareExchange` and the CAS loop pattern.
- **Atom 15.3.6** — `SpinLock`, `SpinWait` — when spinning beats blocking.
- **Atom 15.3.7** — `ManualResetEventSlim`, `AutoResetEvent`, `CountdownEvent`, `Barrier` — signalling between threads.
- **Atom 15.3.8** — `AsyncLocal` and `ThreadLocal`.
- **Atom 15.3.9** — `Lazy<T>` with thread-safety modes; double-checked locking done correctly.

### Unit 15.4 — Tasks and async/await Deeply

- **Atom 15.4.1** — `Task` and `Task<T>`: the promise model, status, continuations, `ContinueWith`.
- **Atom 15.4.2** — TPL: `Task.Run`, `Task.Factory.StartNew` and why the former is usually correct.
- **Atom 15.4.3** — **What `async`/`await` compiles to** — the state machine. Read the decompiled output once; it dissolves the magic.
- **Atom 15.4.4** — **`async` does not mean "on another thread"** — the single most important correction. I/O-bound async uses zero threads while waiting.
- **Atom 15.4.5** — Synchronisation context, `ConfigureAwait(false)`, and how the context differs in ASP.NET Core vs UI apps.
- **Atom 15.4.6** — **Deadlocks from sync-over-async** (`.Result`, `.Wait()`, `GetAwaiter().GetResult()`) — reproduce one, then never write it again.
- **Atom 15.4.7** — `async void` — why it's only for event handlers, and how it swallows exceptions.
- **Atom 15.4.8** — Exception handling in tasks: `AggregateException`, unobserved exceptions, exceptions from `WhenAll`.
- **Atom 15.4.9** — Composition: `Task.WhenAll`, `WhenAny`, `WhenEach`; timeouts; sequential vs parallel awaits.
- **Atom 15.4.10** — **`CancellationToken`**: creation, linking, propagation through call chains, cooperative cancellation, `ThrowIfCancellationRequested`.
- **Atom 15.4.11** — `ValueTask` — the allocation optimisation and its usage restrictions.
- **Atom 15.4.12** — `IAsyncEnumerable` and `await foreach` — async streaming.
- **Atom 15.4.13** — `TaskCompletionSource` — bridging callback-based APIs into the task world.

### Unit 15.5 — Concurrent Collections and Data Parallelism

- **Atom 15.5.1** — `ConcurrentDictionary`: `GetOrAdd`/`AddOrUpdate` semantics, and the surprising fact that the factory can run more than once.
- **Atom 15.5.2** — `ConcurrentQueue`, `ConcurrentStack`, `ConcurrentBag` — and their intended use cases.
- **Atom 15.5.3** — `BlockingCollection<T>` for producer-consumer with bounding.
- **Atom 15.5.4** — **`System.Threading.Channels`** — the modern, async-friendly producer-consumer. Bounded vs unbounded, backpressure.
- **Atom 15.5.5** — Immutable collections and persistent data structures.
- **Atom 15.5.6** — `Parallel.For`, `Parallel.ForEach`, `Parallel.ForEachAsync`, partitioning, degree of parallelism.
- **Atom 15.5.7** — PLINQ: `AsParallel`, ordering, and when it's slower than sequential.
- **Atom 15.5.8** — Choosing between `Parallel`, PLINQ, `Task.WhenAll` and Channels for a given workload.

### Unit 15.6 — Concurrency Patterns

*These are the reusable shapes that make concurrent code correct by construction.*

- **Atom 15.6.1** — **Producer-Consumer** with a bounded buffer and backpressure.
- **Atom 15.6.2** — **Worker pool / task queue** — fixed workers draining a shared queue.
- **Atom 15.6.3** — **Pipeline** — staged processing with a queue between each stage.
- **Atom 15.6.4** — **Fan-out / fan-in** — parallel dispatch and result aggregation.
- **Atom 15.6.5** — **Scatter-gather** with timeouts and partial results.
- **Atom 15.6.6** — **Throttling / bulkhead** — bounding concurrency with `SemaphoreSlim` to protect a downstream service.
- **Atom 15.6.7** — **Circuit breaker** and **retry with exponential backoff + jitter** (Polly) — and why jitter matters.
- **Atom 15.6.8** — **Actor model** — state confined to a single-threaded actor; why it eliminates locks. Orleans/Akka conceptually.
- **Atom 15.6.9** — **Thread confinement and immutability** as patterns, not just properties.
- **Atom 15.6.10** — **Double-buffering / copy-on-write** for read-heavy shared state.
- **Atom 15.6.11** — **Async coordination**: async locks, async initialisation, async caching with single-flight (preventing cache stampede).
- **Atom 15.6.12** — **Idempotency and at-least-once processing** — the pattern that makes distributed retries safe.
- **Atom 15.6.13** — Graceful shutdown: draining in-flight work with cancellation.

### Unit 15.7 — Debugging and Testing Concurrency

- **Atom 15.7.1** — Deadlock detection: dump analysis, `dotnet-dump`, parallel stacks in the debugger.
- **Atom 15.7.2** — Diagnosing thread pool starvation from metrics.
- **Atom 15.7.3** — Reproducing races: stress testing, adding artificial delays, chaos.
- **Atom 15.7.4** — Writing deterministic tests around non-deterministic code; controlling time with an abstracted clock.
- **Atom 15.7.5** — Benchmarking concurrent code honestly with BenchmarkDotNet.

### 📦 MODULE 15 PROOF OF LEARNING

Build a **concurrent web crawler** in C#: bounded parallelism with `SemaphoreSlim`, a work queue via `Channels`, deduplication with `ConcurrentDictionary`, politeness delays per host, retry with backoff, full cancellation support, and graceful shutdown. It must handle 10,000 URLs without leaking threads or losing work. Then write up every concurrency bug you hit and how you found it.

---

# MODULE 16 — High-Level Design (System Design Basics)

> **Why this exists.** For an SDE-1 you are not expected to design Netflix. You *are* expected to understand the vocabulary, reason about trade-offs, and know why the system you work on is shaped the way it is. The interview signal being measured is: can you ask about requirements before designing, do you know that everything is a trade-off, and can you estimate rather than guess? The long-term value is that you stop treating your company's architecture as arbitrary.

### Unit 16.1 — Fundamentals

- **Atom 16.1.1** — Requirements first: functional, non-functional (latency, availability, consistency, durability), and **scale estimation**.
- **Atom 16.1.2** — **Back-of-envelope estimation**: QPS, storage per year, bandwidth, memory for cache. Memorise the latency numbers every programmer should know.
- **Atom 16.1.3** — Vertical vs horizontal scaling; **stateless services** as the precondition for horizontal scaling.
- **Atom 16.1.4** — Availability: the nines and what each means in downtime per year; SLA vs SLO vs SLI.
- **Atom 16.1.5** — Single points of failure; redundancy; failover; active-active vs active-passive.
- **Atom 16.1.6** — Latency vs throughput; tail latency (p50 vs p95 vs p99) and why averages lie.
- **Atom 16.1.7** — The fallacies of distributed computing — read the list and internalise it.

### Unit 16.2 — The Building Blocks

- **Atom 16.2.1** — **Load balancing**: L4/L7, algorithms, health checks, LB redundancy.
- **Atom 16.2.2** — **Caching**: where to cache (browser, CDN, gateway, app, database), cache-aside vs read-through vs write-through vs write-behind, eviction policies, TTL strategy.
- **Atom 16.2.3** — Cache problems: **stampede/thundering herd**, hot keys, invalidation, and staleness as a deliberate choice.
- **Atom 16.2.4** — **CDN** and edge caching; static vs dynamic content.
- **Atom 16.2.5** — **Database scaling**: read replicas, replication lag, sharding, shard key choice, resharding pain, federation.
- **Atom 16.2.6** — **Consistent hashing** — the problem it solves when nodes are added or removed. Virtual nodes.
- **Atom 16.2.7** — **Message queues and event streaming**: point-to-point vs pub/sub; RabbitMQ vs Kafka (queue vs log); partitions, consumer groups, ordering guarantees.
- **Atom 16.2.8** — Delivery semantics: at-most-once, at-least-once, exactly-once (and why the last is a lie without idempotency).
- **Atom 16.2.9** — Dead letter queues, poison messages, replay.
- **Atom 16.2.10** — Blob/object storage vs a database — what never belongs in a relational table.
- **Atom 16.2.11** — Search infrastructure: inverted indexes, Elasticsearch, and keeping a search index in sync.
- **Atom 16.2.12** — API gateway, service discovery, service mesh at vocabulary level.

### Unit 16.3 — Distributed Systems Concepts

- **Atom 16.3.1** — **CAP theorem** — stated precisely (it's about behaviour during a partition), and the common misstatements.
- **Atom 16.3.2** — **PACELC** — the extension that covers the non-partitioned case.
- **Atom 16.3.3** — Consistency models: strong, eventual, causal, read-your-writes, monotonic reads.
- **Atom 16.3.4** — **Idempotency** — idempotency keys, safe retries. The most practically useful concept in this unit.
- **Atom 16.3.5** — Distributed transactions: two-phase commit and why it's avoided; the **Saga pattern** with compensation.
- **Atom 16.3.6** — The **outbox pattern** — the standard solution to "write to DB and publish an event atomically".
- **Atom 16.3.7** — Leader election, consensus (Raft/Paxos conceptually), quorum reads/writes.
- **Atom 16.3.8** — Clocks: why wall clocks are unreliable; logical clocks and vector clocks conceptually.
- **Atom 16.3.9** — **Resilience patterns**: timeout (always), retry with backoff and jitter, circuit breaker, bulkhead, fallback, graceful degradation, load shedding.
- **Atom 16.3.10** — Rate limiting algorithms: fixed window, sliding window log, sliding window counter, token bucket, leaky bucket — with the trade-off of each. Distributed rate limiting with Redis.
- **Atom 16.3.11** — Backpressure across a system.

### Unit 16.4 — Architecture Styles and Operations

- **Atom 16.4.1** — **Monolith vs microservices** — the honest trade-off; why a modular monolith is usually right for a small team; distributed monolith as the failure mode.
- **Atom 16.4.2** — Service boundaries: bounded contexts, and the database-per-service rule.
- **Atom 16.4.3** — Synchronous vs asynchronous communication; when an event beats a call.
- **Atom 16.4.4** — Event-driven architecture; event sourcing and CQRS at a systems level.
- **Atom 16.4.5** — **Observability**: logs, metrics, traces; correlation IDs; RED and USE method dashboards; alerting on symptoms not causes.
- **Atom 16.4.6** — Deployment strategies: rolling, blue-green, canary; feature flags; safe rollback.
- **Atom 16.4.7** — Capacity planning, autoscaling, and cost as a design constraint.
- **Atom 16.4.8** — Multi-region, disaster recovery, RPO/RTO.

### Unit 16.5 — Case Studies

*Practise the same 6-step framework each time: requirements → estimation → API design → data model → high-level architecture → bottlenecks and trade-offs.*

**Start here:** URL shortener · Pastebin · **Rate limiter** · Key-value store · Web crawler · Notification service (email/SMS/push) · File storage (Dropbox-lite)

**Then:** Chat application (delivery, presence, ordering) · News feed (fan-out on write vs read) · **Ticket booking with no double-booking** · Payment system with idempotency · Ride-hailing matching · Video streaming basics · Distributed job scheduler · Leaderboard · Autocomplete/typeahead service · Analytics/metrics pipeline

**Also do:** the design of the system you actually work on. Write it up. Find one thing you'd change and know why.

### 📦 MODULE 16 PROOF OF LEARNING

Ten written designs, each 2–3 pages with a diagram, explicit estimation numbers, and a "trade-offs and what I'd do differently at 100x scale" section. Then actually *build* two of them small-scale — a URL shortener with Redis caching and a distributed rate limiter — and load-test them until they break.

---

## PART 5 — THE FRONTIER

---

# MODULE 17 — Agentic AI

> **Why this exists.** Two reasons, and only one of them is hype. **The career reason:** in 2026 the differentiator for a junior engineer is no longer "can code" but "can build systems that use models correctly" — and most developers using LLMs are doing prompt-and-pray, not engineering. **The engineering reason:** agentic systems are distributed systems with a non-deterministic, expensive, occasionally-lying component in the middle. Everything you learned in Modules 15 and 15 — retries, idempotency, timeouts, circuit breakers, observability, backpressure — applies directly, plus new failure modes. This module is last precisely because it *depends* on all of that.

### Unit 17.1 — How Models Actually Work (enough to engineer with)

- **Atom 17.1.1** — Tokens and tokenisation; why cost and limits are counted in tokens; why models are bad at character-level tasks.
- **Atom 17.1.2** — Next-token prediction, the transformer at a conceptual level, attention as "what should I look at".
- **Atom 17.1.3** — **The context window** — what it includes, why it's the central constraint in agent design, and context rot in long conversations.
- **Atom 17.1.4** — Sampling parameters: temperature, top-p, and when determinism matters.
- **Atom 17.1.5** — Base models vs instruction-tuned vs RLHF; what "alignment" changes.
- **Atom 17.1.6** — **Hallucination** — why it's structural rather than a bug, and the engineering responses (grounding, citations, verification, constrained output).
- **Atom 17.1.7** — **Embeddings**: vectors as meaning, cosine similarity, and why they enable semantic search.
- **Atom 17.1.8** — Model selection: capability vs latency vs cost; when a small model is the right call; routing between models.
- **Atom 17.1.9** — Statelessness: the model remembers nothing; every turn re-sends the history. This drives all memory design.

### Unit 17.2 — Prompting as Engineering

- **Atom 17.2.1** — Anatomy of a prompt: system vs user vs assistant roles and what each is for.
- **Atom 17.2.2** — Specificity, examples, and explicit output format — the three highest-impact levers.
- **Atom 17.2.3** — Zero-shot, few-shot, chain-of-thought; when reasoning steps help and when they waste tokens.
- **Atom 17.2.4** — **Structured output**: JSON mode, schema enforcement, and validating with a parser rather than trusting.
- **Atom 17.2.5** — Prompt templating and versioning — treat prompts as code, in source control, with tests.
- **Atom 17.2.6** — Decomposition: chaining focused prompts instead of one giant one.
- **Atom 17.2.7** — Failure handling: what to do when the model returns malformed output (repair loop, retry with error, fallback).
- **Atom 17.2.8** — Context management: summarisation, truncation strategies, relevance filtering.

### Unit 17.3 — Tool Use and Retrieval

- **Atom 17.3.1** — **Function/tool calling**: schema definition, the model choosing a tool, your code executing it, feeding results back. This is the core agentic mechanism.
- **Atom 17.3.2** — Designing good tools: clear names and descriptions, narrow scope, meaningful error messages back to the model.
- **Atom 17.3.3** — Tool execution safety: validation, sandboxing, permissions, human approval for destructive actions.
- **Atom 17.3.4** — **MCP (Model Context Protocol)** — standardised tool/context servers; building a simple MCP server.
- **Atom 17.3.5** — **RAG, the pipeline**: ingest → chunk → embed → store → retrieve → rerank → generate.
- **Atom 17.3.6** — **Chunking strategies**: fixed, recursive, semantic, document-structure-aware. Overlap. Why chunking quality dominates RAG quality.
- **Atom 17.3.7** — **Vector databases**: pgvector, Qdrant, Pinecone; ANN indexes (HNSW, IVF); the recall/latency trade-off.
- **Atom 17.3.8** — **Hybrid search**: dense + keyword (BM25), reciprocal rank fusion — nearly always better than vectors alone.
- **Atom 17.3.9** — Reranking with a cross-encoder; query rewriting and expansion.
- **Atom 17.3.10** — Metadata filtering and access control in retrieval — *the security problem nobody handles* (a user must not retrieve documents they can't read).
- **Atom 17.3.11** — Evaluating retrieval separately from generation: recall@k, precision, faithfulness, answer relevance.
- **Atom 17.3.12** — When RAG is the wrong answer: use a SQL query, a real search index, or fine-tuning instead.

### Unit 17.4 — Agents

- **Atom 17.4.1** — What makes something an "agent": a loop with tools, state, and a termination condition. Workflow vs agent — and why most problems want a workflow.
- **Atom 17.4.2** — **The ReAct loop**: reason → act → observe → repeat. Implement it by hand before touching a framework.
- **Atom 17.4.3** — Planning: decomposition, plan-and-execute, replanning on failure.
- **Atom 17.4.4** — **Memory**: short-term (conversation), working (scratchpad), long-term (vector or structured store); what to persist and what to forget.
- **Atom 17.4.5** — Reflection and self-critique loops; the diminishing returns.
- **Atom 17.4.6** — **Termination and loop control** — max iterations, budget caps, progress detection. Agents that loop forever are the default failure mode.
- **Atom 17.4.7** — Multi-agent systems: supervisor/worker, specialist agents, handoffs. When multi-agent is genuinely better vs when it's one agent with more tools.
- **Atom 17.4.8** — **Human-in-the-loop**: approval gates, interruption, correction, and designing for the fact that the agent will be wrong.
- **Atom 17.4.9** — Agent-computer interfaces: code execution, browser automation, file systems.
- **Atom 17.4.10** — Frameworks: **Semantic Kernel** and **Microsoft.Extensions.AI** for .NET, LangChain/LangGraph in Python. Understand the primitives well enough to know what the framework hides — and to write it without one.

### Unit 17.5 — Production Concerns

*This unit is where your Modules 8–16 knowledge transfers directly, and where most AI projects fail.*

- **Atom 17.5.1** — **Evaluation**: building an eval set, LLM-as-judge and its biases, regression testing prompts, offline vs online eval. Without evals you are guessing.
- **Atom 17.5.2** — Observability: tracing an agent run, logging every prompt/completion/tool call, LangSmith/Langfuse/OpenTelemetry-style instrumentation.
- **Atom 17.5.3** — **Cost engineering**: token accounting, caching (prompt caching, semantic caching), model routing, batching, budget limits per user.
- **Atom 17.5.4** — **Latency**: streaming responses, parallel tool calls, speculative execution, perceived vs actual latency.
- **Atom 17.5.5** — Reliability: timeouts, retries with backoff, fallback models, circuit breakers, graceful degradation. *(Directly Module 15/15 material.)*
- **Atom 17.5.6** — Rate limits and quota handling across providers.
- **Atom 17.5.7** — **Prompt injection** — direct and indirect. The core insight: the model can't distinguish instructions from data. Mitigations: privilege separation, output filtering, never letting retrieved content grant capability, treating tool output as untrusted.
- **Atom 17.5.8** — Data leakage: PII in prompts, training-data concerns, tenant isolation, what you send to a third-party API.
- **Atom 17.5.9** — Guardrails: input validation, output filtering, content moderation, refusal handling.
- **Atom 17.5.10** — Non-determinism in testing; snapshot testing; setting temperature to 0 and why that still isn't deterministic.
- **Atom 17.5.11** — Fine-tuning vs RAG vs prompting — the decision framework and the cost of each.
- **Atom 17.5.12** — The product question: where an agent genuinely beats a form and a database, and where it's a worse UI with extra steps.

### 📦 MODULE 17 PROOF OF LEARNING

Build **two** things in C#/.NET. **(1) A RAG system over a real corpus** (your own notes from this syllabus would be ideal) — with hybrid search, reranking, citations, an eval set of 50 questions with measured retrieval and answer quality, and cost/latency tracking. **(2) An agent with real tools** — database queries, an external API, and file operations — with approval gates on destructive actions, full tracing, budget caps, iteration limits, and a written threat model covering prompt injection. Then write up where each failed and what you changed.

---

## PART 6 — RUNNING THE PLAN

### The weekly cadence

| | |
|---|---|
| **Mon–Fri** | 2–3 hrs on the current module, hardest material first while you're fresh. Once DSA is done, add 3–4 maintenance problems across the week. |
| **Saturday** | 4–5 hrs project work on the current module's build |
| **Sunday** | 2 hrs review (spaced repetition deck + rewrite one notebook section from memory) + 1 hr planning next week |

Protect the review hour. It's the one that converts everything else into knowledge.

### The monthly review

At the end of each month, answer these four questions in writing:

1. What can I now explain that I couldn't 30 days ago?
2. What did I *think* I understood but failed to explain out loud?
3. What did I build, and what broke in it?
4. What am I avoiding, and why?

Question 4 is the important one. The topic you keep deferring — usually DP, graphs, or concurrency — is the one with the highest return.

### Depth calibration for SDE-1

You do not need equal depth everywhere. Calibrate deliberately:

| Depth | Modules | What "done" means |
|---|---|---|
| **Deep — can build and debug unaided** | JavaScript, React, C#/OOP, ASP.NET Core, DSA, SQL & indexing, LLD | You can implement from scratch, debug production issues, and defend design choices |
| **Solid — can explain mechanisms and apply** | Networks (HTTP/TCP/DNS/TLS), Security (auth + OWASP), Concurrency, OS (processes/memory/scheduling), Terminal + Docker + CI/CD | You can explain *why* it behaves that way and reason about consequences |
| **Working — vocabulary and trade-offs** | HLD, distributed systems, Kubernetes, cloud services beyond the ones you deployed to, Agentic AI production concerns | You can follow a design discussion, ask good questions, and know what to look up |

Trying to reach "deep" everywhere is the most common way this plan fails. Going wide at the wrong depth is the second.

### Closing the tier-3 gap, concretely

The gap closes through **visible artifacts**, not through completion. By the end you should have:

- A public GitHub with 6+ substantial projects, each with a real README explaining the *why* and the trade-offs
- A written notebook covering all 16 modules, in your own words
- 350+ DSA solutions annotated with patterns
- 25 timed machine-coding builds
- 15 implemented LLD problems with diagrams
- 10 written system designs
- One deployed, monitored, load-tested application on a real domain — containerised, on a custom domain with TLS, with its infrastructure in code and a CI/CD pipeline behind it
- 3–5 technical write-ups (blog or repo docs) on things you debugged or built — writing publicly is disproportionately effective for candidates without a brand-name college

Nobody asks where you studied when you can hand them that.

### A final note on sequencing

If you have to compress this, compress in this order — cut depth, never cut a module entirely:

1. **Never cut:** DSA, C#/OOP, ASP.NET Core, SQL, JavaScript, React, LLD
2. **Compress to essentials:** OS (processes, memory, concurrency primitives only), Networks (HTTP, TCP, DNS, TLS only), HLD (building blocks + 5 case studies), Cloud (Units 12.1–12.3 in full, then one provider only — skip the second entirely)
3. **Compress last:** Agentic AI — but don't skip it; it's your differentiator

And the single highest-leverage habit in this whole document: **after every session, close the tab and explain what you learned out loud, from memory, in under two minutes.** Where you stumble is your real syllabus.
