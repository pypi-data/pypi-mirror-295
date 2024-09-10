import argparse
from toorajd._plot import Plot as Plot


def main():
    parser = argparse.ArgumentParser(description="Create a Tooraj-Approved plot.")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(
        dest="plot_type", required=True, help="The type of plot to create."
    )
    manhattan_parser = subparsers.add_parser(
        "manhattan", help="Create a Manhattan plot."
    )
    manhattan_parser.add_argument(
        "data", type=str, help="The path to the data that will be used for plotting"
    )
    manhattan_parser.add_argument(
        "study_type",
        type=str,
        help='The type of study that was conducted. Can be any value in ["gwas", "burden", "phewas"]',
    )
    manhattan_parser.add_argument(
        "-s",
        "--sep",
        type=str,
        default=" ",
        help='The field delimeter for the data if it is a file that will be read. Will automatically read parquet files. Default = " "',
    )
    manhattan_parser.add_argument(
        "--title", type=str, default=None, help="The title of the plot. Default = None."
    )
    manhattan_parser.add_argument(
        "--chrom",
        type=str,
        default="CHROM",
        help='The name of the column in the data that contains the chromosome number. Default = "CHROM".',
    )
    manhattan_parser.add_argument(
        "--pos",
        type=str,
        default="GENPOS",
        help='The name of the column in the data that contains the genomic position information. Default = "GENPOS".',
    )
    manhattan_parser.add_argument(
        "--var_id",
        type=str,
        default="ID",
        help='The name of the column in the data that contains the variant ID information. Assumes CHROM:POS:REF:ALT format. Default = "ID".',
    )

    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
