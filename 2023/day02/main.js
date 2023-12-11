"require strict";
const { open } = require('node:fs/promises');

let inputToLoad = "sample_input.txt";
if (process.argv.length > 2) {
    inputToLoad = process.argv[2];
}

const lineRe = /^Game (\d+): (.*)/;
const entryRe = /(\d+) (red|green|blue)/g;
const bagLimits = { 'red': 12, 'green': 13, 'blue': 14 };

const cubeSetPower = (limits) => {
    const { red, green, blue } = limits;
    return red * green * blue;
};

(async () => {
    const file = await open(inputToLoad);

    let legitGameSum = 0;
    let powerSum = 0;

    for await (const line of file.readLines()) {
        const match = lineRe.exec(line);
        if (match == null) {
            continue;
        }
        let gameIsLegit = true;
        let gameLimits = { 'red': 0, 'green': 0, 'blue': 0 };
        const gameNum = parseInt(match[1]);
        const rest = match[2].split(";");

        for (var round of rest) {
            gameRound = {};
            let r = round.matchAll(entryRe);
            for (var entry of r) {
                const count = parseInt(entry[1]);
                const color = entry[2];
                gameRound[color] = count;
                gameLimits[color] = Math.max(gameLimits[color], count)
            }
            let isLegit = true;
            for (var key in gameRound) {
                if (gameRound.hasOwnProperty(key)) {
                    if (gameRound[key] > bagLimits[key]) {
                        isLegit = false;
                    }
                }
            }
            if (!isLegit) {
                gameIsLegit = false;
            }
        }

        powerSum += cubeSetPower(gameLimits);

        if (gameIsLegit) {
            legitGameSum += gameNum;
        }
    }
    console.log("legitGameSum: " + legitGameSum);
    console.log("powerSum: " + powerSum);
})();
