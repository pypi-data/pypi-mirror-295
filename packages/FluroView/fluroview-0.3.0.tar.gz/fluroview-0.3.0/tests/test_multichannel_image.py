import numpy as np 
import pytest
from BioViz import MultiChannelImage

def test_multichannel_image_creation():
    channels = [np.random.rand(10, 10) for _ in range(3)]
    image = MultiChannelImage(channels, channel_names=['R', 'G', 'B'])
    assert len(image.channels) == 3
    assert image.channel_names == ['R', 'G', 'B']

def test_multichannel_image_composite():
    channels = [np.ones((10, 10)) * i for i in range(3)]
    image = MultiChannelImage(channels, colormaps=['red', 'green', 'blue'])
    composite = image.composite()
    assert composite.shape == (10, 10, 3)
    assert np.allclose(composite[:,:,0], 1)  # Red channel should be full
    assert np.allclose(composite[:,:,1], 0.5)  # Green channel should be half
    assert np.allclose(composite[:,:,2], 0)  # Blue channel should be empty

def test_hex_to_cmap():
    hex_color = '#FF0000'  # Pure red
    cmap = MultiChannelImage.hex_to_cmap(hex_color)
    assert np.allclose(cmap(1.0)[:3], [1, 0, 0])  # Should be pure red at the top end