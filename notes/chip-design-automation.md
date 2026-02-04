# Chip Design Automation Project

## Current Status
Working on constraint handling system and feasible operating point visualization.

---

## Constraints Handling

### User Input Model
- Users construct constraint equations directly as expressions
- Enter constraints as a long line/expression format
- These are **objective truths** the program must respect
- NOT custom functions - pure constraint equations only
- Program handles parsing and enforcement internally

### Constraint Types (KVL/KCL Based)
- **Topology constraints**: How devices are connected, which terminals connect to which
- **Voltage constraints**: Certain voltages on one device equal to voltages on another device
- **Supply constraints**: Expectations based on supply voltage or output DC bias level
- **KVL equations**: Kirchhoff's Voltage Law around loops
- **KCL equations**: Kirchhoff's Current Law at nodes

### Visualization Requirements
- Display what the constraints are
- Show how constraints are affecting the solution space
- Visual feedback on feasibility

---

## Objectives - Two Levels

### Device Level Objectives
Examples:
- **Minimize drain current (Id)** - power efficiency
- **Maximize gm/Id** - transconductance efficiency
- **Maximize self_gain** - ensure high intrinsic gain capability
- **Maximize output resistance (rout)** - especially for mirror devices in first gain stage

### Circuit Level Objectives
Examples:
- **Gain** - overall amplifier gain
- **Power** - total power consumption
- **Bandwidth** - circuit-level frequency response
- **Noise** - input-referred noise

### Benefits of Separation
- Easier to generate **Pareto plots at device level**
- Circuit level metrics update dynamically as devices get biased
- Cleaner separation of concerns
- Can optimize devices individually then see circuit impact

---

## Feasible Operating Point Visualization

### The Problem
- Have a **huge database of operating points** from sweeps
- Need to see what the **feasible solution space** is after applying constraints
- When one device is biased, it **limits feasible points for connected devices**
- Need to know: which additional sweeps would expand the solution space?

### Visualization Ideas

#### 1. Constrained Solution Space View
- Show all operating points in database
- Highlight/filter to show only **feasible points** after constraints applied
- Color coding: feasible (green) vs infeasible (red/gray)
- Animated filtering as constraints are added

#### 2. Dependency Chain Visualization
- When Device A is biased → show how it limits Device B's feasible space
- Tree/graph view of device dependencies
- Click a device to see its feasible operating points given current constraints

#### 3. Sweep Recommendation Engine
- Analyze current feasible space
- Identify which device has the **most constrained** solution space
- Recommend: "Sweep Device X with parameters Y to expand feasible region"
- Show predicted expansion of solution space

#### 4. Pareto Frontier Display
- For device-level objectives (gm/Id vs Id, self_gain vs power)
- Show Pareto-optimal operating points
- Allow selection from Pareto frontier
- Update circuit-level metrics in real-time as selections change

#### 5. Constraint Conflict Detection
- If constraints make solution space **empty** → highlight conflicting constraints
- Suggest which constraint to relax
- Show sensitivity: which constraint is most limiting?

---

## Interactive Workflow Concept

```
1. Load operating point database
2. Define circuit topology (which devices connect where)
3. Enter constraint equations (KVL/KCL based)
   → System shows feasible operating points per device
4. Set device-level objectives
   → System shows Pareto frontiers for each device
5. Select bias points from feasible Pareto regions
   → As each device is biased, connected devices update
   → Feasible space for unbiased devices shrinks/updates
6. If solution space too small:
   → System recommends additional sweeps
   → Shows which parameters to sweep and expected benefit
7. Set circuit-level objectives
   → System evaluates overall circuit performance
   → Iterate on bias points to optimize circuit metrics
```

---

## Technical Considerations

### Data Structure for Operating Points
- Device ID, topology position
- All DCOP parameters: gm, gds, rout, cgs, cgd, ft, id, vdsat, vth, vgs, vgt, gmoverid, self_gain
- Sweep parameters that generated this point
- Feasibility flag (updated as constraints applied)

### Constraint Parser
- Parse user expressions into symbolic equations
- Support device parameter references: `M1.vgs`, `M2.id`, etc.
- Support basic operators: `=`, `<`, `>`, `<=`, `>=`
- Support arithmetic: `+`, `-`, `*`, `/`
- Example: `M1.vgs = M2.vgs + 0.1` or `M1.id < 100u`

### Dependency Graph
- Build graph of device connections
- When device biased → propagate constraints to connected devices
- Recompute feasible sets incrementally

---

*Last updated: 2026-02-04 ~1:40 PM EST*
*Added: Feasible operating point visualization, sweep recommendations, dependency tracking*
