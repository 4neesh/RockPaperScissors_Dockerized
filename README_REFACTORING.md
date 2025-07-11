# Rock-Paper-Scissors Refactoring

## Overview
This refactoring improves the modularity and separation of concerns in the Rock-Paper-Scissors codebase to make it easier to extend to new game types like Rock-Paper-Scissors-Lizard-Spock.

## Key Improvements

### 1. Extracted Game Flow Management
- Created `GameFlowManager` class to handle round execution and timeout logic
- Removed duplicate timeout handling code from main game class
- Centralized round management logic

### 2. Improved Abstraction
- Created generic `GameMove` interface for moves/gestures
- Decoupled game-specific logic from generic game framework
- Made `HandGesture` implement the generic interface

### 3. Enhanced Modularity
- Separated game-specific constants from generic game constants
- Created specialized configuration classes for different game types
- Improved separation between game logic and presentation

### 4. Better Extensibility
- Game rules are now completely data-driven
- Easy to add new game types by implementing the interfaces
- Reduced coupling between components

### 5. Cleaner Code Structure
- Shorter, more focused methods
- Better separation of concerns
- More descriptive class and method names

## Files Modified/Created

### Core Framework (Generic)
- `src/core/game_move.py` - Generic move interface
- `src/core/game_flow_manager.py` - Centralized game flow management
- `src/core/timeout_handler.py` - Centralized timeout handling
- `src/core/round_executor.py` - Round execution logic

### Game-Specific (RPS)
- `src/games/rps/rps_move.py` - RPS-specific move implementation
- `src/games/rps/rps_game.py` - Refactored RPS game class
- `src/games/rps/rps_constants.py` - RPS-specific constants

### Updated Files
- `src/constants.py` - Cleaned up and separated concerns
- `game_paper_scissors_rock.py` - Simplified main game class
- Various other files updated for consistency

## Benefits

1. **Easier to extend**: Adding Rock-Paper-Scissors-Lizard-Spock now only requires:
   - Creating new move enum
   - Defining new rules
   - Adding new constants
   - No changes to core game logic

2. **Better maintainability**: 
   - Shorter methods with single responsibilities
   - Clear separation between generic and game-specific code
   - Eliminated code duplication

3. **Improved testability**: 
   - Smaller, focused classes are easier to test
   - Better mocking capabilities
   - Clear interfaces for testing

4. **Enhanced readability**: 
   - More descriptive names
   - Better organization of code
   - Clearer flow of execution

## Usage

The refactored code maintains the same external interface, so existing usage patterns remain unchanged.