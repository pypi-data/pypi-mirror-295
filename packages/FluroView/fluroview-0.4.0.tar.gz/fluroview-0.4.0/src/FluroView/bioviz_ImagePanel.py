from bioviz_multichannel import*
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patheffects import withStroke
from matplotlib.patches import Rectangle
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.gridspec import GridSpec
import random 
import string

class ImagePanel:
    def __init__(self, rows, cols, margin=0.1, figscaling=5, figsize=None, 
                 title_size=0.05, title_space=0.1, **fig_kwargs):
        self.rows = rows
        self.cols = cols
        self.margin = margin
        self.figsize = figsize
        self.figscaling = figscaling
        self.title_size = title_size
        self.title_space = title_space
        self.fig_kwargs = fig_kwargs
        
        self.images = np.empty((rows, cols), dtype=object)
        self.construct_figure()
    
    def construct_figure(self):
        self.fig = plt.figure(figsize=self.figsize,frameon=False)
        self.gs = GridSpec(self.rows, self.cols, figure=self.fig,
                           left=0.05, right=0.95, bottom=0.05, top=0.90, 
                           wspace=self.margin, hspace=self.margin)
        self.axes = np.empty((self.rows, self.cols), dtype=object)
    
    def add_multichannel_image(self, row, col, image, title=None, panel_label=None,
                               scalebar=False, pixel_size=None, units='μm',
                               panel_label_color='white', panel_label_fontsize=14, 
                               scalebar_color='white', scalebar_fontsize=10,
                               show_frame=False, show_panel_label=True,
                               set_title_color_default=False):  # Added set_title_color_default parameter
        if row >= self.rows or col >= self.cols:
            raise ValueError("Row or column index out of range")
        
        ax = self.fig.add_subplot(self.gs[row, col])
        self.axes[row, col] = ax
        self.images[row, col] = image
        
        image.plot(ax=ax, rescale=True, show_labels=False)
        
        if show_panel_label:
            if panel_label is None:
                panel_label = string.ascii_uppercase[row * self.cols + col]
            ax.text(0.05, 0.95, panel_label, transform=ax.transAxes,
                    color=panel_label_color, fontsize=panel_label_fontsize,
                    va='top', ha='left', fontweight='bold')
        
        if scalebar and pixel_size is not None:
            scalebar = ScaleBar(pixel_size, units, 
                                color=scalebar_color, 
                                box_alpha=0,
                                location='lower right', 
                                font_properties={'size': scalebar_fontsize})
            ax.add_artist(scalebar)
        
        if not show_frame:
            ax.axis('off')
        else:
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_edgecolor(panel_label_color)
                spine.set_linewidth(1)
        
        if title is None:
            title = image.channel_names[0] if image.channel_names else f"Channel {row*self.cols+col+1}"
        
        if set_title_color_default:
            title_color = 'black'
        else:
            title_color = image.get_cmap(image.colormaps[0])(1.0)
        
        ax.set_title(title, color=title_color, fontsize=panel_label_fontsize, pad=10)
        
    def adjust_layout(self):
        if self.figsize is None:
            max_height = max(img.channels[0].shape[0] for img in self.images.ravel() if img is not None)
            max_width = max(img.channels[0].shape[1] for img in self.images.ravel() if img is not None)
            self.fig.set_size_inches(
                w=self.cols * max_width / max(max_height, max_width) * self.figscaling,
                h=(self.rows * max_height / max(max_height, max_width) + 0.5) * self.figscaling
            )
        
        self.fig.tight_layout(rect=[0, 0, 1, 0.95])
        
    def show(self):
        plt.show()
        
    def save(self, filename, dpi=300,format='png'):
        self.fig.savefig(filename, dpi=dpi, bbox_inches='tight', format=format)
