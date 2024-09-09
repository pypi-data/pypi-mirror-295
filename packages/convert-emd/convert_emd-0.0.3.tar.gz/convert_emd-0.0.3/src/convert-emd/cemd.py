import os
from rsciio.emd import file_reader
from skimage import exposure
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def transparent_single_color_cmap(color):
    return mcolors.LinearSegmentedColormap.from_list(
        "", [mcolors.to_rgba(color, 0), mcolors.to_rgba(color, 1)]
    )

def draw_scale_bar(frame, size_x, size_y, sb_x_start, sb_y_start, width_factor, sb_color):
    sb_lst = [0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000]
    scale = frame["axes"][1]["scale"]
    unit = frame["axes"][1]["units"]
    sb_len_float = size_x * scale / 6
    sb_len = sorted(sb_lst, key=lambda a: abs(a - sb_len_float))[0]
    sb_len_px = sb_len / scale
    sb_start_x, sb_start_y, sb_width = (size_x * sb_x_start , size_y * sb_y_start, size_y / width_factor)
    return [plt.Rectangle((sb_start_x, sb_start_y), sb_len_px, sb_width, color=sb_color, fill=True), "_" + str(sb_len) + unit]
    

def cconvert_emd(file, output_type, scale_bar, sb_color, sb_x_start, sb_y_start, sb_width_factor, stretch, overlay_alpha, sub_alpha, eds_color, mapping_overlay):
    output_dir = file + "/"
    output_name = output_dir + file + "_"
    data = file_reader(file + ".emd")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    mapping_frame = []
    overlay = False

    for i in range(len(data)):
        frame = data[i]
        dim = frame["data"].ndim
        title = frame["metadata"]["General"]["title"]

        if dim == 2:
            low_constrain, high_constrain = np.percentile(frame["data"], (stretch[0], stretch[1]))
            frame["data"] = exposure.rescale_intensity(frame["data"], in_range=(low_constrain, high_constrain))

            cmp = "gray"
            if title in eds_color:
                cmp = transparent_single_color_cmap(eds_color.get(title))
                if title in mapping_overlay:
                    mapping_frame.append(i)
                    overlay = True
            elif overlay and title == "HAADF":
                mapping_frame.append(i)
                HADDF_frame_num = len(mapping_frame) - 1
            
            size_x, size_y = (frame["axes"][1]["size"], frame["axes"][0]["size"])
            plt.figure(figsize=(size_x/100, size_y/100), facecolor="black")
            ax = plt.gca()
            plt.imshow(frame["data"], cmap=cmp)

            if scale_bar == True:
                bar = draw_scale_bar(frame, size_x, size_y, sb_x_start, sb_y_start, sb_width_factor, sb_color)
                ax.add_patch(bar[0])
                sb_text = bar[1]
            
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins = (0, 0)
            plt.axis("off")
            if scale_bar == True:
                plt.savefig(output_name + title + "_" + str(i) + sb_text + output_type)
            else:
                plt.savefig(output_name + title + "_" + str(i) + output_type)
            plt.close()

    if overlay:
        element = ""
        HAADF_frame = data[mapping_frame[HADDF_frame_num]]
        size_x, size_y = (HAADF_frame["axes"][1]["size"], HAADF_frame["axes"][0]["size"])

        plt.figure(figsize=(size_x/100, size_y/100), facecolor="black")
        ax = plt.gca()
        plt.imshow(HAADF_frame["data"], cmap="gray", alpha=sub_alpha)
        for i in range(len(mapping_frame)):
            if i == HADDF_frame_num:
                continue
            title = data[mapping_frame[i]]["metadata"]["General"]["title"]
            plt.imshow(data[mapping_frame[i]]["data"], cmap=transparent_single_color_cmap(eds_color.get(title)), alpha=overlay_alpha)
            element = element + "_" + title
        
        if scale_bar == True:
            bar = draw_scale_bar(HAADF_frame, size_x, size_y, sb_x_start, sb_y_start, sb_width_factor, sb_color)
            ax.add_patch(bar[0])
            sb_text = bar[1]

        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins = (0, 0)
        plt.axis("off")
        if scale_bar == True:
            plt.savefig(output_name + "Overlay" + element + sb_text + output_type)
        else:
            plt.savefig(output_name + "Overlay" + element + output_type)
        plt.close()
