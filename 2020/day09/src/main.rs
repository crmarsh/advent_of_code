use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    const PREAMBLE: usize = 25;
    let mut cmd_line = std::env::args();
    
    let file_to_read = if cmd_line.len() > 1 {
        cmd_line.nth(1).unwrap()
    } else {
        "sample_input.txt".to_string()
    };
    let mut numbers = Vec::new();
    if let Ok(lines) = read_lines(file_to_read) {
        for line in lines {
            if let Ok(ip) = line {
                if let Ok(a) = ip.parse::<i32>() {
                    numbers.push(a);
                }
            }
        }
    }
    let mut last_k = HashSet::new();
    let n = numbers.len();
    for i in 0..PREAMBLE {
        last_k.insert(numbers[i]);
    }
    for i in PREAMBLE..n {
        let checking = numbers[i];
        let mut found = false;
        //println!("checking {}", checking);
        // check the last k
        for j in i - PREAMBLE..i {
            let part0 = numbers[j];
            let part1 = checking - part0;
            if last_k.contains(&part1) {
                found = true;
                break;
            }
        }
        if !found {
            println!("{} not sum of {:?}", checking, last_k);
            break;
        }
        // update last k
        last_k.remove(&numbers[i - PREAMBLE]);
        last_k.insert(numbers[i]);
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
