# Polo Template Generator
Instead of using an existing polo template, specify your values and get a neat template!

## Requirements
- Python 3.11 or higher

## How to use:
Install the packages required with `python -m pip install -r requirements.txt`

In the terminal, execute `python main.py` to use it.

Type in your values, and a template, coordinates set and json will be produced!

> **Note**
> Keep in mind, sometimes the head at 0,0 in the animation JSON can float above/below the body, adjusting the height downwards/upwards to place the head at the same height as the 'Default' pose achieves the same thing.

## How it works:
Once you've inputted the values it does the following:
- Uses your number of heads to make multiples of 5 in each row.
- Creates a blank image to start with the rectangles for the default, headless and siloette. This uses the `height` and `width` values provided, just creating 3 rectangles.
- A new image is created for the heads, making the size using the `width` and `headHeight` values.
- It then draws a new rectangle for each head, in order, colouring them in opposites to make it easy to see and labelling them, noting the coordinates down in the `name_coordinates.txt` file.
- Merges the two images and exports it as `name_template.png`
- Creates the JSON file using the values provided earlier, exporting it as `name.json`

## Examples
Options Used:
- Name of Polo File: demo
- Total Animation Frames: 576
- Height: 380
- Width: 164
- Head Height: 199
- Head Count: 8
### Results

- demo_template.png:

![demo_template](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/03fa5599-a63d-46f3-a1f3-deb6e532ef6f)



- demo_coordinates.txt:
```
Head 1 Coords: 0,380
Head 2 Coords: 164,380
Head 3 Coords: 328,380
Head 4 Coords: 492,380
Head 5 Coords: 656,380
Head 6 Coords: 0,579
Head 7 Coords: 164,579
Head 8 Coords: 328,579
```

- demo.json
```json
{
      "animeName": "demo",
      "percentageMax": "0.2",
      "totalFrame": "576",
      "width": "164",
      "height": "380",
      "headHeight": "199",
      "arrayFrame": [
            {
                  "prop": "0,0,0,0"
            }, ... 99 more...
      ]
}
```
