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

### Atom 1.1.1 — How JavaScript Actually Runs

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

---

### Atom 1.1.2 — var vs let vs const: Scope, TDZ, and Why const ≠ Immutable

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

**`const` does NOT freeze the value.** To truly freeze: `Object.freeze(user)` — but that's shallow (nested objects are still mutable).

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

---

### Atom 1.1.3 — The Call Stack (Coming Soon)

---

### What is a Callback?

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

---

### The var Loop Problem — Why 3, 3, 3?

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

---

### Why `let` Gives You 0, 1, 2

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

---

### JavaScript is Single-Threaded

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

The `setTimeout` with `0` delay doesn't mean "run immediately" — it means "run after the current code finishes."

---

## The Gotchas / Things That Bit Me

1. **Hoisting doesn't move code.** The code stays where it is. Only the declarations are processed first.

2. **`let` and `const` ARE hoisted** — people get this wrong. They're hoisted but NOT initialized. That's the Temporal Dead Zone.

3. **Function expressions are NOT hoisted (if using var):**
   ```javascript
   sayHi(); // TypeError: sayHi is not a function
   
   var sayHi = function() {
     console.log("hi");
   };
   ```
   `sayHi` is hoisted as `undefined`, so calling `undefined()` gives TypeError, not ReferenceError.

4. **`typeof` doesn't throw on undeclared variables but DOES throw on TDZ:**
   ```javascript
   console.log(typeof undeclared); // "undefined" — no error
   console.log(typeof letVar);     // ReferenceError — TDZ
   let letVar = 5;
   ```

5. **`const` does NOT freeze the value:**
   ```javascript
   const user = { name: "Alice" };
   user.name = "Bob";    // Works! Object is mutated
   user = { name: "X" }; // TypeError: can't reassign
   ```

6. **`var` in loops creates one variable shared across iterations — THIS IS THE #1 INTERVIEW TRAP:**
   ```javascript
   for (var i = 0; i < 3; i++) {
     setTimeout(() => console.log(i), 100);
   }
   // Output: 3, 3, 3
   ```

---

## Interview-Shaped Questions I Can Now Answer

1. **"Why does `console.log(x)` before `var x = 5` give `undefined` instead of ReferenceError?"**
   Because during the creation phase, `var` declarations are hoisted and initialized as `undefined`. By the time execution reaches `console.log(x)`, the variable exists in memory with value `undefined`.

2. **"Are `let` and `const` hoisted?"**
   Yes, they are hoisted during creation phase, but they are NOT initialized. They enter a "Temporal Dead Zone" from the start of the block until the declaration line. Accessing them during TDZ throws ReferenceError.

3. **"What's the difference between `var` and `let` hoisting?"**
   `var` is hoisted AND initialized as `undefined` — you can read it (getting `undefined`). `let`/`const` are hoisted but NOT initialized — reading them throws ReferenceError until the declaration executes.

4. **"Why does `const` not mean immutable?"**
   `const` prevents reassignment of the variable binding — what the name points to. It does NOT prevent mutation of the value. So `const arr = [1,2,3]; arr.push(4)` works because you're modifying the array, not reassigning `arr`.

5. **"Why is `var` considered bad practice?"**
   `var` is function-scoped, not block-scoped. This means variables "leak" out of if blocks, for loops, and other block scopes. It also allows redeclaration in the same scope.

6. **"What is the Temporal Dead Zone?"**
   The TDZ is the period after a `let`/`const` is hoisted but before its declaration executes. During this period, accessing the variable throws ReferenceError. It exists to prevent silent `undefined` values from causing subtle bugs.

7. **"Why does `for (var i...)` with setTimeout print 3, 3, 3?"**
   `var` is function-scoped — all callbacks share ONE `i`. By the time they execute, the loop is done and `i === 3`. `let` fixes this because each iteration gets its own `i` binding.

---

## Code I Wrote

### once(fn) — Run a function only once
```javascript
function once(fn) {
  let called = false;
  let result;
  return function(...args) {
    if (called) return undefined;
    called = true;
    result = fn.apply(this, args);
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

1. **`once(fn)`** — Implemented above ✓
2. **`memoize(fn)`** — Implemented above ✓
3. **Counter factory** — Implemented above ✓

All three demonstrate closures (private state, retained variables) and proper JavaScript patterns.

---

## Next: Atom 1.1.3 — The Call Stack

The call stack tracks which function is currently running. When function A calls function B which calls function C, the stack grows. When C finishes, it pops off and returns to B. This is how JavaScript knows where to return to.

*Next session: Call stack, stack traces, stack overflow, and how callbacks eventually execute.*
