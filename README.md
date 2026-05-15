# ♿ accessPost

## Author

- **Name:** Hubert Gątarek
- **Email:** hubgatarek@gmail.com

## Overview

InPost has a massive database of locker locations, but looking purely at the data, it's hard to tell if a locker is actually friendly for physically impaired people in a wheelchair. **accessPost** is a modular ETL (Extract, Transform, Load) data pipeline that fetches raw locker data, passes location images URL to a Vision AI to evaluate physical surroundings, and plots the AI-enriched accessibility scores on an interactive 3D map. 

## Demo & Description

My own time constraint for this project was 3 days and I spent almost an entire day primarily finding the right problem to solve. Having analyzed the API's `.json` structure, I noticed a gap: while some lockers have an `easy_access_zone` flag set to true, proper accessibility assessment requires environmental context (curbs, paved paths, obstructions).

To solve this, I designed a **modular ETL pipeline**:
1. **Extract:** A Python ingestion script fetches 500 unique lockers from Warsaw. Because the API's text search didn't reliably filter by street and the city filter broke pagination, I brute-forced the global API. It took me a while to realise that the 150,000+ database is sorted alphabetically by locker code, thus I optimized the script to fast-forward directly to page 1,300 to find `WAW` lockers efficiently.
2. **Transform:** The URLs are sent to Google Cloud's Vertex AI (**Gemini 2.0 Flash**). Using strict prompt engineering, the AI acts as an accessibility auditor, returning a raw JSON object with a score (1-5) and a one-sentence reasoning based on curbs, surfaces, and obstructions.
3. **Load:** The enriched data is saved locally.
4. **Visualize:** A Component-Based frontend built with Streamlit and PyDeck renders the data on an interactive, color-coded dark-mode map.

### 🗂️ Project Architecture

```text
accessPost/
│
├── assets/                             # Screenshots for documentation
|   ├── api_tech.jpg
|   ├── enriching_start.jpg
|   ├── enriching_finish.jpg
|   ├── installing_requirements.jpg
|   ├── openning_localhost.jpg
|   └── map_showcase.jpg
|
├── .streamlit/
│   └── config.toml                     # Custom Streamlit theme (InPost black-yellow palette)
│
├── data/
│   ├── lockers_warszawa_500.json       # Raw dataset downloaded from InPost API
│   └── lockers_warszawa_scored.json    # Enriched dataset with AI accessibility scores
│
├── src/
│   ├── fetch/
│   │   └── request_data.py             # Data ingestion script (extracts target locations)
│   │
│   ├── config.py                       # Global settings and environment variables
│   ├── data_handler.py                 # File I/O operations (Extract & Load)
│   ├── vision_service.py               # Google Cloud Vertex AI integration
│   ├── prompt.py                      # Prompt engineering and AI instructions
│   ├── auditor.py                      # Core business logic (Transform)
│   ├── main.py                         # ETL pipeline entry point
│   │
│   └── frontend/
│       ├── data_loader.py              # Loads and formats the JSON into Pandas
│       ├── map_view.py                 # Handles only the PyDeck map logic
│       ├── ui.py                       # Handles headers, sidebars and tables
│       └── app.py                      # Streamlit orchestrator
│
├── .env.example                        # Template for required environment variables
├── .gitignore                          # Ignored system and secret files
├── requirements.txt                    # Pinned Python dependencies
└── README.md                           # Project documentation
```

## Technologies

*   **Python:** Chosen for its massive data processing ecosystem and seamless AI integrations
*   **Google Vertex AI (Gemini 2.0 Flash):** Allowed for sophisticated, multimodal nuanced analysis from images without needing to train a custom model
*   **Streamlit:** Chosen as my frontend framework because it allows rapid development of interactive, data-driven web applications using pure Python. It completely eliminates the need to write boilerplate HTML/CSS/JS
*   **Pandas:** Used for efficient data manipulation and filtering before sending it to the map
*   **PyDeck:** While Streamlit has a built-in map, PyDeck allows for advanced features like custom color-coding of the locker pins and handling map-radius pixel scaling

## How to run

### Prerequisites
*   Python 3.12+ (If not installed, download it from [python.org](https://www.python.org/downloads/) or use your system's package manager like `apt`)
*   A Google Cloud Project with the **Vertex AI API** enabled.
*   A Google Cloud Service Account JSON key.

### Build & run

This project relies on a `requirements.txt` file to guarantee 100% reproducibility. 

**1. Clone the repository and set up a virtual environment (sandbox)**
```bash
git clone <repo-url> accesPost
cd accessPost
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up Environment Variables**

*(Note: In my opinion, there is no point of rerunning the backend, fetching the data and analyse images with Vision AI, not to mention setting up Google Cloud account and generating JSON account key. On my 9 years old laptop with Windows+WSL setup it took more than 2 hours to process the data. This is heavy-lifting of the project and I have done it for you. If you just want to see the frontend, the `data/` folder already contains a pre-scored dataset of 500 Warsaw lockers which Streamlit will utilise. I highly recommend you to skip directly to point 4, step C. For the pipeline dataflow and auditing images I will embed screenshots)*

Rename `.env.example` to `.env` and provide the path to your Google Cloud Service Account JSON file. Alternatively, set it directly in your terminal:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
```
*(Ensure you update `PROJECT_ID` in `src/config.py` to match your GCP project).*

**4. Run the Pipeline & App**
*(Note: If you just want to see the frontend, the `data/` folder already contains a pre-scored dataset of 500 Warsaw lockers. You can skip directly to step C).*

```bash
# A. Fetch raw data (Extract)
python src/fetch/request_data.py

# B. Run the AI Pipeline (Transform & Load)
python src/main.py

# C. Run the Interactive Map
python -m streamlit run src/frontend/app.py
```
*(Note: Using `python -m streamlit` guarantees the system uses the library installed inside the virtual environment rather than a global installation).*

## What I would do with more time

1. **Network Optimization:** By the time of writing this README, I realized I should have revamped my fetching script to use HTTP Keep-Alive (`requests.Session()`) - in order to the API request was single for flipping the pages entire time. Establishing and tearing down TCP connections builds up network latency; fractions of seconds add up, making fetching time-consuming.
2. **AI Logic Refinement:** Having a glance at a few images' URL to assess how precise was AI with descriptions, I realized some of them are just plain product pictures, not lockers in a working environment. Vertex AI gave these a score of 1 or 2, which is misleading. They should be labeled as N/A via better prompt engineering.
3. **Analyze Smaller Cities:** I should probably take into consideration smaller sites, worse-urbanized areas, as infrastructure in richer cities is often better by default. Perhaps Warsaw shouldn't be the center of gravity for this project but it resonates the best with me, I live here and, not that far from the place I dwell, I have seen space for improvements around the locker.

## AI usage

I used Google Gemini as a pair-programmer, autoreflection and troubleshooting board. While the core idea and architectural decisions were mine, AI helped me debug, for example: specific Python pathing issues, "unpack" it's vague syntax - just switching from C/C++, Python makes me a bit sick haha, optimize the PyDeck map rendering, and help me structure the Streamlit app into a component-based architecture. Last but not least, I had hard times with API pagination and AI also helped me out the traps when InPost endpoints behaved unexpectedly.

## Anything else?

**My focus on Architecture:** 
This project was especially fun because the path I was pursuing for some time and the role I would gladly land is Data Engineer position - in the middle of creative work I realised I'm actually building ETL. A massive personal challenge for me here was maintaining a clean architecture. I've done way bigger projects with way, way worse architecture and this time I've been paying close attention to it. Last group project at 42 grew autonomously without proper structure. Being the architect, I gathered constructive feedback from that experience, this time applying Separation of Concerns (SoC), wanting to do it as beautiful as it gets. Tried my best!

**The "Agentic AI" Rabbit Hole:**
I went down a rabbit hole thinking about how to improve this. Analyzing static locker images is great, but it lacks environmental context.

I prototyped an idea for a **Vision Agent** utilizing the Google Street View API. By dropping an Agentic AI a short distance from the locker, it could take a virtual walk towards the destination, analyzing the sidewalk quality along the route. I ultimately rejected this idea because... there is a catch, or two. This could be far more sophisticated and time-complexed, integrations of Maps APIs are not free, InPost lockers' deployment rate is very high and the surroundings changes faster than Google drives their car around :O 

Nevertheless, the output of my current pipeline is straightforward and visible in Streamlit-generated tables — there is definitely some collaborative work to be done between cities and InPost to avoid excluding impaired people and I feel I proved my concept.

**Docker secound thoughts**
I was hesitant about introducing containerization in this project and finally gave it up. It would only add code overhead while the Python "venv" (virtualisation feature) is hihgly enough and satisfactory for reproducibility.

**Obstacle I couldn't identify**
Really don't wanna make this README longeish, but this funny case is worth mentioning. On first try while running visibly ready project I encountered odd quirk of viewing only 25 lockers in webapp while having 500 lockers enriched and loaded into `.json`. I was sure they are either overlapping and I just dont see them or they blend into the frontend theme colour so I took these paths and experimented. 

Turned out I fetched from API 20 sets of the same 25 locations in Warsaw - pagination really did me dirty :smiling_face_with_tear: In each of 25 location on the map, there were exactly the same 20 points being stacked on the top of each other. I needed to revamp my API request loop and make it work with pagination which didn't come naturally to me in the first place. After additional 2 hours of running the script, eventually got my results unique and visible. To debug I added the line in frontend layout, informing me how many of lockers are unique. 

There is still not 500/500 hit but I decided not to dwell on it any more as it is negligible difference of few lockers.

**Onto the end**
To summarize - I built ETL. Enriched API by AI-driven reasoning, plotted a map with score-pins and finally visualized it using Streamlit framework. I eventually had a chance to properly utilise Python and Pandas. Hopefuly this will get my foot in the InPost doorstep but if that is not going to happen, I took a good lesson of API integration and harnessing the Google Cloud models and touched important social problem. This stays with me as a standalone huge value. Thank you, InPost, for motivating me to do that.

*(Note for InPost evaluator: I highly recommend checking out the "Raw Audit Data" table in the web app to see the AI's reasoning! Also, if you want to deactivate venv in you terminal, just type "deactivate")*