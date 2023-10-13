document.addEventListener('DOMContentLoaded', function () {
    const dropdownElements = document.querySelectorAll('.dropdown');

    dropdownElements.forEach(function (dropdownElement) {
        const selectedOptionsContainer = dropdownElement.querySelector('.selected-options');
        const optionsContainer = dropdownElement.querySelector('.options');
        const arrowElement = dropdownElement.querySelector('.arrow');

        dropdownElement.addEventListener('click', function () {
            if (optionsContainer.style.display === 'block') {
                optionsContainer.style.display = 'none';
                arrowElement.innerHTML = '▽';
            } else {
                optionsContainer.style.display = 'block';
                arrowElement.innerHTML = '△';
            }
        });

        optionsContainer.addEventListener('click', function (e) {
            e.stopPropagation();
            if (e.target.classList.contains('option')) {
                const value = e.target.dataset.value;
                const label = e.target.textContent.trim();


                const previousOption = selectedOptionsContainer.querySelector('.selected-option');
                if (previousOption) {
                    previousOption.remove();
                }

                const optionDiv = document.createElement('div');
                optionDiv.className = 'selected-option';
                optionDiv.dataset.value = value;
                optionDiv.textContent = label;
                selectedOptionsContainer.appendChild(optionDiv);

                optionsContainer.style.display = 'none';
                arrowElement.innerHTML = '▽';

            }
        });

        document.addEventListener('click', function (e) {
            if (!dropdownElement.contains(e.target)) {
                optionsContainer.style.display = 'none';
                arrowElement.innerHTML = '▽';
            }
        });
    });
});
