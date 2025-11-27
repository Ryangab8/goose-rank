# 🪿 Goose Song Ranker

A Streamlit app that lets you rank Goose songs using **Beli-style pairwise comparisons** instead of arbitrary star ratings.

## How It Works

Instead of asking "rate this song 1-10", Goose Ranker asks: **"Which do you prefer: Song A or Song B?"**

Through a series of binary comparisons (using a binary search algorithm), the app slots each new song into exactly the right position in your personal rankings. Your final list is then mapped to a 0-10 scale where your #1 song = 10.0.

### Why Pairwise Comparisons?
- **More meaningful** - Relative rankings beat absolute scores
- **No decision paralysis** - Just pick A or B, no agonizing over numbers  
- **Consistent** - Your rankings stay coherent as you add more songs
- **Personal** - Reflects YOUR taste, not crowd consensus

## Features

- 📊 **257 songs** from the Goose catalog with play frequency data
- 🎛️ **Configurable pool size** - Choose to rank Top 25, 50, 100, 150, or all songs
- 🎸 **Cover toggle** - Include or exclude covers from your ranking pool
- 📈 **Play frequency sorting** - Songs ordered by how often Goose plays them live
- 🔍 Search songs by name or artist
- 📊 Live Beli-style scores (0-10)
- 📈 Progress tracking - see how far along you are in ranking your pool
- 💾 Rankings persist in your session

## Pool Presets

| Preset | Songs | ~Comparisons to Rank All |
|--------|-------|--------------------------|
| Top 25 | 25 | ~117 |
| Top 50 | 50 | ~282 |
| Top 100 | 100 | ~665 |
| Top 150 | 150 | ~1,082 |
| All Songs | 257 | ~2,056 |

*Comparisons estimated using n × log₂(n)*

## Try It Live

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/goose-song-ranker.git
cd goose-song-ranker

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Fork this repo to your GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your forked repo
5. Set main file to `app.py`
6. Deploy!

## Song Database

Data sourced from [El Goose.net](https://elgoose.net) - the comprehensive Goose setlist database.

Includes:
- **Goose Originals** - Arcadia, Madhuvan, Hot Tea, etc.
- **Side Projects** - Vasudo (Flodown, Tumble), Great Blue (Yeti, Pancakes), Swimmer, Orebolo
- **Covers** - Grateful Dead, The Band, Talking Heads, Prince, and 100+ more

## Tech Stack

- [Streamlit](https://streamlit.io) - The app framework
- Python - Core logic
- JSON - Song database

## Credits

- Song data: [El Goose.net](https://elgoose.net)
- Ranking concept: [Beli](https://beliapp.com)
- Band: [Goose](https://goosetheband.com) 🪿

---

*Honk Honk* 🪿
