import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

hatch_list = ["//", "xx", "\\\\", "++", "||", "--"]
# hatch_list = [None, None, None, None, None, None]
color_list = ["#e9a196", "#c3d5b2", "#86beda", "#ddc19e", "#937fb6", "#4f807d"]


def isfloat(val):
    return all([[any([i.isnumeric(), i in [".", "e"]]) for i in val],
                len(val.split(".")) == 2])


def get_labels(data):
    for key, value in data.items():
        return [label[0] for label in value]


def read_data(path):
    elements = []
    labels = []
    cur_key = None
    all_data = {}
    dataeset_name = []
    with open(path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if len(row) == 1:
                "Dataset"
                cur_key = row[0]
                all_data[cur_key] = []
                elements.clear()
                labels.clear()
                dataeset_name.append(cur_key)
            else:
                new_row = []
                for d in row[1:]:
                    if isfloat(d) or d.isdigit():
                        new_row.append(float(d))
                    else:
                        new_row.append(0)
                all_data[cur_key].append([row[0], new_row])

    labels = get_labels(all_data)

    return dataeset_name, header, labels, all_data


def plot(names, object_labels, group_labels, data, lengend, output_path,
         min_ylim, max_ylim, ystep, model_name):
    plt.figure(figsize=(20, 2.5))
    plt.subplots_adjust(wspace=0.2)
    plt.clf()
    # fix parameter
    font_size = 20
    tick_space_len = 1
    plt.rcParams['font.size'] = font_size

    for it, name in enumerate(names):
        ax = plt.subplot(1, 4, it + 1)

        plt.title(name + "-" + model_name,
                  fontsize=font_size,
                  y=-0.52,
                  fontweight="bold")
        ax.tick_params(
            axis="both",
            which="major",
            labelsize=font_size,
            direction="in",
            bottom=True,
            top=True,
            left=True,
            right=True,
        )

        xlim = (1 + len(group_labels)) * tick_space_len
        xlabels = [""] + group_labels
        bar_width = 0.35
        xticks = np.arange(0, xlim, tick_space_len)
        ax.set_xlim(0, xlim)
        ax.set_xticks(xticks, xlabels)
        ax.set_xlabel("#GPUs", fontsize=font_size)

        if it == 0:
            ax.set_ylabel(
                "Throughput",
                fontsize=font_size,
            )
        ax.set_ylim(min_ylim[it], max_ylim[it])
        if max_ylim[it] % ystep[it] == 0:
            ax.set_yticks(
                np.arange(min_ylim[it], max_ylim[it] + ystep[it], ystep[it]))
        else:
            ax.set_yticks(np.arange(min_ylim[it], max_ylim[it], ystep[it]))
        ax.ticklabel_format(style='scientific',
                            axis='y',
                            scilimits=(3, 3),
                            useMathText=True)

        for i in range(len(object_labels)):
            plot_x = np.arange(1 * tick_space_len,
                               (1 + len(group_labels)) * tick_space_len,
                               tick_space_len,
                               dtype=float)

            cluster_len = bar_width * len(group_labels)
            plot_x -= cluster_len / 2  # start offset of bar cluster
            plot_x += bar_width * (i + 1)  # start offset of this bar
            plot_y = []
            plot_label = []
            for e in data[name][i][1]:
                if e > 0.01:
                    plot_y.append(e)
                    # plot_label.append("")
                else:
                    plot_y.append(0)
                    # plot_label.append("x")
            container = ax.bar(
                plot_x,
                plot_y,
                width=bar_width,
                edgecolor="k",
                hatch=hatch_list[i],
                color=color_list[i],
                label=object_labels[i],
                zorder=10,
            )
            plot_y = np.array(plot_y)
            missing_indices = np.where(plot_y == 0)[0]  # 找到缺失数据的索引
            for index in missing_indices:
                plt.scatter(plot_x[index],
                            max_ylim[it] // 20,
                            marker='x',
                            color='k',
                            s=80,
                            zorder=10)
            # ax.bar_label(container,
            #              plot_label,
            #              fontsize=font_size - 2,
            #              zorder=10)

        # plot_x = np.arange(1 * tick_space_len,
        #                    (1 + len(group_labels)) * tick_space_len,
        #                    tick_space_len,
        #                    dtype=float)
        # cluster_len = bar_width * len(object_labels)

        # for i in range(len(plot_y)):
        #     if i > 0:
        #         plot_y[i] = plot_y[i - 1] * 2
        # container = ax.bar(
        #     plot_x,
        #     plot_y,
        #     width=cluster_len,
        #     edgecolor="k",
        #     hatch=None,
        #     color="w",
        #     label=None,
        #     zorder=9,
        # )
        # ax.bar_label(container, plot_label, fontsize=font_size - 2, zorder=10)

        ax.legend(
            fontsize=font_size - 5,
            edgecolor="k",
            ncol=1,
            loc="upper center",
            bbox_to_anchor=(0.25, 1.02),
        )
    plt.rcParams['font.size'] = font_size
    print(f"[Note]Save to {output_path}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close("all")


def draw_figure(input_path, output_path, min_ylim, max_ylim, ystep):
    names, header, labels, all_data = read_data(input_path)

    output_path = "figures/" + "eval_dist_performance_sage.pdf"
    plot(names, labels, header, all_data, None, output_path, min_ylim,
         max_ylim, ystep, "GraphSAGE")


def draw_figure2(input_path, output_path, min_ylim, max_ylim, ystep):
    names, header, labels, all_data = read_data(input_path)

    output_path = "figures/" + "eval_dist_performance_gat.pdf"
    plot(names, labels, header, all_data, None, output_path, min_ylim,
         max_ylim, ystep, "GAT")


if __name__ == "__main__":
    draw_figure("data/eval_dist_performance_sage.csv", "figures", [0, 0, 0, 0],
                [250000, 350000, 450000, 850000],
                [125000, 175000, 225000, 425000])
    draw_figure2("data/eval_dist_performance_gat.csv", "figures", [0, 0, 0, 0],
                 [250000, 350000, 450000, 800000],
                 [125000, 175000, 225000, 400000])
