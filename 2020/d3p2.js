#!/usr/bin/env node

fs = require('fs');

function replaceAt(str, pos, val) {
  return str.substring(0, pos) + val + str.substring(pos+1)
}

function impactsFor(lines, xoff, yoff) {
  var xpos = 0
  var impacts = 0

  for (ypos = 0; ypos < lines.length; ypos += yoff) {
    const line = lines[ypos]
    if (line.length == 0) continue;
    if (line[xpos] == '#') {
      console.log('HIT  ', replaceAt(line, xpos, 'X'))
      if (line.length == 0) continue;
      impacts++
    } else {
      console.log('MISS ', replaceAt(line, xpos, 'O'))
    }
    xpos = (xpos+xoff) % (line.length)
  }

  return impacts
}

fs.readFile('advent-3.txt', 'ascii', (e,file) => {
  const lines = file.split('\n')

  const a = impactsFor(lines, 1, 1)
  const b = impactsFor(lines, 3, 1)
  const c = impactsFor(lines, 5, 1)
  const d = impactsFor(lines, 7, 1)
  const f = impactsFor(lines, 1, 2)
  console.log(a, b, c, d, f, a*b*c*d*f)
});
