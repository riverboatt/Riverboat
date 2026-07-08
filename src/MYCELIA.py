import asyncio
import collections
import queue
import random
import sys
import threading
import time
from pathlib import Path
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

# =====================================================================
# MYCELIA — The Grown Data Center
# BEKW-CODE Open Hardware Spec
# Nature already solved distributed, resilient, self-healing infrastructure. 
# We just forgot to copy the homework.
# =====================================================================

# ---------------------------------------------------------------------
# TUNABLE GAMEPLAY CONFIGURATION
# ---------------------------------------------------------------------
TICK_RATE_SECONDS = 0.20       

# 2.2 The Growth Layer (Expansion Without Land Clearing)
MAX_POD_STACK_DEPTH = 2        
FOOD_BONUS_PER_STACK = 1.5     
KNOWLEDGE_BONUS_PER_STACK = 2.0 

# 2.3 The Surface Layer (Library + Garden — the public-facing organism)
GARDEN_NEIGHBOR_REQ = 2        
LIBRARY_CONNECTIVITY_REQ = 6   

# 5. Why This Solves the Actual Complaint: Blight / Threat / Strain
BLIGHT_START_CHANCE = 0.01     
BLIGHT_GROWTH_PER_TICK = 0.0009 
BLIGHT_MAX_CHANCE = 0.55        
TICKS_PER_EXTRA_STRIKE = 250   

# Economy Yield Defaults (Operating Byproducts)
BASE_FOOD_YIELD = 5      
BASE_KNOWLEDGE_YIELD = 10   

# Passive Self-Healing Effectiveness
HEAL_EFFECT_GARDEN = 0.005      
HEAL_EFFECT_LIBRARY = 0.008     
MAX_HEAL_PROBABILITY = 0.50     

# Action & Maintenance Economics (Resource-Sharing Matrix)
STARTING_FOOD = 100
STARTING_KNOWLEDGE = 100
COST_PLANT_POD = 30             
COST_STACK_POD = 50             
COST_AUTO_HEAL_FOOD = 20        
COST_AUTO_HEAL_KNOW = 20
COST_MANUAL_REPAIR_FOOD = 15    
COST_MANUAL_REPAIR_KNOW = 15
# =====================================================================

# Interface / Render Glyphs (Configured with Rich Styles)
EMPTY = " "
POD_NORMAL = "[green]m[/green]"
POD_STACKED = "[bold green]M[/bold green]"
GARDEN = "[bright_yellow]G[/bright_yellow]"
LIBRARY = "[bright_magenta]L[/bright_magenta]"
PULSE = "[cyan]•[/cyan]"
DAMAGED = "[bold red]X[/bold red]"
CURSOR = "[bold blink white]🔲[/bold blink white]"

class MyceliaCursorGame:
    def __init__(self):
        self.sim_h = 16
        self.sim_w = 40
        
        # Cursor Tracking State
        self.cursor_r = self.sim_h // 2
        self.cursor_c = self.sim_w // 2
        
        self.pods = {}            
        self.surfaces = {}        
        self.damaged_nodes = set()
        self.pulses = []
        
        self.ticks = 0
        self.food_score = STARTING_FOOD
        self.knowledge_score = STARTING_KNOWLEDGE
        
        self.logs = [
            "NAVIGATION ENGINE ONLINE. Use IJKL or WASD keys to navigate.",
            "Press SPACE over a tile to interact based on context:",
            "  - Empty Tile: Plant Pod   - Normal Pod (m): Stack to (M)",
            "  - Severed Node (X): Manually Patch & Repair"
        ]
        
        # 1. Concept & Inversion: Core Architecture Layer
        mid_h, mid_w = self.sim_h // 2, self.sim_w // 2
        self.pods[(mid_h, mid_w - 2)] = 1
        self.pods[(mid_h, mid_w - 1)] = 1
        self.pods[(mid_h + 1, mid_w - 2)] = 1

    def count_local_neighbors(self, r, c):
        # 2.3 Localized waste-heat output
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if (nr, nc) in self.pods and (nr, nc) not in self.damaged_nodes:
                    count += 1 if self.pods[(nr, nc)] == 1 else FOOD_BONUS_PER_STACK
        return count

    def get_mesh_connectivity_score(self, start_node):
        # 2.1 Interconnected mycelial matrix
        if start_node in self.damaged_nodes or start_node not in self.pods:
            return 0
        visited = set()
        queue = [start_node]
        visited.add(start_node)
        total_connectivity_weight = 0
        
        while queue:
            curr = queue.pop(0)
            weight = 1 if self.pods[curr] == 1 else KNOWLEDGE_BONUS_PER_STACK
            total_connectivity_weight += weight
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    neighbor = (curr[0] + dr, curr[1] + dc)
                    if neighbor in self.pods and neighbor not in self.damaged_nodes:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
        return total_connectivity_weight

    def add_log(self, msg):
        self.logs.append(msg)
        if len(self.logs) > 4:
            self.logs.pop(0)

    def game_loop_tick(self):
        self.ticks += 1
        active_pods = [p for p in self.pods if p not in self.damaged_nodes]

        # 2. Core Architecture — Three Layers, One Organism
        for (r, c) in active_pods:
            local_density = self.count_local_neighbors(r, c)
            global_connectivity = self.get_mesh_connectivity_score((r, c))
            
            # 2.3 Greenhouse / Garden Layer
            if local_density >= GARDEN_NEIGHBOR_REQ and (r, c) not in self.surfaces:
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.sim_h and 0 <= nc < self.sim_w and (nr, nc) not in self.pods and (nr, nc) not in self.surfaces:
                        self.surfaces[(nr, nc)] = GARDEN
                        self.add_log(f"Garden Sprouted at ({nr}, {nc})")
                        break
            
            # 2.3 Public Library Layer
            if global_connectivity >= LIBRARY_CONNECTIVITY_REQ:
                for dr, dc in [(-1,-1), (1,1), (-1,1), (1,-1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.sim_h and 0 <= nc < self.sim_w and (nr, nc) not in self.pods and (nr, nc) not in self.surfaces:
                        self.surfaces[(nr, nc)] = LIBRARY
                        self.add_log(f"Library Opened at ({nr}, {nc})")
                        break

        # 3. Systems Detail: Simulated Damage / Failure Mode
        current_threat = BLIGHT_START_CHANCE + (self.ticks * BLIGHT_GROWTH_PER_TICK)
        actual_threat_prob = min(current_threat, BLIGHT_MAX_CHANCE)
        
        if active_pods and random.random() < actual_threat_prob:
            damage_strikes = 1 + (self.ticks // TICKS_PER_EXTRA_STRIKE)
            for _ in range(int(damage_strikes)):
                if active_pods:
                    target = random.choice(active_pods)
                    self.damaged_nodes.add(target)
                    active_pods.remove(target)
                    self.add_log(f"BLIGHT ALERT: Node severed at {target}")

        for (sr, sc), stype in list(self.surfaces.items()):
            has_host = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if (sr+dr, sc+dc) in self.pods and (sr+dr, sc+dc) not in self.damaged_nodes:
                        has_host = True
            if not has_host:
                del self.surfaces[(sr, sc)]
                self.add_log("Decay: Surface structure lost host loop.")

        # 6. Open Questions / Testing & Validation
        num_gardens = list(self.surfaces.values()).count(GARDEN)
        num_libraries = list(self.surfaces.values()).count(LIBRARY)
        
        game_food_yield = num_gardens * BASE_FOOD_YIELD
        game_knowledge_yield = num_libraries * BASE_KNOWLEDGE_YIELD
        
        self.food_score += game_food_yield
        self.knowledge_score += game_knowledge_yield

        calculated_healing = (num_gardens * HEAL_EFFECT_GARDEN) + (num_libraries * HEAL_EFFECT_LIBRARY)
        actual_heal_prob = min(calculated_healing, MAX_HEAL_PROBABILITY)
        
        if self.damaged_nodes and random.random() < actual_heal_prob:
            if self.food_score >= COST_AUTO_HEAL_FOOD and self.knowledge_score >= COST_AUTO_HEAL_KNOW:
                healed_node = random.choice(list(self.damaged_nodes))
                self.damaged_nodes.discard(healed_node)
                self.food_score -= COST_AUTO_HEAL_FOOD
                self.knowledge_score -= COST_AUTO_HEAL_KNOW
                self.add_log(f"Auto-Heal: Repaired {healed_node} (-{COST_AUTO_HEAL_FOOD}F/-{COST_AUTO_HEAL_KNOW}K)")
            else:
                self.add_log("System Warning: Short on resources to auto-heal damage!")

        # 2.1 Active Data Routing
        self.pulses = []
        if len(active_pods) >= 2:
            src, dest = random.choice(active_pods), random.choice(active_pods)
            if src != dest:
                curr_r, curr_c = src
                while (curr_r, curr_c) != dest:
                    if curr_r < dest[0]: curr_r += 1
                    elif curr_r > dest[0]: curr_r -= 1
                    if curr_c < dest[1]: curr_c += 1
                    elif curr_c > dest[1]: curr_c -= 1
                    if (curr_r, curr_c) in self.damaged_nodes:
                        break
                    self.pulses.append((curr_r, curr_c))

    def handle_input(self, key):
        if not key:
            return
        key = key.lower()
        
        # 1. Navigation Mapping (IJKL Layout)
        if key in ('i', 'w') and self.cursor_r > 0:
            self.cursor_r -= 1
        elif key in ('k', 's') and self.cursor_r < self.sim_h - 1:
            self.cursor_r += 1
        elif key in ('j', 'a') and self.cursor_c > 0:
            self.cursor_c -= 1
        elif key in ('l', 'd') and self.cursor_c < self.sim_w - 1:
            self.cursor_c += 1
            
        # 2. Context Action Evaluation Key (Space)
        elif key == ' ':
            target_coord = (self.cursor_r, self.cursor_c)
            
            # Action Condition A: Targeted Repair Check
            if target_coord in self.damaged_nodes:
                if self.food_score >= COST_MANUAL_REPAIR_FOOD and self.knowledge_score >= COST_MANUAL_REPAIR_KNOW:
                    self.damaged_nodes.discard(target_coord)
                    self.food_score -= COST_MANUAL_REPAIR_FOOD
                    self.knowledge_score -= COST_MANUAL_REPAIR_KNOW
                    self.add_log(f"Manual Repair: Patched node {target_coord}")
                else:
                    self.add_log("Error: Deficit to execute manual hardware repair.")
                    
            # Action Condition B: Targeted Structural Level Upgrade Stacking
            elif target_coord in self.pods:
                current_depth = self.pods[target_coord]
                if current_depth < MAX_POD_STACK_DEPTH:
                    if self.knowledge_score >= COST_STACK_POD:
                        self.pods[target_coord] += 1
                        self.knowledge_score -= COST_STACK_POD
                        self.add_log(f"Stacked: Upgraded node {target_coord} to level 2")
                    else:
                        self.add_log("Error: Need more Knowledge to scale infrastructure layers.")
                else:
                    self.add_log("Node already functioning at maximum structural threshold depth.")
                    
            # Action Condition C: New Pod Allocation Placement
            else:
                if self.food_score >= COST_PLANT_POD:
                    self.pods[target_coord] = 1
                    self.food_score -= COST_PLANT_POD
                    self.add_log(f"Cultivated: Added new pod loop asset at {target_coord}")
                else:
                    self.add_log("Error: Deficit! Not enough Food biomass to extend outward.")

    def render_grid(self) -> Text:
        grid_lines = []
        for r in range(self.sim_h):
            row_tokens = []
            for c in range(self.sim_w):
                coord = (r, c)
                
                # Superimpose cursor selection box layout safely on top
                if r == self.cursor_r and c == self.cursor_c:
                    row_tokens.append(CURSOR)
                elif coord in self.damaged_nodes:
                    row_tokens.append(DAMAGED)
                elif coord in self.pods:
                    row_tokens.append(POD_STACKED if self.pods[coord] > 1 else POD_NORMAL)
                elif coord in self.surfaces:
                    row_tokens.append(self.surfaces[coord])
                elif coord in self.pulses:
                    row_tokens.append(PULSE)
                else:
                    row_tokens.append(EMPTY)
            grid_lines.append(" ".join(row_tokens))
        return Text.from_markup("\n".join(grid_lines))

class TerminalInputSource:
    def __init__(self):
        self._queue = queue.Queue()
        self._restore_terminal = lambda: None
        if sys.stdin.isatty():
            import readchar
            try:
                import termios
                fd = sys.stdin.fileno()
                original_settings = termios.tcgetattr(fd)
                self._restore_terminal = lambda: termios.tcsetattr(fd, termios.TCSADRAIN, original_settings)
            except ImportError:
                pass
            thread = threading.Thread(target=self._poll, args=(readchar,), daemon=True)
            thread.start()

    def _poll(self, readchar):
        while True:
            self._queue.put(readchar.readkey())

    def get_nowait(self):
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None

    def close(self):
        self._restore_terminal()

class PyodideInputSource:
    def __init__(self):
        self._keys = collections.deque()

    def close(self):
        pass

    def push_key(self, key):
        self._keys.append(key)

    def get_nowait(self):
        try:
            return self._keys.popleft()
        except IndexError:
            return None

class JSOutput:
    def write(self, text):
        from js import termWrite
        termWrite(text.replace("\n", "\r\n"))

    def flush(self):
        pass

    def isatty(self):
        return True

PYODIDE_COLS, PYODIDE_ROWS = 130, 44

def read_bekw_gist():
    try:
        return (Path(__file__).parent / "Data_center.gist").read_text()
    except OSError:
        return ""

_pyodide_input = None

def push_key(key):
    if _pyodide_input is not None:
        _pyodide_input.push_key(key)

def start_pyodide():
    global _pyodide_input
    _pyodide_input = PyodideInputSource()
    console = Console(file=JSOutput(), force_terminal=True,
                       color_system="truecolor",
                       width=PYODIDE_COLS, height=PYODIDE_ROWS)
    asyncio.ensure_future(main(input_source=_pyodide_input, console=console))

async def main(input_source=None, console=None):
    if input_source is None:
        input_source = TerminalInputSource()
    if console is None:
        console = Console()
    game = MyceliaCursorGame()

    try:
        with Live(console=console, screen=True, auto_refresh=False) as live:
            last_tick = time.monotonic()

            while True:
                # Poll inputs instantly and non-blockingly
                ch = input_source.get_nowait()
                if ch:
                    if ch.lower() == 'q':
                        break
                    else:
                        game.handle_input(ch)

                # Game core tick cycles
                if time.monotonic() - last_tick > TICK_RATE_SECONDS:
                    game.game_loop_tick()
                    last_tick = time.monotonic()

                # Parse sidebar statistics and layout components
                num_gardens = list(game.surfaces.values()).count(GARDEN)
                num_libraries = list(game.surfaces.values()).count(LIBRARY)
                current_threat = BLIGHT_START_CHANCE + (game.ticks * BLIGHT_GROWTH_PER_TICK)
                display_threat = min(current_threat, BLIGHT_MAX_CHANCE) * 100
                display_heal = min(((num_gardens * HEAL_EFFECT_GARDEN) + (num_libraries * HEAL_EFFECT_LIBRARY)), MAX_HEAL_PROBABILITY) * 100
                total_stacked = sum(1 for lvl in game.pods.values() if lvl > 1)

                # Assign View Windows
                grid_panel = Panel(game.render_grid(), title="[bold green]Mycelia Spatial Computing Array[/bold green]", border_style="green")

                stats_table = Table.grid(padding=1)
                stats_table.add_row(f"[bold yellow]Ticks Passed:[/bold yellow] {game.ticks}")
                stats_table.add_row(f"[bold red]Blight Threat:[/bold red] {display_threat:.1f}%")
                stats_table.add_row(f"[bold cyan]Auto-Heal Rate:[/bold cyan] {display_heal:.1f}%")
                stats_table.add_row("")
                stats_table.add_row(f"Target Selection Pos: [bold white]({game.cursor_r}, {game.cursor_c})[/bold white]")
                stats_table.add_row("")
                stats_table.add_row("[bold underline]RESOURCE RESERVES[/bold underline]")
                stats_table.add_row(f"🌾 Food Draw:   [green]{game.food_score}[/green] pts (+{num_gardens * BASE_FOOD_YIELD}/t)")
                stats_table.add_row(f"📜 Knowledge:   [green]{game.knowledge_score}[/green] pts (+{num_libraries * BASE_KNOWLEDGE_YIELD}/t)")
                stats_table.add_row("")
                stats_table.add_row(f"Pods: Normal(m)={len(game.pods)-len(game.damaged_nodes)-total_stacked} Stacked(M)={total_stacked}")
                stats_table.add_row(f"Active Gardens(G): {num_gardens} | Libraries(L): {num_libraries}")
                stats_table.add_row("")
                stats_table.add_row("[dim]Navigation Layout Hotkeys:[/dim]")
                stats_table.add_row("[bold white]  I/W=Up  J/A=Left  K/S=Down  L/D=Right[/bold white]")
                stats_table.add_row("[bold cyan]  SPACE=Execute Context Action (Plant/Stack/Repair)[/bold cyan]")
                stats_table.add_row("[dim]  Q=Quit Session[/dim]")

                stats_panel = Panel(stats_table, title="[bold white]Systems Controls Dashboard[/bold white]", border_style="white")

                # Bottom panel console log lines output box tracking
                log_text = Text.from_markup("\n".join([f">> {log}" for log in game.logs]))
                log_panel = Panel(log_text, title="[dim]System Console Event Loop Log[/dim]", border_style="blue")

                # Main multi-split viewport construction
                root_layout = Layout()
                root_layout.split_column(
                    Layout(name="top", ratio=4),
                    Layout(name="bottom", ratio=1)
                )
                root_layout["top"].split_row(
                    Layout(grid_panel, ratio=3),
                    Layout(stats_panel, ratio=2)
                )
                root_layout["bottom"].update(log_panel)

                live.update(root_layout, refresh=True)
                await asyncio.sleep(0.04)

        console.print(Markdown(read_bekw_gist()))
    finally:
        input_source.close()

if __name__ == "__main__":
    asyncio.run(main())
