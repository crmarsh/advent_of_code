use ::common::*;
use regex::Regex;
//use std::collections::HashMap;
use std::collections::HashSet;
use std::path::Path;
#[macro_use]
extern crate lazy_static;

#[derive(Debug, Default)]
struct InputEntry {
    operation: String,
    argument: i32,
}

lazy_static! {
    static ref RE: Regex = Regex::new(r"^([a-z]+) ([+-]\d+)$").unwrap();
}

fn read_entry(instruction: String) -> Option<InputEntry> {
    let caps_maybe = RE.captures(&instruction);

    match caps_maybe {
        Some(caps) => {
            let entry = InputEntry {
                operation: caps[1].to_string(),
                argument: caps[2].parse().unwrap(),
            };
            Some(entry)
        }
        None => None,
    }
}

fn read_input<P>(filename: P) -> Vec<InputEntry>
where
    P: AsRef<Path>,
{
    let mut entries = Vec::new();

    if let Ok(lines) = common::read_lines(filename) {
        for line_result in lines {
            if let Ok(line) = line_result {
                if let Some(entry) = read_entry(line) {
                    entries.push(entry)
                }
            }
        }
    }

    entries
}

fn main() {
    let mut cmd_line = std::env::args();
    let file_to_read = if cmd_line.len() > 1 {
        cmd_line.nth(1).unwrap()
    } else {
        "sample.txt".to_string()
    };
    let input_entries = read_input(file_to_read);

    for swapped in -1..(input_entries.len() as i32) {
        let mut visited = HashSet::new();
        let mut accumulator: i32 = 0;
        let mut instruction_pointer: i32 = 0;
        loop {
            if visited.contains(&instruction_pointer) {
                if swapped == -1 {
                    println!(
                        "About to loop; acc = {}, ip = {}, swapped {}",
                        accumulator, instruction_pointer, swapped
                    );
                }
                break;
            }
            visited.insert(instruction_pointer);
            if let Some(instruction) = input_entries.get(instruction_pointer as usize) {
                let mut op = instruction.operation.as_str();
                if instruction_pointer == swapped {
                    op = match op {
                        "nop" => "jmp",
                        "jmp" => "nop",
                        _ => op,
                    }
                }

                match op {
                    "nop" => {
                        instruction_pointer += 1;
                    }
                    "jmp" => {
                        instruction_pointer += instruction.argument;
                    }
                    "acc" => {
                        accumulator += instruction.argument;
                        instruction_pointer += 1;
                    }
                    _ => {
                        panic!("Unknown instruction {:?}", instruction);
                    }
                }
            } else {
                println!(
                    "Past end; acc = {}, ip = {}, swapped {}",
                    accumulator, instruction_pointer, swapped
                );
                break;
            }
        }
    }
}
