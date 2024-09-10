import numpy as np
import pytest
from BioViz import ImagePanel
from BioViz import MultiChannelImage

def test_image_panel_creation():
    panel = ImagePanel(rows=2, cols=2)
    assert panel.rows == 2
    assert panel.cols == 2
    assert panel.images.shape == (2, 2)

def test_add_multichannel_image():
    panel = ImagePanel(rows=1, cols=1)
    channels = [np.random.rand(10, 10)]
    image = MultiChannelImage(channels)
    panel.add_multichannel_image(0, 0, image, title='Test')
    assert panel.images[0, 0] is not None
    assert panel.axes[0, 0] is not None