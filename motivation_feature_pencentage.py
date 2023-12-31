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
            total = 0
            for d in row[1:]:
                if isfloat(d) or d.isdigit():
                    new_row.append(float(d))
                    total += float(d)
            for i in range(len(new_row)):
                new_row[i] = new_row[i] / total
            new_row[-1] = 1 - sum(new_row[:-1])
            all_data[cur_key] = new_row

    return labels, all_data


def plot(labels, data, output_path, min_ylim, max_ylim, ystep):
    plt.figure(figsize=(9, 2.5))
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
    ylabels = []
    for tick in yticks:
        ylabels.append("{:d}%".format(int(tick * 100)))
    plt.xticks(np.arange(0, num_yticks * ystep, ystep), ylabels)
    plt.xlabel("Size Ratio", fontsize=font_size)

    for it in range(len(data[labels[0]])):
        plot_x = np.arange(1, 1 + len(labels))
        plot_y = []
        plot_label = []
        for label in labels:
            plot_y.append(data[label][it])
            plot_label.append("{:d}%".format(int(data[label][it] * 100)))
        if it > 0:
            container = plt.barh(
                plot_x,
                plot_y,
                left=plot_y_,
                height=bar_width,
                edgecolor="k",
                hatch=hatch_list[it],
                color=color_list[it],
                label="Feature",
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
                label="Structure",
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
    draw_figure("data/motivation_feature_pencentage.csv",
                "figures/motivation_feature_pencentage.pdf", 0.0, 1.0, 0.25)
