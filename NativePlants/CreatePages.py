import pandas as pd
import os

# Load the TSV file
tsv_path = "PlantContent.tsv"
df = pd.read_csv(tsv_path, sep='\t')

# Extract aligned lists
plants = df['Plant'].tolist()
scientific_names = df['Scientific Name'].tolist()
native_names = df['Native Name'].tolist()
descriptions = df['Description'].tolist()
traditional_uses = df['Traditional Native Uses'].tolist()
image_links = df['Image'].tolist()
icon_types = ["Medicine", "Tech", "Basketry", "Food", "Berries"]

icon_to_color = {
    "Medicine":  "#4D8798",   # Agave
    "Tech":      "#A32035",   # blue
    "Basketry":  "#D15C3B",   # Terracotta
    "Food":      "#7F5E9C",   # Wisteria
    "Berries":   "#B32551"    # Rose
}

output_dir = "./plant-pages"
os.makedirs(output_dir, exist_ok=True)

for i in range(len(plants)):
    plant = plants[i]
    scientific_name = scientific_names[i]

    # Truncate native name at the word "pronounced" (case-insensitive)
    native_name_full = native_names[i]
    if isinstance(native_name_full, str):
        lower_case_native = native_name_full.lower()
        if "pronounced" in lower_case_native:
            cut_index = lower_case_native.index("pronounced")
            native_name = native_name_full[:cut_index].strip()
        else:
            native_name = native_name_full.strip()
    else:
        native_name = ""

    description = descriptions[i]
    native_uses = traditional_uses[i]

    # Build icon list from Use Icons column
    icon_cell = df['Use Icons'][i] if i < len(df) else ""
    icon_html = ""
    color = None

    if isinstance(icon_cell, str):
        for icon in icon_types:
            if icon.lower() in icon_cell.lower():
                if color is None:
                    color = icon_to_color.get(icon, "#000000")
                icon_filename = f"{icon}.png"  # Assuming icon filenames like Medicine.png
                icon_html += f'<img src="https://jacklanders.site/NativePlants/plant-icons/{icon_filename}" alt="{icon} icon">\n'

    # Wrap in icon row div
    icon_row_html = f'<div class="icon-row">\n{icon_html}</div>' if icon_html else '<div class="icon-row"></div>'

    # Make a safe filename for each plant
    filename = f"{plant.replace(' ', '-').replace('/', '-').lower()}.html"
    filepath = os.path.join(output_dir, filename)

    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{plant}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
            color: #333;
        }}

        /* Top Image with Text Overlay */
        .image-header {{
            position: relative;
            width: 100%;
            height: 300px;
            overflow: hidden;
        }}

        .image-header img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .image-header .text-overlay {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            text-align: center;
        }}

        .image-header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}

        .image-header h2, .image-header h3 {{
            margin: 5px 0;
            font-weight: normal;
            font-style: italic;
        }}

        .icon-bar {{
            background-color: {color};
            padding: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .icon-row img {{
            width: 30px;
            height: 30px;
            background: rgba(255,255,255, 1);
            border-radius: 30%;
            padding: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }}

        /* Main Content Sections */
        .content-section {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 1000px;
            margin: 30px auto;
            padding: 10px;
        }}

        .description, .native-uses {{
            flex: 1 1 300px;
            max-width: 45%;
            margin: 10px;
            padding: 15px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        /* Make headers centered for both sections */
        .description h4, .native-uses h4 {{
            margin-top: 0;
            color: {color};
            text-align: center;
        }}

        /* Icon Row under Native Uses Header */
        .icon-row {{
            display: flex;
            justify-content: center;
            margin-left: -530px;
            gap: 10px;
            padding-left: 30px;
        }}
        
        .speaker-button {{
            font-size: 24px;
            background: none;
            border: none;
            cursor: pointer;
        }}
        /* Responsive: Stack on small screens */
        @media (max-width: 768px) {{
            .content-section {{
                flex-direction: column;
                align-items: center;
            }}
            .description, .native-uses {{
                max-width: 90%;
            }}
        }}
    </style>
</head>
<body>
    <audio id="myAudio" src="plant-pronunciations/Example.mp3"></audio>

    <script>
      function playAudio() {{
        const audio = document.getElementById("myAudio");
        audio.currentTime = 0; // rewind to start
        audio.play();
      }}
    </script>
    <div class="image-header">
        <img src="https://jacklanders.site/NativePlants/plant-images/{plant.replace(' ', '_').replace('/', '_')}.jpg" alt="{plant}">
        <div class="text-overlay">
            <h1>{plant}</h1>
            <h2>{scientific_name}</h2>
            <h3>{native_name}
                <button class="speaker-button" onclick="playAudio()">
                      🔊
                </button>
            </h3>
        </div>
    </div>
    
    <div class="icon-bar">
        {icon_row_html}
    </div>

    <div class="content-section">
        <div class="description">
            <h4>Description</h4>
            <p>{description}</p>
        </div>

        <div class="native-uses">
            <div class="native-uses-header">
                <h4>Traditional Native Uses</h4>
            </div>
            <p>{native_uses}</p>
        </div>
    </div>

</body>
</html>"""

    # Write the HTML file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Generated {filename}")
