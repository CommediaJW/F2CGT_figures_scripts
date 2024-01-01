import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# hatch_list = ["//", "\\\\", "xx", "++", "||", "--"]
hatch_list = [None, None, None, None, None, None]
color_list = ["#e9a196", "#86beda", "#c3d5b2", "#ddc19e", "#937fb6", "#4f807d"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def read_data(path):
    labels = []
    data = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            labels.append(row[0])
            data.append(float(row[1]))

    return labels, data


def plot(labels, data, output_path, min_ylim, max_ylim, ystep):
    plt.figure(figsize=(8, 2.5))
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
    # plt.ylabel("#Machines", fontsize=font_size)

    plt.xlim(min_ylim, max_ylim)
    if max_ylim % ystep == 0:
        yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
    else:
        yticks = np.arange(min_ylim, max_ylim, ystep)
    plt.xticks(yticks)
    plt.xlabel("Normalized Throughput", fontsize=font_size, x=0.4)
    plot_x = np.arange(tick_space_len, (1 + len(labels)) * tick_space_len,
                       tick_space_len)
    plot_y = []
    plot_label = []
    for e in data:
        if e > 0.01:
            plot_y.append(e)
            plot_label.append("%.2f" % e)
    container = plt.barh(
        plot_x,
        plot_y,
        height=bar_width,
        edgecolor="k",
        hatch=hatch_list[0],
        color=color_list[3],
        zorder=10,
    )
    plt.bar_label(container,
                  plot_label,
                  fontsize=font_size - 2,
                  zorder=10,
                  padding=3)
    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, min_ylim, max_ylim, ystep):
    labels, data = read_data(input_path)
    print(labels)
    print(data)
    output_path = "figures/" + "motivation_single_vs_dist.pdf"
    plot(labels, data, output_path, min_ylim, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("data/motivation_single_vs_dist.csv", "figures", 0.0, 1.8, 0.9)
