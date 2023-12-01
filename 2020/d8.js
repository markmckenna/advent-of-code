#!/usr/bin/env node

fs = require('fs');

function runProgram(program) {
  var pc = 0
  var acc = 0

  const linesExecuted = []

  while (true) {
    if (linesExecuted.indexOf(pc) != -1) {
      console.log('oops, infinite loop on line', pc, ': ', program[pc])
      return false
    }

    if (pc == program.length) {
      console.log('program completed successfully; accumulator is', acc)
      return true
    }

    linesExecuted.push(pc)

    console.log('executing instruction', pc, ': ', program[pc])

    switch (program[pc][0]) {
      case 'acc': 
        acc += parseInt(program[pc++][1])
        break
      case 'jmp':
        pc = pc + parseInt(program[pc][1])
        break
      default:
        pc++
    }
  }
}

fs.readFile('d8.txt', 'ascii', (e,file) => {

  const program = file
    .split('\n')
    .filter(x => x != '')
    .reduce((acc, cur) => { acc.push(cur.split(' ')); return acc }, [])

  // run a series of trials, with subsequent [jmp] switched to [nop] calls.
  // A trial fails if it executes any instruction a second time.
  // A trial succeeds if it tries to execute nonexistant instruction [n].
  for (i = 0; i < program.length; ++i) {
    const copy = [...program]
    if (copy[i][0] == 'jmp' || copy[i][0] == 'nop') {
      if (copy[i][0] = 'nop') copy[i][0] = 'jmp'
      else if (copy[i][0] = 'jmp') copy[i][0] = 'nop'
      if (runProgram(copy)) {
        console.log('program halted by adjusting instruction', i)
        break
      }
    }
  }

  console.log('done')
});
