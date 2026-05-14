accessPost/
│
├── data/
│   ├── lockers_warszawa_500.json       # Raw dataset downloaded from InPost API
│   └── lockers_warszawa_scored.json    # Enriched dataset with AI accessibility scores
│
├── src/
|   |
│   ├── fetch/
|   |   └── request_data.py             # Data ingestion script (extracts and filters target locations)
|   |
|   |
│   ├── config.py                       # Global settings and environment variables
│   ├── data_handler.py                 # File I/O operations (Extract & Load)
│   ├── vision_service.py               # Google Cloud Vertex AI integration
│   ├── prompts.py                      # Prompt engineering and AI instructions
│   ├── auditor.py                      # Core business logic (Transform)
│   ├── main.py                         # ETL pipeline entry point
│   │
│   └── frontend/
|       ├── data_loader.py              # Loads and formats the JSON into Pandas to make it map-ready
|       ├── map_view.py                 # Handles only the PyDeck map logic
|       ├── ui.py                       # Handles headers, sidebars and tables
│       └── app.py                      # Main orchestrator of interactive web map application (Streamlit)
│
├── .env.example                        # Template for required environment variables
├── .gitignore                          # Ignored system and secret files
├── requirements.txt                    # Pinned Python dependencies
└── README.md                           # Project documentation



Frontend & Visualization:
Streamlit: I chose Streamlit as my frontend framework because it allows rapid development of interactive, data-driven web applications using pure Python. It completely eliminates the need to write boilerplate HTML/CSS/JS, allowing me to focus entirely on the data and the logic.
Pandas: Used for efficient data manipulation and filtering before sending the dataset to the map.
PyDeck: Used to render the interactive map. While Streamlit has a built-in map, PyDeck allows for advanced features like custom color-coding of the locker pins based on their AI accessibility scores.

Streamlit is pure Component-Based Architecture utility demo.   python -m streamlit run src/frontend/app.py