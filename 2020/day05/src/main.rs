use ::common::*;
use std::collections::HashSet;

fn main() {
    let mut cmd_line = std::env::args();
    let file_to_read = match cmd_line.nth(1) {
        Some(fpath) => fpath,
        None => "sample.txt".to_string(),
    };
    let mut min_code = i32::MAX;
    let mut max_code = -1;
    let mut seen = HashSet::new();
    let lines = common::read_lines(file_to_read).unwrap();
    for line_maybe in lines {
        if let Ok(line) = line_maybe {
            let binary_str = line
                .replace("B", "1")
                .replace("F", "0")
                .replace("R", "1")
                .replace("L", "0");
            if let Ok(code) = i32::from_str_radix(binary_str.as_str(), 2) {
                max_code = if max_code > code { max_code } else { code };
                min_code = if min_code > code { code } else { min_code };
                seen.insert(code);
                println!("{} -> {} -> {}", line, binary_str, code);
            }
        }
    }
    println!("Seats code: {} - {}", min_code, max_code);
    for seat in min_code..max_code {
        if !seen.contains(&seat) {
            println!("Seat {} is open", seat);
        }
    }
}
