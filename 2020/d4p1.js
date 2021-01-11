#!/usr/bin/env node

fs = require('fs');

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

    for (const field of ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']) {
      if (!record.hasOwnProperty(field)) {
        invalid++
        console.log('INVALID: does not contain ', field)
        break
      }
    }
  }

  console.log(passports.length - invalid)
});
