const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// --- Constants ---
const WIDTH = 800, HEIGHT = 600, FPS = 30;
const PADDLE_WIDTH = 10, PADDLE_HEIGHT = 100, BALL_SIZE = 10;
const PADDLE_SPEED = 7, BALL_SPEED = 6, WINNING_SCORE = 5;
const WHITE = "#fff", FONT = "32px monospace", FONT_LARGE = "48px monospace";

// --- Game State ---
let state = "start"; // start, name1, name2, playing, gameover
let player1 = { name: "", score: 0, y: HEIGHT/2 - PADDLE_HEIGHT/2 };
let player2 = { name: "", score: 0, y: HEIGHT/2 - PADDLE_HEIGHT/2 };
let ball = { x: WIDTH/2 - BALL_SIZE/2, y: HEIGHT/2 - BALL_SIZE/2, vx: BALL_SPEED, vy: BALL_SPEED };
let winner = "";
let nameBuffer = "";
let keys = {};

// --- Helpers ---
function resetBall() {
    ball.x = WIDTH/2 - BALL_SIZE/2;
    ball.y = HEIGHT/2 - BALL_SIZE/2;
    ball.vx = (Math.random() > 0.5 ? 1 : -1) * BALL_SPEED;
    ball.vy = (Math.random() > 0.5 ? 1 : -1) * BALL_SPEED;
}
function resetGame() {
    player1.score = 0; player2.score = 0;
    player1.y = HEIGHT/2 - PADDLE_HEIGHT/2;
    player2.y = HEIGHT/2 - PADDLE_HEIGHT/2;
    resetBall();
    winner = "";
}

// --- Input ---
window.addEventListener('keydown', e => {
    keys[e.key.toLowerCase()] = true;
    if (state === "start" && e.code === "Space") {
        state = "name1"; nameBuffer = "";
    }
    if ((state === "name1" || state === "name2")) {
        if (e.key.length === 1 && nameBuffer.length < 12 && /^[a-zA-Z0-9 _-]$/.test(e.key)) {
            nameBuffer += e.key;
        }
        if (e.key === "Backspace") nameBuffer = nameBuffer.slice(0, -1);
        if (e.key === "Enter" && nameBuffer.trim()) {
            if (state === "name1") { player1.name = nameBuffer.trim(); state = "name2"; nameBuffer = ""; }
            else if (state === "name2") { player2.name = nameBuffer.trim(); state = "playing"; resetGame(); }
        }
    }
    if (state === "gameover" && (e.key === "r" || e.key === "R")) {
        state = "start";
    }
});
window.addEventListener('keyup', e => {
    keys[e.key.toLowerCase()] = false;
});

// --- Game Loop ---
function update() {
    if (state === "playing") {
        // Paddle movement
        if (keys["w"]) player1.y -= PADDLE_SPEED;
        if (keys["s"]) player1.y += PADDLE_SPEED;
        if (keys["arrowup"]) player2.y -= PADDLE_SPEED;
        if (keys["arrowdown"]) player2.y += PADDLE_SPEED;
        player1.y = Math.max(0, Math.min(HEIGHT - PADDLE_HEIGHT, player1.y));
        player2.y = Math.max(0, Math.min(HEIGHT - PADDLE_HEIGHT, player2.y));
        // Ball movement
        ball.x += ball.vx; ball.y += ball.vy;
        // Wall collision
        if (ball.y <= 0 || ball.y + BALL_SIZE >= HEIGHT) ball.vy *= -1;
        // Paddle collision
        if (ball.x <= 40 && ball.y + BALL_SIZE > player1.y && ball.y < player1.y + PADDLE_HEIGHT) {
            ball.vx = Math.abs(ball.vx);
        }
        if (ball.x + BALL_SIZE >= WIDTH - 40 && ball.y + BALL_SIZE > player2.y && ball.y < player2.y + PADDLE_HEIGHT) {
            ball.vx = -Math.abs(ball.vx);
        }
        // Score
        if (ball.x < 0) {
            player2.score++; resetBall();
        }
        if (ball.x > WIDTH) {
            player1.score++; resetBall();
        }
        // Win
        if (player1.score >= WINNING_SCORE) {
            winner = player1.name || "Player 1";
            state = "gameover";
        }
        if (player2.score >= WINNING_SCORE) {
            winner = player2.name || "Player 2";
            state = "gameover";
        }
    }
}

// --- Drawing ---
function draw() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
    ctx.fillStyle = WHITE;
    ctx.font = FONT;
    if (state === "start") {
        ctx.font = FONT_LARGE;
        ctx.textAlign = "center";
        ctx.fillText("PONG", WIDTH/2, 120);
        ctx.font = FONT;
        ctx.fillText("Press SPACE to Start", WIDTH/2, 200);
        ctx.font = "24px monospace";
        ctx.fillText("Controls:", WIDTH/2, 300);
        ctx.fillText("Player 1: W (up), S (down)", WIDTH/2, 340);
        ctx.fillText("Player 2: ↑ (up), ↓ (down)", WIDTH/2, 370);
    } else if (state === "name1" || state === "name2") {
        ctx.font = FONT;
        ctx.textAlign = "center";
        ctx.fillText(`Enter ${state === "name1" ? "Player 1" : "Player 2"} Name:`, WIDTH/2, 220);
        ctx.font = FONT_LARGE;
        ctx.fillText(nameBuffer + "|", WIDTH/2, 300);
        ctx.font = "24px monospace";
        ctx.fillText("Press ENTER to confirm", WIDTH/2, 370);
    } else if (state === "playing") {
        // Center line
        for (let y = 0; y < HEIGHT; y += 20) {
            ctx.fillRect(WIDTH/2 - 2, y, 4, 10);
        }
        // Paddles
        ctx.fillRect(30, player1.y, PADDLE_WIDTH, PADDLE_HEIGHT);
        ctx.fillRect(WIDTH - 40, player2.y, PADDLE_WIDTH, PADDLE_HEIGHT);
        // Ball
        ctx.fillRect(ball.x, ball.y, BALL_SIZE, BALL_SIZE);
        // Scores
        ctx.font = FONT_LARGE;
        ctx.textAlign = "center";
        ctx.fillText(`${player1.score}   ${player2.score}`, WIDTH/2, 50);
        // Names
        ctx.font = "24px monospace";
        ctx.textAlign = "left";
        ctx.fillText(player1.name, 50, 30);
        ctx.textAlign = "right";
        ctx.fillText(player2.name, WIDTH - 50, 30);
    } else if (state === "gameover") {
        ctx.font = FONT_LARGE;
        ctx.textAlign = "center";
        ctx.fillText(`${winner} Wins!`, WIDTH/2, 220);
        ctx.font = FONT;
        ctx.fillText("Press R to Restart", WIDTH/2, 300);
    }
}

// --- Main Loop ---
function loop() {
    update();
    draw();
    setTimeout(loop, 1000 / FPS);
}
loop();