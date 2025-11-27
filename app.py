import streamlit as st
import json
import base64
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
    "Top 25": 25,
    "Top 50": 50,
    "Top 100": 100,
    "Top 150": 150,
    "All Songs": None
}

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --goose-orange: #FF6B35;
        --goose-teal: #00CED1;
        --goose-purple: #7B68EE;
        --goose-green: #50C878;
        --goose-red: #FF6B6B;
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
    }
    
    .subtitle {
        text-align: center;
        color: #8892b0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }
    
    .tinder-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border: 2px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin: 1rem 0;
    }
    
    .song-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .song-artist {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        color: var(--goose-teal);
        margin-bottom: 0.5rem;
    }
    
    .song-plays {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #666;
    }
    
    .vs-badge {
        background: var(--goose-purple);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        margin: 1rem 0;
    }
    
    .comparison-song {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .comparison-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        color: #ccc;
    }
    
    .comparison-rank {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #666;
    }
    
    .swipe-btn-left {
        background: linear-gradient(135deg, var(--goose-red), #cc5555) !important;
        color: white !important;
        font-size: 1.5rem !important;
        padding: 1rem 2rem !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 700 !important;
    }
    
    .swipe-btn-right {
        background: linear-gradient(135deg, var(--goose-green), #40a060) !important;
        color: white !important;
        font-size: 1.5rem !important;
        padding: 1rem 2rem !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 700 !important;
    }
    
    .instruction-box {
        background: rgba(123,104,238,0.15);
        border: 1px solid var(--goose-purple);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .instruction-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #b8b8d0;
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
    
    .category-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-family: 'JetBrains Mono', monospace;
        margin-left: 0.5rem;
    }
    
    .category-original { background: rgba(0,206,209,0.2); color: var(--goose-teal); }
    .category-cover { background: rgba(255,107,53,0.2); color: var(--goose-orange); }
    
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
    
    .progress-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #8892b0;
        text-align: center;
    }
    
    .user-badge {
        background: linear-gradient(135deg, var(--goose-teal), var(--goose-purple));
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .share-code {
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--goose-teal);
        word-break: break-all;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_songs():
    """Load and process songs - combine side_project into original"""
    with open('goose_songs.json', 'r') as f:
        data = json.load(f)
    
    songs = data['songs']
    # Combine side_project into original
    for song in songs:
        if song['category'] == 'side_project':
            song['category'] = 'original'
    
    return songs


def get_beli_score(position: int, total: int) -> float:
    """Calculate Beli-style score (0-10) based on position"""
    if total <= 1:
        return 10.0
    return round(10 - ((position - 1) / (total - 1)) * 10, 1)


def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'user_name': '',
        'pool_size': 'Top 50',
        'include_covers': True,
        'setup_complete': False,
        'ranked_songs': [],
        'unranked_songs': [],
        'current_song': None,
        'comparison_left': 0,
        'comparison_right': 0,
        'ranking_in_progress': False,
        'total_comparisons': 0,
        'songs_ranked_count': 0,
        # For initial head-to-head
        'initial_matchup': True,
        'song_a': None,
        'song_b': None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def get_filtered_pool(songs: list) -> list:
    """Get song pool based on settings"""
    pool = songs.copy()
    
    if not st.session_state.include_covers:
        pool = [s for s in pool if s['category'] != 'cover']
    
    pool.sort(key=lambda x: x.get('times_played', 0), reverse=True)
    
    limit = POOL_PRESETS.get(st.session_state.pool_size)
    if limit:
        pool = pool[:limit]
    
    return pool


def setup_initial_matchup():
    """Set up the first head-to-head matchup"""
    if len(st.session_state.unranked_songs) >= 2:
        st.session_state.song_a = st.session_state.unranked_songs[0]
        st.session_state.song_b = st.session_state.unranked_songs[1]
        st.session_state.initial_matchup = True


def process_initial_choice(chose_a: bool):
    """Process the initial head-to-head choice"""
    st.session_state.total_comparisons += 1
    
    if chose_a:
        # A is better - A is #1, B is #2
        st.session_state.ranked_songs = [st.session_state.song_a, st.session_state.song_b]
    else:
        # B is better - B is #1, A is #2
        st.session_state.ranked_songs = [st.session_state.song_b, st.session_state.song_a]
    
    # Remove both from unranked
    st.session_state.unranked_songs.remove(st.session_state.song_a)
    st.session_state.unranked_songs.remove(st.session_state.song_b)
    
    # Clear initial matchup state
    st.session_state.initial_matchup = False
    st.session_state.song_a = None
    st.session_state.song_b = None
    st.session_state.songs_ranked_count = 2
    
    # Auto-start next song if available
    if st.session_state.unranked_songs:
        start_ranking_song(st.session_state.unranked_songs[0])


def start_ranking_song(song: dict):
    """Start ranking a new song using binary search"""
    st.session_state.current_song = song
    st.session_state.ranking_in_progress = True
    st.session_state.comparison_left = 0
    st.session_state.comparison_right = len(st.session_state.ranked_songs) - 1


def skip_current_song():
    """Skip the current song and move it to the end of the unranked list"""
    if st.session_state.current_song:
        # Move current song to end of unranked list
        st.session_state.unranked_songs.remove(st.session_state.current_song)
        st.session_state.unranked_songs.append(st.session_state.current_song)
        st.session_state.current_song = None
        st.session_state.ranking_in_progress = False

        # Auto-start next song if available
        if st.session_state.unranked_songs:
            start_ranking_song(st.session_state.unranked_songs[0])


def process_swipe(is_better: bool):
    """Process swipe - True if current song is better than comparison"""
    left = st.session_state.comparison_left
    right = st.session_state.comparison_right
    mid = (left + right) // 2

    st.session_state.total_comparisons += 1

    if is_better:
        # Current song is better, search upper half (lower indices)
        st.session_state.comparison_right = mid - 1
    else:
        # Comparison song is better, search lower half
        st.session_state.comparison_left = mid + 1

    # Check if search is complete
    if st.session_state.comparison_left > st.session_state.comparison_right:
        insert_pos = st.session_state.comparison_left
        st.session_state.ranked_songs.insert(insert_pos, st.session_state.current_song)
        st.session_state.unranked_songs.remove(st.session_state.current_song)
        st.session_state.current_song = None
        st.session_state.ranking_in_progress = False
        st.session_state.songs_ranked_count += 1

        # Auto-start next song if available
        if st.session_state.unranked_songs:
            start_ranking_song(st.session_state.unranked_songs[0])


def get_comparison_song() -> dict:
    """Get current song to compare against"""
    mid = (st.session_state.comparison_left + st.session_state.comparison_right) // 2
    return st.session_state.ranked_songs[mid]


def encode_rankings(name: str, rankings: list) -> str:
    """Encode rankings to shareable string"""
    data = {
        'n': name,
        'r': [s['name'] for s in rankings]
    }
    json_str = json.dumps(data, separators=(',', ':'))
    return base64.urlsafe_b64encode(json_str.encode()).decode()


def decode_rankings(code: str, all_songs: list) -> tuple:
    """Decode rankings from shared code"""
    try:
        json_str = base64.urlsafe_b64decode(code.encode()).decode()
        data = json.loads(json_str)
        name = data['n']
        song_names = data['r']
        
        # Rebuild song objects
        song_dict = {s['name']: s for s in all_songs}
        rankings = [song_dict[n] for n in song_names if n in song_dict]
        
        return name, rankings
    except:
        return None, None


def main():
    init_session_state()
    all_songs = load_songs()
    
    # Header
    st.markdown('<h1 class="main-title">🪿 Goose Ranker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Rank your favorite Goose songs</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check for shared rankings in URL
    params = st.query_params
    if 'r' in params and not st.session_state.setup_complete:
        shared_name, shared_rankings = decode_rankings(params['r'], all_songs)
        if shared_rankings:
            st.markdown(f'### 👀 Viewing {shared_name}\'s Rankings')
            st.markdown(f"*{len(shared_rankings)} songs ranked*")
            st.markdown("---")
            
            for i, song in enumerate(shared_rankings, 1):
                score = get_beli_score(i, len(shared_rankings))
                cat_class = f"category-{song['category']}"
                cat_label = "Original" if song['category'] == 'original' else "Cover"
                
                col1, col2, col3 = st.columns([1, 7, 2])
                with col1:
                    st.markdown(f"**#{i}**")
                with col2:
                    st.markdown(f"**{song['name']}** - {song['artist']} `{cat_label}`")
                with col3:
                    st.markdown(f'<span class="score-badge">{score}</span>', unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("🎵 Create My Own Rankings", type="primary", use_container_width=True):
                st.query_params.clear()
                st.rerun()
            return
    
    # Setup screen
    if not st.session_state.setup_complete:
        st.markdown("### 👋 Let's Get Started")
        
        # User name
        name = st.text_input("Your Name", placeholder="Enter your name...", key="name_input")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 How many songs?")
            pool_size = st.radio(
                "Select pool size",
                list(POOL_PRESETS.keys()),
                index=1,
                key="pool_radio",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("#### 🎤 Include covers?")
            include_covers = st.radio(
                "Include covers",
                ["Yes", "No"],
                index=0,
                key="covers_radio",
                label_visibility="collapsed"
            )
        
        # Preview
        st.markdown("---")
        preview_pool = all_songs.copy()
        if include_covers == "No":
            preview_pool = [s for s in preview_pool if s['category'] != 'cover']
        preview_pool.sort(key=lambda x: x.get('times_played', 0), reverse=True)
        limit = POOL_PRESETS.get(pool_size)
        if limit:
            preview_pool = preview_pool[:limit]
        
        originals = sum(1 for s in preview_pool if s['category'] == 'original')
        covers = sum(1 for s in preview_pool if s['category'] == 'cover')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Songs", len(preview_pool))
        with col2:
            st.metric("Originals", originals)
        with col3:
            st.metric("Covers", covers)
        
        st.markdown("**Top songs in your pool:**")
        top_preview = ", ".join([s['name'] for s in preview_pool[:8]])
        st.markdown(f"*{top_preview}...*")
        
        st.markdown("---")
        
        # Start button
        if st.button("🚀 Start Ranking!", type="primary", use_container_width=True, disabled=not name):
            st.session_state.user_name = name
            st.session_state.pool_size = pool_size
            st.session_state.include_covers = (include_covers == "Yes")
            st.session_state.setup_complete = True

            # Initialize pool - keep sorted by play frequency (most played first)
            pool = get_filtered_pool(all_songs)
            # Pool is already sorted by times_played in descending order from get_filtered_pool
            st.session_state.unranked_songs = pool
            st.session_state.ranked_songs = []

            # Set up initial head-to-head
            setup_initial_matchup()

            st.rerun()
        
        if not name:
            st.caption("*Enter your name to continue*")
        
        return
    
    # Main app - tabs
    tab1, tab2, tab3 = st.tabs(["🎵 Rank Songs", "📊 My Rankings", "ℹ️ About"])
    
    with tab1:
        st.markdown(f'<span class="user-badge">👤 {st.session_state.user_name}</span>', unsafe_allow_html=True)
        
        # Progress
        total_pool = len(st.session_state.ranked_songs) + len(st.session_state.unranked_songs)
        ranked_count = len(st.session_state.ranked_songs)
        
        if total_pool > 0:
            progress = ranked_count / total_pool
            st.progress(progress)
            st.markdown(f'<p class="progress-text">Ranked {ranked_count} of {total_pool} songs • {st.session_state.total_comparisons} comparisons made</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # INITIAL HEAD-TO-HEAD MATCHUP
        if st.session_state.initial_matchup and st.session_state.song_a and st.session_state.song_b:
            song_a = st.session_state.song_a
            song_b = st.session_state.song_b
            
            st.markdown("### 🎯 Which song do you prefer?")
            st.markdown("*Pick your favorite to start building your rankings*")
            
            st.markdown("---")
            
            # Two cards side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="tinder-card" style="min-height: 200px;">
                    <div class="song-title" style="font-size: 1.5rem;">{song_a['name']}</div>
                    <div class="song-artist">{song_a['artist']}</div>
                    <div class="song-plays">Played {song_a.get('times_played', '?')}x</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"⬅️ {song_a['name']}", use_container_width=True, key="pick_a"):
                    process_initial_choice(chose_a=True)
                    st.rerun()
            
            with col2:
                st.markdown(f"""
                <div class="tinder-card" style="min-height: 200px;">
                    <div class="song-title" style="font-size: 1.5rem;">{song_b['name']}</div>
                    <div class="song-artist">{song_b['artist']}</div>
                    <div class="song-plays">Played {song_b.get('times_played', '?')}x</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"{song_b['name']} ➡️", use_container_width=True, key="pick_b"):
                    process_initial_choice(chose_a=False)
                    st.rerun()
        
        # BINARY SEARCH COMPARISONS
        elif st.session_state.ranking_in_progress and st.session_state.current_song:
            current = st.session_state.current_song
            comparison = get_comparison_song()

            st.markdown("### 🎯 Which song do you prefer?")

            st.markdown("---")

            # Two cards side by side
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                <div class="tinder-card" style="min-height: 200px;">
                    <div class="song-title" style="font-size: 1.5rem;">{comparison['name']}</div>
                    <div class="song-artist">{comparison['artist']}</div>
                    <div class="song-plays">Played {comparison.get('times_played', '?')}x</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"⬅️ {comparison['name']}", use_container_width=True, key="swipe_left"):
                    process_swipe(is_better=False)
                    st.rerun()

            with col2:
                st.markdown(f"""
                <div class="tinder-card" style="min-height: 200px;">
                    <div class="song-title" style="font-size: 1.5rem;">{current['name']}</div>
                    <div class="song-artist">{current['artist']}</div>
                    <div class="song-plays">Played {current.get('times_played', '?')}x</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"{current['name']} ➡️", use_container_width=True, key="swipe_right"):
                    process_swipe(is_better=True)
                    st.rerun()

            # Skip button
            st.markdown("---")
            if st.button("⏭️ Skip (too hard to choose)", type="secondary", use_container_width=True, key="skip_song"):
                skip_current_song()
                st.rerun()
        
        elif st.session_state.unranked_songs:
            # Shouldn't normally get here, but handle edge case
            next_song = st.session_state.unranked_songs[0]
            start_ranking_song(next_song)
            st.rerun()
        
        else:
            # All done!
            st.markdown("### 🎉 All Done!")
            st.markdown(f"You've ranked all {len(st.session_state.ranked_songs)} songs!")
            st.markdown("Check out the **My Rankings** tab to see your results and share!")
        
        # Search section (always visible when not done)
        if st.session_state.unranked_songs and not st.session_state.initial_matchup:
            st.markdown("---")
            st.markdown("#### 🔍 Search for a specific song to rank next")
            search = st.text_input("Search", placeholder="Search by name...", label_visibility="collapsed")
            
            if search:
                matches = [s for s in st.session_state.unranked_songs 
                          if search.lower() in s['name'].lower()][:5]
                
                for song in matches:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{song['name']}** - {song['artist']}")
                    with col2:
                        if st.button("Rank", key=f"search_{song['name']}"):
                            # Move this song to front of queue
                            st.session_state.unranked_songs.remove(song)
                            st.session_state.unranked_songs.insert(0, song)
                            start_ranking_song(song)
                            st.rerun()
    
    with tab2:
        st.markdown("### Your Rankings")
        st.markdown(f'<span class="user-badge">👤 {st.session_state.user_name}</span>', unsafe_allow_html=True)
        
        if not st.session_state.ranked_songs:
            st.info("🎵 Start ranking songs to see your list here!")
        else:
            # Stats
            col1, col2, col3 = st.columns(3)
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
                st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{st.session_state.total_comparisons}</div>
                    <div class="stat-label">Comparisons</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Share section
            st.markdown("#### 📤 Share Your Rankings")
            share_code = encode_rankings(st.session_state.user_name, st.session_state.ranked_songs)
            
            st.markdown("Copy this code and add to URL to share:")
            st.code(f"?r={share_code}", language=None)
            st.caption("*Add this to the end of your app URL*")
            
            st.markdown("---")
            
            # Rankings list
            for i, song in enumerate(st.session_state.ranked_songs, 1):
                score = get_beli_score(i, len(st.session_state.ranked_songs))
                cat_label = "Original" if song['category'] == 'original' else "Cover"
                cat_class = f"category-{song['category']}"
                
                col1, col2, col3 = st.columns([1, 7, 2])
                
                with col1:
                    st.markdown(f"<div style='font-size: 1.3rem; font-weight: 700; color: #666;'>#{i}</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    **{song['name']}**  
                    <span style="color: #00CED1; font-size: 0.85rem;">{song['artist']}</span>
                    <span class="category-pill {cat_class}">{cat_label}</span>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f'<span class="score-badge">{score}</span>', unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 0.3rem 0; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Reset option
            if st.button("🔄 Start Over", type="secondary"):
                st.session_state.setup_complete = False
                st.session_state.ranked_songs = []
                st.session_state.unranked_songs = []
                st.session_state.current_song = None
                st.session_state.ranking_in_progress = False
                st.session_state.total_comparisons = 0
                st.session_state.initial_matchup = True
                st.session_state.song_a = None
                st.session_state.song_b = None
                st.session_state.songs_ranked_count = 0
                st.rerun()
    
    with tab3:
        st.markdown("""
        ### How It Works
        
        **Goose Ranker** uses **Beli-style pairwise comparisons** with a Tinder-style interface:
        
        1. **See a new song** you need to rank
        2. **Compare it** against songs you've already ranked
        3. **Swipe right** if the new song is better, **left** if not
        4. Through ~log₂(n) comparisons, it finds the exact position
        5. Your rankings map to a **0-10 score** (top song = 10.0)
        
        ---
        
        ### Why This Works
        
        - **Relative > Absolute** - "Is A better than B?" is easier than "Rate A from 1-10"
        - **Consistent** - No more second-guessing your scores
        - **Fast** - Binary search means ranking 50 songs takes ~6 comparisons each
        - **Personal** - Your list, your taste
        
        ---
        
        ### The Database
        
        **250+ songs** from the Goose catalog:
        - 🎸 **Originals** - Goose songs + Vasudo, Great Blue, Swimmer, Orebolo
        - 🎤 **Covers** - Grateful Dead, Talking Heads, Prince, and more
        
        Sorted by **live play frequency** from [El Goose.net](https://elgoose.net)
        
        ---
        
        *Built for the Goose community • 🪿 Honk Honk*
        """)


if __name__ == "__main__":
    main()
