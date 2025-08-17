## How it Works
The Knight's Tour algorithm in this project uses the **“minimum onward moves” strategy**:

1. **Place the Knight:** The user starts by clicking on any square on the chessboard to place the knight.
2. **Calculate Moves:** At each step, the algorithm calculates **all possible moves** the knight can make from its current position.
3. **Minimum Onward Moves:** For each possible move, it counts **how many future moves are available** from that new square.
4. **Select Move:** The knight moves to the square with the **minimum number of onward moves** (Warnsdorff's rule) to avoid dead-ends.
5. **Visual Feedback:**  
   - Current knight position is shown on the board.  
   - Previously visited squares are marked.  
   - Possible next moves are highlighted with **green lines**.
6. **Advance Move:** The user must **press the right arrow key** to make the knight perform its next move.
7. **Repeat:** Steps 2–6 repeat until the knight has visited all squares or no moves remain.

This creates an **interactive and animated visualization** of the knight completing its tour efficiently across the chessboard.
