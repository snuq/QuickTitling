NOTE THAT THE 2.8 BRANCH IS NOT WORKING YET

# QuickTitling Addon For Blender

This addon will create and edit simple scenes for title overlays.  

Watch the demo video showing some features:  
[![Demo Video](https://img.youtube.com/vi/d3RPO53RBBw/0.jpg)](https://www.youtube.com/watch?v=d3RPO53RBBw)

Watch the tutorial video showing how to make a title:  
[![Tutorial Video](https://img.youtube.com/vi/_wM1iMVHkaI/0.jpg)](https://www.youtube.com/watch?v=_wM1iMVHkaI)

Development for this script is supported by my multimedia and video production business, [Creative Life Productions](http://www.creativelifeproductions.com)  
But, time spent working on this addon is time I cannot spend earning a living, so if you find this addon useful, consider donating:  

PayPal | Bitcoin
------ | -------
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=XHRXZBQ3LGLH6) | ![Bitcoin Donate QR Code](http://www.snuq.com/snu-bitcoin-address.png) <br> 1JnX9ZFsvUaMp13YiQgr9V36EbTE2SA8tz  

Or support me by hiring Creative Life Productions if you have a need for the services provided.


## Installation
* Download the release or master zip file to a location you can find easily.  
* Open Blender, and from the 'File' menu, select 'User Preferences'.
* In this new window, click on the "Add-ons" tab at the top.
* Click the 'Install Add-on from File...' button at the bottom of this window.
* Browse to and select the zip file you downloaded, click the 'Install Add-on from File' button.
* You should now see the addon displayed in the preferences window, click the checkbox next to the name to enable it.
* Click the 'Save User Settings' button to ensure this addon is loaded next time Blender starts.
* Once installed, the interface can be found in the sequence editor properties panel.  


## Title Editing
When a created QuickTitle is selected, the settings can be adjusted and will be shown in real-time.  It is recommended to enable OpenGL preview in the sequencer preview area to keep editing quick.  

Select a title in the VSE to edit it, or select no titles to edit new presets, or create new titles.  

Titles can be edited from the sequencer preview window, or from the QuickTitling panel

You can add a new title from a built-in or custom preset directly in the sequencer by pressing 'Shift-T' and selecting a preset. This will overwrite the current selected preset, and create a new title at the cursor location.  
This menu will also appear as a 'QuickTitle' sub-menu in the default sequencer strip add menu.  


The QuickTitling panel is divided into two sections:
* The top lets you select or import presets, create titles, and update the selected title.
   * Select Preset Menu

      Displays the internal presets, and all presets you have created in the current scene.  
      Click on a preset name to load it into the preset editor.  
      This menu will not be displayed when editing a title to prevent accidental overwrite.  
      Custom presets will have a 'X' button next to them in the menu, click this to delete the preset.  

   * Import Preset Button

      Opens a file dialog to browse to a saved xml preset file.  
      When opened, the preset will be loaded into the preset editor, it must be saved after this.  
      This will not be displayed when editing a title to prevent accidental overwrite.

   * Create New Title Button

      This will use the settings in the preset editor to create a new title in the VSE.  
      This will not be displayed when editing a title.

   * Render To Image Button
   
      This will create a static image of the currently selected title, you will be prompted for a location to save the image.  
      The original title will be muted, but unchanged, the image will be placed over it.  
      This is useful for speeding up the timeline when using static (non-animated) titles.  

   * Update Title Button
   
      This will force a manual update of all objects in the selected title.  
      Use this to fix anything that might be displaying improperly, or when not using auto-update mode.
      
   * Auto-Update Titles Checkbox
   
      When activated, the title will be automatically updated when any settings are changed in the interface.  
      Disable this if you wish to make several changes without slowing Blender down, or if you wish to make manual changes to the title scene.  

* The bottom section is an editor for the currently selected preset, or title.

   * Save To Custom Titles Button
   
      Only activated if the current title or preset is modified.  
      This will save the current title preset settings to the scene custom titles under the preset name.  
      WARNING: This will automatically overwrite a custom title that already exists with the same name!  
      Use this while editing a title to copy the preset back to the scene presets, so direct copies of the current title can be created.

   * Export Button
      
      Allows you to export your title preset to an xml file to share with others, or save for later.  
      If you are exporting an existing title, a preview image will be generated in the same folder as the xml.  
      Export to the script preset folder (<Blender's addon script folder>/QuickTitling/QuickTitling Presets) to have your title show up in the built-in titles.  
      
   * Preset Name
   
      Give your preset a name here, this is what it will show up as in the preset menu when you save it, and it will define the name of the title scene.  
      
   * Description
   
      Write some information about your title here.

   * Scene Length
   
      Frame length of the title scene.  
      When editing a title, this will change the length of the sequence in the timeline.  
      Do not change the length of the title by other means, or animations may be broken.  
      
   * Z Depth Scale
   
      Determines how far apart title objects are in 3d space.  
      If thick objects are colliding with each other, increase this value to spread them out.  
      Note that changing this value will affect the shadows, larger values will result in larger and softer shadows.  

   * Objects List
   
      A list of objects in this title are displayed here.  
      The list order determines how close objects are to the camera. Objects higher in the list will be placed in front of objects lower in the list.  
      Use the arrows on the right to change the object order.  
      Click the 'X' button next to an object to delete it.  
      Click on an object to select it, and edit it in the settings below.  
      
   * Add Buttons
   
      Use these buttons to add new objects of the basic types.  
      New objects will be placed at the top of the list.  
    
   * Object Editor
   
      Different object types have different features.  
      
      ### General Settings
      
      * Object Name
      
         Used to identify the object in the list.  
         
      * Text (Only For Text Objects)
      
         The text to be displayed by this object.  
         You can add multiple lines of text using new line characters '\n'.  
         Note that if you wish to put a backslash in the text, you must use two '\\'.  
      
      * Font Menu (Only For Text Objects)
      
         A drop-down menu showing all the loaded fonts in the blend file.  
         Load additional fonts using the '+' button.  
         
      * Wrapping Checkbox (Only For Text Objects)
      
         Enable word-wrapping on this text object.  Use this to keep long lines from overflowing out of the view.  
         
      * Wrapping Width (Only For Text Objects)
      
         Width of the text wrap area.  
         A value of 1 is the full width of the screen.  
         
      * Text Justification (Only For Text Objects)
      
         Determines the position of the text relative to it's center point.  
         If wrapping is enabled, the text will justify to the edges of the bounding area.  
      
      * Pos
      
         Use these values to position the object in the title.  
         X is horizontal position.  0 is at the screen center, negative values move the object left, positive values move it right.  1 and -1 should be about the edges of the screen.  
         Y is the vertical position.  0 is at the screen center, negative values move the object down, positive values move the object up.  
         Z is the depth position.  0 is normal position, positive values will move the object towards the camera, negative values move it away.  Because the title is in 3d perspective, this will change the horizontal and vertical positions of the object.  

      * Rot

         Use these values to rotate the object in the title.  
         Note that these will rotate the object around its center, so if text is left-justified, its rotation may be undesirable.  
         X is the 'tilt' of the object along the X axis, positive values will rotate the object's top towards the camera, negative values will rotate it away.  
         Y is the horizontal 'turn' of the object.  Positive values will rotate it around to the right, negative rotate it around to the left.  
         Z is the 'spin' of the object, while keeping it facing the camera.  Positive values will spin it clockwise, negative spin it counter-clockwise.  
         
      * Shearing
         
         Defines a 'slant' of the object, causing it to 'lean' forward or back.  Positive values will 'lean' the object forward, negative 'lean' it back.  
         This gives text an italic style, and will make a square into a rhombus.  
         
      * Scale
      
         The overall scale of the object, changes height and width the same amount.  
         
      * Width
      
         Adjust only the width of the object, make a square into a rectangle, or a circle into an oval.  
         This is a multiple of the overall scale, both can be used at once.  
         
      * Height
      
         Adjust only the height of the object.  Like the width, this is a multiple of the overall scale.  
         
      ### Thickness Settings (Not For Image Objects)
      
      * Thickness (Not For Image Objects)
      
         Gives the object a 3d thickness, instead of being perfectly flat.  
      
      * Bevel (Not For Image Objects)
      
         Cuts off the edges of the object, giving it rounded or squared off corners.  
         Note that some fonts will not work well with this setting, if you see strange jagged edges, try a different font.  
      
      * Bevel Resolution (Not For Image Objects)
      
         Resolution of the bevel, higher values result in curved corners, 0 results in sharp corners.  
      
      ### Outline Settings (Not For Image Objects)
      
      * Outline Enable (Not For Image Objects)
      
         Enables an outline for this object.  
         This is actually a beveled copy of the object, so any issues with beveling will also show here.  
         
      * Outline Size (Not For Image Objects)
      
         Size of the outline, larger numbers result in a wider outline.  
         Note that setting this too high may cause strange artifacts around the object, especially on text.  
      
      * Outline Alpha (Not For Image Objects)
      
         Alpha transparency of the outline, 0 is fully transparent, 1 is fully opaque.  
      
      * Outline Color (Not For Image Objects)
      
         Color of the outline.  
         Note that the outline will have no shading applied, it will be completely this color.  
         
      ### Material Settings
      
      * Set Material
      
         Enable this to display a dropdown menu allowing the material of this object to be set to a pre-existing material.  
         This is useful for making multiple titles have the same material for similar objects, allowing for easily tweaking the materials of all at once.   
      
      * Use No Shading
      
         Enable this to make the material of this object a solid color with no shading or specularity.  
      
      * Cast Shadows
      
         Enable this to allow this object to cast shadows on objects behind it.  
      
      * Material Color
      
         Basic diffuse color of the object.  
         
      * Specular
      
         Set the amount of reflectivity or 'shinyness' on this object.  
         0 results in no shinyness, 1 is full shinyness.  
      
      * Hardness
      
         Determines how sharp or wide the specular reflections are.  
         The higher this number, the sharper the reflections are.  
         
      * Specular Color
      
         Set the color of the reflections.  
         
      * Transparency (Only For Image Objects)
      
         Enables transparency on images that include it (such as png images with an alpha channel).  
         This will be automatically enabled on other object types.  
      
      * Alpha
      
         Set the transparency of this object.  0 is fully invisible, 1 is fully opaque.  
      
      * Texture (Only For Image Objects)
      
         Load an image or video to display it on this object.  
         
      * Alpha Texture (Only For Image Objects)
      
         Load an image or video to control the alpha transparency of this image.  
         This works best with a black and white image or video.  
      
      * Loop Video (Only For Image Objects, Only With Video Texture)
      
         Enables looping on a video texture, repeat play of the video as long as needed.  

      * Frame Offset (Only For Image Objects, Only With Video Texture)
         
         Offset the beginning of this video by a number of frames.  
         Set this above 0 to cut off the beginning of the video.  
      
      * Frame Length (Only For Image Objects, Only With Video Texture)
         
         The number of frames to play back of this video.  
         This value will be set automatically to the length of the video when a new video is loaded.  
         Set this lower than the default to cut off the end of the video.  
      
      ### Animations
      
      * Add Animation Menu
      
         Select an animation from this menu to add it to the current object.  
      
      * Apply To All Objects
      
         Apply the animations of the current object to all objects in the title, overwriting any existing animations.  
      
      * Animate In/Animate Out
      
         Enable this to animate this variable 'in' at the beginning of the title, or 'out' at the end.  
         This allows things such as making the object fade in, or slide in at the beginning of the title.  
      
      * In Length/Out Length
      
         How many frames to animate the variable in or out.  
         Setting an alpha fade in to an in length of 15 means it will take 15 frames for the object to become fully visible.  
      
      * In Frame Offset/Out Frame Offset
      
         Distance from the start or end of the title that the animation will take place.  
         Setting the In Frame Offset to 30 will delay the in animation by 30 frames.  
         Setting the Out Frame Offset to 30 will make the out animation end 30 frames before the end of the title.  
      
      * In Amount/Out Amount
      
         The value that the in or out animation will end on.  
         Set this to 0.5 for an alpha in animation to start the object at half visible, and fade to fully visible.  
      
      * Animation Cycle Menu
      
         Select a cyclic animation from this menu to enable repeated animation on this object.  
         Random - Results in a randomized animation curve.  Useful for making an object randomly jump around.  
         Sine - A smooth animation curve regularly alternating between high and low.  Useful for making an object wobble back and forth.  
         Tangent - Starts at one extreme value, slows down, and ends at another extreme.  Useful for making an object spin.  
      
      * X Scale (Only When Animation Cycle Enabled)
      
         Scales the animation curve along the time axis.  
         Larger values results in longer animations.  
      
      * Y Scale  (Only When Animation Cycle Enabled)
      
         Scales the animation curve along the amplitude axis.  
         Larger values result in higher animation values.  
         Set this to negative to invert a tangent curve.  
      
      * Offset  (Only When Animation Cycle Enabled)
      
         Time offset of animation curve.  
         Use this to desync multiple animation curves of the same type.  
      
      ### Title Shadows
      
      * Shadow Amount
      
         Determines how strong the shadows in the title will be.  
         0 results in no shadows, higher values result in darker shadows.  
      
      * Distance
      
         Vertical distance of the shadow casting lamp.  
         Higher values result in longer and softer shadows.  
         Setting this too low can result in the shadow lamp being inside another object, or not casting shadows from all objects.  
      
      * Soft
      
         Softness of the shadows.  0 results in fully sharp shadows, higher values result in softer shadows.  
      
      * X Offset/Y Offset
      
         Position of the shadow casting lamp.  
         Use this to change the direction and angle of the shadows.  
         Setting this too high will result in the shadows disappearing.  
      
      * High Quality Shadows
      
         Enable high quality raytraced shadows.  
         These are much more accurate than the default shadows, but will GREATLY increase render times.  
         Note that these will not be seen in the opengl previews of the title scene, only in final renders.  


## Editing Titles In The Sequencer Preview

If a title is selected in the sequencer, and while the mouse is over the preview window, the title can be edited using various shortcuts.  

* Left-Click on title elements to select them  

* Press 'G' to enter grab/move mode for the selected element.  You can constrain movement to the three axis by pressing the x, y and z keys after entering move mode.  When moving on a single axis, you can type in exact movement values.  

* Press 'S' to enter scale mode for the selected element.  Like grab, you can constrain to an axis, or type in values directly.  Constraining to the z axis will modify the object's extrude value (not available for image types).  

* Press 'R' to enter rotate mode for the selected element.  Again, you can constrain on an axis, and type in values.  

* Press 'L' to enter grab mode for the shadow casting lamp.  This will behave just like object grab mode.  

* Press Shift-A to open the add object menu.  

* Press 'X' or 'Delete' to delete the selected object.  

* Press 'Page Up' to move the selected object up one in the object stack.  

* Press 'Page Down' to move the selected object down one in the object stack.  



## Advanced Scene Editing
QuickTitling generates standard blender scenes that can be edited after they are generated.  If you wish to edit the scene, it is recommended to remove 'QuickTitle:' from the scene name, this will prevent QuickTitling from updating the scene and overwriting anything you may have changed, but it will also prevent the usage of the interface to adjust title settings.  

If you wish to maintain the ability to edit the title using QuickTitling:  
* New objects can be added and scene and render settings can be changed without issues.  

* If you wish to change a material, any settings not covered by the QuickTitling interface should be able to be changed without reverting.  Extra textures can be added to objects, just for an image type make sure they are using texture slots other than the first two.  

* If you wish to edit an object, it is recommended to rename it, this will prevent QuickTitling from finding the object.  After you rename it, delete it from the object list or it will be re-created on the next update.  



## Changelog
### 0.1
   * First stand-alone version, just separated from VSE Quick Functions, no changes
### 0.2
   * Updated interface - made it look better, and its now easier to tell when a scene is being edited
   * When a title scene is edited, changes now happen in realtime
   * Added word-wrapping
   * The values in the interface are now a bit more sane - bevel is multiplied by 100, X location of 1 is the edge of the screen
   * Added shadow offset option
   * Added specular material options
   * Added ability to use ray traced shadows
### 0.5
   * Implemented adding multiple objects of 4 basic types: image, box, circle, and text
   * Implemented presets
   * Implemented saving/loading presets
   * Reworked interface
   * Added animation abilities and presets
   * Implemented new way of handling materials
   * Implemented saving preset preview images
### 0.5.1
   * Fixed bug not checking vertices for curve objects properly, oops
   * Fixed bug where Blender 2.78 changed the variable name for text 'align' to 'align_x'
### 0.6
   * Changed interface and workflow, should make a lot more sense now
   * Built-in titles are now shown in preset menu, with preview images
   * Newly added objects are named
   * Circles are now actually circles
   * Now keeps track of if a title is edited and displays this
   * Added video settings (loop, frame offset, length), only shown if the loaded texture is a video
   * Added outline options for all but image type, uses a beveled copy of the object to create an outline
   * Added animation oscillations and animation presets for these
   * Added duplicate object button
   * Word wrapping behaves better now, changing the text scale does not change the wrapping size
   * Exported presets are cleaner now - default variables are not saved and xml files have line returns and indenting
   * Updated old presets and added new ones
   * Added overlays in preview windows to show selected title objects
   * Added grab, rotate and scale shortcuts (G, R, S in preview area) for selected object. You can also constrain on an axis, and type in values
   * Added click to selected title elements! Unfortunately, for some reason, I can't make this right click... doesn't work, so had to do left...
   * Added page up/page down shortcuts to change the current object layer
   * Added Shift-T shortcut in sequencer to pop up the title preset menu and add a new title quickly
