use ::common::*;
use regex::Regex;
#[macro_use]
extern crate lazy_static;

#[derive(Debug, Default)]
struct Passport {
    byr: String, // (Birth Year)
    iyr: String, // (Issue Year)
    eyr: String, // (Expiration Year)
    hgt: String, // (Height)
    hcl: String, // (Hair Color)
    ecl: String, // (Eye Color)
    pid: String, // (Passport ID)
    cid: String, // (Country ID) -- optional
}

lazy_static! {
    static ref FIELD_RE: Regex = Regex::new(r"^(...):(.*)$").unwrap();
    static ref YEAR_RE: Regex = Regex::new(r"^(\d{4})$").unwrap();
    static ref HGT_RE: Regex = Regex::new(r"^(\d+)(in|cm)$").unwrap();
    static ref COLOR_RE: Regex = Regex::new(r"^#[0-9a-f]{6}$").unwrap();
    static ref EYE_RE: Regex = Regex::new(r"^amb|blu|brn|gry|grn|hzl|oth$").unwrap();
    static ref PID_RE: Regex = Regex::new(r"^(\d{9})$").unwrap();
}

fn parse_passport(line: &String) -> Passport {
    let mut passport = Passport {
        ..Default::default()
    };

    for part in line.split_ascii_whitespace() {
        let caps_maybe = FIELD_RE.captures(&part);
        match caps_maybe {
            Some(caps) => {
                let key = &caps[1];
                let val = caps[2].to_string();
                match key {
                    "byr" => {
                        passport.byr = val;
                    }
                    "iyr" => {
                        passport.iyr = val;
                    }
                    "eyr" => {
                        passport.eyr = val;
                    }
                    "hgt" => {
                        passport.hgt = val;
                    }
                    "hcl" => {
                        passport.hcl = val;
                    }
                    "ecl" => {
                        passport.ecl = val;
                    }
                    "pid" => {
                        passport.pid = val;
                    }
                    "cid" => {
                        passport.cid = val;
                    }
                    _ => {}
                }
            }
            None => {}
        }
    }

    return passport;
}

fn passport_valid_p1(passport: &Passport) -> bool {
    if passport.byr.is_empty() {
        return false;
    }
    if passport.iyr.is_empty() {
        return false;
    }
    if passport.eyr.is_empty() {
        return false;
    }
    if passport.hgt.is_empty() {
        return false;
    }
    if passport.hcl.is_empty() {
        return false;
    }
    if passport.ecl.is_empty() {
        return false;
    }
    if passport.pid.is_empty() {
        return false;
    }

    return true;
}

fn valid_year(s: &String, min_year: i32, max_year: i32) -> bool {
    match YEAR_RE.captures(s.as_str()) {
        Some(caps) => {
            match caps[1].parse::<i32>() {
                Ok(year) => {
                    if year < min_year || max_year < year {
                        return false;
                    }
                }
                _ => {
                    return false;
                }
            };
        }
        None => {
            return false;
        }
    }
    return true;
}

fn passport_valid_p2(passport: &Passport) -> bool {
    if !valid_year(&passport.byr, 1920, 2002) {
        return false;
    }

    if !valid_year(&passport.iyr, 2010, 2020) {
        return false;
    }

    if !valid_year(&passport.eyr, 2020, 2030) {
        return false;
    }

    match HGT_RE.captures(passport.hgt.as_str()) {
        Some(caps) => {
            let range = match &caps[2] {
                "cm" => (150, 193),
                "in" => (59, 76),
                _ => {
                    return false;
                }
            };
            match caps[1].parse::<i32>() {
                Ok(height) => {
                    if height < range.0 || range.1 < height {
                        return false;
                    }
                }
                _ => {
                    return false;
                }
            }
        }
        _ => {
            return false;
        }
    }

    if !COLOR_RE.is_match(passport.hcl.as_str()) {
        return false;
    }

    if !EYE_RE.is_match(passport.ecl.as_str()) {
        return false;
    }

    if !PID_RE.is_match(passport.pid.as_str()) {
        return false;
    }

    return true;
}

fn main() {
    let mut cmd_line = std::env::args();
    let file_to_read = match cmd_line.nth(1) {
        Some(fpath) => fpath,
        None => "sample.txt".to_string(),
    };
    let lines = common::read_lines(file_to_read).unwrap();
    let mut entry_line = "".to_string();
    let mut entries = Vec::new();
    for line_result in lines {
        if let Ok(line) = line_result {
            if line.len() == 0 {
                let pp = parse_passport(&entry_line);
                entries.push(pp);
                entry_line.clear();
            } else {
                entry_line.push_str(line.as_str());
                entry_line.push(' ');
            }
        }
    }
    let pp = parse_passport(&entry_line);
    entries.push(pp);

    let mut count_valid_1 = 0;
    let mut count_valid_2 = 0;
    for entry in entries {
        let valid_p1 = passport_valid_p1(&entry);
        if valid_p1 {
            count_valid_1 += 1;
        }
        let valid_p2 = passport_valid_p2(&entry);
        if valid_p2 {
            count_valid_2 += 1;
        }
        println!("{:?} -> {}, {}", entry, valid_p1, valid_p2);
    }
    println!("Num valid: {} p1, {} p2", count_valid_1, count_valid_2);
}
