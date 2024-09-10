import numpy as np
from pandas import DataFrame
import polars as pl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns

from toorajd._plot import Plot


# These are all genetics-specific constants that are used in the Manhattan plot.
CUMULATIVE_LEN_Y = 57227415 + 3031042417
CUMULATIVE_CHROM_LENS = {
    1: 0,
    2: 248956422,
    3: 491149951,
    4: 689445510,
    5: 879660065,
    6: 1061198324,
    7: 1232004303,
    8: 1391350276,
    9: 1536488912,
    10: 1674883629,
    11: 1808681051,
    12: 1943767673,
    13: 2077042982,
    14: 2191407310,
    15: 2298451028,
    16: 2400442217,
    17: 2490780562,
    18: 2574038003,
    19: 2654411288,
    20: 2713028904,
    21: 2777473071,
    22: 2824183054,
    23: 2875001522,
    24: 3031042417,
    25: CUMULATIVE_LEN_Y,
}

CHROM_MIDPOINTS = {
    i: (CUMULATIVE_CHROM_LENS[i] + CUMULATIVE_CHROM_LENS[i + 1]) // 2
    for i in range(1, 25)
}

TOTAL_PLOT_POINTS = 1_500_000


class Manhattan(Plot):
    """A class for creating Manhattan plots. Inherits from Plot. Assumes you've used `regenie` for GWAS.
    :param data: the data that will be used for plotting. Can be a path or polars/pandas dataframe.
    :param study_type: The type of study that was conducted. Can be any value in ['gwas', 'burden', 'phewas'].
    :param sep: the field delimeter for the data if it is a file that will be read. Will automatically read parquet files. Default = ' '.
    :param **kwargs: any additional keywords to be passed to pl.read_csv()
    """

    def __init__(
        self,
        data: str | pl.DataFrame | DataFrame,
        study_type: str,
        sep: str = " ",
        **kwargs,
    ) -> None:
        super().__init__(data, sep, **kwargs)
        self._check_study_type(study_type)

    def _check_study_type(self, study_type: str) -> None:
        if study_type not in ["gwas", "burden", "phewas"]:
            raise ValueError(
                f"Study type not supported: {study_type}. Please provide a valid study type ['gwas', 'burden', 'phewas']."
            )
        self.study_type = study_type

    def plot(
        self,
        title: str = None,
        chrom: str = "CHROM",
        pos: str = "GENPOS",
        var_id: str = "ID",
        logp: str = "LOG10P",
        is_logp: bool = True,
        suggestive_line: float = 5e-8,
        remove_y_chrom: bool = False,
        split_id: bool = True,
        id_delim: str = ":",
        palette: str = "tab20",
        **kwargs,
    ):
        """Plot a manhattan plot. Can accept any keyword arguments used by seaborn.relplot
        :param title: the title of the plot. Default = None.
        :param chrom: the name of the column in the data that contains the chromosome information. Default = 'CHROM'.
        :param pos: the name of the column in the data that contains the genomic position information. Default = 'GENPOS'.
        :param var_id: the name of the column in the data that contains the variant ID information. Assumes CHROM:POS:REF:ALT format. Default = 'ID'.
        :param logp: the name of the column in the data that contains the -log10(p) information. Default = 'LOG10P'.
        :param is_logp: whether or not the p-values are already log transformed. Default = True.
        :param suggestive_line: the p-value threshold for suggestive significance. Default = 5e-8.
        :param remove_y_chrom: whether or not to remove the Y chromosome from the plot. Default = False.
        :param split_id: whether or not to split the variant ID into chromosomes. Useful if Y-chromosome variants were used in analysis. Default = True.
        :param id_delim: the delimiter to use when splitting the variant ID. Default = ':'.
        :param palette: the color palette to use for the plot. Default = 'tab20'.
        """
        if self.study_type == "gwas":
            self._plot_gwas(
                title,
                chrom,
                pos,
                var_id,
                logp,
                is_logp,
                suggestive_line,
                remove_y_chrom,
                split_id,
                id_delim,
                palette,
                **kwargs,
            )
        elif self.study_type == "burden":
            pass
        elif self.study_type == "phewas":
            pass

    def _plot_gwas(
        self,
        title,
        chrom,
        pos,
        var_id,
        logp,
        is_logp,
        suggestive_line,
        remove_y_chrom,
        split_id,
        id_delim,
        palette,
        **kwargs,
    ):
        plot_data = self.data
        if split_id:  # Split variant ID into chromosome column
            plot_data = plot_data.with_columns(
                [
                    pl.col(var_id)
                    .str.split(id_delim)
                    .list[0]
                    .str.replace("chr", "")
                    .replace({"X": "23", "Y": "24"})
                    .cast(pl.UInt8)
                    .alias(chrom),
                ]
            )
        plot_data = (
            plot_data.with_columns(
                [
                    pl.col(chrom)
                    .cast(pl.String)
                    .replace({"23": "X", "24": "Y"})
                    .alias("chrom_str"),
                    pl.col(chrom)
                    .cast(pl.Int64)
                    .replace(CUMULATIVE_CHROM_LENS)
                    .alias("chrom_max_bp"),
                ]
            )
            .with_columns([(pl.col(pos) + pl.col("chrom_max_bp")).alias("cum_pos")])
            .with_columns(
                [(pl.col("cum_pos") - pl.col("cum_pos").min()).alias("plotting_index")]
            )
        )
        if remove_y_chrom:
            plot_data = plot_data.filter(pl.col("chrom_str") != "Y")
        if not is_logp:
            plot_data = plot_data.with_columns([(-np.log10(pl.col(logp))).alias(logp)])
        plot_data = plot_data.sort("plotting_index").with_row_index()
        # Set up the plot
        # Split the xticks and xlabels based on the results
        unique_chroms = plot_data[chrom].unique()
        xticks = sorted([CHROM_MIDPOINTS[val] for val in unique_chroms])
        xlabels = [str(x).replace("23", "X").replace("24", "Y") for x in unique_chroms]
        # Split the data into significant and insignificant points
        sig_thresh = 1.5
        sig_data = plot_data.filter(pl.col(logp) >= sig_thresh)
        nonsig_data = plot_data.filter(pl.col(logp) < sig_thresh)
        # Set the target number of points to extract from non-significant data
        target_points = TOTAL_PLOT_POINTS - len(sig_data)
        points_per_chrom = target_points // nonsig_data[chrom].n_unique()
        sampled_nonsig = self._sample_nonsig_data(nonsig_data, chrom, points_per_chrom)
        result_data = pl.concat([sig_data, sampled_nonsig]).sort("plotting_index")
        # Plot
        base_args = {"aspect": 3, "linewidth": 0, "s": 3, "legend": None}
        base_args.update(kwargs)
        fig = sns.relplot(
            data=result_data,
            x="plotting_index",
            y=logp,
            hue=chrom,
            palette=sns.color_palette(palette),
            **base_args,
        )
        if title is not None:
            plt.title(title)
        plt.xticks(ticks=xticks, labels=xlabels)
        plt.xlabel("Chromosome")
        plt.ylabel("-log10(p)")
        plt.axhline(
            y=-np.log10(suggestive_line), color="red", linestyle="--", linewidth=1
        )
        self.figure = fig
        plt.show()

    def show(self) -> Figure:
        """Show the plot."""
        fig = self.figure.figure
        return fig

    def save(self, path: str, **kwargs) -> None:
        """Save the plot to a file.
        :param path: the path to save the plot to.
        :param **kwargs: any additional keyword arguments to be passed to plt.savefig().
        Default savefig arguments are dpi=300, bbox_inches='tight', and facecolor='w'.
        """
        base_args = {"dpi": 300, "bbox_inches": "tight", "facecolor": "w"}
        base_args.update(kwargs)
        self.figure.savefig(path, **base_args)

    @staticmethod
    def _sample_nonsig_data(nonsig_data, chrom_col, points_per_chrom):
        sampled_nonsig = pl.DataFrame()
        for chrom, data in nonsig_data.group_by(chrom_col):
            min_idx, max_idx = data["index"].min(), data["index"].max()
            select_indexes = np.linspace(
                min_idx, max_idx, points_per_chrom, dtype=np.int64
            )
            sampled_data = data.filter(pl.col("index").is_in(select_indexes))
            sampled_nonsig = pl.concat([sampled_nonsig, sampled_data])
        return sampled_nonsig
