import curses
import random
import time

# =====================================================================
# TUNABLE GAMEPLAY CONFIGURATION
# =====================================================================
TICK_RATE_SECONDS = 0.20       # Lower = faster game cycles (0.15 is snappy)

# Structural Stacking
MAX_POD_STACK_DEPTH = 2        # Max stack levels (1 = Normal, 2 = Stacked)
FOOD_BONUS_PER_STACK = 1.5     # Heat/food multiplier if a host pod is stacked
KNOWLEDGE_BONUS_PER_STACK = 2.0 # Network connectivity weight multiplier if stacked

# Symbiotic Pattern Thresholds
GARDEN_NEIGHBOR_REQ = 2        # Local adjacent pods needed to trigger a Garden
LIBRARY_CONNECTIVITY_REQ = 6   # Minimum global mesh group size needed to trigger a Library

# Threat / Blight Scaling
BLIGHT_START_CHANCE = 0.01     # Initial chance per tick of a blight strike
BLIGHT_GROWTH_PER_TICK = 0.0003 # Escalation slope over time
BLIGHT_MAX_CHANCE = 0.55       # Upper threshold limit for blight strikes
TICKS_PER_EXTRA_STRIKE = 250   # Older networks experience multiple simultaneous strikes

# Economy Yield Defaults
BASE_FOOD_YIELD = 5      
BASE_KNOWLEDGE_YIELD = 10   

# Passive Self-Healing Effectiveness
HEAL_EFFECT_GARDEN = 0.005      # Heal chance modifier per active Garden
HEAL_EFFECT_LIBRARY = 0.008     # Heal chance modifier per active Library
MAX_HEAL_PROBABILITY = 0.50     # Absolute upper threshold limit for self-healing

# Action & Maintenance Economics
STARTING_FOOD = 100
STARTING_KNOWLEDGE = 100
COST_PLANT_POD = 30             # Deducted from Food
COST_STACK_POD = 50             # Deducted from Knowledge
COST_AUTO_HEAL_FOOD = 20        # Resource tax when the system automatically fixes an X
COST_AUTO_HEAL_KNOW = 20
COST_MANUAL_REPAIR_FOOD = 15    # Resource tax when you click-to-fix an X
COST_MANUAL_REPAIR_KNOW = 15
# =====================================================================

# Interface / Render Glyphs
EMPTY = ' '
POD_NORMAL = 'm'                # Lowercase for unstacked asset visibility
POD_STACKED = 'M'               # Uppercase for stacked asset visibility
GARDEN = 'G'      
LIBRARY = 'L'     
PULSE = '•'       
DAMAGED = 'X'     

class MyceliaEconomicGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # Grid boundaries optimized for portability
        self.sim_h = min(20, self.height - 8)
        self.sim_w = min(45, self.width - 32)
        
        self.pods = {}            
        self.surfaces = {}        
        self.damaged_nodes = set()
        self.pulses = []
        
        self.ticks = 0
        self.food_score = STARTING_FOOD
        self.knowledge_score = STARTING_KNOWLEDGE
        
        self.logs = [
            "ECONOMY ENGINE ONLINE.",
            f"New Pod: -{COST_PLANT_POD} Food. Stack Pod: -{COST_STACK_POD} Knowledge.",
            f"Auto-Healing consumes -{COST_AUTO_HEAL_FOOD}F / -{COST_AUTO_HEAL_KNOW}K."
        ]
        
        # Plant foundational free starter colony
        mid_h, mid_w = self.sim_h // 2, self.sim_w // 2
        self.pods[(mid_h, mid_w)] = 1
        self.pods[(mid_h, mid_w + 1)] = 1


    def count_local_neighbors(self, r, c):
        """Measures immediate physical density in an 8-way adjacent radius."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if (nr, nc) in self.pods and (nr, nc) not in self.damaged_nodes:
                    count += 1 if self.pods[(nr, nc)] == 1 else FOOD_BONUS_PER_STACK
        return count

    def get_mesh_connectivity_score(self, start_node):
        """Calculates size of the active network component via a flood-fill check."""
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

        # 1. BIOMIMETIC PATTERN PARSING
        for (r, c) in active_pods:
            local_density = self.count_local_neighbors(r, c)
            global_connectivity = self.get_mesh_connectivity_score((r, c))
            
            # A. Density Trigger -> Garden Sprout
            if local_density >= GARDEN_NEIGHBOR_REQ and (r, c) not in self.surfaces:
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 1 <= nr < self.sim_h and 1 <= nc < self.sim_w and (nr, nc) not in self.pods and (nr, nc) not in self.surfaces:
                        self.surfaces[(nr, nc)] = GARDEN
                        self.add_log(f"Garden Sprouted at ({nr}, {nc})")
                        break
            
            # B. Connectivity Trigger -> Library Sprout
            if global_connectivity >= LIBRARY_CONNECTIVITY_REQ:
                for dr, dc in [(-1,-1), (1,1), (-1,1), (1,-1)]:
                    nr, nc = r + dr, c + dc
                    if 1 <= nr < self.sim_h and 1 <= nc < self.sim_w and (nr, nc) not in self.pods and (nr, nc) not in self.surfaces:
                        self.surfaces[(nr, nc)] = LIBRARY
                        self.add_log(f"Library Opened at ({nr}, {nc})")
                        break

        # 2. ESCALATING ECO-BLIGHT THREAT
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

        # Prune isolated surface structures that lost host contact
        for (sr, sc), stype in list(self.surfaces.items()):
            has_host = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if (sr+dr, sc+dc) in self.pods and (sr+dr, sc+dc) not in self.damaged_nodes:
                        has_host = True
            if not has_host:
                del self.surfaces[(sr, sc)]
                self.add_log("Decay: Surface structure lost host loop.")

        # 3. YIELD ACCUMULATION & TAX-BASED SELF-HEALING
        num_gardens = list(self.surfaces.values()).count(GARDEN)
        num_libraries = list(self.surfaces.values()).count(LIBRARY)
        
        self.food_score += num_gardens * BASE_FOOD_YIELD
        self.knowledge_score += num_libraries * BASE_KNOWLEDGE_YIELD

        # Automated recovery probability logic
        calculated_healing = (num_gardens * HEAL_EFFECT_GARDEN) + (num_libraries * HEAL_EFFECT_LIBRARY)
        actual_heal_prob = min(calculated_healing, MAX_HEAL_PROBABILITY)
        
        if self.damaged_nodes and random.random() < actual_heal_prob:
            # Check if reserves can afford the automatic biomass patch cost
            if self.food_score >= COST_AUTO_HEAL_FOOD and self.knowledge_score >= COST_AUTO_HEAL_KNOW:
                healed_node = random.choice(list(self.damaged_nodes))
                self.damaged_nodes.discard(healed_node)
                self.food_score -= COST_AUTO_HEAL_FOOD
                self.knowledge_score -= COST_AUTO_HEAL_KNOW
                self.add_log(f"Auto-Heal: Repaired {healed_node} (-{COST_AUTO_HEAL_FOOD}F/-{COST_AUTO_HEAL_KNOW}K)")
            else:
                self.add_log("System Warning: Short on resources to auto-heal damage!")

        # 4. MESH ROUTING GRAPHICS GENERATOR
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

    def handle_click(self, mx, my, is_double_click):
        if 0 < my < self.sim_h and 0 < mx < self.sim_w:
            # Route Action A: Manual Repair Click
            if (my, mx) in self.damaged_nodes:
                if self.food_score >= COST_MANUAL_REPAIR_FOOD and self.knowledge_score >= COST_MANUAL_REPAIR_KNOW:
                    self.damaged_nodes.discard((my, mx))
                    self.food_score -= COST_MANUAL_REPAIR_FOOD
                    self.knowledge_score -= COST_MANUAL_REPAIR_KNOW
                    self.add_log(f"Manual Repair: Fixed ({my}, {mx}) (-{COST_MANUAL_REPAIR_FOOD}F/-{COST_MANUAL_REPAIR_KNOW}K)")
                else:
                    self.add_log("Error: Short on resources for manual repair.")
            
            # Route Action B: Upgrade Stack Level Click
            elif (my, mx) in self.pods:
                if is_double_click:
                    if self.pods[(my, mx)] < MAX_POD_STACK_DEPTH:
                        if self.knowledge_score >= COST_STACK_POD:
                            self.pods[(my, mx)] += 1
                            self.knowledge_score -= COST_STACK_POD
                            self.add_log(f"Stacked: Upgraded to '{POD_STACKED}' (-{COST_STACK_POD} Knowledge)")
                        else:
                            self.add_log("Error: Need more Knowledge to stack infrastructure.")
                else:
                    self.add_log("Node occupied. DOUBLE-CLICK to stack up.")
            
            # Route Action C: Plant New Infrastructure Pod Click
            else:
                if self.food_score >= COST_PLANT_POD:
                    self.pods[(my, mx)] = 1
                    self.food_score -= COST_PLANT_POD
                    self.add_log(f"Cultivated: Placed '{POD_NORMAL}' pod (-{COST_PLANT_POD} Food)")
                else:
                    self.add_log("Error: Deficit! Not enough Food to build new hardware.")

    def draw(self):
        self.stdscr.erase()
        
        # Frame Layout Bounds
        for r in range(self.sim_h + 1):
            for c in range(self.sim_w + 1):
                if r == 0 or r == self.sim_h or c == 0 or c == self.sim_w:
                    self.stdscr.addch(r, c, '#', curses.A_DIM)

        # Draw Field Objects
        for (r, c), stack_level in self.pods.items():
            if (r, c) in self.damaged_nodes:
                self.stdscr.addch(r, c, DAMAGED, curses.A_REVERSE)
            else:
                ch = POD_STACKED if stack_level > 1 else POD_NORMAL
                self.stdscr.addch(r, c, ch)

        for (r, c), stype in self.surfaces.items():
            if (r, c) not in self.pods:
                self.stdscr.addch(r, c, stype, curses.A_UNDERLINE)

        for (r, c) in self.pulses:
            if 0 < r < self.sim_h and 0 < c < self.sim_w:
                if self.stdscr.inch(r, c) & curses.A_CHARTEXT == ord(' '):
                    self.stdscr.addch(r, c, PULSE)

        # Dashboard Sidebar Telemetry Parsing
        num_gardens = list(self.surfaces.values()).count(GARDEN)
        num_libraries = list(self.surfaces.values()).count(LIBRARY)
        
        current_threat = BLIGHT_START_CHANCE + (self.ticks * BLIGHT_GROWTH_PER_TICK)
        display_threat = min(current_threat, BLIGHT_MAX_CHANCE) * 100
        display_heal = min(((num_gardens * HEAL_EFFECT_GARDEN) + (num_libraries * HEAL_EFFECT_LIBRARY)), MAX_HEAL_PROBABILITY) * 100

        sb_c = self.sim_w + 4
        self.stdscr.addstr(1, sb_c, "╔══════════════════════════╗")
        self.stdscr.addstr(2, sb_c, "║   MYCELIAL MATRIX SIM    ║", curses.A_BOLD)
        self.stdscr.addstr(3, sb_c, "╚══════════════════════════╝")
        
        self.stdscr.addstr(5, sb_c, f"Maturity (Ticks):      {self.ticks}")
        self.stdscr.addstr(6, sb_c, f"Blight Threat Rate:    {display_threat:.1f}%")
        self.stdscr.addstr(7, sb_c, f"Auto-Healing Bio-Rate: {display_heal:.1f}%")
        
        self.stdscr.addstr(9, sb_c, "RESOURCE RESERVES:", curses.A_UNDERLINE)
        self.stdscr.addstr(10, sb_c, f"🌾 Food:      {self.food_score} pts  [+{num_gardens * BASE_FOOD_YIELD}/t]")
        self.stdscr.addstr(11, sb_c, f"📜 Knowledge: {self.knowledge_score} pts  [+{num_libraries * BASE_KNOWLEDGE_YIELD}/t]")
        
        total_stacked = sum(1 for lvl in self.pods.values() if lvl > 1)
        self.stdscr.addstr(13, sb_c, f"Pods: Normal({POD_NORMAL})={len(self.pods)-len(self.damaged_nodes)-total_stacked} Stacked({POD_STACKED})={total_stacked}")
        self.stdscr.addstr(14, sb_c, f"Active Gardens  (G): {num_gardens}")
        self.stdscr.addstr(15, sb_c, f"Active Libraries(L): {num_libraries}")
        
        self.stdscr.addstr(17, sb_c, "ACTIONS COST SHEET:", curses.A_DIM)
        self.stdscr.addstr(18, sb_c, f"- Click Empty:  Pod ({COST_PLANT_POD} Food)")
        self.stdscr.addstr(19, sb_c, f"- Dbl-Click {POD_NORMAL}:  Stack ({COST_STACK_POD} Knowledge)")
        self.stdscr.addstr(20, sb_c, f"- Fix Damage {DAMAGED}: Repair ({COST_MANUAL_REPAIR_FOOD}F/{COST_MANUAL_REPAIR_KNOW}K)")

        # Log Board
        log_start_y = self.sim_h + 2
        self.stdscr.addstr(log_start_y, 1, "[ RESOURCE & INFRASTRUCTURE CONTROL ]", curses.A_DIM)
        for idx, log in enumerate(self.logs):
            self.stdscr.addstr(log_start_y + 1 + idx, 1, f">> {log}")

        self.stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    
    game = MyceliaEconomicGame(stdscr)
    last_tick = time.time()
    
    while True:
        ch = stdscr.getch()
        
        if ch == ord('q') or ch == ord('Q'):
            break
            
        elif ch == curses.KEY_MOUSE:
            try:
                _, mx, my, _, bstate = curses.getmouse()
                is_double = True if (bstate & curses.BUTTON1_DOUBLE_CLICKED) else False
                if bstate & (curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED | curses.BUTTON1_DOUBLE_CLICKED):
                    game.handle_click(mx, my, is_double)
            except curses.error:
                pass
        
        if time.time() - last_tick > TICK_RATE_SECONDS:
            game.game_loop_tick()
            game.draw()
            last_tick = time.time()
            
        time.sleep(0.02)

if __name__ == "__main__":
    curses.wrapper(main)
