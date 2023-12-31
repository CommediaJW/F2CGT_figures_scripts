import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

marker_list = ["o", "^", "o", "^"]
color_list = ["#819fa6", "#c18076", "#3d4a55", "#d1b5ab"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def get_labels(data):
    for key, value in data.items():
        return [label[0] for label in value]


def read_data(path):
    all_data = {}
    with open(path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        print(header)
        for name in header:
            all_data[name] = []
        for row in reader:
            for i in range(len(row)):
                all_data[header[i]].append(float(row[i]))
    print(all_data)

    return header, all_data


def plot(names, data, output_path, min_ylim, max_ylim, ystep):
    plt.figure(figsize=(4.2, 2.5))
    plt.clf()
    # fix parameter
    font_size = 20
    plt.rcParams['font.size'] = font_size
    # plt.title("PD-GraphSAGE", fontsize=font_size + 1, y=-0.3)
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
    max_xlim = len(data[names[0]]) + 1
    plt.xlim(0, max_xlim)
    x = np.arange(1, max_xlim)
    xticks = np.arange(0, max_xlim + 1, 5)
    plt.ylim(min_ylim, max_ylim)
    if (max_ylim - min_ylim) % ystep == 0:
        yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
    else:
        yticks = np.arange(min_ylim, max_ylim, ystep)
    plt.xlabel("Epoch", fontsize=font_size)
    plt.ylabel("Test Accuracy", fontsize=font_size)
    plt.xticks(xticks)
    plt.yticks(yticks)
    for it, name in enumerate(names):
        print(data[name])
        plt.plot(x,
                 data[name],
                 label=name,
                 linestyle='-',
                 color='k',
                 marker=marker_list[it],
                 markerfacecolor=color_list[it],
                 markersize=8,
                 markeredgecolor='k',
                 markeredgewidth=1)

    plt.legend(
        fontsize=font_size - 2,
        edgecolor="k",
        ncol=1,
        loc="upper center",
        bbox_to_anchor=(0.69, 0.55),
    )

    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def plot2(names, data, output_path, min_ylim, max_ylim, ystep):
    plt.figure(figsize=(4.2, 2.5))
    plt.clf()
    # fix parameter
    font_size = 20
    plt.rcParams['font.size'] = font_size
    # plt.title("PD-GraphSAGE", fontsize=font_size + 1, y=-0.3)
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
    max_xlim = len(data[names[0]]) + 1
    plt.xlim(0, max_xlim)
    x = np.arange(1, max_xlim)
    xticks = np.arange(0, max_xlim + 1, 5)
    plt.ylim(min_ylim, max_ylim)
    if (max_ylim - min_ylim) % ystep == 0:
        yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
    else:
        yticks = np.arange(min_ylim, max_ylim, ystep)
    plt.xlabel("Epoch", fontsize=font_size)
    # plt.ylabel("Test Accuracy", fontsize=font_size)
    plt.xticks(xticks)
    plt.yticks(yticks)
    for it, name in enumerate(names):
        print(data[name])
        plt.plot(x,
                 data[name],
                 label=name,
                 linestyle='-',
                 color='k',
                 marker=marker_list[it],
                 markerfacecolor=color_list[it],
                 markersize=8,
                 markeredgecolor='k',
                 markeredgewidth=1)

    plt.legend(
        fontsize=font_size - 2,
        edgecolor="k",
        ncol=1,
        loc="upper center",
        bbox_to_anchor=(0.69, 0.55),
    )

    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, min_ylim, max_ylim, ystep):
    header, all_data = read_data(input_path)

    output_path = "figures/" + "eval_accuracy_graphsage.pdf"
    plot(header, all_data, output_path, min_ylim, max_ylim, ystep)


def draw_figure2(input_path, output_path, min_ylim, max_ylim, ystep):
    header, all_data = read_data(input_path)

    output_path = "figures/" + "eval_accuracy_gat.pdf"
    plot2(header, all_data, output_path, min_ylim, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("data/eval_accuracy_graphsage.csv", "figures", 0, 1.0, 0.5)
    draw_figure2("data/eval_accuracy_gat.csv", "figures", 0, 1.0, 0.5)
