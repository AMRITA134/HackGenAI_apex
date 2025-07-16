# HackGenAI_apex




Absolutely! Here's a **step-by-step guide** to run your `real_timewebcam.py` file using DeepFace on a **new computer** from scratch:

---

## ✅ Prerequisites

Make sure:

* You have **Python 3.10** installed (required for TensorFlow 2.11).
* You know the script is compatible with DeepFace and a webcam.

---

## 💻 Step-by-Step Instructions

### 🥽 1. **Install Python 3.10**

* Download from [https://www.python.org/downloads/release/python-3100/](https://www.python.org/downloads/release/python-3100/)
* During installation:

  * ✅ Check **"Add Python to PATH"**
  * ✅ Choose "Customize Installation" → Make sure `pip` is selected

---

### 🗂️ 2. **Open Command Prompt (cmd) and navigate to your script folder**

```bash
cd D:\python
```

(Replace `D:\python` with your actual folder path)

---

### 🧪 3. **Create a virtual environment**

```bash
py -3.10 -m venv emotion-env
```

Then activate it:

```bash
emotion-env\Scripts\activate
```

You should now see:
`(emotion-env)` in the terminal prompt.

---

### 📦 4. **Install required packages**

Install these **exact versions** to avoid compatibility issues:

```bash
pip install numpy==1.26.4
pip install tensorflow==2.11.0 keras==2.11.0 protobuf==3.19.6 tensorboard==2.11.0
pip install opencv-python
pip install deepface
```

> 💡 This ensures everything works with DeepFace and your webcam.

---

### 🎥 5. **Run your Python script**

```bash
python real_timewebcam.py
```

---

## 🧼 Optional (but recommended)

### 📌 Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

---

## ✅ Common Issues to Avoid

| Issue                                   | Fix                                 |
| --------------------------------------- | ----------------------------------- |
| `ImportError: cannot import name 'xxx'` | Ensure package versions are correct |
| Webcam doesn’t open                     | Make sure no other app is using it  |
| `TensorFlow` too new or old             | Stick to `tensorflow==2.11.0`       |
| Wrong Python version                    | Use **Python 3.10** only            |

---

Would you like me to turn this into a ready-to-share `.txt` or `.md` setup guide too?
