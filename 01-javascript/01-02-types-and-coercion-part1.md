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

#### The Problem

You know the rule "use `===`". But code you *didn't write* uses `==` — legacy code, code with `x == null` (which you must NOT "fix" to `x === null`), and a bug that shows up in your own `===` code anyway. The scenario where lack of this atom actually hurts:

```js
// API returns: { "expiry": 0 } when the token has expired, number
if (expiry === 0) { refresh(); }
// Bug: some APIs return expiry as the STRING "0"
typeof expiry; // "string"
expiry === 0;  // false — never refreshes. Token silently expires.
```

And the reverse failure — an interviewer asks you to *evaluate* `[] == false`, `"" == 0`, `"true" == true` where guessing is impossible. If you can't run the algorithm in your head, `==` stays black magic forever.

#### The Mental Model

> Think of `===` as a **strict customs officer**: it reads the type tag on each passport and if they don't match, it says no *without even opening the bag*. `==` is a **cooperative translator**: it only starts translating when the two passports differ, and it translates by fixed spec rules — *string becomes number, boolean becomes number first, object becomes a primitive string*. After translation, it compares like `===` would. So every `==` comparison you can't solve instantly is just a small chain of translations away from a `===` you can.

**One-liner:** *`===` compares tags; `==` translates until the tags match, then compares.*

#### The Explanation — a solver's checklist you can run mechanically
# JavaScript `==` — Solver's Checklist with Examples

Evaluate ANY `==` expression using these steps, in order. Stop as soon as one applies.

## STEP 1 — Same types on both sides?

Both values have the same data type (number, string, boolean, etc.).

- **YES:** Compare exactly like `===`. No conversion happens.
- **NO:** Go to Step 2.

Examples:

```javascript
5 == 5       // true  (number == number)
"5" == "5"   // true  (string == string)
"5" == 5     // Different types → go to Step 2
```

## STEP 2 — Is either side `null` or `undefined`?

- **YES:** True ONLY if the other side is also `null` or `undefined`.
- `null` pairs with `undefined` — with NOTHING else (not `0`, not `""`, not `false`).
- **NO:** Go to Step 3.

Examples:

```javascript
null == undefined  // true
null == null       // true
undefined == undefined // true

null == 0          // false
null == ""         // false
null == false      // false
```

## STEP 3 — Is either side a boolean?

- **YES:** Convert the boolean into a number:
  - `true` → `1`
  - `false` → `0`
- RESTART from Step 1.
- **NO:** Go to Step 4.

Examples:

```javascript
true == 1       // true  (true → 1)
false == 0      // true  (false → 0)
true == "1"     // true  (true → 1, then "1" → 1)
false == ""     // true  (false → 0, "" → 0)
true == "hello" // false (true → 1, "hello" → NaN)
```

## STEP 4 — Is one side a number and the other a string?

- **YES:** Convert the STRING into a number.
- RESTART from Step 1.
- **NO:** Go to Step 5.

Examples:

```javascript
5 == "5"       // true  ("5" → 5)
10 == "10"     // true  ("10" → 10)
0 == ""        // true  ("" → 0)
0 == "hello"   // false ("hello" → NaN)
5 == "05"      // true  ("05" → 5)
```

## STEP 5 — Is either side an object? (Arrays are objects too!)

- **YES:** Convert the object into a primitive value.
  - First, try `valueOf()`.
  - If that doesn't return a primitive, try `toString()`.
  - An array's `toString()` behaves like `.join(",")`.
    - `[]` → `""`
    - `[1,2]` → `"1,2"`
- RESTART from Step 1.
- **NO:** Go to Step 6.

Examples:

```javascript
[] == ""          // true  ([] → "")
[] == 0           // true  ([] → "" → 0)
[5] == 5          // true  ([5] → "5" → 5)
[1,2] == "1,2"    // true  ([1,2] → "1,2")
[1,2] == 12       // false ("1,2" → NaN)
{} == "[object Object]" // true (object → "[object Object]")
```

## STEP 6 — No rule applies?

- You have reached the end of the applicable cases.
- The comparison is false for the remaining primitive type combinations.

Example:

```javascript
Symbol() == 5  // false
```

---

## Quick Revision Table

| Expression | Result | Why? |
|---|---|---|
| `5 == "5"` | `true` | String → number |
| `true == 1` | `true` | Boolean → number |
| `false == ""` | `true` | Boolean → 0, string → 0 |
| `null == 0` | `false` | Null only matches null/undefined |
| `[] == 0` | `true` | Array → "" → 0 |
| `[5] == 5` | `true` | Array → "5" → 5 |
| `[1,2] == 12` | `false` | "1,2" → NaN |

## Final Takeaway

**Remember:** `==` doesn't blindly convert everything into the same type.

It follows a specific order of rules. Whenever a conversion happens, RESTART the comparison from Step 1.

**Bonus:** Prefer `===` in everyday JavaScript because it avoids implicit type conversion and makes comparisons more predictable.

**Drills — run the checklist yourself, then check:**

```js
"" == 0;        // STEP 1 no, STEP 2 no, STEP 3 no, STEP 4: ""→0, START: 0 == 0 → true
"1" == true;    // STEP 3: true→1. RESTART. STEP 4: "1"→1. → 1 == 1 → true
"2" == true;    // STEP 3: true→1. STEP 4: "2"→2. → 2 == 1 → false!!
[1,2] == "1,2"; // STEP 5: [1,2].toString() = "1,2" → STEP 1: same string tag → true
[null] == 0;    // STEP 5: [null].toString() = "" → STEP 4: ""→0 → true
NaN == NaN;     // STEP 1: same tag (both number)... but NaN REFUSES all equality by definition → false
null == 0;      // STEP 2 fires: false — null pairs with undefined only
null == undefined; // STEP 2 fires: true
"true" == true; // STEP 3: true→1. STEP 4: "true"→NaN. → NaN == 1 → false (the classic trap)
```

Notice `NaN`: the checklist would reach "same tags, compare like ===" — but NaN is the one value the equality *rules* say no to, always. (Why: Atom 1.2.6 — IEEE 754 says an "invalid number" cannot equal anything, and JS chose to inherit that rule.)

**The debugging side — when an equality comparison fails in production, classify the symptom:**

| Symptom | Usually the cause | The debug move |
|---|---|---|
| Comparison silently never true | Type mismatch you didn't notice — `"0" === 0`, `"null"` vs `null` | `console.log(typeof a, typeof b)` FIRST, always |
| `==` gave a **surprising true** | A string got converted (`"" == 0`, `"\n" == 0`, `[] == false`) | Re-run the checklist step by step by hand |
| `==` gave a **surprising false** | Boolean on one side (`"true" == true` → false) or NaN | Same — checklist shows the boolean→number step |
| Object comparison fails | Address comparison — different objects (Atom 1.2.2) | Don't compare identity; compare a field like `a.id === b.id` |

**The fix playbook — three real-world patterns:**

```js
// BUG PATTERN 1 — type mismatch from the outside world (the expiry "0" bug)
// Fix: convert at the boundary, once, then === forever
const expiryNum = Number(apiResponse.expiry);      // one place, deliberate
if (expiryNum === 0) refresh();

// BUG PATTERN 2 — "missing" vs "falsy" confusion
// Fix: name what you mean. One idiomatic == exists:
if (input == null) { ... }   // exactly "input is null OR undefined", nothing else
// never false for 0 / "" / NaN — it compares ONLY against null and undefined

// BUG PATTERN 3 — you wrote == null, and later someone "fixed" it to === null
// Fix: keep the ==, add a comment that names the intent:
// `input == null` — DELIBERATE: covers undefined (missing key) AND null (explicit empty)
```

And the special-case quiz that wrecks people — **relational operators are a DIFFERENT algorithm** (numbers only, no special null case):

```js
null == 0;   // false (checklist step 2: null pairs with undefined only)
null >= 0;   // true!  relational: both sides → numbers → null becomes 0 → 0 >= 0
null > 0;    // false → 0 > 0
```

**Checklist recap to recite:** *same tags → ===; null/undefined pair only with each other; boolean → number first, restart; number-vs-string → string becomes number; object → primitive, restart.*

#### The Gotchas

- **Boolean converts FIRST, before anything else** — this single fact explains `"1" == true` (true) AND `"true" == true` (false). Both start with true → 1.
- **NaN is unfixable by conversion** — `Number("blah") → NaN` and then *every comparison against it fails*, including `NaN == NaN`. If a numeric comparison mysteriously never fires, check for a NaN feed: `Number.isNaN(x)`.
- **`null == 0` is false but `null >= 0` is true** — two different algorithms. `==` has a special null-pairing rule; `>=` coerces null to 0. Writing tests for exactly this triple is worth an afternoon, once.
- **`[] == ""` is true, `[] == []` is false** — first one went through the checklist (STEP 5 → `.toString()` is `""`, then number comparison with 0); second one is plain address comparison from Atom 1.2.2. Objects equal only themselves.
- **Don't rewrite legacy `x == null` into `x === null`** — the original deliberately accepts undefined too; your "fix" changes behavior and silently breaks tests that pass `undefined`.

#### Interview-Shaped Questions

1. **"What does `==` actually do vs `===`?"**
   *"`===` compares type tags and rejects mismatches with zero conversion. `==` compare same-tag values identically, and when tags differ it runs a fixed translation ladder: null/undefined pair only with each other, boolean becomes a number FIRST, string becomes a number, object becomes a primitive, re-running the ladder after each step."*

2. **"Walk me through `[] == false` — out loud, with steps."**
   Boolean first: false → 0. Array → primitive: `[].toString() = ""`. String → number: `"" → 0`. Result: `0 == 0` → true. Say the steps explicitly — that's what they're actually testing.

3. **"Why is `null >= 0` true but `null == 0` false?"**
   Relational operators coerce both sides to numbers — null becomes 0. Coercive equality treats null as a unique value that pairs only with undefined. Two algorithms, one value.

4. **"When would you still WRITE `==`?"**
   Only deliberately, for the null idiom: `x == null` catches both null and undefined as "no value here" — nothing else gets caught accidentally. It's the one `==` use senior codebases accept, usually with a comment.

---

### Atom 1.2.4 — Truthy/falsy — the exact list of 8

#### The Problem

Truthiness is where "it works but is wrong" bugs hide, because the *data* never looks broken. Three real failures, all from one habit — using `if (value)` when you mean something more precise:

```js
// FAILURE 1 — valid-but-falsy counts as missing
renderCount(0); // with: if (count) → prints "No items". 0 IS a count.

// FAILURE 2 — you guard against the wrong emptiness
const userNames = [];
if (userNames) render(userNames);        // array is ALWAYS truthy → renders empty UI, no error

// FAILURE 3 — React renders the guard value itself
{count && <Badge count={count} />}       // count = 0 → React renders a naked 0 on screen
```

The scary part: FAILURE 2 produces an *empty*, not-more-broken, UI. No exception. Nobody files a bug — they just see a blank card. This is why the "exact list" matters: you can't diagnose a `0`-swallowed-as-missing bug without knowing the falsy roster cold.

#### The Mental Model

> Truthiness is not about importance, presence, or "having data" — it's one narrow question: **what does this value become when it's pushed through a boolean slot?** Boolean slots are `if (…)`, `&&`, `||`, `!`, ternaries. The conversion has a tiny fixed guest list: **8 values** come out `false` — `false`, `0`/`-0`, `NaN`, `0n`, `""`, `null`, `undefined`, `document.all` — and *everything else* comes out `true`. Crucially, one whole tag never even applies: objects (including empty-ish things like `[]` and `{}`) are structurally outside the guest list. Shoot: don't ask "does my data exist" — ask "which of those 8 is my value, or is it none of them?"

**One-liner:** *8 values are falsy, in a boolean slot; every object — even `[]` and `{}` — is truthy, every time.*

#### The Explanation — memorize the list as a structural statement

```text
THE 8 FALSY VALUES, by tag:
  boolean   → false
  number    → 0, -0, NaN          (2 of 3 are the same "zero family"; NaN is defined-invalid)
  bigint    → 0n
  string    → "" ONLY             (even " " and "0" are truthy!)
  object    → NEVER falsy         ([], {}, function(){} — all truthy)
  null      → always falsy
  undefined → always falsy
  document.all → falsy (a legacy IE relic — even typeof document.all === "undefined")
```

Recite these three facts instead of trying to list unordered: *`""` is the only falsy string; null/undefined are always falsy; objects are never falsy.* That covers all 8 between them.

**Now the debugging side — an if-behaves-wrongly procedure, 3 steps:**

```text
STEP 1 — What IS the value? console.log it with its tag:
         console.log(value, typeof value)
         This kills 90% of confusion — the surprise is usually: you assumed number,
         it's a string ("0" is TRUTHY — only "" is falsy among strings).

STEP 2 — Does the value sit on the falsy list?
         If YES → your if/&&/! branch took the false path, and it's NOT a bug —
         but decide: is that path correct for THIS value? (0 is a real count!)

STEP 3 — Rewrite the condition to state your actual INTENT, not truthiness:
         "is it missing?"            → x == null            (null or undefined only)
         "is it an empty string?"    → x === ""
         "is it zero?"               → x === 0
         "are there items?"          → x.length > 0         (arrays)
         "does it have any keys?"    → Object.keys(x).length > 0
         "does the property exist?"  → 'id' in obj  (or  obj?.id != null)
```

The single move of STEP 3: **stop testing what the value converts to; test what the value is.** Every bug in the failure list at the top is from testing conversion instead of meaning.

Practice by re-fixing the three failures:

```js
// Fix 1 — 0 is a real count; null/undefined mean missing:
if (count != null) return `${count} items`;
// (== null deliberately — Atom 1.2.3 notes why this is the ONE idiomatic ==)

// Fix 2 — arrays never fail the if, so you can't guard via truthiness — test emptiness:
if (userNames.length > 0) render(userNames);

// Fix 3 — React: && returns the falsy operand itself; 0 escapes the guard and renders
{count > 0 && <Badge count={count} />}          // boolean-only guard
{count ? <Badge count={count} /> : null}        // ternary — anything falsy-unwanted renders null
```

Why Fix 3 works: `&&`/`||` don't return booleans — they return **the last operand evaluated** (from Atom 1.2.2's "return the operands" list). `0 && anything` evaluates to `0`, React receives the number 0, and React renders any value that isn't `false`/`null`/`undefined`. So the fix has two styles: make the guard produce a boolean (`count > 0`) or make the fallback produce nothing visible (`count ? … : null`).

#### The Gotchas

- **`""` falsy, `"0"` truthy, `[]` truthy** — the exact trio that trips people who memorize the list *unordered* instead of learning the tag rule: strings only go falsy when *empty*; objects never go falsy at all.
- **`if (arr)` succeeds even for an empty array** — the array itself is the truthy thing, not its contents. If you meant "has items", write `arr.length > 0`.
- **`document.all` is the 8th falsy value and `typeof document.all === "undefined"`** — IE-era relic. Ignore it in practice, but knowing it beats confidently saying "six falsy values" in an interview.
- **`if (x)` never checks whether "x is good data"** — it only asks which of the 8 slot-values `x` converts to. A missing variable (`undefined`) and an empty container (`[]`) take opposite paths purely because of their tags, not their contents.
- **A `0 && guard` slipped into JSX is one of the highest-frequency React bugs** — it passes code review, because the bug renders where nobody looks: DOM text `0`, invisible in dev but a live bug once data has zeros. Prefer boolean-only operands or ternaries in JSX guards everywhere.

#### Interview-Shaped Questions

1. **"Name every falsy value."**
   `false` (boolean), `0`/`-0`, `NaN` (number), `0n` (bigint), `""` (string), `null`, `undefined`, and the legacy `document.all`. Everything else is truthy — including all objects, even empty `[]` and `{}`.

2. **"Why can't `if (userNames)` guard an array?"**
   Arrays are objects and objects are never falsy — empty or not. The guard tests the *array reference's truthiness*, which is always true. Guard contents instead: `userNames.length > 0` — test emptiness, not truthiness.

3. **"Why does `{count && <Badge />}` render a 0 in the DOM when count is 0?"**
   `&&` returns the last operand evaluated — `0` escapes the short-circuit as the number 0, and React renders any value that isn't `false`/`null`/`undefined`. Fix by making the guard boolean-only (`count > 0 && …`) or using a ternary with explicit `: null`.

4. **"`if (count)` broke in production. Walk me through your debugging."**
   Log `typeof count` first — most surprises are type surprises (`"0"` string vs `0` number). Check the falsy list to confirm what the branch actually did. Then rewrite the condition to state intent: `count != null` to test presence, `count === 0` to specifically mean zero — never test truthiness when you mean a value.

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

**For atoms 1.2.3 and 1.2.4:** the gotchas live inside each atom's section (post-rewrite) — no global duplicates here.

**The one capstone gotcha that spans all four atoms:** everything in this unit is the *tag* deciding behavior. `typeof` reads tags (1.2.1); tags decide copy-vs-share (1.2.2); tags decide whether `==` needs conversion (1.2.3); tags decide the falsy list (1.2.4). When any type behavior surprises you, ask "What is the *tag* here?" — before guessing about the value.

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

*From atoms 1.2.3 and 1.2.4 (post-rewrite): full interview Q&As live inside each atom's section — equality solver's checklist, `null >= 0` vs `null == 0`, the falsy roster, and the debugging walkthroughs for `if (count)` and JSX 0-render bugs.*

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