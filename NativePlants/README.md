## What CreatePages.py Does

This script is a simple static‑site generator that turns your tabular plant data into individual, styled HTML pages. Here’s a high‑level overview:

### 1. Load the Data
- Reads a TSV file (`PlantContent.tsv`) into a Pandas DataFrame.  
- Extracts columns into Python lists:  
  - `Plant`  
  - `Scientific Name`  
  - `Native Name`  
  - `Description`  
  - `Traditional Native Uses`  
  - `Image`  
  - `Use Icons`

### 2. Pre‑process Fields
- For each **Native Name**, if it contains the word “pronounced” (case‑insensitive), truncate everything from “pronounced” onward.  
- Strips extra whitespace.

### 3. Determine Icon Styling
- Defines icon categories: `Medicine`, `Tech`, `Basketry`, `Food`, `Berries`.  
- Maps each category to a hex color.  
- Scans the “Use Icons” cell for each plant:  
  - Finds matching categories.  
  - Picks the first matching category’s color for the background bar.  
  - Builds a small HTML `<img>` snippet for each relevant icon.

### 4. Generate HTML Pages
- Creates a `./plant-pages` directory.  
- For each plant:  
  1. Converts the plant name into a safe filename (e.g., `yarrow.html`).  
  2. Fills in an HTML template that includes:  
     - A “hero” image with overlayed common name, scientific name, and a pronunciation button (`🔊`).  
     - A colored icon bar (`.icon-bar`) showing the relevant icons.  
     - Two content cards (`.description` and `.native-uses`) with headers and text.  
     - Responsive CSS for mobile support.  
  3. Writes the file and logs `Generated <filename>` to the console.
