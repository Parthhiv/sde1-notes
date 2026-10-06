# Unit 1.1 — The Execution Model (Part 1)

> **Why this exists.** React is a library, not a language. Almost every "React bug" is actually a JavaScript misunderstanding — stale closures, reference equality, `this` binding, unhandled promise rejection. Engineers who learn React without learning JavaScript hit a ceiling in about eight months and can never debug anything the tutorial didn't cover. Also: JS is the most-interviewed frontend topic and the one where tier-3 candidates are most obviously exposed.

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
The engine scans through ALL your code and does two things:

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

**What's Actually Happening in Memory:**

After Phase 2 (Creation), your code's memory looks like this:

```
┌─────────────────────────────────────────────────┐
│  name  →  undefined                             │  (var declaration)
│  age   →  [in TDZ, cannot access]               │  (let declaration)
│  greet  →  function greet() { ... }             │  (function declaration)
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

2. **Function expressions are NOT hoisted (if using var):**
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
   Yes, they are hoisted during creation phase, but they are NOT initialized. They enter a "Temporal Dead Zone" from the start of the block until the declaration line. Accessing them during TDZ throws ReferenceError.

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
console.log(arr); // [1, 2, 3, 4]

const obj = { name: "Alice" };
obj.name = "Bob"; // Fine! Mutating the object, not reassigning obj
obj.age = 30;     // Fine! Adding a new property
// obj = {};      // TypeError: Cannot reassign
```

**The key distinction:**

```
const x = 5;       // x points to the value 5
x = 10;            // ERROR: can't change what x points to

const arr = [1,2]; // arr points to an array in memory
arr.push(3);       // OK: you're changing what the array CONTAINS, not what arr POINTS TO
```

**`const` does NOT freeze the value.** To truly freeze: `Object.freeze(user)` — but that's shallow (nested objects are still mutable). See Atom 1.4.2 for property descriptors and the shallowness of `freeze`.

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

#### Deep Dive — Callbacks, the var Loop Puzzle, and Single-Threaded Execution

> **Placement note.** This deep dive lived loose between Atom 1.1.2 and Atom 1.1.3. It belongs with Atom 1.1.2 because the loop puzzle is *purely* about `var` being function-scoped. The callback and single-threading sections are early previews of Atom 1.6.1 (why async exists) and Atom 1.6.4 (callbacks and inversion of control) — you'll formalise them there.

##### What is a Callback?

A **callback** is a function you pass to another function to be executed **later**, not right now.

```javascript
// Regular function call — executes immediately
function greet() {
  console.log("hello");
}
greet(); // runs NOW

// Callback — passed as an argument, runs LATER
setTimeout(function() {
  console.log("hello");
}, 1000); // runs AFTER 1000ms
```

**Real-world analogy:**

You order food at a restaurant. You don't stand in the kitchen watching them cook. You give them your order (the callback function) and say "call me when it's ready." You go sit down, and when the food is ready, they come get you.

The callback = "when the food is ready, do this."

**Common callbacks you'll see:**

```javascript
// Button click — run this WHEN the user clicks
button.addEventListener("click", function() {
  console.log("clicked");
});

// After fetch completes — run this WHEN data arrives
fetch("/api/data").then(function(data) {
  console.log(data);
});

// After time passes — run this WHEN 1000ms have elapsed
setTimeout(function() {
  console.log("done");
}, 1000);
```

##### The var Loop Problem — Why 3, 3, 3?

**The Key Insight:** `var` is **function-scoped**, not block-scoped. That means the entire `for` loop shares **ONE** `i` variable. There aren't three `i`'s — there's only one.

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3
```

**Step-by-Step Execution:**

```
Step 1: var i = 0;
        setTimeout(() => console.log(i), 100);  // schedules callback #1

Step 2: i becomes 1 (i++)
        setTimeout(() => console.log(i), 100);  // schedules callback #2

Step 3: i becomes 2 (i++)
        setTimeout(() => console.log(i), 100);  // schedules callback #3

Step 4: i becomes 3 (i++)
        Loop condition: 3 < 3 is FALSE → loop stops

NOW: All three callbacks execute (after 100ms)
     But the loop is done. i === 3.
     All three callbacks share the SAME i.
     So all three print 3.
```

**Visual: One `i`, Three Callbacks**

```
┌─────────────────────────────────────────────┐
│  Function scope (one var i)                 │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  for loop                           │    │
│  │                                     │    │
│  │  i = 0 → callback #1 ──┐           │    │
│  │  i = 1 → callback #2 ──┼── all    │    │
│  │  i = 2 → callback #3 ──┘   point  │    │
│  │                              to   │    │
│  │  i = 3 → loop ends         same  │    │
│  │                         ┌────┘    │    │
│  │                         ▼         │    │
│  │                      var i        │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

The callbacks don't capture the **value** of `i` at scheduling time. They capture a **reference** to the variable `i` itself. When they finally execute 100ms later, they read the current value of that variable — which is `3`.

**Even with a slow loop, it's still 3, 3, 3:**

```javascript
function slowLoop() {
  for (var i = 0; i < 3; i++) {
    // Simulate slow code
    let start = Date.now();
    while (Date.now() - start < 500) {} // busy wait 500ms

    setTimeout(() => console.log(i), 0);
  }
}
// Output: 3, 3, 3 (still!)
```

Why? Because even though the loop is slow, `var` still creates ONE variable. The callbacks still share the same `i`. The slowness doesn't change the scoping. The loop completes before any callbacks execute, so `i` is always `3`.

##### Why `let` Gives You 0, 1, 2

`let` is **block-scoped**. Each iteration of the loop creates a **brand new** `i` variable:

```javascript
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2
```

**What happens in memory:**

```
Iteration 1: creates NEW i (value: 0)
             callback #1 captures THIS i

Iteration 2: creates NEW i (value: 1)
             callback #2 captures THIS i

Iteration 3: creates NEW i (value: 2)
             callback #3 captures THIS i

Loop ends. Three separate i variables exist.
Each callback reads its own i → 0, 1, 2
```

**The Core Difference:**

```
var:  ONE variable, THREE references to it
let:  THREE variables, each callback has its own
```

> **Forward reference.** "What exactly is retained in memory" is the subject of Atom 1.1.5 (Closures). The one-line version: the callback retains the *variable binding*, not a snapshot of its value.

##### JavaScript is Single-Threaded

JavaScript has **one call stack** and **one thread**. It can only do one thing at a time. When it hits `setTimeout`, it doesn't pause — it schedules the callback and moves on.

```
┌─────────────────────────────────────────────────────┐
│  JavaScript (one thread)                            │
│                                                     │
│  1. Run loop iteration 0                            │
│  2. Schedule callback (don't run it yet)            │
│  3. Run loop iteration 1                            │
│  4. Schedule callback (don't run it yet)            │
│  5. Run loop iteration 2                            │
│  6. Schedule callback (don't run it yet)            │
│  7. Loop ends                                       │
│  8. NOW run all three callbacks (they're all "ready")│
└─────────────────────────────────────────────────────┘
```

The `setTimeout` with `0` delay doesn't mean "run immediately" — it means "run after the current code finishes." The full mechanism (task queue vs microtask queue) is Atom 1.6.2.

#### Gotchas — Atom 1.1.2

1. **`let` and `const` ARE hoisted** — people get this wrong. They're hoisted but NOT initialized. That's the Temporal Dead Zone.

2. **`const` does NOT freeze the value:**
   ```javascript
   const user = { name: "Alice" };
   user.name = "Bob";    // Works! Object is mutated
   user = { name: "X" }; // TypeError: can't reassign
   ```

3. **`var` in loops creates one variable shared across iterations — THIS IS THE #1 INTERVIEW TRAP:**
   ```javascript
   for (var i = 0; i < 3; i++) {
     setTimeout(() => console.log(i), 100);
   }
   // Output: 3, 3, 3
   ```
   Full trace in the Deep Dive above.

4. **Making the loop slow does NOT fix it.** Developers try adding an async operation inside the loop to "force" per-iteration capture. It still prints 3, 3, 3 — the problem is scoping, not timing. See the `slowLoop()` example above.

5. **`const` on an object doesn't make its properties read-only.** `Object.freeze` does, and even that is only one level deep.

#### Interview Questions — Atom 1.1.2

1. **"Why does `const` not mean immutable?"**
   `const` prevents reassignment of the variable binding — what the name points to. It does NOT prevent mutation of the value. So `const arr = [1,2,3]; arr.push(4)` works because you're modifying the array, not reassigning `arr`.

2. **"Why is `var` considered bad practice?"**
   `var` is function-scoped, not block-scoped. This means variables "leak" out of if blocks, for loops, and other block scopes. It also allows redeclaration in the same scope.

3. **"What is the Temporal Dead Zone?"**
   The TDZ is the period after a `let`/`const` is hoisted but before its declaration executes. During this period, accessing the variable throws ReferenceError. It exists to prevent silent `undefined` values from causing subtle bugs.

4. **"Why does `for (var i...)` with setTimeout print 3, 3, 3?"**
   `var` is function-scoped — all callbacks share ONE `i`. By the time they execute, the loop is done and `i === 3`. `let` fixes this because each iteration gets its own `i` binding.

5. **"What exactly does the callback capture — the value of `i` or the variable?"**
   The variable (the binding). `setTimeout` stores the arrow function, and that function closes over the scope where it was written. Since all three closures were written in the same function scope, they all read the same `i`. `let` fixes this by creating a new scope per iteration.

6. **"If I put `await` inside a `var` loop, does it fix the 3, 3, 3 problem?"**
   No. `await` changes *when* the code runs, not *what is scoped*. The loop still shares one `i`, so once the loop finishes all callbacks read the final value. You need `let`, or an explicit `const captured = i` inside the body.

---

### Atom 1.1.3 — The Call Stack

#### Why the call stack exists

When function A calls function B, which calls function C, JavaScript needs to know: **when C finishes, where do I go back to?** Without this mechanism, nested function calls would lose their way. The call stack is the answer — it's JavaScript's GPS for function execution.

**The failure mode**: Developers who don't understand the call stack can't read stack traces, can't debug recursion, and don't understand why a deep enough recursion crashes with "Maximum call stack size exceeded."

#### How to think about it

Think of the call stack like a **stack of plates**. You can only add or remove from the top. When a function is called, you put a plate on the stack with that function's name. When the function finishes, you take the plate off. The plate on top is always the function currently running. The plate underneath is where you'll return to.

#### The Explanation

The call stack is a **LIFO (Last In, First Out)** data structure that tracks function execution.

```javascript
function first() {
  console.log("first start");
  second();
  console.log("first end");
}

function second() {
  console.log("second start");
  third();
  console.log("second end");
}

function third() {
  console.log("third");
}

first();
```

**What happens step by step:**

```
┌─────────────────────────────────────────────┐
│  Stack at start (global)                    │
│  ┌─────────────────────────────────────┐   │
│  │ global                              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

first() is called:
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐   │
│  │ first()          ← TOP (running)   │   │
│  │ global                              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

first() calls second():
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐   │
│  │ second()        ← TOP (running)    │   │
│  │ first()                         │   │
│  │ global                              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

second() calls third():
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐   │
│  │ third()          ← TOP (running)   │   │
│  │ second()                        │   │
│  │ first()                         │   │
│  │ global                              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

third() finishes (no more calls):
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐   │
│  │ second()        ← TOP (resumes)    │   │
│  │ first()                         │   │
│  │ global                              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

second() finishes:
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐   │
│  │ first()          ← TOP (resumes)   │   │
│  │ global                              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

first() finishes:
┌─────────────────────────────────────────────┐
│  ┌─────────────────────────────────────┐   │
│  │ global         ← TOP (resumes)     │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Output:**
```
first start
second start
third
second end
first end
```

Each function call adds a **frame** to the stack. Each return removes a frame. The top frame is always the currently executing function.

#### Stack Trace — Reading the Map

When an error occurs, JavaScript gives you a stack trace. It's a snapshot of the call stack at the moment of the error.

```javascript
function a() { b(); }
function b() { c(); }
function c() { throw new Error("oops"); }

a();
```

**Stack trace:**
```
Error: oops
    at c (script.js:3)
    at b (script.js:2)
    at a (script.js:1)
    at <anonymous> (script.js:5)
```

**How to read it:**
- **Top** = where the error happened (most recent call)
- **Bottom** = where execution started
- Each line = one stack frame

This tells you: `a` called `b`, `b` called `c`, and `c` threw the error.

#### Stack Overflow — When the Stack Breaks

The call stack has a **maximum size**. If you recurse without a base case, the stack fills up and crashes.

```javascript
function recurse() {
  recurse(); // no base case!
}

recurse();
// RangeError: Maximum call stack size exceeded
```

Each `recurse()` call adds a frame. They never get removed because the function never returns. Eventually the stack hits its limit (usually ~10,000-15,000 frames depending on the engine).

**Real-world example — infinite recursion in a bug:**

```javascript
function factorial(n) {
  return n * factorial(n - 1); // forgot the base case!
}

factorial(5); // Stack overflow!
```

**Fixed with base case:**

```javascript
function factorial(n) {
  if (n <= 1) return 1; // base case — stops the recursion
  return n * factorial(n - 1);
}

factorial(5); // 120
```

#### Tracing Through a Stack Overflow

```
recurse() → stack: [recurse, recurse, recurse, ...]
                       ↑
                    keeps growing
                       ↑
              eventually hits limit
                       ↑
              RangeError thrown
```

The engine literally runs out of memory to store more frames.

#### Gotchas — Atom 1.1.3

1. **The stack is NOT the same as the heap.** Stack = function calls (LIFO, fast, limited size). Heap = objects/data (random access, larger, managed by GC). Stack overflow ≠ memory leak.

2. **Async functions don't stay on the stack.** When you `await` or use callbacks, the function returns immediately and the stack unwinds. The callback runs later on a fresh stack.

3. **Stack traces only show synchronous calls.** If an error happens in a `setTimeout` callback, the trace won't show the code that *scheduled* the callback.

4. **Tail call optimization doesn't exist in most JS engines.** Even if a function's last action is calling another function, the stack frame isn't reused (except in Safari with strict mode).

5. **The frame limit is engine- and environment-dependent.** "~10,000 frames" is a rule of thumb for browsers. Deep-but-legitimate recursion (e.g. walking a deeply nested JSON tree) can blow it in production even though it's not a bug — know the iterative alternative.

#### Interview Questions — Atom 1.1.3

1. **"What is the call stack?"**
   A LIFO data structure that tracks function execution. Each function call pushes a frame; each return pops a frame. The top frame is the currently executing function.

2. **"How do you read a stack trace?"**
   Read from top to bottom. The top is where the error occurred. Each line is a function that called the one above it. The bottom is the entry point.

3. **"What causes a stack overflow?"**
   Infinite recursion (no base case) or extremely deep recursion. Each recursive call adds a stack frame; they're never removed because the function never returns.

4. **"Why doesn't `setTimeout` show up in a stack trace?"**
   `setTimeout` schedules a callback to run later. The scheduling function returns immediately and the stack unwinds. When the callback runs later, it's on a completely new stack with no connection to the original caller.

5. **"What's the difference between a stack overflow and a memory leak?"**
   Stack overflow is exhausting the call stack with too many nested frames — it crashes immediately and is deterministic. A memory leak is unreachable-or-unwanted objects accumulating on the heap over time. Different memory region, different fix, different symptom.

#### Code I Wrote — Atom 1.1.3

##### Tracing Stack Frames Manually

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
  return function read() {
    return secret;
  };
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
  │ outer()      a? YES ───────────┐   │      │  3rd stop
  │              (never asked) │   │      │   │
  ├────────────────────────────┼───┼──────┼───┤
  │ module / global scope   │   │      │   │  4th stop
  │           nothing relevant   │      │   │
  ├────────────────────────────┼───┼──────┼───┤
  │ globalThis ← last resort │   │      │   │
  │ (unreachable from ESM)  ▼   ▼      ▼   ▼   │
  └───────────────────────────────────────────────┘

 a ✓ (found in outer)   b ✓ (found in middle)   c ✗ → ReferenceError
```

Three things to read off that diagram:

1. **Each name is walked independently.** Finding `b` in `middle` does not stop the engine from continuing outward to find `a` in `outer`. They resolve separately, in their own walks.
2. **Shadowing is just "nearest wins."** If `outer` also declared a `b`, the `middle` one would win. Same name, nearer binding, done — no error, no warning.
3. **There is exactly one failure mode.** Reach the bottom without a match → `ReferenceError`. The engine never quietly returns "nothing here." The *only* reason undeclared reads sometimes give `undefined` is Atom 1.1.1's hoisting: a `var` already parked an `undefined` in the chain.

##### Proof: Write Time, Not Call Time

This is the example that makes the model stick.

```javascript
const secret = "global secret";

function read() {
  return secret;          // read() was WRITTEN at top level
}

function makeReader() {
  const secret = "local secret";
  return read;            // we hand over the FUNCTION, not the value
}

const reader = makeReader();
console.log(reader());     // "global secret"
```

Most people predict `"local secret"` — the reader was *called* from inside `makeReader`, after all. It's wrong.

Trace it:

- The only question that matters is: **what does the text immediately around `read` look like?** Answer: top level.
- So `read`'s chain is permanently `[module scope → globalThis]`. The engine committed to this when it parsed that line — before `makeReader` ever ran.
- `makeReader`'s local `secret` is **not in that chain**. Nothing about `read`'s location in memory, or which variable holds it, changes the list.

The payoff line: **a JavaScript function carries its birthplace, not its current address.** Passing `read` into `makeReader` and getting it back changed where it *lives*. It did not change what it can *see*.

##### Why This Design and Not The Obvious One

In a hypothetical dynamically-scoped language, this would be a compile error — the compiler can't prove `secret` exists:

```csharp
// Dynamic scoping in C# would be DEAD CODE — no `secret` in Main.
Func<string> reader = () => secret;
```

JavaScript makes that decision for you at parse time, using the text on screen. Nothing is inferred from the call site. That is precisely what "lexical" means.

| | C# | JavaScript |
|---|---|---|
| Lambda captures | the *variables* it references | the *scope it was written in* |
| Opt out of capture | `static` local functions | impossible — always lexical |
| Decided at | compile time | parse time |
| Enclosing scope for a lambda | where the lambda is written | where the lambda is written (same) |

The real difference isn't *what* gets captured — it's that JS gives you **no escape hatch**. In C# a `static` lambda refuses to capture. In JavaScript every function is implicitly "static" in that sense: it only ever sees its own birth scope.

##### Block Scope in the Chain

Blocks are just more rungs on the ladder:

```javascript
for (var i = 0; i < 3; i++) {}
console.log(i);        // 3

for (let i = 0; i < 3; i++) {}
console.log(i);        // ReferenceError: i is not defined
```

`var i`'s binding belongs to the enclosing function/module scope, so it outlives the loop. `let i`'s binding belongs to the loop's block, which is destroyed when the loop exits — so outside the block there is **no binding at all**. Not an `undefined` binding: *no binding*. Identical rule, different rung.

##### The Chain Can Outlive Its Creator

```javascript
function makeReader() {
  const secret = "local secret";
  return function read() { return secret; };
}
const reader = makeReader();   // makeReader's scope is now unreachable...
reader();                      // ...except through reader. Still works.
```

`read`'s chain *points at a place in the program that still has a name*. `makeReader` finished executing long ago, but the scope it created is still reachable, because something still points into it.

That is a **closure**, and it is Atom 1.1.5. You now have both halves:

- **the chain is fixed at write time** — Atom 1.1.4
- **the chain can outlive the call that created it** — Atom 1.1.5

##### The Chain Meets the TDZ

The TDZ isn't a separate mechanism — it's a rung on the chain holding an *uninitialised* binding. Walk into it and the walk still fails, but for a different reason than "not found":

```javascript
{
  console.log(typeof count);   // ReferenceError, not "undefined"
  let count = 0;
}
```

The chain finds `count`. The rung exists. But the binding has no value yet, so reading it throws. Compare Atom 1.1.1:

```javascript
console.log(typeof notDeclaredAnywhere);  // "undefined" — no error, not in chain
```

Same walk, two outcomes: **absent from the chain** vs **present but uninitialised**.

##### Prediction Exercises

The five questions used to build this model. Work them before reading the answers.

**Q1 — Where does the chain stop?**

```javascript
function findSecret() {
  console.log(secret);
}
findSecret();

var secret = "I live at the top of the file";
```

<details><summary>Answer</summary>

**B — prints `undefined`.** `var secret` hoists to module scope and parks `undefined` there (Atom 1.1.1). `findSecret` runs before the assignment line executes, so the chain finds a real binding holding `undefined`.

</details>

**Q2 — Which `secret`?**

```javascript
const secret = "global secret";

function makeReader() {
  const secret = "local secret";
  return function read() { return secret; };
}

const reader = makeReader();
console.log(reader());
```

<details><summary>Answer</summary>

**B — `"local secret"`.** `read` was written inside `makeReader`, so the inner `secret` is one rung closer.

</details>

**Q3 — Prove it's write time, not call time**

```javascript
const secret = "global secret";

function read() {
  return secret;          // written at top level
}

function makeReader() {
  const secret = "local secret";
  return read;            // pass the FUNCTION, not the value
}

const reader = makeReader();
console.log(reader());
```

<details><summary>Answer</summary>

**B — `"global secret"`.** `read`'s chain was committed at parse time and contains only top-level scopes. The call site is irrelevant. This is the atom's central claim.

</details>

**Q4 — Chain walking with a hole**

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

**B — `ReferenceError: c is not defined`.** `a` found in `outer`, `b` found in `middle`, `c` found nowhere. The subtle part: had `outer` declared `var c`, you'd get `undefined` instead. Same walk, different failure mode.

</details>

**Q5 — Post-loop access**

```javascript
for (var i = 0; i < 3; i++) {}
console.log(i);          // 3

for (let i = 0; i < 3; i++) {}
console.log(i);          // ReferenceError
```

<details><summary>Answer</summary>

`var` → `3`. `let` → `ReferenceError: i is not defined`. See "Block Scope in the Chain" above.

</details>

#### Gotchas — Atom 1.1.4

1. **"Captures the value" is the wrong answer and it's the most common one.** A closure captures the **binding**, not a snapshot of its value. Proof:

   ```javascript
   function counter() {
     let n = 0;
     return { inc: () => ++n, get: () => n };
   }
   const c = counter();
   c.inc(); c.inc();
   console.log(c.get());   // 2 — the binding is live, not a copy
   ```

   If it captured values, `get()` would still return `0`. (Full treatment: Atom 1.1.5.)

2. **Moving a function textually changes what it can see — even if you call it from the same place as before.** Move `read` *inside* `makeReader` in Q3 and the answer flips from `"global secret"` to `"local secret"`. Nothing about the call site changed. Only the birth location.

3. **Shadowing is completely silent.** An inner `const total = 5` over an outer `total = 100` is legal, warning-free, and produces a bug that's genuinely hard to find, because the code reads correctly. Linters flag this; your eyes won't.

4. **`ReferenceError` vs `undefined` tells you *which kind* of chain-walk failed.** Absent from the chain → `ReferenceError`. Present but hoisted as `undefined` → `undefined`. Present but in the TDZ → `ReferenceError`. The message can't distinguish the last two, but the fix is different, so check the declaration form.

5. **Implicit globals pollute the chain in sloppy mode.** `function f() { undeclared = 5; }` succeeds in a classic script — the failed assignment walks to the bottom and *creates* a global. That bottom rung is why typos become silent cross-function bugs. Always declare.

6. **Every function gets two free rungs you didn't declare:** its own name (for recursion) and `arguments`. So `arguments` works inside any non-arrow function, and a function can call itself by name without `const f = () => {}`.

7. **`this` is _not_ resolved by the scope chain.** It's resolved by call-site rules (Atom 1.3.2). Mixing the two up is the source of most "why is `this` undefined" confusion — and it's also why arrow functions have no `this`: they inherit it from the enclosing scope chain instead.

8. **Module scope is not global scope.** In Node/CommonJS your top-level code is wrapped in a function, so top-level `var` is module-local. In ESM, top-level declarations are module-scoped and unbound names are a hard `ReferenceError` — you can't reach `globalThis` by accident. In a classic `<script>` tag, top-level `var` **is** global, and two scripts can collide.

#### Interview Questions — Atom 1.1.4

1. **"What does a closure capture?"**
   The **binding**, not the value. A closure retains a reference to a variable in an enclosing scope. Reads and writes go to the same live variable, so mutating it inside the closure is visible outside and vice versa. Capturing a *value* would make `createCounter().getCount()` always return `0` after an increment.

2. **"Walk me through how JavaScript resolves a variable name."**
   At parse time, the engine builds a scope chain for each piece of code from its textual nesting. At runtime, for each name, it walks outward rung by rung. The first rung containing that name wins — that's shadowing. If it reaches the bottom with no match, `ReferenceError`. Each name is walked independently.

3. **"What is the scope chain?"**
   The ordered list of scopes surrounding a piece of code, from innermost to outermost, ending at the global scope. It's built once from *where the code is written*, not rebuilt per call. Lookups walk it outward until the name is found.

4. **"Why does this log `0` forever?"** (the `useEffect` case)

   ```jsx
   useEffect(() => {
     const id = setInterval(() => console.log(count), 1000);
     return () => clearInterval(id);
   }, []);   // empty deps
   ```

   The interval callback was *written* during the first render, so its scope chain contains the first render's `count` — which is `0`. That chain is frozen at parse time and never updated. The empty dep array says "create this interval once," so the closure capturing the stale binding is never replaced. This is exactly "a function carries its birthplace, not its current address."

5. **"What is shadowing, and is it a bug?"**
   An inner declaration with the same name as an outer one. The inner scope is nearer, so it wins. Legal, silent, and a common source of bugs — especially when the shadowed name is a typo or a slightly different variable. Not a language bug; a readability hazard.

6. **"Does moving a function to a different part of the file change what it can access?"**
   Yes — and this is the question that proves you understand lexical scoping. The chain is derived from textual position. If a function's text moves such that it's now inside another function, its accessible variables change. The call sites are irrelevant to scoping.

7. **"Why does JavaScript use lexical scope instead of dynamic scope? What do we lose?"**
   Lexical makes scope predictable from reading the source: what a function touches is visible on the page, without tracing the call graph. The cost is that capturing loop variables or `this` behaves in ways that surprise people (the 3,3,3 trap), and there's no opt-out mechanism the way C# has `static` local functions.

8. **"How is JavaScript's scope chain different from C#'s lexical scoping?"**
   Mostly the same for lambdas. Two differences: JavaScript has no `static` equivalent, so every function's capture set is immutable; and JS functions implicitly capture their own name and `arguments`. Also `var`'s function-scoped hoisting means the "enclosing scope" can be further out than the nearest brace.

9. **"What happens if a name isn't found anywhere in the scope chain?"**
   A `ReferenceError` is thrown. The engine does not return `undefined`. If you *see* `undefined` for a name you didn't declare, it's because hoisting created the binding as `undefined` — a different situation with a different fix.

10. **"How would you debug a bug where a function reads the wrong variable?"**
    Check where the function is **written** first, not where it's called. That's the only thing that determines its chain. Then look for a same-named declaration in an intermediate scope (shadowing), then check whether `var` hoisting or the TDZ is involved. Use a debugger breakpoint to confirm the actual chain rather than assuming it.

#### Code I Wrote — Atom 1.1.4

*Pending — the scope-chain tracer is the proof-of-learning build for this atom. Model it on `getStackDepth` in Atom 1.1.3's Code section: a function that reports the chain of names visible at its call point, so you observe the chain instead of reasoning about it.*

---

### Atom 1.1.5 — Closures: What's Retained, the Loop Puzzle, and Three Real Uses

#### The Problem This Solves

You've seen a function keep working after the function that made it has finished:

```javascript
function makeReader() {
  const secret = "local secret";
  return function read() { return secret; };
}

const reader = makeReader();   // makeReader is done
reader();                      // still works
```

Two questions follow, and people usually only ever ask the first one.

**Question 1: what's being kept alive?** Not "how do I make this work" — you can already do that. The real question is what JavaScript is holding in memory on your behalf, and for how long. Get this wrong and a two-line component holds a 50MB dataset alive forever. That's Atom 1.1.6.

**Question 2: why does a loop with `var` print `3, 3, 3`?** Everyone memorises the fix (`use let`) and nobody can explain it afterwards. This atom makes the fix derivable instead.

#### The Mental Model

A closure is a function that carries a **key** to a room.

The variables it uses don't move and don't get copied. They stay in that room. As long as somebody is holding the key, JavaScript can't throw the room away — even if the function that built it finished running long ago.

The word that matters is **room**. People picture a closure as a function carrying a snapshot of a variable. It's not a snapshot. It's a key to the place where the variable still lives.

#### The Explanation

##### A closure holds a live link, not a copy

This is the cleanest proof, because it's the same shape as code you already wrote:

```javascript
function makeGreeter() {
  let greeting = "Hello";

  return {
    say:    (name) => `${greeting}, ${name}!`,   // reads it
    change: (g) => { greeting = g; }             // writes it
  };
}

const greeter = makeGreeter();

console.log(greeter.say("Alice"));   // Hello, Alice!
greeter.change("Yo");
console.log(greeter.say("Bob"));     // Yo, Bob!
```

`change()` assigns to `greeting`, and then `say()` sees the new value. That can only happen if **there is one `greeting`**, and both arrows point at it.

If a closure captured a copy, `say("Bob")` would still print `"Hello, Bob!"`.

> **Shortcut:** if two functions can see each other's writes, they share one variable. If they can't, each has its own copy. Closures share.

##### Every call to a factory makes a brand-new room

```javascript
function makeCounter() {
  let count = 0;
  return {
    inc: () => ++count,
    get: () => count
  };
}

const a = makeCounter();
const b = makeCounter();

a.inc();
a.inc();

console.log(a.get(), b.get());   // 2  0
```

`a.inc()` twice gives `2`. `b.get()` is still `0`, because running `makeCounter()` a second time created a **second `count`** in a second room.

The rule: **one call to the outer function = one scope = one copy of every variable inside it.** A closure captures one specific variable in one specific room.

##### The loop puzzle, solved properly

You've seen this:

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// 3, 3, 3
```

Stop memorising the fix. Count the **rooms** instead. Three versions:

```javascript
// Version A — let
const a = [];
for (let i = 0; i < 3; i++) {
  a.push(() => i);
}

// Version B — var, but a fresh block-scoped copy
const b = [];
for (var i = 0; i < 3; i++) {
  const captured = i;        // fresh binding EVERY iteration
  b.push(() => captured);    // reads `captured`, never `i`
}

// Version C — var, wrapped in a function
const c = [];
for (var i = 0; i < 3; i++) {
  c.push((function (j) { return () => j; })(i));
}

console.log(a.map(f => f()), b.map(f => f()), c.map(f => f()));
// [0,1,2]  [0,1,2]  [0,1,2]
```

```javascript
// Version D — var, no fix at all
const d = [];
for (var i = 0; i < 3; i++) {
  d.push(() => i);
}
console.log(d.map(f => f()));   // [3,3,3]
```

Here's the table that makes all four obvious:

| Version | How the arrow was written | Rooms | Output |
|---|---|---|---|
| A | directly in the body, `let i` | 3 | `0,1,2` |
| B | directly in the body, `const captured` | 3 | `0,1,2` |
| C | inside an IIFE | 3 | `0,1,2` |
| D | directly in the body, `var i` | 1 | `3,3,3` |

> **The rule: count the rooms the arrow function was written in. That is the entire puzzle.**

The loop is not the problem. Whether the arrow was written inside a fresh block on each iteration is the problem.

And notice what version B actually is: **`const captured = i` is `let` in disguise.** It gets a fresh binding every iteration for exactly the same reason `let` does. You've been using `let` all along without naming it.

##### What actually stays in memory

The syllabus asks this directly, and the honest answer has three layers.

**What the language says:** a closure holds a reference to its *scope* — the whole room, every variable declared in it.

```javascript
function setup() {
  const bigData = new Array(1_000_000).fill("some long string");
  const small = 42;

  return function use() {
    return small;        // only ever touches `small`
  };
}

const fn = setup();
```

**What engines actually do:** V8 and JSC have an optimisation where they keep only the bindings an inner closure genuinely references. So `bigData` may well get dropped, since `use` never mentions it.

**Why you should still assume the worst:** it's an implementation detail, it varies by engine, and adding a single reference to `bigData` *anywhere* in `setup` — even in a branch that never runs — flips the result back.

> **A closure retains its whole scope. Assume nothing is cleaned up unless you cleaned it up yourself.**

This is the one to carry into Atom 1.1.6, where a long-lived closure turns that assumption into a real leak.

##### Why anyone bothers: three uses

All three are the same pattern — **store a variable in a room, hand out functions that read and write it.**

**1. Private state.** Nothing outside can reach in and change it.

```javascript
function createCounter() {
  let count = 0;                       // unreachable from outside
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount:  () => count
  };
}

const counter = createCounter();
counter.getCount();          // 0
counter.count;               // undefined — no such property
```

There's no `private` keyword here. The variable is simply in a room nobody else has a key to.

**2. Function factories.** Build a specialised function once, cheaply.

```javascript
function once(fn) {
  let called = false;
  let result;
  return function (...args) {
    if (called) return undefined;
    called = true;
    result = fn.apply(this, args);
    return result;
  };
}

const greetOnce = once(name => console.log(`Hello, ${name}`));
greetOnce("Alice");   // Hello, Alice
greetOnce("Bob");     // undefined
```

The `called` flag exists inside `once`'s room. Every caller gets the same guard for free.

**3. Memoisation.** Cache results in a room nobody else can corrupt.

```javascript
function memoize(fn) {
  const cache = {};
  return function (...args) {
    const key = JSON.stringify(args);
    if (key in cache) {
      console.log("cache hit");
      return cache[key];
    }
    console.log("cache miss");
    cache[key] = fn(...args);
    return cache[key];
  };
}

const add = memoize((a, b) => a + b);
add(1, 2);   // "cache miss" → 3
add(1, 2);   // "cache hit"  → 3
```

`cache` is unreachable from outside, so nothing can put a wrong value in it or clear it behind your back.

##### Why this is React's biggest bug source

A closure is stale the moment it's created, because its room was fixed at write time:

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      console.log(count);        // logs 0 forever
    }, 1000);
    return () => clearInterval(id);
  }, []);                        // empty deps — create once

  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

The interval callback was *written* during the first render, so its room holds the first render's `count`, which is `0`. That room is never updated. The `[]` says "build this closure once," so the stale one is never replaced.

Two fixes, both worth knowing:

```jsx
// Fix 1 — declare the dependency. The effect re-runs, so a FRESH closure is built.
useEffect(() => {
  const id = setInterval(() => console.log(count), 1000);
  return () => clearInterval(id);
}, [count]);

// Fix 2 — don't close over the value at all. setCount's updater form reads the
// current state at call time, so there's nothing to go stale.
useEffect(() => {
  const id = setInterval(() => setCount(c => c + 1), 1000);
  return () => clearInterval(id);
}, []);
```

Fix 2 is the better habit. Any time you close over state inside an effect, ask whether an updater function would remove the need for a dependency entirely.

#### Gotchas — Atom 1.1.5

1. **Every call to a factory makes a new variable.** This is the mistake in Q1 above. Two calls to `createCounter()` means two `count`s. A closure captures *one* variable in *one* room, never "a variable of that shape."

2. **"It captures the value" is wrong, and it's the most common wrong answer.** The `makeGreeter` example is the proof: `change()` is visible to `say()`. If it captured values, they wouldn't share.

3. **`const captured = i` inside a `var` loop is not a hack — it's `let`.** It works for exactly the reason `let` works: fresh binding per block entry. Version B is not a workaround, it's the same mechanism written longhand.

4. **The loop is not the problem — the room count is.** Once you can count rooms, you can derive every case, including ones you haven't seen. Memorising "use `let`" gives you the one case you've memorised.

5. **`for...of` and `for...in` are different.** `for (const x of arr)` creates a fresh binding per iteration, so closures over `x` are safe. `for (const k in obj)` does not iterate per-iteration scopes the same way, and closures over `k` need care. Don't generalise "const in the head is always safe" until you've checked which loop it is.

6. **A closure retains its whole scope, even the parts it never touches.** Assume every engine keeps everything. See "What actually stays in memory" above — and note that one stray reference anywhere changes the outcome.

7. **`memoize` with `JSON.stringify(args)` is wrong for objects.** Two different objects with the same shape produce the same key, so you get a wrong cached answer. It also throws on `undefined` inside an array and collapses `{a:1}` and `{a:"1"}`. A correct key needs identity, which is what `Map` + `WeakMap` are for.

8. **Arrow functions and `this`.** A closure inside an object method can accidentally change what `this` is, because arrow functions inherit `this` from the surrounding room rather than getting their own. That's Atom 1.3.3, and it's why the `once` implementation above uses `fn.apply(this, args)` carefully.

9. **Long-lived closures are the leak vector.** A closure stored on a component, a module-level cache, or an event listener holds its room indefinitely. Every variable in that room is retained with it. That's Atom 1.1.6.

#### Interview Questions — Atom 1.1.5

1. **"What is a closure?"**
   A function plus a live reference to the scope it was created in. Because that link survives the original call, the function can keep reading and writing variables whose declaring function has already returned.

2. **"What does a closure capture — a value or a variable?"**
   The variable. It holds a live link, not a snapshot. Proof: if two functions returned from the same factory can see each other's writes, they're sharing one variable. If a closure captured values, `makeGreeter().change("Yo")` would have no effect on `say()`.

3. **"What does a closure retain in memory?"**
   Its whole scope. Engines like V8 may optimise down to only the captured bindings, but that's an implementation detail that varies by engine and changes if anything else references the other variables. Code as if everything in that scope stays alive — and if that scope is long-lived, that's a leak.

4. **"Why does `for (var i...)` with `setTimeout` print 3, 3, 3?"**
   All three callbacks were written in the same room, and `var` made that room contain exactly one `i`. Three callbacks, one variable, and by the time they run the loop is done so `i` is `3`. `let` gives each iteration its own room, so each callback reads its own `i`.

5. **"How do you capture the loop variable without `let`?"**
   Declare a fresh binding inside the body — `const captured = i;` — and close over that. It's `let` written longhand. An IIFE that takes `i` as a parameter does the same thing.

6. **"You have `const fns = []; for (const x of items) fns.push(() => x)`. Is this safe?"**
   Yes. `for...of` with a block-scoped binding creates a new binding per iteration, so each closure captures its own `x`. The unsafe patterns are `var` in the head, or closing over the loop *variable* of a `for...in`.

7. **"Give me three real uses for closures."**
   Private state (a counter nobody can tamper with), function factories (`once`, `curry` — build a specialised function once), and memoisation (a private cache). All three are the same pattern: keep a variable in a scope, hand out functions that read and write it.

8. **"Why does my `useEffect` log a stale value?"**
   The callback was written during the render where the value was X, and closures are fixed at write time. The effect created that closure once and never replaced it, so it keeps reading the original value. Fixes: list the value as a dependency so a fresh closure is built, or avoid closing over it entirely by using a state updater function.

9. **"Does `memoize` above work correctly? What's wrong with it?"**
   `JSON.stringify(args)` is a value-based key, so two distinct objects with identical shape collide and you return a wrong cached value. It also mishandles `undefined` and conflates `1` with `"1"`. You need a key that respects reference identity — a `Map`, or `WeakMap` for object keys so entries don't themselves leak.

10. **"Do closures cause memory leaks?"**
    Not inherently, but they're the most common cause. A closure retains its entire scope, so anything in that scope stays reachable as long as the closure does. Store a closure somewhere long-lived — a module-level cache, a component that never unmounts, an unremoved event listener — and its room never gets collected. See Atom 1.1.6.

#### Code I Wrote — Atom 1.1.5

The three uses from **Code I Wrote (Unit Proof)** below are this atom's builds. Re-reading them with the room model:

| Build | The room | The key |
|---|---|---|
| `createCounter()` | `count` | `increment` / `decrement` / `getCount` |
| `once(fn)` | `called`, `result` | the returned wrapper |
| `memoize(fn)` | `cache` | the returned wrapper |

All three are the same two lines of design: *declare a variable, return a function that closes over it.*

Two improvements worth making, both from the gotchas above:

```javascript
// Before — collides on shape, throws on undefined
const key = JSON.stringify(args);

// After — respects reference identity, and doesn't keep dead entries alive
const cache = new Map();
const key = args.length === 0
  ? Symbol.for("no-args")
  : args[0] && typeof args[0] === "object"
    ? args[0]                       // object key → identity-based, matches by reference
    : JSON.stringify(args);
```

*Pending — the retention proof (`retainedScope()` then `weakRefProbe()`) hasn't been written yet. That build is what turns "a closure retains its whole scope" from something you were told into something you measured.*

---

## Code I Wrote (Unit Proof)

> **Placement note.** These three are closure exercises — the syllabus assigns "three real uses: private state, function factories, memoisation" to **Atom 1.1.5**, which is now written up in this file. They stay under the unit-level heading as the original build record; Atom 1.1.5's **Code I Wrote** section maps each one back to the room/key model.

### once(fn) — Run a function only once

```javascript
function once(fn) {
  let called = false;
  let result;
  return function(...args) {
    if (called) return undefined;
    called = true;
    result = fn.apply(this, args); // this helps to understand 'this' keywork in js
    return result;
  };
} 

const greetOnce = once(name => console.log(`Hello, ${name}`));
greetOnce("Alice"); // "Hello, Alice"
greetOnce("Bob");   // undefined (second call does nothing)
```

### memoize(fn) — Cache function results

```javascript
function memoize(fn) {
  const cache = {};
  return function(...args) {
    const key = JSON.stringify(args);
    if (key in cache) {
      console.log("cache hit");
      return cache[key];
    }
    console.log("cache miss");
    cache[key] = fn(...args);
    return cache[key];
  };
}

const add = memoize((a, b) => a + b);
add(1, 2); // "cache miss" → 3
add(1, 2); // "cache hit" → 3
```

### Counter Factory — Truly private state

```javascript
function createCounter() {
  let count = 0; // private — can't access from outside
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count
  };
}

const counter = createCounter();
counter.increment(); // 1
counter.increment(); // 2
counter.decrement(); // 1
counter.getCount();  // 1
// counter.count is undefined — truly private
```

---

## Proof of Learning

1. **`once(fn)`** — Implemented ✓ → Atom 1.1.3 (function factory + closure)
2. **`memoize(fn)`** — Implemented ✓ → Atom 1.1.5 (memoisation)
3. **Counter factory** — Implemented ✓ → Atom 1.1.5 (private state)
4. **Stack frame tracer** — Implemented ✓ → Atom 1.1.3 (proves runtime stack measurement)

All four demonstrate closures (private state, retained variables) and proper JavaScript patterns.

**Self-check — can you answer these without looking?**

- [ ] Why does `console.log(x)` before `var x = 5` print `undefined`?
- [ ] What's the difference between being hoisted and being initialized?
- [ ] Why does `const arr = [1]; arr.push(2)` work but `arr = []` throw?
- [ ] Why does the `var` loop print 3, 3, 3 — and what does `let` change about memory?
- [ ] Read a stack trace top-to-bottom: what does each line tell you?
- [ ] What's the difference between `ReferenceError` and `TypeError` here, and why does the distinction matter?

---

## Atom Coverage In This File

| Atom | Topic | Sections present |
|------|-------|------------------|
| 1.1.1 | How JS runs: parsing, creation/execution, hoisting | Explanation, Gotchas, Interview Questions |
| 1.1.2 | `var` vs `let` vs `const`, TDZ, the loop puzzle | Explanation, Deep Dive, Gotchas, Interview Questions |
| 1.1.3 | Call stack, stack trace, stack overflow | Explanation, Gotchas, Interview Questions, Code I Wrote |
| 1.1.4 | Lexical scope and the scope chain | Explanation, Gotchas, Interview Questions |
| 1.1.5 | Closures: what's retained, loop puzzle, real uses | Explanation, Gotchas, Interview Questions, Code I Wrote |
| 1.1.6 | Closures and memory leaks | Not started |
| 1.1.7 | IIFEs and module pattern | Not started |

**Gaps:**
- Atom 1.1.1, 1.1.2, 1.1.4 have no "Code I Wrote" section — no proof build written yet
- Atom 1.1.4 and 1.1.5 teach-back not yet done; both left at `In Progress` in PROGRESS.md
- Atom 1.1.5's retention proof (`retainedScope()` / `weakRefProbe()`) not written
- Atom 1.1.4 and 1.1.5 prose is plainer than 1.1.1–1.1.3, which are still in the original denser style

---

## Next: Atom 1.1.6 — Closures and Memory Leaks

You now know a closure retains its entire scope. Atom 1.1.6 asks the follow-up: **when does that retention become a leak?** What it looks like when a closure holds a large object alive longer than you intended — the component that never unmounts, the event listener you forgot to remove, the module-level cache that grows forever, and how you diagnose it in a real heap snapshot.