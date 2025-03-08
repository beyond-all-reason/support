5.3. 2025

Sorry for the messy .blend file! 
Tested to work with Blender 4.4
Originally made with Blender 3.3 in 2022

How it works, is that you render out the image, and then the compositor does some magic and outputs 3 different image files out. File locations are specified inside the compositor, File Output node.

Compositor Magic: 

It utilizes Blender's shader AOV system to separate roughness, metalness, normalmap, emission and TeamColor from the render. All the shaders in the scene have an AOV output to make this possible.

After the render, the compositor combines Roughness, Metalness and Emission as the blue, green and red channels into an image and saves it as "cor_other0001.png"
Normalmap as "cor_normal0001.png"
Color render as "cor_color0001.exr"

The comp also adds a specific color swatch palette image on top of the "color" and "other" images, which will be used in various stuff by the game.

The ONLY way I could get the "color"s alpha channel to work is by outputting it as an .exr image file. However, that will not convert without issues into a .dds so you must open it in Gimp, then save as a tga and then do the .dds process.

After you have converted the cor_other, cor_normal and cor_color into .dds -files the game can understand, the process is completed.

-Zagupi