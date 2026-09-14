// Complete, executable examples for the bilingual Week 2 slides.
const examples = {
  state: `<script>
  let name = $state('world');
  let on = $state(false);
  let list = $state(['a']);
</script>

<input aria-label="Name"
  bind:value={name} />
<button onclick={() => on = !on}>
  {on ? 'ON' : 'OFF'}
</button>
<button
  onclick={() => list.push('item')}>
  Add
</button>
<p>{name} / {list.length}</p>`,
  derived: `<script>
  let prices = $state(
    [1000, 2500, 3000]
  );
  let total = $derived(
    prices.reduce((s, p) => s + p, 0)
  );
  let label = $derived(
    total.toLocaleString('en-US') +
      ' KRW'
  );
</script>

<p>{total} / {label}</p>`,
  focus: `<script>
  let open = $state(false);
  let el = $state();
  $effect(() => {
    if (open && el) el.focus();
  });
</script>

<button onclick={() => open = !open}>
  {open ? 'Close' : 'Open'}
</button>
{#if open}
  <input aria-label="Note"
    bind:this={el} />
{/if}`,
  todos: `<script>
  let nextId = 3;
  let todos = $state([
    { id: 1, text: 'Learn Svelte', done: false },
    { id: 2, text: 'Practice runes', done: true }
  ]);
  function add() {
    todos.push({
      id: nextId++, text: 'New task', done: false
    });
  }
</script>

<button onclick={add}>Add</button>
<ul>
  {#each todos as todo (todo.id)}
    <li><label>
      <input type="checkbox" bind:checked={todo.done} />
      {todo.text}
    </label></li>
  {/each}
</ul>`,
  mouse: `<script>
  let m = $state({ x: 0, y: 0 });
  function handleMousemove(event) {
    m.x = event.clientX;
    m.y = event.clientY;
  }
</script>

<svelte:window onmousemove={handleMousemove} />
<p>Mouse: {m.x} × {m.y}</p>`,
  navigation: `<script>
  import { beforeNavigate } from '$app/navigation';
  let { children } = $props();
  let dirty = $state(false);

  beforeNavigate((nav) => {
    if (!dirty) return;
    if (nav.type === 'leave' ||
        !confirm('Leave without saving?')) {
      nav.cancel();
    }
  });
</script>

<label>Draft
  <textarea oninput={() => dirty = true}></textarea>
</label>
<main>{@render children()}</main>`,
  Child: `<script>
  const { msg } = $props();
</script>

<p>{msg}</p>`,
  Parent: `<script>
  import Child from './Child.svelte';
  let message = $state('Hello!');
</script>

<button onclick={() => message = 'Updated!'}>
  Update
</button>
<Child msg={message} />`,
  Card: `<script>
  let { title, summary, href } = $props();
</script>

<article class="card">
  <h3><a href={href}>{title}</a></h3>
  <p>{summary}</p>
</article>`,
  Cards: `<script>
  import Card from '$lib/Card.svelte';
  let { data } = $props();
</script>

<h2>Projects</h2>
{#each data.projects as p (p.slug)}
  <Card title={p.title} summary={p.summary}
    href={'/projects/' + p.slug} />
{:else}
  <p>No projects yet.</p>
{/each}`
};

const korean = {
  state: examples.state.replace('>\n  Add\n<', '>\n  추가\n<'),
  derived: examples.derived.replace("'en-US'", "'ko-KR'").replace("' KRW'", "'원'"),
  focus: examples.focus.replace("'Close' : 'Open'", "'닫기' : '열기'").replace('aria-label="Note"', 'aria-label="메모"'),
  todos: examples.todos.replace('Learn Svelte', 'Svelte 학습').replace('Practice runes', 'Runes 연습').replace('New task', '새 할 일').replace('>Add<', '>추가<'),
  mouse: examples.mouse.replace('Mouse:', '마우스:'),
  navigation: examples.navigation.replace('Leave without saving?', '저장하지 않고 이동?').replace('<label>Draft', '<label>작성 중인 내용'),
  Parent: examples.Parent.replace('Hello!', '안녕!').replace('Updated!', '변경된 인사말').replace('  Update\n', '  변경\n'),
  Cards: examples.Cards.replace('No projects yet.', '등록된 프로젝트 없음')
};

const localized = name => [korean[name] || examples[name], examples[name]];
module.exports = { examples, korean, localized };
