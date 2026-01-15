# 🎨 Visual Painter – Hand Gesture Based Drawing App

A **virtual drawing application** built using **OpenCV** and **MediaPipe**, where you can draw on the screen using **hand gestures** instead of a mouse or stylus.  
Your **index finger becomes the brush**, and different hand gestures let you **select colors, draw, or erase** in real time using your webcam.

---

## ✨ Features

- 🖐️ **Hand Tracking** using MediaPipe
- ✏️ **Draw with index finger**
- 🎨 **Color selection** using two-finger gesture
- 🧽 **Eraser mode**
- 🖼️ **Overlay toolbar** for brush colors
- ⚡ **Real-time FPS display**
- 📷 Works with any standard webcam

---

## 🧠 How It Works

The project uses:

- **MediaPipe Hands** to detect hand landmarks
- A custom **HandTrackingModule**
- Finger state detection (open / closed fingers)
- Gesture-based mode switching:
  - **Selection Mode** → Choose color
  - **Drawing Mode** → Draw on canvas

---

## 🖐️ Gesture Controls

| Gesture                       | Action                        |
| ----------------------------- | ----------------------------- |
| ✋ All fingers up             | Reset / Eraser mode           |
| ✌️ Index + Middle fingers     | Selection mode (choose color) |
| ☝️ Only index finger          | Drawing mode                  |
| ☝️ Index finger (black color) | Eraser                        |

---

## 🛠️ Requirements

Install the required dependencies:

```bash
pip install opencv-python mediapipe numpy
```

---

## How to Run?!

1. Clone the repository
2. Ensure your webcam is connected
3. Run the main file:

```bash
python main.py
```

---
