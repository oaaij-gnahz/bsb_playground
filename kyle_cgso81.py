"""
Kyle Hendricks complete game shutout on 81 pitches, May 3, 2019
"""

#%% 
import os
import pybaseball
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# import matplotlib.cm as cm

csv_path = "data_kyle_cgso81.csv"
if os.path.exists(csv_path):
    data = pd.read_csv(csv_path)
else:
    player_df = playerid_lookup("hendricks", "kyle")
    player_id = player_df['key_mlbam'].values[0]
    data = statcast_pitcher("2019-05-03", "2019-05-03", player_id=player_id)
    data.to_csv(csv_path)
#%%
# axis: X: horizontal (pitcher to his right), Y: depth (plate to mound), Z: vertical (how much above ground)
release_pos = data[['release_pos_x', 'release_pos_y', 'release_pos_z']]
pitch_types = data['pitch_type']
sz_bot = data['sz_bot']
sz_top = data['sz_top']

#%% plot release location vs. pitch type
# plot realse positions in 3d pitch by pitch, color by pitch type
# overlaied with zone top and bottom
pitch_types_cat = pitch_types.astype('category')
pitch_type_codes = pitch_types_cat.cat.codes.to_numpy()
pitch_type_labels = pitch_types_cat.cat.categories
print(pitch_type_codes)
num_categories = len(pitch_type_labels)
# print(num_categories)
# print(labels)
# uniq_codes, uniq_inds = np.unique(codes, return_index=True)
# print(uniq_codes) # starts from 0
# uniq_labels = labels[uniq_inds]
cmap = plt.get_cmap('tab10')
# norm = matplotlib.colors.Normalize(vmin=0, vmax=num_categories - 1)
norm = matplotlib.colors.BoundaryNorm(boundaries=np.arange(num_categories + 1) - 0.5, ncolors=num_categories)
# colors = cmap.colors
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(
    xs=release_pos['release_pos_x'],
    ys=release_pos['release_pos_y'],
    zs=release_pos['release_pos_z'],
    c=pitch_type_codes,
    alpha=1, cmap=cmap, norm=norm, s=10)
ax.set_xlabel('Release Position X')
ax.set_ylabel('Release Position Y')
ax.set_zlabel('Release Position Z')
ax.set_title('Kyle Hendricks Release Position on May 3, 2019')

# plot zone top and bottom
# for i in range(len(sz_top)):
#     ax.plot([0, 0], [sz_bot[i], sz_top[i]], [0, 0], color='k', alpha=0.5)
# legend
legend_elements = [
    plt.Line2D([0], [0], marker='o', label=label,
               color=cmap(code), markersize=10)
    for code, label in enumerate(pitch_type_labels)
]
ax.legend(handles=legend_elements, title="Pitch Type")
ax.view_init(elev=0, azim=-90)
plt.savefig("release_pos.png", dpi=300)
plt.close()
#%% release velocity for each pitch type
release_velos = data[["vx0", "vy0", "vz0"]].to_numpy()
hist_bin_edges = [np.histogram_bin_edges(release_velos[:, i], bins=5) for i in range(3)]
fig = plt.figure(figsize=(10, 10))
axes = fig.subplots(num_categories, 3, sharex="col", sharey=True)
for i_pitch in range(num_categories):
    pitch_type_str = pitch_type_labels[i_pitch]
    axes[i_pitch, 0].set_ylabel(pitch_type_str)
    for j_axis in range(3):
        ax = axes[i_pitch, j_axis]
        ax.hist(release_velos[pitch_type_codes == i_pitch, j_axis], bins=hist_bin_edges[j_axis], color=cmap(i_pitch))
        ax.set_xlim(hist_bin_edges[j_axis][0], hist_bin_edges[j_axis][-1])
        # if i_pitch != num_categories - 1:
        #     ax.set_xticklabels([])
axes[num_categories-1, 0].set_xlabel('Release Velocity X')
axes[num_categories-1, 1].set_xlabel('Release Velocity Y')
axes[num_categories-1, 2].set_xlabel('Release Velocity Z')
fig.suptitle('Release Velocity by Pitch Type')
fig.tight_layout()
fig.savefig("release_velo_hist_by_pitchtype.png", dpi=300)
plt.close()
#%% release velocity
release_velocities = data.groupby('pitch_type').agg({'vx0': ['mean', 'std'], 'vy0': ['mean', 'std'], 'vz0': ['mean', 'std'], "release_spin_rate": ['mean', 'std']})
print("Aggregated Release Velocities by Pitch Type")
print(release_velocities)
#%% release 