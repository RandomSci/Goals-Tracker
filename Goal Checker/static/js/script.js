document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';

    // Set the current theme on load
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        themeToggleButton.textContent = '☀️'; // Sun icon for light mode
    }

    // Toggle theme on button click
    themeToggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        
        // Toggle the button icon
        if (document.body.classList.contains('dark-mode')) {
            themeToggleButton.textContent = '☀️'; // Sun icon
            localStorage.setItem('theme', 'dark');
        } else {
            themeToggleButton.textContent = '🌙'; // Moon icon
            localStorage.setItem('theme', 'light');
        }
    });
});
