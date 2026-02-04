# Chip Design Automation Project

## Current Status
Working on constraint handling system.

## Constraints Handling - Ideas

### User Input
- Users should construct constraint equations directly
- Enter constraints as a long line/expression
- These are objective truths the program must respect
- NOT custom functions - just pure constraint equations
- Program handles parsing and enforcement from there

### Visualization Needs
- Want the program to visualize/display:
  - What the constraints are
  - How they're affecting things
- Still figuring out the best approach

## Objectives - Two Levels

### Device Level Objectives
- Set objectives at the device level separately
- Enables Pareto plots at device level when needed
- Device biasing considerations

### Circuit Level Objectives
- Set objectives at the circuit level separately
- Generate circuit level performance metrics as they become available

### Benefits of Separation
- Easier to generate Pareto plots at device level
- Circuit level performance metrics update as devices get biased
- Cleaner separation of concerns

---

*Last updated: 2026-02-04*
