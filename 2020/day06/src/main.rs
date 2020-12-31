use ::common::*;
use std::collections::HashSet;

fn main() {
    let mut cmd_line = std::env::args();
    let file_to_read = match cmd_line.nth(1) {
        Some(fpath) => fpath,
        None => "sample.txt".to_string(),
    };
    let lines = common::read_lines(file_to_read).unwrap();
    let mut groups_any = Vec::new();
    let mut groups_all = Vec::new();
    let mut curr_group_any = HashSet::<char>::new();
    let mut curr_group_all = HashSet::<char>::new();
    let mut first_person = true;
    for line_maybe in lines {
        if let Ok(line) = line_maybe {
            if line.is_empty() {
                groups_any.push(curr_group_any);
                curr_group_any = HashSet::new();
                groups_all.push(curr_group_all);
                curr_group_all = HashSet::new();
                first_person = true;
            } else {
                let mut curr_person = HashSet::new();
                for c in line.chars() {
                    curr_person.insert(c);
                }
                curr_group_any.extend(&curr_person);
                if first_person {
                    curr_group_all.extend(&curr_person);
                } else {
                    curr_group_all = curr_group_all.intersection(&curr_person).cloned().collect();
                }
                first_person = false;
            }
        }
    }
    groups_any.push(curr_group_any);
    groups_all.push(curr_group_all);

    let mut count_any = 0;
    for group in groups_any {
        count_any += group.len();
    }

    let mut count_all = 0;
    for group in groups_all {
        count_all += group.len();
    }
    println!("count_any: {}", count_any);
    println!("count_all: {}", count_all);
}
