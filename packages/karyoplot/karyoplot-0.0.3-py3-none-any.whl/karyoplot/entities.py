import pysam

from matplotlib import collections as mc
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt


class Sequence():
    def __init__(self, *args, **kwargs):

        self.kwargs = kwargs

        self.zoom = Utils.check_kwargs(self.kwargs,'zoom', str, '')
        self.size = Utils.check_kwargs(self.kwargs,'size', int, 1)
        self.color = Utils.check_kwargs(self.kwargs,'color', str, 'black')
        self.limitesize = Utils.check_kwargs(self.kwargs,'limitesize', int, 50)
        self.reference = Utils.check_kwargs(self.kwargs,'reference', str, '')
        self.scale = Utils.check_kwargs(self.kwargs,'scale', bool, False)
        self.seq_fontsize = Utils.check_kwargs(self.kwargs,'seq_fontsize', int, 14)
        self.x_label_fontsize = Utils.check_kwargs(self.kwargs, 'x_label_fontsize', int, 20)
        self.sharex = True
        if self.zoom:
            self.sharex = False


    def validate(self):
        if pysam.FastaFile(self.reference):
            return True


class Chromosome:

    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.zoom_min = 0
        self.zoom_max = length


class Track:
    def __init__(self, *args, **kwargs):

        self.kwargs = kwargs

        self.section = args[0]
        self.title = Utils.check_kwargs(self.kwargs,'title', str, '')
        self.graph_type = Utils.check_kwargs(self.kwargs,'graph_type', str, '')
        self.size = Utils.check_kwargs(self.kwargs,'size', float, 1)
        self.thickness = Utils.check_kwargs(self.kwargs,'thickness', float, 1)
        self.color = Utils.check_kwargs(self.kwargs,'color', str, 'red')
        self.colorin = Utils.check_kwargs(self.kwargs,'colorin', bool, False)
        self.data = Utils.check_kwargs(self.kwargs,'data', str, '')
        self.datatype = Utils.check_kwargs(self.kwargs,'datatype', str, '')
        self.background_color = Utils.check_kwargs(self.kwargs,'background_color', str, 'white')
        self.GC_window_length = Utils.check_kwargs(self.kwargs,'gc_window_length', int, 1000)
        self.GC_window_overlap = Utils.check_kwargs(self.kwargs,'gc_window_overlap', int, 100)
        self.scaley = Utils.check_kwargs(self.kwargs,'scaley', bool, False)
        self.y_label_fontsize = Utils.check_kwargs(self.kwargs, 'y_label_fontsize', int, 20)
        self.show_small_features = Utils.check_kwargs(self.kwargs,'show_small_features', bool, False)

        self._check_args()

    def _check_args(self):
        '''Check if all required args available'''

        no_datatype_required_graph = ['gc']

        if not self.datatype and self.graph_type.lower() \
                not in no_datatype_required_graph:
                    raise Exception("missing datatype in {}".format(self.section))


    def draw_track(self, sequence, ax, chrom, canvas):

        if not sequence.sharex:
            ax.set_xlim([chrom.zoom_min, chrom.zoom_max])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)

        # Parsed depending on datatype option
        if self.datatype.lower() == "bed":
            tbx = pysam.TabixFile(self.data)
            coordinates = []
            colors = []
            for data in tbx.fetch(chrom.name, chrom.zoom_min, chrom.zoom_max, parser=pysam.asTuple()):
                coordinates.append([[int(data[1]), 1], [int(data[2]), 1]])
                if self.colorin and len(data) >= 5:
                    if mcolors.is_color_like(data[4]):
                        colors.append(data[4])
                    else:
                        colors.append(self.color)
                else:
                    colors = self.color

            if self.show_small_features:
                coordinates = self.__resize_small_features(coordinates, chrom, canvas)
              
            lc = mc.LineCollection(coordinates, colors=colors, linewidths=self.thickness)
            ax.add_collection(lc)
            ax.set_ylim([0, 2])


        if self.datatype.lower() == "vcf":
            tbx = pysam.TabixFile(self.data)
            coordinates = []
            for vcf in tbx.fetch(chrom.name, chrom.zoom_min, chrom.zoom_max, parser=pysam.asVCF()):
                coordinates.append([vcf[1], 1])

            lc = mc.LineCollection(coordinates, colors=self.color, linewidths=self.thickness)
            ax.add_collection(lc)
            ax.set_ylim([0, 2])

        # If type is gc a sliding window must be called
        gc_min = []
        gc_max = []
        if self.graph_type.lower() == "gc":
            base_start, gcContent = self.__GC(sequence, chrom)
            ax.plot(base_start, gcContent, c=self.color, linewidth=self.thickness)

            gc_max.append(max(gcContent))
            gc_min.append(min(gcContent))

            if self.scaley:
                ax.set_ylim([min(gc_min) - 2, max(gc_max) + 2])
                ax.spines['left'].set_visible(True)
                ax.get_yaxis().set_visible(True)
                ax.tick_params(axis='y', labelsize=self.y_label_fontsize)

        # re-add background limited to max x
        # axis off, turned off set_facecolor
        # see: https://stackoverflow.com/questions/60805253/matplotlib-turning-axes-off-and-setting-facecolor-at-the-same-time-not-possible
        #ax.add_patch(plt.Rectangle((0, -5), chrom.length, 100, facecolor=self.background_color, zorder=-100))
        ax.add_patch(plt.Rectangle((chrom.zoom_min, -5), chrom.zoom_max-chrom.zoom_min, 100, facecolor=self.background_color, zorder=-100))

    def __resize_small_features(self, coordinates, chrom, canvas):

        ratio_base = (chrom.zoom_max-chrom.zoom_min)/(canvas.width*100)
        for coord in coordinates:
            if (coord[1][0]-coord[0][0]) < ratio_base:
                coord[0][0] = int((coord[0][0]+coord[1][0])/2) - int(ratio_base/2)
                coord[1][0] = int(coord[0][0] + ratio_base*1.25)
        return coordinates

    def __GC(self, sequence, chrom):

        fasta_file = pysam.FastaFile(sequence.reference)
        base_start = []
        gcContent = []
        step = self.GC_window_length - self.GC_window_overlap
        seq = fasta_file.fetch(chrom.name)[chrom.zoom_min:chrom.zoom_max].lower()
        for i in range(chrom.zoom_min, chrom.zoom_max, step):
            idx = i - chrom.zoom_min
            base_start.append(int(i + (step / 2)))  # use middle of window as x
            gc = seq[idx:idx + step].count("g") + seq[idx:idx + step].count("c")
            gcContent.append(gc / step * 100)
        return base_start, gcContent


class Canvas:
    def __init__(self, *args, **kwargs):

        self.kwargs = kwargs

        self.title = Utils.check_kwargs(self.kwargs,'title', str, '')
        self.height = Utils.check_kwargs(self.kwargs,'height', int, 10)
        self.width = Utils.check_kwargs(self.kwargs,'width', int, 10)
        self.background_color = Utils.check_kwargs(self.kwargs,'background_color', str, 'white')
        self.legend = Utils.check_kwargs(self.kwargs,'legend', bool, False)
        self.constrained_layout = Utils.check_kwargs(self.kwargs,'constrained_layout', bool, False)
        self.title_fontsize = Utils.check_kwargs(self.kwargs, 'title_fontsize', int, 20)


class Utils:

    @staticmethod
    def check_kwargs(kwargs, val, t, default):

        if val in kwargs and kwargs[val]:
            if t == int:
                return (int(kwargs[val]))
            if t == str:
                return (str(kwargs[val]))
            if t == float:
                return (float(kwargs[val]))
            if t == bool:
                if kwargs[val].lower() == "true":
                    return True
                if kwargs[val].lower() == "false":
                    return False
        else:
            return default
