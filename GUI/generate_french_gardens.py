import french_gardens_utils
import plotting_utils
import poisson_disk.poisson_disc as poi

beta = 1
num_p_selector = poi.weighted_round_or_one
fill_final = False
data = None
save_plotly=False
show=False
save=True

bounds_map_creator_args = french_gardens_utils.french_demo_bac()

plotting_utils.generate_garden_scatter_and_area(beta, num_p_selector, bounds_map_creator_args, fill_final,
                                                data=data, save_plotly=save_plotly, show=show, save=save)