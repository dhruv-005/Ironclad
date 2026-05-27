# 🛡️ Ironclad - Advanced Face Detective & OSINT Engine

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Cost](https://img.shields.io/badge/Cost-$0-brightgreen)
![Local](https://img.shields.io/badge/Runs-100%25%20Local-purple)

## 🎯 What Is Ironclad?
Ironclad is a production-grade, completely free, locally-run
face-search and OSINT investigation engine. Upload a face image
and get a complete intelligence dossier including social media
profiles, professional background, news mentions, and more.

## ✨ Features
- 👁️ **ArcFace Biometric Analysis** - 99.8% accuracy face recognition
- 🔍 **Deep OSINT Search** - 15+ intelligence queries per target
- 📱 **Social Media Detection** - LinkedIn, Twitter, Facebook, Instagram, GitHub
- 🖼️ **Reverse Image Search** - Find where photos appear online
- 📋 **Full Dossier Report** - Structured markdown intelligence report
- ⚡ **Direct Mode** - No LLM required for fast results
- 🤖 **Agent Mode** - LangChain + Ollama AI reasoning
- 💰 **100% Free** - Zero API costs, runs fully local

## 🚀 Quick Start
\`\`\`bash
git clone https://github.com/YOURUSERNAME/Ironclad.git
cd Ironclad
pip install -r requirements.txt
python init_db.py
streamlit run app.py
\`\`\`

## 🏗️ Architecture
\`\`\`
User → Streamlit UI → Face Detection (ArcFace)
                    → FAISS Vector Search
                    → Deep OSINT (DuckDuckGo)
                    → Dossier Report Generation
\`\`\`

## 💻 Tech Stack
| Component | Technology |
|-----------|-----------|
| UI | Streamlit |
| Face AI | InsightFace ArcFace |
| Vector DB | FAISS HNSW |
| OSINT | DuckDuckGo API |
| LLM Brain | Ollama (optional) |
| Agent | LangChain ReAct |

## 📁 Project Structure
\`\`\`
Ironclad/
├── app.py              # Main UI & Investigation Engine
├── sherlock_server.py  # MCP Server
├── init_db.py          # Database Seeder
├── config/             # Settings & Config
├── utils/              # Helper Modules
├── assets/             # CSS & Images
├── profiles/           # Face Database Images
├── data/               # Vector Database
├── tests/              # Test Suite
└── logs/               # Investigation Reports
\`\`\`

## 📜 License
MIT License - See LICENSE file
