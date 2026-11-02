"""
Generates sde1_study_plan.xlsx - a week-by-week planner for the priority
SDE-1 modules, with a "flex week" after every N units so that a missed
target can be absorbed instead of cascading.

Run:  python generate_syllabus_plan.py
"""

from datetime import datetime, timedelta

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# --------------------------------------------------------------------------
# CONFIG  -- tweak these
# --------------------------------------------------------------------------
START_DATE = datetime(2026, 9, 28)   # Monday of week 1

# A flex week is inserted after every FLEX_EVERY_UNITS units.
#   1 = flex after every unit    (max slack, ~20 months)
#   2 = flex after every 2 units (~15 months)  <- default
#   0 = no flex weeks            (tight schedule)
FLEX_EVERY_UNITS = 2

# Weeks of tail time for consolidation / spaced revision / interview drills
TAIL_WEEKS = 2

# Nominal study pace per module: how many units you try to cover per week.
# Keep this at 1.0 for the "deep" modules and 1.5-2.0 for lighter ones.
UNITS_PER_WEEK = {
    "JavaScript": 1.5,
    "C# and OOP": 1.5,
    "React": 1.5,
    "ASP.NET Core": 1.0,
    "LLD": 1.0,
    "Multithreading & Concurrency": 1.0,
    "High-Level Design": 1.0,
}

MODULES = [
    ("JavaScript", [
        "1.1  The Execution Model",
        "1.2  Types and Coercion",
        "1.3  Functions and `this`",
        "1.4  Objects and Prototypes",
        "1.5  Arrays and Data Transformation",
        "1.6  Asynchronous JavaScript",
        "1.7  Modules and Tooling",
        "1.8  Browser, DOM and Networking",
        "1.9  Modern Syntax and Advanced Corners",
        "1.10  TypeScript",
    ]),
    ("React", [
        "6.1  The Mental Model",
        "6.2  State",
        "6.3  Effects and the Outside World",
        "6.4  Refs, Context and Escape Hatches",
        "6.5  Custom Hooks",
        "6.6  Performance",
        "6.7  Forms, Data and Routing",
        "6.8  Rendering Strategies and Beyond",
    ]),
    ("C# and OOP", [
        "3.1  The Type System and Memory",
        "3.2  Object-Oriented Programming Properly",
        "3.3  Generics and Collections",
        "3.4  Delegates, Lambdas and LINQ",
        "3.5  Modern C# Language Features",
        "3.6  Exceptions and Defensive Code",
    ]),
    ("ASP.NET Core", [
        "8.1  Foundations and the Request Pipeline",
        "8.2  Dependency Injection and Configuration",
        "8.3  Building APIs",
        "8.4  Entity Framework Core and Data Access",
        "8.5  Authentication and Authorisation",
        "8.6  Cross-Cutting Concerns",
        "8.7  Architecture and Testing",
    ]),
    ("LLD", [
        "14.1  Design Principles",
        "14.2  Modelling and Diagrams",
        "14.3  Creational Patterns",
        "14.4  Structural Patterns",
        "14.5  Behavioural Patterns",
        "14.6  Code Smells and Refactoring",
        "14.7  LLD Problem Set",
    ]),
    ("Multithreading & Concurrency", [
        "15.1  Foundations",
        "15.2  Shared State and Its Hazards",
        "15.3  Synchronisation Primitives in C#",
        "15.4  Tasks and async/await Deeply",
        "15.5  Concurrent Collections and Data Parallelism",
        "15.6  Concurrency Patterns",
        "15.7  Debugging and Testing Concurrency",
    ]),
    ("High-Level Design", [
        "16.1  Fundamentals",
        "16.2  The Building Blocks",
        "16.3  Distributed Systems Concepts",
        "16.4  Architecture Styles and Operations",
        "16.5  Case Studies",
    ]),
]

# Priority order drives the sequence and the colour ramp
PRIORITY = [
    ("JavaScript", "C6EFCE"),
    ("React", "D9EAD3"),
    ("C# and OOP", "D6E4F0"),
    ("ASP.NET Core", "BDD7EE"),
    ("LLD", "FCE4D6"),
    ("Multithreading & Concurrency", "F8CBAD"),
    ("High-Level Design", "E4DFEC"),
]
COLOR = dict(PRIORITY)
PRIORITY_RANK = {name: i + 1 for i, (name, _) in enumerate(PRIORITY)}

STUDY, FLEX, TAIL = "Study", "Flex", "Consolidation"

# --------------------------------------------------------------------------
# BUILD THE SCHEDULE
# --------------------------------------------------------------------------
# Each row is (module, label, kind, [week indices])
rows = []
cursor = 0
module_spans = {}

for mod, units in MODULES:
    start_wk = cursor
    pace = UNITS_PER_WEEK[mod]              # units covered per week
    n = len(units)
    total = max(1, min(n, round(n / pace)))  # study weeks for this module
    # spread n units over `total` weeks: q units in the first `rem` weeks, q+1 after
    q, rem = divmod(n, total)
    week_of_unit = []
    for w in range(total):
        take = q + 1 if w < rem else q
        week_of_unit.extend([cursor + w] * take)
    cursor += total

    for i, unit in enumerate(units):
        rows.append([mod, unit, STUDY, [week_of_unit[i]]])

        if FLEX_EVERY_UNITS and (i + 1) % FLEX_EVERY_UNITS == 0 and i != len(units) - 1:
            rows.append([mod, f"flex  -  absorb any slip from '{unit}'", FLEX, [cursor]])
            cursor += 1

    if FLEX_EVERY_UNITS:
        rows.append([mod, "flex  -  module catch-up week", FLEX, [cursor]])
        cursor += 1
    module_spans[mod] = (start_wk, cursor)

for i in range(TAIL_WEEKS):
    rows.append(["Consolidation", "Spaced revision, review deck, interview drills", TAIL, [cursor]])
    cursor += 1

NUM_WEEKS = cursor
week_dates = [START_DATE + timedelta(weeks=i) for i in range(NUM_WEEKS)]
END_DATE = week_dates[-1] + timedelta(days=6)

# --------------------------------------------------------------------------
# STYLES
# --------------------------------------------------------------------------
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

HDR_FILL = PatternFill("solid", start_color="1F4E79", end_color="1F4E79")
HDR_FONT = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
FLEX_FILL = PatternFill("solid", start_color="FFF2CC", end_color="FFF2CC")
TAIL_FILL = PatternFill("solid", start_color="EDEDED", end_color="EDEDED")
DONE_FILL = PatternFill("solid", start_color="C6EFCE", end_color="C6EFCE")
WIP_FILL = PatternFill("solid", start_color="FFEB9C", end_color="FFEB9C")

# --------------------------------------------------------------------------
# SHEET 1 - the plan
# --------------------------------------------------------------------------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Study Plan"

FIXED_COLS = ["Module", "Unit", "Type", "Status", "Done", "Notes"]
W0 = len(FIXED_COLS) + 1  # first week column index

TITLE_R, SUB_R, HDR_R, DATE_R = 1, 2, 4, 5
DATA_R = 6

ws.merge_cells(start_row=TITLE_R, start_column=1, end_row=TITLE_R, end_column=W0 + NUM_WEEKS - 1)
t = ws.cell(TITLE_R, 1, "SDE-1  |  Priority Module Study Plan")
t.font = Font(name="Calibri", bold=True, size=16, color="1F4E79")
t.alignment = Alignment(horizontal="center")

ws.merge_cells(start_row=SUB_R, start_column=1, end_row=SUB_R, end_column=W0 + NUM_WEEKS - 1)
s = ws.cell(
    SUB_R, 1,
    f"{START_DATE:%d %b %Y}  ->  {END_DATE:%d %b %Y}   |   {NUM_WEEKS} weeks   |   "
    f"Order: JavaScript > React > C#/OOP > ASP.NET Core > LLD > Concurrency > HLD",
)
s.font = Font(name="Calibri", size=10, italic=True, color="595959")
s.alignment = Alignment(horizontal="center")

# headers
for c, h in enumerate(FIXED_COLS, 1):
    cell = ws.cell(HDR_R, c, h)
    cell.font = HDR_FONT
    cell.fill = HDR_FILL
    cell.border = BORDER
    cell.alignment = Alignment(horizontal="center", vertical="center")

for i in range(NUM_WEEKS):
    cell = ws.cell(HDR_R, W0 + i, f"W{i + 1}")
    cell.font = HDR_FONT
    cell.fill = HDR_FILL
    cell.border = BORDER
    cell.alignment = Alignment(horizontal="center")

    d = ws.cell(DATE_R, W0 + i, week_dates[i].strftime("%d %b"))
    d.font = Font(name="Calibri", size=8, italic=True, color="1F4E79")
    d.alignment = Alignment(horizontal="center")
    d.border = BORDER

for c in range(1, W0):
    ws.cell(DATE_R, c, "").border = BORDER

# data
r = DATA_R
for mod, label, kind, weeks in rows:
    fill = PatternFill("solid", start_color=COLOR.get(mod, "FFFFFF"), end_color=COLOR.get(mod, "FFFFFF"))

    ws.cell(r, 1, mod if kind == STUDY else "").font = Font(bold=True, size=10)
    ws.cell(r, 2, label)
    ws.cell(r, 3, kind)
    ws.cell(r, 4, "Not started")
    ws.cell(r, 5, "")
    ws.cell(r, 6, "")

    for c in range(1, W0):
        cell = ws.cell(r, c)
        cell.border = BORDER
        cell.alignment = Alignment(vertical="center", wrap_text=(c in (1, 2, 6)))
        if c == 1 and kind == STUDY:
            cell.fill = fill
        if c == 3:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = Font(size=9, italic=True, color="808080")
    ws.cell(r, 4).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(r, 5).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(r, 5).number_format = "dd mmm"

    for w in weeks:
        cell = ws.cell(r, W0 + w)
        cell.border = BORDER
        cell.alignment = Alignment(horizontal="center", vertical="center")
        if kind == STUDY:
            cell.value = "\u25a0"          # filled square
            cell.fill = fill
            cell.font = Font(size=11, color="404040")
        elif kind == FLEX:
            cell.value = "\u25cb"          # open circle = up for grabs
            cell.fill = FLEX_FILL
            cell.font = Font(size=11, color="BF9000")
        else:
            cell.value = "\u25c6"
            cell.fill = TAIL_FILL
    r += 1

LAST_R = r - 1

# status dropdown + date validation
dv = DataValidation(
    type="list",
    formula1='"Not started,In progress,Done,Skipped"',
    allow_blank=True,
    showDropDown=False,
)
ws.add_data_validation(dv)
dv.add(f"D{DATA_R}:D{LAST_R}")

dv_date = DataValidation(type="date", operator="between",
                         formula1="DATE(2026,1,1)", formula2="DATE(2030,12,31)", allow_blank=True)
ws.add_data_validation(dv_date)
dv_date.add(f"E{DATA_R}:E{LAST_R}")

# conditional formatting on status
ws.conditional_formatting.add(
    f"D{DATA_R}:D{LAST_R}",
    openpyxl.formatting.rule.CellIsRule(operator="equal", formula=['"Done"'], fill=DONE_FILL),
)
ws.conditional_formatting.add(
    f"D{DATA_R}:D{LAST_R}",
    openpyxl.formatting.rule.CellIsRule(operator="equal", formula=['"In progress"'], fill=WIP_FILL),
)

# column widths
ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 46
ws.column_dimensions["C"].width = 9
ws.column_dimensions["D"].width = 12
ws.column_dimensions["E"].width = 10
ws.column_dimensions["F"].width = 30
for i in range(NUM_WEEKS):
    ws.column_dimensions[get_column_letter(W0 + i)].width = 3.4

ws.row_dimensions[HDR_R].height = 22
ws.row_dimensions[DATE_R].height = 13
ws.freeze_panes = ws.cell(DATA_R, W0)
ws.auto_filter.ref = f"A{HDR_R}:{get_column_letter(W0 + NUM_WEEKS - 1)}{LAST_R}"
ws.sheet_view.showGridLines = False

# --------------------------------------------------------------------------
# SHEET 2 - how to use
# --------------------------------------------------------------------------
ws2 = wb.create_sheet("How to use")
ws2.column_dimensions["A"].width = 26
ws2.column_dimensions["B"].width = 95
ws2.sheet_view.showGridLines = False

ws2["A1"] = "How to use this plan"
ws2["A1"].font = Font(size=15, bold=True, color="1F4E79")
ws2.merge_cells("A1:B1")

notes = [
    ("Legend", ""),
    ("\u25a0  Study week", "A week reserved for that unit. The cell is tinted with the module colour."),
    ("\u25cb  Flex week", "Empty capacity. If the unit above slipped, move it into this week. "
                          "If it didn't, treat it as a lighter week (revision, review deck, catch up on reading) and carry on."),
    ("\u25c6  Consolidation", "Tail weeks for spaced revision and interview drills."),
    ("", ""),
    ("When you fall behind", ""),
    ("1", "Do NOT re-plan the whole sheet. Just drag the missed unit's work down into the next \u25cb flex week."),
    ("2", "If two units slip into the same flex week, the following unit's block absorbs it - split the days."),
    ("3", "Set Status to 'In progress' the week you start, 'Done' when you can explain it out loud "
          "(not when you finish reading)."),
    ("4", "Only once two consecutive flex weeks go unused should you consider pulling the schedule forward."),
    ("", ""),
    ("Columns", ""),
    ("Status", "Dropdown: Not started / In progress / Done / Skipped."),
    ("Done", "Date you actually closed the unit. Use it to see real pace vs plan."),
    ("Notes", "What broke, what you couldn't explain, what to redo."),
    ("", ""),
    ("Re-planning", ""),
    ("To rebuild with different pacing", "Edit UNITS_PER_WEEK (study pace per module) or FLEX_EVERY_UNITS "
                                        "(1 = flex after every unit, 2 = every 2nd, 0 = none) at the top of the "
                                        "script and re-run it."),
    ("To start on a different Monday", "Change START_DATE and re-run."),
]

r2 = 3
for k, v in notes:
    a = ws2.cell(r2, 1, k)
    b = ws2.cell(r2, 2, v)
    b.alignment = Alignment(wrap_text=True, vertical="top")
    a.alignment = Alignment(vertical="top")
    if v == "" and k:
        a.font = Font(bold=True, size=11, color="1F4E79")
        a.border = Border(bottom=thin)
    else:
        a.font = Font(bold=True, size=10)
    if r2 == 3:
        a.font = Font(bold=True, size=11, color="1F4E79")
    r2 += 1

# legend colours
r2 += 1
ws2.cell(r2, 1, "Module order").font = Font(bold=True, size=11, color="1F4E79")
r2 += 1
for name, hexcol in PRIORITY:
    c = ws2.cell(r2, 1, f"#{PRIORITY_RANK[name]}  {name}")
    c.fill = PatternFill("solid", start_color=hexcol, end_color=hexcol)
    c.font = Font(bold=True, size=10)
    c.border = BORDER
    lo, hi = module_spans.get(name, (0, 0))
    ws2.cell(r2, 2, f"W{lo + 1}\u2013W{hi}  ({hi - lo} weeks incl. flex)").font = Font(size=10)
    r2 += 1

ws2.cell(r2 + 1, 1, "Total").font = Font(bold=True, size=10)
ws2.cell(r2 + 1, 2, f"{NUM_WEEKS} weeks  |  {START_DATE:%d %b %Y} \u2192 {END_DATE:%d %b %Y}").font = Font(bold=True, size=10)

# --------------------------------------------------------------------------
out = "sde1_study_plan.xlsx"
wb.save(out)

print(f"Created : {out}")
print(f"Range   : {START_DATE:%d %b %Y} -> {END_DATE:%d %b %Y}  ({NUM_WEEKS} weeks)")
print(f"Rows    : {len(rows)} ({sum(1 for x in rows if x[2] == STUDY)} units, "
      f"{sum(1 for x in rows if x[2] == FLEX)} flex, {TAIL_WEEKS} consolidation)")
print()
for name, _ in PRIORITY:
    lo, hi = module_spans[name]
    print(f"  {PRIORITY_RANK[name]}. {name:<30} W{lo + 1:>2}-W{hi:<2}  ({hi - lo} wks)")
