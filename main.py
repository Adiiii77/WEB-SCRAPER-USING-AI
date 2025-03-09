import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama
import time

# Page configuration
st.set_page_config(
    page_title="Elegant Web Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme state management
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"  # Default to dark mode based on the image


# Theme toggle function
def toggle_theme():
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"


# Custom CSS with dynamic theming - Completely overhauled
def get_theme_css():
    if st.session_state.theme == "dark":
        return """
        <style>
            /* Main background and text */
            body {
                color: #f0f0f0;
                background-color: #1e1e1e;
            }

            .stApp {
                background-color: #1e1e1e;
            }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: #252525;
                border-right: 1px solid #333;
            }

            section[data-testid="stSidebar"] .stMarkdown {
                color: #e0e0e0;
            }

            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
            }

            /* Buttons */
            .stButton button {
                background-color: #4b6fff;
                color: white;
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                border: none;
                transition: all 0.3s;
            }

            .stButton button:hover {
                background-color: #3a5cff;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                transform: translateY(-2px);
            }

            /* Text inputs */
            .stTextInput input {
                border-radius: 5px;
                border: 1px solid #444;
                padding: 0.5rem;
                background-color: #2d2d2d;
                color: #f0f0f0;
            }

            /* Text areas */
            .stTextArea textarea {
                background-color: #2d2d2d;
                color: #f0f0f0;
                border: 1px solid #444;
                border-radius: 5px;
            }

            /* Select boxes */
            .stSelectbox, div[data-baseweb="select"] {
                background-color: #2d2d2d;
            }

            div[data-baseweb="select"] > div {
                background-color: #2d2d2d;
                border: 1px solid #444;
                color: #f0f0f0;
            }

            div[data-baseweb="popover"] > div {
                background-color: #2d2d2d;
                color: #f0f0f0;
            }

            /* Tabs */
            .stTabs button {
                color: #f0f0f0;
            }

            .stTabs button[aria-selected="true"] {
                color: #4b6fff;
                border-bottom-color: #4b6fff;
                font-weight: bold;
            }

            .stTabs button:hover {
                color: #ffffff;
            }

            /* Status messages */
            .stAlert {
                background-color: #2d2d2d;
                color: #f0f0f0;
            }

            /* Custom classes */
            .title-section {
                padding: 2rem 0;
                margin-bottom: 2rem;
            }

            .content-section {
                background-color: #2d2d2d;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                margin-bottom: 1rem;
            }

            .results-container {
                background-color: #2a3a5a;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #4b6fff;
                margin-top: 1rem;
            }

            .footer {
                text-align: center;
                margin-top: 3rem;
                color: #aaaaaa;
                font-size: 0.8rem;
            }

            .history-item {
                background-color: #3d3d3d;
                padding: 1rem;
                border-radius: 5px;
                margin-bottom: 0.5rem;
                cursor: pointer;
            }

            .history-item:hover {
                background-color: #4d4d4d;
            }

            .tab-content {
                padding-top: 1rem;
            }

            /* Expanders */
            .stExpander {
                border-radius: 8px;
                border: 1px solid #444;
                background-color: #2d2d2d;
            }

            /* Progress Bars */
            .stProgress > div > div {
                background-color: #4b6fff;
            }

            /* Horizontal Rule */
            hr {
                border-color: #444;
            }

            /* Status elements */
            .element-container div[data-testid="stDecoration"] {
                background-color: #2d2d2d !important;
            }

            /* Alerts */
            [data-testid="stInfoBox"] {
                background-color: rgba(75, 111, 255, 0.1) !important;
                border-left-color: #4b6fff !important;
                color: #f0f0f0 !important; 
            }

            [data-testid="stSuccessBox"] {
                background-color: rgba(40, 167, 69, 0.1) !important;
                border-left-color: #28a745 !important;
                color: #f0f0f0 !important;
            }

            [data-testid="stWarningBox"] {
                background-color: rgba(255, 193, 7, 0.1) !important;
                border-left-color: #ffc107 !important;
                color: #f0f0f0 !important;
            }

            [data-testid="stErrorBox"] {
                background-color: rgba(220, 53, 69, 0.1) !important;
                border-left-color: #dc3545 !important;
                color: #f0f0f0 !important;
            }

            /* Subheader */
            .subheader {
                color: #aaaaaa;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }
        </style>
        """
    else:
        return """
        <style>
            /* Main background and text */
            body {
                color: #2c3e50;
                background-color: #f8f9fa;
            }

            .stApp {
                background-color: #f8f9fa;
            }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: #f0f2f5;
                border-right: 1px solid #eaeaea;
            }

            section[data-testid="stSidebar"] .stMarkdown {
                color: #2c3e50;
            }

            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #2c3e50 !important;
            }

            /* Buttons */
            .stButton button {
                background-color: #4b6fff;
                color: white;
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                border: none;
                transition: all 0.3s;
            }

            .stButton button:hover {
                background-color: #3a5cff;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transform: translateY(-2px);
            }

            /* Text inputs */
            .stTextInput input {
                border-radius: 5px;
                border: 1px solid #e0e0e0;
                padding: 0.5rem;
                background-color: #ffffff;
                color: #2c3e50;
            }

            /* Text areas */
            .stTextArea textarea {
                background-color: #ffffff;
                color: #2c3e50;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
            }
            
            /* Add placeholder styling for light mode */
            .stTextInput input::placeholder,
                .stTextArea textarea::placeholder {
                color: #7f8c8d;
                opacity: 0.7;
            }

            /* Select boxes */
            .stSelectbox, div[data-baseweb="select"] {
                background-color: #ffffff;
            }

            div[data-baseweb="select"] > div {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                color: #2c3e50;
            }

            div[data-baseweb="popover"] > div {
                background-color: #ffffff;
                color: #2c3e50;
            }

            /* Tabs */
            .stTabs button {
                color: #7f8c8d;
            }

            .stTabs button[aria-selected="true"] {
                color: #4b6fff;
                border-bottom-color: #4b6fff;
                font-weight: bold;
            }

            .stTabs button:hover {
                color: #2c3e50;
            }

            /* Status messages */
            .stAlert {
                background-color: #ffffff;
                color: #2c3e50;
            }

            /* Custom classes */
            .title-section {
                padding: 2rem 0;
                margin-bottom: 2rem;
            }

            .content-section {
                background-color: #ffffff;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                margin-bottom: 1rem;
            }

            .results-container {
                background-color: #f1f8ff;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #4b6fff;
                margin-top: 1rem;
            }

            .footer {
                text-align: center;
                margin-top: 3rem;
                color: ##2c3e50;
                font-size: 0.8rem;
            }

            .history-item {
                background-color: #f8f9fa;
                padding: 1rem;
                border-radius: 5px;
                margin-bottom: 0.5rem;
                cursor: pointer;
                border: 1px solid #e0e0e0;
            }

            .history-item:hover {
                background-color: #f1f1f1;
            }

            .tab-content {
                padding-top: 1rem;
            }

            /* Expanders */
            .stExpander {
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
            }

            /* Progress Bars */
            .stProgress > div > div {
                background-color: #4b6fff;
            }

            /* Horizontal Rule */
            hr {
                border-color: #e0e0e0;
            }

            /* Alerts */
            [data-testid="stInfoBox"] {
                background-color: rgba(75, 111, 255, 0.1) !important;
                border-left-color: #4b6fff !important;
                color: #2c3e50 !important;  /* Make sure this is set to a dark color */
            }

            [data-testid="stSuccessBox"] {
                background-color: rgba(40, 167, 69, 0.1) !important;
                border-left-color: #28a745 !important;
                color: #2c3e50 !important;
            }

            [data-testid="stWarningBox"] {
                background-color: rgba(255, 193, 7, 0.1) !important;
                border-left-color: #ffc107 !important;
                color: #2c3e50 !important;
            }

            [data-testid="stErrorBox"] {
                background-color: rgba(220, 53, 69, 0.1) !important;
                border-left-color: #dc3545 !important;
                color: #2c3e50 !important;
            }

            /* Subheader */
            .subheader {
                color: #7f8c8d;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }
        </style>
        """


# Apply the theme CSS
st.markdown(get_theme_css(), unsafe_allow_html=True)

# Initialize session state for search history
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Initialize session state for saved results
if 'saved_results' not in st.session_state:
    st.session_state.saved_results = []

# Sidebar
with st.sidebar:
    st.markdown("## About")
    st.markdown(
        "This AI-powered web scraper extracts content from websites and allows you to parse specific information using natural language instructions.")

    st.markdown("## How to use")
    st.markdown("1. Enter a website URL")
    st.markdown("2. Click 'Scrape Website'")
    st.markdown("3. Describe what information you want to extract")
    st.markdown("4. Click 'Parse Content'")

    st.markdown("## Settings")
    theme_label = "Switch to Light Mode" if st.session_state.theme == "dark" else "Switch to Dark Mode"
    if st.button(theme_label):
        toggle_theme()
        st.rerun()

    # Add a section to view search history
    if len(st.session_state.search_history) > 0:
        st.markdown("## Recent Searches")
        for idx, item in enumerate(st.session_state.search_history[-5:]):  # Show only the last 5 searches
            if st.button(f"{item['url']} - {item['description'][:20]}...", key=f"history_{idx}"):
                # Load this history item
                st.session_state.loaded_url = item['url']
                st.session_state.loaded_description = item['description']
                st.rerun()

# Main content - Title section without extra containers
st.markdown('<div class="title-section">', unsafe_allow_html=True)
st.markdown('<h1>AI Web Scraper</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Extract and analyze web content with the power of AI</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Create tabs for different functions
tab1, tab2, tab3 = st.tabs(["Web Scraper", "Saved Results", "Batch Processing"])

# Tab 1: Web Scraper (Main Functionality)
with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)

    # Content section
    # st.markdown('<div class="content-section">', unsafe_allow_html=True)

    # URL input with columns for better layout
    col1, col2 = st.columns([3, 1])
    with col1:
        # Use loaded URL from history if available
        initial_url = st.session_state.get('loaded_url', '')
        url = st.text_input("Enter a Website URL:", value=initial_url, placeholder="https://example.com")
    with col2:
        scrape_button = st.button("Scrape Website", use_container_width=True)

    # Scraping process with progress indicator
    if scrape_button:
        if url:
            with st.spinner("Scraping the website..."):
                # Progress bar for visual feedback
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)

                # Actual scraping
                result = scrape_website(url)
                body_content = extract_body_content(result)
                cleaned_content = clean_body_content(body_content)
                st.session_state.dom_content = cleaned_content

                # Add to search history
                if 'url' not in st.session_state or st.session_state.url != url:
                    st.session_state.url = url

                # Success message
                st.success("Website scraped successfully!")

                # Display content in a styled expander
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
        else:
            st.error("Please enter a valid URL")

    st.markdown('<hr>', unsafe_allow_html=True)

    # Parsing section
    if "dom_content" in st.session_state:
        st.subheader("Extract Information")

        # Instruction with better styling
        st.info("Describe what information you want to extract from the website")

        # Use loaded description from history if available
        initial_description = st.session_state.get('loaded_description', '')
        parse_description = st.text_area(
            "Extraction Instructions:",
            value=initial_description,
            placeholder="Example: Extract all product prices and names",
            height=100
        )

        # Columns for better button placement
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            parse_button = st.button("Parse Content", use_container_width=True)

        if parse_button:
            if parse_description:
                # Add to search history
                history_item = {
                    'url': st.session_state.url,
                    'description': parse_description,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.search_history.append(history_item)

                # Clear loaded items
                if 'loaded_url' in st.session_state:
                    del st.session_state.loaded_url
                if 'loaded_description' in st.session_state:
                    del st.session_state.loaded_description

                with st.spinner("Parsing content with AI..."):
                    # Progress bar for visual feedback
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)

                    # Actual parsing
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    result = parse_with_ollama(dom_chunks, parse_description)

                    # Save the result
                    result_item = {
                        'url': st.session_state.url,
                        'description': parse_description,
                        'result': result,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.current_result = result_item

                    # Display results in a nice container
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    st.subheader("Extracted Results")
                    st.write(result)

                    # Add save button
                    if st.button("Save this result"):
                        st.session_state.saved_results.append(result_item)
                        st.success("Result saved successfully!")

                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe what you want to extract")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Saved Results
with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    # st.markdown('<div class="content-section">', unsafe_allow_html=True)

    st.subheader("Saved Extraction Results")

    if len(st.session_state.saved_results) > 0:
        # Create a dropdown to select saved results
        result_options = [f"{item['url']} - {item['description'][:20]}... ({item['timestamp']})"
                          for item in st.session_state.saved_results]
        selected_result = st.selectbox("Select a saved result to view", result_options)

        # Get the index of the selected result
        selected_index = result_options.index(selected_result)

        # Display the selected result
        result = st.session_state.saved_results[selected_index]

        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown(f"**URL:** {result['url']}")
        st.markdown(f"**Query:** {result['description']}")
        st.markdown(f"**Timestamp:** {result['timestamp']}")
        st.markdown("**Result:**")
        st.write(result['result'])

        # Add delete button
        if st.button("Delete this result"):
            st.session_state.saved_results.pop(selected_index)
            st.success("Result deleted successfully!")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No saved results yet. Use the Web Scraper tab to extract and save information.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Batch Processing
with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    # st.markdown('<div class="content-section">', unsafe_allow_html=True)

    st.subheader("Batch Process Multiple URLs")
    st.info("Enter multiple URLs (one per line) and a single extraction query to process them all at once")

    # Text area for multiple URLs
    batch_urls = st.text_area(
        "Enter URLs (one per line):",
        placeholder="https://example1.com\nhttps://example2.com",
        height=100
    )

    # Query for all URLs
    batch_query = st.text_area(
        "Extraction Query for All URLs:",
        placeholder="Extract all product prices and names",
        height=100
    )

    # Process button
    if st.button("Process Batch"):
        if batch_urls and batch_query:
            urls = [url.strip() for url in batch_urls.split('\n') if url.strip()]

            if len(urls) > 0:
                # Initialize results container
                batch_results = []

                # Process each URL
                progress_text = st.empty()
                progress_bar = st.progress(0)

                for i, url in enumerate(urls):
                    progress_text.text(f"Processing {url}...")
                    progress_value = int((i / len(urls)) * 100)
                    progress_bar.progress(progress_value)

                    try:
                        # Scrape the website
                        result = scrape_website(url)
                        body_content = extract_body_content(result)
                        cleaned_content = clean_body_content(body_content)

                        # Parse the content
                        dom_chunks = split_dom_content(cleaned_content)
                        parsed_result = parse_with_ollama(dom_chunks, batch_query)

                        # Add to results
                        batch_results.append({
                            'url': url,
                            'result': parsed_result,
                            'status': 'success'
                        })
                    except Exception as e:
                        # Handle errors
                        batch_results.append({
                            'url': url,
                            'result': f"Error: {str(e)}",
                            'status': 'error'
                        })

                # Complete the progress bar
                progress_bar.progress(100)
                progress_text.text("Processing complete!")

                # Display results
                st.subheader("Batch Processing Results")

                for result in batch_results:
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    st.markdown(f"**URL:** {result['url']}")
                    st.markdown(f"**Status:** {result['status']}")
                    st.markdown("**Result:**")
                    st.write(result['result'])
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                # Add option to save all results
                if st.button("Save All Batch Results"):
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    for result in batch_results:
                        if result['status'] == 'success':
                            result_item = {
                                'url': result['url'],
                                'description': batch_query,
                                'result': result['result'],
                                'timestamp': timestamp
                            }
                            st.session_state.saved_results.append(result_item)

                    st.success(
                        f"Saved {len([r for r in batch_results if r['status'] == 'success'])} results successfully!")
            else:
                st.error("No valid URLs provided")
        else:
            st.warning("Please enter both URLs and an extraction query")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown('Elegant Web Scraper • Powered by AI', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)