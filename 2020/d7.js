#!/usr/bin/env node

fs = require('fs');

fs.readFile('d7.txt', 'ascii', (e,file) => {
  const rules = file.split('\n').filter(x => x != '')

  const containmentTree = {}

  for (rule of rules) {
    const [container, rest] = rule.split(' bags contain ')
    const contained = rest
      .split(/ bags?[,. ]*/)
      .filter(x => x != '')
      .filter(x => x != 'no other')
      .reduce((ob, v) => { 
        const num = v.substring(0,1)
        const type = v.substring(2)
        ob[type] = num
        return ob
      }, {})
    containmentTree[container] = contained
  }

  console.log(containmentTree)

  // part 1: find all bags that can directly or indirectly contain 'shiny gold'.
  var candidates = {}
  candidates['shiny gold'] = 1
  var lastqty = 0

  // stabilization search--keep adding to candidates until it stops changing
  while (Object.keys(candidates).length != lastqty) {
    lastqty = Object.keys(candidates).length

    for (candidate of Object.keys(candidates)) {
      for (container of Object.keys(containmentTree)) {
        if (containmentTree[container][candidate]) {
          candidates[container] = 1
        }
      }
    }
  }

  delete candidates['shiny gold']

  console.log(candidates)
  console.log('in total we can store our bag this many ways:', Object.keys(candidates).length)

  // part 2: count how many bags our shiny gold bag has to contain.
  // DFS. On pop, multiply nested result by parent quantity.

  function countNestedContents(bagName) {
    const bag = containmentTree[bagName]
    var count = 0

    for (subbagName of Object.keys(bag)) {
      count += parseInt(bag[subbagName]) * (1+countNestedContents(subbagName))
    }

    console.log('bag', bagName, 'needs', count, 'subbags in total')
    return count
  }

  console.log('your shiny gold bag needs', countNestedContents('shiny gold'), 'inner bags in total')
});
