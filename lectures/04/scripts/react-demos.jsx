import React, { useEffect, useId, useLayoutEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { mountJqueryCounter, Counter } from './comparison-examples.jsx';

// Adapted from react.dev/learn/thinking-in-react (names translated for class).
const PRODUCTS = [
  { id: 'apple', ko: '사과', en: 'Apple', category: 0, price: '$1', stocked: true },
  { id: 'dragonfruit', ko: '용과', en: 'Dragonfruit', category: 0, price: '$1', stocked: true },
  { id: 'passionfruit', ko: '패션프루트', en: 'Passionfruit', category: 0, price: '$2', stocked: false },
  { id: 'spinach', ko: '시금치', en: 'Spinach', category: 1, price: '$2', stocked: true },
  { id: 'pumpkin', ko: '호박', en: 'Pumpkin', category: 1, price: '$4', stocked: false },
  { id: 'peas', ko: '완두콩', en: 'Peas', category: 1, price: '$1', stocked: true },
];
function useLocale() {
  const [locale, setLocale] = useState(document.documentElement.lang === 'en' ? 'en' : 'ko');
  useEffect(() => {
    const deck = document.querySelector('[data-web-deck]');
    const update = () => setLocale(document.documentElement.lang === 'en' ? 'en' : 'ko');
    deck.addEventListener('webdeck:localechange', update);
    return () => deck.removeEventListener('webdeck:localechange', update);
  }, []);
  return locale;
}
function ProductRow({ product, locale }) {
  return <div className={`react-product-row ${product.stocked ? '' : 'is-unavailable'}`} data-product={product.id}>
    <span>{product[locale]}{!product.stocked && <small>{locale === 'ko' ? '품절' : 'Out of stock'}</small>}</span>
    <span>{product.price}</span>
  </div>;
}
function SearchBar({ locale, query, setQuery, stockOnly, setStockOnly, editable }) {
  const id = useId();
  return <div className="react-searchbar" data-component="SearchBar">
    <label htmlFor={id}>{locale === 'ko' ? '상품명 검색' : 'Search products'}</label>
    <input id={id} type="search" value={query} placeholder={locale === 'ko' ? '상품명 입력' : 'Product name'} readOnly={!editable} onChange={e => setQuery(e.target.value)} />
    <label className="react-stock-label"><input type="checkbox" checked={stockOnly} disabled={!editable} onChange={e => setStockOnly(e.target.checked)} />{locale === 'ko' ? '재고 있는 상품만' : 'Only products in stock'}</label>
  </div>;
}
function ProductTable({ products, locale }) {
  return <div className="react-product-table" data-component="ProductTable">
    <div className="react-result-count" aria-live="polite">{locale === 'ko' ? `검색 결과 ${products.length}개` : `${products.length} ${products.length === 1 ? 'result' : 'results'}`}</div>
    <div className="react-product-head"><span>{locale === 'ko' ? '상품명' : 'Name'}</span><span>{locale === 'ko' ? '가격' : 'Price'}</span></div>
    {[0, 1].map(category => {
      const items = products.filter(p => p.category === category);
      return items.length > 0 && <React.Fragment key={category}>
        <div className="react-category">{locale === 'ko' ? ['과일', '채소'][category] : ['Fruits', 'Vegetables'][category]}</div>
        {items.map(product => <ProductRow key={product.id} product={product} locale={locale} />)}
      </React.Fragment>;
    })}
    {!products.length && <div className="react-no-results">{locale === 'ko' ? '조건에 맞는 상품 없음' : 'No matching products'}</div>}
  </div>;
}
function ProductApp({ locale, stock = false, queryPreset = false, editable = false, boundaries = false, reuse = false }) {
  const [query, setQuery] = useState(queryPreset ? (locale === 'ko' ? '사과' : 'Apple') : '');
  const [stockOnly, setStockOnly] = useState(stock);
  const [showBounds, setShowBounds] = useState(false);
  useEffect(() => { setQuery(queryPreset ? (locale === 'ko' ? '사과' : 'Apple') : ''); setStockOnly(stock); }, [locale, stock, queryPreset]);
  const products = PRODUCTS.filter(p => (!stockOnly || p.stocked) && p[locale].toLowerCase().includes(query.trim().toLowerCase()));
  return <div className={`react-product-app ${showBounds ? 'show-boundaries' : ''} ${reuse ? 'show-reuse' : ''}`}>
    <div className="react-app-title"><strong>{locale === 'ko' ? '상품 검색' : 'Product Search'}</strong>{boundaries && <button className="react-demo-button" aria-pressed={showBounds} onKeyDown={e => e.stopPropagation()} onClick={() => setShowBounds(!showBounds)}>{locale === 'ko' ? (showBounds ? '경계 숨기기' : '컴포넌트 경계') : (showBounds ? 'Hide boundaries' : 'Component boundaries')}</button>}</div>
    <SearchBar {...{locale,query,setQuery,stockOnly,setStockOnly,editable}} />
    <ProductTable products={products} locale={locale} />
  </div>;
}
function FilterComparison({ locale }) {
  const ko = locale === 'ko';
  return <>
    <div className="react-comparison">
      <div><h3>{ko ? '전체 상품 · 6개' : 'All Products · 6 Items'}</h3><ProductApp locale={locale} /></div>
      <div><h3>{ko ? '검색 조건 적용' : 'Search Criteria Applied'}</h3><ProductApp locale={locale} stock editable /></div>
    </div>

  </>;
}
function DomExample({ locale }) {
  const ko = locale === 'ko';
  return <div className="react-dom-columns">
    <div><h3>{ko ? '브라우저에 보이는 결과' : 'Visible Browser Output'}</h3><section className="react-result-fragment"><p>{ko ? '검색 결과 1개' : '1 result'}</p><ul><li>{ko ? '사과' : 'Apple'} $1</li></ul></section><p className="react-detail">{ko ? '‘사과’ 검색 결과의 목록 부분' : 'List area for the search “Apple”'}</p></div>
    <div><h3>DOM</h3><div className="react-tree"><div>section</div><div className="react-indent">p → {ko ? '검색 결과 1개' : '1 result'}</div><div className="react-indent">ul</div><div className="react-indent-2">li → {ko ? '사과' : 'Apple'} $1</div></div></div>
    <div><h3>Virtual DOM</h3><div className="react-tree react-tree--memory"><div>section</div><div className="react-indent">p → {ko ? '검색 결과 1개' : '1 result'}</div><div className="react-indent">ul</div><div className="react-indent-2">li → {ko ? '사과' : 'Apple'} $1</div></div></div>
    <dl className="react-concepts react-dom-summary">
      <div className="react-concept"><dt><strong>{ko ? 'DOM - 브라우저가 보유한 문서 노드' : 'DOM - Document nodes held by the browser'}</strong></dt></div>
      <div className="react-concept">
        <dt><strong>{ko ? 'Virtual DOM - 원하는 UI를 나타내는 트리' : 'Virtual DOM - A tree of the desired UI'}</strong></dt>
        <dd><ul className="react-concept-details">
          <li>{ko ? 'JavaScript 객체로 표현한 메모리의 UI 구조' : 'In-memory UI structure described by JavaScript objects'}</li>
          <li>{ko ? '실제 DOM 변경을 계산하는 기준' : 'A basis for calculating changes to the actual DOM'}</li>
        </ul></dd>
      </div>
    </dl>
  </div>;
}
// The same marked examples power the code comparison and the DOM observation.
function ObservedCounter({ engine, locale, inspect }) {
  const host = useRef(null);
  const [observation, setObservation] = useState(null);
  useLayoutEffect(() => {
    const element = host.current;
    const jqueryButton = engine === 'jquery' ? mountJqueryCounter(element) : null;
    const original = element.querySelector('button');
    const observer = new MutationObserver(() => {
      const current = element.querySelector('button');
      setObservation({ retained: original === current, text: current.textContent });
    });
    if (inspect) observer.observe(element, {childList: true, subtree: true, characterData: true});
    return () => { observer.disconnect(); jqueryButton?.remove(); };
  }, [engine, inspect]);
  const ko = locale === 'ko';
  return <div className="react-counter-example" data-counter-engine={engine}>
    <h3>{engine === 'jquery' ? 'jQuery' : 'React'} · {ko ? '실행 화면' : 'Live Output'}</h3>
    <div className="react-counter-host" ref={host} onKeyDown={e => {if (e.target.tagName === 'BUTTON') e.stopPropagation();}}>
      {engine === 'react' && <Counter />}
    </div>
    {inspect && <p className="react-counter-observation" aria-live="polite" data-retained={observation?.retained ?? ''}>
      {observation ? (observation.retained ? (ko ? '기존 버튼 유지 · 텍스트 변경' : 'Same button retained · Text changed') : (ko ? '버튼 노드 교체' : 'Button node replaced')) : (ko ? '초기 버튼 · 클릭 수 0' : 'Initial button · Count 0')}
    </p>}
  </div>;
}
function CounterComparison({ locale, inspect = false }) {
  return <div className="react-counter-comparison">
    <ObservedCounter engine="jquery" locale={locale} inspect={inspect} />
    <ObservedCounter engine="react" locale={locale} inspect={inspect} />
  </div>;
}
function UiSnapshot({ locale, after }) {
  const ko = locale === 'ko';
  const products = after ? PRODUCTS.filter(p => p.stocked) : PRODUCTS;
  return <div className="react-ui-snapshot" data-ui-snapshot={after ? 'after' : 'before'}>
    <div>section</div>
    <div className={`react-snapshot-count ${after ? 'is-new-text' : 'is-old-text'}`}>p → {ko ? `검색 결과 ${products.length}개` : `${products.length} results`}</div>
    <div className="react-snapshot-list">ul</div>
    {products.map(p => <div className={`react-snapshot-row ${!p.stocked ? 'is-removed' : ''}`} key={p.id}>li → {p[locale]} {p.price}{!p.stocked && <small>{ko ? '삭제' : 'remove'}</small>}</div>)}
  </div>;
}
function CommitExample({ locale }) {
  const ko = locale === 'ko';
  return <div className="react-commit-example">
    <div className="react-commit-columns">
      <div><h3>{ko ? '이전 UI · 전체 6개' : 'Previous UI · All 6 Items'}</h3><UiSnapshot locale={locale} after={false} /></div>
      <div><h3>{ko ? '새 UI · 재고 있는 4개' : 'New UI · 4 In Stock'}</h3><UiSnapshot locale={locale} after /></div>
      <div><h3>{ko ? 'DOM 반영 후 화면' : 'Output After DOM Updates'}</h3><div className="react-committed-output"><section className="react-result-fragment"><p>{ko ? '검색 결과 4개' : '4 results'}</p><ul>{PRODUCTS.filter(p => p.stocked).map(p => <li key={p.id} data-product={p.id}>{p[locale]} {p.price}</li>)}</ul></section></div></div>
    </div>
    <ol className="react-phase-flow">
      <li><strong>{ko ? '① Trigger - 갱신 시작' : '① Trigger - Update Start'}</strong><span>{ko ? '재고 조건 선택' : 'Stock filter selected'}</span></li>
      <li><strong>{ko ? '② Render - UI 계산' : '② Render - UI Calculation'}</strong><span>{ko ? '컴포넌트 실행' : 'Components called'}</span><span>{ko ? '새 UI 계산 · 비교' : 'New UI calculated and compared'}</span></li>
      <li><strong>{ko ? '③ Commit - DOM 반영' : '③ Commit - DOM Updates'}</strong><span>{ko ? '품절 2행 제거' : '2 unavailable rows removed'}</span><span>{ko ? '검색 결과 개수 변경' : 'Result count changed'}</span></li>
      <li><strong>{ko ? '④ Browser - 화면 표시' : '④ Browser - Screen Display'}</strong><span>{ko ? '필요한 스타일 · 레이아웃 · 페인트' : 'Required style · Layout · Paint'}</span></li>
    </ol>
  </div>;
}
// One React render per second; an uncontrolled input retains its actual DOM node.
function Clock({ locale }) {
  const [time, setTime] = useState(new Date());
  const id = useId();
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);
  return <div className="react-clock">
    <div className="react-clock-face"><span>{locale === 'ko' ? '현재 시간' : 'Current Time'}</span><time>{time.toLocaleTimeString('en-GB', { hour12:false })}</time></div>
    <label htmlFor={id}>{locale === 'ko' ? '입력 중인 메모' : 'Memo in Progress'}</label>
    <input id={id} type="text" defaultValue="React" aria-label={locale === 'ko' ? '입력 중인 메모' : 'Memo in Progress'} />
    <p>{locale === 'ko' ? '시간이 바뀌어도 그대로 남아 있는 입력 내용' : 'Typed text retained as the time changes'}</p>
  </div>;
}
function HelloResults({ locale }) {
  const ko = locale === 'ko';
  return <div className="react-hello-results">
    <figure><figcaption>{ko ? '최초 저장 · Hello, World!' : 'First Save · Hello, World!'}</figcaption><img src="materials/images/hello-world.png" alt="Hello, World!" /></figure>
    <figure><figcaption>{ko ? '문구 변경 후 저장 · Hello, React!' : 'Text Changed and Saved · Hello, React!'}</figcaption><img src="materials/images/hello-react.png" alt="Hello, React!" /></figure>
    <p className="react-detail">{ko ? 'Vite 개발 서버 · App.tsx 저장 전후의 실제 화면' : 'Vite Dev Server · Actual Output Before and After Saving App.tsx'}</p>
  </div>;
}
function Demo({ mode }) {
  const locale = useLocale();
  switch (mode) {
    case 'components': return <ProductApp locale={locale} boundaries />;
    case 'reuse': return <ProductApp locale={locale} reuse />;
    case 'filter': return <FilterComparison locale={locale} />;
    case 'declarative': return <ProductApp locale={locale} queryPreset />;
    case 'dom': return <DomExample locale={locale} />;
    case 'commit': return <CommitExample locale={locale} />;
    case 'programming': return <CounterComparison locale={locale} />;
    case 'dom-updates': return <CounterComparison locale={locale} inspect />;
    case 'clock': return <Clock locale={locale} />;
    case 'hello': return <HelloResults locale={locale} />;
    default: throw new Error(`Unknown React demo: ${mode}`);
  }
}
for (const element of document.querySelectorAll('[data-react-demo]')) {
  createRoot(element).render(<Demo mode={element.dataset.reactDemo} />);
}
function updateImageLabels() {
  const locale = document.documentElement.lang === 'en' ? 'en' : 'ko';
  for (const element of document.querySelectorAll('[data-react-alt]')) element.alt = window.LECTURE_CONTENT[locale][element.dataset.reactAlt];
}
document.querySelector('[data-web-deck]').addEventListener('webdeck:localechange', updateImageLabels);
updateImageLabels();
