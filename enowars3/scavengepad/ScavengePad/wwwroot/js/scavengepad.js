var wsConnection = null;

const selectedOperationContainerApp = new Vue({
    el: '#scavengepadContainer',
    methods: {
        sendOperationUpdate() {
            wsConnection.send(JSON.stringify({
                "ModifyOperationMessage": selectedOperationContainerApp.operation
            }));
        },
        _selectObjective(objective, e) {
            e.stopPropagation();
            e.preventDefault();
            selectObjective(objective);
        },
        _openObjectiveFiles(objective, e) {
            e.stopPropagation();
            e.preventDefault();
            selectObjective(objective);
            selectedOperationContainerApp.fileList = objective.Files.sort((a, b) => (a.Id > b.Id) ? 1 : ((b.Id > a.Id) ? - 1 : 0));
            $('#filesContainer').removeClass('d-none');
            $('#padContainer').addClass('d-none');
        },
        _openOperationFiles(operation, e) {
            e.stopPropagation();
            e.preventDefault();
            //TODO
        }
    },
    data: {
        operation: {
            Files: [],
            Categories: {}
        },
        totalObjectives: 0,
        solvedObjectives: 0,
        archievedPoints: 0,
        totalPoints: 0,
        fileList: [],
        selectedObjective: null
    }
});

const navbarContainerApp = new Vue({
    el: '#scavengepadNavbar',
    methods: {
        selectOperation(operation) {
            selectedOperationContainerApp.operation = operation;
            displayScavengePad();
            updateOperationUI(operation);
        }
    },
    data: {
        operations: [],
        loggedin: false
    }
});

const modifyOperationApp = new Vue({
    el: '#modifyOperationModal',
    methods: {
        clear() {
            modifyOperationApp.operation.Objectives = [];
            addDefaultObjectiveToModifyModal();
        }
    },
    data: {
        operation: {
            Objectives: []
        }
    }
});

function init() {
    $("#loginForm").submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "api/Login",
            dataType: "json",
            data: {
                username: $("#loginFormUsername").val(),
                password: $("#loginFormPassword").val()
            },
            success: function (result) {
                initOperation(result);
                $('#loginContainer').addClass('d-none');
                $('#noOperationChosenContainer').removeClass('d-none');
                $('#filesContainer').addClass('d-none');
                $('#padContainer').addClass('d-none');
                $('#registrationContainer').addClass('d-none');
            }
        });
    });
    $("#registrationForm").submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "api/Registration",
            dataType: "json",
            data: {
                username: $("#registrationFormUsername").val(),
                password1: $("#registrationFormPassword").val(),
                authkey: $("#registrationFormAuthkey").val()
            },
            success: function (result) {
                initOperation(result);
                $('#loginContainer').addClass('d-none');
                $('#noOperationChosenContainer').removeClass('d-none');
                $('#padContainer').addClass('d-none');
                $('#registrationContainer').addClass('d-none');
            }
        });
    });
    $("#objectiveFileUploadForm").submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        if (selectedOperationContainerApp.selectedObjective !== null) {
            formData.append("objectiveId", selectedOperationContainerApp.selectedObjective.Id);
        }
        formData.append("operationId", selectedOperationContainerApp.operation.Id);

        $.ajax({
            type: "POST",
            url: "api/fileupload",
            data: formData,
            success: function (result) {
                console.log("success!");
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
    $('#modifyOperationModal').on('show.bs.modal', function (e) {
        var newObjective = $(e.relatedTarget).data('new-objective');
        if (newObjective !== true) {
            modifyOperationApp.operation = getCurrentOperationFlattened();
            if (modifyOperationApp.operation.Objectives.length === 0) {
                addDefaultObjectiveToModifyModal();
            }
        } else {
            modifyOperationApp.clear();
        }
    });
}

function initOperation(initialInformation) {
    var hostUrl = new URL(location.origin);
    if (hostUrl.protocol === "http:") {
        wsConnection = new WebSocket(`ws://${hostUrl.hostname}:${hostUrl.port}/scavengepadws/`);
    } else {
        wsConnection = new WebSocket(`wss://${hostUrl.hostname}:${hostUrl.port}/scavengepadws/`);
    }
    wsConnection.onopen = function () {
        console.log("onopen");
    };
    wsConnection.onclose = function () {
        console.log("onclose");
    };
    wsConnection.onerror = function (error) {
        console.log('WebSocket Error ' + error);
    };
    wsConnection.onmessage = function (e) {
        var json = JSON.parse(e.data);
        if (json["ModifyOperationMessage"] !== null) {
            handleModifyOperationMessage(json["ModifyOperationMessage"]);
        } else if (json["NotLoggedInMessage"] === true) {
            displayRegistration();
        } else if (json["OperationListMessage"] !== null) {
            navbarContainerApp.loggedin = true;
            handleOperationListUpdate(json["OperationListMessage"]["OperationMessages"], json["OperationListMessage"]["TeamId"]);
        } else {
            console.log('<<< ' + e.data);
        }
    };
}

function updateOperationUI(updatedOperation) {
    if (selectedOperationContainerApp.operation.Id === updatedOperation.Id) {
        var totalPoints = 0;
        var archievedPoints = 0;
        var totalObjectives = 0;
        var solvedObjectives = 0;
        for (var category in updatedOperation.Categories) {
            category = updatedOperation.Categories[category];
            category.forEach(function (objective) {
                totalPoints += objective.Points;
                if (objective.Points >= 0) {
                    totalObjectives += 1;
                    if (objective.Solved) {
                        solvedObjectives += 1;
                        archievedPoints += objective.Points;
                    }
                }

                if (selectedOperationContainerApp.selectedObjective !== null && objective.Id === selectedOperationContainerApp.selectedObjective.Id) {
                    selectedOperationContainerApp.fileList = objective.Files.sort((a, b) => (a.Id > b.Id) ? 1 : ((b.Id > a.Id) ? - 1 : 0));
                }
            });
        }

        selectedOperationContainerApp.operation = updatedOperation;
        selectedOperationContainerApp.totalPoints = totalPoints;
        selectedOperationContainerApp.archievedPoints = archievedPoints;
        selectedOperationContainerApp.totalObjectives = totalObjectives;
        selectedOperationContainerApp.solvedObjectives = solvedObjectives;
        //TODO update operation files
    }
}

function selectObjective(objective) {
    $('#scavengepadContainer').removeClass('d-none');
    $('#filesContainer').addClass('d-none');
    if (selectedOperationContainerApp.selectedObjective === null || objective.Id !== selectedOperationContainerApp.selectedObjective.Id) {
        var iFrameLink = `<iframe class="card" style="width:100%; height:100%; border:0; border-style:solid;" src="PAD_${objective.ObjectivePadSuffix}?both"></iframe>`;
        $('#padContainer').html(iFrameLink);
        selectedOperationContainerApp.selectedObjective = objective;
    }
    $('#filesContainer').addClass('d-none');
    $('#padContainer').removeClass('d-none');
}

function displayLogin() {
    $('#loginContainer').removeClass('d-none');
    $('#noOperationChosenContainer').addClass('d-none');
    $('#filesContainer').addClass('d-none');
    $('#scavengepadContainer').addClass('d-none');
    $('#registrationContainer').addClass('d-none');
    $('#welcomeContainer').addClass('d-none');
}

function displayRegistration() {
    $('#loginContainer').addClass('d-none');
    $('#noOperationChosenContainer').addClass('d-none');
    $('#filesContainer').addClass('d-none');
    $('#scavengepadContainer').addClass('d-none');
    $('#registrationContainer').removeClass('d-none');
    $('#welcomeContainer').addClass('d-none');
}

function displayScavengePad() {
    $('#loginContainer').addClass('d-none');
    $('#registrationContainer').addClass('d-none');
    $('#noOperationChosenContainer').addClass('d-none');
    $('#scavengepadContainer').removeClass('d-none');
    $('#welcomeContainer').addClass('d-none');
}

function handleModifyOperationMessage(operation) {
    updateOperationUI(operation);
    Vue.set(navbarContainerApp.operations, operation.Id, operation);
}

function handleOperationListUpdate(operations, teamId) {
    navbarContainerApp.operations = {};
    selectedOperationContainerApp.teamId = teamId;
    operations.forEach(function (operation) {
        navbarContainerApp.operations[operation.Id] = operation;
    });
}

function handleModifyOperationModalClosed() {
    var operation = {
        Id: modifyOperationApp.operation.Id,
        Title: modifyOperationApp.operation.Title,
        TeamId: selectedOperationContainerApp.teamId,
        Categories: getModifyModalCategories()
    };
    wsConnection.send(JSON.stringify({
        "ModifyOperationMessage": operation
    }));
}

function getModifyModalCategories() {
    var categories = {};
    modifyOperationApp.operation.Objectives.forEach(function (objective) {
        if (objective.Category in categories) {
            categories[objective.Category].push(objective);
        } else {
            categories[objective.Category] = [objective];
        }
    });
    return categories;
}

function getCurrentOperationFlattened() {
    var objectives = [];
    for (var category in selectedOperationContainerApp.operation.Categories) {
        selectedOperationContainerApp.operation.Categories[category].forEach(function (objective) {
            objectives.push(jsonCopy(objective));
        });
    }
    return {
        Title: selectedOperationContainerApp.operation.Title,
        Objectives: objectives,
        Id: selectedOperationContainerApp.operation.Id
    };
}

function addDefaultObjectiveToModifyModal() {
    modifyOperationApp.operation.Objectives.push({ "Solved": false, "TeamId": selectedOperationContainerApp.teamId, "ObjectivePadSuffix": "default" });
}

function jsonCopy(src) {
    return JSON.parse(JSON.stringify(src));
}
