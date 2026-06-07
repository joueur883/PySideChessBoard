# Use the ChessBoard API

## **Note**: more API features will be added soon



### **Reset the board**
```python
board.resetBoard()
```


### **Set board position from FEN**
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

### Set the moves history
```python
board.setMovesHistory(["fen1", "fen2", "fen3", ...])
```

### Set the timeline position
```python
board.setTimelinePosition(0) # Start position
```
