# Unit 1.1 — The Execution Model (Part 1)

> **Why this exists.** React is a library, not a language. Almost every "React bug" is actually a JavaScript misunderstanding — stale closures, reference equality, `this` binding, unhandled promise rejection. Engineers who learn React without learning JavaScript hit a ceiling in about eight months and can never debug anything the tutorial didn't cover. Also: JS is the most-interviewed frontend topic and the one where tier-3 candidates are most obviously exposed.

> **Part 1 of 2 — Atoms 1.1.1 → 1.1.4.** *How code runs and what it can see.* Closures, memory leaks and modules are in `01-01-the-execution-model-part2.md`.

## The Problem This Solves

Before 1995, web pages were static documents. You could read them, but you couldn't interact with them. If you wanted a button to change text, you had to send a request back to the server and reload the entire page.

JavaScript was invented to solve one problem: **interactivity in the browser without requiring a server round-trip for every user action.**

JavaScript's design constraints (single-threaded, event-driven, prototype-based) are NOT obvious if you come from C#. These constraints create the entire landscape of React bugs, async bugs, and interview trick questions. If you don't understand *why* JS works this way, you'll memorize syntax without understanding behavior.

## The Mental Model

JavaScript is like a play rehearsal. Before the actors start performing (execution phase), the director reads through the entire script and assigns roles — "You're Hamlet, you're Ophelia, you're the ghost" (creation phase). By the time the play starts, everyone knows who they are, even though some characters don't appear until Act 3. **Hoisting** is that role assignment happening before performance begins.

---

## The Details

Each atom below is self-contained: the explanation, the code, the gotchas, and the interview questions for a topic all live in one place.

---

### Atom 1.1.1 — How JavaScript Actually Runs

#### The Explanation

JavaScript doesn't just run line by line. There are **three distinct phases** before a single line of your code executes:

```
Your Code → 1. Parsing (syntax check) → 2. Creation Phase → 3. Execution Phase → Result
```

**Phase 1: Parsing**
The engine reads your code. If there's a syntax error (like a missing bracket), it stops here. Nothing runs.

**Phase 2: Creation (This is where hoisting happens)**
The engine scans through ALL your code and does three things:

1. **For `var` declarations**: Allocates memory and initializes them as `undefined`
2. **For `function` declarations**: Allocates memory AND stores the entire function body
3. **For `let`/`const` declarations**: Allocates memory but does NOT initialize them — they enter the "Temporal Dead Zone" (TDZ)

**Phase 3: Execution**
Now it runs line by line, assigning values and executing code.

```javascript
// PHASE 2 already happened — memory is allocated
console.log(name);  // undefined (var is hoisted with undefined)
var name = "Alice";

console.log(age);   // ReferenceError! (let is hoisted but TDZ)
let age = 30;

greet();            // Works! Function declaration is fully hoisted
function greet() {
  console.log("hello");
}
```

**What's actually happening in memory:**

```
┌─────────────────────────────────────────────────┐
│  name  →  undefined                             │  (var declaration)
│  age   →  [in TDZ, cannot access]               │  (let declaration)
│  greet →  function greet() { ... }              │  (function declaration)
└─────────────────────────────────────────────────┘
```

Now Phase 3 runs line by line:
- `console.log(name)` → reads `undefined` from memory ✓
- `name = "Alice"` → updates the value ✓
- `console.log(age)` → tries to read but TDZ → **ReferenceError!** ✗
- `greet()` → calls the stored function ✓

**Hoisting doesn't move code.** The code stays where it is. Only the declarations are processed first. It's like a table of contents — the chapters don't move, but you know what's coming.

#### Gotchas — Atom 1.1.1

1. **Hoisting is declaration-only, not code movement.** A common misconception is that `greet()` "moves up" to the top of the file. Nothing moved — the *function body* was already in memory before Phase 3 began.

2. **Function expressions are NOT hoisted (if using `var`):**
   ```javascript
   sayHi(); // TypeError: sayHi is not a function

   var sayHi = function() {
     console.log("hi");
   };
   ```
   `sayHi` is hoisted as `undefined`, so calling `undefined()` gives TypeError, not ReferenceError.

3. **`typeof` doesn't throw on undeclared variables but DOES throw on TDZ:**
   ```javascript
   console.log(typeof undeclared); // "undefined" — no error
   console.log(typeof letVar);     // ReferenceError — TDZ
   let letVar = 5;
   ```

#### Interview Questions — Atom 1.1.1

1. **"Why does `console.log(x)` before `var x = 5` give `undefined` instead of ReferenceError?"**
   Because during the creation phase, `var` declarations are hoisted and initialized as `undefined`. By the time execution reaches `console.log(x)`, the variable exists in memory with value `undefined`.

2. **"Are `let` and `const` hoisted?"**
   Yes, they are hoisted during the creation phase, but they are NOT initialized. They enter a "Temporal Dead Zone" from the start of the block until the declaration line. Accessing them during TDZ throws ReferenceError.

3. **"What's the difference between `var` and `let` hoisting?"**
   `var` is hoisted AND initialized as `undefined` — you can read it (getting `undefined`). `let`/`const` are hoisted but NOT initialized — reading them throws ReferenceError until the declaration executes.

4. **"Why does calling a hoisted function expression give `TypeError` instead of `ReferenceError`?"**
   Because the variable exists — `var` initialised it to `undefined`. `ReferenceError` means "no such binding"; `TypeError` means "binding exists but isn't callable". The distinction tells you whether the problem is scoping or the value.

---

### Atom 1.1.2 — var vs let vs const: Scope, TDZ, and Why const ≠ Immutable

#### The Explanation

**`var` — Function-scoped, redeclarable**

```javascript
function demo() {
  var x = 1;
  var x = 2;  // Fine — redeclaration allowed
  console.log(x); // 2

  if (true) {
    var y = 10; // var ignores block scope — y is visible in the whole function
  }
  console.log(y); // 10 — y "leaked" out of the if block
}
```

**`let` — Block-scoped, not redeclarable**

```javascript
function demo() {
  let x = 1;
  // let x = 2;  // SyntaxError! Cannot redeclare

  if (true) {
    let y = 10; // y only exists in this block
  }
  // console.log(y); // ReferenceError — y is gone
}
```

**`const` — Block-scoped, not redeclarable, NOT reassignable**

```javascript
const PI = 3.14159;
// PI = 3; // TypeError: Assignment to constant variable

const arr = [1, 2, 3];
arr.push(4);   // Fine! You're not reassigning arr, you're mutating the array

const obj = { name: "Alice" };
obj.name = "Bob"; // Fine! Mutating the object, not reassigning obj
// obj = {};      // TypeError: Cannot reassign
```

**The key distinction:**

```
const x = 5;       // x points to the value 5
x = 10;            // ERROR: can't change what x points to

const arr = [1,2]; // arr points to an array in memory
arr.push(3);       // OK: you're changing what the array CONTAINS, not what arr POINTS TO
```

`const` does **NOT** freeze the value. `Object.freeze(user)` does, but it's shallow — nested objects are still mutable (Atom 1.4.2).

**Why does TDZ exist?** It prevents a class of bugs where you accidentally use a variable before it has a meaningful value. With `var`, you'd get `undefined` silently. With `let`/`const`, you get an explicit error — which is better because it forces you to fix the logic.

```javascript
var secret = "before";
{
  // TDZ for inner secret
  console.log(secret); // undefined — the OUTER secret, confusing!
  let secret = "after";
}
```

Without TDZ, that `console.log` would silently read the outer variable. TDZ makes this a clear error.

#### The var Loop Puzzle — Why 3, 3, 3?

This is previewed here because it's **purely** about `var` being function-scoped. Atom 1.1.5 gives the full treatment — why `let` fixes it, and two other ways to fix it without `let`.

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3
```

`var` is function-scoped, so the whole loop shares **ONE** `i`. There aren't three `i`'s — there's only one.

```
i = 0 → schedule callback #1 ┐
i = 1 → schedule callback #2 ┼─ all three point at
i = 2 → schedule callback #3 ┘  the SAME variable
i = 3 → loop condition false, loop ends

100ms later the callbacks run. The loop is done. i === 3. All three print 3.
```

The callbacks don't capture the **value** of `i`. They capture a **reference to the variable** — and by the time they run, it holds `3`.

`let` creates a fresh binding per iteration, so each callback captures its own:

```javascript
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2
```

> **Making the loop slow does NOT fix it.** Developers add an `await` or a busy-wait inside the body to "force" per-iteration capture. Still `3, 3, 3` — the problem is scoping, not timing.

> **Forward reference.** Callbacks ("a function you pass to run later") and single-threaded execution are Atom 1.6.4 and 1.6.1/1.6.2. They're not defined here.

#### Gotchas — Atom 1.1.2

1. **`let` and `const` ARE hoisted** — people get this wrong. They're hoisted but NOT initialized. That's the Temporal Dead Zone.

2. **`const` does NOT freeze the value.** `const user = { name: "Alice" }; user.name = "Bob"` works. `user = {}` throws. Only `Object.freeze` freezes, and only one level deep.

3. **`var` in loops creates one variable shared across iterations — THIS IS THE #1 INTERVIEW TRAP.** Trace above.

4. **`await` or slowness inside the loop does not fix it.** The loop shares one `i` regardless of timing. You need `let`, or `const captured = i` inside the body.

#### Interview Questions — Atom 1.1.2

1. **"Why does `const` not mean immutable?"**
   `const` prevents reassignment of the variable binding — what the name points to. It does NOT prevent mutation of the value. So `const arr = [1,2,3]; arr.push(4)` works because you're modifying the array, not reassigning `arr`.

2. **"Why is `var` considered bad practice?"**
   `var` is function-scoped, not block-scoped. Variables "leak" out of if blocks, for loops, and other block scopes. It also allows redeclaration in the same scope.

3. **"What is the Temporal Dead Zone?"**
   The period after a `let`/`const` is hoisted but before its declaration executes. Accessing the variable during this period throws ReferenceError. It exists to prevent silent `undefined` values from causing subtle bugs.

4. **"Why does `for (var i...)` with setTimeout print 3, 3, 3?"**
   `var` is function-scoped — all callbacks share ONE `i`. By the time they execute, the loop is done and `i === 3`. `let` fixes this because each iteration gets its own binding.

5. **"If I put `await` inside a `var` loop, does it fix the 3, 3, 3 problem?"**
   No. `await` changes *when* the code runs, not *what is scoped*. The loop still shares one `i`, so once it finishes all callbacks read the final value. You need `let`, or an explicit `const captured = i` inside the body.

---

### Atom 1.1.3 — The Call Stack

#### Why the call stack exists

When function A calls function B, which calls function C, JavaScript needs to know: **when C finishes, where do I go back to?** Without this mechanism, nested function calls would lose their way. The call stack is the answer — it's JavaScript's GPS for function execution.

**The failure mode**: Developers who don't understand the call stack can't read stack traces, can't debug recursion, and don't understand why a deep enough recursion crashes with "Maximum call stack size exceeded."

#### How to think about it

Think of the call stack like a **stack of plates**. You can only add or remove from the top. When a function is called, you put a plate on the stack with that function's name. When the function finishes, you take the plate off. The plate on top is always the function currently running. The plate underneath is where you'll return to.

#### The Explanation

The call stack is a **LIFO (Last In, First Out)** data structure that tracks function execution. Each call adds a **frame**; each return removes one.

```javascript
function first()  { console.log("first start");  second(); console.log("first end"); }
function second() { console.log("second start"); third(); console.log("second end"); }
function third()  { console.log("third"); }

first();
```

The stack, step by step — push on call, pop on return:

```
start          first()        second()       third()        third done    second done
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│ global │     │ first  │ ←   │ second │ ←   │ third  │ ←   │ second │     │ first  │
└────────┘     │ global │ TOP └────────┘ TOP └────────┘ TOP └────────┘ TOP └────────┘
               └────────┘     │ global │     │ second │     │ global │     └────────┘
                             └────────┘     │ first  │     └────────┘
                                           │ global │
                                           └────────┘
```

**Output:**
```
first start
second start
third
second end
first end
```

The top frame is always the currently executing function. Nothing else about the stack is hidden machinery.

#### Stack Trace — Reading the Map

When an error occurs, JavaScript gives you a stack trace. It's a snapshot of the call stack at the moment of the error.

```javascript
function a() { b(); }
function b() { c(); }
function c() { throw new Error("oops"); }

a();
```

```
Error: oops
    at c (script.js:3)      ← where the error happened
    at b (script.js:2)      ← b called c
    at a (script.js:1)      ← a called b
    at <anonymous> (script.js:5)   ← entry point
```

**How to read it:** top = where the error happened. Bottom = where execution started. Each line is one frame. So: `a` called `b`, `b` called `c`, `c` threw.

#### Stack Overflow — When the Stack Breaks

The call stack has a **maximum size**. If you recurse without a base case, the stack fills up and crashes.

```javascript
function recurse() { recurse(); }   // no base case!
recurse();
// RangeError: Maximum call stack size exceeded
```

Each call adds a frame. They're never removed because the function never returns. Eventually the stack hits its limit (usually ~10,000–15,000 frames, engine-dependent).

**Real-world example — a forgotten base case:**

```javascript
function factorial(n) {
  return n * factorial(n - 1); // forgot n <= 1
}

factorial(5);   // Stack overflow!

// Fixed with a base case:
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
factorial(5);   // 120
```

#### Gotchas — Atom 1.1.3

1. **The stack is NOT the same as the heap.** Stack = function calls (LIFO, fast, limited). Heap = objects/data (random access, larger, GC-managed). Stack overflow ≠ memory leak — different memory region, different fix, different symptom.

2. **Async functions don't stay on the stack.** When you `await` or use callbacks, the function returns immediately and the stack unwinds. The callback runs later on a fresh stack.

3. **Stack traces only show synchronous calls.** An error inside a `setTimeout` callback won't show the code that *scheduled* it.

4. **Tail call optimization doesn't exist in most JS engines.** Even when a function's last action is calling another, the frame isn't reused (Safari under strict mode is the exception). And deep-but-legitimate recursion — walking a nested JSON tree — can blow the limit in production even though it isn't a bug. Know the iterative rewrite.

#### Interview Questions — Atom 1.1.3

1. **"What is the call stack?"**
   A LIFO data structure that tracks function execution. Each function call pushes a frame; each return pops a frame. The top frame is the currently executing function.

2. **"How do you read a stack trace?"**
   Read from top to bottom. The top is where the error occurred. Each line is a function that called the one above it. The bottom is the entry point.

3. **"What causes a stack overflow?"**
   Infinite recursion (no base case) or extremely deep recursion. Each recursive call adds a stack frame; they're never removed because the function never returns.

4. **"What's the difference between a stack overflow and a memory leak?"**
   Stack overflow is exhausting the call stack with too many nested frames — it crashes immediately and is deterministic. A memory leak is unreachable-but-wanted objects accumulating on the heap over time. Different region, different fix, different symptom.

#### Code I Wrote — Atom 1.1.3

```javascript
function trace(label) {
  console.log(`${label} — stack depth: ${getStackDepth()}`);
}

function getStackDepth() {
  try { throw new Error(); }
  catch (e) { return e.stack.split('\n').length - 3; }
}

function a() { trace("a start"); b(); trace("a end"); }
function b() { trace("b start"); c(); trace("b end"); }
function c() { trace("c"); }

a();

// Output:
// a start — stack depth: 2
// b start — stack depth: 3
// c — stack depth: 4
// b end — stack depth: 3
// a end — stack depth: 2
```

This proves you can measure the stack at runtime rather than only reasoning about it on paper — and the depth going 2 → 3 → 4 → 3 → 2 is the push/pop behaviour made observable.

---

### Atom 1.1.4 — Lexical Scope and the Scope Chain

#### The Problem This Solves

Here is a function whose creator has already finished running:

```javascript
function makeReader() {
  const secret = "local secret";
  return function read() { return secret; };
}

const reader = makeReader();   // makeReader's frame is destroyed here
reader();                      // "local secret" — still works
```

`secret` was declared inside a function that has already returned. By every rule you learned in C#, that name should be dead. It isn't. To explain why, you need to know that `read` never "went looking" for `secret` at call time — it was **wired to that scope before it ever existed as a value.**

Without understanding that scope is fixed at *write* time, you cannot answer these:

- Why does the `useEffect` in every React codebase log a stale value forever?
- Why does moving a function to a different part of a file change what it can read?
- Why does a function "remember" its birth variables even after the parent is gone?

And the interview question that separates tier-1 from tier-3 candidates:

> **"What does a closure capture?"**

Almost everyone answers *"the variable's value."* The correct answer is *"the binding — the variable itself, not a snapshot of it."* If you can't explain the difference, you don't have the model.

#### The Mental Model

Every function is born holding a fixed list of names — the variables that surround the line of code where it was **written**. It carries that list with it forever.

Calling it from somewhere else doesn't add anything to the list. Changing a variable's value doesn't update the list. The list is printed once, when the code is written down, and never reprinted.

So: **a JavaScript function carries its birthplace, not its current address.** Knowing where a function was *written* tells you everything about what it can *see*. Knowing where it was *called* tells you nothing at all.

#### The Explanation

Two rules. This is the entire atom.

**Rule 1 — The scope chain is built from where the code is _written_, once, at parse time.**

**Rule 2 — Each variable name is resolved by walking _outward_ through that chain until a match is found.**

The word for this is **lexical** scope, and it's lexical because scope follows the *letters of the source*. The engine reads your file, and for every function it writes down the list of enclosing scopes that surround that text. It never rebuilds that list.

##### The Chain, Drawn

```javascript
function outer() {
  const a = "outer a";
  function middle() {
    const b = "middle b";
    function inner() {
      console.log(a, b, c);   // ← the chain is fixed HERE, at this line
    }
    inner();
  }
  middle();
}
outer();
```

```
  console.log(a, b, c);   ← written here

   ┌───────────────────────────────────────────────┐
   │ inner()      a? no    b? no    c? no         │  1st stop
   ├───────────────────────────────────────────────┤
   │ middle()     a? no    b? YES ────────────┐   │  2nd stop
   │              c? no              │      │   │
   ├──────────────────────────────┼──────┼───┤
   │ outer()      a? YES ───────────┐   │      │   │  3rd stop
   │              (never asked) │   │   │      │   │
   ├────────────────────────────┼───┼──────┼───┤
   │ module / global scope   │   │      │   │   │  4th stop
   ├────────────────────────────┼───┼──────┼───┤
   │ globalThis ← last resort │   │      │   │   │
   │ (unreachable from ESM)  ▼   ▼      ▼   ▼   │
   └───────────────────────────────────────────────┘

  a ✓ (found in outer)   b ✓ (found in middle)   c ✗ → ReferenceError
```

Three things to read off that diagram:

1. **Each name is walked independently.** Finding `b` in `middle` does not stop the engine from continuing outward to find `a` in `outer`. They resolve separately, in their own walks.
2. **Shadowing is just "nearest wins."** If `outer` also declared a `b`, the `middle` one would win. Same name, nearer binding, done — no error, no warning.
3. **There is exactly one failure mode.** Reach the bottom without a match → `ReferenceError`. The *only* reason undeclared reads sometimes give `undefined` is Atom 1.1.1's hoisting: a `var` already parked an `undefined` in the chain.

##### Proof: Write Time, Not Call Time

```javascript
const secret = "global secret";

function read() { return secret; }          // read() was WRITTEN at top level

function makeReader() {
  const secret = "local secret";
  return read;                              // we hand over the FUNCTION, not the value
}

const reader = makeReader();
console.log(reader());                     // "global secret"
```

Most people predict `"local secret"` — the reader was *called* from inside `makeReader`, after all. It's wrong. The only question that matters is: **what does the text immediately around `read` look like?** Answer: top level. So its chain is permanently `[module scope → globalThis]`, committed when the line was parsed — before `makeReader` ever ran.

**A JavaScript function carries its birthplace, not its current address.** Passing `read` into `makeReader` and getting it back changed where it *lives*. It did not change what it can *see*.

##### Why This Design and Not The Obvious One

In a hypothetical dynamically-scoped language, this would be a compile error — the compiler can't prove `secret` exists. JavaScript makes that decision for you at parse time, using the text on screen. That is precisely what "lexical" means.

| | C# | JavaScript |
|---|---|---|
| Lambda captures | the *variables* it references | the *scope it was written in* |
| Opt out of capture | `static` local functions | impossible — always lexical |
| Decided at | compile time | parse time |

The real difference isn't *what* gets captured — it's that JS gives you **no escape hatch**. In C# a `static` lambda refuses to capture. In JavaScript every function is implicitly "static" in that sense: it only ever sees its own birth scope.

##### Block Scope in the Chain

```javascript
for (var i = 0; i < 3; i++) {}
console.log(i);        // 3

for (let i = 0; i < 3; i++) {}
console.log(i);        // ReferenceError: i is not defined
```

`var i`'s binding belongs to the enclosing function/module scope, so it outlives the loop. `let i`'s binding belongs to the loop's block, destroyed when the loop exits — so outside there is **no binding at all**. Not an `undefined` binding: *no binding*. Identical rule, different rung.

##### The Chain Can Outlive Its Creator

```javascript
function makeReader() {
  const secret = "local secret";
  return function read() { return secret; };
}
const reader = makeReader();   // makeReader's scope is now unreachable...
reader();                      // ...except through reader. Still works.
```

`read`'s chain *points at a place in the program that still has a name*. The scope it created is still reachable because something still points into it. That is a **closure** — Atom 1.1.5, in Part 2.

##### The Chain Meets the TDZ

The TDZ isn't a separate mechanism — it's a rung on the chain holding an *uninitialised* binding:

```javascript
{
  console.log(typeof count);   // ReferenceError, not "undefined"
  let count = 0;
}
```

The chain finds `count`. The rung exists. But the binding has no value yet, so reading it throws. Compare:

```javascript
console.log(typeof notDeclaredAnywhere);  // "undefined" — no error, not in chain
```

Same walk, two outcomes: **absent from the chain** vs **present but uninitialised**.

#### Prediction Exercises

Predict first, then reveal. Each one combines two atoms, which is what makes them worth doing.

**Q1 — Hoisting meets the chain**

```javascript
function findSecret() { console.log(secret); }
findSecret();
var secret = "I live at the top of the file";
```

<details><summary>Answer</summary>

**Prints `undefined`.** `var secret` hoists to module scope and parks `undefined` there (Atom 1.1.1). `findSecret` runs before the assignment line, so the chain finds a real binding holding `undefined` — not a missing one.

</details>

**Q2 — Chain walking with a hole**

```javascript
function outer() {
  const a = "outer a";
  function middle() {
    const b = "middle b";
    function inner() { console.log(a, b, c); }
    inner();
  }
  middle();
}
outer();
```

<details><summary>Answer</summary>

**`ReferenceError: c is not defined`.** `a` found in `outer`, `b` found in `middle`, `c` found nowhere. The subtle part: had `outer` declared `var c`, you'd get `undefined` instead. Same walk, different failure mode.

</details>

**Q3 — Shadowing silently**

```javascript
const total = 100;
function render() {
  const total = 5;      // different meaning entirely
  console.log(total);
}
render();                // 5
console.log(total);      // 100
```

<details><summary>Answer</summary>

Both print cleanly. No error, no warning. The inner `total` simply wins because it's nearer. If the inner one were a typo of the outer one, you'd have a genuinely hard bug in code that reads correctly. Linters flag this; your eyes won't.

</details>

#### Gotchas — Atom 1.1.4

1. **"Captures the value" is the wrong answer and it's the most common one.** A closure captures the **binding**, not a snapshot:

   ```javascript
   function counter() {
     let n = 0;
     return { inc: () => ++n, get: () => n };
   }
   const c = counter();
   c.inc(); c.inc();
   console.log(c.get());   // 2 — the binding is live, not a copy
   ```

2. **Moving a function textually changes what it can see — even if you call it from the same place as before.** Move `read` *inside* `makeReader` above and the answer flips from `"global secret"` to `"local secret"`. Nothing about the call site changed. Only the birth location.

3. **Shadowing is completely silent.** An inner `const total = 5` over an outer `total = 100` is legal, warning-free, and produces a bug that's hard to find, because the code reads correctly.

4. **The error message tells you *which kind* of chain-walk failed.** Absent from the chain → `ReferenceError`. Present but hoisted as `undefined` → `undefined`. Present but in the TDZ → `ReferenceError`. The message can't distinguish the last two, but the fix differs, so check the declaration form.

5. **Implicit globals pollute the chain in sloppy mode.** `function f() { undeclared = 5; }` succeeds in a classic script — the failed assignment walks to the bottom and *creates* a global. That bottom rung is why typos become silent cross-function bugs. Always declare.

6. **`this` is _not_ resolved by the scope chain.** It's resolved by call-site rules (Atom 1.3.2). Mixing the two up is the source of most "why is `this` undefined" confusion — and it's why arrow functions have no `this`: they inherit it from the enclosing scope chain instead.

7. **Module scope is not global scope.** In Node/CommonJS your top-level code is wrapped in a function, so top-level `var` is module-local. In ESM, top-level declarations are module-scoped and unbound names are a hard `ReferenceError`. In a classic `<script>` tag, top-level `var` **is** global, and two scripts can collide. (Atom 1.1.7.)

#### Interview Questions — Atom 1.1.4

1. **"What does a closure capture?"**
   The **binding**, not the value. A closure retains a reference to a variable in an enclosing scope. Reads and writes go to the same live variable, so mutating it inside the closure is visible outside and vice versa. Capturing a *value* would make the counter example always return `0` after an increment.

2. **"Walk me through how JavaScript resolves a variable name."**
   At parse time, the engine builds a scope chain for each piece of code from its textual nesting. At runtime, for each name, it walks outward rung by rung. The first rung containing that name wins — that's shadowing. Reaching the bottom with no match throws `ReferenceError`. Each name is walked independently.

3. **"What is the scope chain?"**
   The ordered list of scopes surrounding a piece of code, innermost to outermost, ending at the global scope. Built once from *where the code is written*, not rebuilt per call. Lookups walk it outward until the name is found.

4. **"Why does this log `0` forever?"** (the `useEffect` case)

   ```jsx
   useEffect(() => {
     const id = setInterval(() => console.log(count), 1000);
     return () => clearInterval(id);
   }, []);   // empty deps
   ```

   The interval callback was *written* during the first render, so its chain contains the first render's `count` — `0`. That chain is frozen at parse time. The empty dep array says "create this interval once," so the stale closure is never replaced.

5. **"What is shadowing, and is it a bug?"**
   An inner declaration with the same name as an outer one. The inner scope is nearer, so it wins. Legal, silent, and a common source of bugs. Not a language bug; a readability hazard.

6. **"Why does JavaScript use lexical scope instead of dynamic scope, and what do we lose?"**
   Lexical makes scope predictable from reading the source: what a function touches is visible on the page, without tracing the call graph. The cost is that capturing loop variables or `this` behaves in ways that surprise people (the 3,3,3 trap), and there's no opt-out the way C# has `static` local functions.

7. **"How do you debug a bug where a function reads the wrong variable?"**
   Check where the function is **written** first, not where it's called. That's the only thing that determines its chain. Then look for a same-named declaration in an intermediate scope (shadowing), then check whether `var` hoisting or the TDZ is involved.

#### Code I Wrote — Atom 1.1.4

*Pending — the scope-chain tracer is the proof-of-learning build for this atom. Model it on `getStackDepth` in Atom 1.1.3's Code section: a function that reports the chain of names visible at its call point, so you observe the chain instead of reasoning about it.*

---

## Atom Coverage In This File

| Atom | Topic | Sections present |
|------|-------|------------------|
| 1.1.1 | How JS runs: parsing, creation/execution, hoisting | Explanation, Gotchas, Interview Questions |
| 1.1.2 | `var` vs `let` vs `const`, TDZ, the loop puzzle | Explanation, Gotchas, Interview Questions |
| 1.1.3 | Call stack, stack trace, stack overflow | Explanation, Gotchas, Interview Questions, Code I Wrote |
| 1.1.4 | Lexical scope and the scope chain | Explanation, Prediction Exercises, Gotchas, Interview Questions |

**Gaps:**
- Atom 1.1.1, 1.1.2, 1.1.4 have no "Code I Wrote" section — no proof build written yet
- Atom 1.1.4 teach-back not yet done; left at `In Progress` in PROGRESS.md
- Callbacks and single-threaded execution were cut from Atom 1.1.2's old "Deep Dive" — they belong to Atom 1.6.1 and 1.6.4, where they'll be formalised

---

## Next: `01-01-the-execution-model-part2.md` — Atoms 1.1.5 → 1.1.7

You have the machine: phases, hoisting, TDZ, the call stack, and lexical scope. Part 2 covers what a function *keeps alive* — closures, why retention becomes a leak, and why IIFEs existed to fake module scope.