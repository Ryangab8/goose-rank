import streamlit as st
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Goose Song Ranker",
    page_icon="🪿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Preset options for song pool size
POOL_PRESETS = {
    "Top 25 Most Played": 25,
    "Top 50 Most Played": 50,
    "Top 100 Most Played": 100,
    "Top 150 Most Played": 150,
    "All Songs": None  # None means no limit
}

# Custom CSS for a distinctive look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --goose-orange: #FF6B35;
        --goose-teal: #00CED1;
        --goose-purple: #7B68EE;
        --goose-dark: #1a1a2e;
        --goose-darker: #0f0f1a;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--goose-darker) 0%, var(--goose-dark) 50%, #16213e 100%);
    }
    
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #fff !important;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--goose-orange), var(--goose-teal), var(--goose-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -1px;
    }
    
    .subtitle {
        text-align: center;
        color: #8892b0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        margin-top: 0;
    }
    
    .song-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .song-card:hover {
        background: rgba(255,107,53,0.15);
        border-color: var(--goose-orange);
        transform: translateY(-4px);
    }
    
    .song-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .song-artist {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--goose-teal);
    }
    
    .song-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .vs-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--goose-purple);
        text-align: center;
        margin: 1rem 0;
    }
    
    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--goose-orange), var(--goose-purple));
        color: white;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 1rem;
    }
    
    .rank-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #666;
        width: 40px;
    }
    
    .ranked-song {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid var(--goose-orange);
    }
    
    .category-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-family: 'JetBrains Mono', monospace;
        margin-left: 0.5rem;
    }
    
    .category-original { background: rgba(0,206,209,0.2); color: var(--goose-teal); }
    .category-side_project { background: rgba(123,104,238,0.2); color: var(--goose-purple); }
    .category-cover { background: rgba(255,107,53,0.2); color: var(--goose-orange); }
    
    .stButton > button {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stat-box {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    .stat-number {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--goose-orange);
    }
    
    .stat-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #8892b0;
    }
    
    div[data-testid="stSelectbox"] label {
        color: #8892b0 !important;
    }
</style>
""", unsafe_allow_html=True)


# Load songs database
@st.cache_data
def load_songs():
    with open('goose_songs.json', 'r') as f:
        data = json.load(f)
    return data['songs']


def get_beli_score(position: int, total: int) -> float:
    """Calculate Beli-style score (0-10) based on position in ranked list"""
    if total <= 1:
        return 10.0
    return round(10 - ((position - 1) / (total - 1)) * 10, 1)


def binary_search_insert(ranked_list: list, new_song: dict, comparisons: list) -> int:
    """
    Perform binary search to find correct position for new song.
    Returns the index where the song should be inserted.
    Uses comparisons list to track which songs to compare against.
    """
    if not ranked_list:
        return 0
    
    left, right = 0, len(ranked_list) - 1
    
    while left <= right:
        mid = (left + right) // 2
        comparisons.append(mid)
        return mid  # Return the mid index for comparison
    
    return left


def init_session_state():
    """Initialize session state variables"""
    if 'ranked_songs' not in st.session_state:
        st.session_state.ranked_songs = []
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'current_song' not in st.session_state:
        st.session_state.current_song = None
    if 'comparison_left' not in st.session_state:
        st.session_state.comparison_left = 0
    if 'comparison_right' not in st.session_state:
        st.session_state.comparison_right = 0
    if 'comparison_count' not in st.session_state:
        st.session_state.comparison_count = 0
    # Pool configuration settings
    if 'pool_size' not in st.session_state:
        st.session_state.pool_size = "Top 50 Most Played"
    if 'include_covers' not in st.session_state:
        st.session_state.include_covers = True
    if 'setup_complete' not in st.session_state:
        st.session_state.setup_complete = False


def get_filtered_song_pool(songs: list) -> list:
    """Get the song pool based on current settings"""
    pool = songs.copy()
    
    # Filter out covers if excluded
    if not st.session_state.include_covers:
        pool = [s for s in pool if s['category'] != 'cover']
    
    # Sort by times played (most played first)
    pool.sort(key=lambda x: x.get('times_played', 0), reverse=True)
    
    # Apply size limit
    limit = POOL_PRESETS.get(st.session_state.pool_size)
    if limit is not None:
        pool = pool[:limit]
    
    return pool


def start_ranking(song: dict):
    """Start the ranking process for a new song"""
    st.session_state.comparison_mode = True
    st.session_state.current_song = song
    st.session_state.comparison_left = 0
    st.session_state.comparison_right = len(st.session_state.ranked_songs) - 1
    st.session_state.comparison_count = 0


def process_comparison(prefer_new: bool):
    """Process comparison result and update search bounds"""
    left = st.session_state.comparison_left
    right = st.session_state.comparison_right
    mid = (left + right) // 2
    
    st.session_state.comparison_count += 1
    
    if prefer_new:
        # New song is better, search upper half (lower indices = higher rank)
        st.session_state.comparison_right = mid - 1
    else:
        # Existing song is better, search lower half
        st.session_state.comparison_left = mid + 1
    
    # Check if we've found the position
    if st.session_state.comparison_left > st.session_state.comparison_right:
        # Insert at comparison_left position
        insert_pos = st.session_state.comparison_left
        st.session_state.ranked_songs.insert(insert_pos, st.session_state.current_song)
        st.session_state.comparison_mode = False
        st.session_state.current_song = None
        st.rerun()


def get_comparison_song() -> dict:
    """Get the current song to compare against"""
    mid = (st.session_state.comparison_left + st.session_state.comparison_right) // 2
    return st.session_state.ranked_songs[mid]


def main():
    init_session_state()
    all_songs = load_songs()
    
    # Header
    st.markdown('<h1 class="main-title">🪿 Goose Ranker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Rank your favorite Goose songs, Beli-style</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Show setup screen if not complete
    if not st.session_state.setup_complete:
        st.markdown("### 🎛️ Configure Your Ranking Pool")
        st.markdown("*Choose how many songs you want to rank and whether to include covers*")
        
        st.markdown("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Pool Size")
            pool_choice = st.radio(
                "How many songs to rank?",
                list(POOL_PRESETS.keys()),
                index=1,  # Default to Top 50
                key="pool_size_radio",
                help="Songs are sorted by live play frequency - most played songs first"
            )
        
        with col2:
            st.markdown("#### Include Covers?")
            include_covers = st.radio(
                "Include cover songs?",
                ["Yes - Include covers", "No - Originals & side projects only"],
                index=0,
                key="covers_radio"
            )
        
        # Preview of pool
        st.markdown("---")
        st.markdown("#### 📊 Pool Preview")
        
        # Calculate preview
        preview_pool = all_songs.copy()
        if include_covers == "No - Originals & side projects only":
            preview_pool = [s for s in preview_pool if s['category'] != 'cover']
        preview_pool.sort(key=lambda x: x.get('times_played', 0), reverse=True)
        
        limit = POOL_PRESETS.get(pool_choice)
        if limit is not None:
            preview_pool = preview_pool[:limit]
        
        # Stats
        originals = sum(1 for s in preview_pool if s['category'] == 'original')
        side_projects = sum(1 for s in preview_pool if s['category'] == 'side_project')
        covers = sum(1 for s in preview_pool if s['category'] == 'cover')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Songs", len(preview_pool))
        with col2:
            st.metric("Originals", originals)
        with col3:
            st.metric("Side Projects", side_projects)
        with col4:
            st.metric("Covers", covers)
        
        # Show top 10 preview
        if preview_pool:
            st.markdown("**Top 10 in your pool (by play count):**")
            preview_text = ""
            for i, song in enumerate(preview_pool[:10], 1):
                preview_text += f"{i}. **{song['name']}** ({song.get('times_played', '?')}x) - {song['artist']}\n"
            st.markdown(preview_text)
            
            if len(preview_pool) > 10:
                min_plays = preview_pool[-1].get('times_played', 0)
                st.markdown(f"*...and {len(preview_pool) - 10} more songs (minimum {min_plays} plays)*")
        
        st.markdown("---")
        
        # Start button
        if st.button("🚀 Start Ranking!", type="primary", use_container_width=True):
            st.session_state.pool_size = pool_choice
            st.session_state.include_covers = (include_covers == "Yes - Include covers")
            st.session_state.setup_complete = True
            st.rerun()
        
        return  # Don't show main interface until setup is complete
    
    # Get filtered song pool based on settings
    song_pool = get_filtered_song_pool(all_songs)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎵 Add Songs", "📊 My Rankings", "⚙️ Settings", "ℹ️ About"])
    
    with tab1:
        # Show current pool info
        st.markdown(f"*Pool: {st.session_state.pool_size} • {'Including' if st.session_state.include_covers else 'Excluding'} covers • {len(song_pool)} songs available*")
        
        if st.session_state.comparison_mode:
            # Comparison UI
            st.markdown("### Which do you prefer?")
            st.markdown(f"*Comparison {st.session_state.comparison_count + 1}*")
            
            compare_song = get_comparison_song()
            new_song = st.session_state.current_song
            
            col1, col2, col3 = st.columns([5, 1, 5])
            
            with col1:
                st.markdown(f"""
                <div class="song-card" style="border-color: var(--goose-orange);">
                    <div class="song-name">{new_song['name']}</div>
                    <div class="song-artist">{new_song['artist']}</div>
                    <div class="song-meta">New song</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("⬆️ This one!", key="prefer_new", use_container_width=True):
                    process_comparison(prefer_new=True)
            
            with col2:
                st.markdown('<div class="vs-text">VS</div>', unsafe_allow_html=True)
            
            with col3:
                current_pos = (st.session_state.comparison_left + st.session_state.comparison_right) // 2 + 1
                current_score = get_beli_score(current_pos, len(st.session_state.ranked_songs))
                st.markdown(f"""
                <div class="song-card" style="border-color: var(--goose-teal);">
                    <div class="song-name">{compare_song['name']}</div>
                    <div class="song-artist">{compare_song['artist']}</div>
                    <div class="song-meta">Currently #{current_pos} • Score: {current_score}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("⬆️ This one!", key="prefer_existing", use_container_width=True):
                    process_comparison(prefer_new=False)
            
            st.markdown("---")
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.comparison_mode = False
                st.session_state.current_song = None
                st.rerun()
        
        else:
            # Song selection UI
            st.markdown("### Add a song to your rankings")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                category_filter = st.selectbox(
                    "Category",
                    ["All", "Originals", "Side Projects", "Covers"] if st.session_state.include_covers else ["All", "Originals", "Side Projects"],
                    key="category_filter"
                )
            with col2:
                search = st.text_input("Search songs", key="search", placeholder="Type to search...")
            
            # Filter songs from the pool
            filtered_songs = song_pool.copy()
            
            # Exclude already ranked songs
            ranked_names = {s['name'] for s in st.session_state.ranked_songs}
            filtered_songs = [s for s in filtered_songs if s['name'] not in ranked_names]
            
            if category_filter != "All":
                cat_map = {
                    "Originals": "original",
                    "Side Projects": "side_project", 
                    "Covers": "cover"
                }
                filtered_songs = [s for s in filtered_songs if s['category'] == cat_map[category_filter]]
            
            if search:
                search_lower = search.lower()
                filtered_songs = [s for s in filtered_songs if search_lower in s['name'].lower() or search_lower in s['artist'].lower()]
            
            # Already sorted by times played from pool
            
            # Display songs
            remaining = len([s for s in song_pool if s['name'] not in ranked_names])
            st.markdown(f"*Showing {len(filtered_songs)} of {remaining} unranked songs*")
            
            # Quick add for first song
            if len(st.session_state.ranked_songs) == 0:
                st.info("👆 Pick your first song to start building your rankings!")
            
            # Song grid
            for i in range(0, min(len(filtered_songs), 50), 2):
                cols = st.columns(2)
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(filtered_songs):
                        song = filtered_songs[idx]
                        cat_class = f"category-{song['category']}"
                        cat_label = song['category'].replace('_', ' ').title()
                        
                        with col:
                            with st.container():
                                st.markdown(f"""
                                **{song['name']}**  
                                <span style="color: #00CED1; font-size: 0.85rem;">{song['artist']}</span>
                                <span class="category-pill {cat_class}">{cat_label}</span>  
                                <span style="color: #666; font-size: 0.75rem;">Played {song.get('times_played', '?')}x</span>
                                """, unsafe_allow_html=True)
                                
                                if st.button("➕ Add", key=f"add_{song['name']}", use_container_width=True):
                                    if len(st.session_state.ranked_songs) == 0:
                                        st.session_state.ranked_songs.append(song)
                                        st.rerun()
                                    else:
                                        start_ranking(song)
                                        st.rerun()
    
    with tab2:
        st.markdown("### Your Rankings")
        
        if not st.session_state.ranked_songs:
            st.info("🎵 No songs ranked yet! Go to 'Add Songs' to start building your list.")
        else:
            # Progress bar
            total_in_pool = len(song_pool)
            ranked_count = len(st.session_state.ranked_songs)
            progress = ranked_count / total_in_pool if total_in_pool > 0 else 0
            
            st.progress(progress, text=f"Ranked {ranked_count} of {total_in_pool} songs ({progress*100:.0f}%)")
            
            # Stats row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{len(st.session_state.ranked_songs)}</div>
                    <div class="stat-label">Songs Ranked</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                originals = sum(1 for s in st.session_state.ranked_songs if s['category'] == 'original')
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{originals}</div>
                    <div class="stat-label">Originals</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                side_projects = sum(1 for s in st.session_state.ranked_songs if s['category'] == 'side_project')
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{side_projects}</div>
                    <div class="stat-label">Side Projects</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                covers = sum(1 for s in st.session_state.ranked_songs if s['category'] == 'cover')
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{covers}</div>
                    <div class="stat-label">Covers</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Rankings list
            for i, song in enumerate(st.session_state.ranked_songs, 1):
                score = get_beli_score(i, len(st.session_state.ranked_songs))
                cat_class = f"category-{song['category']}"
                cat_label = song['category'].replace('_', ' ').title()
                
                col1, col2, col3, col4 = st.columns([1, 6, 2, 1])
                
                with col1:
                    st.markdown(f"<div style='font-size: 1.5rem; font-weight: 700; color: #666;'>#{i}</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    **{song['name']}**  
                    <span style="color: #00CED1; font-size: 0.85rem;">{song['artist']}</span>
                    <span class="category-pill {cat_class}">{cat_label}</span>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f'<span class="score-badge">{score}</span>', unsafe_allow_html=True)
                
                with col4:
                    if st.button("🗑️", key=f"del_{i}", help="Remove from rankings"):
                        st.session_state.ranked_songs.pop(i-1)
                        st.rerun()
                
                st.markdown("<hr style='margin: 0.5rem 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
            
            # Clear all button
            st.markdown("---")
            if st.button("🗑️ Clear All Rankings", type="secondary"):
                st.session_state.ranked_songs = []
                st.rerun()
    
    with tab3:
        st.markdown("### ⚙️ Pool Settings")
        st.markdown(f"""
        **Current Configuration:**
        - Pool Size: **{st.session_state.pool_size}**
        - Covers: **{'Included' if st.session_state.include_covers else 'Excluded'}**
        - Songs in Pool: **{len(song_pool)}**
        - Songs Ranked: **{len(st.session_state.ranked_songs)}**
        """)
        
        st.markdown("---")
        
        st.warning("⚠️ Changing settings will reset your current rankings!")
        
        if st.button("🔄 Change Pool Settings", use_container_width=True):
            st.session_state.ranked_songs = []
            st.session_state.setup_complete = False
            st.session_state.comparison_mode = False
            st.session_state.current_song = None
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 📊 Pool Statistics")
        
        # Play count distribution
        play_counts = [s.get('times_played', 0) for s in song_pool]
        if play_counts:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Most Played", f"{max(play_counts)}x")
            with col2:
                st.metric("Avg Plays", f"{sum(play_counts)//len(play_counts)}x")
            with col3:
                st.metric("Min Plays", f"{min(play_counts)}x")
        
        # Top 5 most played in pool
        st.markdown("**Most Played Songs in Your Pool:**")
        for i, song in enumerate(song_pool[:5], 1):
            cat_label = song['category'].replace('_', ' ').title()
            st.markdown(f"{i}. **{song['name']}** - {song.get('times_played', '?')} plays ({cat_label})")
    
    with tab4:
        st.markdown("""
        ### How It Works
        
        **Goose Ranker** uses the same ranking system as [Beli](https://beliapp.com) - instead of 
        giving songs arbitrary star ratings, you make **pairwise comparisons**.
        
        #### The Process:
        1. **Pick a song** to add to your rankings
        2. If you have existing rankings, you'll be asked: *"Which do you prefer?"*
        3. Through ~log₂(n) comparisons, the app finds exactly where your new song fits
        4. Your rankings are mapped to a **0-10 scale** (top song = 10.0)
        
        #### Why This Works:
        - **Relative rankings** are more meaningful than absolute scores
        - No more agonizing over "is this a 7 or an 8?"
        - Your list reflects YOUR taste, not crowd consensus
        - Rankings stay consistent as you add more songs
        
        ---
        
        ### Song Database
        
        This app includes **250+ songs** from the Goose catalog:
        - 🎸 **Originals** - Songs written by Goose
        - 🎭 **Side Projects** - Vasudo, Great Blue, Swimmer, Orebolo, St. John's Revival
        - 🎤 **Covers** - From Grateful Dead to Talking Heads to Prince
        
        Data sourced from [El Goose.net](https://elgoose.net)
        
        ---
        
        *Built with Streamlit • 🪿 Honk Honk*
        """)


if __name__ == "__main__":
    main()
