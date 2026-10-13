import streamlit as st

st.set_page_config(page_title="Game Rắn Săn Mồi Pro", page_icon="🐍", layout="centered")
st.title("🐍 Game Rắn Săn Mồi Cực Đẹp!")
st.write("Đầu rắn có mắt, mồi hình quả táo 🍎 và bàn cờ phong cách Google Snake!")

snake_apple_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f6; margin: 0; padding: 5px; }
        .score-box { background: #ffffff; display: inline-block; padding: 8px 20px; border-radius: 20px; font-size: 22px; font-weight: bold; color: #2e7d32; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 5px; }
        canvas { display: block; margin: 10px auto; border: 5px solid #2e7d32; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.15); }
        .controls { display: grid; grid-template-columns: repeat(3, 1fr); width: 200px; margin: 15px auto; gap: 12px; }
        .btn { background: #4CAF50; color: white; border: none; padding: 18px; font-size: 20px; font-weight: bold; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.15); touch-action: manipulation; }
        .btn:active { background: #388E3C; transform: scale(0.95); }
        .empty { visibility: hidden; }
    </style>
</head>
<body>
    <div class="score-box">🍎 Điểm: <span id="scoreVal">0</span></div>
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
        const grid = 20; // Tăng kích thước ô lên cho sắc nét hơn
        let snake, dx, dy, food, score, gameInterval;

        function resetGame() {
            clearInterval(gameInterval);
            snake = [
                {x: 140, y: 140},
                {x: 120, y: 140},
                {x: 100, y: 140}
            ];
            dx = grid; dy = 0; score = 0;
            document.getElementById("scoreVal").innerText = score;
            document.getElementById("startBtn").innerText = "Lại";
            generateFood();
            gameInterval = setInterval(update, 170); // Tốc độ vừa vặn cho điện thoại
        }

        function generateFood() {
            // Đảm bảo mồi xuất hiện trúng ô ma trận
            food = {
                x: Math.floor(Math.random() * (canvas.width / grid)) * grid,
                y: Math.floor(Math.random() * (canvas.height / grid)) * grid
            };
            // Không cho quả táo mọc đè lên thân rắn
            for (let i = 0; i < snake.length; i++) {
                if (food.x === snake[i].x && food.y === snake[i].y) {
                    generateFood();
                    break;
                }
            }
        }

        function changeDirection(dir) {
            if (dir === 'LEFT' && dx === 0) { dx = -grid; dy = 0; }
            if (dir === 'UP' && dy === 0) { dx = 0; dy = -grid; }
            if (dir === 'RIGHT' && dx === 0) { dx = grid; dy = 0; }
            if (dir === 'DOWN' && dy === 0) { dx = 0; dy = grid; }
        }

        // Hỗ trợ nút bàn phím nếu mở trên máy tính
        document.addEventListener("keydown", e => {
            if (e.key === "ArrowLeft" || e.key === "a") changeDirection('LEFT');
            if (e.key === "ArrowUp" || e.key === "w") changeDirection('UP');
            if (e.key === "ArrowRight" || e.key === "d") changeDirection('RIGHT');
            if (e.key === "ArrowDown" || e.key === "s") changeDirection('DOWN');
        });

        // Hàm vẽ quả táo sắc nét
        function drawApple(x, y) {
            let r = grid / 2;
            let cx = x + r;
            let cy = y + r;
            
            // Vẽ thân quả táo đỏ mọng
            ctx.fillStyle = "#e74c3c";
            ctx.beginPath();
            ctx.arc(cx - 2, cy + 1, r - 2, 0, 2 * Math.PI);
            ctx.arc(cx + 2, cy + 1, r - 2, 0, 2 * Math.PI);
            ctx.fill();
            
            // Vẽ cuống táo màu nâu
            ctx.strokeStyle = "#795548";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(cx, cy - 4);
            ctx.quadraticCurveTo(cx + 2, cy - 10, cx + 5, cy - 9);
            ctx.stroke();
            
            // Vẽ lá táo màu xanh cỏ
            ctx.fillStyle = "#2ecc71";
            ctx.beginPath();
            ctx.ellipse(cx + 3, cy - 7, 3, 1.5, Math.PI / 4, 0, 2 * Math.PI);
            ctx.fill();
        }

        // Hàm vẽ con rắn cute có mắt
        function drawSnake() {
            snake.forEach((part, index) => {
                let r = 4; // Độ bo góc đốt thân
                
                if (index === 0) { // ĐẦU RẮN (Màu xanh ngọc đậm hơn)
                    ctx.fillStyle = "#27ae60";
                    ctx.beginPath();
                    ctx.roundRect(part.x + 1, part.y + 1, grid - 2, grid - 2, 8);
                    ctx.fill();
                    
                    // Vẽ 2 mắt đen nhấp nháy dựa theo hướng đi của rắn
                    ctx.fillStyle = "#ffffff"; // Lòng trắng
                    let mx1, my1, mx2, my2;
                    if (dx > 0) { // Đi phải
                        mx1 = part.x + 12; my1 = part.y + 4; mx2 = part.x + 12; my2 = part.y + 12;
                    } else if (dx < 0) { // Đi trái
                        mx1 = part.x + 4; my1 = part.y + 4; mx2 = part.x + 4; my2 = part.y + 12;
                    } else if (dy < 0) { // Đi lên
                        mx1 = part.x + 4; my1 = part.y + 4; mx2 = part.x + 12; my2 = part.y + 4;
                    } else { // Đi xuống
                        mx1 = part.x + 4; my1 = part.y + 12; mx2 = part.x + 12; my2 = part.y + 12;
                    }
                    ctx.beginPath(); ctx.arc(mx1, my1, 2.5, 0, 2 * Math.PI); ctx.arc(mx2, my2, 2.5, 0, 2 * Math.PI); ctx.fill();
                    ctx.fillStyle = "#000000"; // Lòng đen mắt
                    ctx.beginPath(); ctx.arc(mx1, my1, 1.2, 0, 2 * Math.PI); ctx.arc(mx2, my2, 1.2, 0, 2 * Math.PI); ctx.fill();
                    
                } else { // THÂN RẮN (Màu xanh sáng bo tròn nhẹ)
                    ctx.fillStyle = "#2ecc71";
                    ctx.beginPath();
                    ctx.roundRect(part.x + 1, part.y + 1, grid - 2, grid - 2, 5);
                    ctx.fill();
                }
            });
        }

        function update() {
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};
            
            // Xử lý xuyên tường sang bờ bên kia
            if (head.x < 0) head.x = canvas.width - grid;
            if (head.x >= canvas.width) head.x = 0;
            if (head.y < 0) head.y = canvas.height - grid;
            if (head.y >= canvas.height) head.y = 0;

            // Kiểm tra cắn vào đuôi
            for (let i = 0; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    alert("💥 GAME OVER! Điểm số của bạn: " + score + "\\nBấm OK rồi ấn nút Lại để phục thù!");
                    clearInterval(gameInterval); return;
                }
            }

            snake.unshift(head);
            if (head.x === food.x && head.y === food.y) {
                score += 10; document.getElementById("scoreVal").innerText = score; generateFood();
            } else { snake.pop(); }

            // VẼ BÀN CỜ HIỆU ỨNG CARO (GOOGLE SNAKE STYLE)
            for (let row = 0; row < canvas.height / grid; row++) {
                for (let col = 0; col < canvas.width / grid; col++) {
                    ctx.fillStyle = (row + col) % 2 === 0 ? "#aad751" : "#a2d149"; // Hai màu xanh đan xen
                    ctx.fillRect(col * grid, row * grid, grid, grid);
                }
            }

            // Vẽ quả táo đỏ và chú rắn hoạt hình
            drawApple(food.x, food.y);
            drawSnake();
        }
        resetGame();
    </script>
</body>
</html>
"""

st.components.v1.html(snake_apple_html, height=560, scrolling=False)
