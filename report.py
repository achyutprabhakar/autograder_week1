from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

out = "/mnt/data/agentic01.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=19, leading=24, alignment=TA_CENTER, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"], fontSize=10, leading=14,
    alignment=TA_CENTER, textColor=colors.HexColor("#444444"), spaceAfter=16
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontSize=13, leading=16,
    textColor=colors.HexColor("#17365D"), spaceBefore=10, spaceAfter=6
))
styles.add(ParagraphStyle(
    name="SubSection", parent=styles["Heading2"], fontSize=10.5, leading=13,
    spaceBefore=6, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"], fontSize=9.3, leading=13,
    spaceAfter=5
))
styles.add(ParagraphStyle(
    name="SmallCustom", parent=styles["BodyText"], fontSize=8, leading=10,
    spaceAfter=3
))
styles.add(ParagraphStyle(
    name="Cell", parent=styles["BodyText"], fontSize=8, leading=10
))
styles.add(ParagraphStyle(
    name="CellHead", parent=styles["BodyText"], fontName="Helvetica-Bold",
    fontSize=8, leading=10, textColor=colors.white
))

def P(txt, style="BodyCustom"):
    return Paragraph(txt, styles[style])

doc = SimpleDocTemplate(
    out, pagesize=A4, rightMargin=1.7*cm, leftMargin=1.7*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm,
    title="AutoGrader Progress Report - agentic01",
    author="Project Team"
)

story = []
story.append(Spacer(1, 0.3*cm))
story.append(P("AutoGrader: A Rule-Driven Evaluator for C Programs", "ReportTitle"))
story.append(P("Implementation Plan, Workload Distribution, Progress and Future Timeline", "Subtitle"))

meta = [
    [P("<b>Course / Lab</b>", "Cell"), P("Computing Lab / Agentic Project", "Cell")],
    [P("<b>Report</b>", "Cell"), P("agentic01.pdf — Progress Report", "Cell")],
    [P("<b>Project duration</b>", "Cell"), P("4 weeks (planned)", "Cell")],
    [P("<b>Team members</b>", "Cell"), P("Add names and roll numbers before submission", "Cell")],
]
t = Table(meta, colWidths=[4.0*cm, 12.0*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#EAF0F7")),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#B7C4D3")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 7),
    ("RIGHTPADDING", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.35*cm))

story.append(P("1. Project Overview", "Section"))
story.append(P(
    "The objective is to develop an automated evaluator for C programming submissions. "
    "The system should compile and run a submitted program against instructor-defined test cases, "
    "apply configurable grading rules, and produce a clear report. The design is intended to keep "
    "problem rules, tests, thresholds and scoring configuration outside the core Python code so that "
    "instructors can modify them without rewriting the evaluator.", "BodyCustom"
))
story.append(P("Planned capabilities", "SubSection"))
for item in [
    "Compile submitted C source files and record compiler output.",
    "Run test cases with expected input/output and a time limit; identify failures and runtime errors.",
    "Load rules and test cases from editable configuration files.",
    "Calculate a score and produce machine-readable JSON and human-readable text reports.",
    "Extend the prototype with independent analyzers for correctness, efficiency, code structure and similarity/originality indicators.",
    "Explain incorrect results using test input, expected output and actual output where available.",
    "Evaluate safety, usefulness and limitations with concrete examples."
]:
    story.append(P("• " + item, "BodyCustom"))

story.append(P("2. Implementation Plan and Architecture", "Section"))
story.append(P(
    "The initial implementation uses Python as the coordinator and GCC as the C compiler. "
    "The planned pipeline is: (1) read submission and configuration, (2) compile the source, "
    "(3) execute the compiled program for each test, (4) compare output and check runtime limits, "
    "(5) compute the score, and (6) save the report. Later stages will add separate analyzers and "
    "a configurable weighted aggregation layer.", "BodyCustom"
))
arch = [
    [P("Component", "CellHead"), P("Purpose", "CellHead"), P("Current / planned status", "CellHead")],
    [P("main.py", "Cell"), P("Coordinates compilation, test execution, scoring and report creation.", "Cell"), P("Basic Week 1 prototype exists.", "Cell")],
    [P("config/rules.json", "Cell"), P("Stores compiler flags, runtime limit and grading configuration.", "Cell"), P("Exists; memory limit is configured but not enforced yet.", "Cell")],
    [P("tests/tests.json", "Cell"), P("Stores test inputs and expected outputs.", "Cell"), P("Three integer-addition cases included.", "Cell")],
    [P("submissions/add.c", "Cell"), P("Sample submission used for a smoke test.", "Cell"), P("Included.", "Cell")],
    [P("reports/", "Cell"), P("Stores JSON and text grading reports.", "Cell"), P("Report generation works, including error details in JSON.", "Cell")],
    [P("Analyzers and weighted score", "Cell"), P("Independent correctness, complexity, structure and similarity checks.", "Cell"), P("Planned for Weeks 2–3.", "Cell")],
]
at = Table(arch, colWidths=[3.2*cm, 7.2*cm, 5.6*cm], repeatRows=1)
at.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365D")),
    ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#B7C4D3")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(at)

story.append(P("3. Progress Achieved So Far", "Section"))
story.append(P(
    "A Week 1 starter prototype has been created with a Python driver, external JSON configuration, "
    "sample C submission, three test cases, and JSON/text report generation. The test cases cover "
    "ordinary positive inputs, zero values, and a negative input. The project is structured so that "
    "configuration and tests are not hardcoded into the Python coordinator.", "BodyCustom"
))
progress = [
    [P("Task", "CellHead"), P("Progress / evidence", "CellHead"), P("Status", "CellHead")],
    [P("Project skeleton", "Cell"), P("main.py, config/rules.json, tests/tests.json, submissions/add.c, README and report output paths.", "Cell"), P("Completed", "Cell")],
    [P("Compilation", "Cell"), P("Local run report shows GCC returned code 0 with no compiler errors.", "Cell"), P("Verified", "Cell")],
    [P("Test execution", "Cell"), P("Current Windows run is blocked when the compiled executable is launched.", "Cell"), P("Blocked", "Cell")],
    [P("Error diagnosis", "Cell"), P("Report identifies [WinError 4551] — an Application Control policy blocked the executable; zero tests ran.", "Cell"), P("Identified", "Cell")],
    [P("Scoring and reports", "Cell"), P("Report files are generated, but this failed run shows 0/0 tests and a zero score because execution did not start.", "Cell"), P("Partially verified", "Cell")],
    [P("Advanced analyzers / sandbox", "Cell"), P("Not implemented in the current prototype.", "Cell"), P("Pending", "Cell")],
]
pt = Table(progress, colWidths=[3.0*cm, 10.0*cm, 3.0*cm], repeatRows=1)
pt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365D")),
    ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#B7C4D3")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(pt)
story.append(Spacer(1, 0.15*cm))
story.append(P(
    "<b>Current issue and next action:</b> GCC compilation succeeds, but Windows Application Control blocks "
    "execution of the generated program. The team will investigate the approved execution environment or "
    "seek administrator approval if the device is managed. The policy will not be bypassed. Until execution "
    "is permitted, the end-to-end test result cannot be considered verified.", "BodyCustom"
))

story.append(P("4. Proposed Workload Distribution", "Section"))
story.append(P(
    "The table below is a suggested division for a team of up to four. Replace Member 1–4 with actual "
    "names and roll numbers, and adjust the division to match the work actually agreed by the team. "
    "For a smaller team, combine responsibilities.", "BodyCustom"
))
work = [
    [P("Team role", "CellHead"), P("Primary responsibilities", "Cell"), P("Main outputs", "Cell")],
    [P("Member 1 — Core system", "Cell"), P("Python coordinator, compilation pipeline, command-line interface and integration.", "Cell"), P("Working main.py and integration notes.", "Cell")],
    [P("Member 2 — Testing and reliability", "Cell"), P("Test-case format, output comparison, timeouts, runtime failures and safe-execution research.", "Cell"), P("Test suite and reliability tests.", "Cell")],
    [P("Member 3 — Rules and scoring", "Cell"), P("Editable rules, metrics, thresholds, weights and score aggregation.", "Cell"), P("Example rule sets and scoring module.", "Cell")],
    [P("Member 4 — Evaluation and documentation", "Cell"), P("Sample submissions, validation, similarity-analysis research, usefulness/limitations report, README and demo.", "Cell"), P("Evaluation cases, installation guide and presentation/video.", "Cell")],
]
wt = Table(work, colWidths=[3.7*cm, 7.5*cm, 4.8*cm], repeatRows=1)
wt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365D")),
    ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#B7C4D3")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(wt)

story.append(P("5. Future Timeline (Four Weeks)", "Section"))
timeline = [
    [P("Week", "CellHead"), P("Planned work", "Cell"), P("Expected milestone", "Cell")],
    [P("Week 1 — Foundation", "Cell"), P("Finalize the architecture; maintain editable rules and tests; make compile/run/test flow work in an approved environment; improve error reporting.", "Cell"), P("Reliable baseline that grades the sample program end-to-end.", "Cell")],
    [P("Week 2 — Reliability and safety", "Cell"), P("Handle compilation errors, wrong answers, crashes and timeouts; add boundary/edge tests; investigate OS-level isolation and enforce resource limits where feasible.", "Cell"), P("Robust execution and correctness test suite.", "Cell")],
    [P("Week 3 — Scoring and analysis", "Cell"), P("Implement analyzer interfaces, configurable weighted scoring, clearer counterexample feedback, basic code metrics and similarity indicators.", "Cell"), P("Combined score and explainable reports.", "Cell")],
    [P("Week 4 — Integration and delivery", "Cell"), P("Test with correct and incorrect submissions; document strengths and limitations with concrete cases; finalize README/installation guide, GitHub repository and 15–20 minute demonstration video.", "Cell"), P("Integrated project and final deliverables.", "Cell")],
]
tt = Table(timeline, colWidths=[3.0*cm, 8.5*cm, 4.5*cm], repeatRows=1)
tt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365D")),
    ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#B7C4D3")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(tt)

story.append(P("6. Risks, Limitations and Mitigation", "Section"))
risks = [
    ("Execution blocked by Windows policy", "The current environment compiles but cannot launch the binary. Use an approved environment or request administrator approval; do not bypass institutional controls."),
    ("Untrusted C programs", "A subprocess timeout alone is not a secure sandbox. Add OS/container/VM isolation and resource restrictions before evaluating untrusted code."),
    ("Memory limit not enforced", "The current JSON contains a memory-limit setting, but the prototype does not enforce it. Implement and test enforcement before describing it as a supported feature."),
    ("Similarity/plagiarism detection uncertainty", "Similarity signals can produce false positives and false negatives. Treat them as review flags, not definitive proof of misconduct."),
    ("Limited test coverage", "Three addition tests are only a smoke test. Expand to boundary values, invalid cases where relevant, overflow policy and diverse sample submissions."),
]
for title, desc in risks:
    story.append(P(f"<b>{title}:</b> {desc}", "BodyCustom"))

story.append(P("7. Immediate Next Steps", "Section"))
for item in [
    "Replace team-role placeholders with the actual members’ names and roll numbers.",
    "Resolve the approved execution-environment issue and confirm the sample passes all three tests.",
    "Add at least one deliberately incorrect program and one program that fails to compile to validate report behavior.",
    "Track changes in Git and publish the repository with setup instructions when ready.",
    "Update this report at each weekly evaluation to distinguish completed work from planned work."
]:
    story.append(P("• " + item, "BodyCustom"))

story.append(Spacer(1, 0.2*cm))
story.append(P(
    "<b>Progress summary:</b> The Week 1 project structure, configurable test inputs, GCC compilation and report generation are in place. "
    "End-to-end execution remains blocked by a Windows Application Control policy, and the advanced analyzers and secure sandbox are future work. "
    "This report intentionally records that limitation rather than claiming unverified functionality.", "BodyCustom"
))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(1.7*cm, 0.8*cm, "AutoGrader — Progress Report (agentic01)")
    canvas.drawRightString(A4[0] - 1.7*cm, 0.8*cm, f"Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)

print(f"Created: {out}")
print(f"Size: {os.path.getsize(out)} bytes")
