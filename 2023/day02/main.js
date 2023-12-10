"require strict";
const { open } = require('node:fs/promises');

let inputToLoad = "sample_input.txt";
if (process.argv.length > 2) {
    inputToLoad = process.argv[2];
}

const lineRe = /^Game (\d+): (.*)/;
const entryRe = /(\d+) (red|green|blue)/g;
const bagLimits = { 'red': 12, 'green': 13, 'blue': 14 };

(async () => {
    const file = await open(inputToLoad);

    let legitGameSum = 0;

    for await (const line of file.readLines()) {
        const match = lineRe.exec(line);
        if (match == null) {
            continue;
        }
        let gameIsLegit = true;
        const gameNum = parseInt(match[1]);
        const rest = match[2].split(";");
        //console.log(gameNum);

        for (var round of rest) {
            //console.log(round);
            gameRound = {};
            let r = round.matchAll(entryRe);
            for (var entry of r) {
                const count = parseInt(entry[1]);
                const color = entry[2];
                gameRound[color] = count;
            }
            //console.log(gameRound);
            let isLegit = true;
            for (var key in gameRound) {
                if (gameRound.hasOwnProperty(key)) {
                    if (gameRound[key] > bagLimits[key]) {
                        isLegit = false;
                        break;
                    }
                }
            }
            if (!isLegit) {
                gameIsLegit = false;
                break;
            }
        }

        if (gameIsLegit) {
            legitGameSum += gameNum;
        }
    }
    console.log("legitGameSum: " + legitGameSum);
})();
