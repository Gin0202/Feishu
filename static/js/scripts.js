document.addEventListener('DOMContentLoaded', function() {
    const tokenSettingForm = document.querySelector('#tokenSetting form');
    const dropdownSettingForm = document.querySelector('#dropdownSetting');
    const customDropdownContainer = document.querySelector('.custom-dropdown-container');
    const loadingDiv = document.getElementById('loading');
    const submitButton = document.getElementById('tokenSubmitButton');
    const progressStatus = document.getElementById('progressStatus');

    let appToken = null;
    let personalBaseToken = null;
    let tableId = null;

    // First form's submit listener
    tokenSettingForm.addEventListener('submit', function(e) {
        e.preventDefault();

        loadingDiv.innerText = '加载中，请等待...';
        loadingDiv.style.display = 'block';
        submitButton.disabled = true;

        const formData = new FormData(tokenSettingForm);

        fetch('/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingDiv.innerText = '加载完成';  // 修改此处
        setTimeout(() => {  // 添加此段代码
            loadingDiv.style.display = 'none';
        }, 3000);
            submitButton.disabled = false;

            if (data.success) {
                appToken = formData.get('appToken');
                personalBaseToken = formData.get('personalBaseToken');
                tableId = formData.get('tableId');

                const optionsContainer = document.querySelector('.options');
                if (optionsContainer) {
                    optionsContainer.innerHTML = '';
                    data.options.forEach(option => {
                        const optionDiv = document.createElement('div');
                        optionDiv.className = 'option';
                        optionDiv.dataset.value = option;
                        optionDiv.textContent = option;
                        optionsContainer.appendChild(optionDiv);
                    });
                    customDropdownContainer.style.display = 'block';
                }
            } else {
                alert(data.message || 'Error occurred.');
            }
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            submitButton.disabled = false;
            console.error('There was an error!', error);
        });
    });

    // Second form's submit listener
    dropdownSettingForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const selectedValue = document.querySelector('.selected-option') ? document.querySelector('.selected-option').dataset.value : null;

        if (!selectedValue) {
            alert('请从下拉菜单中选择一个选项。');
            return;
        }

        loadingDiv.innerText = '时间戳转换中...';
        loadingDiv.style.display = 'block';

        const postData = new FormData();
        postData.append('selected_value', selectedValue);
        postData.append('appToken', appToken);
        postData.append('personalBaseToken', personalBaseToken);
        postData.append('tableId', tableId);

        fetch(`/confirm_logic`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: postData
        })
        .then(response => response.text())
        .then(data => {
            loadingDiv.innerText = '转换完成';
            setTimeout(() => {
                loadingDiv.style.display = 'none';
            }, 3000);  // 3秒后隐藏消息
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            console.error('There was an error!', error);
        });
    });

    // Dropdown interactions
    const dropdownElements = document.querySelectorAll('.dropdown');
    dropdownElements.forEach(function(dropdownElement) {
        const selectedOptionsContainer = dropdownElement.querySelector('.selected-options');
        const optionsContainer = dropdownElement.querySelector('.options');

        if (!optionsContainer) return;

        const arrowElement = dropdownElement.querySelector('.arrow');

        dropdownElement.addEventListener('click', function() {
            if (optionsContainer.style.display === 'block') {
                optionsContainer.style.display = 'none';
                arrowElement.innerHTML = '▽';
            } else {
                optionsContainer.style.display = 'block';
                arrowElement.innerHTML = '△';
            }
        });

        optionsContainer.addEventListener('click', function(e) {
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

        document.addEventListener('click', function(e) {
            if (!dropdownElement.contains(e.target)) {
                optionsContainer.style.display = 'none';
                arrowElement.innerHTML = '▽';
            }
        });
    });
});
