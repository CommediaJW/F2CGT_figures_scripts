import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

hatch_list = ["\\\\", "//", "xx", "++", "||", "--"]
# hatch_list = [None, None, None, None, None, None]
color_list = ["#e9a196", "#86beda", "#c3d5b2", "#ddc19e", "#937fb6", "#4f807d"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def read_data(path):
    labels = []
    all_data = {}
    with open(path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            new_row = []
            cur_key = row[0]
            labels.append(cur_key)
            all_data[cur_key] = row[1:]

    return labels, all_data


def plot(labels, data, output_path, min_ylim, max_ylim, ystep):
    plt.figure(figsize=(7, 2.5))
    plt.clf()
    # fix parameter
    font_size = 20
    tick_space_len = 1
    bar_width = 0.5
    plt.rcParams['font.size'] = font_size

    plt.tick_params(
        axis="both",
        which="major",
        labelsize=font_size,
        direction="in",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    xlim = (len(labels) + 1) * tick_space_len
    xlabels = [""] + labels + [""]
    xticks = np.arange(0, len(labels) + 1 + tick_space_len, tick_space_len)
    plt.ylim(0, xlim)
    plt.yticks(xticks, xlabels)
    # plt.ylabel("Dataset", fontsize=font_size)

    plt.xlim(min_ylim, max_ylim)
    num_yticks = max_ylim // ystep + 1
    yticks = np.arange(0, num_yticks * ystep, ystep)
    plt.xticks(yticks)
    plt.xlabel("Latency (sec)", fontsize=font_size)

    for it in range(len(data[labels[0]])):
        plot_x = np.arange(1, 1 + len(labels))
        plot_y = []
        for label in labels:
            plot_y.append(float(data[label][it]))
        plot_y = np.array(plot_y)
        if it > 0:
            container = plt.barh(
                plot_x,
                plot_y,
                left=plot_y_,
                height=bar_width,
                edgecolor="k",
                hatch=hatch_list[it],
                color=color_list[it],
                label="Model Computation",
                zorder=10,
            )
            plot_y_ = np.add(plot_y_, plot_y)
        else:
            container = plt.barh(
                plot_x,
                plot_y,
                height=bar_width,
                edgecolor="k",
                hatch=hatch_list[it],
                color=color_list[it],
                label="Data Processing",
                zorder=10,
            )
            plot_y_ = plot_y
    plt.legend(fontsize=font_size - 2,
               edgecolor="k",
               ncol=2,
               loc="upper center",
               bbox_to_anchor=(0, 1.35, 1, 0))
    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, min_ylim, max_ylim, ystep):
    labels, all_data = read_data(input_path)

    plot(labels, all_data, output_path, min_ylim, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("data/motivation_single_vs_dist_v2.csv",
                "figures/motivation_single_vs_dist_v2.pdf", 0.0, 12.0, 4.0)
