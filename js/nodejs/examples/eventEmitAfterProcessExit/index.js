var readline = require('readline'),
    fs = require('fs')

var testPath = 'test.log'
var testRL = readline.createInterface({
  input: fs.createReadStream(testPath),
  crlfDelay: Infinity
})

console.log('process.exit(0)')
process.exit(0)

testRL.on('line', (line) => {
  console.log(`LINE RECEIEVED: ${line}`)
})

testRL.on('close', (err) => {
  console.log('READ TEST FINISHED!')
})