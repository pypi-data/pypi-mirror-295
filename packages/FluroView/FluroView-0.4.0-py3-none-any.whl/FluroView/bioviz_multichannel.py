import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Colormap, hex2color
from matplotlib.patheffects import withStroke
from matplotlib.patches import Rectangle
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.gridspec import GridSpec
import random 
import string

# Define custom colormaps
num_colors = 256
pure_red = ListedColormap(np.c_[np.linspace(0,1,num_colors), np.zeros(num_colors), np.zeros(num_colors)])
pure_green = ListedColormap(np.c_[np.zeros(num_colors), np.linspace(0,1,num_colors), np.zeros(num_colors)])
pure_blue = ListedColormap(np.c_[np.zeros(num_colors), np.zeros(num_colors), np.linspace(0,1,num_colors)])
pure_cyan = ListedColormap(np.c_[np.zeros(num_colors), np.linspace(0,1,num_colors), np.linspace(0,1,num_colors)])
pure_magenta = ListedColormap(np.c_[np.linspace(0,1,num_colors), np.zeros(num_colors), np.linspace(0,1,num_colors)])
pure_yellow = ListedColormap(np.c_[np.linspace(0,1,num_colors), np.linspace(0,1,num_colors), np.zeros(num_colors)])

class MultiChannelImage:
    custom_cmaps = {
        'pure_red': ListedColormap(np.c_[np.linspace(0,1,256), np.zeros(256), np.zeros(256)]),
        'pure_green': ListedColormap(np.c_[np.zeros(256), np.linspace(0,1,256), np.zeros(256)]),
        'pure_blue': ListedColormap(np.c_[np.zeros(256), np.zeros(256), np.linspace(0,1,256)]),
        'pure_cyan': ListedColormap(np.c_[np.zeros(256), np.linspace(0,1,256), np.linspace(0,1,256)]),
        'pure_magenta': ListedColormap(np.c_[np.linspace(0,1,256), np.zeros(256), np.linspace(0,1,256)]),
        'pure_yellow': ListedColormap(np.c_[np.linspace(0,1,256), np.linspace(0,1,256), np.zeros(256)])
    }

    def __init__(self, channels, channel_names=None, colormaps=None, random_colors=False):
        self.channels = channels if isinstance(channels, list) else [channels]
        self.channel_names = channel_names or [f"Channel {i+1}" for i in range(len(self.channels))]
        
        if random_colors:
            self.colormaps = self.generate_unique_colormaps(len(self.channels))
        elif colormaps is None:
            self.colormaps = ['viridis'] * len(self.channels)
        else:
            self.colormaps = colormaps if isinstance(colormaps, list) else [colormaps]
    @classmethod
    def get_cmap(cls, cmap):
        if isinstance(cmap, str):
            if cmap.startswith('#'):  # It's a hex color
                return cls.hex_to_cmap(cmap)
            elif cmap in cls.custom_cmaps:
                return cls.custom_cmaps[cmap]
            return plt.get_cmap(cmap)
        elif isinstance(cmap, (ListedColormap, Colormap)):
            return cmap
        else:
            raise ValueError("Unsupported colormap type. Use a string name of a matplotlib colormap, "
                             "a custom colormap name, a hex color code, or a Colormap object.")
    @staticmethod
    def hex_to_cmap(hex_color):
        """Convert a hex color to a colormap that goes from black to the specified color."""
        rgb_color = hex2color(hex_color)
        return ListedColormap(np.array([np.linspace(0, c, 256) for c in rgb_color]).T)
    
    def apply_colormap(self, channel_index=0, cmap=None):
        """
        Apply a colormap to a grayscale image.
        
        Parameters:
        channel_index (int): Index of the channel to apply the colormap to.
        cmap: Colormap to apply. If None, uses the colormap specified for this channel.
        
        Returns:
        numpy.ndarray: RGB image after applying the colormap.
        """
        if cmap is None:
            cmap = self.colormaps[channel_index]
        
        cmap_func = self.get_cmap(cmap)
        normalized_image = self.rescale_intensity(self.channels[channel_index])
        return cmap_func(normalized_image)[:, :, :3]

    def composite(self, selected_channels=None, rescale=True):
        if selected_channels is None:
            selected_channels = range(len(self.channels))
        
        # Determine the shape of the output composite
        sample_channel = self.channels[0]
        if sample_channel.ndim == 2:
            composite_shape = (*sample_channel.shape, 3)
        elif sample_channel.ndim == 3 and sample_channel.shape[2] == 3:
            composite_shape = sample_channel.shape
        else:
            raise ValueError("Unsupported channel format. Expected 2D array or 3D array with 3 color channels.")
        
        composite = np.zeros(composite_shape)
        
        for i, channel in enumerate(selected_channels):
            cmap = self.get_cmap(self.colormaps[channel])
            
            if rescale:
                channel_data = self.rescale_intensity(self.channels[channel])
            else:
                channel_data = self.channels[channel]
            
            if channel_data.ndim == 2:
                # For 2D grayscale images
                colored_channel = cmap(channel_data)[:,:,:3]
            elif channel_data.ndim == 3 and channel_data.shape[2] == 3:
                # For 3D RGB images
                colored_channel = channel_data
            else:
                raise ValueError(f"Unsupported channel format for channel {channel}.")
            
            composite += colored_channel
        
        return np.clip(composite, 0, 1)

    @staticmethod
    def rescale_intensity(image, in_range='image'):
        if in_range == 'image':
            imin, imax = np.min(image), np.max(image)
        else:
            imin, imax = in_range
        out = np.clip(image, imin, imax)
        return (out - imin) / (imax - imin)

    def plot(self, ax=None, selected_channels=None, show_labels=True, rescale=True, 
             label_position='top-left', label_color='white', label_font_size=10):
        if ax is None:
            _, ax = plt.subplots()
        
        composite = self.composite(selected_channels, rescale=rescale)
        ax.imshow(composite)
        
        if show_labels:
            if label_position == 'top-left':
                x, y = 0.05, 0.95
                va, ha = 'top', 'left'
                dy = -0.05
            elif label_position == 'top-right':
                x, y = 0.95, 0.95
                va, ha = 'top', 'right'
                dy = -0.05
            elif label_position == 'bottom-left':
                x, y = 0.05, 0.05
                va, ha = 'bottom', 'left'
                dy = 0.05
            elif label_position == 'bottom-right':
                x, y = 0.95, 0.05
                va, ha = 'bottom', 'right'
                dy = 0.05
            else:
                raise ValueError("Unsupported label position")

            for i, name in enumerate(self.channel_names):
                cmap = self.get_cmap(self.colormaps[i])
                color = cmap(1.0)
                ax.text(x, y + i*dy, name, color=color, 
                        transform=ax.transAxes, va=va, ha=ha, fontsize=label_font_size)
        
        ax.axis('off')
        return ax
    
    @staticmethod
    def add_panel_label(ax, label, position='upper left', fontsize=14, color='white', pad=0.05):
        """Add a panel label (A, B, C, etc.) to the axes."""
        if position == 'upper left':
            x, y = pad, 1 - pad
            ha, va = 'left', 'top'
        elif position == 'upper right':
            x, y = 1 - pad, 1 - pad
            ha, va = 'right', 'top'
        else:
            raise ValueError("Unsupported position")

        ax.text(x, y, label, fontsize=fontsize, color=color,
                transform=ax.transAxes, ha=ha, va=va, fontweight='bold')
    
    @staticmethod
    def add_scalebar(ax, pixel_size, units='μm', color='white', position='lower right', 
                 font_size=10, scale_loc=None, box_alpha=0):
        """Add a scalebar to the axes using matplotlib-scalebar."""
        if scale_loc is None:
            scale_loc = position
        scalebar = ScaleBar(pixel_size, units, 
                            color=color, 
                            box_alpha=box_alpha,
                            location=scale_loc, 
                            font_properties={'size': font_size})
        ax.add_artist(scalebar)
    
    def create_multichannel_figure(image, pixel_size, units='μm', panel_label='A', rescale=True, 
                               label_position='top-left', label_color='white', 
                               channel_label_show=True, scalebar_color='white', 
                               scalebar_font_size=10, panel_label_color='white',
                               panel_label_font_size=14, channel_label_font_size=10,
                               scalebar_position='lower right', panel_label_position='upper left',
                               figsize=(6, 6), scalebar_box_alpha=0):
        
        fig, ax = plt.subplots(figsize=figsize,frameon=False)
        image.plot(ax=ax, rescale=rescale, label_position=label_position, 
               show_labels=channel_label_show, label_color=label_color,
               label_font_size=channel_label_font_size)
    
        image.add_panel_label(ax, panel_label, position=panel_label_position, 
                          fontsize=panel_label_font_size, color=panel_label_color)
        
        # Add scalebar
        image.add_scalebar(ax, pixel_size, units=units, color=scalebar_color, 
                      position=scalebar_position, font_size=scalebar_font_size, 
                      box_alpha=scalebar_box_alpha)
        
        plt.tight_layout()
        return fig, ax
