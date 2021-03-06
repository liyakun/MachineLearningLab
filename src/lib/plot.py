"""
This file provide plot tools
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.lines as mlines
import matplotlib.backends.backend_pdf as pltpage
from pylab import *
from mpl_toolkits.mplot3d import  Axes3D


class Plot:

    def __init__(self):
        pass

    def file_to_list(self, file_open):
        """
        Convert the readed file to list
        """
        line_list = [line for line in file_open.readlines()]
        temp_list, center_list, average_list, all_list = [], [], [], []
        length = len(line_list)
        for i,  line in enumerate(line_list):
            if i <= (length-4):
                temp_list.append(float(line.split(":")[1].rstrip()))
            elif i == length-3:
                average_list.append(float(line.split(":")[1].rstrip()))
            elif i == length-2:
                center_list.append(float(line.split(":")[1].rstrip()))
            else:
                all_list.append(float(line.split(":")[1].rstrip()))
        return temp_list, average_list, center_list, all_list

    def file_to_list_all_points(self, file_open):
        """
        Convert file to list, specialized for all point.
        """
        line_list = [line for line in file_open.readlines()]
        temp_list = []
        for i,  line in enumerate(line_list):
            temp_list.append(float(line.split(":")[1].rstrip()))
        return temp_list

    def plot(self, weights_all):
        """
        plot the error for SGD
        """
        size = len(weights_all)
        with pltpage.PdfPages("../resources/pic/weights.pdf") as pdf:
            for i in xrange(0, size):
                fig = plt.figure(figsize=(8.27, 11.69), dpi=100)
                plt.title("%dth weights convergence" % i)
                plt.plot(weights_all[i])
                pdf.savefig(fig)
                plt.close()

    def plot3dpoints(self, points, coefficients, mean_point):
        """
        Plot 3-D objects
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        _x, _y, _z = [], [], []
        for i in range(len(points)):
            _x.append(points[i][0])
            _y.append(points[i][1])
            _z.append(points[i][2])

        ax.scatter(_x, _y, _z, c='r', marker='o', color='yellow')
        ax.scatter(coefficients[0], coefficients[1], coefficients[2], color='red', marker='o')
        ax.scatter(mean_point[0], mean_point[1], mean_point[2], color='blue', marker='o')
        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
        ax.set_zlabel('z axis')
        plt.show()

    def plot_error(self, path):
        """
        Plot error in a more general manner.
        """
        fr = open(path)
        temp_list = []
        for line in fr:
                temp_list.append(line.split(":")[1])

        with pltpage.PdfPages(path+".weights.pdf") as pdf:
            fig = plt.figure()
            plt.title("error")
            plt.plot(temp_list, marker='.', linestyle='--', color='blue', markeredgecolor='red')
            pdf.savefig(fig)
            plt.close()

    def plot_time(self, path):
        """
        Plot the run time
        """
        time_list = []
        for i in range(100, 3000, 100):
            fr = open(path+"result_30_1000_"+str(i)+"/time.txt")
            #fr = open(path+str(i)+"/time.txt")
            for line in fr:
                line = line.replace("seconds", '')
                line = line.replace("---", '')
                time_list.append(float(line) / 3600)
        with pltpage.PdfPages(path+"run_time_diagram.pdf") as pdf:
            fig = plt.figure()
            ax = fig.gca()
            ax.set_xlabel('Number of instances for each single model, 1000-3000')
            #ax.set_xlabel('Number of Models, 1000-6000')
            ax.set_ylabel('Run time (hours)')
            xs = range(100, 3000, 100)
            ys = time_list
            ax.set_ylim(ymin=0.00)
            ax.set_ylim(ymax=30.00)
            ax.plot(xs, ys)
            pdf.savefig(fig)
            plt.close()

    def plot_time_dimensions(self, path):
        """
        Plot time for dimension test
        """
        time_list = []
        for i in range(2, 15, 1):
            fr = open(path+str(i)+"/time.txt")
            for line in fr:
                time_list.append(float(line) / 3600)
        with pltpage.PdfPages(path+"run_time_diagram.pdf") as pdf:
            fig = plt.figure()
            ax = fig.gca()
            ax.set_xlabel('Number of features, 2-14')
            ax.set_ylabel('Run time (hours)')
            xs = range(2, 15, 1)
            ys = time_list
            ax.set_ylim(ymin=0.00)
            ax.set_ylim(ymax=30.00)
            ax.plot(xs, ys)
            pdf.savefig(fig)
            plt.close()

    def plot_comparing_median(self, n, path):
        """
        Plot the Tverberg point comparison of dimension test
        """
        random_list = []
        random_all, random_mean, random_tverberg = [], [], []
        for j in range(100, 3000, 100):
            random_special_list = [[], [], []]
            for i in range(n):
                fr_random = (open(path+"result_30_1000_"+str(j)+"/"+str(i)+"error_random.txt"))
                random_, ra_average_list, ra_center_list, ra_all_list = self.file_to_list(fr_random)
                random_list.append(random_)
                random_special_list[0].append(ra_average_list)
                random_special_list[1].append(ra_center_list)
                random_special_list[2].append(ra_all_list)
            random_all.append(random_special_list[2])
            random_tverberg.append(random_special_list[1])
            random_mean.append(random_special_list[0])

        self.box_plot_no_special_point(random_mean, path, "random", "average_")
        self.box_plot_no_special_point(random_tverberg, path, "random", "tverberg_")
        self.box_plot_no_special_point(random_all, path, "random", "all_")

    def box_plot_with_special_point(self, equal_list, equal_special_list, path, str_):
        """
        box plot with single models, as well as Tverberg point, Average point, All point
        """
        fig1 = plt.figure(1, figsize=(14, 14))
        ax = fig1.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        meanlineprops = dict(linestyle='--', linewidth=2.5, color='purple')

        # get all the variance value w.r.t equal_list(random_list)
        """
        randomDists = [str(round(np.var(equal_list[0]), 4))+'/t_1', str(round(np.var(equal_list[1]), 4))+'/t_2', str(round(np.var(equal_list[2
             ]), 4))+'/t_3', str(round(np.var(equal_list[3]), 4))+'/t_4', str(round(np.var(equal_list[4]), 4))+'/t_5',
             str(round(np.var(equal_list[5]), 4))+'/t_6', str(round(np.var(equal_list[6]), 4))+'/t_7', str(round(np.var(equal_list[7]), 4))+'/t_8',
             str(round(np.var(equal_list[8]), 4))+'/t_9', str(round(np.var(equal_list[9]), 4))+'/t_10', str(round(np.var(equal_list[10]), 4))+'/t_11', str(round(np.var(equal_list[11]), 4))+'/t_12', str(round(np.var(equal_list[12
             ]), 4))+'/t_13', str(round(np.var(equal_list[13]), 4))+'/t_14', str(round(np.var(equal_list[14]), 4))+'/t_15',
             str(round(np.var(equal_list[15]), 4))+'/t_16', str(round(np.var(equal_list[16]), 4))+'/t_17', str(round(np.var(equal_list[17]), 4))+'/t_18',
             str(round(np.var(equal_list[18]), 4))+'/t_19', str(round(np.var(equal_list[19]), 4))+'/t_20', str(round(np.var(equal_list[20]), 4))+'/t_21', str(round(np.var(equal_list[21]), 4))+'/t_22', str(round(np.var(equal_list[22
             ]), 4))+'/t_23', str(round(np.var(equal_list[23]), 4))+'/t_24', str(round(np.var(equal_list[24]), 4))+'/t_25',
             str(round(np.var(equal_list[25]), 4))+'/t_26', str(round(np.var(equal_list[26]), 4))+'/t_27', str(round(np.var(equal_list[27]), 4))+'/t_28',
             str(round(np.var(equal_list[28]), 4))+'/t_29', str(round(np.var(equal_list[29]), 4))+'/t_30']
        """
        bp_0 = ax.boxplot(equal_list, 1, meanprops=meanlineprops, meanline=True, showmeans=True)

        bp_1 = ax.boxplot(equal_special_list[0])
        for i, median in enumerate(bp_1['medians']):
            if i == 0:
                median.set(color='red', linewidth=1, label="mean_point")
            else:
                median.set(color='red', linewidth=1)

        bp_2 = ax.boxplot(equal_special_list[1])
        for i, median in enumerate(bp_2['medians']):
            if i == 0:
                median.set(color='magenta', linewidth=1, label="tverberg_point")
            else:
                median.set(color='magenta', linewidth=1)

        bp_3 = ax.boxplot(equal_special_list[2])
        for i, median in enumerate(bp_3['medians']):
            if i == 0:
                median.set(color='yellow', linewidth=1, label="all_point")
            else:
                median.set(color='yellow', linewidth=1)

        # Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        # Hide these grid behind plot objects
        ax.set_axisbelow(True)

        # add xtick name with variance value
        # xticksNames = plt.setp(ax, xticklabels=np.repeat(randomDists, 1))
        # plt.setp(xticksNames, fontsize=5)

        # change outline color, fill color and linewidth of the boxes
        for box in bp_0['boxes']:
            # change outline color
            box.set(color='#7570b3', linewidth=1)

        # change color and linewidth of the whiskers
        for whisker in bp_0['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the caps
        for cap in bp_0['caps']:
            cap.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the medians
        for i, median in enumerate(bp_0['medians']):
            if i == 0:
                median.set(color='#b2df8a', linewidth=2, label="error_median")
            else:
                median.set(color='#b2df8a', linewidth=2)

        dash_line = mlines.Line2D([], [], color='purple', label='error_mean', linestyle='--')

        if str_ == "equal":
            ax.set_xlabel('Equal Sample-Lists of Weight Vectors with variance at bottom')
        else:
            ax.set_xlabel('Random Sample-Lists of Weight Vectors')
        ax.set_ylabel('Errors of Each Weight Vector')
        # Put a legend below current axis
        f1 = plt.legend(handles=[dash_line], loc=1)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        ax = plt.gca().add_artist(f1)

        if str_ == "equal":
            fig1.savefig(path+'fig_equal.png', bbox_inches='tight')
        else:
            fig1.savefig(path+'fig_random.png', bbox_inches='tight')

        plt.close()

    def box_plot_no_special_point(self, equal_list, path, str_, name_=""):
        """
        box plot of single models only
        """
        fig1 = plt.figure(1, figsize=(10, 10))
        ax = fig1.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        meanlineprops = dict(linestyle='--', linewidth=2.5, color='purple')
        # randomDists = [str(np.var(equal_list[0]))+'expt_1', np.var(equal_list[1]), np.var(equal_list[2]), np.var(equal_list[3]), np.
        #     var(equal_list[4]), np.var(equal_list[5]), np.var(equal_list[6]), np.var(equal_list[7]),
        #                np.var(equal_list[8]), np.var(equal_list[9])]
        bp_0 = ax.boxplot(equal_list, 1, meanprops=meanlineprops, meanline=True, showmeans=True)

        y = []

        for i in range(len(equal_list)):
            y.append(np.median(np.array(equal_list[i])))

        x = np.arange(1, 30, 1)

        ax.plot(x, y, 'b-')

        ax.set_ylim(ymin=0.2)
        ax.set_ylim(ymax=0.7)
        # Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        # Hide these grid behind plot objects
        ax.set_axisbelow(True)

        # add xtick name with variance value
        # xticksNames = plt.setp(ax, xticklabels=np.repeat(randomDists, 1))
        # plt.setp(xticksNames, rotation=45, fontsize=8)

        # change outline color, fill color and linewidth of the boxes
        for box in bp_0['boxes']:
            # change outline color
            box.set(color='#7570b3', linewidth=1)

        # change color and linewidth of the whiskers
        for whisker in bp_0['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the caps
        for cap in bp_0['caps']:
            cap.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the medians
        for i, median in enumerate(bp_0['medians']):
            if i == 0:
                median.set(color='#b2df8a', linewidth=2, label="error_median")
            else:
                median.set(color='#b2df8a', linewidth=2)


        dash_line = mlines.Line2D([], [], color='purple', label='error_mean', linestyle='--')
        median_line = mlines.Line2D([], [], color='green', label='error_median')
        ax.set_ylabel('Errors')
        f2 = plt.legend(handles=[dash_line, median_line], loc=2)

        if str_ == "equal":
            ax.set_xlabel('Equal Sample-Lists of Weight Vector with variance at bottom')
            fig1.savefig(path+name_+'fig_equal_.png', bbox_inches='tight')
        elif str_ == "random":
            ax.set_xlabel(name_+'points: Increasing number of training instance(100-2900, step 100), 29 tests')
            fig1.savefig(path+name_+'fig_random_.png', bbox_inches='tight')
        else:
            ax.set_xlabel('Errors_Different_Number_of_Instances')
            fig1.savefig(path+name_+'fig_all_.png', bbox_inches='tight')

        plt.close()

    def box_plot_only_special_point(self, special_list, path, str_):
        """
        box plot for Tverberg point, Average point, and All point
        """
        fig1 = plt.figure(1, figsize=(10, 10))
        ax = fig1.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        meanlineprops = dict(linestyle='--', linewidth=2.5, color='purple')

        """
        randomDists = [str(round(np.var(special_list[0]), 6))+'/mean_points', str(round(np.var(special_list[1]), 6))+
                       '/tverberg_points', str(round(np.var(special_list[2]), 6))+'/all_points',
                       str(round(np.var(special_list[3]), 5))+'/single_points']
        """
        randomDists = [str(round(np.var(special_list[0]), 6))+'/mean_points', str(round(np.var(special_list[1]), 6))+
                       '/tverberg_points', str(round(np.var(special_list[2]), 6))+'/all_points']

        bp_0 = ax.boxplot(special_list, 1, meanprops=meanlineprops, meanline=True, showmeans=True)

        # Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        # Hide these grid behind plot objects
        ax.set_axisbelow(True)

        # add xtick name with variance value
        xticksNames = plt.setp(ax, xticklabels=np.repeat(randomDists, 1))
        plt.setp(xticksNames, fontsize=8)

        # change outline color, fill color and linewidth of the boxes
        for box in bp_0['boxes']:
            # change outline color
            box.set(color='#7570b3', linewidth=1)

        # change color and linewidth of the whiskers
        for whisker in bp_0['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the caps
        for cap in bp_0['caps']:
            cap.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the medians
        for i, median in enumerate(bp_0['medians']):
            if i == 0:
                median.set(color='#b2df8a', linewidth=2, label="error_median")
            else:
                median.set(color='#b2df8a', linewidth=2)
        dash_line = mlines.Line2D([], [], color='purple', label='error_mean', linestyle='--')
        median_line = mlines.Line2D([], [], color='green', label='error_median')
        ax.set_ylabel('Errors')
        f2 = plt.legend(handles=[dash_line, median_line], loc=1)
        if str_ == "equal":
            ax.set_xlabel('Equal Sample-Lists of mean points, tverberg points and all points with variance at bottom')
            fig1.savefig(path+'fig_special_equal_.png', bbox_inches='tight')
        else:
            ax.set_xlabel('Random Sample-Lists of  mean points, tverberg points, and all points with variance at bottom')
            fig1.savefig(path+'fig_special_random_.png', bbox_inches='tight')

        plt.close()

    def box_plot(self, n, path):
        """
        A general box plot
        """
        equal_list, random_list = [], []
        equal_special_list, random_special_list = [[], [], []], [[], [], []]
        for i in range(n):
            fr_equal = (open(path+str(i)+"error_equal.txt"))
            fr_random = (open(path+str(i)+"error_random.txt"))
            equal, eq_average_list, eq_center_list, eq_all_list = self.file_to_list(fr_equal)
            random_, ra_average_list, ra_center_list, ra_all_list = self.file_to_list(fr_random)
            equal_list.append(equal)
            equal_special_list[0].append(eq_average_list)
            equal_special_list[1].append(eq_center_list)
            equal_special_list[2].append(eq_all_list)
            random_list.append(random_)
            random_special_list[0].append(ra_average_list)
            random_special_list[1].append(ra_center_list)
            random_special_list[2].append(ra_all_list)

        self.box_plot_with_special_point(equal_list, equal_special_list, path, "equal")
        self.box_plot_with_special_point(random_list, random_special_list, path, "random")
        self.box_plot_no_special_point(equal_list, path, "equal")
        self.box_plot_no_special_point(random_list, path, "random")
        self.box_plot_only_special_point(equal_special_list, path, "equal")
        self.box_plot_only_special_point(random_special_list, path, "random")

    def box_plot_random(self, n, path):
        """
        box plot only for random partition
        """
        random_list, random_list_all = [], []
        #random_special_list = [[], [], [], []]
        random_special_list = [[], [], []]
        for i in range(n):
            fr_random = (open(path+str(i)+"error_random.txt"))
            random_, ra_average_list, ra_center_list, ra_all_list = self.file_to_list(fr_random)
            random_list.append(random_)
            random_list_all.extend(random_)
            random_special_list[0].append(ra_average_list)
            random_special_list[1].append(ra_center_list)
            random_special_list[2].append(ra_all_list)
        #random_special_list[3] = random_list_all

        self.box_plot_with_special_point(random_list, random_special_list, path, "random")
        #self.box_plot_no_special_point(random_list, path, "random")
        self.box_plot_only_special_point(random_special_list, path, "random")

    def box_plot_all(self, n, path):
        """
        Box plot for testing all point
        """
        all_list = []
        for i in range(n):
            fr_all = (open(path+"error_all_half_step"+str(i)+".txt"))
            temp = self.file_to_list_all_points(fr_all)
            all_list.append(temp)

        all_all_list = []
        print len(all_list[0])
        for j in range(len(all_list[0])):
            temp_ = []
            for i in range(len(all_list)):
                temp_.append(all_list[i][j])
            all_all_list.append(temp_)

        self.box_plot_no_special_point(all_all_list, path, "all")

    def box_plot_special_point_dimension(self, special_list, path, str_):
        """
        box plot with speical point for dimension test
        """
        fig1 = plt.figure(1, figsize=(10, 10))
        ax = fig1.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        meanlineprops = dict(linestyle='--', linewidth=2.5, color='purple')

        randomDists = [str(2)+"-dim", str(3)+"-dim", str(4)+"-dim", str(5)+"-dim", str(6)+"-dim", str(7)+"-dim", str(8)+
                       "-dim", str(9)+"-dim", str(10)+"-dim", str(11)+"-dim", str(12)+"-dim", str(13)+"-dim", str(14)+
                       "-dim", str(15)+"-dim", str(16)+"-dim", str(17)+"-dim", str(18)+"-dim", str(19)+"-dim"]
        """
        randomDists = [str(2)+"-dim", str(3)+"-dim", str(4)+"-dim", str(5)+"-dim", str(6)+"-dim", str(7)+"-dim", str(8)+
                       "-dim", str(9)+"-dim", str(10)+"-dim", str(11)+"-dim", str(12)+"-dim", str(13)+"-dim",
                       str(14)+"-dim"]
        """
        bp_0 = ax.boxplot(special_list, 1, meanprops=meanlineprops, meanline=True, showmeans=True)

        y = []

        for i in range(len(special_list)):
            y.append(np.median(np.array(special_list[i])))

        x = np.arange(1, 19, 1)

        ax.plot(x, y, 'b-')
        ax.set_ylim(ymin=0.10)
        ax.set_ylim(ymax=0.80)
        # Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        # Hide these grid behind plot objects
        ax.set_axisbelow(True)

        # add xtick name with variance value
        xticksNames = plt.setp(ax, xticklabels=np.repeat(randomDists, 1))
        plt.setp(xticksNames, fontsize=8)

        # change outline color, fill color and linewidth of the boxes
        for box in bp_0['boxes']:
            # change outline color
            box.set(color='#7570b3', linewidth=1)

        # change color and linewidth of the whiskers
        for whisker in bp_0['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the caps
        for cap in bp_0['caps']:
            cap.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the medians
        for i, median in enumerate(bp_0['medians']):
            if i == 0:
                median.set(color='#b2df8a', linewidth=2, label="error_median")
            else:
                median.set(color='#b2df8a', linewidth=2)
        dash_line = mlines.Line2D([], [], color='purple', label='error_mean', linestyle='--')
        median_line = mlines.Line2D([], [], color='green', label='error_median')
        ax.set_ylabel('Errors')
        f2 = plt.legend(handles=[dash_line, median_line], loc=2)

        if str_ == "tverberg":
            ax.set_xlabel('Tverberg points with increasing dimensions.')
            fig1.savefig(path+'tverberg.png', bbox_inches='tight')
        elif str_ == "average":
            ax.set_xlabel('Average points with increasing dimensions')
            fig1.savefig(path+'average.png', bbox_inches='tight')
        else:
            ax.set_xlabel('All points with increasing dimensions')
            fig1.savefig(path+'all_.png', bbox_inches='tight')

        plt.close()

    def box_plot_special_point_instance(self, special_list, path, str_):
        """
        box plot for special point of instance test
        """
        fig1 = plt.figure(1, figsize=(10, 10))
        ax = fig1.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        meanlineprops = dict(linestyle='--', linewidth=2.5, color='purple')
        randomDists = [str(1000), str(1500), str(2000), str(2500), str(3000), str(3500), str(4000), str(4500), str(5000),
                       str(5500), str(6000), str(6500), str(7000), str(7500), str(8000), str(8500), str(9000), str(9500), str(10000)]
        bp_0 = ax.boxplot(special_list, 1, meanprops=meanlineprops, meanline=True, showmeans=True)

        # Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        # Hide these grid behind plot objects
        ax.set_axisbelow(True)

        # add xtick name with variance value
        xticksNames = plt.setp(ax, xticklabels=np.repeat(randomDists, 1))
        plt.setp(xticksNames, fontsize=8)

        y = []

        for i in range(len(special_list)):
            y.append(np.median(np.array(special_list[i])))

        x = np.arange(1000, 19, 1)

        # change outline color, fill color and linewidth of the boxes
        for box in bp_0['boxes']:
            # change outline color
            box.set(color='#7570b3', linewidth=1)

        # change color and linewidth of the whiskers
        for whisker in bp_0['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the caps
        for cap in bp_0['caps']:
            cap.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the medians
        for i, median in enumerate(bp_0['medians']):
            if i == 0:
                median.set(color='#b2df8a', linewidth=2, label="error_median")
            else:
                median.set(color='#b2df8a', linewidth=2)
        ax.set_ylabel('Errors')
        if str_ == "tverberg":
            ax.set_xlabel('Tverberg points with increasing single models.')
            fig1.savefig(path+'tverberg.png', bbox_inches='tight')
        elif str_ == "average":
            ax.set_xlabel('Average points with increasing single models')
            fig1.savefig(path+'average.png', bbox_inches='tight')
        else:
            ax.set_xlabel('All points with increasing single models')
            fig1.savefig(path+'all_.png', bbox_inches='tight')

        plt.close()

    def box_plot_special_point_vectors(self, special_list, path, str_):
        """
        box plot of special point for varying number of models test
        """
        fig1 = plt.figure(1, figsize=(10, 10))
        ax = fig1.add_subplot(111)
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
        meanlineprops = dict(linestyle='--', linewidth=2.5, color='purple')
        """
        randomDists = [str(2)+"-dim", str(3)+"-dim", str(4)+"-dim", str(5)+"-dim", str(6)+"-dim", str(7)+"-dim", str(8)+
                       "-dim", str(9)+"-dim", str(10)+"-dim", str(11)+"-dim", str(12)+"-dim", str(13)+"-dim", str(14)+
                       "-dim", str(15)+"-dim", str(16)+"-dim", str(17)+"-dim", str(18)+"-dim", str(19)+"-dim"]
        """

        randomDists = [str(1000), str(1500), str(2000), str(2500), str(3000), str(3500), str(4000), str(4500),
                       str(5000), str(5500), str(6000)]

        bp_0 = ax.boxplot(special_list, 1, meanprops=meanlineprops, meanline=True, showmeans=True)

        y = []

        for i in range(len(special_list)):
            y.append(np.median(np.array(special_list[i])))

        x = np.arange(1, 12, 1)

        ax.plot(x, y, 'b-')
        ax.set_ylim(ymin=0.20)
        ax.set_ylim(ymax=0.70)
        # Remove top axes and right axes ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        # Hide these grid behind plot objects
        ax.set_axisbelow(True)

        # add xtick name with variance value

        xticksNames = plt.setp(ax, xticklabels=np.repeat(randomDists, 1))
        plt.setp(xticksNames, fontsize=8)


        # change outline color, fill color and linewidth of the boxes
        for box in bp_0['boxes']:
            # change outline color
            box.set(color='#7570b3', linewidth=1)

        # change color and linewidth of the whiskers
        for whisker in bp_0['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the caps
        for cap in bp_0['caps']:
            cap.set(color='#7570b3', linewidth=2)

        # change color and linewidth of the medians
        for i, median in enumerate(bp_0['medians']):
            if i == 0:
                median.set(color='#b2df8a', linewidth=2, label="error_median")
            else:
                median.set(color='#b2df8a', linewidth=2)
        dash_line = mlines.Line2D([], [], color='purple', label='error_mean', linestyle='--')
        median_line = mlines.Line2D([], [], color='green', label='error_median')
        ax.set_ylabel('Errors')
        f2 = plt.legend(handles=[dash_line, median_line], loc=2)

        if str_ == "tverberg":
            ax.set_xlabel('Tverberg points with increasing number of models.')
            fig1.savefig(path+'tverberg.png', bbox_inches='tight')
        elif str_ == "average":
            ax.set_xlabel('Average points with increasing number of models')
            fig1.savefig(path+'average.png', bbox_inches='tight')
        else:
            ax.set_xlabel('All points with increasing models')
            fig1.savefig(path+'all_.png', bbox_inches='tight')

        plt.close()

    def box_plot_different_dimensions(self, n, path):
        """
        box plot for dimension test
        """
        special_list_list = [[], [], []]
        for i in range(2, n):
            random_special_list = [[], [], []]
            m = 20
            for j in range(m):
                fr_random = open(path+str(i)+"/"+str(j)+"error_random.txt")
                random_, ra_average_list, ra_center_list, ra_all_list = self.file_to_list(fr_random)
                random_special_list[0].append(ra_average_list)
                random_special_list[1].append(ra_center_list)
                random_special_list[2].append(ra_all_list)
            special_list_list[0].append(random_special_list[0])
            special_list_list[1].append(random_special_list[1])
            special_list_list[2].append(random_special_list[2])
        self.box_plot_special_point_dimension(special_list_list[0], path, "average")
        self.box_plot_special_point_dimension(special_list_list[1], path, "tverberg")
        self.box_plot_special_point_dimension(special_list_list[2], path, "all")

    def box_plot_different_instances(self, n, path):
        """
        box plot for varying number of instances test
        """
        special_list_list = [[], [], []]
        list_ = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]
        for i in list_:
            random_special_list = [[], [], []]
            for j in range(10):
                fr_random = open(path+str(i) +"/"+str(j)+"error_random.txt")
                random_, ra_average_list, ra_center_list, ra_all_list = self.file_to_list(fr_random)
                random_special_list[0].append(ra_average_list)
                random_special_list[1].append(ra_center_list)
                random_special_list[2].append(ra_all_list)
            special_list_list[0].append(random_special_list[0])
            special_list_list[1].append(random_special_list[1])
            special_list_list[2].append(random_special_list[2])
        self.box_plot_special_point_instance(special_list_list[0], path, "average")
        self.box_plot_special_point_instance(special_list_list[1], path, "tverberg")
        self.box_plot_special_point_instance(special_list_list[2], path, "all")

    def box_plot_different_vectors(self, path):
        """
        box plot for varying number of vectors
        """
        special_list_list = [[], [], []]
        for i in range(1000, 6500, 500):
            random_special_list = [[], [], []]
            m = 30
            for j in range(m):
                fr_random = open(path+str(i)+"/"+str(j)+"error_random.txt")
                random_, ra_average_list, ra_center_list, ra_all_list = self.file_to_list(fr_random)
                random_special_list[0].append(ra_average_list)
                random_special_list[1].append(ra_center_list)
                random_special_list[2].append(ra_all_list)
            special_list_list[0].append(random_special_list[0])
            special_list_list[1].append(random_special_list[1])
            special_list_list[2].append(random_special_list[2])
        self.box_plot_special_point_vectors(special_list_list[0], path, "average")
        self.box_plot_special_point_vectors(special_list_list[1], path, "tverberg")
        self.box_plot_special_point_vectors(special_list_list[2], path, "all")
