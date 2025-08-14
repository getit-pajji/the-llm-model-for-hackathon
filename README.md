# 🌊 AquaSentry: AI-Powered Marine Exploration Dashboard

![AquaSentry Banner](https://placehold.co/1200x300/0a2540/a7c7ee?text=AquaSentry%20Command%20Center)

**An intelligent, multi-page web application built with Python and Streamlit for real-time monitoring and AI-driven analysis of underwater environments. This project showcases the power of combining specialized AI models with a large language model for comprehensive understanding.**

[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-username/your-repo-name)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-username/your-repo-name)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ Features

- **🐠 AI-Powered Recognition**: Conceptually designed to use a multi-model approach:
    - **YOLOv8** for real-time object detection of marine life.
    - **YAMNet** for classifying underwater sounds from hydrophones.
    - **Llama 3.2 (90M)** for nuanced text-based assistance and summaries.
    - All insights are synthesized and explained by a powerful **Gemini-based script** for a rich user experience.
- **📊 Live Overview Dashboard**: Displays real-time (simulated) data from an underwater ROV, including depth, temperature, battery, and mission progress with live-updating charts.
- **📹 Multi-View Camera Feeds**: A dedicated control panel to switch between different ROV camera views (Forward, Bottom, Rear) and manage manual controls.
- **🎨 Immersive UI/UX**: Features a stunning, full-screen ocean background image with a responsive, modern interface designed for a command center feel.
- **🚀 Deployable & Scalable**: Ready for deployment on Vercel, allowing you to share your application with the world.

---

## 🚀 Live Demo

Experience the AquaSentry Command Center live!

**[➡️ Launch Live Demo](https://the-llm-model-for-hackathon.vercel.app/)**

![AquaSentry Screenshot](https://placehold.co/800x500/12294a/ffffff?text=AquaSentry%20Dashboard%20UI)

---

## 🛠️ Tech Stack

- **Backend & Frontend**: [Python](https://www.python.org/) with [Streamlit](https://streamlit.io/)
- **AI Models & Frameworks**:
    - **Core Logic**: Google Gemini 1.5 Flash (via API)
    - **Object Detection**: YOLOv8
    - **Audio Classification**: YAMNet
    - **Language Model**: Llama 3.2 (90M)
- **Data Visualization**: [Altair](https://altair-viz.github.io/)
- **Deployment**: [Vercel](https://vercel.com/)

---

## ⚙️ Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have Python 3.8+ installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install the required Python libraries:**
    Create a `requirements.txt` file with the following content:
    ```text
    streamlit
    google-generativeai
    pandas
    altair
    Pillow
    ```
    Then, run the installation command:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Gemini API Key:**
    - Create a folder in your project's root directory named `.streamlit`.
    - Inside this folder, create a file named `secrets.toml`.
    - Add your API key to this file:
      ```toml
      # .streamlit/secrets.toml
      GOOGLE_API_KEY = "AIzaSy...your...actual...api...key"
      ```

### Running Locally

1.  **Launch the application:**
    Open your terminal in the project's root directory and run:
    ```bash
    streamlit run app.py
    ```
    Your default web browser will open with the running application. The background image is set directly in the code.

---

## ☁️ Deployment to Vercel

This project is configured for easy deployment on Vercel.

1.  **Push your project to GitHub.**

2.  **Create configuration files:**
    - Ensure you have the `requirements.txt` file as described above.
    - Create a `vercel.json` file in your root directory:
      ```json
      {
        "builds": [
          {
            "src": "app.py",
            "use": "@vercel/python",
            "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
          }
        ],
        "routes": [ { "src": "/(.*)", "dest": "app.py" } ]
      }
      ```
    - Create a `.slugignore` file to reduce deployment size:
      ```
      __pycache__/
      *.pyc
      /venv/
      ```

3.  **Import your project on Vercel:**
    - Sign up or log in to [Vercel](https://vercel.com/).
    - Import your GitHub repository.

4.  **Set Environment Variables:**
    - In your Vercel project's settings, go to **Environment Variables**.
    - Add your Gemini API key:
      - **Name:** `GOOGLE_API_KEY`
      - **Value:** `AIzaSy...your...actual...api...key`

5.  **Deploy!** Vercel will automatically build and deploy your application.

---

## 📂 Project Structure


.
├── .streamlit/
│   └── secrets.toml      # Local API key storage
├── app.py                # Main Streamlit application script
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment configuration
└── .slugignore           # Vercel deployment ignore file
