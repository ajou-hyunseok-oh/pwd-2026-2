import React, { useEffect, useId, useState } from 'react';
import { createRoot } from 'react-dom/client';

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
    update();
    return () => deck.removeEventListener('webdeck:localechange', update);
  }, []);
  return locale;
}
function ProductRow({ product, locale }) {
  return <div className={`react-product-row ${product.stocked ? '' : 'is-unavailable'}`} data-product={product.id} data-component={product.id === 'apple' ? 'ProductRow ×6' : undefined}>
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
  const [showBounds, setShowBounds] = useState(boundaries);
  useEffect(() => { setQuery(queryPreset ? (locale === 'ko' ? '사과' : 'Apple') : ''); setStockOnly(stock); }, [locale, stock, queryPreset]);
  const products = PRODUCTS.filter(p => (!stockOnly || p.stocked) && p[locale].toLowerCase().includes(query.trim().toLowerCase()));
  return <div className={`react-product-app ${showBounds ? 'show-boundaries' : ''} ${reuse ? 'show-reuse' : ''}`}>
    <div className="react-app-title"><strong>{boundaries && showBounds ? `ProductApp · ${locale === 'ko' ? '상품 검색' : 'Product Search'}` : (locale === 'ko' ? '상품 검색' : 'Product Search')}</strong>{boundaries && <button className="react-demo-button" aria-pressed={showBounds} onKeyDown={e => e.stopPropagation()} onClick={() => setShowBounds(!showBounds)}>{locale === 'ko' ? (showBounds ? '경계 숨기기' : '컴포넌트 경계') : (showBounds ? 'Hide boundaries' : 'Component boundaries')}</button>}</div>
    <SearchBar {...{locale,query,setQuery,stockOnly,setStockOnly,editable}} />
    <ProductTable products={products} locale={locale} />
  </div>;
}
function FilterComparison({ locale }) {
  const ko = locale === 'ko';
  return <>
    <div className="react-comparison">
      <div><h3>{ko ? '선택 전 · 전체 6개' : 'Before · All 6 Products'}</h3><ProductApp locale={locale} /></div>
      <div><h3>{ko ? '재고 조건 선택 · 초기 결과 4개' : 'In Stock Only · Initially 4 Results'}</h3><ProductApp locale={locale} stock editable /></div>
    </div>

  </>;
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
