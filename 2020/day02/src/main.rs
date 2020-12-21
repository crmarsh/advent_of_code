use regex::Regex;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
#[macro_use]
extern crate lazy_static;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Debug, Default)]
struct InputEntry {
    min_count: i32,
    max_count: i32,
    letter: char,
    password: String,
}

lazy_static! {
    static ref RE: Regex = Regex::new(r"^(\d+)-(\d+) (.): (.+)$").unwrap();
}

fn read_entry(line: String) -> Option<InputEntry> {
    let caps_maybe = RE.captures(&line);

    return match caps_maybe {
        Some(caps) => {
            let entry = InputEntry {
                min_count: caps[1].parse().unwrap_or_default(),
                max_count: caps[2].parse().unwrap_or_default(),
                letter: caps[3].chars().nth(0).unwrap(),
                password: caps[4].to_string(),
            };
            Some(entry)
        }
        None => None,
    };
}

fn read_input<P>(filename: P) -> Vec<InputEntry>
where
    P: AsRef<Path>,
{
    let mut entries = Vec::new();

    if let Ok(lines) = read_lines(filename) {
        for line_result in lines {
            if let Ok(line) = line_result {
                match read_entry(line) {
                    Some(entry) => entries.push(entry),
                    None => {}
                }
            }
        }
    }

    return entries;
}

fn is_valid_part1(entry: &InputEntry) -> bool {
    let mut count_of_letter = 0;
    for c in entry.password.chars() {
        if c == entry.letter {
            count_of_letter += 1;
        }
    }
    return entry.min_count <= count_of_letter && count_of_letter <= entry.max_count;
}

fn is_valid_part2(entry: &InputEntry) -> bool {
    let c0 = entry.password.chars().nth((entry.min_count - 1) as usize);
    let c1 = entry.password.chars().nth((entry.max_count - 1) as usize);
    let a = Some(entry.letter);
    return (c0 == a && c1 != a) || (c0 != a && c1 == a);
}

fn main() {
    let mut cmd_line = std::env::args();
    let file_to_read = if cmd_line.len() > 1 {
        cmd_line.nth(1).unwrap()
    } else {
        "sample.txt".to_string()
    };
    let input_entries = read_input(file_to_read);
    let mut valid_part1_count = 0;
    let mut valid_part2_count = 0;
    for entry in input_entries {
        let valid_part1 = is_valid_part1(&entry);
        if valid_part1 {
            valid_part1_count += 1;
        }
        let valid_part2 = is_valid_part2(&entry);
        if valid_part2 {
            valid_part2_count += 1;
        }
        //println!("Entry: {:?}, {}, {}", entry, valid_part1, valid_part2);
    }
    println!("Valid counts: {}, {}", valid_part1_count, valid_part2_count);
}
