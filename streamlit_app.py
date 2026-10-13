import streamlit as st

st.set_page_config(page_title="Game Rắn Săn Mồi", page_icon="🐍", layout="centered")
st.title("🐍 Trò chơi Rắn Săn Mồi!")
st.write("Bấm các nút mũi tên ở dưới bàn cờ để điều khiển rắn ăn mồi nhé!")

snake_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: #f0f2f6; margin: 0; padding: 5px; }
        canvas { background: #111; display: block; margin: 10px auto; border: 4px solid #333; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .score { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 5px; }
        .controls { display: grid; grid-template-columns: repeat(3, 1fr); width: 180px; margin: 15px auto; gap: 10px; }
        .btn { background: #4CAF50; color: white; border: none; padding: 15px; font-size: 18px; border-radius: 8px; cursor: pointer; touch-action: manipulation; }
        .btn:active { background: #3e8e41; }
        .empty { visibility: hidden; }
    </style>
</head>
<body>
    <div class="score">Điểm: <span id="scoreVal">0</span></div>
    <canvas id="gameCanvas" width="300" height="300"></canvas>

    <div class="controls">
        <div class="empty"></div>
        <button class="btn" onclick="changeDirection('UP')">▲</button>
        <div class="empty"></div>
        
        <button class="btn" onclick="changeDirection('LEFT')">◀</button>
        <button class="btn" id="startBtn" onclick="resetGame()" style="background:#2196F3; font-size:14px; padding:5px;">Chơi</button>
        <button class="btn" onclick="changeDirection('RIGHT')">▶</button>
        
        <div class="empty"></div>
        <button class="btn" onclick="changeDirection('DOWN')">▼</button>
        <div class="empty"></div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas"), ctx = canvas.getContext("2d");
        const grid = 15;
        let snake, dx, dy, food, score, gameInterval;

        function resetGame() {
            clearInterval(gameInterval);
            snake = [{x: 150, y: 150}, {x: 135, y: 150}];
            dx = grid; dy = 0; score = 0;
            document.getElementById("scoreVal").innerText = score;
            document.getElementById("startBtn").innerText = "Lại";
            generateFood();
            gameInterval = setInterval(update, 160);
        }

        function generateFood() {
            food = {
                x: Math.floor(Math.random() * (canvas.width / grid)) * grid,
                y: Math.floor(Math.random() * (canvas.height / grid)) * grid
            };
        }

        function changeDirection(dir) {
            if (dir === 'LEFT' && dx === 0) { dx = -grid; dy = 0; }
            if (dir === 'UP' && dy === 0) { dx = 0; dy = -grid; }
            if (dir === 'RIGHT' && dx === 0) { dx = grid; dy = 0; }
            if (dir === 'DOWN' && dy === 0) { dx = 0; dy = grid; }
        }

        function update() {
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};
            if (head.x < 0) head.x = canvas.width - grid;
            if (head.x >= canvas.width) head.x = 0;
            if (head.y < 0) head.y = canvas.height - grid;
            if (head.y >= canvas.height) head.y = 0;

            for (let i = 0; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    alert("Game Over! Điểm của bạn là: " + score);
                    clearInterval(gameInterval); return;
                }
            }

            snake.unshift(head);
            if (head.x === food.x && head.y === food.y) {
                score += 10; document.getElementById("scoreVal").innerText = score; generateFood();
            } else { snake.pop(); }

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#FF5722"; ctx.fillRect(food.x, food.y, grid - 2, grid - 2);
            snake.forEach((part, index) => {
                ctx.fillStyle = index === 0 ? "#8BC34A" : "#4CAF50";
                ctx.fillRect(part.x, part.y, grid - 2, grid - 2);
            });
        }
        resetGame();
    </script>
</body>
</html>
"""

st.components.v1.html(snake_html, height=530, scrolling=False)

