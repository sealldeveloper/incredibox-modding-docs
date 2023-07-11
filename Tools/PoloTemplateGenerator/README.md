# Polo Template Generator
Instead of using an existing polo template, specify your values and get a neat template!

## Requirements
- Python 3.11 or higher

## How to use:
Install the packages required with `python -m pip install -r requirements.txt`

In the terminal, execute `python main.py` to use it.

Type in your values, and a template and coordinates set will be produced!


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

![demo_template](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/7a24d525-63c0-4bf4-9ae6-02f2b030b108)


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
      "percentageMax": 0.2,
      "totalFrame": 576,
      "width": 164,
      "height": 380,
      "headHeight": 199,
      "arrayFrame": [
            {
                  "prop": "0,0,0,0"
            }, ... 99 more...
      ]
}
```
