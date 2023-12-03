import Foundation
import ArgumentParser

struct Day01Solution: ParsableCommand {
  @Option(help: "Specify the input file")
  public var input: String = "sample_input.txt"

  public func run() throws {
    // Swift doesn't have native "read shit from a file", so hack reopen file as stdin
    guard freopen(input, "r", stdin) != nil else {
        print("File not present.")
        // wtf is all this shit just to throw an error
        throw NSError(coder:NSCoder())!
    }
 
    var total: Int = 0
    while let line = readLine() {
        var firstDigit: Int? = nil
        var lastDigit: Int? = nil
        for c in line {
            let d = c.wholeNumberValue
            if d != nil {
                lastDigit = d
                if firstDigit == nil {
                    firstDigit = d
                }
            }
        }

        let lineVal = 10 * firstDigit! + lastDigit!
        //print("lineVal \(lineVal)")
        total += lineVal
    }
    print("total \(total)")
  }
}

// Can't @main this for some reason, need to call this way instead
Day01Solution.main()
