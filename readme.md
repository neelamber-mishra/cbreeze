# CBreeze - Terminal Wind Simulation

## Overview

CBreeze is a high-performance terminal-based wind simulation engine implemented in Python using the curses library. It generates realistic fluid dynamics visualizations through particle systems and density mapping, providing both interactive and programmable wind pattern simulations.

## Features

### Core Simulation
- **Particle System**: Configurable particle-based wind flow with variable density
- **Fluid Dynamics**: Wave-based particle motion with amplitude and frequency modulation
- **Wind Patterns**: Dynamic wind strength variation with gust simulation
- **Direction Control**: Real-time wind direction changes (left/right flow)

### Visualization Modes
- **Particle View**: Individual wind particle rendering with layer-based depth
- **Density Mapping**: Multi-layer density visualization showing wind concentration
- **Color Systems**: Configurable color palettes with layer-based coloring

### Technical Capabilities
- **High Density Rendering**: Support for up to 2000 simultaneous particles
- **Real-time Controls**: Interactive parameter adjustment during simulation
- **Terminal Resize Handling**: Dynamic adaptation to terminal dimension changes
- **Performance Optimized**: Frame rate control and efficient particle management

## Installation

### Prerequisites
- Python 3.7+
- Terminal with curses support
- POSIX-compliant system (Linux, macOS, WSL)

### Installation Methods

**From Source:**
```bash
git clone https://github.com/your-username/cbreeze.git
cd cbreeze
pip install .
```

**Direct Execution:**
```bash
python cbreeze.py [options]
```

## Usage

### Basic Simulation
```bash
cbreeze
```

### Advanced Configuration
```bash
cbreeze --color blue --density --normal-density
```

### Command Line Options

- `--color COLOR`: Set wind color (cyan, blue, white, magenta, green, yellow, red)
- `--density`: Enable density visualization mode
- `--normal-density`: Use normal particle density instead of high density

### Interactive Controls

During simulation:
- `Q`: Exit simulation
- `D`: Toggle density visualization mode
- `H`: Toggle between high and normal density modes
- `+/-`: Adjust wind strength
- `Left/Right Arrow`: Change wind direction

## Technical Architecture

### Particle System
- **WindParticle Class**: Individual particle with wave motion parameters
- **Layer Management**: Three depth layers with different rendering properties
- **Lifecycle Management**: Particle regeneration and lifetime control

### Wind Simulation Engine
- **WindSimulation Class**: Core simulation controller
- **Pattern Generation**: Procedural wind strength and gust simulation
- **Density Mapping**: Real-time density calculation and visualization

### Rendering Pipeline
- **Curses Integration**: Terminal graphics and color management
- **Frame Rate Control**: Fixed time step simulation loop
- **Resize Handling**: Dynamic buffer reallocation

## API Reference

### Core Classes

#### WindParticle
```python
class WindParticle:
    def __init__(self, x, y, max_rows, max_cols, density_mode=False)
    def update(self, wind_strength, wind_direction)
    def reset(self)
```

#### WindSimulation
```python
class WindSimulation:
    def __init__(self, stdscr, wind_color='cyan', show_density=False, high_density=True)
    def update(self)
    def draw(self)
```

### Key Methods

- `update_wind_pattern()`: Procedural wind pattern generation
- `generate_particles()`: Dynamic particle population control
- `update_density_map()`: Density visualization computation
- `draw_particles()`: Particle rendering with layer sorting

## Configuration

### Performance Tuning
- `UPDATE_INTERVAL`: Simulation time step (default: 0.03s)
- Particle count scaling based on terminal dimensions
- Layer-based rendering optimization

### Visual Parameters
- `WIND_CHARS`: Character set for particle rendering
- `WIND_PARTICLES`: Density visualization characters
- Color pair mappings for terminal compatibility

## Examples



## Performance Considerations

- Terminal size significantly impacts performance
- High density mode requires capable terminal emulators
- Color support affects visual quality but not core functionality
- Recommended minimum terminal size: 80x24 characters

## Compatibility

### Supported Systems
- Linux terminals ( Kitty, Konsole , etc.)
- macOS Terminal and iTerm2
- Windows Subsystem for Linux (WSL)
- Most POSIX-compliant terminal emulators

### Requirements
- Python curses module (standard library)
- Terminal with 256-color support recommended
- UTF-8 character encoding

## Development

### Building from Source
```bash
git clone https://github.com/your-username/cbreeze.git
cd cbreeze
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Testing
```bash
python -m pytest tests/
```

## License

MIT License - See LICENSE file for details.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## Version History

- 1.0.0: Initial release with core simulation features

## Support

For bug reports and feature requests, please use the GitHub issue tracker.

## Acknowledgments

- Inspired by terminal-based particle systems and fluid dynamics simulations
- Built upon Python's curses library for terminal graphics
- Algorithm references from computational fluid dynamics literature
