#!/usr/bin/env python3

import curses
import time
import random
import os
import argparse
from math import sin, cos, pi

UPDATE_INTERVAL = 0.03  # Faster updates for denser simulation
WIND_CHARS = ['·', '°', '~', '∴', '∵', '⋮', '⋯', '︙', '⡀', '⡄', '⡆', '⡇', '⣀', '⣤', '⣦', '⣶', '⣷', '⣿']
WIND_PARTICLES = ['░', '▒', '▓', '█', '🮆', '🮇', '🮈', '🮉']  

# Color mapping for command-line arguments
CURSES_COLOR_MAP = {
    'black': curses.COLOR_BLACK,
    'red': curses.COLOR_RED,
    'green': curses.COLOR_GREEN,
    'yellow': curses.COLOR_YELLOW,
    'blue': curses.COLOR_BLUE,
    'magenta': curses.COLOR_MAGENTA,
    'cyan': curses.COLOR_CYAN,
    'white': curses.COLOR_WHITE,
}

class WindParticle:
    def __init__(self, x, y, max_rows, max_cols, density_mode=False):
        self.x = x
        self.y = y
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.speed = random.uniform(0.5, 1.5)  # Faster speeds
        self.char = random.choice(WIND_CHARS)
        self.amplitude = random.uniform(0.8, 3.0)  # Larger waves
        self.frequency = random.uniform(0.2, 0.5)  # Higher frequency
        self.phase = random.uniform(0, 2 * pi)
        self.original_x = x
        self.lifetime = random.uniform(2, 6)  # Shorter lifetime for more turnover
        self.age = 0
        self.density_char = random.choice(WIND_PARTICLES)
        self.density = random.random()
        self.density_mode = density_mode
        self.layer = random.randint(1, 3)  # Different layers for depth
        self.opacity = random.uniform(0.7, 1.0)  # For visual variety

    def update(self, wind_strength, wind_direction):
        """Update particle position based on wind parameters"""
        self.age += UPDATE_INTERVAL
        
        layer_speed = self.speed * (1 + (self.layer - 1) * 0.3)
        self.x += layer_speed * wind_strength * wind_direction
        
        base_wave = sin(self.age * self.frequency * 8 + self.phase) * self.amplitude
        secondary_wave = cos(self.age * self.frequency * 4 + self.phase * 2) * self.amplitude * 0.3
        wave_offset = (base_wave + secondary_wave) * 0.4
        
        self.y += wave_offset
        
        if self.x >= self.max_cols or self.x < 0:
            self.reset()
        
        if self.y >= self.max_rows:
            self.y = self.max_rows - 1
            self.phase += pi  # Reverse phase on bounce
        elif self.y < 0:
            self.y = 0
            self.phase += pi  # Reverse phase on bounce
            
        # Reset if lifetime expired
        if self.age >= self.lifetime:
            self.reset()

    def reset(self):
        if random.random() < 0.3:  
            self.x = 0
        else:  
            self.x = random.randint(0, self.max_cols - 1)
            
        self.y = random.randint(0, self.max_rows - 1)
        self.speed = random.uniform(0.5, 1.5)
        self.char = random.choice(WIND_CHARS)
        self.amplitude = random.uniform(0.8, 3.0)
        self.frequency = random.uniform(0.2, 0.5)
        self.phase = random.uniform(0, 2 * pi)
        self.lifetime = random.uniform(2, 6)
        self.age = 0
        self.density_char = random.choice(WIND_PARTICLES)
        self.density = random.random()
        self.layer = random.randint(1, 3)
        self.opacity = random.uniform(0.7, 1.0)

class WindSimulation:
    def __init__(self, stdscr, wind_color='cyan', show_density=False, high_density=True):
        self.stdscr = stdscr
        self.wind_color = wind_color
        self.show_density = show_density
        self.high_density = high_density
        
        self.wind_strength = 1.0
        self.wind_direction = 1
        self.base_wind_strength = 1.0
        self.wind_variation_timer = 0
        self.gust_timer = 0
        self.gust_active = False
        self.gust_strength = 0
        
        self.particles = []
        self.rows, self.cols = stdscr.getmaxyx()
        self.last_update_time = time.time()
        self.frame_count = 0
        
        self.density_layers = []
        self.init_density_layers()
        
        # Initialize colors
        self.setup_colors()

    def init_density_layers(self):
        """Initialize density visualization layers"""
        self.density_layers = []
        for _ in range(3):  
            layer = [' '] * (self.cols * self.rows)
            self.density_layers.append(layer)

    def setup_colors(self):
        """Initialize color pairs"""
        if curses.has_colors():
            curses.start_color()
            if curses.can_change_color():
                curses.use_default_colors()
                bg = -1
            else:
                bg = curses.COLOR_BLACK

            wind_fg = CURSES_COLOR_MAP.get(self.wind_color.lower(), curses.COLOR_CYAN)
            
            curses.init_pair(1, wind_fg, bg)  
            curses.init_pair(2, curses.COLOR_WHITE, bg)  
            curses.init_pair(3, curses.COLOR_BLUE, bg)   
            curses.init_pair(4, curses.COLOR_CYAN, bg)   
            curses.init_pair(5, curses.COLOR_WHITE, bg)  
            curses.init_pair(6, curses.COLOR_MAGENTA, bg) 

    def update_wind_pattern(self):
        """Update wind strength and direction with natural variation"""
        self.wind_variation_timer += UPDATE_INTERVAL
        
        base_variation = sin(self.wind_variation_timer * 0.8) * 0.4
        secondary_variation = cos(self.wind_variation_timer * 0.3) * 0.2
        self.base_wind_strength = max(0.5, 1.2 + base_variation + secondary_variation)
        
        # More frequent gusts in high density mode
        gust_chance = 0.01 if self.high_density else 0.005
        
        if not self.gust_active and random.random() < gust_chance:
            self.gust_active = True
            self.gust_timer = 0
            self.gust_strength = random.uniform(2.5, 5.0)
        
        if self.gust_active:
            self.gust_timer += UPDATE_INTERVAL
            gust_duration = random.uniform(0.3, 1.2)
            
            if self.gust_timer < gust_duration:
                progress = self.gust_timer / gust_duration
                if progress < 0.2:
                    gust_multiplier = progress / 0.2
                elif progress < 0.8:
                    gust_multiplier = 1.0
                else:
                    gust_multiplier = 1.0 - ((progress - 0.8) / 0.2)
                
                self.wind_strength = self.base_wind_strength + self.gust_strength * gust_multiplier
            else:
                self.gust_active = False
                self.wind_strength = self.base_wind_strength
        else:
            self.wind_strength = self.base_wind_strength
        
        # More frequent direction changes in high density
        direction_chance = 0.003 if self.high_density else 0.001
        if random.random() < direction_chance:
            self.wind_direction *= -1

    def generate_particles(self):
        """Generate new wind particles with high density"""
        if self.high_density:
            # Much higher particle count for dense simulation
            target_count = int(self.cols * self.rows * 0.15)  # 15% of screen area
            target_count = min(target_count, 2000)  # Cap at 2000 particles
        else:
            target_count = int(self.cols * 0.5)
        
        while len(self.particles) < target_count:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            self.particles.append(WindParticle(x, y, self.rows, self.cols, self.show_density))

    def update_density_map(self):
        """Update the density visualization map"""
        # Clear density layers
        for layer in self.density_layers:
            for i in range(len(layer)):
                layer[i] = ' '
        
        # Update density based on particle positions
        for particle in self.particles:
            x, y = int(particle.x), int(particle.y)
            if 0 <= x < self.cols and 0 <= y < self.rows:
                idx = y * self.cols + x
                density_char = WIND_PARTICLES[min(int(particle.density * len(WIND_PARTICLES)), len(WIND_PARTICLES)-1)]
                layer_idx = min(particle.layer - 1, len(self.density_layers) - 1)
                self.density_layers[layer_idx][idx] = density_char

    def update(self):
        """Update simulation state"""
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        
        if delta_time < UPDATE_INTERVAL:
            time.sleep(UPDATE_INTERVAL - delta_time)
        
        self.last_update_time = time.time()
        self.frame_count += 1
        
        # Update wind pattern
        self.update_wind_pattern()
        
        # Generate particles
        self.generate_particles()
        
        # Update all particles
        for particle in self.particles:
            particle.update(self.wind_strength, self.wind_direction)
        
        # Update density map if in density mode
        if self.show_density:
            self.update_density_map()

    def draw(self):
        """Draw the wind simulation"""
        self.stdscr.clear()
        
        if self.show_density:
            # Draw density visualization
            self.draw_density()
        else:
            # Draw individual particles
            self.draw_particles()
        
        # Draw UI information
        self.draw_ui()

    def draw_density(self):
        """Draw density visualization"""
        for layer_idx, layer in enumerate(self.density_layers):
            color_attr = curses.color_pair(3 + layer_idx)  # Different colors per layer
            if layer_idx == 2:  # Top layer
                color_attr |= curses.A_BOLD
            
            for y in range(self.rows):
                for x in range(self.cols):
                    idx = y * self.cols + x
                    char = layer[idx]
                    if char != ' ':
                        try:
                            self.stdscr.addstr(y, x, char, color_attr)
                        except curses.error:
                            pass

    def draw_particles(self):
        """Draw individual wind particles"""
        # Sort particles by layer for proper rendering
        sorted_particles = sorted(self.particles, key=lambda p: p.layer)
        
        for particle in sorted_particles:
            try:
                # Dynamic color based on speed and layer
                if self.gust_active and self.wind_strength > 2.0:
                    if particle.speed > 1.2:
                        color_attr = curses.color_pair(2) | curses.A_BOLD  # White for fast particles in gusts
                    else:
                        color_attr = curses.color_pair(6) | curses.A_BOLD  # Magenta for medium particles
                else:
                    if particle.layer == 1:
                        color_attr = curses.color_pair(1) | curses.A_DIM
                    elif particle.layer == 2:
                        color_attr = curses.color_pair(1)
                    else:  # layer 3
                        color_attr = curses.color_pair(1) | curses.A_BOLD
                
                # Draw the particle
                if 0 <= int(particle.y) < self.rows and 0 <= int(particle.x) < self.cols:
                    self.stdscr.addstr(int(particle.y), int(particle.x), particle.char, color_attr)
            except curses.error:
                pass

    def draw_ui(self):
        """Draw user interface information"""
        try:
            # Wind information
            strength_bar = '|' * int(self.wind_strength * 4)
            direction_char = '→' if self.wind_direction > 0 else '←'
            info_line = f"Wind: {strength_bar} {self.wind_strength:.1f} {direction_char}"
            
            if self.gust_active:
                info_line += " 💨 GUST!"
                
            info_line += f" Parts: {len(self.particles)}"
            
            self.stdscr.addstr(0, 0, info_line, curses.A_BOLD)
            
            # Help text
            help_items = [
            ]
            help_text = " ".join(help_items)
            
            if len(help_text) < self.cols:
                self.stdscr.addstr(self.rows - 1, 0, help_text, curses.A_DIM)
                
            # Mode indicator
            mode_text = f"Mode: {'HIGH DENSITY' if self.high_density else 'Normal'}"
            if self.show_density:
                mode_text += " | DENSITY VISUALIZATION"
                
            if len(mode_text) < self.cols:
                self.stdscr.addstr(1, 0, mode_text, curses.A_DIM)
                
        except curses.error:
            pass

def wind_simulation(stdscr, wind_color='cyan', show_density=False, high_density=True):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1)
    
    simulation = WindSimulation(stdscr, wind_color, show_density, high_density)
    
    while True:
        # Handle input
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q') or key == 27:
            break
        elif key == ord('d') or key == ord('D'):
            simulation.show_density = not simulation.show_density
            if simulation.show_density:
                simulation.init_density_layers()
        elif key == ord('h') or key == ord('H'):
            simulation.high_density = not simulation.high_density
            simulation.particles.clear()  # Reset particles for new density
        elif key == ord('+'):
            simulation.base_wind_strength = min(8.0, simulation.base_wind_strength + 0.3)
        elif key == ord('-'):
            simulation.base_wind_strength = max(0.1, simulation.base_wind_strength - 0.3)
        elif key == curses.KEY_RIGHT:
            simulation.wind_direction = 1
        elif key == curses.KEY_LEFT:
            simulation.wind_direction = -1
        elif key == curses.KEY_RESIZE:
            simulation.rows, simulation.cols = stdscr.getmaxyx()
            simulation.particles.clear()
            simulation.init_density_layers()
        
        # Update and draw
        simulation.update()
        simulation.draw()
        
        stdscr.noutrefresh()
        curses.doupdate()

def main():
    if not os.isatty(1) or os.environ.get('TERM') == 'dumb':
        print("Error: This script requires a TTY with curses support.")
        return

    parser = argparse.ArgumentParser(description="High-density wind simulation in the terminal")
    valid_colors = list(CURSES_COLOR_MAP.keys())
    
    parser.add_argument(
        '--color',
        type=str,
        default='cyan',
        choices=valid_colors,
        help=f"Wind color. Choices: {', '.join(valid_colors)}"
    )
    
    parser.add_argument(
        '--density',
        action='store_true',
        help="Show wind density visualization"
    )
    
    parser.add_argument(
        '--normal-density',
        action='store_true',
        help="Use normal density instead of high density"
    )
    
    args = parser.parse_args()

    try:
        curses.wrapper(wind_simulation, args.color, args.density, not args.normal_density)
    except curses.error as e:
        try:
            curses.endwin()
        except Exception:
            pass
        print(f"\nCurses error: {e}")
        print("Try resizing terminal or using different terminal emulator.")
    except KeyboardInterrupt:
        print("\nExiting wind simulation...")
    except Exception as e:
        try:
            curses.endwin()
        except Exception:
            pass
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()
