#!/usr/bin/env node

fs = require('fs');

// inclusive range check; true iff in range
const between = (val, low, high) => (val >= low && val <= high)

// membership check; true iff val exactly matches one entry in list, otherwise throws
function oneOf(val, list) {
  for (i of list) if (val == i) return true
  throw 'not in ' + list.toString()
}

// expects fn() to return true. Propagates throws for more information.
function assert(msg, fn, ...args) {
  var out
  try { out = fn(...args) } 
  catch (e) { throw msg + ': ' + e }

  if (typeof out != 'undefined' && !out) throw msg
}


fs.readFile('d4.txt', 'ascii', (e,file) => {
  const passports = file.split('\n\n')
  var invalid = 0

  for (passport of passports) {
    const fields = passport.split(/[\n\t ]+/)

    const record = fields.reduce((ob, field) => {
      const [key, value] = field.split(':')
      ob[key] = value
      return ob
    }, {})

    console.log('passport is ', record)

    try {
      assert('missing field', () => {
        for (const field of ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
          if (!record.hasOwnProperty(field))
            throw field
      })

      assert('birth year of length 4', () => record.byr.length == 4)
      assert('issue year incorrect length', () => record.iyr.length == 4)
      assert('expiration year incorrect length', () => record.eyr.length == 4)

      assert('birth year range', () => between(record.byr, 1920, 2002))
      assert('issue year range', () => between(record.iyr, 2010, 2020))
      assert('expiration year range', () => between(record.eyr, 2020, 2030))

      assert('height range', val => {
        if (val.endsWith('cm')) assert('cm range', () => between(parseInt(val), 150, 193))
        else if (val.endsWith('in')) assert('in range', () => between(parseInt(val), 59, 76))
        else throw 'bad suffix: ' + val
      }, record.hgt)

      assert('hair colour', val => val.match(/^#[0-9a-f]{6}$/), record.hcl)
      assert('eye colour', val => oneOf(val, ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']), record.ecl)

      assert('passport id', val => val.match(/^[0-9]{9}$/), record.pid)

    } catch (e) {
      invalid++
      console.log('INVALID: ', e)
    }
  }

  console.log(passports.length - invalid)
});
