// convertCurlToPython.js
async function convertCurlToPython(curlCommand) {
    const curlconverter = await import('curlconverter');
    return curlconverter.toPython(curlCommand);
}
async function main() {
    if (process.argv.length < 3) {
        console.error('Usage: node convertCurlToPython.js "<CURL COMMAND>"');
        process.exit(1);
    }

    const curlCommand = process.argv[2];
    try {
        const pythonCode = await convertCurlToPython(curlCommand);
        console.log(pythonCode);
    } catch (error) {
        console.error('Error converting curl command:', error);
    }
}

main();