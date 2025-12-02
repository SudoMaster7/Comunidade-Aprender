const themeToggle = document.getElementById('theme-toggle');
const htmlElement = document.documentElement;
const icon = themeToggle.querySelector('i');

// Check for saved theme preference, otherwise use system preference
const getPreferredTheme = () => {
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme) {
        return storedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

const setTheme = (theme) => {
    if (theme === 'light') {
        htmlElement.setAttribute('data-theme', 'light');
        icon.classList.remove('bi-moon-fill');
        icon.classList.add('bi-sun-fill');
    } else {
        htmlElement.removeAttribute('data-theme'); // Default is dark
        icon.classList.remove('bi-sun-fill');
        icon.classList.add('bi-moon-fill');
    }
    localStorage.setItem('theme', theme);
};

// Initialize
setTheme(getPreferredTheme());

// Toggle event
themeToggle.addEventListener('click', () => {
    const currentTheme = htmlElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
});
