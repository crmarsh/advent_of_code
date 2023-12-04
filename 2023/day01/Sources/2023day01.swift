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

    public func transformPrefix(of: inout String, at: String.Index, from: String, to: Character) {
        let charsLeft = of.distance(from:at, to:of.endIndex)
        if charsLeft < from.length {
            return
        }

        let endFromIndex = of.index(at, offsetBy: from.length)
        if of[at..<endFromIndex] != from {
            return
        }

        //print("removing \(of) \(at) \(endFromIndex) \(from) \(to)")

        of.replaceSubrange(at...at, with: repeatElement(to, count: 1))
        let newAt = of.index(after: at)
        of.removeSubrange(newAt..<endFromIndex)
    }

  public func transformDigits(of: String) -> String {
    var replaced = of
    var index = replaced.index(replaced.startIndex, offsetBy: 0)
    while index < replaced.endIndex {
        transformPrefix(of: &replaced, at: index, from:"one",   to:"1")
        transformPrefix(of: &replaced, at: index, from:"two",   to:"2")
        transformPrefix(of: &replaced, at: index, from:"three", to:"3")
        transformPrefix(of: &replaced, at: index, from:"four",  to:"4")
        transformPrefix(of: &replaced, at: index, from:"five",  to:"5")
        transformPrefix(of: &replaced, at: index, from:"six",   to:"6")
        transformPrefix(of: &replaced, at: index, from:"seven", to:"7")
        transformPrefix(of: &replaced, at: index, from:"eight", to:"8")
        transformPrefix(of: &replaced, at: index, from:"nine",  to:"9")
        index = replaced.index(after: index)
    }
    return replaced
  }

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
            print(line)
            let fd = firstDigit(of: line)
            let ld = lastDigit(of: line)
            print(fd, ld)
            let changedLine = transformDigits(of: line)
            print(changedLine)

            var firstDigit: Int? = nil
            var lastDigit: Int? = nil
            for c in changedLine {
                let d = c.wholeNumberValue
                if d != nil {
                    lastDigit = d
                    if firstDigit == nil {
                        firstDigit = d
                    }
                }
            }

            let lineVal = 10 * firstDigit! + lastDigit!
            print("lineVal \(lineVal)\n")
            total += lineVal
        }
        print("total \(total)")
    }
}

// Can't @main this for some reason, need to call this way instead
Day01Solution.main()
