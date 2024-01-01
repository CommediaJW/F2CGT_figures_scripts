import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

marker_list = ["o", "^", "s", "v"]
color_list = ["#e9a196", "#c3d5b2", "#86beda", "#ddc19e"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def get_labels(data):
    for key, value in data.items():
        return [label[0] for label in value]


def read_data(path):
    all_data = {}
    labels = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 1:
                all_data[row[0]] = []
                labels.append(row[0])
            else:
                all_data[labels[-1]].append(row)

    return labels, all_data


def tick_switch(input, ticks):
    output = []
    for number in input:
        for i in range(len(ticks)):
            if i < len(ticks) - 1:
                if number >= ticks[i] and number < ticks[i + 1]:
                    break
        if i == len(ticks) - 1:
            output.append(len(ticks) - 1)
        else:
            switched = i + (number - ticks[i]) / (ticks[i + 1] - ticks[i])
            output.append(switched)
    return output


def plot(names, data, output_path, min_ylim, max_ylim, ystep):
    plt.figure(figsize=(8.5, 2.5))
    plt.clf()
    font_size = 20
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
    x_tikcs = [0, 1, 2, 3, 4]
    x_labels = [1, 4, 16, 64, 256]
    plt.xlim(0, 4)
    plt.xticks(x_tikcs, x_labels)
    plt.xlabel("Compression Ratio", fontsize=font_size)

    plt.ylim(min_ylim, max_ylim)
    if (max_ylim - min_ylim) % ystep == 0:
        yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
    else:
        yticks = np.arange(min_ylim, max_ylim, ystep)
    plt.ylabel("Accuracy", fontsize=font_size)
    ylabels = []
    for ytick in yticks:
        ylabels.append("{:2.1f}%".format(ytick * 100))
    plt.yticks(yticks, ylabels)

    for it, name in enumerate(names):
        this_data = data[name]
        xplot = []
        yplot = []
        for item in this_data:
            xplot.append(float(item[0]))
            yplot.append(float(item[1]))
        xplot_tick = tick_switch(xplot, x_labels)
        plt.plot(xplot_tick,
                 yplot,
                 label=name,
                 linestyle='-',
                 color='k',
                 marker=marker_list[it],
                 markerfacecolor=color_list[it],
                 markersize=8,
                 markeredgecolor='k',
                 clip_on=False,
                 zorder=10,
                 markeredgewidth=1)

    plt.legend(
        fontsize=font_size - 2,
        edgecolor="k",
        ncol=1,
        loc="upper center",
        bbox_to_anchor=(0.11, 0.55),
    )

    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, min_ylim, max_ylim, ystep):
    header, all_data = read_data(input_path)

    output_path = "figures/" + "compression_vq_sq.pdf"
    plot(header, all_data, output_path, min_ylim, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("data/compression_vq_sq.csv", "figures", 0.95, 0.965, 0.005)
