use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    const TARGET_NUMBER: i32 = 2020;
    let mut numbers = Vec::new();
    let mut adds_to = HashMap::new();
    let mut cmd_line = std::env::args();
    let file_to_read = if cmd_line.len() > 1 {
        cmd_line.nth(1).unwrap()
    } else {
        "sample_input.txt".to_string()
    };
    if let Ok(lines) = read_lines(file_to_read) {
        for line in lines {
            if let Ok(ip) = line {
                if let Ok(a) = ip.parse::<i32>() {
                    match adds_to.get(&a) {
                        Some(other) => {
                            let b = numbers[*other];
                            println!("Found {} and {}, mult to {}", a, b, a * b);
                        }
                        None => {}
                    }

                    let index: usize = numbers.len();
                    numbers.push(a);
                    let inv = TARGET_NUMBER - a;
                    adds_to.insert(inv, index);
                }
            }
        }
    }
    let n = numbers.len();
    for i in 0..n {
        for j in i + 1..n {
            let a = numbers[i];
            let b = numbers[j];
            let temp = a + b;
            match adds_to.get(&temp) {
                Some(k) => {
                    if *k < j {
                        continue;
                    }
                    let c = numbers[*k];
                    println!("Found {}, {}, and {}, mult to {}", a, b, c, a * b * c);
                }
                None => {
                    continue;
                }
            }
        }
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
