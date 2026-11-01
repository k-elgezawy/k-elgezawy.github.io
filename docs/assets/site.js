(()=>{'use strict';
const root=document.documentElement;
const getPref=k=>{try{return localStorage.getItem(k)}catch{return null}};
const setPref=(k,v)=>{try{localStorage.setItem(k,v)}catch{}};
let lang=getPref('karim-language')==='en'?'en':'ar';
const langButton=document.getElementById('language-toggle');
const themeButton=document.getElementById('theme-toggle');
const setLanguage=value=>{
 lang=value;root.lang=lang;root.dir=lang==='ar'?'rtl':'ltr';setPref('karim-language',lang);
 document.querySelectorAll('[data-ar][data-en]').forEach(el=>el.textContent=el.dataset[lang]);
 document.querySelectorAll('[data-placeholder-ar]').forEach(el=>el.placeholder=el.dataset['placeholder'+(lang==='ar'?'Ar':'En')]);
 document.querySelectorAll('[data-label-ar]').forEach(el=>el.setAttribute('aria-label',el.dataset['label'+(lang==='ar'?'Ar':'En')]));
 if(langButton){langButton.textContent=lang==='ar'?'English':'العربية';langButton.setAttribute('aria-label',lang==='ar'?'Switch to English':'التبديل للعربية')}
 if(root.dataset.titleAr&&root.dataset.titleEn)document.title=root.dataset[lang==='ar'?'titleAr':'titleEn'];
 filterArticles();
};
const normalize=s=>s.toLocaleLowerCase().normalize('NFKD').replace(/[\u064b-\u065f\u0670]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي');
const articleSearch=document.getElementById('article-search'),articleCategory=document.getElementById('article-category');
function filterArticles(){let count=0;const q=normalize(articleSearch?.value||''),cat=articleCategory?.value||'all';document.querySelectorAll('.article-card[data-search]').forEach(card=>{const matches=normalize(card.dataset.search).includes(q)&&(cat==='all'||card.dataset.category===cat);card.hidden=!matches;if(matches)count++});const empty=document.getElementById('articles-empty');if(empty)empty.hidden=count!==0;const total=document.getElementById('article-result-count');if(total)total.textContent=lang==='ar'?`${count} مقال`:`${count} articles`}
langButton?.addEventListener('click',()=>setLanguage(lang==='ar'?'en':'ar'));
const changeTheme=t=>{root.dataset.theme=t;setPref('karim-theme',t);if(themeButton){themeButton.textContent=t==='dark'?'☀':'☾';themeButton.setAttribute('aria-pressed',String(t==='light'))}};
themeButton?.addEventListener('click',()=>changeTheme(root.dataset.theme==='light'?'dark':'light'));
document.querySelectorAll('[data-project-filter]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-project-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('.project[data-category]').forEach(card=>card.hidden=button.dataset.projectFilter!=='all'&&card.dataset.category!==button.dataset.projectFilter)}));
articleSearch?.addEventListener('input',filterArticles);articleCategory?.addEventListener('change',filterArticles);
changeTheme(getPref('karim-theme')==='light'?'light':'dark');setLanguage(lang);
})();
