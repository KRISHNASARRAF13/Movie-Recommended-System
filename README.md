# 🎬 Movie Recommendation System

A production-grade movie recommendation system built with **Content-Based Filtering** (TF-IDF + Cosine Similarity) and **Collaborative Filtering** (Truncated SVD Matrix Factorization), deployed as an interactive Streamlit web app.

---

## 👤 Developer

**Krishna Sarraf**  
B.Tech CSE · 3rd Year · VIT Vellore  
GitHub: [KRISHNASARRAF13](https://github.com/KRISHNASARRAF13)

---

## 📊 Dataset

**MovieLens ml-latest-small** — Harper & Konstan (2015), ACM TIIS  
- 9,742 movies | 100,836 ratings | 610 users  
- Rating scale: 0.5 – 5.0 (half-star)

---

## 🧠 Algorithms

| Method | Technique | Purpose |
|--------|-----------|---------|
| Content-Based | TF-IDF + Cosine Similarity | Find similar movies by genre |
| Collaborative | Truncated SVD (20 components) | Personalised user recommendations |
| Evaluation | RMSE on 80/20 train-test split | Model accuracy measurement |

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/KRISHNASARRAF13/Movie-Recommended-System.git
cd Movie-Recommended-System

# Create virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
├── app.py              # Streamlit UI (teal/gold dark theme)
├── recommender.py      # Core ML logic (TF-IDF, SVD, RMSE)
├── requirements.txt    # Python dependencies
└── data/
    ├── movies.csv      # MovieLens movie catalogue
    └── ratings.csv     # User ratings data
```

---

## 📦 Tech Stack

- **Python 3.9+**
- **Streamlit** — web UI
- **Scikit-Learn** — TF-IDF, SVD, RMSE
- **Pandas / NumPy** — data processing

---

## 📚 Reference

> Harper, F.M. & Konstan, J.A. (2015). *The MovieLens Datasets: History and Context.* ACM Transactions on Interactive Intelligent Systems, 5(4), Article 19. DOI: [10.1145/2827872](https://doi.org/10.1145/2827872)
