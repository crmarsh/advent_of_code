import Foundation
import ArgumentParser

var digitStrings = [
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9)
]

struct Day01Solution: ParsableCommand {
    @Option(help: "Specify the input file")
    public var input: String = "sample_input.txt"

    public func firstDigit(of: String) -> Int {
        var index = of.startIndex
        while index < of.endIndex {
            let d = of[index].wholeNumberValue
            if d != nil {
                return d!
            }

            for digitPair in digitStrings {
                if of[index...].starts(with:digitPair.0) {
                    return digitPair.1
                }
            }

            index = of.index(after: index)
        }
        return -1
    }

    public func lastDigit(of: String) -> Int {
        var index = of.endIndex
        while index > of.startIndex {
            index = of.index(before: index)
            let d = of[index].wholeNumberValue
            if d != nil {
                return d!
            }

            for digitPair in digitStrings {
                if of[index...].starts(with:digitPair.0) {
                    return digitPair.1
                }
            }
        }
        return -1
    }

    public func run() throws {
        // Swift doesn't have native "read shit from a file", so hack reopen file as stdin
        guard freopen(input, "r", stdin) != nil else {
            print("File not present.")
            // wtf is all this shit just to throw an error
            throw NSError(coder:NSCoder())!
        }
    
        var total: Int = 0
        while let line = readLine() {
            //print(line)
            let firstDigit = firstDigit(of: line)
            let lastDigit = lastDigit(of: line)
            
            let lineVal = 10 * firstDigit + lastDigit
            //print("lineVal \(lineVal)\n")
            total += lineVal
        }
        print("total \(total)")
    }
}

// Can't @main this for some reason, need to call this way instead
Day01Solution.main()
