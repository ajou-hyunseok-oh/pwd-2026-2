// 화면과 이벤트: 입력을 계산기에 전달하고 바뀐 상태를 화면에 표시합니다.
const display = document.querySelector<HTMLOutputElement>('#display')!;
const expression = document.querySelector<HTMLParagraphElement>('#expression')!;
const message = document.querySelector<HTMLParagraphElement>('#message')!;
const buttons = document.querySelectorAll<HTMLButtonElement>('[data-key]');

function formatDisplay(value: string): string {
  // 정수 부분에만 쉼표를 넣어 입력 중인 소수점과 끝자리 0을 유지합니다.
  const parts = value.split('.');
  if (!value.includes('e')) parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  return parts.join('.');
}

// 부수 효과: 계산한 문자열을 실제 DOM에 반영하는 부분입니다.
function render(): void {
  const value = state.waiting ? formatNumber(Number(state.input)) : state.input;
  display.textContent = state.error ? 'Error' : formatDisplay(value);
  message.textContent = state.error;
  expression.textContent = pendingExpression(state);
}

buttons.forEach((button) => {
  // 클릭 콜백은 나중에 실행되어도 바깥 범위의 button을 참조합니다(클로저).
  button.addEventListener('click', () => {
    const key = button.dataset.key;
    if (key) {
      handleKey(key);
      render();
    }
  });
});

render();
