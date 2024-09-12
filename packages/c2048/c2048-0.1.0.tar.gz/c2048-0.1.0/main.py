from c2048 import C2048, Move

game = C2048()
print(game)

# clones the game, so the original doesn't get affected
down = game.clone_move(Move.Down)
print(down)

# moves up, changing the original
game.move(Move.Left)
print(game)

# Prints all the moves done
print(game.moves)

# The main loop should be like this
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

# to get the all the moves
# print(f"Moves: {game.moves}")

# to get all the tile spawns
# print(f"Spawns: {game.spawns}")