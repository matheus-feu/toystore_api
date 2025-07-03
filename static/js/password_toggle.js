$(document).ready(function () {
    $('input[type="password"]').each(function () {
        var $input = $(this);
        var $inputGroup = $input.closest('.input-group');
        var $toggleBtn = $('<button type="button" class="btn btn-outline-secondary toggle-password" tabindex="-1"><i class="fa-solid fa-eye"></i></button>');
        $inputGroup.append($toggleBtn);

        $toggleBtn.on('click', function () {
            const isPassword = $input.attr('type') === 'password';
            $input.attr('type', isPassword ? 'text' : 'password');
            $(this).find('i').toggleClass('fa-eye').toggleClass('fa-eye-slash');
        });
    });
});