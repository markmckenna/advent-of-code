#!/usr/bin/env node

fs = require('fs');

const bitFor = c => (c == 'B' || c == 'R') ? 1 : 0

fs.readFile('d6.txt', 'ascii', (e,file) => {
  var sum = 0

  const groups = file.split('\n\n')

  for (group of groups) {
    console.log(group)

    const people = group.split('\n').filter(x => x != '')
    const groupSize = people.length
    var groupYesses = {}
    for (i=97; i< 97+26; ++i) groupYesses[String.fromCharCode(i)] = 0
    for (person of people) {
      for (answer of person) {
        groupYesses[answer] += 1
      }
    }
    var ct = 0
    for (answer of Object.keys(groupYesses)) if (groupYesses[answer] == groupSize) ct++
    console.log('yesses in group of size', groupSize, groupYesses, ct)
    sum += ct 
  }

  console.log('total group yesses is', sum)
});
