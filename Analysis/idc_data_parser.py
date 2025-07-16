import adds
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class IDCDataParser:
    def __init__(self):
        # Load master DataFrame with dendrite scores and RGB values
        self.master = adds.get_master(dendrite_score_col=True)

    def plot_rgb_boxplots(self, show=True, save_path=None):
        """
        Plots boxplots of the difference in R, G, B values between exposed and pristine images, grouped by pattern.
        If save_path is provided, saves the plot to that path.
        If show is True, displays the plot.
        Returns the FacetGrid object.
        """
        df = self.master.copy()
        df["Red"] = df["R_EXPOSED"] - df["R_PRISTINE"]
        df["Green"] = df["G_EXPOSED"] - df["G_PRISTINE"]
        df["Blue"] = df["B_EXPOSED"] - df["B_PRISTINE"]

        # Convert to long for easy plotting
        df_long = pd.melt(
            df,
            id_vars=["Board ID", "Sensor", "Pattern"],
            value_vars=["Red", "Green", "Blue"],
            var_name="Channel",
            value_name="Channel Difference"
        )

        # Create a FacetGrid
        g = sns.FacetGrid(
            data=df_long,
            col="Channel",
            margin_titles=True,
            hue="Channel",
            palette={"Red": "#FF0000", "Green": "#00FF00", "Blue": "#0000FF"}
        )

        g.map_dataframe(
            sns.boxplot,
            x="Pattern", y="Channel Difference",
        )

        g.set_titles(col_template="{col_name}")
        g.set_xticklabels([1, 4, 7, 10])

        if save_path:
            plt.savefig(save_path)
        if show:
            plt.show()
        return g 