# 🏓 Ping Pong Game

This is a simple 2D ping pong game built with Pygame.
Two players can compete by controlling paddles to hit a bouncing ball.

You can play it directly in your browser here:  
🌐 **[Play the Game](https://maplesofficial.com/projects/pingpong)**  


## 🛠️ Technologies Used
- **Python**
- **Pygame**
- **Pygbag** – to run the game in the browser (WebAssembly)

## 🖥️ How to Run Locally

1. **Install Python**  
   Make sure Python 3.x is installed on your machine.

2. **Install Pygame**  
   ```bash
   pip install pygame

3. **Run the Game**
   ```bash
   python main.py

## 🌐 Web Version with Pygbag
This game was converted to WebAssembly using Pygbag, allowing it to run directly in the browser.

To build your own web version:
```bash
  pip install pygbag
  pygbag --build main.py
```
Upload the ```build/``` folder contents to GitHub Pages or any web hosting platform.

## 🎮 Controls
- **Left Player**: ```W``` and ```S```
- **Right Player**: ```↑``` and ```↓```

## Inspiration

This project was inspired by a YouTube tutorial: [*Ping Pong Game Tutorial*](https://www.youtube.com/watch?v=vVGTZlnnX3U)  
I followed the tutorial and then modified the game to make it my own.
