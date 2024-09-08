import numpy as np
import tifffile

def write_ome_tiff(data, channel_names, output_filename, pixel_size_x=1, pixel_size_y=1, physical_size_z=1, imagej=False, create_pyramid=True, compression='zlib', Unit='µm', downsample_count=4):
    """
    Write an array to an OME-TIFF file with optional pyramid creation.

    Parameters:
    data (numpy.ndarray): The image data (must be in ZCYX format).
    channel_names (list of str): Names of the channels.
    output_filename (str): Path to save the OME-TIFF file.
    pixel_size_x (float): Pixel size in the X dimension in microns.
    pixel_size_y (float): Pixel size in the Y dimension in microns.
    physical_size_z (float): Physical size in the Z dimension in microns (for 3D data).
    imagej (bool): Flag to use ImageJ compatibility mode.
    create_pyramid (bool): Flag to create a pyramid if the dimensions are suitable.
    compression (str): Compression method, defaults to 'zlib'.
    Unit (str): Unit for physical sizes, defaults to 'µm' (micrometers).
    downsample_count (int): Number of pyramid downsample levels, defaults to 4.
    """
    
    # Ensure the data is in ZCYX format (4D array: Z-slices, Channels, Y, X)
    if len(data.shape) != 4:
        raise ValueError(f"Input data must have 4 dimensions (ZCYX). Found {len(data.shape)} dimensions.")
    
    if data.shape[1] != len(channel_names):
        raise ValueError(f"Number of channels in the data ({data.shape[1]}) does not match the length of 'channel_names' ({len(channel_names)}).")

    # Handle unit conversion for ImageJ compatibility (ImageJ expects 'um' instead of 'µm')
    if Unit == 'µm' and imagej:
        Unit = 'um'

    # Handle 3D data (ZCYX format)
    if data.shape[0] > 1:
        print("Detected 3D data (multiple z-slices)")
        metadata = {
            'axes': 'ZCYX',
            'Channel': [{'Name': name, 'SamplesPerPixel': 1} for name in channel_names],
            'PhysicalSizeX': pixel_size_x,
            'PhysicalSizeXUnit': Unit,
            'PhysicalSizeY': pixel_size_y,
            'PhysicalSizeYUnit': Unit,
            'PhysicalSizeZ': physical_size_z,
            'PhysicalSizeZUnit': Unit,
            'Photometric': 'minisblack',
        }
        print(f"3D data shape: {data.shape}")
        
        # Handle pyramid creation
        if create_pyramid:
            print(f"Writing with pyramid, {downsample_count} downsample levels")
            with tifffile.TiffWriter(output_filename, bigtiff=True, imagej=imagej) as tif:
                tif.write(data, subifds=downsample_count, metadata=metadata, compression=compression)
                for level in range(1, downsample_count + 1):
                    data = data[:, :, ::2, ::2]  # Downsampling each level
                    tif.write(data, subfiletype=1, metadata=metadata, compression=compression)
        else:
            print("Writing without pyramid")
            with tifffile.TiffWriter(output_filename, bigtiff=True, imagej=imagej) as tif:
                tif.write(data, subifds=0, metadata=metadata, compression=compression)

    # Handle 2D data (CYX format)
    else:
        print("Detected 2D data (single z-slice with multiple channels)")
        metadata = {
            'axes': 'CYX',
            'Channel': [{'Name': name, 'SamplesPerPixel': 1} for name in channel_names],
            'PhysicalSizeX': pixel_size_x,
            'PhysicalSizeXUnit': Unit,
            'PhysicalSizeY': pixel_size_y,
            'PhysicalSizeYUnit': Unit,
            'Photometric': 'minisblack',
            'Planarconfig': 'separate',
        }
        
        # Remove the z-dimension (since it's a single z-slice)
        data = data[0, ...]  # Now data has shape (C, Y, X)
        print(f"2D data shape: {data.shape}")

        # Handle pyramid creation
        if create_pyramid:
            print(f"Writing with pyramid, {downsample_count} downsample levels")
            with tifffile.TiffWriter(output_filename, bigtiff=True, imagej=imagej) as tif:
                tif.write(data, subifds=downsample_count, metadata=metadata, compression=compression)
                for level in range(1, downsample_count + 1):
                    data = data[:, ::2, ::2]  # Downsampling each level
                    tif.write(data, subfiletype=1, metadata=metadata, compression=compression)
        else:
            print("Writing without pyramid")
            with tifffile.TiffWriter(output_filename, bigtiff=True, imagej=imagej) as tif:
                tif.write(data, subifds=0, metadata=metadata, compression=compression)

    print(f"OME-TIFF file written successfully: {output_filename}")
