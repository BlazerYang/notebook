var a = new Date()
// 2 method get UTC date&time string
console.log(`toISOString:        ${a.toISOString()}`)
console.log(`toUTCString:        ${a.toUTCString()}`)
// 2 method get locale date&time string
console.log(`toString:           ${a.toString()}`)
console.log(`toLocaleString:     ${a.toLocaleString()}`)
// get locale date string in toString() format
console.log(`toDateString:       ${a.toDateString()}`)
// get locale time string in toString() format
console.log(`toTimeString:       ${a.toTimeString()}`)
// get locale date string in toLocaleString() format
console.log(`toLocaleDateString: ${a.toLocaleDateString()}`)
// get locale time string in toLocaleString() format
console.log(`toLocaleTimeString: ${a.toLocaleTimeString()}`)

var args = [a.getFullYear(), a.getMonth(), a.getDate(), a.getHours(), a.getMinutes(), a.getSeconds(), a.getMilliseconds()]
console.log(`args: ${args.join()}`)
// parameter is locale time, return Date object
c = new Date(...args)
// parameter is utc time, return miliseconds from 1970-01-01T00:00:00.000Z
d = new Date(Date.UTC(...args))
console.log(a)
console.log(c)
console.log(d)

console.log(a.getTime())
console.log(c.getTime())
console.log(d.getTime())