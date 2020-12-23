use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug, PartialEq)]
enum MapTile {
    Open,
    Tree,
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn read_map_line(line: String) -> Vec<MapTile> {
    let mut map_line = Vec::new();

    for c in line.chars() {
        if c == '.' {
            map_line.push(MapTile::Open);
        } else if c == '#' {
            map_line.push(MapTile::Tree);
        }
    }
    return map_line;
}

fn read_map_lines<P>(filename: P) -> Vec<Vec<MapTile>>
where
    P: AsRef<Path>,
{
    let mut map_lines = Vec::new();

    let lines = read_lines(filename).unwrap();
    for line_result in lines {
        if let Ok(line) = line_result {
            let ml = read_map_line(line);
            map_lines.push(ml);
        }
    }

    return map_lines;
}

fn main() {
    let mut cmd_line = std::env::args();
    let file_to_read = match cmd_line.nth(1) {
        Some(fpath) => fpath,
        None => "sample.txt".to_string(),
    };
    let map_board = read_map_lines(file_to_read);
    let offsets = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)];
    let mut mult = 1;

    for offset in offsets.iter() {
        let dx = offset.0;
        let dy = offset.1;
        let mut tree_count = 0;
        let mut x = 0;
        let mut y = 0;
        while y < map_board.len() {
            let map_line = &map_board[y];
            let map_tile = &map_line[x % map_line.len()];
            if *map_tile == MapTile::Tree {
                tree_count += 1;
            }

            x += dx;
            y += dy;
        }
        println!("{},{} Trees: {}", dx, dy, tree_count);
        mult *= tree_count;
    }

    println!("Final multiple: {}", mult);
}
