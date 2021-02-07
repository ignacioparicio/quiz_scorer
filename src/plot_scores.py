import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import yaml
import pickle

scores_dict = {"Ig": 41, "Jk": 27, "ds":32, "ls": 15}

def get_palette_from_values(values, template_palette):
    normalized = (np.array(values) - min(values)) / (max(values) - min(values))
    indices = np.round(normalized * (len(values) - 1)).astype(np.int32)
    palette = sns.color_palette(template_palette, len(values))
    return np.array(palette).take(indices, axis=0)

def add_labeled_bands(bands, ax, x_offset=0.1):
    x_max = ax.get_xlim()[1]
    for label, label_params in bands.items():
        y_min, y_max = label_params["range"]
        ax.annotate(label, (x_max + x_offset, (y_min + y_max)/2), annotation_clip=False, color=label_params["color"], style='italic', fontsize="small")
        ax.fill_between(np.arange(-0.5, x_max+0.5), y_min, y_max, color=label_params["color"], alpha=0.1)

def plot_scores(scores_dict, palette, dpi, bands):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6), dpi=dpi)
    names, scores = list(scores_dict.keys()), list(scores_dict.values())
    graph_scores = sns.barplot(x=names, y=scores,
                               palette=get_palette_from_values(scores, palette))

    # Add value label to top of bars
    for p in graph_scores.patches:
        graph_scores.annotate('{:.0f}'.format(p.get_height()),
                              (p.get_x() + p.get_width() / 2, p.get_height() + 0.1),
                              ha='center', va='bottom',
                              color='black')

    add_labeled_bands(bands, ax)
    ax.set_title('Game scores')
    plt.margins(0, 0)
    ax.grid(False)
    sns.set_style("ticks", {"xtick.major.size": 1})
    plt.savefig('../outputs/game_scores.png', bbox_inches='tight')

def show_template():
    pass

if __name__ == "__main__":
    try:
        with open('../outputs/scores_dict.p', 'rb') as f:
            scores_dict = pickle.load(f)
    except FileNotFoundError as e:
        print("Can't plot because scores haven't been generated yet.")
        raise(e)
    with open("../conf/config.yml") as file:  # Load configuration
        config = yaml.full_load(file)
    palette, dpi, bands = config["palette"], config["dpi"], config["bands"]
    plot_scores(scores_dict, palette, dpi, bands)