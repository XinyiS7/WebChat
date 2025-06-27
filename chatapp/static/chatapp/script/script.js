const toggle = document.getElementById('modeToggle');
const label = document.getElementById('modeLabel');
const hiddenInput = document.getElementById('selectedMode');

toggle.addEventListener('change', function () {
    if (this.checked) {
        label.textContent = 'Search 模式';
        hiddenInput.value = 'search';
    } else {
        label.textContent = 'Chat 模式';
        hiddenInput.value = 'chat';
    }
});

