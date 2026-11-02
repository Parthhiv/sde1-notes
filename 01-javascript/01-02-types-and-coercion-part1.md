# Unit 1.2 — Types and Coercion (Part 1)

> **Why this exists.** `==` bugs, `NaN` propagation, and the "why did my object comparison fail" class of bugs all come from not knowing what values *are* and what happens when they meet. Part 1 covers atoms 1.2.1–1.2.4 complete; Part 2 (atoms 1.2.5–1.2.7) next.

---

## The Problem This Solves

In C#, the compiler checks types *before* the program runs — the whole type system is a hierarchy descending from `Object`, and value types get boxed into that hierarchy only when needed. Two classes of bugs happen when that mental model leaks into JavaScript:

1. **The null check that never fires.** `typeof value === "null"` is never true, because `typeof null` returns `"object"` — a frozen 1995 quirk. Silent no-op in production.
2. **The wrong type that sails through.** `half("10")` returns `5` with no error because JS checks types only when an operation forces coercion, at runtime. A string can slip all the way to production.

Interview failure mode: "Why does `typeof null` return `object`?" — Answering "I don't know, it's just weird" fails; the answer is a *historical bit-pattern freeze*, and knowing it signals you understand the type system underneath.

---

## The Mental Model

> JavaScript values are **tags in memory**, not objects in a hierarchy. Every value carries a small type tag — 8 possible tags: **7 primitives** (`number`, `string`, `boolean`, `undefined`, `null`, `symbol`, `bigint`) and **object**. `typeof` doesn't inspect a class definition like C# — it just reads the tag. That's why it's instant, why there's no boxing (primitives never get wrapped just to be asked a question), and why `typeof null` lies: the `null` value's tag shared a bit pattern with fresh objects in the very first engine, and the quirk got frozen into the spec forever because fixing it would break every website on Earth.

**One-liner:** *`typeof` reads a tag, not a truth.*

---

## The Details

### Atom 1.2.1 — The 7 primitives + object, `typeof` and its lies

All tags in one place, with the two surprises marked:

```js
typeof 42;             // "number"    (integers AND decimals — one tag, i.e. float64)
typeof "hi";           // "string"
typeof true;           // "boolean"
typeof undefined;      // "undefined"
typeof null;           // "object"    ← THE FAMOUS LIE
typeof Symbol();       // "symbol"
typeof 10n;            // "bigint"
typeof {};             // "object"
typeof [];             // "object"    ← surprise 1: arrays get no dedicated tag
typeof function () {}; // "function"  ← surprise 2: functions DO get one
```

**Surprise 1 — arrays.** `[1,2,3]` is an object with a `length` property and number-like keys. There is no "array" tag, so a `typeof`-based array check never fires:

```js
const scores = [90, 85];
typeof scores;              // "object"
if (typeof scores === "array") {}   // NEVER true — broken check
Array.isArray(scores);      // true  ← the only safe array check
```

**Surprise 2 — functions.** Functions ARE objects (they carry properties — `fn.name`, `fn.length`), but they're callable, so the spec gives them their own tag. `typeof` is the standard check for anything callable.

**Methods on primitives — the temporary ghost:**

```js
"hi".toUpperCase(); // "HI" — but strings are primitives. How?
```

The engine wraps the primitive in a temporary object, calls the method on the wrapper as a borrow, returns the result, and discards the wrapper. No boxing is persisted. Prove it: assign a property to a primitive and the write vanishes (or throws in strict mode) — the wrapper is gone before you can read it.

**Real use — shape-checking at an API boundary:**

```js
function renderUser({ name }) {
  if (typeof name !== "string") {
    throw new TypeError(`Expected name as string, got ${typeof name}`);
  }
  return name.toUpperCase();
}
renderUser({ name: 42 }); // TypeError: Expected name as string, got number
```

But know what `typeof` does NOT catch here: `null` passes `typeof x === "object"`, so the null check must be `value === null`, never `typeof value === "null"`.

**Presence vs shape — the broken existence check:**

```js
// Broken: null passes, then crashes on use
if (typeof value === "object") { value.something; } // TypeError when value === null

// Fixed: explicit null check first
if (typeof value === "object" && value !== null) { ... }
// or: value != null  (loose == catches both null and undefined — see Atom 1.2.5)
```

---

### Atom 1.2.2 — Value vs reference semantics

**The C# bridge:** `int a = 5; int b = a;` copies the value; `Student y = x;` copies the *reference*. JavaScript has the identical rule — 7 primitives copy the value, the 8th tag (object) copies the address. The trap is thinking this is *like* C# and then getting surprised by one thing C# doesn't have: **mutating objects is legal from anywhere, including through props.** *(Learner predicts first — was answered "primitives vs object split" before teaching.)*

The classic bug it causes:

```js
const player = { score: 10 };
const copy = player;

copy.score = 999;
console.log(player.score); // 999 — "I never touched player…?!"
```

And the React escalation — invisible to `console.log` because the data *looks* updated:

```js
// Broken React — component seems to never re-render
function addItem(items, newItem) {
  items.push(newItem); // mutates the same array React received as props
  setItems(items);     // same reference → React sees "nothing changed" → skips render
}
```

**Mental model of this atom:** *primitives copy the thing; objects copy the address*. A primitive variable holds the value itself — a photocopy, independent after assignment. An object variable holds a **heap address** — like two email aliases for one mailbox: editing the mailbox shows through both names, deleting an alias (reassignment) touches neither the other name nor the mailbox.

**All three surprises in one run:**

```js
let a = 5;
let b = a;
b = 10;
console.log(a, b); // 5, 10  — primitive: photocopy, independent

let objA = { n: 1 };
let objB = objA;     // copies the ADDRESS, not the object
objB.n = 2;
console.log(objA.n); // 2 — same object, seen through two names

objB = { n: 99 };    // reassign objB to a NEW object
console.log(objA.n); // 2 — reassignment changes the name, not the shared object
```

**Function arguments — the interview question. JS is *always* pass-by-value:**

```js
function reassign(input) {
  input = { n: 100 }; // rebinds the local name only
}
const outer = { n: 1 };
reassign(outer);
console.log(outer.n); // 1 — reassignment invisible outside

function mutate(input) {
  input.n = 100; // follows the COPIED address to the shared object
}
mutate(outer);
console.log(outer.n); // 100 — mutation is visible outside
```

Interview phrasing: *"JS is purely pass-by-value. For objects, the value being passed is a reference, so mutations through the parameter reach the caller's object, but reassignment never does."*

**The React fix — replace, don't mutate. Same data, new reference:**

```js
setItems([...items, newItem]);            // new array, same elements
setItems(items.filter(i => i.id !== id)); // fresh array
setUser({ ...user, score: 999 });         // fresh object
```

**Equality connects here:** `const x = { n: 1 }; x === { n: 1 };` — `false`. Object equality is an *address comparison* ("same identity"), never contents. Two identically-fetched API users are never `===`. This is the root of "why did my object comparison fail" (mechanics land in Atom 1.2.3).

---

### Atom 1.2.3 — Abstract vs strict equality

**Mental model of this atom:** *`===` compares tags; `==` converts then compares those.* `===` reads nothing but the type tags — types differ, `false` instantly, no conversion. `==` behaves exactly like `===` when tags match, and when they don't, converts both operands toward a shared shape using a fixed spec algorithm:

| `==` case | rule |
|---|---|
| `null == undefined` | `true` — spec-defined special pair, nothing else converts to either |
| `null == 0 / "0" / false` | `false` — null's only ==-partner is `undefined` |
| `NaN == anything` (even NaN) | `false` — NaN refuses every comparison |
| `number == string` | string → number, then number vs number |
| `boolean == anything` | boolean → number FIRST (`true` → 1), then continue |
| `number/bigint == object` | object → primitive via `ToPrimitive` (`valueOf`, then `toString`) |

**The famous `[] == false`, walked step by step:**

```js
[] == false;
// Step 1: boolean present → convert to number first: false → 0 → [] == 0
// Step 2: array (object) vs number → ToPrimitive: valueOf([]) is itself, so toString → ""
//         → "" == 0
// Step 3: number == string → string → number: "" → 0 → 0 == 0
// → true
```

And the apparent contradiction it causes: `!![]` is `true` (truthiness — all objects are truthy) while `[] == false` is `true` (coercive equality — different algorithm). **Truthiness ≠ Equality.**

**Why `"true" == true` is false — the boolean-first trap:**

```js
"true" == true;
// true → 1 first (boolean→number), then string→number: "true" → NaN
// NaN == 1 → false
```

The fix: keep tags equal, never negotiate.

```js
const isActive = String(confirmValue).toLowerCase() === "true";
```

**The one idiomatic `==`:**

```js
if (value == null) { // "no value" — true for null AND undefined, nothing else
  return "no value";
}
// never accidentally catches 0, "", NaN — see Atom 1.2.4's if (count) bug
```

**The most-brainbreaking fact — relational operators use a *different* algorithm:**

```js
null == 0;   // false — == treats null as a special value
null >= 0;   // true!  — relational ops convert both sides to number: null → 0
null > 0;    // false
```

Interview phrasing: *"Relational operators run a number-only algorithm, so null → 0 → 0 >= 0 is true. Coercive equality treats null as a unique value that only pairs with undefined. Two algorithms, one value."*

---

### Atom 1.2.4 — Truthy/falsy — the exact list of 8

**Mental model of this atom:** truthiness is a property of a value in a **boolean slot** (`if`, `&&`, `?`, `!!`). JS has exactly 8 falsy values — everything else is truthy:

```js
false; 0 / -0; ""; 0n; null; undefined; NaN; document.all; // the 8 (document.all = legacy IE footnote)
```

And the counterintuitive pair to memorize so they're never separated again: **`""` is falsy, but `[]` and `{}` are ALWAYS truthy** — objects never make the falsy list (tag reasoning from Atom 1.2.1). Also `"0"` is truthy — only the empty *string* is falsy.

The bug the syllabus names by hand — `if (count)`:

```js
// Broken: treats "falsy" as "absent"
function renderCount(count) {
  if (count) return `${count} items`;
  return "No items";
}
renderCount(0); // "No items" — count EXISTS, its value is literally 0!
```

The fix isn't `count === undefined` shell-games — it's *naming what "missing" means*:

```js
function renderCountFixed(count) {
  if (count != null) {        // the "no value" idiom from Atom 1.2.3 — 0 is a real value here
    return `${count} items`;
  }
  return "No items";
}
```

Re-derivable truthiness table:

| Tag | Falsy only when |
|---|---|
| `number` | `0`, `-0`, `NaN` |
| `bigint` | `0n` |
| `string` | `""` only |
| `boolean` | `false` |
| `object` | **never** (`[]`, `{}` truthy; legacy exception `document.all`) |
| `null`/`undefined` | **always** |

**The React rendering version of the same bug:**

```jsx
// Broken: renders a naked 0 on screen
{itemCount && <Counter items={itemCount} />}
// itemCount = 0 → `0 && ...` returns 0 → React renders the number 0

// Fixed: boolean-only expression, or ternary
{itemCount > 0 && <Counter items={itemCount} />}
{itemCount ? <Counter items={itemCount} /> : null}
```

Why: `&&`/`||` **return the operands, not booleans** — the falsy side's value escapes the short-circuit, and React renders anything that isn't `false`/`null`/`undefined`.

---

## The Gotchas / Things That Bit Me

**From Atom 1.2.1:**

- **`typeof null === "object"`** — the never-fixable quirk. Check null with `value === null`. The keyword can't be repurposed without breaking the web, so the lie is permanent.
- **`typeof` returns strings** — `"number"`, not `number`. `typeof x == typeof y` compares strings.
- **Arrays report `"object"`** — `typeof arr === "object"` is true for arrays and plain objects alike. Only `Array.isArray()` separates them.
- **`typeof NaN === "number"`** — NaN is tagged as a number, just an *invalid* one (full story in Atom 1.2.6).
- **`typeof` on a missing variable** doesn't throw — `typeof undeclaredVar` returns `"undefined"` even though *reading* `undeclaredVar` throws a ReferenceError. Handy, but it also masks typos.
- **`typeof` checks shape, not presence** — `typeof value === "object"` is true for `null`, arrays, and objects; every combined "is it complex" check needs extra conditions.

**From Atom 1.2.2:**

- **`const` doesn't freeze objects** — it locks only the address: `const user = {}; user.age = 5` works, `user = {}` throws. Value locks live via `Object.freeze` (Atom 1.4.2).
- **Spread is shallow at one level** — `{ ...obj }` is a new object, but nested values inside are still shared addresses (full mechanics + fix in Atom 1.2.7).
- **C# analogy that breaks: `string`** — C# strings are reference types; JS strings are *primitives*. Both behave "safe" on reassignment, but the reason differs: value copy in JS, immutable-by-design reference in C#.
- **Reassignment vs mutation through a parameter** — `fn(x)` can never change your variable `x`, but can always change `x`'s *contents*. `arr.sort()` mutates in place as a side effect (Atom 1.5.6 list).
- **Primitive property writes silently vanish** — `"hello".foo = "bar"` does nothing (sloppy) or throws TypeError (strict); the temporary wrapper is gone before you can read it.

**From Atom 1.2.3:**

- **`NaN == NaN` is false** — NaN is *defined* to be inequal to everything including itself; the only value where `x === x` is false (math reason lands in Atom 1.2.6).
- **`null == 0` false but `null >= 0` true** — relational operators run a number-only algorithm (null → 0); coercive equality treats null as a special value. Worth writing a test for once, just to believe it.
- **`"true" == true` is false** — boolean→number conversion happens FIRST, so it becomes `NaN == 1`. Never trust remembered `==` outcomes; recall the step order instead.
- **Truthiness ≠ equality** — `!![]` is `true`, and `[] == false` is also `true`. Two different conversion paths, no contradiction — but never let one intuition leak into the other.
- **`[] == ""` is true, `[] == []` is false** — the first is `ToPrimitive` + `"" → 0`; the second is address comparison from 1.2.2.

**From Atom 1.2.4:**

- **`[]` and `{}` are truthy even though `""` isn't** — objects never make the falsy list. `if (arr)` succeeds even for an empty array; use `arr.length > 0` when you mean "has items".
- **`document.all` is the 8th falsy value** — an ancient IE relic (it even reports `typeof === "undefined"`). Ignore it in daily work, but knowing "7 real + 1 legacy footnote" beats anyone who confidently says "six falsy values".
- **`"0"` the string is truthy** — only `""` is falsy among strings. Yes, that's why `if (requestStatus)` behaves differently from `if (Number(requestStatus))`.
- **`&&`/`||` return the OPERANDS, not booleans** — `0 || "fallback"` → `"fallback"`; this is the mechanism behind the React 0-render bug and the `??` design (Atom 1.2.5).

---

## Interview-Shaped Questions I Can Now Answer

1. **"Why does `typeof null` return `object`?"**
   Historical: the `null` value's type tag shared a bit pattern with an empty object reference in the original 1995 engine. Freezing it into the spec preserved backward compatibility with every deployed page. It's a *documented lie* — check null via `value === null`. (TypeScript models this too: `typeof x === "object"` admits `null` until `strictNullChecks` narrows it.)

2. **"Why does `typeof () => {}` return `"function"` but `typeof []` return `"object"`?"**
   Functions are callable objects carrying properties, and callability is special enough to warrant a dedicated tag per spec. Arrays chose no dedicated tag — they behave as plain objects, so the only safe array check is `Array.isArray()`.

3. **"If strings/numbers are primitives, why do `"hi".toUpperCase()` and `42.toFixed(2)` work?"**
   The engine wraps the primitive in a temporary object, calls the method on the wrapper, returns the result, and discards the wrapper. No lasting boxing — which is why property assignments on primitives don't stick (the wrapper is gone by the time you read it).

4. **"How would you safely test whether a value is an object (not null, not array)?"**
   `typeof value === "object" && value !== null && !Array.isArray(value)` — three conditions, because the tag lies for `null` and arrays share the tag.

*From Atom 1.2.2:*

5. **"Is JS pass-by-value or pass-by-reference?"**
   Pure pass-by-value; for objects the value is a reference. Mutation is visible to the caller, reassignment never is — demonstrate both live to prove it.

6. **"Why did my `useEffect` fire forever, or never?"**
   Dependency comparison uses `Object.is` on the *addresses*. A fresh object literal in deps → new address each render → fires forever. Mutating a dep in place → same address → never fires even though the data changed.

7. **"Two users fetched from the API have identical fields — why does `user1 === user2` fail?"**
   Object equality is address/identity comparison, never contents. Options: field-by-field, `JSON.stringify` (caveats: key order, `undefined`, functions, circular refs), or holding one canonical shared reference.

*From Atom 1.2.3:*

8. **"What does `==` actually do vs `===`?"**
   Same tags → identical behavior. Different tags → spec-defined coercion (string→number, boolean→number first, object→primitive via `ToPrimitive`). `===` compares tags and rejects mismatch with no conversion. Use `===` everywhere except the deliberate `x == null` nullable idiom.

9. **"Why is `null >= 0` true but `null == 0` false?"**
   Relational operators run a number-only algorithm — null converts to 0, so `0 >= 0` is true. Coercive equality treats null as unique and only ever pairs it with `undefined`. Two algorithms, one value — this is the answer that separates memorizers from spec-readers.

*From Atom 1.2.4:*

10. **"Name every falsy value — and why does `if (count)` break?"**
    `false`, `0`/`-0`, `NaN`, `0n`, `""`, `null`, `undefined`, `document.all`. `if` coerces to truthiness, so a real-but-zero `count` short-circuits. The fix is naming what "missing" means — `count != null` (present) vs `count == null` (absent).

11. **"Why does `{itemCount && <Component />}` render a 0 on screen?"**
    `&&` returns its operands, not booleans — `0` escapes the short-circuit, and React renders any value except `false`/`null`/`undefined`. Fix: boolean-only guards (`itemCount > 0 && ...`) or ternaries.

---

## Code I Wrote

*(Session proofs for atoms 1.2.2+ will be appended here as they're completed — nothing run yet for Unit 1.2.)*

| # | Build | Atom | Status |
|---|---|---|---|
| — | — | — | pending first proof |

---

## Atom Coverage In This File

| Atom | Topic | Sections present |
|------|-------|------------------|
| 1.2.1 | 7 primitives + object, `typeof` lies | Explanation, Gotchas, Interview Questions |
| 1.2.2 | Value vs reference semantics | Explanation, Gotchas, Interview Questions |
| 1.2.3 | Abstract vs strict equality | Explanation, Gotchas, Interview Questions |
| 1.2.4 | Truthy/falsy — the 8 falsy values | Explanation, Gotchas, Interview Questions |

**Gaps:**
- Part 1 teaches-back were skipped/light in session — the four one-liners (tag reading, address copy, tag comparison, 8-value roster) should be recited before interviews
- No proof-of-learning run yet for Unit 1.2 — unit proof is `deepEqual(a, b)`, due after Part 2

---

*Next: `01-02-types-and-coercion-part2.md` (covers atoms 1.2.5–1.2.7 — null/undefined, NaN & floating-point, shallow vs deep copy)*
*Part 2 is created once atoms 1.2.5–1.2.7 are taught.*