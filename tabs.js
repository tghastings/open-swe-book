// Language tabs for multi-language code examples.
//
// Authoring convention: write 2-5 CONSECUTIVE fenced code blocks in the canonical
// (alphabetical) order go, java, javascript, python, ruby, typescript (any subset, no other blocks between
// them). At page load this script groups such runs into a tabbed widget. On
// print.html (and therefore in the EPUB pipeline, which renders that page) the
// blocks stay stacked in order, so every language remains visible in print.
(() => {
    if (/print[^/]*\.html$/.test(window.location.pathname)) return;

    const LANGS = ['go', 'java', 'javascript', 'python', 'ruby', 'typescript'];
    const NAME = {
        python: 'Python', java: 'Java', javascript: 'JavaScript',
        go: 'Go', ruby: 'Ruby', typescript: 'TypeScript',
    };
    const KEY = 'swebook-lang';

    // Persist ?lang= immediately — even on pages with no tab groups (front
    // page, curriculum) — so a ?lang= link works from anywhere on the site.
    const fromUrl = new URLSearchParams(window.location.search).get('lang');
    if (LANGS.includes(fromUrl)) {
        try { localStorage.setItem(KEY, fromUrl); } catch (e) { /* private mode */ }
    }

    const langOf = (pre) => {
        const code = pre.querySelector(':scope > code');
        if (!code) return null;
        for (const cls of code.classList) {
            if (cls.startsWith('language-')) {
                const l = cls.slice('language-'.length);
                if (LANGS.includes(l)) return l;
            }
        }
        return null;
    };

    // Collect runs of adjacent sibling <pre> blocks with distinct known languages.
    const groups = [];
    document.querySelectorAll('main pre').forEach((pre) => {
        if (pre.dataset.tabbed) return;
        const first = langOf(pre);
        if (!first) return;
        const group = [[first, pre]];
        let el = pre.nextElementSibling;
        while (el && el.tagName === 'PRE') {
            const l = langOf(el);
            if (!l || group.some(([g]) => g === l)) break;
            group.push([l, el]);
            el = el.nextElementSibling;
        }
        group.forEach(([, p]) => { p.dataset.tabbed = '1'; });
        if (group.length >= 2) groups.push(group);
    });

    const widgets = [];
    if (!groups.length) { /* no tab groups; still add line numbers below */ }
    const select = (lang) => {
        try { localStorage.setItem(KEY, lang); } catch (e) { /* private mode */ }
        widgets.forEach(({ tabs, panes }) => {
            const has = panes.some(([l]) => l === lang);
            const show = has ? lang : panes[0][0];
            panes.forEach(([l, p]) => { p.style.display = (l === show) ? '' : 'none'; });
            tabs.forEach(([l, b]) => {
                b.classList.toggle('active', l === show);
                b.setAttribute('aria-selected', l === show ? 'true' : 'false');
                b.tabIndex = (l === show) ? 0 : -1;
            });
        });
    };

    groups.forEach((group) => {
        const wrap = document.createElement('div');
        wrap.className = 'lang-tabs';
        const bar = document.createElement('div');
        bar.className = 'lang-tab-bar';
        group[0][1].parentNode.insertBefore(wrap, group[0][1]);
        wrap.appendChild(bar);
        bar.setAttribute('role', 'tablist');
        bar.setAttribute('aria-label', 'Example language');
        const tabs = [];
        group.forEach(([l, p]) => {
            const b = document.createElement('button');
            b.type = 'button';
            b.textContent = NAME[l] || l;
            b.setAttribute('role', 'tab');
            b.addEventListener('click', () => select(l));
            bar.appendChild(b);
            tabs.push([l, b]);
            p.setAttribute('role', 'tabpanel');
            wrap.appendChild(p);
        });
        bar.addEventListener('keydown', (e) => {
            const i = tabs.findIndex(([, b]) => b === document.activeElement);
            if (i < 0) return;
            let j = null;
            if (e.key === 'ArrowRight') j = (i + 1) % tabs.length;
            else if (e.key === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
            else if (e.key === 'Home') j = 0;
            else if (e.key === 'End') j = tabs.length - 1;
            if (j !== null) {
                e.preventDefault();
                tabs[j][1].focus();
                select(tabs[j][0]);
            }
        });
        widgets.push({ tabs, panes: group });
    });

    let saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) { /* private mode */ }
    select(LANGS.includes(fromUrl) ? fromUrl : (LANGS.includes(saved) ? saved : 'ruby'));


// Line-number gutters for every fenced code block (not mermaid diagrams).
// The gutter is a sibling of <code>, so copy buttons and text selection of
// the code itself stay clean. print.html is excluded by the guard above,
// which also keeps the EPUB pipeline free of number columns.
document.querySelectorAll('main pre:not(.mermaid) > code').forEach((code) => {
    const pre = code.parentElement;
    if (pre.querySelector('.code-ln')) return;
    const text = code.textContent.replace(/\n$/, '');
    const n = text.split('\n').length;
    const gutter = document.createElement('span');
    gutter.className = 'code-ln';
    gutter.setAttribute('aria-hidden', 'true');
    gutter.textContent = Array.from({ length: n }, (_, i) => i + 1).join('\n');
    pre.insertBefore(gutter, code);
    pre.classList.add('has-ln');
});

})();
