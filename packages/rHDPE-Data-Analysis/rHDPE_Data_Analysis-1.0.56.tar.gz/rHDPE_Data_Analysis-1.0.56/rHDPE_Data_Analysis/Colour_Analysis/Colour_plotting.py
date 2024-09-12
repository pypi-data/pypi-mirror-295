# Imports.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .. import Global_Utilities as gu

# Function definitions.

def plot_data( directory, output_directory, file_data, data, savefig = True ):

    resin_data = gu.get_list_of_resins_data( directory )

    feature_names, features = gu.csv_to_df_to_array_and_column_titles( output_directory + "Colour/Features/Features.csv" )

    sample, sample_array, samples_present, samples_present_array = gu.sample_data_from_file_data( file_data )

    sample_mask = [11, 14, 10, 4, 13, 21, 23, 18, 22, 20, 2, 3, 17, 16, 19, 1, 15, 12, 6, 5, 7, 9, 8, 24]

    sample_mask = gu.remove_redundant_samples( sample_mask, samples_present )

    specimens = False
    mean = True

    if specimens:

        ab_euclidean = np.sqrt( features[:, 1] * features[:, 1] + features[:, 2] * features[:, 2] )

        gu.plot_scatterplot_of_two_features( ab_euclidean, features[:, 0], sample_array, [f[2] for f in file_data], line_of_best_fit = False, xlabel = "sqrt(a*^2 + b*^2)", ylabel = "L*", savefig = savefig, filename = output_directory + "Colour/Plots/L_vs_Colour.pdf" )

        gu.plot_scatterplot_of_three_features( features[:, 1], features[:, 2], features[:, 0], sample_array, [f[2] for f in file_data], title = "", xlabel = "a*", ylabel = "b*", zlabel = "L*", savefig = savefig, filename = output_directory + "Colour/Plots/3D.pdf" )

    if mean:

        resin_colours = pd.read_csv( output_directory + "Colour/Sandbox/rgb_colours.csv", header = None )

        resin_colours[0] = resin_colours[0].astype( int )

        resin_colours.index = resin_colours[0]

        resin_colours.drop( columns = [0], inplace = True )

        resin_colours_list = [[resin_colours.loc[s, 1] / 255, resin_colours.loc[s, 2] / 255, resin_colours.loc[s, 3] / 255] for s in sample_mask]

        mean_features = gu.extract_mean_features( features, sample_array, sample_mask )

        std_of_features = gu.extract_std_of_features( features, sample_array, sample_mask )

        ab_euclidean = np.sqrt( features[:, 1] * features[:, 1] + features[:, 2] * features[:, 2] )

        ab_euclidean_mean = gu.extract_mean_features( ab_euclidean[:, np.newaxis], sample_array, sample_mask )

        ab_euclidean_std = gu.extract_std_of_features( ab_euclidean[:, np.newaxis], sample_array, sample_mask )

        # gu.plot_scatterplot_of_two_features( ab_euclidean_mean[:, 0], mean_features[:, 0], sample_mask, [resin_data.loc[i]["Label"] for i in sample_mask], errorbars = True, std = [ab_euclidean_std[:, 0], std_of_features[:, 0]], line_of_best_fit = False, xlabel = "sqrt(a*^2 + b*^2)", ylabel = "L*", savefig = savefig, filename = output_directory + "Colour/Plots/L_vs_Colour.pdf" )

        gu.plot_scatterplot_of_two_features( mean_features[:, 1], mean_features[:, 0], resin_colours_list, [resin_data.loc[i]["Label"] for i in sample_mask], line_of_best_fit = False, xlabel = "a*", ylabel = "L*", savefig = savefig, filename = output_directory + "Colour/Plots/L_vs_a.pdf" )

        gu.plot_scatterplot_of_two_features( mean_features[:, 2], mean_features[:, 0], resin_colours_list, [resin_data.loc[i]["Label"] for i in sample_mask], line_of_best_fit = False, xlabel = "b*", ylabel = "L*", savefig = savefig, filename = output_directory + "Colour/Plots/L_vs_b.pdf" )

        gu.plot_scatterplot_of_three_features( mean_features[:, 1], mean_features[:, 2], mean_features[:, 0], sample_mask, [resin_data.loc[i]["Label"] for i in sample_mask], title = "", xlabel = "a*", ylabel = "b*", zlabel = "L*", savefig = savefig, filename = output_directory + "Colour/Plots/3D.pdf" )
