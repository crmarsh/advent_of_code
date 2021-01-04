use ::common::*;
use regex::Regex;
use std::collections::HashMap;
use std::collections::HashSet;
use std::path::Path;
#[macro_use]
extern crate lazy_static;

#[derive(Debug, Default)]
struct InputEntry {
    bag_name: String,
    contains: Vec<(String, u64)>,
    contains_total: u64,
}

lazy_static! {
    static ref RE: Regex = Regex::new(r"^([a-z ]+) bags contain (.+)\.$").unwrap();
    static ref BAG_ENTRY: Regex = Regex::new(r"^(\d+) ([a-z ]+) bags?+$").unwrap();
}

fn read_contains(bags_string: String) -> Vec<(String, u64)> {
    let mut result = Vec::<(String, u64)>::new();

    if bags_string == "no other bags" {
        return result;
    }

    for bag_str in bags_string.as_str().split(", ") {
        if let Some(caps) = BAG_ENTRY.captures(&bag_str) {
            let entry = (caps[2].to_string(), caps[1].parse().unwrap());
            result.push(entry);
        } else {
            println!("Parse error with {}", bag_str);
        }
    }

    return result;
}

fn read_entry(line: String) -> Option<InputEntry> {
    let caps_maybe = RE.captures(&line);

    return match caps_maybe {
        Some(caps) => {
            let contains_string = caps[2].to_string();
            let contains = read_contains(contains_string);

            let entry = InputEntry {
                bag_name: caps[1].to_string(),
                contains: contains,
                contains_total: 0,
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

    if let Ok(lines) = common::read_lines(filename) {
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

fn main() {
    let mut cmd_line = std::env::args();
    let file_to_read = if cmd_line.len() > 1 {
        cmd_line.nth(1).unwrap()
    } else {
        "sample.txt".to_string()
    };
    let mut input_entries = read_input(file_to_read);
    let start_bag = "shiny gold";
    let mut outer_bags = HashSet::<String>::new();
    let mut last_bag_count = 0;
    outer_bags.insert(start_bag.to_string());
    let mut bag_count = 1;
    while last_bag_count != bag_count {
        let current_bags = outer_bags
            .iter()
            .map(|x| x.clone())
            .collect::<Vec<String>>();
        for bag in current_bags {
            for entry in &input_entries {
                for contain in &entry.contains {
                    if contain.0 == *bag {
                        if outer_bags.insert(entry.bag_name.clone()) {
                            println!("adding {}", entry.bag_name);
                        }
                        break;
                    }
                }
            }
        }
        last_bag_count = bag_count;
        bag_count = outer_bags.len();
        println!("pass {} -> {}", last_bag_count, bag_count);
    }
    outer_bags.remove(&start_bag.to_string());
    println!("{} outer bags: {:?}", outer_bags.len(), outer_bags);
    let mut num_resolved = 0;
    let mut bag_lookup = HashMap::<String, usize>::new();
    let mut i = 0;
    for entry in input_entries.iter() {
        bag_lookup.insert(entry.bag_name.clone(), i);
        i += 1;
    }
    println!("bag_lookup {:?}", bag_lookup);
    let mut pass = 0;
    bag_count = input_entries.len();
    while num_resolved < bag_count {
        for entry_index in 0..bag_count {
            {
                let mut entry = &mut input_entries[entry_index];
                if entry.contains_total > 0 {
                    continue;
                }
                if entry.contains.len() == 0 {
                    entry.contains_total = 1;
                    num_resolved += 1;
                    println!("resolved trivially {:?}", entry);
                    continue;
                }
            }
            let mut this_bag_count: u64 = 1;
            for sub_entry in &input_entries[entry_index].contains {
                if let Some(sub_bag_index) = bag_lookup.get(&sub_entry.0) {
                    let sub_bag = &input_entries[*sub_bag_index];
                    if sub_bag.contains_total > 0 {
                        this_bag_count += sub_entry.1 * sub_bag.contains_total;
                    } else {
                        this_bag_count = 0;
                        break;
                    }
                }
            }
            if this_bag_count > 0 {
                input_entries[entry_index].contains_total = this_bag_count;
                num_resolved += 1;
                //println!("resolved {:?}", input_entries[entry_index]);
            }
        }
        println!("pass {}, {} / {} resolved", pass, num_resolved, bag_count);
        pass += 1;
    }

    if let Some(shiny_index) = bag_lookup.get("shiny gold") {
        let entry = &input_entries[*shiny_index];
        let contains_bags = entry.contains_total - 1;
        println!("Shiny gold: {}", contains_bags);
    }
}
