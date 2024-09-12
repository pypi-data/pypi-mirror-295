# C2048
C2048 is a Python library that implements the 2048 game written in Rust.

The game loop should look like this
```python
from c2048 import C2048, Move
game = C2048()

while True:
    print(f"Score: {game.score()}")
    print(game)
    # pick a random move
    move = Move.random()
    game.move(move)
    
    if game.has_moved:
        # Probability of getting a 2
        game.spawn_tile(0.9)
        # resets the game.has_moved
        game.reset()
    
    if game.is_win():
        print("You win, max tile: ", game.highest())
        break
    elif game.is_lose():
        print("You lose, max tile: ", game.highest())
        break
```