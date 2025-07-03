document.addEventListener('DOMContentLoaded', function () {
    const collapseVendas = document.getElementById('collapseVendas');
    const chevron = document.getElementById('chevronVendas');
    if (collapseVendas && chevron) {
        collapseVendas.addEventListener('show.bs.collapse', function () {
            chevron.classList.remove('bi-chevron-right');
            chevron.classList.add('bi-chevron-down');
        });
        collapseVendas.addEventListener('hide.bs.collapse', function () {
            chevron.classList.remove('bi-chevron-down');
            chevron.classList.add('bi-chevron-right');
        });
    }
});