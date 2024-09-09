function openApp(appValue) {
    const url = '/open-app';

    const data = {
        app: appValue
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.redirect_path) {
                window.open(data.redirect_path);
            } else {
                // Handle the case where the redirect path is missing
                console.error('No redirect path found in response');
                alert('No redirect path found');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error sending POST request');
        });
}

function getCurrentFormattedDateTime() {
    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
    const day = String(now.getDate()).padStart(2, '0');

    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    return `${hours}:${minutes}:${seconds}, ${day}-${month}-${year}`;
}

function displayErrorToast(title, message) {
    const toastHTML = `
        <div class="toast-header">
            <svg class="rounded me-2 text-danger" width="2em" height="2em" fill="currentColor">
                <use xlink:href="/assets/bootstrap/icons/bootstrap-icons.svg#bell-fill"></use>
            </svg>
          <strong class="me-auto">${title}</strong>
          <small>${getCurrentFormattedDateTime()}</small>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          ${message}
        </div>
    `;
    // Inject the toast into the container
    const errorToast = document.getElementById('errorToast');
    errorToast.innerHTML = toastHTML;

    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(errorToast)
    toastBootstrap.show();
}

function displayAbout() {
    fetch('get-about')  // Change the URL to your server endpoint
        .then(response => response.json())
        .then(data => {
            const tabPane = document.createElement('div');
            tabPane.id = 'tabPane';
            tabPane.style.padding = '10px';
            tabPane.style.fontSize = "12px";

            const ulTabs = document.createElement('ul');
            ulTabs.className = 'nav nav-tabs';
            ulTabs.id = 'aboutTabs';
            ulTabs.role = "tablist"

            tabPane.appendChild(ulTabs);

            data.forEach(tab => {
                const li = document.createElement('li');
                li.className = 'nav-item';
                li.setAttribute('role', 'presentation');

                const button = document.createElement('button');
                button.className = `nav-link ${tab.selected ? 'active' : ''}`;
                button.id = tab.tab_id + '-tab';
                button.setAttribute('data-bs-toggle', 'tab');
                button.setAttribute('data-bs-target', '#' + tab.tab_id);
                button.dataset.tab_id = tab.tab_id;
                button.type = 'button';
                button.setAttribute('role', 'tab');
                button.setAttribute('aria-controls', ('#' + tab.tab_id).substring(1));
                button.setAttribute('aria-selected', tab.selected);

                button.textContent = tab.tab_title;

                li.appendChild(button);
                ulTabs.appendChild(li);
            });

            const tabContent = document.createElement('div');
            tabContent.id = 'tabContent';
            tabContent.style.paddingRight = '10px';
            tabContent.className = 'tab-content mt-3';

            tabPane.appendChild(tabContent)

            data.forEach(tab => {
                const div = document.createElement('div');
                if (tab.selected) {
                    div.className = 'tab-pane fade show active';
                } else {
                    div.className = 'tab-pane fade';
                }
                div.id = tab.tab_id;
                div.role = 'tabpanel';
                div.ariaLabel = tab.tab_id

                const strong = document.createElement('strong');
                strong.innerHTML = tab.tab_title
                strong.className = 'mb-1';
                const br = document.createElement('br');
                const small = document.createElement('small');
                small.innerHTML = 'Version: ' + tab.version;

                const tabContentArea = document.createElement('div');
                tabContentArea.id = tab.tab_id + '-tabContentArea';

                const p = document.createElement('p');
                p.innerHTML = tab.description;
                tabContentArea.appendChild(p)
                if (tab.copyright) {
                    const p2 = document.createElement('p');
                    p2.innerHTML = tab.copyright;
                    p2.style.fontSize = "12px";
                    p2.className = "text-center";
                    tabContentArea.appendChild(br)
                    tabContentArea.appendChild(p2)
                }
                const hr = document.createElement('hr');
                div.appendChild(strong);
                div.appendChild(br);
                div.appendChild(small);
                div.appendChild(hr);
                div.appendChild(tabContentArea);
                tabContent.appendChild(div);
            });

            document.getElementById('aboutBody').innerHTML = tabPane.innerHTML;
        })
        .catch(error => {
            displayErrorToast('Error Loading About', error);
        });
}

function getIcon(icon, width, height, classes) {
    const svg = document.createElement('svg');
    svg.className = classes;
    svg.setAttribute("width", width);   // Set the width to 50 units (pixels by default)
    svg.setAttribute("height", height);  // Set the height to 50 units
    svg.setAttribute("fill", "currentColor");
    const useElement = document.createElement("use");
    const hrefValue = "/assets/bootstrap/icons/bootstrap-icons.svg#" + icon;
    useElement.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", hrefValue);
    svg.appendChild(useElement)
    return svg;
}

function loadSecretsList(count, secretsList, store, scope) {
    if (store.available) {
        store.index.forEach(secret => {
            console.log(scope);
            count += 1;
            const secretLi = document.createElement('li');
            secretLi.className = 'list-group-item d-flex justify-content-between align-items-center';
            const secretSpan = document.createElement('span');
            if (scope === 'App_Local_Store') {
                secretSpan.appendChild(getIcon('people', '1em', '1em', 'bi me-2'));
            } else {
                secretSpan.appendChild(getIcon('person', '1em', '1em', 'bi me-2'));
            }

            const secretLabel = document.createElement('span');
            secretLabel.textContent = secret;
            secretSpan.appendChild(secretLabel);
            const secretButtonSpan = document.createElement('span');

            if (!store.read_only) {
                const secretChangeButtonSpan = document.createElement('button');
                secretChangeButtonSpan.className = 'btn btn-primary btn-sm mr-2';
                secretChangeButtonSpan.textContent = 'Change';
                secretChangeButtonSpan.setAttribute('data-secret-action', 'Change');
                secretChangeButtonSpan.setAttribute('data-secret-key', secret);
                secretChangeButtonSpan.setAttribute('data-secret-scope', scope);


                const secretDeleteButtonSpan = document.createElement('button');
                secretDeleteButtonSpan.className = 'btn btn-danger btn-sm';
                secretDeleteButtonSpan.textContent = 'Delete';
                secretDeleteButtonSpan.setAttribute('data-secret-action', 'Delete');
                secretDeleteButtonSpan.setAttribute('data-secret-key', secret);
                secretDeleteButtonSpan.setAttribute('data-secret-scope', scope);

                const spacer = document.createElement('span')
                spacer.style.paddingRight = "10px";
                secretButtonSpan.appendChild(secretChangeButtonSpan);
                secretButtonSpan.appendChild(spacer);
                secretButtonSpan.appendChild(secretDeleteButtonSpan);
            }
            secretLi.appendChild(secretSpan);
            secretLi.appendChild(secretButtonSpan);
            secretsList.appendChild(secretLi);
        });
    }
    return count
}

function loadSecretsTab(data, ulTabs, tabPane) {
    const secretsLi = document.createElement('li');
    secretsLi.className = 'nav-item';
    secretsLi.setAttribute('role', 'presentation');

    const secretsButton = document.createElement('button');
    secretsButton.className = `nav-link active`;
    secretsButton.id = 'secretsTab';
    secretsButton.setAttribute('data-bs-toggle', 'tab');
    secretsButton.setAttribute('data-bs-target', '#secrets');
    secretsButton.type = 'button';
    secretsButton.setAttribute('role', 'tab');
    secretsButton.setAttribute('aria-controls', ('#secrets').substring(1));
    secretsButton.setAttribute('aria-selected', 'true');

    secretsButton.textContent = "Secrets Manager";

    secretsLi.appendChild(secretsButton);
    ulTabs.appendChild(secretsLi);

    const tabContent = document.createElement('div');
    tabContent.id = 'tabContent';
    tabContent.style.paddingRight = '10px';
    tabContent.className = 'tab-content mt-3';

    tabPane.appendChild(tabContent)

    const secretsDiv = document.createElement('div');
    secretsDiv.className = 'tab-pane fade show active';
    secretsDiv.id = 'secrets';
    secretsDiv.role = 'tabpanel';
    secretsDiv.ariaLabel = 'secrets'

    const secretsNav = document.createElement('nav');
    secretsNav.className = 'navbar bg-body-tertiary';
    const secretsToolbarDiv = document.createElement('div');
    secretsToolbarDiv.className = 'container-fluid justify-content-start';
    const addSecretButton = document.createElement('button');
    addSecretButton.className = 'btn btn-sm btn-outline-primary me-2';
    addSecretButton.id = 'addSecretButton';
    addSecretButton.textContent = 'Add Secret'

    const clearAllSecretButton = document.createElement('button');
    clearAllSecretButton.className = 'btn btn-sm btn-outline-warning';
    clearAllSecretButton.textContent = 'Clear All Secrets';
    clearAllSecretButton.id = 'clearAllSecretButton';
    secretsToolbarDiv.appendChild(addSecretButton);
    secretsToolbarDiv.appendChild(clearAllSecretButton);
    secretsNav.appendChild(secretsToolbarDiv);

    secretsDiv.appendChild(secretsNav);
    secretsDiv.appendChild(document.createElement('hr'));

    const secretsContainer = document.createElement('div');
    secretsContainer.className = 'container mt-4';
    let secretsList = document.createElement('ul');
    secretsList.className = 'list-group';
    let count = 0
    count += loadSecretsList(count, secretsList, data.secrets.App_Local_Store, 'App_Local_Store');
    count += loadSecretsList(count, secretsList, data.secrets.User_Local_Store, 'User_Local_Store');

    if (count > 0) {
        secretsContainer.appendChild(secretsList);
    } else {
        const noSecretsLabel = document.createElement('strong');
        noSecretsLabel.innerText = "No Secrets have been defined."
        secretsContainer.appendChild(noSecretsLabel);
    }

    secretsDiv.appendChild(secretsContainer);
    tabContent.appendChild(secretsDiv);
}

function loadSettingTab(data, title, ulTabs, tabPane, scope) {
    const settingsLi = document.createElement('li');
    settingsLi.className = 'nav-item';
    settingsLi.id = scope + 'TabLi';
    settingsLi.setAttribute('role', 'presentation');

    const settingsButton = document.createElement('button');
    settingsButton.className = `nav-link`;
    settingsButton.id = scope + 'Tab';
    settingsButton.setAttribute('data-bs-toggle', 'tab');
    settingsButton.setAttribute('data-bs-target', '#' + scope);
    settingsButton.type = 'button';
    settingsButton.setAttribute('role', 'tab');
    settingsButton.setAttribute('aria-controls', ('#' + scope).substring(1));
    settingsButton.setAttribute('aria-selected', 'false');

    settingsButton.textContent = title;

    settingsLi.appendChild(settingsButton);
    ulTabs.appendChild(settingsLi);

    const tabContent = document.createElement('div');
    tabContent.id = 'tabContent' + scope;
    tabContent.style.paddingRight = '10px';
    tabContent.className = 'tab-content mt-3';

    tabPane.appendChild(tabContent)

    const settingsDiv = document.createElement('div');
    settingsDiv.className = 'tab-pane fade show';
    settingsDiv.id = scope;
    settingsDiv.role = 'tabpanel';
    settingsDiv.ariaLabel = scope

    const settingsNav = document.createElement('nav');
    settingsNav.className = 'navbar bg-body-tertiary';
    const settingsToolbarDiv = document.createElement('div');
    settingsToolbarDiv.className = 'container-fluid justify-content-start';
    const settingsApplyButton = document.createElement('button');
    settingsApplyButton.className = 'btn btn-sm btn-outline-primary me-2';
    settingsApplyButton.id = 'settingsApplyButton' + scope;
    settingsApplyButton.textContent = 'Apply Settings'
    settingsApplyButton.setAttribute('textarea-target', 'codeEditor' + scope)
    settingsApplyButton.setAttribute('textarea-scope', scope)

    settingsToolbarDiv.appendChild(settingsApplyButton);
    settingsNav.appendChild(settingsToolbarDiv);

    settingsDiv.appendChild(settingsNav);
    settingsDiv.appendChild(document.createElement('hr'));

    const settingsContainer = document.createElement('div');
    settingsContainer.className = 'container mt-4';
    settingsContainer.style.height = '100%';
    settingsContainer.style.width = '100%';

    const codeEditor = document.createElement('textarea');
    codeEditor.id = 'codeEditor' + scope;
    codeEditor.style.width = "100%";
    codeEditor.style.height = "500px";
    codeEditor.className = "CodeEditor";
    codeEditor.style.fontFamily = 'Courier, monospace';
    codeEditor.style.whiteSpace = 'pre';
    codeEditor.style.overflowWrap = 'normal';
    codeEditor.style.wordWrap = 'normal';
    codeEditor.style.resize = 'none';

    codeEditor.textContent = data.raw_data;
    settingsContainer.appendChild(codeEditor);

    settingsDiv.appendChild(settingsContainer);
    tabContent.appendChild(settingsDiv);

    if (data.read_only) {
        settingsApplyButton.disabled = true;
        codeEditor.disabled = true;
        const readOnlyLabel = document.createElement('span');
        readOnlyLabel.textContent = 'These Settings are Read-Only and can not be Modified.';
        settingsToolbarDiv.appendChild(readOnlyLabel);
    }
}

function loadSettingsTabs(data, ulTabs, tabPane) {
    loadSettingTab(data.settings.current_user, 'User Settings', ulTabs, tabPane, 'current_user');
    loadSettingTab(data.settings.all_user, 'All Users Settings', ulTabs, tabPane, 'all_user');
    loadSettingTab(data.settings.app, 'Application Settings', ulTabs, tabPane, 'app');
}


function loadDisplaySettings() {
    document.getElementById('settingsBody').innerHTML = '';
    fetch('/get-settings')  // Change the URL to your server endpoint
        .then(response => response.json())
        .then(data => {
            const tabPane = document.createElement('div');
            tabPane.id = 'settingsTabPane';
            tabPane.style.padding = '10px';
            tabPane.style.fontSize = "12px";

            const ulTabs = document.createElement('ul');
            ulTabs.className = 'nav nav-tabs';
            ulTabs.id = 'settingsTabs';
            ulTabs.role = "tablist"

            tabPane.appendChild(ulTabs);
            loadSecretsTab(data, ulTabs, tabPane);
            loadSettingsTabs(data, ulTabs, tabPane);
            document.getElementById('settingsBody').innerHTML = tabPane.innerHTML;
            loadSettingsListeners(data);
            $('#settingsModal').modal('show');

        })
        .catch(error => {
            displayErrorToast('Error Loading Settings Page', error);
        });
}

function addSecret() {
    let formData = {};
    formData['currentUser'] = document.getElementById('currentUser').checked
    formData['allUsers'] = document.getElementById('allUsers').checked
    formData['secretName'] = document.getElementById('secretName').value
    formData['secretValue'] = document.getElementById('secretValue').value

    fetch('/add-secret', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.state === 'error') {
            displayErrorToast('Error Adding New Secret', data.msg)
        }
        loadDisplaySettings();
    })
    .catch((error) => {
        displayErrorToast('Error Adding New Secret', error)
    });
}

function clearSecrets(key, scope) {
    let formData = {};
    formData['key'] = key;
    formData['scope'] = scope;

    fetch('/clear-secrets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.state === 'error') {
            displayErrorToast('Error Clearing Secrets', data.msg)
        }
        loadDisplaySettings();
    })
    .catch((error) => {
        displayErrorToast('Error Clearing Secrets', error)
    });
}

function showAddChangeSecret(key, scope, data) {
    document.getElementById('new-secret-form').reset();
    $('#settingsModal').modal('hide');
    if (key === null) {
        document.getElementById('newSecretModalLabel').textContent = 'Add New Secret';
        document.getElementById('currentUser').disabled  = !data.secrets.User_Local_Store.available;
        document.getElementById('allUsers').disabled  = !data.secrets.App_Local_Store.available;
        document.getElementById('secretName').disabled  = false;
    } else {
        document.getElementById('newSecretModalLabel').textContent = 'Change Secret';
        document.getElementById('currentUser').disabled  = true;
        document.getElementById('allUsers').disabled  = true;
        if (scope === 'User_Local_Store') {
            document.getElementById('currentUser').checked  = true;
        } else {
            document.getElementById('allUsers').checked  = true;
        }
        document.getElementById('secretName').disabled  = true;
        document.getElementById('secretName').value = key;
    }
    $('#newSecretModal').modal('show');
}

function loadSettingsListeners(data) {

    document.getElementById('addSecretButton').addEventListener('click', () => {
        showAddChangeSecret(null, null, data);
    });

    // Cancel Adding New Secret
    document.getElementById('cancelAddSecret').addEventListener('click', () => {
        $('#newSecretModal').modal('hide');
        loadDisplaySettings();
    });

    document.getElementById('new-secret-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way
        $('#newSecretModal').modal('hide');
        addSecret()
    });

    document.getElementById('clearAllSecretButton').addEventListener('click', () => {
        clearDeleteSecrets(null, null);
    });

    let buttons = document.querySelectorAll('button[data-secret-action]');
    buttons.forEach(button => {
        button.addEventListener('click', (event) => {
            let action = button.getAttribute('data-secret-action');
            let key = button.getAttribute('data-secret-key');
            let scope = button.getAttribute('data-secret-scope');
            secretAction(action, key, scope);
        });
    });

    let applySettingsButtons = document.querySelectorAll('button[textarea-target]');
    applySettingsButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            let textareaId = button.getAttribute('textarea-target');
            let scope = button.getAttribute('textarea-scope');
            persistSettings(textareaId, scope);
        });
    });
}

function persistSettings(textareaId, scope) {
    const content = document.getElementById(textareaId).value;
    let formData = {};
    formData['content'] = content;
    formData['scope'] = scope;

    fetch('/persist-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.state === 'error') {
            displayErrorToast('Error Persisting Settings', data.msg)
        }
        loadDisplaySettings();
    })
    .catch((error) => {
        displayErrorToast('Error Persisting Settings', error)
    });
}

function clearDeleteSecrets(key, scope) {

    document.getElementById('dontClearSecrets').addEventListener('click', () => {
        $('#clearAllSecretModal').modal('hide');
        $('#settingsModal').modal('show');
    });

    document.getElementById('clearSecrets').addEventListener('click', () => {
        $('#clearAllSecretModal').modal('hide');
        clearSecrets(key, scope);
    });

    if (key === null) {
        document.getElementById('clearAllSecretModalLabel').textContent = 'Clear All Secrets';
        document.getElementById('clearSecrets').textContent = 'Clear All Secrets';
    } else {
        document.getElementById('clearAllSecretModalLabel').textContent = 'Clear "' + key + '"';
        document.getElementById('clearSecrets').textContent = 'Clear "' + key + '"';
    }

    $('#settingsModal').modal('hide');
    $('#clearAllSecretModal').modal('show');
}

function changeSecret(key, scope) {
    showAddChangeSecret(key, scope);
}

function deleteSecret(key, scope) {
    clearDeleteSecrets(key, scope)
}

function secretAction(action, key, scope) {
    if (action === 'Change') {
        changeSecret(key, scope);
    }

    if (action === 'Delete') {
        deleteSecret(key, scope);
    }
}

function displaySettings() {
    loadDisplaySettings();
}