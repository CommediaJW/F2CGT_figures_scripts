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


def plot(model_names, names, data, output_path, min_ylim, max_ylim, ystep):
    plt.figure(figsize=(9, 2.5))
    plt.subplots_adjust(wspace=0.4)
    plt.clf()
    # fix parameter
    font_size = 20
    plt.rcParams['font.size'] = font_size

    for it, model_name in enumerate(model_names):
        plt.subplot(1, 2, it + 1)
        plt.title(model_name, fontsize=font_size, y=-0.55, fontweight="bold")
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
        max_xlim = len(data[model_name][names[model_name][0]]) + 1
        plt.xlim(0, max_xlim)
        x = np.arange(1, max_xlim)
        xticks = np.arange(0, max_xlim + 1, 5)
        plt.ylim(min_ylim, max_ylim)
        if (max_ylim - min_ylim) % ystep == 0:
            yticks = np.arange(min_ylim, max_ylim + ystep, ystep)
        else:
            yticks = np.arange(min_ylim, max_ylim, ystep)
        ylabels = []
        for ytick in yticks:
            ylabels.append("{:d}%".format(int(ytick * 100)))
        plt.xlabel("Epoch", fontsize=font_size)
        if it == 0:
            plt.ylabel("Test Accuracy", fontsize=font_size)
        plt.xticks(xticks)
        plt.yticks(yticks, ylabels)
        for it, name in enumerate(names[model_name]):
            print(data[model_name][name])
            plt.plot(x,
                     data[model_name][name],
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


def draw_figure(output_path, min_ylim, max_ylim, ystep):
    sage_header, sage_all_data = read_data("data/eval_accuracy_graphsage.csv")
    gat_header, gat_all_data = read_data("data/eval_accuracy_gat.csv")

    output_path = output_path + "eval_accuracy.pdf"
    plot(["GraphSAGE", "GAT"], {
        "GraphSAGE": sage_header,
        "GAT": gat_header
    }, {
        "GraphSAGE": sage_all_data,
        "GAT": gat_all_data
    }, output_path, min_ylim, max_ylim, ystep)


if __name__ == "__main__":
    draw_figure("figures/", 0, 1.0, 0.5)
