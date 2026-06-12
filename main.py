"""
=============================================================
  WAREHOUSE ROBOT TASK SCHEDULER USING AI TECHNIQUES
  =====================================================
  A complete academic AI project demonstrating:
    CO1 - Problem Formulation & Environment Modeling
    CO2 - Search Algorithms (BFS, DFS, UCS, A*)
    CO3 - Constraint Satisfaction (CSP Scheduling)
    CO4 - Utility-Based & Multi-Agent Decisions
    CO5 - Probabilistic Reasoning (Bayesian)
    CO6 - Hybrid AI Architecture

  Author   : [Your Name]
  Course   : Artificial Intelligence
  Date     : 2024
=============================================================
"""

import sys
import time

# ── Module imports ──────────────────────────────────────
from modules.co1_environment import (
    WarehouseState, RobotState, Task, Position,
    TraceLogger, display_peas_model, display_environment_types,
    build_adjacency_graph, display_graph_info, ACTIONS
)
from modules.co2_search import (
    bfs, dfs, ucs, astar, compare_algorithms, display_path_on_grid
)
from modules.co3_csp import (
    CSPScheduler, display_schedule, explain_csp_concepts
)
from modules.co4_utility import run_co4_demo
from modules.co5_probabilistic import run_co5_demo
from modules.co6_hybrid import HybridAISystem, display_co_mapping
from modules.grid_display import display_grid, customize_grid


# ─────────────────────────────────────────────────────────
# DEFAULT WAREHOUSE SETUP
# ─────────────────────────────────────────────────────────

def create_default_warehouse() -> WarehouseState:
    """
    Create the default 5×6 warehouse scenario.
    Layout:
      R1  .   .   X   .   T1
       .  .   .   .   .   .
       .  X   .   .   T2  .
       .  .   .   X   .   .
      R2  .   .   .   .   D
    """
    ROWS, COLS = 5, 6

    robots = {
        "R1": RobotState("R1", Position(0, 0), battery=85),
        "R2": RobotState("R2", Position(4, 0), battery=60),
    }

    tasks = {
        "T1": Task("T1", pickup=Position(0, 5), dropoff=Position(4, 5), priority=3),
        "T2": Task("T2", pickup=Position(2, 4), dropoff=Position(4, 5), priority=2),
    }

    obstacles: set = {
        (0, 3), (1, 3),           # vertical wall segment
        (2, 1),                    # shelf
        (3, 3),                    # another obstacle
    }

    delivery_zone = Position(4, 5)

    return WarehouseState(
        robots=robots,
        tasks=tasks,
        obstacles=obstacles,
        delivery_zone=delivery_zone,
        grid_rows=ROWS,
        grid_cols=COLS,
    )


# ─────────────────────────────────────────────────────────
# MENU SYSTEM
# ─────────────────────────────────────────────────────────

def print_banner():
    print("\n" + "█"*62)
    print("█" + " "*60 + "█")
    print("█   WAREHOUSE ROBOT TASK SCHEDULER — AI TECHNIQUES      █")
    print("█" + " "*60 + "█")
    print("█   CO1: Environment  | CO2: Search  | CO3: CSP         █")
    print("█   CO4: Utility      | CO5: Bayes   | CO6: Hybrid      █")
    print("█" + " "*60 + "█")
    print("█"*62)


def print_menu():
    print("\n" + "─"*60)
    print("  MAIN MENU")
    print("─"*60)
    print("  [1] CO1 — Environment & State (PEAS, Graph)")
    print("  [2] CO2 — Search Algorithms (BFS/DFS/UCS/A*)")
    print("  [3] CO3 — CSP Task Scheduling")
    print("  [4] CO4 — Utility & Multi-Agent Decisions")
    print("  [5] CO5 — Probabilistic / Bayesian Reasoning")
    print("  [6] CO6 — Hybrid AI System (Full Pipeline)")
    print("  [7] Customize Warehouse Grid")
    print("  [8] Show Grid")
    print("  [9] CO Mapping Summary")
    print("  [0] Exit")
    print("─"*60)


def run_co1(state: WarehouseState, logger: TraceLogger):
    """Run CO1 demonstrations."""
    display_peas_model()
    display_environment_types()
    logger.section("CO1: State Representation")
    for rid, robot in state.robots.items():
        logger.show_state(robot)
    graph = build_adjacency_graph(state)
    display_graph_info(graph, state)
    logger.log("CO1 complete: Environment formulated, graph built.")


def run_co2(state: WarehouseState):
    """Run CO2 search algorithm demonstrations."""
    print("\n" + "="*60)
    print("  CO2 ── SEARCH ALGORITHMS DEMO")
    print("="*60)

    # Pick first robot and its first task
    robot = list(state.robots.values())[0]
    task  = list(state.tasks.values())[0]
    start = robot.position
    goal  = task.pickup

    print(f"\n  Planning path: {start} → {goal}")
    print(f"  Robot: {robot.robot_id}  |  Task: {task.task_id}")

    results = []

    print("\n  ── Running BFS ──")
    r_bfs = bfs(state, start, goal, verbose=True)
    r_bfs.summary()
    results.append(r_bfs)

    print("\n  ── Running DFS ──")
    r_dfs = dfs(state, start, goal, verbose=True)
    r_dfs.summary()
    results.append(r_dfs)

    print("\n  ── Running UCS ──")
    r_ucs = ucs(state, start, goal, verbose=True)
    r_ucs.summary()
    results.append(r_ucs)

    print("\n  ── Running A* ──")
    r_astar = astar(state, start, goal, verbose=True)
    r_astar.summary()
    results.append(r_astar)

    # Comparison table
    compare_algorithms(results)

    # Display path on grid
    display_path_on_grid(state, r_astar, start, goal)

    # Also show BFS path for comparison
    print("\n  BFS path on grid (for comparison):")
    display_path_on_grid(state, r_bfs, start, goal)


def run_co3(state: WarehouseState):
    """Run CO3 CSP scheduling."""
    scheduler = CSPScheduler(state.tasks, state.robots)
    assignment = scheduler.solve()
    display_schedule(assignment, state.tasks, state.robots)
    explain_csp_concepts()

    # Update state with assignments
    if assignment:
        for tid, rid in assignment.items():
            state.tasks[tid].assigned_to = rid


# ─────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────

def main():
    print_banner()
    print("\n  Initializing warehouse simulation...")
    time.sleep(0.3)

    state  = create_default_warehouse()
    logger = TraceLogger()

    # Show initial grid
    display_grid(state, "DEFAULT WAREHOUSE — INITIAL STATE")

    print("\n  Welcome! The warehouse has been initialized.")
    print("  Use the menu to run each AI module (CO1–CO6).")

    while True:
        print_menu()
        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            run_co1(state, logger)

        elif choice == "2":
            run_co2(state)

        elif choice == "3":
            run_co3(state)

        elif choice == "4":
            run_co4_demo(state)

        elif choice == "5":
            run_co5_demo(state)

        elif choice == "6":
            hybrid = HybridAISystem(state)
            hybrid.run()

        elif choice == "7":
            state = customize_grid(state)
            display_grid(state, "UPDATED WAREHOUSE GRID")

        elif choice == "8":
            display_grid(state, "CURRENT WAREHOUSE STATE")

        elif choice == "9":
            display_co_mapping()

        elif choice == "0":
            print("\n  Thank you for using the Warehouse Robot AI System!")
            print("  Exiting...\n")
            sys.exit(0)

        else:
            print("\n  [!] Invalid choice. Please enter 0–9.")


if __name__ == "__main__":
    main()
