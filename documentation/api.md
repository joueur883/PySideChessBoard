# Use the ChessBoard API

## **Note**: more API features will be added soon


# Board utilities

### Reset the board
```python
board.resetBoard()
```

### Set a custom board
```python
board.setBoard(chess.Board())
```

### Get the current board
```python
board.getBoard()
```

### Set the turn
```python
# With the chess module
import chess
board.setTurn(chess.WHITE) # White's turn
board.setTurn(chess.BLACK) # Black's turn

# With boolean
board.setTurn(True) # White's turn
board.setTurn(False) # Black's turn
```

### Get the turn
```python
board.getTurn()
```


### Set board position from FEN
```python
board.setFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
```

### Select white/black view
```python
board.setIsWhiteView(True) # White view
board.setIsWhiteView(False) # Black view
```

### Set the squares size
```python
board.setTileSize(100) # Default value: 80
```

### Enable/disable legal moves highlighting
```python
board.setShowLegalMoves(True) # Enabled
board.setShowLegalMoves(False) # Disabled
```


# Graphics

### Add an arrow
```python
board.addOrRemoveArrow("e2", "e4") # Adds the arrow if it doesn't exists
# If the arrow exists, it removes it
```

### Check if an arrow is somewhere
```python
board.isArrowAt("e2", "e4")
```

### Clear all arrows
```python
board.clearAllArrows()
```

### Add color annotation
```python
board.addColorAnnotation("e4", "red") # Red annotation
board.addColorAnnotation("d4", "yellow") # Yellow annotation
board.addColorAnnotation("e5", "green") # Green annotation
board.addColorAnnotation("d5", "blue") # Blue annotation
```

### Remove a color annotation
```python
board.removeColorAnnotation("e4")
```

### Clear all color annotations
```python
board.clearAllColorAnnotations()
```



# History management

### Set the moves history
```python
board.setMovesHistory(["fen1", "fen2", "fen3", ...])
```

### Get the moves history
```python
board.getMovesHistory()
```

### Set the timeline position
```python
board.setTimelinePosition(0) # Start position
```



### Get the timeline position
```python
board.getTimelinePosition()
```
