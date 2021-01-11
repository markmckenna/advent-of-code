#!/usr/bin/env node

fs = require('fs');

const bitFor = c => (c == 'B' || c == 'R') ? 1 : 0

fs.readFile('d5.txt', 'ascii', (e,file) => {
  var lowest = 99999
  var highest = -1
  var seatsSeen = {}

  const passes = file.split('\n')

  for (pass of passes) {
    console.log(pass)

    const aisle = 
      bitFor(pass[0]) * 64 + 
      bitFor(pass[1]) * 32 + 
      bitFor(pass[2]) * 16 + 
      bitFor(pass[3]) * 8 + 
      bitFor(pass[4]) * 4 + 
      bitFor(pass[5]) * 2 + 
      bitFor(pass[6]) * 1

    const seat =
      bitFor(pass[7]) * 4 + 
      bitFor(pass[8]) * 2 + 
      bitFor(pass[9]) * 1

    const code = aisle*8 + seat

    console.log('code is', code)

    if (code > highest) highest = code
    if (code < lowest) lowest = code
    seatsSeen[code] = 1
  }

  console.log(seatsSeen)

  for (i=0; i < 951; ++i) {
    if (!seatsSeen[i] && seatsSeen[i-1] && seatsSeen[i+1]) console.log('your seat is', i)
  }


  console.log('highest code is', highest)
});
