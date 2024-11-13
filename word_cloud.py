from wordcloud import WordCloud
import matplotlib.pyplot as plt

target_color = [0, 214, 255]
min_alpha_value = 0.5

word_frequencies = {}
alpha_colors = {}

# Define words with their frequencies
old_word_frequencies = {
    "Python": 100,
    "data": 80,
    "visualization": 20,
    "example": 5,
    "library": 50,
}


def read_tab_separated_file(file_path):
    result_dict = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        ignore_first_line = True
        for line in file:
            if ignore_first_line:
                ignore_first_line = False
                continue
            # Strip whitespace and split the line by tabs
            parts = line.strip().split('\t')
            if len(parts) == 2:  # Ensure there are exactly two columns
                key = parts[0]
                value = float(parts[1])
                result_dict[key] = value

    return result_dict


def remap(value, from_min, from_max, to_min, to_max, cap=False):
    from_range = from_max - from_min
    to_range = to_max - to_min
    return (value - from_min) * to_range / from_range + to_min


def normalize_data(in_dict):
    min_val = min(in_dict.values())
    max_val = max(in_dict.values())

    return {x: remap(in_dict[x], min_val, max_val, min_alpha_value, 1.0) for x in in_dict.keys()}


# Custom color function based on word frequency
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    global alpha_colors
    alpha = alpha_colors[word]
    color = [int(c * alpha) for c in target_color]
    return f"rgb({color[0]}, {color[1]},{color[2]})"

def generate_wordcloud(input_file_path, output_image_path):
    global word_frequencies, alpha_colors
    word_frequencies = read_tab_separated_file(input_file_path)
    alpha_colors = normalize_data(word_frequencies)

    font_path = r"data\AkzidenzGroteskBQ-MdCnd.ttf"

    # Generate the word cloud with the custom color function
    gen_wordcloud = WordCloud(
        width=720, height=280, font_path=font_path,
        background_color="rgba(255, 255, 255, 0)", mode="RGBA",
        color_func=color_func).generate_from_frequencies(word_frequencies)

    # Save and display the word cloud
    gen_wordcloud.to_file(output_image_path)
    return gen_wordcloud

if __name__ == "__main__":
    gen_wordcloud = generate_wordcloud(r"data\hotwords.tsv", r"data\colored_wordcloud4.png")
    plt.imshow(gen_wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
