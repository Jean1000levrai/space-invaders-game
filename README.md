# Space Invaders Game

## 🕹️ Description

Project made for school. 
A Space Invaders like game: you are a small ship, invaders are dropping from space, eliminate them before they touch the ground or loose! 
I have learnt about basic 2D game logic and object oriented programming.


## 🚀 Features

- Player-controlled spaceship
- Multiple enemy invaders
- 3 Health Points

## 🛠️ Technologies Used

- Python 3.10
- Tkinter
- Pillow for images
- Pygame for sound

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jean1000levrai/space-invaders-game.git
   cd space-invaders-game
   ```
2. Create a virtual environment (optional but recommended):
    Mac or Linux
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    Windows
    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## ▶️ How to Play

1. Run the game:

    ```bash
    python space_invader.py
    ```

2. Controls:
    - Move: <Arrow keys>
    - Shoot: <Space>

## 📁 Project Structure

    ```bash
    space-invaders-game/
    ├── space_invader.py
    ├── open_img_tk.py
    ├── liste_cahinee_double.py
    ├── img/
    ├── sounds/
    ├── README.md
    └── requirements.txt
    ```

## 🧩 Known Issues / To Do

- sound: remove commented line regarding sound and add pygame
- Play button didn't work in macos for some reason

## 📄 License

MIT license



