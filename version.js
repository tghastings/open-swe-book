// Build-version line at the bottom of the sidebar index. VERSION is
// overwritten at deploy time by CI (git describe --tags with the leading "v"
// stripped, i.e. the v1.0bN beta tag scheme plus commit distance for untagged
// builds); the "1.0b1" default appears only in local previews.
// The print icon leads to the per-language PDF/EPUB downloads instead of
// print.html: a printout should come from a single-language edition, not the
// all-languages print page.
(() => {
    const el = document.getElementById('print-button');
    const btn = el && (el.tagName === 'A' ? el : el.closest('a'));
    if (btn) {
        btn.href = 'https://github.com/tghastings/open-swe-book/releases/latest';
        btn.title = 'Download a PDF or EPUB edition (per language)';
        btn.removeAttribute('target');
    }
})();

// Sidebar numbering: show the team-project appendix as "A." (and any further
// appendices as "B.", "C.", …) instead of a chapter number, and drop the number
// from suffix entries after it (curriculum, contributing), so the sidebar reads
// as "chapters + appendix" no matter how many chapters precede it. Matches the
// appendix by title rather than a fixed position, so adding a chapter never
// misnumbers it.
(() => {
    let past = false;
    document.querySelectorAll('#sidebar ol.chapter > li.chapter-item > a')
        .forEach((a) => {
            const st = a.querySelector(':scope > strong');
            if (!st) return;
            const m = (a.textContent || '').match(/\bAppendix\s+([A-Z])\b/);
            if (m) { st.textContent = m[1] + '.'; past = true; }
            else if (past) { st.textContent = ''; }
        });
})();

(() => {
    const VERSION = "1.0b1";
    const box = document.querySelector('#sidebar .sidebar-scrollbox');
    if (!box) return;
    const div = document.createElement('div');
    div.className = 'site-version';
    const link = document.createElement('a');
    link.href = 'https://github.com/tghastings/open-swe-book/releases';
    link.textContent = VERSION;
    link.title = 'Release history';
    div.append('First Edition · ');
    div.appendChild(link);
    box.appendChild(div);
})();
