from common.grid import Grid, Point

ImageInfo = tuple[str, Grid[str]]
def get_image_info(lines: list[str]) -> ImageInfo:
    image_enhancement = lines[0]
    grid: Grid[str] = Grid(lines[2:], lambda x: '1' if x=='#' else '0')
    return (image_enhancement, grid)

def get_number_of_pixels_lit(image_info: ImageInfo, steps=2) -> int:
    enhancement, grid = image_info
    for step in range(steps):
        grid = enhance(enhancement, grid, step)
    return list(grid.values()).count('1')

def enhance(enhancement: str, grid: Grid[str], step: int) -> Grid[str]:
    new_grid: Grid[str] = Grid([])
    for point in grid:
        new_grid[point] = get_new_value(enhancement, grid, point, step)

    outskirts = grid.get_outskirt_points()
    outskirt_values = [get_new_value(enhancement, grid, p, step)
                       for p in outskirts]
    if '1' in outskirt_values:
        for p,v in zip(outskirts, outskirt_values):
            new_grid[p] = v

    return new_grid

def get_new_value(enhancement: str, grid: Grid[str],
                  point: Point, step: int) -> str:
    #specific to input
    default = '0' if step%2 == 0 else '1'
    block = sorted(grid.get_neighbors(point, default, True) +
                   [(point, grid.get(point, default))], key=lambda x:x[0][::-1])
    index = int(''.join(b for _,b in block), base=2)
    return '1' if enhancement[index]=='#' else '0'

with open("input/input20.txt", encoding="utf-8") as f:
    IMAGE_INFO = get_image_info([x.strip() for x in f.readlines()])

if __name__ == "__main__":
    print(f"Pixels lit: {get_number_of_pixels_lit(IMAGE_INFO)}")
    print(f"Pixels lit (50): {get_number_of_pixels_lit(IMAGE_INFO, 50)}")
