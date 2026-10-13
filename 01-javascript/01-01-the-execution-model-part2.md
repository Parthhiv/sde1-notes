# Unit 1.1 — The Execution Model (Part 2)

> **Part 2 of 2 — Atoms 1.1.5 → 1.1.7.** *What a function keeps alive.* Part 1 (`01-01-the-execution-model-part1.md`) covers the machine: phases, hoisting, TDZ, the call stack, lexical scope. Part 2 picks up from the one rule Part 1 leaves open — **a function's chain can outlive the call that created it.**

## The Problem This Solves

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

**Question 1: what's being kept alive?** Not "how do I make this work" — you can already do that. The real question is what JavaScript is holding in memory on your behalf, and for how long. Get this wrong and a two-line component holds a 50MB dataset alive forever (Atom 1.1.6).

**Question 2: why does a loop with `var` print `3, 3, 3`?** Everyone memorises the fix (`use let`) and nobody can explain it afterwards. This atom makes the fix derivable instead.

Then there's the packaging question: **how do you keep variables private when every file on the page shares one global scope?** That answer is the IIFE, and understanding *why it existed* tells you what to use instead (Atom 1.1.7).

## The Mental Model

A closure is a function that carries a **key** to a room.

The variables it uses don't move and don't get copied. They stay in that room. As long as somebody is holding the key, JavaScript can't throw the room away — even if the function that built it finished running long ago.

The word that matters is **room**. People picture a closure as a function carrying a snapshot of a variable. It's not a snapshot. It's a key to the place where the variable still lives.

---

## The Details

### Atom 1.1.5 — Closures: What's Retained, the Loop Puzzle, and Three Real Uses

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
  return { inc: () => ++count, get: () => count };
}

const a = makeCounter();
const b = makeCounter();

a.inc();
a.inc();

console.log(a.get(), b.get());   // 2  0
```

`a.inc()` twice gives `2`. `b.get()` is still `0`, because running `makeCounter()` a second time created a **second `count`** in a second room.

The rule: **one call to the outer function = one scope = one copy of every variable inside it.**

##### The loop puzzle, solved properly

Atom 1.1.2 showed you `3, 3, 3` and that `let` fixes it. Stop memorising the fix. Count the **rooms** instead. Three versions:

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

// Version D — var, no fix at all
const d = [];
for (var i = 0; i < 3; i++) {
  d.push(() => i);
}

console.log(a.map(f => f()), b.map(f => f()), c.map(f => f()), d.map(f => f()));
// [0,1,2]  [0,1,2]  [0,1,2]  [3,3,3]
```

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

`cache` is unreachable from outside, so nothing can put a wrong value in it or clear it behind your back. (The `JSON.stringify` key is wrong for objects — see Gotcha 4.)

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

1. **Every call to a factory makes a new variable.** Two calls to `createCounter()` means two `count`s. A closure captures *one* variable in *one* room, never "a variable of that shape."

2. **"It captures the value" is wrong, and it's the most common wrong answer.** The `makeGreeter` example is the proof: `change()` is visible to `say()`.

3. **The loop is not the problem — the room count is.** Once you can count rooms you can derive every case, including ones you haven't seen. Memorising "use `let`" gives you the one case you memorised.

4. **`for...of` is safe; `for...in` needs care.** `for (const x of arr)` creates a fresh binding per iteration. Don't generalise "const in the head is always safe" until you've checked which loop it is.

5. **`memoize` with `JSON.stringify(args)` is wrong for objects.** Two different objects with the same shape produce the same key, so you return a wrong cached answer. It also throws on `undefined` inside an array. A correct key needs reference identity — which is what `Map` and `WeakMap` are for.

6. **Arrow functions and `this`.** A closure inside an object method can accidentally change what `this` is, because arrows inherit `this` from the surrounding room rather than getting their own. That's Atom 1.3.3, and it's why `once` above uses `fn.apply(this, args)` carefully.

#### Interview Questions — Atom 1.1.5

1. **"What is a closure?"**
   A function plus a live reference to the scope it was created in. Because that link survives the original call, the function can keep reading and writing variables whose declaring function has already returned.

2. **"What does a closure capture — a value or a variable?"**
   The variable. It holds a live link, not a snapshot. Proof: if two functions returned from the same factory can see each other's writes, they're sharing one variable. If a closure captured values, `makeGreeter().change("Yo")` would have no effect on `say()`.

3. **"What does a closure retain in memory?"**
   Its whole scope. Engines like V8 may optimise down to only the captured bindings, but that's an implementation detail that varies by engine and changes if anything else references the other variables. Code as if everything in that scope stays alive — and if that scope is long-lived, that's a leak.

4. **"Why does `for (var i...)` with `setTimeout` print 3, 3, 3?"**
   All three callbacks were written in the same room, and `var` made that room contain exactly one `i`. Three callbacks, one variable, and by the time they run the loop is done so `i` is `3`. `let` gives each iteration its own room.

5. **"How do you capture the loop variable without `let`?"**
   Declare a fresh binding inside the body — `const captured = i;` — and close over that. It's `let` written longhand. An IIFE that takes `i` as a parameter does the same thing.

6. **"Give me three real uses for closures."**
   Private state (a counter nobody can tamper with), function factories (`once`, `curry` — build a specialised function once), and memoisation (a private cache). All three are the same pattern: keep a variable in a scope, hand out functions that read and write it.

7. **"Why does my `useEffect` log a stale value?"**
   The callback was written during the render where the value was X, and closures are fixed at write time. The effect created that closure once and never replaced it, so it keeps reading the original value. Fixes: list the value as a dependency so a fresh closure is built, or avoid closing over it entirely by using a state updater function.

8. **"Do closures cause memory leaks?"**
   Not inherently, but they're the most common cause. A closure retains its entire scope, so anything in that scope stays reachable as long as the closure does. Store a closure somewhere long-lived — a module-level cache, a component that never unmounts, an unremoved event listener — and its room never gets collected. See Atom 1.1.6.

#### Code I Wrote — Atom 1.1.5

The three builds from **Proof of Learning** below map directly onto the room model:

| Build | The room | The key |
|---|---|---|
| `createCounter()` | `count` | `increment` / `decrement` / `getCount` |
| `once(fn)` | `called`, `result` | the returned wrapper |
| `memoize(fn)` | `cache` | the returned wrapper |

All three are the same two lines of design: *declare a variable, return a function that closes over it.*

Worth improving, from Gotcha 5 — `JSON.stringify` keys collide on shape, so respect reference identity instead:

```javascript
// Before — collides on shape, throws on undefined
const key = JSON.stringify(args);

// After — respects reference identity, and doesn't keep dead entries alive
const cache = new Map();
const key = args.length === 0
  ? Symbol.for("no-args")
  : args[0] && typeof args[0] === "object"
    ? args[0]                       // object key → matched by reference
    : JSON.stringify(args);
```

The retention proof (`retainedScope()` then `weakRefProbe()`) lives in Atom 1.1.6's Code I Wrote — a leak is the only situation where "a closure retains its whole scope" becomes observable.

---

### Atom 1.1.6 — Closures and Memory Leaks

#### The Problem This Solves

Atom 1.1.5 gave you the line *"a closure retains its whole scope."* It's true, it's why people blame closures for every memory problem they see, and on its own it's **incomplete** — which means it can't be used to fix anything.

The failure mode: a component navigates away, the fetched dataset, the detached DOM node, the 2000-row array — all still resident. Memory climbs for the whole session and never comes down, and eventually the tab dies. What makes this so hard is that **every line of code you can read is correct.** There's no bug to point at, only a structure nobody ever tore down.

The interview trap is the popular explanation. Most people answer *"closures leak because they create reference cycles."* That's wrong, and if you build your debugging intuition on it you'll go hunting for circular references in code that has none.

#### The Mental Model

A garbage collector never asks *"is this object being used right now?"* It asks exactly one question: **starting from the roots, can I draw a path to this object?**

Roots are a short list — the global object (`window` / `globalThis`), the stack of whatever code is running right now, and a handful of browser-held handles. That's the whole set. Everything reachable from a root survives. Everything unreachable is collected, no matter how long ago it stopped being useful.

So a leak is **not** "memory is being used." A leak is **an object that has outlived its purpose and is still reachable from a root.** Three things must be true simultaneously:

```
leak = a long-lived ROOT
     + a path from that root into a closure's retained scope
     + something big inside that scope
```

Remove any one of the three and nothing leaks. That's the entire diagnostic strategy, and it's why *"find the root"* is the only question worth asking when a heap snapshot tells you something grew.

#### The Explanation

##### Cycles are not leaks — the correction that matters

The popular story — *"a closure captures its parent scope, so it forms a cycle, and cycles leak"* — is wrong:

```javascript
function makeSelfReferentialThing() {
  const node = { child: null };
  node.child = node;          // a cycle, with no root anywhere
  return node;
}

const dead = [makeSelfReferentialThing(), makeSelfReferentialThing()];
// drop `dead` — the GC collects both, cycle and all
```

A tracing collector walks **outward** from roots and marks whatever it reaches. An unreachable cycle is unreachable, and unreachable is precisely the collection condition. Cycles aren't collected because of *when* they break — they're collected because the walker never arrives.

Reference-counting languages genuinely leak on cycles. That was IE6. JavaScript has never had that failure mode.

> **A cycle is not a leak. Only a *rooted* graph is.**

##### Where roots actually live

```
ROOT ───────────────────────────────────────────► never goes away on its own
  │
  ├─ window / globalThis        survives for the life of the page
  ├─ module scope              survives for the life of the page load
  ├─ addEventListener(...)     survives until removeEventListener
  ├─ setInterval / setTimeout  survives until cleared
  ├─ document / body nodes     survives until removed AND dereferenced
  └─ your own caches / arrays  survives until you delete the entry
```

Every leak you'll diagnose is one of those six holding a chain into something it shouldn't.

##### Leak 1 — event listeners never removed

```javascript
function ChatPanel() {
  useEffect(() => {
    const onScroll = () => console.log(scrollY); // closes over this render's scope
    window.addEventListener("scroll", onScroll);
    // ❌ no removeEventListener — window is a root, onScroll is now permanent
  }, []);
}
```

`window` is a root. `onScroll` is reachable forever, and `onScroll`'s scope holds this render's `messages` array. Navigate away and back fifty times and you have fifty copies of `messages` plus fifty listeners all firing on every scroll event.

##### Leak 2 — timers never cleared

```javascript
useEffect(() => {
  setInterval(() => setNow(new Date()), 1000);
  // ❌ no clearInterval — rooted in the timer queue forever, fires after unmount
}, []);
```

Same shape, different root. The `setState on an unmounted component` warning is the symptom, not the bug. The leak already happened; the warning is the timer mentioning it on the way past.

##### Leak 3 — detached DOM nodes

This is the classic one, and its mechanism is usually stated backwards.

```javascript
function attachTooltips() {
  document.querySelectorAll(".tip").forEach(node => {
    node.addEventListener("mouseenter", () => {
      console.log(node.dataset.text);   // ← the callback closes over `node`
    });
  });
}
```

Later a re-render replaces the subtree, or a filter empties the list. The nodes are gone from the **document tree** — but being detached is not the same as being unreachable. If anything outside the cluster holds one reference, the whole thing survives:

```javascript
const eventLog = [];   // ← module scope = a root

function attachTooltips() {
  document.querySelectorAll(".tip").forEach(node => {
    node.addEventListener("mouseenter", () => {
      eventLog.push(node);              // now the cluster IS rooted
      console.log(node.dataset.text);
    });
  });
}
```

Now the chain is `eventLog` → listener → closure scope → `node` → `node.parentNode` → every ancestor inside the removed subtree. Each remount adds another island. In DevTools these appear as **`Detached HTMLElement`** with a retained size, because there's no node left in the document that a devtools panel could otherwise attach itself to.

Note the subtlety: in the *first* version, with nothing external referencing the nodes, the cluster is unrooted and the GC would clean it up on its own. The listener isn't the root — it's just another member of the same garbage island.

##### Leak 4 — unbounded caches

```javascript
const responseCache = {};                 // module scope = a root, forever

async function fetchUser(id) {
  if (responseCache[id]) return responseCache[id];
  const response = await fetch(`/api/users/${id}`);
  responseCache[id] = await response.json();
  return responseCache[id];
}
```

No closure involved, and it still leaks — a root that grows without bound. Worth knowing because it proves the model isn't *"closures are bad."* It's *"roots that grow are bad."*

##### The React rule that covers leaks 1, 2 and 3

**Every `useEffect` that registers something external must return a function that unregisters it.** If the thing you register outlives your effect body — a listener, a timer, a subscription, an observer — then you, not React, own its removal.

```javascript
useEffect(() => {
  const onScroll = () => setOffset(window.scrollY);
  window.addEventListener("scroll", onScroll);

  const id = setInterval(() => setNow(Date.now()), 1000);

  return () => {                          // the cleanup
    window.removeEventListener("scroll", onScroll);
    clearInterval(id);
  };
}, []);
```

React invokes that returned function on unmount **and** before every re-run of the effect, so it also covers the dependency-change case. Miss it and the callback is rooted for the life of the page.

##### Diagnosing it for real

This is the part that separates *"knows about leaks"* from *"has found one."*

**Step 1 — confirm it's a leak, not just allocation.** Force a GC (the trash-can icon in DevTools → Memory, or `globalThis.gc()` with `--js-flags=--expose-gc`). If memory returns to baseline, you were allocating, not leaking. A leak grows and **stays** grown no matter how many times you force collection.

**Step 2 — compare three snapshots.** Take three in a row with the *same* interaction between each. Snapshot 1 warms everything up; snapshots 2 and 3 are the meaningful comparison. Growth between 2 and 3 under identical actions is the leak. Growth between 1 and 2 is usually just lazy loading.

**Step 3 — read the retainers.** Select the object and switch the bottom pane to the **Retainers** view. You get a chain:

> `Detached HTMLElement` ← *retained by* ← `HTMLDivElement` ← *retained by* ← `Closure (context)` ← *retained by* ← `Array` ← *retained by* ← `Module` ← *retained by* ← `Global`

Read it bottom-up. Every hop names a structure that's holding on; the last line is your root, and the root is what you have to fix. Ends at `Global` or `Module` → module-scope state. Ends at `EventListener` / `NativeInternal` → an unremoved listener.

Chrome also surfaces a one-click *"why is this still here"* column in the Objects view, plus a class filter. **Filtering the class list for `Detached` is the fastest confirmation of a frontend leak.**

##### Fixes, in order of preference

**1 — Remove the root.** Clear the listener, clear the timer, delete the cache entry. This is the actual fix; everything below is mitigation.

**2 — Null out the reference.** When an object legitimately holds something it doesn't always need:

```javascript
this.buffer = null;   // drops the only remaining path to a 40MB payload
```

**3 — Don't capture what you don't need.** A closure retains its *whole* scope, so shrinking the closure's scope shrinks the blast radius:

```javascript
// ❌ the interval's scope includes the whole rows array
useEffect(() => {
  const id = setInterval(() => setRowCount(rows.length), 1000);
  return () => clearInterval(id);
}, [rows]);

// ✅ hoist the primitive out — the closure's scope now holds a number
useEffect(() => {
  const rowCount = rows.length;
  const id = setInterval(() => setRowCount(rowCount), 1000);
  return () => clearInterval(id);
}, [rowCount]);
```

Identical behaviour, and nothing can reach the array through that timer anymore.

**4 — Use weak references when the lifetimes genuinely don't match.**

```javascript
const cache = new WeakMap();     // keyed by object — the entry dies with the key
```

For "hold this if it's still around, but never keep it alive":

```javascript
const ref = new WeakRef(hugeObject);

const obj = ref.deref();
if (obj) {
  use(obj);
}
// else: already collected — a normal outcome, not an exception
```

`deref()` returning `undefined` is expected behaviour, which is precisely why `WeakRef` is only appropriate for caches and registry lookups — never for data you're about to use. `FinalizationRegistry` is the cleanup counterpart: register an object, get a callback after it's collected.

#### Gotchas — Atom 1.1.6

1. **Cycles are not leaks.** If your diagnosis starts with *"it's a circular reference,"* you're reasoning like it's 2005. A tracing GC collects unreachable cycles without being asked. You need a root.

2. **`"setState on an unmounted component"` is a symptom.** It means an interval or subscription outlived its component. Silencing the warning doesn't fix the leak; clearing the timer does.

3. **Memory that grows then plateaus is not a leak.** GC is lazy and non-deterministic. Only growth that survives a forced collection *and* repeats under identical user actions is real.

4. **Removing a DOM node detaches it — it doesn't free it.** It leaves the document tree only. Any surviving reference, including the node's own event listener, keeps the entire subtree alive.

5. **`WeakRef.deref()` can return `undefined` immediately**, even for a variable you're still using, because the engine may collect it the instant you drop your last strong reference. Never hold only a `WeakRef` to something you can't survive losing. (`WeakMap` has no such problem — it only drops entries when the key is genuinely gone. Use it for `memoize` keyed on object arguments.)

6. **A leak is about reachability, not ownership.** You don't need to own an object to keep it alive. One array in module scope holding one reference is enough to pin a megabyte. Ownership intuition actively misleads here.

7. **Nothing in the language forces cleanup.** No `using`, no `IDisposable`, no deterministic destruction. The GC tells nobody when it runs, so there's nowhere to hang a destructor. This is the single biggest divergence from C#, and it's why every JS resource rule is *"return the cleanup function."*

#### Interview Questions — Atom 1.1.6

1. **"What is a memory leak in JavaScript?"**
   An object that's still reachable from a root, so the GC can't collect it, but that has no live purpose. The GC collects by *reachability*, not usefulness — if I can draw a path from `window`, the stack, or a registered listener, it stays, indefinitely.

2. **"A closure captures its parent scope. Doesn't that leak memory?"**
   Only if that scope is reachable from a root. A closure whose result is dropped gets collected along with everything it retained — cycles included, because the GC is a tracing collector, not a reference counter. The closure is the *path*; something long-lived has to hold the other end.

3. **"How would you diagnose a leak in a browser app?"**
   Force a GC and check whether memory returns to baseline. If it doesn't, take three heap snapshots with identical interactions between each, diff 2 against 3, then open the Retainers view on the growing objects. It prints the exact chain of references from the root, and the final hop names the thing to change. Filtering the class list for `Detached` confirms a DOM leak fastest.

4. **"Why do detached DOM nodes appear in memory snapshots?"**
   Removing a node detaches it from the document tree without freeing it. If any reference survives — an array, a global, or the node's own listener — the node and its whole subtree stay reachable. Chrome labels them `Detached HTMLElement` and shows the retained size precisely because there's no live node for a devtools panel to attach to.

5. **"Your `useEffect` returns nothing. What's the bug?"**
   Any effect registering something outside React — listener, interval, subscription, observer — must return a cleanup function. Without one, that callback is rooted for the life of the page and it keeps its entire scope alive. The cleanup runs on unmount and before every effect re-run, so it covers the dependency-change case too.

6. **"A colleague says 'we have a circular reference in our store, that's the leak.' What do you tell them?"**
   Circular references are collected normally by a tracing GC — the walker just never reaches them, which is exactly the condition for collection. Ask instead what roots the graph: which listener, timer, module-scope variable, or array still points into it. That's the only question that identifies a leak, and a cycle is never the answer.

7. **"C# has `using` and `IDisposable`. Why does JS need cleanup functions?"**
   JS objects have no deterministic destruction point. The GC reclaims memory whenever it decides to and notifies nobody, so there's no place to hang a destructor. Hence the convention: the function that registers an external resource returns the teardown function, and the caller must call it.

#### Code I Wrote — Atom 1.1.6

The retention proof. The point isn't to believe *"a closure retains its whole scope"* — it's to **watch the GC agree or disagree**, case by case. Save as `leak-probe.js` and run `node --expose-gc leak-probe.js`.

```javascript
// Every case creates the SAME ~60MB payload via a closure.
// The only thing that varies is whether a ROOT holds the result.

function makeHeavyPayload() {
  const bigData = Array.from({ length: 200_000 }, (_, id) => ({
    id,
    blob: "x".repeat(128),          // ~200k objects ≈ 60MB
  }));

  return {
    bytes: bigData.length,
    peek: () => bigData.length,     // ← closes over bigData: its scope is retained
  };
}

// FinalizationRegistry fires a callback once an object is genuinely collected.
const collected = [];
const registry = new FinalizationRegistry(tag => collected.push(tag));

const track = (payload, tag) => {
  registry.register(payload, tag);
  return payload;
};

// ---- Case 1: dropped. Unrooted island — the GC should collect it. -------
track(makeHeavyPayload(), "1-dropped");

// ---- Case 2: stored in a module-level array. That array is a root. ------
const leakedCache = [];
leakedCache.push(track(makeHeavyPayload(), "2-cached"));

// ---- Case 3: rooted through an event listener (the React mistake). -----
const handlers = {};
function attachHandler() {
  const payload = track(makeHeavyPayload(), "3-listener");
  handlers.onScroll = () => payload.peek();      // same as addEventListener
}
attachHandler();

// ---- Case 4: retained only by its own listener, nothing external. -------
// The cluster is unrooted, so this is NOT a leak, despite the cycle.
function attachIsland() {
  const payload = track(makeHeavyPayload(), "4-unrooted-island");
  document.querySelector("#scratch")?.addEventListener("click", () => payload.peek());
  // no reference to `payload` escapes this function
}

globalThis.gc();
globalThis.gc();

setTimeout(() => {
  console.log("collected:", collected);
  console.log("cache size:", leakedCache.length);   // never shrinks
  console.log("registered handlers:", Object.keys(handlers).length);
}, 200);
```

Expected shape of the output:

```
collected: [ '1-dropped', '4-unrooted-island' ]   // cycles collect fine
cache size: 1                                        // rooted → immortal
registered handlers: [ 'onScroll' ]                  // rooted → immortal
```

Two things this proves that a textbook can't:

- **Case 4 collects.** A node/listener cycle with no path from a root is garbage, exactly like case 1. If you'd trusted *"cycles leak,"* you'd have gone looking for the bug in the wrong place.
- **Cases 2 and 3 don't, for the same reason in both.** The only difference between them is *which* root holds the chain. That's why the diagnostic is always "follow the retainers to the root," never "find the cycle."

> **Caveat worth internalising:** GC timing is non-deterministic. `FinalizationRegistry` callbacks fire on a later macrotask, and a fast-moving runtime may never collect case 1 during a short run. That's *also* the lesson from Gotcha 3 — absence of collection in a two-second script is not proof of a leak.

---

### Atom 1.1.7 — IIFEs and the Module Pattern

#### The Problem This Solves

Before ES modules, every `<script>` tag on a page shared **one** global scope:

```html
<script src="jquery.js"></script>
<script src="utils.js"></script>
<script src="app.js"></script>
```

A top-level `var name = "utils"` in `utils.js` creates `window.name` and silently overwrites whatever another file put there — in load order, with no warning. Two files with the same variable name clobber each other, and there was no way to declare *"this file exposes these three things and hides everything else."*

The IIFE was the hand-rolled fix for exactly one of those problems. The module pattern fixed the other two. Knowing *which* problem each one solved is what tells you what to reach for in 2026.

#### The Mental Model

An IIFE doesn't do anything. It moves your variables out of the shared global scope **into a function scope** that dies when it returns.

The module pattern adds one step: that function **returns an object containing only the names you chose to publish.**

```
IIFE            = a private room
Module pattern  = a private room with a door you built
```

That's the whole idea, and there's nothing mysterious in it — you already wrote this exact code. It's `createCounter` from Atom 1.1.5 wearing a different hat, and recognising that is the point of this atom.

#### The Explanation

##### The IIFE

```javascript
(function () {
  "use strict";
  var secret = "nobody outside this function can see me";
  doSomething();
})();
```

Read it as: *a function expression, called on the spot.* Its variables are scoped to the call and vanish when it returns. `secret` never reaches `window`.

##### The module pattern — an IIFE that returns

```javascript
const Counter = (function () {
  let count = 0;                       // private: unreachable from outside

  return {
    increment: () => ++count,          // the only door out
    getCount:  () => count
  };
})();

Counter.increment();
Counter.increment();
console.log(Counter.getCount());      // 2
console.log(Counter.count);            // undefined — no such property exists
```

Compare that with your `createCounter` from 1.1.5. **It is the same function.** "Module pattern" is only the name people gave to *"an IIFE that returns an object"* — which is the universal shape of the closure factory: *declare a variable, return functions that close over it.*

##### Name the function

```javascript
(function counterModule () {      // ← named function expression
  let count = 0;
  return { get: () => count };
})();
```

An anonymous function expression appears as `anonymous` in every stack trace that passes through it. `at anonymous (app.js:412)` tells you nothing. `at counterModule (app.js:412)` tells you which module broke.

##### Why each piece existed — and what replaced it

| The problem | The pre-ESM answer | What replaced it |
|---|---|---|
| All `<script>` tags share one global scope | IIFE wrapper | module scope (automatic, per file) |
| No way to declare "these are public" | return an object | `export` |
| Need strict mode per file | `"use strict"` inside the IIFE | modules are strict by default |
| Node needs the same isolation | CommonJS wrapper | `require` / `module.exports` |
| Need a namespace across CDN bundles | UMD wrapper | bundlers |

**Node solved the identical problem with CommonJS.** Every `.js` file it loads is wrapped in a function whose parameters are `module`, `exports`, `require`, `__dirname`, `__filename`. CommonJS *is* an IIFE at the module-system level — which is why `require` and `module.exports` behave the way they do, and why you can hold a private `const` at the top of a CJS file without it becoming global. That's Atom 1.7.3.

##### Where you still see them

**1. The async IIFE — the one that's still worth writing.**

```javascript
(async () => {
  const user = await fetchUser();
  const posts = await fetchPosts(user.id);
  render(user, posts);
})().catch(handleError);
```

Top-level `await` only exists inside an ES module. In a classic `<script>` tag or a CommonJS file there's no such thing, so the standard shape is to wrap the file body in an async IIFE. Note the `.catch()`: without it, a rejection inside becomes an **unhandled promise rejection**, which in Node 15+ terminates the process by default. An async IIFE whose promise nobody holds is a floating promise — there is no later opportunity to catch it.

**2. Build-tool output.** Babel and webpack emit IIFE-shaped helpers constantly: `_typeof`, `_defineProperty`, UMD preambles. You'll meet these in `node_modules` forever, because the output still targets ES5.

**3. Legacy libraries.** jQuery plugins ship as `(function ($) { ... })(jQuery)`. Anything published before ~2015 for CDN support still uses a UMD wrapper.

**4. Loop scoping.** Version C from Atom 1.1.5:

```javascript
for (var i = 0; i < 3; i++) {
  handlers.push((function (j) { return () => j; })(i));
}
```

An IIFE used as a hand-made block scope. Use `let`.

#### Gotchas — Atom 1.1.7

1. **The module pattern gives privacy, not security.** `Counter.count` is `undefined` because you never returned it — not because anything is enforcing it. Anyone can mutate the internals of what you *did* return. It's private by omission, exactly like a C# `private` field that's reachable through a getter you wrote.

2. **The ASI hazard, which will actually bite you.** `(` after an expression parses as a **call** on that expression:

   ```javascript
   const previous = function () {}
   (function () { console.log("iife ran"); })()        // ❌ missing semicolon above

   // Parses as: previous( function () { ... }() )
   // Your IIFE becomes an argument instead. Silently wrong, no error thrown.
   ```

   Fix: `;(function () { ... })()` — a leading semicolon defensively terminates the previous statement.

3. **`this` inside a bare IIFE isn't what you'd guess.** In a classic script in sloppy mode, a top-level IIFE's `this` is `window`. In a module or under strict mode it's `undefined`. UMD wrappers exist partly because of this — they pass `this` in explicitly as a parameter: `(function (root, factory) { ... }(this, function () { ... }))`.

4. **The async IIFE's floating rejection.** Always terminate it with `.catch(...)`. Nothing else in your program holds that promise, so nothing else can catch it, and Node exits non-zero on an unhandled rejection. (Relatedly: `"use strict"` must be the *first* statement inside an IIFE — one line lower and it's just a string literal that does nothing.)

5. **An IIFE gives privacy only to things created inside it.** Assigning to `window` from within the IIFE is still global. The wrapper doesn't sandbox anything. And nested IIFEs are unreadable past two levels — that's the signal to use a real module.

#### Interview Questions — Atom 1.1.7

1. **"What is an IIFE, and why did we stop using them?"**
   An Immediately Invoked Function Expression — a function expression called on the spot, so its variables get function scope instead of landing in the shared global scope. We stopped using them for that purpose because ES modules give every file its own scope automatically, are strict by default, and have real `import`/`export`. The wrapper became pure ceremony. They persist in build output, UMD libraries, and as async IIFEs where top-level `await` is needed outside a module.

2. **"Explain the module pattern."**
   An IIFE that returns an object containing only the values you want public; everything else stays in the function's scope and is unreachable from outside, giving private state without a class. Its limitations are that it can't be extended and it's verbose. ESM named exports plus real `private` / `#field` syntax replaced both halves of it.

3. **"How is the module pattern different from `private` in C#?"**
   `private` is enforced by the compiler and the runtime. The module pattern's privacy is enforced by nothing — it's just the fact that you didn't return the variable. You can still mutate anything you did return. It's a convention, not a boundary.

4. **"Why did IIFEs exist before ES modules?"**
   Classic `<script>` tags share one global scope, so a top-level `var` in one file overwrites the same name in another in load order. An IIFE gave a file a private scope; returning an object from it gave that file an explicit public surface. Node's CommonJS wraps every file the same way, which is why `module` and `require` are effectively IIFE parameters.

5. **"When would you still write an IIFE today?"**
   Three cases: wrapping an entry file in an async IIFE to get `await` at the top level in a classic script or a CommonJS file; deliberately scoping a loop iteration when `let` isn't available; and reading third-party bundles, which are full of UMD wrappers and transpiler helpers.

6. **"What's the semicolon-before-IIFE thing about?"**
   JavaScript parses `(` following an expression as a call on that expression. So a missing semicolon on the previous line turns your IIFE into an argument to whatever came before it, silently and without error. The fix is a leading `;` — `;(function () {})()` — which terminates the previous statement regardless of what it was.

#### Code I Wrote — Atom 1.1.7

A `Counter` written three ways. The first is the historical module pattern; the second is the same thing as a plain closure factory (Atom 1.1.5's version, which needs no wrapper at all); the third is the ESM replacement with a real private field. All three behave identically.

```javascript
// 1. Module pattern — the pre-ESM answer. Note the name, for stack traces.
const CounterLegacy = (function counterModule () {
  let count = 0;                              // private by omission

  const increment = () => ++count;
  const getCount  = () => count;

  return { increment, getCount };
})();

// 2. Plain closure factory — the same idea, no IIFE needed since ES2015.
function createCounter() {
  let count = 0;
  return { increment: () => ++count, getCount: () => count };
}

// 3. ESM replacement — real privacy, enforced by the engine.
class Counter {
  #count = 0;                                 // genuinely unreachable
  increment() { return ++this.#count; }
  getCount()  { return this.#count; }
}
```

```javascript
// Verification: all three behave identically, and all three are opaque.
const implementations = [CounterLegacy, createCounter, () => new Counter()];

for (const makeCounter of implementations) {
  const counter = makeCounter();
  counter.increment();
  counter.increment();
  console.log(counter.getCount());            // 2 for every one of them
  console.log(counter.count);                 // undefined — no such property
}

// The async IIFE, with the .catch that keeps it from being a floating promise.
(async () => {
  try {
    const data = await Promise.resolve("loaded");
    console.log(data);
  } catch (error) {
    console.error("failed", error);
  }
})();
```

The comparison worth sitting with: **version 2 needs no wrapper at all.** A top-level function declaration already gives you a private scope and a named stack frame. The IIFE existed to make that scope *anonymous and temporary* — which was the point in 2005 (leave no names on `window`) and is the entire reason it's noise today.

---

## Code I Wrote (Unit Proof)

> **Placement note.** These three are the closure exercises the syllabus assigns to **Atom 1.1.5**. The atom section above explains the room/key model; this is the build record.

### once(fn) — Run a function only once

```javascript
function once(fn) {
  let called = false;
  let result;
  return function(...args) {
    if (called) return undefined;
    called = true;
    result = fn.apply(this, args); // `this` forwarding is covered in Atom 1.3.2
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
add(1, 2); // "cache hit"  → 3
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

| # | Build | Atom | Status |
|---|---|---|---|
| 1 | **`once(fn)`** | 1.1.5 — function factory + closure | Implemented ✓ |
| 2 | **`memoize(fn)`** | 1.1.5 — memoisation | Implemented ✓ |
| 3 | **Counter factory** | 1.1.5 — private state | Implemented ✓ |
| 4 | **Stack frame tracer** | 1.1.3 — runtime stack measurement | Implemented ✓ |
| 5 | **`leak-probe.js`** | 1.1.6 — root vs cycle, measured | Written, **not yet run** |
| 6 | **Three-way `Counter`** | 1.1.7 — module pattern / factory / `#private` | Written, **not yet run** |

The first four demonstrate closures. The last two make the first four *measurable* — one shows retention being released vs held, the other shows the same program written three ways.

**Self-check — can you answer these without looking?**

- [ ] Why does the `var` loop print 3, 3, 3 — and what does `let` change about memory?
- [ ] What are the GC roots, and why does "circular reference" not identify a leak?
- [ ] A heap snapshot shows a growing `Detached HTMLElement` — where do you look first, and what do you change?
- [ ] Why is an unremoved `setInterval` a leak even though the arrow it holds captures nothing?
- [ ] What does the module pattern actually give you that a plain closure factory doesn't?

*(Part 1's self-check covers atoms 1.1.1 → 1.1.4 — see `01-01-the-execution-model-part1.md`.)*

---

## Atom Coverage In This File

| Atom | Topic | Sections present |
|------|-------|------------------|
| 1.1.5 | Closures: what's retained, loop puzzle, real uses | Explanation, Gotchas, Interview Questions, Code I Wrote |
| 1.1.6 | Closures and memory leaks | Explanation, Gotchas, Interview Questions, Code I Wrote |
| 1.1.7 | IIFEs and module pattern | Explanation, Gotchas, Interview Questions, Code I Wrote |

**Gaps:**
- Atom 1.1.5, 1.1.6, 1.1.7 teach-back not yet done; left at `In Progress` in PROGRESS.md
- `leak-probe.js` and the three-way `Counter` are written but never executed — both make a claim that needs observing
- Unit 1.1 is complete at the notes level; nothing written yet for Unit 1.2 (Types and Coercion)

---

## Next: Unit 1.2 — Types and Coercion

Unit 1.1 is closed. You have the execution model end to end: hoisting and TDZ, the call stack, lexical scope, closures and what they retain, why retention becomes a leak, and what module scope is (and why IIFEs existed to fake it).

Unit 1.2 moves from *when things run* to *what things are*. It starts with Atom 1.2.1 — the 7 primitives plus object, and `typeof`'s famous lies (`typeof null === "object"`, `typeof function === "function"`). That atom is also the on-ramp to Atom 1.2.2, value vs reference semantics, which is where "why did my React prop change?" comes from.