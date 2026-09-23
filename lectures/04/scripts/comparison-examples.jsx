import React, { useState } from 'react';
import $ from 'jquery';

// The marked sections are displayed verbatim in the lecture.
export function mountJqueryCounter(host) {
  // [lesson:jquery]
  let count = 0;
  const button = $('<button>').appendTo(host);
  button.text(`Clicked ${count} times`);
  button.on('click', () => {
    count += 1;
    button.text(`Clicked ${count} times`);
  });
  // [/lesson:jquery]
  return button;
}

// [lesson:react]
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
// [/lesson:react]
export { Counter };
